#!/usr/bin/env python3
"""One-shot activation transforms for FLEET_REGISTRY.yaml (report-only enforcement)."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

REPO = Path(__file__).resolve().parent.parent
REGISTRY_PATH = REPO / "FLEET_REGISTRY.yaml"

FLEET_LINE_RE = re.compile(
    r"^Fleet \(25 Nov 2026\): parent .+ \([0-9a-f]{8}\), tier .+\. "
    r"Source: cth-plugin FLEET_REGISTRY\.yaml\.\s*$",
    re.MULTILINE,
)

REPORT_PARENT_RE = re.compile(
    r"(?i)(?:reports?\s+to|reporting\s+to)\s+([^.(:\n]+?)"
    r"(?:\s*\(([0-9a-f]{8})\))?",
)


def transform_node(obj: Any, bot_tier: str | None = None) -> Any:
    if isinstance(obj, dict):
        out: dict[str, Any] = {}
        for key, val in obj.items():
            if key == "proposed" and val is True:
                out["status"] = "active"
                continue
            if key == "enforcement" and val == "off":
                out[key] = "report_only"
                continue
            if key == "enforce":
                out[key] = val
                continue
            child_tier = bot_tier
            if key == "tier" and isinstance(val, str):
                child_tier = val
            out[key] = transform_node(val, child_tier)
        if "enforce" not in out and obj.get("proposed") is True:
            out["enforce"] = False
        if "status" in out and out["status"] == "active" and "enforce" not in out:
            if any(k in out for k in ("grok_weekly_share_alert_pct", "mid_week_grok_share_trip_pct", "banned", "target", "enabled")):
                out["enforce"] = False
        return out
    if isinstance(obj, list):
        return [transform_node(item, bot_tier) for item in obj]
    return obj


def activate_registry(data: dict) -> dict:
    reg = data["fleet_registry"]
    reg["version"] = "2026-11-25-active"
    reg["enforcement_default"] = "report_only"
    reg["activation"] = {
        "status": "active",
        "gideon_go": "2026-11-25 16:56 COT",
        "enforcement_mode": "report_only",
    }

    for block in ("auto_pause", "circuit_breaker"):
        section = reg.get(block)
        if isinstance(section, dict):
            section.pop("proposed", None)
            section["status"] = "active"
            section["enforce"] = False
            section["enforcement"] = "report_only"

    for templates_key in ("auto_pause_tier_templates", "circuit_breaker_tier_templates"):
        templates = reg.get(templates_key) or {}
        for tpl in templates.values():
            if isinstance(tpl, dict):
                tpl.pop("proposed", None)
                tpl["status"] = "active"
                tpl["enforce"] = False
                tpl["enforcement"] = "report_only"

    bots = reg.get("bots") or []
    by_id = {b["id"]: b for b in bots}
    for bot in bots:
        tier = str(bot.get("tier", ""))
        bot["enforcement"] = "report_only"

        parent = bot.get("parent") or {}
        if parent.get("proposed") is True:
            parent.pop("proposed", None)
            parent["status"] = "active"
        bot["parent"] = parent

        reset = bot.get("reset") or {}
        reset["enforcement"] = "report_only"
        if tier in ("0", "1a", "1b") and bot.get("status") == "active":
            reset["clone_and_reset"] = True
        bot["reset"] = reset

        model = bot.get("model") or {}
        model["enforcement"] = "report_only"
        if tier == "2":
            model["fast"] = True
            model["slug"] = model.get("slug") or "cursor-grok-4.5-low-fast"
        elif tier == "4":
            model["fast"] = True
        else:
            model["fast"] = False
        bot["model"] = model

        if tier == "2":
            bc = bot.get("browser_cua") or {}
            bc.pop("proposed", None)
            bc["status"] = "active"
            bc["enforce"] = False
            bc["enforcement"] = "report_only"
            bot["browser_cua"] = bc

        if bot["id"] == "e68ca92f":
            for sub in ("archive", "triggers"):
                block = bot.get(sub) or {}
                block.pop("proposed", None)
                block["status"] = "active"
                block["enforce"] = False
                block["enforcement"] = "report_only"
                bot[sub] = block

        iso = bot.get("isolation")
        if isinstance(iso, dict):
            iso["enforcement"] = "report_only"

    reg["bots"] = bots
    data["fleet_registry"] = transform_node(reg)
    return data


def main() -> int:
    text = REGISTRY_PATH.read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    activated = activate_registry(data)
    REGISTRY_PATH.write_text(
        yaml.dump(activated, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )
    print(f"Activated {REGISTRY_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())