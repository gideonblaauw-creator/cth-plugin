#!/usr/bin/env python3
"""Validate FLEET_REGISTRY.yaml structure and tier counts."""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

import yaml

TIER_TARGETS = {
    "0": 2,
    "1a": 33,
    "1b": 31,
    "2": 20,
    "3": 6,
    "4": 1,  # at least one Hands lane bot (OpenCode); Cursor Hands is harness pool
}


def load_registry(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if "fleet_registry" not in data:
        raise ValueError("Missing top-level fleet_registry key")
    return data["fleet_registry"]


def validate(registry: dict) -> list[str]:
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

    roots = []
    for b in bots:
        parent = b.get("parent") or {}
        pid = parent.get("id")
        if pid is None:
            if b["id"] != "5dc64ea4":
                errors.append(f"{b['id']}: null parent only allowed for Orchestrator")
            roots.append(b["id"])
            continue
        if pid not in id_set:
            errors.append(f"{b['id']}: parent {pid} not in registry")

    # Cycle detection
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
    stated_orphans = sum(
        1
        for b in bots
        if (b.get("parent") or {}).get("proposed") and b["id"] != "fbc6f772"
    )
    if expected_orphans != 36:
        errors.append(f"orphan_parent_proposals: expected 36 entries, got {expected_orphans}")
    if stated_orphans < 36:
        errors.append(
            f"expected at least 36 proposed parent records on bots, got {stated_orphans}"
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate FLEET_REGISTRY.yaml")
    parser.add_argument(
        "registry",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "FLEET_REGISTRY.yaml",
    )
    args = parser.parse_args()
    registry = load_registry(args.registry)
    errors = validate(registry)
    if errors:
        print("VALIDATION FAILED", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    tiers = Counter(str(b["tier"]) for b in registry["bots"])
    print("VALIDATION OK")
    print(f"  bots: {len(registry['bots'])}")
    print(f"  tiers: {dict(sorted(tiers.items()))}")
    print(f"  orphan proposals: {len(registry.get('orphan_parent_proposals', []))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())