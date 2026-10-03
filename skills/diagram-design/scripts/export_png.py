#!/usr/bin/env python3
"""Export wire HTML to PNG via Playwright (Chromium, scale 2, solid paper background)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PAPER = "#B2EEFA"


def export_png(html_path: Path, png_path: Path, scale: int = 2) -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise SystemExit(
            "Playwright is required. Install with: pip install playwright && playwright install chromium"
        ) from exc

    html_path = html_path.resolve()
    png_path.parent.mkdir(parents=True, exist_ok=True)
    url = html_path.as_uri()
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(
            device_scale_factor=scale,
            viewport={"width": 1280, "height": 900},
        )
        page.goto(url, wait_until="networkidle")
        page.evaluate(
            """() => document.documentElement.style.background = '%s'"""
            % PAPER
        )
        page.wait_for_timeout(100)
        page.screenshot(path=str(png_path), full_page=True, omit_background=False)
        browser.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--scale", type=int, default=2)
    args = parser.parse_args()
    try:
        export_png(args.html, args.out, scale=args.scale)
    except Exception as exc:  # noqa: BLE001 — CLI surface
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"OK {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
