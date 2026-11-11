#!/usr/bin/env python3
"""Capture energiacoop demo screenshots (ES + EN)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets" / "demo"
ASSETS.mkdir(parents=True, exist_ok=True)
DEMO_DIR = Path(__file__).resolve().parent.parent / "demo-cth-brand"
VIEWPORT = {"width": 1440, "height": 900}
SCREENS = 7
BANNED = re.compile(r"promigas", re.I)
PROMIGAS_SCREENS: list[int] = []


def ensure_playwright():
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def click_animate_if_present(page) -> None:
    btn = page.locator("#btn-transform")
    if not btn.count():
        return
    btn.scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    btn.click(force=True)
    page.wait_for_timeout(3000)


def capture_lang(lang: str) -> None:
    from playwright.sync_api import sync_playwright

    suffix = "es" if lang == "es" else "en"
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = browser.new_page(viewport=VIEWPORT)
        page.goto(DEMO_DIR.joinpath("index.html").as_uri(), wait_until="networkidle", timeout=120000)
        page.wait_for_timeout(2000)
        if lang == "en":
            for sel in (
                "button:has-text('EN')",
                "[data-lang='en']",
                "button:has-text('English')",
            ):
                loc = page.locator(sel)
                if loc.count():
                    loc.first.click()
                    page.wait_for_timeout(800)
                    break
        for i in range(SCREENS):
            path = ASSETS / f"demo-{suffix}-{i + 1:02d}.png"
            if i > 0:
                nxt = page.locator("#nav-next")
                if nxt.count():
                    nxt.click()
                else:
                    page.keyboard.press("ArrowRight")
                page.wait_for_timeout(1800)
            if i == 0:
                click_animate_if_present(page)
            page.wait_for_timeout(1200)
            page.screenshot(path=str(path), full_page=False)
            text = page.inner_text("body")
            if BANNED.search(text):
                PROMIGAS_SCREENS.append(i + 1)
            print("wrote", path)
        browser.close()


def main() -> int:
    ensure_playwright()
    capture_lang("es")
    capture_lang("en")
    if PROMIGAS_SCREENS:
        print("PROMIGAS_VISIBLE_ON_SCREENS:", sorted(set(PROMIGAS_SCREENS)), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
