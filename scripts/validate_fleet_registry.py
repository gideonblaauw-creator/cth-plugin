#!/usr/bin/env python3
"""Validate FLEET_REGISTRY.yaml structure and tier counts."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

TIER_TARGETS = {
    "0": 2,
    "1a": 33,
    "1b": 31,
    "2": 20,
    "3": 6,
    "4": 1,
}

DEFAULT_CATALOG = Path(
    "/cursor/stores/bot/fleet-redesign-2026-11-25/org-chart/catalog.json"
)

ISOLATION_EXPECTED = {
    "client": 27,
    "grant_draft": 3,
    "workstream": 4,
    "personal": 7,
}

GAP2_ID = "e68ca92f"


def load_registry(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if "fleet_registry" not in data:
        raise ValueError("Missing top-level fleet_registry key")
    return data["fleet_registry"]


def iter_enforcement(obj: Any, path: str = "") -> list[tuple[str, Any]]:
    found: list[tuple[str, Any]] = []
    if isinstance(obj, dict):
        for key, val in obj.items():
            p = f"{path}.{key}" if path else key
            if key == "enforcement":
                found.append((p, val))
            found.extend(iter_enforcement(val, p))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            found.extend(iter_enforcement(item, f"{path}[{i}]"))
    return found


def iter_fast_flags(obj: Any, path: str = "") -> list[tuple[str, bool]]:
    found: list[tuple[str, bool]] = []
    if isinstance(obj, dict):
        for key, val in obj.items():
            p = f"{path}.{key}" if path else key
            if key == "fast" and val is True:
                found.append((p, val))
            found.extend(iter_fast_flags(val, p))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            found.extend(iter_fast_flags(item, f"{path}[{i}]"))
    return found


def validate_enforcement_off(registry: dict) -> list[str]:
    errors: list[str] = []
    for loc, val in iter_enforcement(registry):
        if val != "off":
            errors.append(f"enforcement must be off everywhere, got {val!r} at {loc}")
    if registry.get("enforcement_default") != "off":
        errors.append("fleet_registry.enforcement_default must be 'off'")
    return errors


def validate_no_fast_true(registry: dict) -> list[str]:
    errors: list[str] = []
    for loc, _ in iter_fast_flags(registry):
        errors.append(f"fast:true not allowed (17 Nov lock) at {loc}")
    return errors


def validate_catalog_parity(registry: dict, catalog_path: Path) -> list[str]:
    errors: list[str] = []
    if not catalog_path.is_file():
        errors.append(f"catalog not found for parity check: {catalog_path}")
        return errors
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    catalog_ids = sorted(b["id8"] for b in catalog)
    registry_ids = sorted(b["id"] for b in registry.get("bots", []))
    if catalog_ids != registry_ids:
        missing = set(catalog_ids) - set(registry_ids)
        extra = set(registry_ids) - set(catalog_ids)
        if missing:
            errors.append(f"registry missing catalog id8: {sorted(missing)}")
        if extra:
            errors.append(f"registry extra id8 vs catalog: {sorted(extra)}")
    return errors


def validate_gap2(bot: dict | None) -> list[str]:
    if bot is None:
        return [f"gap 2: missing bot {GAP2_ID}"]
    errors: list[str] = []
    if bot.get("status") != "parked":
        errors.append(f"gap 2: {GAP2_ID} status must remain parked")
    archive = bot.get("archive") or {}
    for key, expected in (
        ("target", "archived"),
        ("enforcement", "off"),
        ("proposed", True),
    ):
        if archive.get(key) != expected:
            errors.append(f"gap 2: archive.{key} expected {expected!r}, got {archive.get(key)!r}")
    triggers = bot.get("triggers") or {}
    for key, expected in (
        ("enabled", False),
        ("enforcement", "off"),
        ("proposed", True),
    ):
        if triggers.get(key) != expected:
            errors.append(f"gap 2: triggers.{key} expected {expected!r}, got {triggers.get(key)!r}")
    return errors


def validate_gap6(registry: dict) -> list[str]:
    errors: list[str] = []
    kinds = Counter(
        (b.get("isolation") or {}).get("kind")
        for b in registry.get("bots", [])
        if b.get("isolation")
    )
    for kind, expected in ISOLATION_EXPECTED.items():
        got = kinds.get(kind, 0)
        if got != expected:
            errors.append(f"gap 6: isolation.kind {kind} expected {expected}, got {got}")
    return errors


def validate_governance_defaults(registry: dict) -> list[str]:
    errors: list[str] = []
    for block in ("auto_pause", "circuit_breaker"):
        section = registry.get(block)
        if not isinstance(section, dict):
            errors.append(f"missing fleet {block} block")
            continue
        if section.get("proposed") is not True or section.get("enforcement") != "off":
            errors.append(f"{block} must have proposed: true and enforcement: off")
    for templates_key in ("auto_pause_tier_templates", "circuit_breaker_tier_templates"):
        templates = registry.get(templates_key)
        if not isinstance(templates, dict):
            errors.append(f"missing {templates_key}")
            continue
        for tier, tpl in templates.items():
            if tpl.get("proposed") is not True or tpl.get("enforcement") != "off":
                errors.append(f"{templates_key}.{tier} must have proposed: true and enforcement: off")
    return errors


def validate_tier2_browser_cua(bots: list[dict]) -> list[str]:
    errors: list[str] = []
    for b in bots:
        if str(b.get("tier")) != "2":
            continue
        bc = b.get("browser_cua") or {}
        if bc.get("banned") is not True:
            errors.append(f"{b['id']}: tier-2 browser_cua.banned must be true")
        if bc.get("enforcement") != "off" or bc.get("proposed") is not True:
            errors.append(f"{b['id']}: tier-2 browser_cua must be proposed with enforcement off")
    return errors


def validate(
    registry: dict,
    catalog_path: Path | None = None,
) -> list[str]:
    errors: list[str] = []
    bots = registry.get("bots")
    if not isinstance(bots, list):
        return ["bots must be a list"]
    if len(bots) != 93:
        errors.append(f"expected 93 bots, got {len(bots)}")

    ids = [b.get("id") for b in bots]
    if len(ids) != len(set(ids)):
        errors.append("duplicate bot ids")

    id_set = set(ids)
    by_id = {b["id"]: b for b in bots}

    for b in bots:
        for field in (
            "id",
            "name",
            "tier",
            "type",
            "parent",
            "status",
            "tools_whitelist",
            "max_context_tokens",
            "reset",
            "budget_share_cap",
        ):
            if field not in b:
                errors.append(f"{b.get('id', '?')}: missing {field}")

    for b in bots:
        parent = b.get("parent") or {}
        pid = parent.get("id")
        if pid is None:
            if b["id"] != "5dc64ea4":
                errors.append(f"{b['id']}: null parent only allowed for Orchestrator")
            continue
        if pid not in id_set:
            errors.append(f"{b['id']}: parent {pid} not in registry")

    visiting: set[str] = set()
    visited: set[str] = set()

    def dfs(nid: str) -> bool:
        if nid in visiting:
            return True
        if nid in visited:
            return False
        visiting.add(nid)
        bot = by_id.get(nid)
        if bot:
            pid = (bot.get("parent") or {}).get("id")
            if pid and dfs(pid):
                return True
        visiting.remove(nid)
        visited.add(nid)
        return False

    for bid in id_set:
        if dfs(bid):
            errors.append("parent graph contains a cycle")
            break

    tiers = Counter(str(b["tier"]) for b in bots)
    for tier, expected in TIER_TARGETS.items():
        got = tiers.get(tier, 0)
        if tier == "4" and got < expected:
            errors.append(f"tier {tier}: expected >={expected} Hands lane bots, got {got}")
        elif tier != "4" and got != expected:
            errors.append(f"tier {tier}: expected {expected}, got {got}")

    if registry.get("bot_count") != 93:
        errors.append("fleet_registry.bot_count must be 93")

    expected_orphans = len(registry.get("orphan_parent_proposals") or [])
    if expected_orphans != 36:
        errors.append(f"orphan_parent_proposals: expected 36 entries, got {expected_orphans}")

    errors.extend(validate_enforcement_off(registry))
    errors.extend(validate_no_fast_true(registry))
    errors.extend(validate_gap2(by_id.get(GAP2_ID)))
    errors.extend(validate_gap6(registry))
    errors.extend(validate_governance_defaults(registry))
    errors.extend(validate_tier2_browser_cua(bots))

    cat = catalog_path or DEFAULT_CATALOG
    errors.extend(validate_catalog_parity(registry, cat))

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate FLEET_REGISTRY.yaml")
    parser.add_argument(
        "registry",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "FLEET_REGISTRY.yaml",
    )
    parser.add_argument(
        "--catalog",
        type=Path,
        default=DEFAULT_CATALOG,
        help="Org-chart catalog.json for id8 parity",
    )
    args = parser.parse_args()
    registry = load_registry(args.registry)
    errors = validate(registry, catalog_path=args.catalog)
    if errors:
        print("VALIDATION FAILED", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    tiers = Counter(str(b["tier"]) for b in registry["bots"])
    kinds = Counter(
        (b.get("isolation") or {}).get("kind")
        for b in registry["bots"]
        if b.get("isolation")
    )
    print("VALIDATION OK")
    print(f"  bots: {len(registry['bots'])}")
    print(f"  tiers: {dict(sorted(tiers.items()))}")
    print(f"  orphan proposals: {len(registry.get('orphan_parent_proposals', []))}")
    print(f"  isolation kinds: {dict(sorted((k, v) for k, v in kinds.items() if k))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())