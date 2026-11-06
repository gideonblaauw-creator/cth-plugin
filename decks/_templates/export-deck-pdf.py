#!/usr/bin/env python3
"""Export a co-located print-ready PDF for CTH HTML decks (HARD 4 Nov 2026).

Forces reveal/animation final states and [data-count] values, then prints with
Chromium (Playwright): A4 landscape, backgrounds on.

Usage:
  python3 export-deck-pdf.py --pdf my-deck.pdf
  python3 export-deck-pdf.py --index /path/to/index.html --pdf out.pdf --mode slides

Requires: playwright (+ chromium). Installed on demand if missing.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

PREP_JS = """
() => {
  document.querySelectorAll('.reveal').forEach(el => el.classList.add('visible'));
  document.querySelectorAll('.reveal-on-scroll').forEach(el => el.classList.add('is-visible'));
  document.querySelectorAll('[data-count]').forEach(el => {
    const t = el.dataset.count;
    if (t !== undefined && t !== '') el.textContent = t;
  });
  if (document.querySelector('.deck .slide')) {
    document.body.classList.add('print-all');
  }
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


def build_url(index: Path, mode: str) -> str:
    uri = index.resolve().as_uri()
    if mode == "slides":
        sep = "&" if "?" in uri else "?"
        return f"{uri}{sep}print"
    return uri


def main() -> None:
    parser = argparse.ArgumentParser(description="Export HTML deck to A4 landscape PDF")
    parser.add_argument("--index", type=Path, default=Path("index.html"), help="Deck index.html")
    parser.add_argument("--pdf", type=Path, required=True, help="Output PDF filename (same folder recommended)")
    parser.add_argument(
        "--mode",
        choices=("auto", "scroll", "slides"),
        default="auto",
        help="scroll: long page; slides: 1920 stage with ?print; auto: slides if .deck .slide exists",
    )
    args = parser.parse_args()

    index = args.index.resolve()
    if not index.is_file():
        raise SystemExit(f"Missing index: {index}")

    ensure_playwright()
    from playwright.sync_api import sync_playwright

    mode = args.mode
    if mode == "auto":
        mode = "slides"  # decided after load if needed

    pdf_out = args.pdf if args.pdf.is_absolute() else (index.parent / args.pdf)
    pdf_out.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        url = build_url(index, "slides" if mode == "slides" else "scroll")
        page.goto(url, wait_until="networkidle")

        has_stage = page.locator(".deck .slide").count() > 0
        if args.mode == "auto":
            mode = "slides" if has_stage else "scroll"
            if mode == "slides" and "?print" not in page.url and "#print" not in page.url:
                page.goto(build_url(index, "slides"), wait_until="networkidle")

        page.evaluate(PREP_JS)
        page.emulate_media(media="print")

        if mode == "slides":
            page.set_viewport_size({"width": 1920, "height": 1080})

        page.pdf(
            path=str(pdf_out),
            format="A4",
            landscape=True,
            print_background=True,
            margin={"top": "0.4in", "right": "0.4in", "bottom": "0.4in", "left": "0.4in"},
        )
        browser.close()

    print("wrote", pdf_out, f"mode={mode}")


if __name__ == "__main__":
    main()
