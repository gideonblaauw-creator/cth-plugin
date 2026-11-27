#!/usr/bin/env python3
"""Generate docs/fleet/atlassian/space-map.csv (lean v2 — Jira + Confluence only)."""
from __future__ import annotations

import csv
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "FLEET_REGISTRY.yaml"
OUT = ROOT / "docs/fleet/atlassian/space-map.csv"

CTHORCH = "CTHORCH"
CTHOPS = "CTHOPS"
CTHHANDS = "CTHHANDS"
CTHINT = "CTHINT"
CTHHUB = "CTHHUB"
ACCOUNTABLE = "Gideon Blaauw (HITL)"


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


def client_project_key(bot: dict, used: set[str]) -> str:
    cand = f"CTH{slug4(bot['name'])}"[:10]
    cand = re.sub(r"[^A-Z0-9]", "", cand.upper())
    if not cand[0].isalpha():
        cand = "C" + cand
    bid = bot["id"]
    while cand in used and len(cand) < 10:
        cand = (cand + bid[0].upper())[:10]
    if cand in used:
        cand = f"CTH{bid[:6].upper()}"[:10]
    used.add(cand)
    return cand


def jira_mapping(bot: dict, used_client: set[str]) -> str:
    bid = bot["id"]
    if bid == "5dc64ea4":
        return CTHORCH
    if bid == "c656afb9":
        return CTHOPS
    if bid == "5d95b30d":
        return CTHHANDS
    kind = (bot.get("isolation") or {}).get("kind")
    if bot["type"] == "isolated_desk" and kind == "client":
        return client_project_key(bot, used_client)
    if bot["type"] == "workbench":
        return f"{CTHINT}/cmp:WB-{bid[:8]}"
    if bot["type"] == "capability":
        return f"{CTHINT}/cmp:CP-{bid[:8]}"
    if bot["type"] == "orchestrator":
        return CTHORCH
    return f"{CTHINT}/cmp:DS-{bid[:8]}"


def confluence_mapping(bot: dict, jira: str) -> str:
    kind = (bot.get("isolation") or {}).get("kind")
    if bot["type"] == "isolated_desk" and kind == "client":
        base = jira.split("/")[0]
        return f"{CTHHUB}+page:{base}"
    return CTHHUB


def isolation_flag(bot: dict) -> str:
    iso = bot.get("isolation") or {}
    kind = iso.get("kind", "")
    if bot["type"] == "isolated_desk" and kind == "client":
        return "client_project"
    if kind in ("grant_draft",):
        return "grant_component"
    if kind == "personal":
        return "personal"
    if kind == "workstream":
        return "workstream"
    return "internal"


def parent_id(bot: dict) -> str:
    p = bot.get("parent") or {}
    return p.get("id") or ""


def main() -> None:
    data = yaml.safe_load(REGISTRY.read_text())["fleet_registry"]["bots"]
    used_client: set[str] = {CTHORCH, CTHOPS, CTHHANDS, CTHINT}
    rows = []
    for bot in sorted(data, key=lambda b: (b["tier"], b["type"], b["name"])):
        jira = jira_mapping(bot, used_client)
        rows.append(
            {
                "bot_id": bot["id"],
                "bot_name": bot["name"],
                "tier": bot["tier"],
                "parent_id": parent_id(bot),
                "agent_id": bot["id"],
                "accountable": ACCOUNTABLE,
                "jira_project_key": jira,
                "confluence_space_key": confluence_mapping(bot, jira),
                "isolation_flag": isolation_flag(bot),
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "bot_id",
        "bot_name",
        "tier",
        "parent_id",
        "agent_id",
        "accountable",
        "jira_project_key",
        "confluence_space_key",
        "isolation_flag",
    ]
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    clients = sum(1 for r in rows if r["isolation_flag"] == "client_project")
    print(f"Wrote {len(rows)} rows ({clients} client Jira projects) to {OUT}")


if __name__ == "__main__":
    main()