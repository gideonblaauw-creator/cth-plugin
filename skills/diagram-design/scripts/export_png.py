#!/usr/bin/env python3
"""Export wire HTML to PNG via Playwright (Chromium, scale 2, solid paper background)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PAPER = "#F7FBFD"


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
        page = browser.new_page(device_scale_factor=scale)
        page.goto(url, wait_until="networkidle")
        page.evaluate(
            """() => {
              document.documentElement.style.background = '%s';
              document.body.style.background = '%s';
              document.body.style.padding = '0';
              document.body.style.margin = '0';
            }"""
            % (PAPER, PAPER)
        )
        page.wait_for_function("document.fonts.ready")
        svg = page.locator(".diagram svg").first
        svg.wait_for(state="visible")
        box = svg.bounding_box()
        if box:
            page.set_viewport_size(
                {
                    "width": max(1, int(box["width"])),
                    "height": max(1, int(box["height"])),
                }
            )
        svg.screenshot(path=str(png_path), omit_background=False)
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
