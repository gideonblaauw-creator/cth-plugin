#!/usr/bin/env python3
"""Tests for scripts/deck-brand-guard/check_decks.py"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "deck-brand-guard"))

import check_decks as dg  # noqa: E402


class DeckBrandGuardTests(unittest.TestCase):
    def test_cth_colors_pass(self) -> None:
        text = """
        :root {
          --cth-primary: #2D6A4F;
          --cth-dark: #1B4332;
          --cth-accent: #95D5B2;
          --cth-light: #D8F3DC;
          --cth-white: #FFFFFF;
          --cth-text: #333333;
        }
        """
        expected = dg.load_yaml(dg.GUARD_DIR / "expected.yaml")
        self.assertEqual(dg.check_cth_colors("demo", text, expected), [])

    def test_cth_colors_missing_var(self) -> None:
        expected = dg.load_yaml(dg.GUARD_DIR / "expected.yaml")
        findings = dg.check_cth_colors("demo", ":root {}", expected)
        self.assertTrue(any(f.check == "cth.colors" for f in findings))

    def test_inter_not_matched_in_international(self) -> None:
        expected = dg.load_yaml(dg.GUARD_DIR / "expected.yaml")
        prose = "<p>International mentors and isInteractiveTarget()</p>"
        findings = dg.check_cth_fonts("demo", prose, expected)
        self.assertTrue(any(f.check == "cth.fonts" for f in findings))

    def test_logo_pass(self) -> None:
        expected = dg.load_yaml(dg.GUARD_DIR / "expected.yaml")
        html = '<img src="assets/cth-logo.png" alt="CleantechHUB">'
        self.assertEqual(dg.check_cth_logo("demo", html, expected), [])

    def test_confidential_slug(self) -> None:
        findings = dg.check_no_confidential(
            "cth-rein-funding-oct2026",
            "<html></html>",
            {"cth-rein-funding-oct2026"},
            [],
        )
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].check, "repo.no_confidential")

    def test_price_on_public_deck(self) -> None:
        html = "<p>Total cost is $1,234 USD for the program.</p>"
        findings = dg.check_public_no_prices("pub", html, {"pub"}, [])
        self.assertTrue(any(f.check == "public.no_prices" for f in findings))

    def test_price_allowlist_cop_conference(self) -> None:
        import re

        allow = dg.compile_allowlist([r"\bCOP\b(?!\s*\d)"])
        html = "<p>We meet at COP and Climate Week NYC.</p>"
        findings = dg.check_public_no_prices("pub", html, {"pub"}, allow)
        self.assertEqual(findings, [])

    def test_baseline_distinguishes_new(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            baseline = Path(tmp) / "baseline.json"
            baseline.write_text(
                json.dumps(
                    {
                        "violations": [
                            {
                                "deck": "x",
                                "check": "cth.logo",
                                "message": "no logo",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            keys = dg.load_baseline(baseline)
            self.assertIn(("x", "cth.logo", "no logo"), keys)


if __name__ == "__main__":
    unittest.main()
