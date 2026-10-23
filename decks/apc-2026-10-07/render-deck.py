#!/usr/bin/env python3
"""Render APC deck PDF + per-slide PNGs via Playwright (1920×1080, printBackground)."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"
PDF_OUT = ROOT / "APC-CTH-2026-10-07.pdf"
PNG_DIR = ROOT / "png"


def ensure_playwright():
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        from playwright.sync_api import sync_playwright  # noqa: F401


def main():
    ensure_playwright()
    from playwright.sync_api import sync_playwright

    PNG_DIR.mkdir(parents=True, exist_ok=True)
    url = INDEX.as_uri() + "?print"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
        page.goto(url, wait_until="networkidle")
        page.emulate_media(media="screen")

        slides = page.locator(".deck .slide")
        count = slides.count()
        if count != 21:
            raise SystemExit(f"Expected 21 slides, found {count}")

        for i in range(count):
            nn = f"{i + 1:02d}"
            out = PNG_DIR / f"{nn}.png"
            slides.nth(i).screenshot(path=str(out))
            print("wrote", out)

        page.pdf(
            path=str(PDF_OUT),
            width="1920px",
            height="1080px",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        print("wrote", PDF_OUT)
        browser.close()


if __name__ == "__main__":
    main()
