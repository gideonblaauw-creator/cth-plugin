#!/usr/bin/env python3
"""Export Open Air Sandbox one-pager HTML to A4 portrait PDF (2 pages)."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def ensure_playwright() -> None:
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def export_pdf(html: Path, pdf: Path) -> None:
    ensure_playwright()
    from playwright.sync_api import sync_playwright

    uri = html.resolve().as_uri()
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = browser.new_page(viewport={"width": 794, "height": 1123})
        page.goto(uri, wait_until="networkidle")
        page.emulate_media(media="print")
        page.pdf(
            path=str(pdf),
            format="A4",
            landscape=False,
            print_background=True,
            prefer_css_page_size=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()


def export_page_pngs(html: Path, out_dir: Path, prefix: str) -> list[Path]:
    ensure_playwright()
    from playwright.sync_api import sync_playwright

    uri = html.resolve().as_uri()
    paths: list[Path] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = browser.new_page(viewport={"width": 794, "height": 1123})
        page.goto(uri, wait_until="networkidle")
        for i, sel in enumerate([".page-1", ".page-2"], start=1):
            loc = page.locator(sel)
            out = out_dir / f"{prefix}-page-{i}.png"
            loc.screenshot(path=str(out))
            paths.append(out)
        browser.close()
    return paths


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--html", type=Path, required=True)
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--png-prefix", type=str, default="")
    args = parser.parse_args()

    html = args.html.resolve()
    pdf = args.pdf if args.pdf.is_absolute() else html.parent / args.pdf
    export_pdf(html, pdf)
    print("wrote", pdf)

    prefix = args.png_prefix or html.stem.replace("open-air-sandbox-", "")
    pngs = export_page_pngs(html, html.parent, f"open-air-sandbox-{prefix}")
    for p in pngs:
        print("wrote", p)


if __name__ == "__main__":
    main()
