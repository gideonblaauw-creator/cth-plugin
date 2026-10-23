#!/usr/bin/env python3
"""Apply approved 04 REIN chapter markdown to existing Docmost pages (by title).

Chapter source files live outside git (default ~/oa/rein-chapters/). Idempotent:
re-applying unchanged content is a no-op. Does not upload attachments, change shares,
or send invites. Keeps searchIndexing off on writes.

Chapters 02, 06, 09 and 05x: titles and dates only (body stripped).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from http.cookiejar import CookieJar
from pathlib import Path
from typing import Any

API_BASE = os.environ.get("NCUK_DOCMOST_API", "http://127.0.0.1:3076/api")
SPACE_ID = "01a16500-098f-7bcb-be4b-74d17b66280f"
REIN_ROOT_ID = "01a16500-0da7-7e62-9bd0-44110d202164"
REIN_ROOT_TITLE = "04 REIN"
DEFAULT_CHAPTERS_DIR = Path("/home/debian/oa/rein-chapters")
DEFAULT_TREE_BACKUP = Path("/home/debian/oa/ncuk-tree-before-task-o.json")
AUTOMATION_EMAIL_KEY = "NCUK_DOCMOST_AUTOMATION_EMAIL"
AUTOMATION_PASSWORD_KEY = "NCUK_DOCMOST_AUTOMATION_PASSWORD"
DEFAULT_AUTOMATION_EMAIL = "admin@cleantechhub.net"

TITLES_ONLY_CHAPTER_KEYS = frozenset({"02", "06", "09", "05x"})

CHAPTER_FILES: tuple[str, ...] = (
    "01_e1f8.md",
    "02_37fb.md",
    "03_bef6.md",
    "03-colombia_f2e6.md",
    "03-peru_bafb.md",
    "03-guatemala_4616.md",
    "03-costa-rica_cf21.md",
    "03-el-salvador_405f.md",
    "04_30ea.md",
    "05_5f6d.md",
    "05x_0367.md",
    "06_e0db.md",
    "07_34bb.md",
    "08_f41c.md",
    "09_74c3.md",
)

# Map chapter H1 (from markdown) to leaf title path under 04 REIN (excluding root).
H1_TO_PATH: dict[str, tuple[str, ...]] = {
    "01 Overview & governance": ("01 Overview & governance",),
    "02 Agreements": ("02 Agreements",),
    "03 Hubs": ("03 Hubs",),
    "03 Hubs › Colombia (Externado)": ("03 Hubs", "Colombia · Externado"),
    "03 Hubs › Peru": ("03 Hubs", "Peru · Universidad del Pacífico"),
    "03 Hubs › Guatemala (Landívar)": ("03 Hubs", "Guatemala · Rafael Landívar"),
    "03 Hubs › Costa Rica (Véritas)": ("03 Hubs", "Costa Rica · LCI Veritas"),
    "03 Hubs › El Salvador (UTEC)": ("03 Hubs", "El Salvador · UTEC"),
    "04 Programme design": ("04 Programme design",),
    "05 Reports & results": ("05 Reports & results",),
    "05 Reports & results › 05x Performance reports (internal)": (
        "05 Reports & results",
        "05x Performance reports (internal)",
    ),
    "06 Finance": ("06 Finance",),
    "07 Media & brand": ("07 Media & brand",),
    "08 Partners & funders": ("08 Partners & funders",),
    "09 Pipeline & proposals": ("09 Pipeline",),
}

# For titles-only tables: keep these column headers (case-insensitive match).
TABLE_KEEP_COLUMNS: dict[str, tuple[str, ...]] = {
    "02": ("Agreement", "Signed date"),
    "06": ("Item", "Year"),
    "09": ("Opportunity", "Deadline"),
    "05x": ("Report", "Period"),
}


@dataclass(frozen=True)
class PageRef:
    path: tuple[str, ...]
    page_id: str | None
    title: str


@dataclass
class PlanRow:
    page_label: str
    action: str
    chars: int
    detail: str = ""


def read_infisical_token() -> str:
    token_path = "/etc/gideon-tracker/infisical.env"
    if os.access(token_path, os.R_OK):
        env_text = Path(token_path).read_text(encoding="utf-8")
    else:
        proc = subprocess.run(
            ["sudo", "-n", "cat", "--", token_path],
            check=False,
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            raise RuntimeError("cannot read Infisical token file")
        env_text = proc.stdout
    inf_token = os.environ.get("INFISICAL_TOKEN", "").strip()
    if not inf_token:
        for line in env_text.splitlines():
            if line.startswith("INFISICAL_TOKEN="):
                inf_token = line.split("=", 1)[1].strip().strip('"').strip("'")
                break
    if not inf_token:
        raise RuntimeError("Infisical token missing")
    return inf_token


def fetch_infisical_secrets(keys: tuple[str, ...]) -> dict[str, str]:
    import urllib.parse

    inf_token = read_infisical_token()
    project = os.environ.get(
        "INFISICAL_PROJECT_ID", "c84fe8b3-d64e-485a-82d7-250dc57a6453"
    )
    q = urllib.parse.urlencode(
        {"workspaceId": project, "environment": "prod", "secretPath": "/"}
    )
    req = urllib.request.Request(
        f"https://app.infisical.com/api/v3/secrets/raw?{q}",
        headers={"Authorization": f"Bearer {inf_token}"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        payload = json.loads(resp.read())
    found: dict[str, str] = {}
    for item in payload.get("secrets") or []:
        key = item.get("secretKey")
        value = item.get("secretValue")
        if key in keys and isinstance(value, str) and value:
            found[key] = value
    return found


def read_docmost_credentials() -> tuple[str, str]:
    email = os.environ.get(AUTOMATION_EMAIL_KEY, "").strip() or DEFAULT_AUTOMATION_EMAIL
    password = os.environ.get(AUTOMATION_PASSWORD_KEY, "").strip()
    if password:
        return email, password
    secrets = fetch_infisical_secrets((AUTOMATION_EMAIL_KEY, AUTOMATION_PASSWORD_KEY))
    email = secrets.get(AUTOMATION_EMAIL_KEY, email)
    password = secrets.get(AUTOMATION_PASSWORD_KEY, "")
    if not password:
        raise RuntimeError(f"{AUTOMATION_PASSWORD_KEY} not found in env or Infisical")
    return email, password


class DocmostClient:
    def __init__(self, email: str, password: str) -> None:
        cj = CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        req = urllib.request.Request(
            f"{API_BASE}/auth/login",
            data=json.dumps({"email": email, "password": password}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            self.opener.open(req, timeout=60).read()
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")[:200]
            raise RuntimeError(f"Docmost login failed ({exc.code}): {body}") from exc
        token = next(c.value for c in cj if c.name == "authToken")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "Cookie": f"authToken={token}",
        }

    def post(self, path: str, payload: dict[str, Any]) -> Any:
        req = urllib.request.Request(
            f"{API_BASE}{path}",
            data=json.dumps(payload).encode(),
            headers=self.headers,
            method="POST",
        )
        with self.opener.open(req, timeout=120) as resp:
            body = json.loads(resp.read())
        if body.get("success") is False:
            raise RuntimeError(f"{path}: {body}")
        return body.get("data", body)

    def sidebar(self, page_id: str | None = None) -> list[dict[str, Any]]:
        payload: dict[str, Any] = {"spaceId": SPACE_ID}
        if page_id:
            payload["pageId"] = page_id
        return self.post("/pages/sidebar-pages", payload)["items"]

    def fetch_rein_tree(self) -> list[dict[str, Any]]:
        def build(pid: str) -> list[dict[str, Any]]:
            nodes = []
            for it in self.sidebar(pid):
                kids = build(it["id"]) if it.get("hasChildren") else []
                nodes.append({"title": it["title"], "id": it["id"], "children": kids})
            return nodes

        return build(REIN_ROOT_ID)

    def find_child_page_id(self, parent_page_id: str, title: str) -> str | None:
        for item in self.sidebar(parent_page_id):
            if (item.get("title") or "") == title:
                return item.get("id")
        return None

    def page_markdown(self, page_id: str) -> str:
        page = self.post("/pages/info", {"pageId": page_id})
        content = page.get("content")
        if not content:
            return ""
        # Docmost returns ProseMirror JSON; compare via exported text if present.
        text = page.get("text") or page.get("markdown") or ""
        if isinstance(text, str) and text.strip():
            return text.strip()
        return json.dumps(content, sort_keys=True)


def export_tree(path: Path, client: DocmostClient | None = None) -> dict[str, Any]:
    if client is None:
        email, password = read_docmost_credentials()
        client = DocmostClient(email, password)
    tree = client.fetch_rein_tree()
    doc = {"root": REIN_ROOT_TITLE, "id": REIN_ROOT_ID, "tree": tree, "exported_via": "live"}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return doc


def load_tree(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def flatten_tree(
    nodes: list[dict[str, Any]], prefix: tuple[str, ...] = ()
) -> dict[tuple[str, ...], str]:
    found: dict[tuple[str, ...], str] = {}
    for node in nodes:
        path = prefix + (node["title"],)
        found[path] = node["id"]
        found.update(flatten_tree(node.get("children") or [], path))
    return found


def parse_h1(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("chapter file missing H1")


def chapter_key(filename: str, h1: str) -> str:
    base = filename.split("_")[0]
    if base == "05x" or "05x" in filename:
        return "05x"
    return base.split("-")[0]


def split_preamble_and_body(text: str) -> tuple[str, str]:
    """Preamble: through drive/internal callouts before first ## section."""
    lines = text.splitlines()
    pre: list[str] = []
    body_start = len(lines)
    for i, line in enumerate(lines):
        if line.startswith("## "):
            body_start = i
            break
        pre.append(line)
    return "\n".join(pre).strip(), "\n".join(lines[body_start:]).strip()


def parse_markdown_tables(body: str) -> list[tuple[str, list[str], list[list[str]]]]:
    """Return (heading, headers, rows) for each pipe table in body."""
    tables: list[tuple[str, list[str], list[list[str]]]] = []
    current_heading = ""
    i = 0
    lines = body.splitlines()
    while i < len(lines):
        line = lines[i]
        if line.startswith("## ") or line.startswith("### "):
            current_heading = line.lstrip("#").strip()
            i += 1
            continue
        if line.strip().startswith("|") and i + 1 < len(lines) and re.match(
            r"^\|\s*[-:| ]+\|\s*$", lines[i + 1].strip()
        ):
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            rows: list[list[str]] = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                rows.append(row)
                i += 1
            tables.append((current_heading, header, rows))
            continue
        i += 1
    return tables


def filter_table(
    header: list[str], rows: list[list[str]], keep: tuple[str, ...]
) -> tuple[list[str], list[list[str]]]:
    idx = []
    lower = [h.casefold() for h in header]
    for name in keep:
        try:
            idx.append(lower.index(name.casefold()))
        except ValueError:
            continue
    if not idx:
        return header, rows
    new_header = [header[j] for j in idx]
    new_rows = [[row[j] if j < len(row) else "" for j in idx] for row in rows]
    return new_header, new_rows


def render_table(header: list[str], rows: list[list[str]]) -> str:
    if not header:
        return ""
    sep = "| " + " | ".join("---" for _ in header) + " |"
    out = ["| " + " | ".join(header) + " |", sep]
    for row in rows:
        padded = row + [""] * (len(header) - len(row))
        out.append("| " + " | ".join(padded[: len(header)]) + " |")
    return "\n".join(out)


def strip_chapter_body(raw: str, key: str) -> str:
    preamble, body = split_preamble_and_body(raw)
    keep_cols = TABLE_KEEP_COLUMNS.get(key)
    if not keep_cols:
        return raw
    parts = [preamble, "", "> **Internal only – not for NCUK.** Titles and dates only on this page."]
    for heading, header, rows in parse_markdown_tables(body):
        nh, nr = filter_table(header, rows, keep_cols)
        if not nr:
            continue
        if heading:
            parts.extend(["", f"### {heading}"])
        parts.extend(["", render_table(nh, nr)])
    text = "\n".join(parts).strip() + "\n"
    return text


def prepare_markdown(raw: str, filename: str) -> str:
    h1 = parse_h1(raw)
    key = chapter_key(filename, h1)
    if key in TITLES_ONLY_CHAPTER_KEYS:
        return strip_chapter_body(raw, key)
    # Full chapters: drop trailing Sources block.
    trimmed = re.split(r"\n---\n### Sources\b", raw, maxsplit=1)[0].strip() + "\n"
    return trimmed


def normalize_for_compare(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def resolve_page(
    path_suffix: tuple[str, ...], index: dict[tuple[str, ...], str]
) -> PageRef:
    full = path_suffix
    page_id = index.get(full)
    return PageRef(path=full, page_id=page_id, title=full[-1] if full else "")


def plan_apply(
    chapters_dir: Path,
    index: dict[tuple[str, ...], str],
    client: DocmostClient | None,
) -> list[PlanRow]:
    rows: list[PlanRow] = []
    missing_pages: list[str] = []

    for filename in CHAPTER_FILES:
        src = chapters_dir / filename
        if not src.is_file():
            rows.append(
                PlanRow(
                    page_label=filename,
                    action="error",
                    chars=0,
                    detail="chapter file missing",
                )
            )
            continue
        raw = src.read_text(encoding="utf-8")
        h1 = parse_h1(raw)
        path_suffix = H1_TO_PATH.get(h1)
        if not path_suffix:
            rows.append(
                PlanRow(
                    page_label=h1,
                    action="error",
                    chars=0,
                    detail="no H1→Docmost mapping",
                )
            )
            continue
        md = prepare_markdown(raw, filename)
        ref = resolve_page(path_suffix, index)
        label = " / ".join((REIN_ROOT_TITLE,) + ref.path)
        page_id = ref.page_id
        if page_id is None and client is not None and len(path_suffix) > 1:
            parent_id = index.get(path_suffix[:-1])
            if parent_id:
                page_id = client.find_child_page_id(parent_id, path_suffix[-1])

        if page_id is None:
            missing_pages.append(label)
            rows.append(
                PlanRow(
                    page_label=label,
                    action="create_page",
                    chars=len(md),
                    detail=f"from {filename}",
                )
            )
            continue

        action = "update"
        detail = f"from {filename}"
        if client is not None:
            try:
                current = client.page_markdown(page_id)
                if normalize_for_compare(current) == normalize_for_compare(md):
                    action = "skip"
                    detail = "unchanged"
            except Exception as exc:  # noqa: BLE001 — dry-run continues
                detail = f"compare failed: {exc.__class__.__name__}"
        if ref.page_id is None and page_id is not None:
            detail = (detail + "; " if detail else "") + "resolved existing child by title"

        rows.append(PlanRow(page_label=label, action=action, chars=len(md), detail=detail))

    if missing_pages:
        rows.append(
            PlanRow(
                page_label="(missing pages)",
                action="list",
                chars=0,
                detail="; ".join(missing_pages),
            )
        )
    return rows


def apply_rows(
    chapters_dir: Path,
    index: dict[tuple[str, ...], str],
    client: DocmostClient,
    dry_run: bool,
) -> list[PlanRow]:
    plan = plan_apply(chapters_dir, index, client if not dry_run else client)
    if dry_run:
        return plan

    parent_cache: dict[tuple[str, ...], str] = dict(index)

    for filename in CHAPTER_FILES:
        src = chapters_dir / filename
        if not src.is_file():
            continue
        raw = src.read_text(encoding="utf-8")
        h1 = parse_h1(raw)
        path_suffix = H1_TO_PATH.get(h1)
        if not path_suffix:
            continue
        md = prepare_markdown(raw, filename)
        page_id = parent_cache.get(path_suffix)
        if page_id is None:
            parent_path = path_suffix[:-1]
            parent_id = parent_cache.get(parent_path)
            if parent_id is None:
                raise RuntimeError(f"cannot create page; missing parent {parent_path}")
            page_id = client.find_child_page_id(parent_id, path_suffix[-1])
            if page_id is None:
                created = client.post(
                    "/pages/create",
                    {
                        "spaceId": SPACE_ID,
                        "parentPageId": parent_id,
                        "title": path_suffix[-1],
                        "searchIndexing": False,
                    },
                )
                page_id = (
                    created["id"]
                    if isinstance(created, dict)
                    else created.get("pageId")
                )
            parent_cache[path_suffix] = page_id

        client.post(
            "/pages/update",
            {
                "pageId": page_id,
                "content": md,
                "format": "markdown",
                "operation": "replace",
                "searchIndexing": False,
            },
        )
    return plan


def print_table(rows: list[PlanRow]) -> None:
    print("| page | action | chars |")
    print("| --- | --- | ---: |")
    for row in rows:
        if row.action == "list":
            print(f"| {row.page_label} | {row.action} | {row.detail} |")
        else:
            extra = f" ({row.detail})" if row.detail else ""
            print(f"| {row.page_label} | {row.action}{extra} | {row.chars} |")


def cmd_export(args: argparse.Namespace) -> int:
    try:
        export_tree(Path(args.tree))
        print(f"exported: {args.tree}")
        return 0
    except Exception as exc:
        print(f"export failed: {exc}", file=sys.stderr)
        return 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--chapters-dir",
        type=Path,
        default=DEFAULT_CHAPTERS_DIR,
        help="Server-only chapter markdown directory",
    )
    parser.add_argument(
        "--tree",
        type=Path,
        default=DEFAULT_TREE_BACKUP,
        help="04 REIN tree JSON (from export or backup)",
    )
    parser.add_argument(
        "--export-tree",
        action="store_true",
        help="Refresh --tree from live Docmost before planning",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print plan table; do not write Docmost",
    )
    parser.add_argument(
        "--export-only",
        action="store_true",
        help="Only export tree to --tree and exit",
    )
    args = parser.parse_args(argv)

    if args.export_only:
        return cmd_export(args)

    client: DocmostClient | None = None
    if args.export_tree:
        try:
            email, password = read_docmost_credentials()
            client = DocmostClient(email, password)
            export_tree(args.tree, client)
        except Exception as exc:
            print(f"live export failed: {exc}", file=sys.stderr)
            if not args.tree.is_file():
                return 2

    if not args.tree.is_file():
        print(f"tree file missing: {args.tree}", file=sys.stderr)
        return 2

    tree_doc = load_tree(args.tree)
    index = flatten_tree(tree_doc.get("tree") or [])

    if args.dry_run:
        # Compare with live content when login works.
        try:
            if client is None:
                email, password = read_docmost_credentials()
                client = DocmostClient(email, password)
        except Exception:
            client = None
        rows = plan_apply(args.chapters_dir, index, client)
        print_table(rows)
        return 0

    if client is None:
        email, password = read_docmost_credentials()
        client = DocmostClient(email, password)
    rows = apply_rows(args.chapters_dir, index, client, dry_run=False)
    print_table(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
