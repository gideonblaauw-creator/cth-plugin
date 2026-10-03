#!/usr/bin/env python3
"""Unit tests for wire-brief scripts."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
EXAMPLES = ROOT / "examples"


class SteLintTests(unittest.TestCase):
    def test_lint_runs_on_en_example(self) -> None:
        brief = EXAMPLES / "en-diagram-tool-brief.md"
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS / "ste_lint.py"), str(brief), "--json"],
            capture_output=True,
            text=True,
            check=True,
        )
        report = json.loads(proc.stdout)
        self.assertIn("summary", report)
        self.assertGreater(report["summary"]["sentence_count"], 0)
        self.assertIn("scores", report["sentences"][0])

    def test_lint_runs_on_es_example(self) -> None:
        brief = EXAMPLES / "es-voice-strategy-brief.md"
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS / "ste_lint.py"), str(brief)],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("STE-80 lint", proc.stdout)
        self.assertIn("JSON", proc.stdout)


class FactCheckTests(unittest.TestCase):
    def test_fact_check_flags_missing_number(self) -> None:
        source = "We need 42 servers on VPS by 2026-10-15."
        brief = "We need servers on VPS."
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "source.txt"
            br = Path(tmp) / "brief.md"
            src.write_text(source, encoding="utf-8")
            br.write_text(brief, encoding="utf-8")
            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "fact_check.py"),
                    str(src),
                    str(br),
                    "--json",
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(proc.returncode, 0)
            report = json.loads(proc.stdout)
            missing_numbers = report["missing"]["numbers"]
            self.assertTrue(any("42" in n for n in missing_numbers))

    def test_en_example_facts_present(self) -> None:
        proc = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "fact_check.py"),
                str(EXAMPLES / "en-diagram-tool-source.txt"),
                str(EXAMPLES / "en-diagram-tool-brief.md"),
                "--json",
            ],
            capture_output=True,
            text=True,
        )
        report = json.loads(proc.stdout)
        # GitHub must be reflected
        self.assertNotIn("GitHub", report["missing"]["entities"])


if __name__ == "__main__":
    unittest.main()
