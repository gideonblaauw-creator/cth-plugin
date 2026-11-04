#!/usr/bin/env python3
"""Capture each main section and deck-source card at 1440×900."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
OUT_DIR = Path("/opt/cursor/artifacts/nexus-co2-slides")

SECTIONS = [
    "hero",
    "method",
    "explore",
    "chart",
    "table",
    "coverage",
    "deck-cards",
]


def ensure_playwright():
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def main():
    ensure_playwright()
    from playwright.sync_api import sync_playwright

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    base = "http://127.0.0.1:8765/index.html"

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(base, wait_until="networkidle")
        page.wait_for_timeout(800)
        paths = []
        for i, sec in enumerate(SECTIONS, start=1):
            el = page.locator(f"#{sec}")
            if el.count():
                el.scroll_into_view_if_needed()
                page.wait_for_timeout(400)
                out = OUT_DIR / f"slide-{i:02d}-{sec}-1440x900.png"
                page.screenshot(path=str(out), full_page=False)
                paths.append(out)
                print("wrote", out)
        cards = page.locator("#deck-card-grid .deck-card")
        for j in range(cards.count()):
            cards.nth(j).scroll_into_view_if_needed()
            page.wait_for_timeout(300)
            slug = cards.nth(j).get_attribute("id") or f"card-{j}"
            out = OUT_DIR / f"deck-card-{j + 1:02d}-{slug.replace('deck-card-', '')}-1440x900.png"
            page.screenshot(path=str(out), full_page=False)
            paths.append(out)
            print("wrote", out)
        browser.close()
    print(f"Captured {len(paths)} screenshots")


if __name__ == "__main__":
    main()
