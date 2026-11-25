#!/usr/bin/env python3
"""Build docs/fleet/activation/profile-diff.json from snapshot + FLEET_REGISTRY.yaml."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
REGISTRY = REPO / "FLEET_REGISTRY.yaml"
SNAPSHOT = REPO / "docs/fleet/activation/profile-snapshot-2026-11-25T1700.json"
OUT_JSON = REPO / "docs/fleet/activation/profile-diff.json"
OUT_MD = REPO / "docs/fleet/activation/profile-diff-summary.md"

FLEET_LINE_RE = re.compile(
    r"Fleet \(25 Nov 2026\): parent .+?\(([0-9a-f]{8})\), tier ([^.\n]+)\. "
    r"Source: cth-plugin FLEET_REGISTRY\.yaml\.?",
    re.IGNORECASE,
)
PARENT_ID_RE = re.compile(r"\(([0-9a-f]{8})\)")
REPORTS_TO_RE = re.compile(
    r"(?i)(?:reports?\s+to|reporting\s+to)\s+([^.\n(]+?)(?:\s*\(([0-9a-f]{8})\))?"
)


def parent_ids_in_description(desc: str) -> set[str]:
    found: set[str] = set()
    m = FLEET_LINE_RE.search(desc)
    if m:
        found.add(m.group(1).lower())
    for m in PARENT_ID_RE.finditer(desc):
        found.add(m.group(1).lower())
    for m in REPORTS_TO_RE.finditer(desc):
        if m.group(2):
            found.add(m.group(2).lower())
    return found


def extract_named_parent_conflict(desc: str, registry_parent: str) -> str | None:
    """If description states a parent id different from registry, return note."""
    ids = parent_ids_in_description(desc)
    ids.discard(registry_parent.lower())
    fleet_m = FLEET_LINE_RE.search(desc)
    if fleet_m and fleet_m.group(1).lower() != registry_parent.lower():
        return (
            f"Fleet line names parent {fleet_m.group(1)}; registry parent is {registry_parent}"
        )
    if not ids:
        return None
    extra = sorted(ids)
    if registry_parent.lower() not in parent_ids_in_description(desc):
        if len(extra) == 1:
            return f"Description cites parent id {extra[0]}; registry parent is {registry_parent}"
        return f"Description cites parent ids {extra}; registry parent is {registry_parent}"
    for pid in extra:
        if pid != registry_parent.lower():
            return f"Description cites parent id {pid}; registry parent is {registry_parent}"
    return None


def fleet_line(parent_name: str, parent_id: str, tier: str) -> str:
    return (
        f"Fleet (25 Nov 2026): parent {parent_name} ({parent_id}), tier {tier}. "
        "Source: cth-plugin FLEET_REGISTRY.yaml."
    )


def apply_fleet_line(desc: str, line: str) -> str:
    if FLEET_LINE_RE.search(desc):
        return FLEET_LINE_RE.sub(line, desc).rstrip() + "\n"
    return desc.rstrip() + "\n" + line + "\n"


def main() -> int:
    registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))["fleet_registry"]
    bots = {b["id"]: b for b in registry["bots"]}
    by_full = {b["id_full"]: b for b in registry["bots"]}

    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    snapshot_by8: dict[str, dict] = {}
    for row in snapshot:
        id8 = row["id"][:8]
        snapshot_by8[id8] = row

    changes: list[dict] = []
    conflicts: list[dict] = []
    skipped_unchanged: list[str] = []
    snapshot_not_in_registry: list[str] = []
    registry_not_in_snapshot: list[str] = []

    for id8, bot in sorted(bots.items()):
        if id8 not in snapshot_by8:
            registry_not_in_snapshot.append(id8)
            continue

        snap = snapshot_by8[id8]
        parent_id = (bot.get("parent") or {}).get("id")
        parent_name = "Gideon (HITL)" if parent_id is None else (
            bots.get(parent_id, {}).get("name", parent_id)
        )
        tier = str(bot["tier"])
        current = snap.get("description") or ""
        note = extract_named_parent_conflict(current, parent_id or "")
        line = fleet_line(parent_name, parent_id or "null", tier)

        if note and parent_id:
            if parent_id.lower() not in parent_ids_in_description(current):
                conflicts.append({"id": id8, "name": bot["name"], "note": note})
                continue
            ids = parent_ids_in_description(current)
            if ids and parent_id.lower() not in ids:
                conflicts.append({"id": id8, "name": bot["name"], "note": note})
                continue

        new_desc = apply_fleet_line(current, line)
        if new_desc.strip() == current.strip():
            skipped_unchanged.append(id8)
            continue

        summary = "Append or replace Fleet (25 Nov 2026) parent/tier line"
        changes.append(
            {
                "id": id8,
                "name": bot["name"],
                "current_description": current,
                "new_description": new_desc,
                "change_summary": summary,
            }
        )

    for id8 in sorted(snapshot_by8):
        if id8 not in bots:
            snapshot_not_in_registry.append(id8)

    batch_size = 20
    for i, row in enumerate(changes):
        row["batch"] = (i // batch_size) + 1

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(changes, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    batches: dict[int, int] = {}
    for row in changes:
        batches[row["batch"]] = batches.get(row["batch"], 0) + 1

    md_lines = [
        "# Profile diff summary (activation B — not applied in Grok UI)",
        "",
        f"**Generated from:** `{SNAPSHOT.name}` + `FLEET_REGISTRY.yaml`",
        "",
        "## Counts",
        "",
        f"- Total profile changes: **{len(changes)}**",
        f"- Unchanged (skipped): **{len(skipped_unchanged)}**",
        f"- Conflicts (manual): **{len(conflicts)}**",
        f"- Registry bots missing from snapshot: **{len(registry_not_in_snapshot)}**",
        f"- Snapshot ids not in registry: **{len(snapshot_not_in_registry)}**",
        "",
        "## Per batch",
        "",
    ]
    if batches:
        for b in sorted(batches):
            md_lines.append(f"- Batch {b}: {batches[b]} bots")
    else:
        md_lines.append("- _(no batches)_")

    md_lines.extend(["", "## Conflicts", ""])
    if conflicts:
        for c in conflicts:
            md_lines.append(f"- `{c['id']}` **{c['name']}** — {c['note']}")
    else:
        md_lines.append("- None")

    md_lines.extend(["", "## Skipped unchanged", ""])
    if skipped_unchanged:
        md_lines.append(", ".join(f"`{x}`" for x in skipped_unchanged[:20]))
        if len(skipped_unchanged) > 20:
            md_lines.append(f"\n… and {len(skipped_unchanged) - 20} more.")
    else:
        md_lines.append("- None")

    md_lines.extend(["", "## Snapshot ids not in registry", ""])
    if snapshot_not_in_registry:
        md_lines.append(", ".join(f"`{x}`" for x in snapshot_not_in_registry))
    else:
        md_lines.append("- None")

    OUT_MD.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(changes)} changes to {OUT_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())