#!/usr/bin/env python3
"""Generate FLEET_REGISTRY.yaml from org-chart catalog.json (read-only inputs)."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

DEFAULT_CATALOG = (
    Path("/cursor/stores/bot/fleet-redesign-2026-11-25/org-chart/catalog.json")
)

# Plan §3.1 normalized parents for workbenches and gap fixes (id8).
PARENT_OVERRIDE_ID8: dict[str, str] = {
    "fbc6f772": "85949e8a",  # Health → Engine Room (gap 5; profile still says Infra)
    "49495613": "7ffbe815",  # Sustenttia Fillout → Sustenttia (gap 4)
    "2592cf74": "27bd8324",  # Monday Teclogi → Teclogi (gap 3 fold-in target)
}

# Gap 6 isolation kinds (enforcement off until profile sync).
ISOLATION_KIND: dict[str, str] = {
    "9360f6b2": "workstream",
    "462857ec": "workstream",
    "f5576adb": "workstream",
    "6479618a": "workstream",
    "9657a5a3": "personal",
    "b258f16f": "personal",
    "a6610a66": "personal",
    "0255b102": "personal",
    "2599f250": "personal",
    "75be842c": "personal",
    "9d25c2ea": "personal",
}

FOLD_IN_NOTES: dict[str, dict[str, str]] = {
    "2592cf74": {"into": "27bd8324", "status": "active"},
    "49495613": {"into": "7ffbe815", "status": "active"},
}

STATUS_FROM_NOTE: dict[str, str] = {
    "e68ca92f": "parked",
}


def tier_for(bot: dict) -> str:
    id8 = bot["id8"]
    layer = bot["layer"]
    if id8 in ("5dc64ea4", "c656afb9"):
        return "0"
    if layer == "Isolated client desk":
        return "1b"
    if layer == "Desk":
        return "1a"
    if layer == "Workbench":
        return "2"
    if layer == "Capability":
        return "3"
    if layer == "Cloud Hands":
        return "4"
    if layer == "Orchestrator":
        return "0"
    raise ValueError(f"Unknown layer for {bot['name']}: {layer}")


def bot_type(layer: str) -> str:
    return {
        "Orchestrator": "orchestrator",
        "Desk": "desk",
        "Isolated client desk": "isolated_desk",
        "Workbench": "workbench",
        "Capability": "capability",
        "Cloud Hands": "cloud_hands",
    }[layer]


def tier_budget_share(tier: str) -> str:
    return {
        "0": "4%",
        "1a": "10%",
        "1b": "6%",
        "2": "8%",
        "3": "5%",
        "4": "67%",
    }[tier]


def max_context_and_turns(tier: str, id8: str) -> tuple[int, int]:
    if tier == "0":
        return (50000, 4) if id8 == "c656afb9" else (40000, 3)
    if tier == "1a":
        return (60000, 5)
    if tier == "1b":
        return (50000, 5)
    if tier == "2":
        return (25000, 1)
    if tier == "3":
        return (40000, 2)
    return (0, 0)


def model_block(tier: str, id8: str) -> dict:
    if tier == "4":
        if id8 == "5d95b30d":
            return {
                "model_tier": "tier-execution",
                "provider": "opencode",
                "slug": "opencode-cloud-hands",
                "fast": False,
                "enforcement": "off",
            }
        return {
            "model_tier": "tier-execution",
            "provider": "cursor",
            "slug": "composer-2.5",
            "fast": False,
            "enforcement": "off",
        }
    if tier == "2":
        return {"model_tier": "tier-routine", "enforcement": "off"}
    if tier == "3":
        return {"model_tier": "tier-routine", "enforcement": "off"}
    return {"model_tier": "tier-reasoning", "enforcement": "off"}


SYSTEM_ALIASES: dict[str, str] = {
    "gmail": "gmail",
    "google calendar": "google_calendar",
    "calendar": "google_calendar",
    "whatsapp": "whatsapp",
    "odoo": "odoo",
    "monday": "monday",
    "drive": "google_drive",
    "github": "github",
    "n8n": "n8n",
    "n8n-li": "n8n",
    "slack": "slack",
    "slack connector": "slack",
    "telegram": "telegram",
    "moodle": "moodle",
    "fillout": "fillout",
    "meet / zoom / teams": "meeting_bridge",
    "meet/zoom/teams": "meeting_bridge",
    "x connector": "x",
    "airtable": "airtable",
    "vps": "vps",
    "docker": "docker",
    "dns": "dns",
    "vercel": "vercel",
    "sec edgar": "sec_edgar",
    "cognee": "cognee",
    "docmost": "docmost",
    "bookstack": "bookstack",
    "odoo api via hands or vps": "odoo",
    "instagram / channel tools": "instagram",
    "ads tools": "google_ads",
    "facebook / channel tools": "facebook",
    "linkedin connector": "linkedin",
    "stt": "voice_stt",
    "whatsapp / n8n": "whatsapp",
    "whatsapp / channel audio": "whatsapp",
    "meetings db": "vault_meetings_db",
    "archive": "archive",
    "hands": "hands",
    "repos": "repos",
    "google ads": "google_ads",
    "linkedin": "linkedin",
    "instagram": "instagram",
    "facebook": "facebook",
}


def _slug(token: str) -> str:
    low = token.strip().lower()
    return SYSTEM_ALIASES.get(low, re.sub(r"[^a-z0-9]+", "_", low).strip("_"))


def parse_tools_whitelist(deps: str) -> list[str]:
    if not deps:
        return []
    parts = re.split(r",\s*", deps)
    out: list[str] = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        low = p.lower()
        if low in ("orchestrator", "orchestrator or the requesting desk"):
            continue
        if "hands" in low:
            out.append("hands")
        if " or " in low:
            for sub in low.split(" or "):
                slug = _slug(sub)
                if slug and slug not in ("desks", "workbenches", "workbenches"):
                    out.append(slug)
            continue
        if "/" in p and "meet" not in low:
            for sub in p.split("/"):
                slug = _slug(sub.strip())
                if slug and len(slug) > 2:
                    out.append(slug)
            continue
        if any(kw in low for kw in ("workbench", "desk", "desks", "skill")):
            # Channel references like "Gmail workbench" → underlying system
            if "gmail" in low:
                out.append("gmail")
            elif "calendar" in low:
                out.append("google_calendar")
            continue
        slug = _slug(p)
        if slug and slug not in out:
            out.append(slug)
    return sorted(set(out))


def build_name_index(catalog: list[dict]) -> dict[str, str]:
    idx: dict[str, str] = {}
    for b in catalog:
        idx[b["name"].lower()] = b["id8"]
        short = b["name"].split("·")[0].strip().lower()
        if short not in idx:
            idx[short] = b["id8"]
    aliases = {
        "gideon": None,
        "orchestrator": "5dc64ea4",
        "control tower · infra": "c656afb9",
        "control tower": "c656afb9",
        "socials · desks": "22eef082",
        "socials": "22eef082",
        "inbox": "d3d9dd60",
        "cth meetings": "7ea170b4",
        "academy · desks": "b65940e2",
        "teclogi": "27bd8324",
        "sustenttia": "7ffbe815",
        "rein hubs": "fd48890b",
    }
    for k, v in aliases.items():
        if v:
            idx[k] = v
    return idx


def resolve_parent_id8(bot: dict, name_index: dict[str, str]) -> str | None:
    reports = (bot.get("reports") or "").strip()
    if reports.lower() == "gideon":
        return None
    id8 = bot["id8"]
    if id8 in PARENT_OVERRIDE_ID8:
        return PARENT_OVERRIDE_ID8[id8]
    key = reports.lower()
    if key in name_index:
        return name_index[key]
    for name, pid in name_index.items():
        if name in key or key in name:
            return pid
    raise KeyError(f"Cannot resolve parent for {bot['name']!r} reports={reports!r}")


def parent_proposal_reason(bot: dict, parent_id8: str | None) -> str:
    id8 = bot["id8"]
    if id8 == "fbc6f772":
        return "Gap 5: Health alerts route to Engine Room before Infra checker escalation."
    if id8 == "49495613":
        return "Gap 4: Fillout I/O workbench belongs under Sustenttia, not Orchestrator orphan."
    if id8 == "2592cf74":
        return "Gap 3: Monday CRM lane folds into Teclogi; standalone parent should be Teclogi desk."
    if id8 == "c656afb9":
        return "Infra desk parent is Orchestrator; profile omitted explicit parent link."
    return (
        "Org chart v1 profile omitted parent metadata; normalized per build-plan §3.1."
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument(
        "-o", "--output", type=Path, default=Path("FLEET_REGISTRY.yaml")
    )
    args = parser.parse_args()

    catalog: list[dict] = json.loads(args.catalog.read_text(encoding="utf-8"))
    assert len(catalog) == 93, len(catalog)

    name_index = build_name_index(catalog)
    id8_set = {b["id8"] for b in catalog}

    bots_out = []
    meta_orphans = []

    for bot in catalog:
        tier = tier_for(bot)
        id8 = bot["id8"]
        parent_id8 = resolve_parent_id8(bot, name_index)

        parent_block: dict = {"id": parent_id8}
        if bot["name"] == "Orchestrator":
            parent_block = {"id": None, "hitl": "Gideon"}
        elif id8 in PARENT_OVERRIDE_ID8:
            parent_block["proposed"] = True
            parent_block["reason"] = parent_proposal_reason(bot, parent_id8)
        elif not bot["parent_stated"]:
            parent_block["proposed"] = True
            parent_block["reason"] = parent_proposal_reason(bot, parent_id8)
        if parent_block.get("proposed") and not bot["parent_stated"]:
            meta_orphans.append(
                {
                    "id": id8,
                    "name": bot["name"],
                    "parent": parent_id8,
                    "reason": parent_block["reason"],
                }
            )

        max_ctx, max_turns = max_context_and_turns(tier, id8)
        status = STATUS_FROM_NOTE.get(id8, "active")

        record: dict = {
            "id": id8,
            "id_full": bot["id"],
            "name": bot["name"],
            "tier": tier,
            "type": bot_type(bot["layer"]),
            "org_layer": bot["layer"],
            "parent": parent_block,
            "status": status,
            "tools_whitelist": parse_tools_whitelist(bot.get("deps", "")),
            "max_context_tokens": max_ctx,
            "reset": {
                "max_turns": max_turns,
                "at_tokens": 80000 if tier in ("0", "1a", "1b") else max_ctx,
                "clone_and_reset": tier in ("0", "1a", "1b"),
                "enforcement": "off",
            },
            "model": model_block(tier, id8),
            "stateless": tier == "2",
            "budget_share_cap": tier_budget_share(tier),
            "routines": [],
            "enforcement": "off",
        }

        if id8 == "f8b4b4c2":
            record["routines"] = [
                {
                    "name": "weekly_token_audit",
                    "schedule": "Mon 08:00 UTC",
                    "enforcement": "off",
                }
            ]

        if id8 in ISOLATION_KIND:
            record["isolation"] = {
                "kind": ISOLATION_KIND[id8],
                "enforcement": "off",
            }

        if tier == "1b" and bot["domain"] == "Isolated client" and id8 not in ISOLATION_KIND:
            record["isolation"] = {"kind": "client", "enforcement": "off"}

        if id8 in FOLD_IN_NOTES:
            record["fold_in"] = {**FOLD_IN_NOTES[id8], "enforcement": "off"}

        if bot.get("note"):
            record["org_chart_note"] = bot["note"]

        bots_out.append(record)

    doc = {
        "fleet_registry": {
            "version": "2026-11-25-draft",
            "source": "cth-bot-org-chart v1 + build-plan-2026-11-25.md Part 3.1",
            "bot_count": 93,
            "tier_targets": {
                "0": 2,
                "1a": 33,
                "1b": 31,
                "2": 20,
                "3": 6,
                "4_hands": "1+",
            },
            "enforcement_default": "off",
            "orphan_parent_proposals": meta_orphans,
            "bots": bots_out,
        }
    }

    def str_representer(dumper, data):
        if "\n" in data:
            return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
        return dumper.represent_scalar("tag:yaml.org,2002:str", data)

    yaml.add_representer(str, str_representer)
    args.output.write_text(
        yaml.dump(doc, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )
    print(f"Wrote {args.output} ({len(bots_out)} bots, {len(meta_orphans)} proposals)")
    # Parent sanity
    for b in bots_out:
        pid = b["parent"].get("id")
        if pid is not None and pid not in id8_set:
            print(f"WARN unresolved parent {pid} for {b['name']}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())