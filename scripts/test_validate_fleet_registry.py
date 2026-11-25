#!/usr/bin/env python3
"""Unit tests for validate_fleet_registry.py"""
from __future__ import annotations

import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_fleet_registry import load_registry, validate

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY = REPO_ROOT / "FLEET_REGISTRY.yaml"


class FleetRegistryValidationTest(unittest.TestCase):
    def test_registry_file_exists(self) -> None:
        self.assertTrue(REGISTRY.is_file(), f"missing {REGISTRY}")

    def test_full_validation_passes(self) -> None:
        registry = load_registry(REGISTRY)
        errors = validate(registry)
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

    def test_detects_cycle_in_fixture(self) -> None:
        fixture = {
            "bot_count": 2,
            "orphan_parent_proposals": [],
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
                    "reset": {},
                    "budget_share_cap": "0%",
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
                    "reset": {},
                    "budget_share_cap": "0%",
                },
            ],
        }
        errors = validate(fixture)
        self.assertTrue(any("cycle" in e for e in errors))


if __name__ == "__main__":
    unittest.main()