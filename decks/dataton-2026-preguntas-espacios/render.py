#!/usr/bin/env python3
"""Render A4 PDF and per-page PNGs from index.html."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"
PDF_OUT = ROOT / "dataton-preguntas-espacios.pdf"
PNG_DIR = ROOT / "_png"


def ensure_playwright():
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def main() -> None:
    ensure_playwright()
    from playwright.sync_api import sync_playwright

    if not INDEX.is_file():
        raise SystemExit("Run generate.py first")

    PNG_DIR.mkdir(parents=True, exist_ok=True)
    url = INDEX.as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        # A4 at ~96dpi CSS pixels
        page = browser.new_page(viewport={"width": 794, "height": 1123}, device_scale_factor=2)
        page.goto(url, wait_until="networkidle")
        page.emulate_media(media="print")

        pages = page.locator("section.page")
        count = pages.count()
        if count != 17:
            raise SystemExit(f"Expected 17 pages, got {count}")

        for i in range(count):
            out = PNG_DIR / f"p{i + 1:02d}.png"
            pages.nth(i).scroll_into_view_if_needed()
            pages.nth(i).screenshot(path=str(out))
            print("wrote", out)

        page.pdf(
            path=str(PDF_OUT),
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        print("wrote", PDF_OUT)
        browser.close()


if __name__ == "__main__":
    main()