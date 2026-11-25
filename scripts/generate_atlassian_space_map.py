#!/usr/bin/env python3
"""Generate docs/fleet/atlassian/space-map.csv from FLEET_REGISTRY.yaml (design-only)."""
from __future__ import annotations

import csv
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "FLEET_REGISTRY.yaml"
OUT = ROOT / "docs/fleet/atlassian/space-map.csv"

SHARED_HANDS = "CTHHANDS"
SHARED_ORCH = "CTHORCH"
SHARED_OPS = "CTHOPS"
SHARED_CAP = "CTHCAP"


def slug4(name: str) -> str:
    name = re.sub(r"[^\w\s·/-]", "", name)
    name = name.replace("·", " ").replace("/", " ")
    parts = [p for p in re.split(r"[\s_-]+", name.strip()) if p]
    if not parts:
        return "BOT"
    if len(parts) == 1:
        base = parts[0][:4].upper()
    else:
        base = "".join(p[0] for p in parts[:4]).upper()
    return (base + "XXXX")[:4]


def jira_key(bot: dict, used: set[str]) -> str:
    bid = bot["id"]
    if bid == "5dc64ea4":
        return SHARED_ORCH
    if bid == "c656afb9":
        return SHARED_OPS
    if bid == "5d95b30d":
        return SHARED_HANDS
    if bot["type"] == "capability":
        cand = f"CAP{slug4(bot['name'])}"[:10]
    elif bot["type"] == "workbench":
        return ""  # inherits parent project + component
    else:
        cand = f"CTH{slug4(bot['name'])}"[:10]
    cand = re.sub(r"[^A-Z0-9]", "", cand.upper()) or f"CTH{bid[:4].upper()}"
    if not cand[0].isalpha():
        cand = "C" + cand
    while cand in used and len(cand) < 10:
        cand = (cand + bid[0].upper())[:10]
    if cand in used:
        cand = f"CTH{bid[:6].upper()}"[:10]
    used.add(cand)
    return cand


def parent_id(bot: dict) -> str:
    p = bot.get("parent") or {}
    pid = p.get("id")
    return pid or ""


def resolve_project_key(
    bot_id: str, key_by_id: dict[str, str], bots_by_id: dict[str, dict]
) -> str:
    if bot_id in (None, ""):
        return SHARED_ORCH
    bot = bots_by_id.get(bot_id)
    if not bot:
        return SHARED_ORCH
    raw = key_by_id.get(bot_id) or ""
    if raw and "/" not in raw:
        return raw
    pid = parent_id(bot)
    if pid:
        return resolve_project_key(pid, key_by_id, bots_by_id)
    return SHARED_ORCH


def isolation_flag(bot: dict) -> str:
    iso = bot.get("isolation") or {}
    kind = iso.get("kind", "")
    if bot["type"] == "isolated_desk" and kind in ("client", "grant_draft"):
        return "strict"
    if kind in ("client", "grant_draft"):
        return "strict"
    if kind == "personal":
        return "personal"
    if kind == "workstream":
        return "internal"
    return "shared"


def main() -> None:
    data = yaml.safe_load(REGISTRY.read_text())["fleet_registry"]["bots"]
    bots_by_id = {b["id"]: b for b in data}
    used_keys: set[str] = {SHARED_ORCH, SHARED_OPS, SHARED_HANDS, SHARED_CAP}
    rows = []
    key_by_id: dict[str, str] = {}

    for bot in data:
        key_by_id[bot["id"]] = (
            jira_key(bot, used_keys) if bot["type"] != "workbench" else ""
        )

    for bot in sorted(data, key=lambda b: (b["tier"], b["type"], b["name"])):
        pid = parent_id(bot)
        jira = key_by_id.get(bot["id"], "")
        if bot["type"] == "workbench" and pid:
            parent_key = resolve_project_key(pid, key_by_id, bots_by_id)
            jira = f"{parent_key}/cmp:WB-{bot['id'][:8]}"
        elif bot["type"] == "capability":
            jira = f"{SHARED_CAP}/cmp:CP-{bot['id'][:8]}"
            key_by_id[bot["id"]] = SHARED_CAP

        conf = jira.split("/")[0] if jira and "/" not in jira[:20] else ""
        if not conf or conf.startswith("cmp:"):
            conf = resolve_project_key(pid, key_by_id, bots_by_id) if pid else (
                jira.split("/")[0] if "/" in jira else jira or SHARED_ORCH
            )
        loom = f"/Fleet/T{bot_tier(bot)}/{bot['id']}/{slug_folder(bot['name'])}"
        rovo = f"scope:cth-fleet/{bot['type']}/{bot['id'][:8]}"
        rows.append(
            {
                "bot_id": bot["id"],
                "bot_name": bot["name"],
                "tier": bot["tier"],
                "parent_id": pid,
                "jira_project_key": jira,
                "confluence_space_key": conf,
                "loom_folder": loom,
                "rovo_agent_scope": rovo,
                "isolation_flag": isolation_flag(bot),
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "bot_id",
                "bot_name",
                "tier",
                "parent_id",
                "jira_project_key",
                "confluence_space_key",
                "loom_folder",
                "rovo_agent_scope",
                "isolation_flag",
            ],
        )
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUT}")


def bot_tier(bot: dict) -> str:
    return str(bot["tier"]).replace(".", "")


def slug_folder(name: str) -> str:
    s = re.sub(r"[^\w\s-]", "", name.lower())
    s = re.sub(r"\s+", "-", s.strip())
    return s[:48] or "bot"


if __name__ == "__main__":
    main()