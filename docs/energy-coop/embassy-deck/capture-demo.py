#!/usr/bin/env python3
"""Capture live energiacoop demo screenshots (ES + EN)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets" / "demo"
ASSETS.mkdir(parents=True, exist_ok=True)
LIVE_URL = "https://energiacoop.cleantechhub.net/demo/"
VIEWPORT = {"width": 1600, "height": 900}
SCALE = 2
SCREENS = 6
BANNED = re.compile(r"promigas", re.I)
PROMIGAS_SCREENS: list[int] = []


def ensure_playwright():
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def active_title(page) -> str:
    loc = page.locator("section.screen.active h1")
    if loc.count():
        return loc.first.inner_text().strip()
    return ""


def click_animate_if_present(page) -> None:
    btn = page.locator("#btn-transform")
    if not btn.count():
        return
    btn.scroll_into_view_if_needed()
    page.wait_for_timeout(400)
    btn.click(force=True)
    page.wait_for_timeout(3500)


def capture_lang(lang: str) -> list[str]:
    from playwright.sync_api import sync_playwright

    suffix = "es" if lang == "es" else "en"
    titles: list[str] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        context = browser.new_context(
            viewport=VIEWPORT,
            device_scale_factor=SCALE,
        )
        page = context.new_page()
        page.goto(LIVE_URL, wait_until="networkidle", timeout=120000)
        page.wait_for_timeout(2500)
        if lang == "en":
            page.locator("[data-lang='en']").click(force=True)
            page.wait_for_timeout(1000)
        for i in range(SCREENS):
            page.evaluate(
                """(idx) => {
                  if (typeof goTo === 'function') goTo(idx);
                  else document.querySelectorAll('section.screen').forEach((s, j) => {
                    s.classList.toggle('active', j === idx);
                  });
                }""",
                i,
            )
            page.wait_for_timeout(1800)
            if i == 0:
                click_animate_if_present(page)
            if i == 1:
                btn = page.locator("#btn-guajira")
                if btn.count():
                    try:
                        if btn.is_enabled():
                            btn.click()
                            page.wait_for_timeout(3000)
                    except Exception:
                        pass
            page.wait_for_timeout(800)
            title = active_title(page)
            titles.append(title)
            path = ASSETS / f"demo-{suffix}-{i + 1:02d}.png"
            page.screenshot(path=str(path), full_page=False)
            if title and not title[0].isalnum() and title[0] not in "¿¡":
                print("WARN title may be clipped:", repr(title), file=sys.stderr)
            text = page.inner_text("body")
            if BANNED.search(text):
                PROMIGAS_SCREENS.append(i + 1)
            print("wrote", path, "|", title[:60])
        context.close()
        browser.close()
    return titles


def main() -> int:
    ensure_playwright()
    es_titles = capture_lang("es")
    en_titles = capture_lang("en")
    print("ES titles:", es_titles)
    print("EN titles:", en_titles)
    if PROMIGAS_SCREENS:
        print("PROMIGAS_VISIBLE_ON_SCREENS:", sorted(set(PROMIGAS_SCREENS)), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
