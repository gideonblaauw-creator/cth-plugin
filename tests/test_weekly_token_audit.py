#!/usr/bin/env python3
"""Tests for scripts/weekly_token_audit.py"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "weekly_token_audit.py"
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "usage-events-small.csv"


class WeeklyTokenAuditTests(unittest.TestCase):
    def test_fixture_counts_and_kpis(self) -> None:
        proc = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                str(FIXTURE),
                "--json",
                "/tmp/audit-test.json",
                "--markdown",
                "/tmp/audit-test.md",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("enforcement disabled (needs Gideon GO)", proc.stdout)
        data = json.loads(Path("/tmp/audit-test.json").read_text(encoding="utf-8"))
        self.assertEqual(data["window"]["event_count"], 5)
        self.assertEqual(data["totals"]["all_tokens"], 93_800)
        self.assertAlmostEqual(data["totals"]["grok_share_pct"], 100 * 91_600 / 93_800, places=2)
        self.assertEqual(data["rapid_fire"]["under_15s"], 1)
        self.assertEqual(data["grok_turns_over_80k"], 1)
        self.assertIn("default", data["grok_model_shares_pct_of_grok"])
        self.assertEqual(len(data["heatmap_america_bogota"]["tokens_by_hour"]), 24)

    def test_enforce_without_approval(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), str(FIXTURE), "--enforce"],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(
            proc.stdout.strip(),
            "enforcement disabled (needs Gideon GO)",
        )

    def test_enforce_with_approval_logs_would_actions(self) -> None:
        env = {**dict(__import__("os").environ), "ENFORCE_APPROVED": "1"}
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), str(FIXTURE), "--enforce"],
            capture_output=True,
            text=True,
            check=True,
            env=env,
        )
        self.assertIn("[WOULD]", proc.stdout)


if __name__ == "__main__":
    unittest.main()