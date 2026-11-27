#!/usr/bin/env python3
"""Fallback A4 PDF for hoja print HTML via Playwright."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
html = ROOT / "hojas/hoja-5-pitch-print.html"
pdf = ROOT / "hoja-5-pitch.pdf"


def main() -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page()
        page.goto(html.as_uri(), wait_until="networkidle")
        page.pdf(
            path=str(pdf),
            format="A4",
            margin={"top": "14mm", "bottom": "14mm", "left": "14mm", "right": "14mm"},
            print_background=True,
        )
        browser.close()
    print("wrote", pdf)


if __name__ == "__main__":
    main()