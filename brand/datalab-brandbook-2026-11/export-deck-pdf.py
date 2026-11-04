#!/usr/bin/env python3
"""Export brand book PDF: A4 landscape, one slide per page, embedded fonts (Playwright)."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

PREP_JS = """
() => {
  document.body.classList.add('print-all', 'es');
  document.querySelectorAll('.deck .slide').forEach(el => {
    el.classList.add('active');
    el.style.display = 'flex';
  });
  document.querySelectorAll('.topbar, .site-footer, .pdf-dl-fixed').forEach(el => {
    el.style.display = 'none';
  });
  document.querySelectorAll('*').forEach(el => {
    el.style.setProperty('animation', 'none', 'important');
    el.style.setProperty('transition', 'none', 'important');
  });
}
"""


def ensure_playwright() -> None:
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Export HTML brand book to A4 landscape PDF")
    parser.add_argument("--index", type=Path, default=Path("index.html"))
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--mode", choices=("auto", "scroll", "slides"), default="auto")
    args = parser.parse_args()

    index = args.index.resolve()
    pdf_out = args.pdf if args.pdf.is_absolute() else (index.parent / args.pdf)
    pdf_out.parent.mkdir(parents=True, exist_ok=True)

    ensure_playwright()
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=True,
            args=["--no-sandbox", "--disable-gpu", "--font-render-hinting=none"],
        )
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        page.goto(index.as_uri(), wait_until="networkidle")
        page.wait_for_timeout(400)
        page.evaluate(PREP_JS)
        page.emulate_media(media="print")
        page.pdf(
            path=str(pdf_out),
            format="A4",
            landscape=True,
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()

    print("wrote", pdf_out, "mode=slides engine=playwright-a4")


if __name__ == "__main__":
    main()
