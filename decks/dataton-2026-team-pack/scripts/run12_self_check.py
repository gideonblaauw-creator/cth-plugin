#!/usr/bin/env python3
"""Run 12 — Prompts-IA PDF empty header template (no Chromium timestamp)."""
from __future__ import annotations

import hashlib
import io
import re
import subprocess
import sys
import zipfile
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent.parent
PROOFS = ROOT / "_png" / "run12"
BASE = "59e987145b5ab3e09c2575d64296abdde59057d9"
RUN11_ZIP_SHA = "c9563ff9624dba740dd961a0ccf3a1b62b36d57556373a1bee23fdcfb3398989"
SHEET_DOCX_SHA = "b8649f50454b71eb64504d721b482b1d1f5099558a1652679cae9ce6159a74ed"
V3_SHA = "4cd248ad16227c7cbd6fc33a5b89548920ab978371525a5e57a5de9b95e2fe6a"

ZIP = ROOT / "team-pack-es-pdfs-v0.4.zip"
SHEET_PDF = ROOT / "dist" / "Prompts-IA-Dataton-24nov.pdf"
SHEET_C = ROOT / "cuestionario" / "Prompts-IA-Dataton-24nov.pdf"
SHEET_DOCX = ROOT / "dist" / "Prompts-IA-Dataton-24nov.docx"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_bytes(relpath: str, ref: str = BASE) -> bytes:
    return subprocess.check_output(
        ["git", "-C", str(REPO), "show", f"{ref}:decks/dataton-2026-team-pack/{relpath}"]
    )


def pdffonts_ok(stdout: str) -> tuple[bool, str]:
    bad: list[str] = []
    for line in stdout.splitlines():
        if not line.strip() or line.startswith("name") or set(line.strip()) == {"-"}:
            continue
        name = line.split()[0]
        if name.startswith("-") or name == "Open":
            continue
        if "NotoColorEmoji" in line:
            continue
        if "OpenSans" not in name:
            bad.append(name)
    return len(bad) == 0, ", ".join(bad)


def export_page(pdf: Path, page: int, dest: Path) -> None:
    doc = fitz.open(pdf)
    doc[page].get_pixmap(dpi=110).save(dest)
    doc.close()


def zip_delta_members() -> list[str]:
    ref = zipfile.ZipFile(io.BytesIO(git_bytes("team-pack-es-pdfs-v0.4.zip")))
    with ref, zipfile.ZipFile(ZIP) as new:
        delta = []
        for name in sorted(set(ref.namelist()) | set(new.namelist())):
            b1 = ref.read(name) if name in ref.namelist() else b""
            b2 = new.read(name) if name in new.namelist() else b""
            if hashlib.sha256(b1).digest() != hashlib.sha256(b2).digest():
                delta.append(name)
    ref.close()
    return delta


def main() -> int:
    PROOFS.mkdir(parents=True, exist_ok=True)
    head = subprocess.check_output(["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True).strip()
    lines = ["# Run 12 notes", "", f"Head: `{head}`.", f"Base: `{BASE}`.", ""]
    lines.append("## Ticket")
    lines.append("- `hands-tickets/dataton-teampack-run12-sheet-header.md` (sha `cd151258` — not in repo clone)")
    lines.append("")

    pf = subprocess.run(["pdffonts", str(SHEET_PDF)], capture_output=True, text=True, check=True)
    ok_fonts, font_detail = pdffonts_ok(pf.stdout)
    (PROOFS / "pdffonts-sheet.txt").write_text(pf.stdout, encoding="utf-8")
    lines.append("## Prompts-IA PDF header fix")
    lines.append(f"- pages: **{fitz.open(SHEET_PDF).page_count}** (expect 3)")
    lines.append(f"- pdffonts Open Sans + emoji only: **{ok_fonts}** ({font_detail or 'ok'})")
    lines.append(f"- pdf sha256: `{sha256(SHEET_PDF)}`")
    lines.append(f"- cuestionario/dist pdf identical: **{sha256(SHEET_C) == sha256(SHEET_PDF)}**")
    lines.append(f"- sheet docx unchanged (`{SHEET_DOCX_SHA}`): **{sha256(SHEET_DOCX) == SHEET_DOCX_SHA}**")
    p2_on_2 = len(fitz.open(SHEET_PDF)) > 1 and "Parte: Parte 2" in fitz.open(SHEET_PDF)[1].get_text()
    lines.append(f"- Parte 2 on page 2: **{p2_on_2}**")
    lines.append("")

    date_hits: list[str] = []
    ts_re = re.compile(r"\b\d{1,2}/\d{1,2}/\d{2,4},?\s+\d{1,2}:\d{2}\s+[AP]M\b", re.I)
    doc = fitz.open(SHEET_PDF)
    for i in range(doc.page_count):
        t = doc[i].get_text()
        if ts_re.search(t) or "11/24/26" in t:
            date_hits.append(f"page {i + 1}")
    doc.close()
    lines.append("## Timestamp grep (must be empty)")
    lines.append(f"- hits: **{date_hits or 'none'}**")
    (PROOFS / "timestamp-grep.txt").write_text("\n".join(date_hits) or "none\n", encoding="utf-8")
    lines.append("")

    for i in range(fitz.open(SHEET_PDF).page_count):
        export_page(SHEET_PDF, i, PROOFS / f"sheet-p{i + 1:02d}-110dpi.png")

    lines.append("## Zip vs run 11 (`c9563ff9`)")
    lines.append(f"- zip sha256: `{sha256(ZIP)}` (was `{RUN11_ZIP_SHA}`)")
    delta = zip_delta_members()
    lines.append(f"- delta members: `{delta}`")
    with zipfile.ZipFile(ZIP) as zf:
        for name in sorted(zf.namelist()):
            lines.append(f"- `{name}`: `{hashlib.sha256(zf.read(name)).hexdigest()[:8]}`")
    lines.append("")

    pinned = [
        ("prompts.txt", sha256(ROOT / "cuestionario" / "prompts.txt"), V3_SHA),
        ("Prompts-IA docx", sha256(SHEET_DOCX), SHEET_DOCX_SHA),
    ]
    lines.append("## Pinned")
    for label, got, want in pinned:
        lines.append(f"- {label}: **{got == want}**")

    diff = subprocess.check_output(
        ["git", "-C", str(REPO), "diff", "--stat", f"{BASE}..HEAD", "--", "decks/dataton-2026-team-pack/"],
        text=True,
    ).strip()
    lines.append("")
    lines.append("## git diff --stat vs base")
    lines.append("```")
    lines.append(diff or "(empty)")
    lines.append("```")

    (ROOT / "run12-notes.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(ROOT / "run12-notes.md")

    fail = (
        not ok_fonts
        or fitz.open(SHEET_PDF).page_count != 3
        or date_hits
        or sha256(SHEET_DOCX) != SHEET_DOCX_SHA
        or sha256(SHEET_C) != sha256(SHEET_PDF)
        or delta != ["Prompts-IA-Dataton-24nov.pdf"]
        or not p2_on_2
    )
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())