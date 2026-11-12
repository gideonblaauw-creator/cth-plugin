#!/usr/bin/env python3
"""Render javeriana deck to PDF (16:9) and preview PNGs."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"
PDF_OUT = ROOT / "javeriana-2026-11.pdf"
ARTIFACTS = Path("/opt/cursor/artifacts")


def ensure_playwright():
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def main():
    ensure_playwright()
    from playwright.sync_api import sync_playwright

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    url = INDEX.as_uri() + "?print"

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=2)
        page.goto(url, wait_until="networkidle", timeout=120000)
        page.emulate_media(media="screen")
        slides = page.locator(".deck .slide")
        count = slides.count()
        if count < 1:
            raise SystemExit("No slides in the DOM")
        preview_indices = [0, min(4, count - 1), count - 1]
        for i in preview_indices:
            out = ARTIFACTS / f"javeriana-slide-{i + 1:02d}.png"
            slides.nth(i).screenshot(path=str(out))
            print("preview", out)
        png_dir = ROOT / "_render_png"
        png_dir.mkdir(exist_ok=True)
        png_paths = []
        for i in range(count):
            out = png_dir / f"{i + 1:02d}.png"
            slides.nth(i).screenshot(path=str(out))
            png_paths.append(out)
        try:
            import img2pdf
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "img2pdf", "-q"])
            import img2pdf
        layout = img2pdf.get_layout_fun((img2pdf.mm_to_pt(508), img2pdf.mm_to_pt(285.75)))
        with open(PDF_OUT, "wb") as pdf_file:
            pdf_file.write(img2pdf.convert([str(p) for p in png_paths], layout_fun=layout))
        print("wrote", PDF_OUT, f"({len(png_paths)} pages)")
        browser.close()


if __name__ == "__main__":
    main()
