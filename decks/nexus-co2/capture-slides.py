#!/usr/bin/env python3
"""Capture each slide at 1440×900 (navigation mode, one slide active)."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"
OUT_DIR = Path("/opt/cursor/artifacts/nexus-co2-slides")


def ensure_playwright():
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def main():
    ensure_playwright()
    from playwright.sync_api import sync_playwright

    if not INDEX.is_file():
        raise SystemExit("Run ./build.sh first")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    base = INDEX.as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        count = page.locator(".deck .slide").count()
        paths = []
        for i in range(1, 20):
            page.goto(f"{base}#{i}", wait_until="networkidle")
            page.wait_for_timeout(400)
            slides = page.locator(".deck .slide")
            if slides.count() < i:
                break
            out = OUT_DIR / f"slide-{i:02d}-1440x900.png"
            page.screenshot(path=str(out), full_page=False)
            paths.append(out)
            print("wrote", out)
        browser.close()
    print(f"Captured {len(paths)} slides")


if __name__ == "__main__":
    main()
