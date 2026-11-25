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

ORCHESTRATOR_ID = "5dc64ea4"
LAST_BATCH_IDS = frozenset({"7ea170b4", "d3d9dd60"})
FLEET_LINE_IN_DESC = re.compile(
    r"^Fleet \(25 Nov 2026\): .+ Source: cth-plugin FLEET_REGISTRY\.yaml\.\s*$",
    re.MULTILINE,
)


def reports_to_parent_id8(desc: str) -> str | None:
    """Parent id8 from the Reports-to clause only (not child workbench mentions)."""
    m = re.search(r"(?i)reports?\s+to", desc)
    if not m:
        return None
    rest = desc[m.end() :]
    clause_end = len(rest)
    stop = re.search(r"[.\n]", rest[:160])
    if stop:
        clause_end = stop.start()
    clause = rest[:clause_end]
    id_m = re.search(r"\(([0-9a-f]{8})", clause)
    if id_m:
        return id_m.group(1).lower()
    if re.search(r"(?i)(?:the\s+)?orchestrator\b", clause):
        return ORCHESTRATOR_ID
    return None


def reporting_parent_conflict(desc: str, registry_parent_id: str) -> str | None:
    if not registry_parent_id:
        return None
    cited = reports_to_parent_id8(desc)
    if cited is None:
        return None
    if cited == registry_parent_id.lower():
        return None
    return (
        f"Reports-to line cites parent {cited}; registry parent is {registry_parent_id}"
    )


def fleet_line(bot_id: str, parent_id: str | None, parent_name: str, tier: str) -> str:
    if bot_id == ORCHESTRATOR_ID:
        return (
            f"Fleet (25 Nov 2026): parent Gideon Blaauw (HITL root), tier {tier}. "
            "Source: cth-plugin FLEET_REGISTRY.yaml."
        )
    pid = parent_id or "null"
    return (
        f"Fleet (25 Nov 2026): parent {parent_name} ({pid}), tier {tier}. "
        "Source: cth-plugin FLEET_REGISTRY.yaml."
    )


def expected_new_description(current: str, line: str) -> str:
    if FLEET_LINE_IN_DESC.search(current):
        raise ValueError("current description already contains a Fleet line; use append-only policy")
    return current.rstrip("\n") + "\n" + line + "\n"


def assign_batches(changes: list[dict]) -> None:
    pinned = [c for c in changes if c["id"] in LAST_BATCH_IDS]
    normal = [c for c in changes if c["id"] not in LAST_BATCH_IDS]
    batch_size = 20
    for i, row in enumerate(normal):
        row["batch"] = (i // batch_size) + 1
    last_batch = max((c["batch"] for c in normal), default=0) + (1 if normal else 1)
    for row in pinned:
        row["batch"] = last_batch


def verify_append_only(changes: list[dict]) -> list[str]:
    errors: list[str] = []
    for row in changes:
        line = fleet_line(
            row["id"],
            (row.get("_parent_id")),
            row.get("_parent_name", ""),
            row.get("_tier", ""),
        )
        expected = expected_new_description(row["current_description"], line)
        if row["new_description"] != expected:
            errors.append(f"{row['id']}: new_description does not equal current + one appended line")
    return errors


def main() -> int:
    registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))["fleet_registry"]
    bots = {b["id"]: b for b in registry["bots"]}

    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    snapshot_by8: dict[str, dict] = {row["id"][:8]: row for row in snapshot}

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
        if parent_id is None and id8 != ORCHESTRATOR_ID:
            parent_name = "Gideon (HITL)"
        elif parent_id:
            parent_name = bots.get(parent_id, {}).get("name", parent_id)
        else:
            parent_name = "Gideon Blaauw (HITL root)"
        tier = str(bot["tier"])
        current = snap.get("description") or ""
        line = fleet_line(id8, parent_id, parent_name, tier)

        if id8 != ORCHESTRATOR_ID and parent_id:
            note = reporting_parent_conflict(current, parent_id)
            if note:
                extra = {"id": id8, "name": bot["name"], "note": note}
                if id8 == "fbc6f772":
                    extra["flag"] = "Awaiting Gideon — profile says Infra (c656afb9); registry Engine Room (85949e8a)"
                conflicts.append(extra)
                continue

        if FLEET_LINE_IN_DESC.search(current):
            skipped_unchanged.append(id8)
            continue

        try:
            new_desc = expected_new_description(current, line)
        except ValueError:
            skipped_unchanged.append(id8)
            continue

        if new_desc.strip() == current.strip():
            skipped_unchanged.append(id8)
            continue

        changes.append(
            {
                "id": id8,
                "name": bot["name"],
                "current_description": current,
                "new_description": new_desc,
                "change_summary": "Append Fleet (25 Nov 2026) parent/tier line",
                "_parent_id": parent_id,
                "_parent_name": parent_name,
                "_tier": tier,
            }
        )

    for id8 in sorted(snapshot_by8):
        if id8 not in bots:
            snapshot_not_in_registry.append(id8)

    assign_batches(changes)

    verify_errors = verify_append_only(changes)
    if verify_errors:
        print("BYTE-CHECK FAILED", file=sys.stderr)
        for e in verify_errors[:20]:
            print(f"  - {e}", file=sys.stderr)
        return 1

    for row in changes:
        row.pop("_parent_id", None)
        row.pop("_parent_name", None)
        row.pop("_tier", None)

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

    md_lines.extend(
        [
            "",
            "## Fleet line exceptions",
            "",
            f"- **`{ORCHESTRATOR_ID}` Orchestrator** — append-only line uses "
            "`parent Gideon Blaauw (HITL root)` (no `(null)`); registry `parent.id` is null / HITL.",
            "",
            "## Conflicts",
            "",
        ]
    )
    if conflicts:
        for c in conflicts:
            flag = f" — **{c['flag']}**" if c.get("flag") else ""
            md_lines.append(f"- `{c['id']}` **{c['name']}** — {c['note']}{flag}")
    else:
        md_lines.append("- None")

    md_lines.extend(
        [
            "",
            f"**Last-batch pins:** `{', '.join(sorted(LAST_BATCH_IDS))}` share the final batch.",
            "",
            "## Skipped unchanged",
            "",
        ]
    )
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

    md_lines.extend(["", "## Byte-check", "", "- All `new_description` values verified: `current.rstrip() + \"\\n\" + fleet_line + \"\\n\"`"])

    OUT_MD.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(changes)} changes to {OUT_JSON} (byte-check OK)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())