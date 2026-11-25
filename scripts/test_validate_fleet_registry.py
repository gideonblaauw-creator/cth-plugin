#!/usr/bin/env python3
"""Unit tests for validate_fleet_registry.py"""
from __future__ import annotations

import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_fleet_registry import (
    DEFAULT_CATALOG,
    load_registry,
    validate,
    validate_enforcement_off,
    validate_gap2,
    validate_gap6,
    validate_no_fast_true,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY = REPO_ROOT / "FLEET_REGISTRY.yaml"


class FleetRegistryValidationTest(unittest.TestCase):
    def test_registry_file_exists(self) -> None:
        self.assertTrue(REGISTRY.is_file(), f"missing {REGISTRY}")

    def test_full_validation_passes(self) -> None:
        registry = load_registry(REGISTRY)
        errors = validate(registry, catalog_path=DEFAULT_CATALOG)
        self.assertEqual(errors, [], "\n".join(errors))

    def test_tier_counts(self) -> None:
        registry = load_registry(REGISTRY)
        from collections import Counter

        tiers = Counter(str(b["tier"]) for b in registry["bots"])
        self.assertEqual(tiers["0"], 2)
        self.assertEqual(tiers["1a"], 33)
        self.assertEqual(tiers["1b"], 31)
        self.assertEqual(tiers["2"], 20)
        self.assertEqual(tiers["3"], 6)
        self.assertGreaterEqual(tiers["4"], 1)

    def test_gap2_and_gap6_on_live_registry(self) -> None:
        registry = load_registry(REGISTRY)
        by_id = {b["id"]: b for b in registry["bots"]}
        self.assertEqual(validate_gap2(by_id["e68ca92f"]), [])
        self.assertEqual(validate_gap6(registry), [])

    def test_detects_cycle_in_fixture(self) -> None:
        fixture = {
            "bot_count": 2,
            "orphan_parent_proposals": [],
            "enforcement_default": "off",
            "auto_pause": {"proposed": True, "enforcement": "off"},
            "circuit_breaker": {"proposed": True, "enforcement": "off"},
            "auto_pause_tier_templates": {"1a": {"proposed": True, "enforcement": "off"}},
            "circuit_breaker_tier_templates": {"1a": {"proposed": True, "enforcement": "off"}},
            "bots": [
                {
                    "id": "aaaa0001",
                    "name": "A",
                    "tier": "1a",
                    "type": "desk",
                    "parent": {"id": "aaaa0002"},
                    "status": "active",
                    "tools_whitelist": [],
                    "max_context_tokens": 1,
                    "reset": {"enforcement": "off"},
                    "budget_share_cap": "0%",
                    "model": {"fast": False, "enforcement": "off"},
                },
                {
                    "id": "aaaa0002",
                    "name": "B",
                    "tier": "1a",
                    "type": "desk",
                    "parent": {"id": "aaaa0001"},
                    "status": "active",
                    "tools_whitelist": [],
                    "max_context_tokens": 1,
                    "reset": {"enforcement": "off"},
                    "budget_share_cap": "0%",
                    "model": {"fast": False, "enforcement": "off"},
                },
            ],
        }
        errors = validate(fixture)
        self.assertTrue(any("cycle" in e for e in errors))

    def test_rejects_enforcement_on(self) -> None:
        reg = {"enforcement_default": "on", "bots": []}
        errors = validate_enforcement_off(reg)
        self.assertTrue(errors)

    def test_rejects_fast_true(self) -> None:
        reg = {"bots": [{"model": {"fast": True}}]}
        errors = validate_no_fast_true(reg)
        self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()