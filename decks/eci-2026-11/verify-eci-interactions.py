#!/usr/bin/env python3
"""Headless smoke test for decks/eci-2026-11: nav, filters, explorer, tabs, stepper.

Run from repo root with a local server, e.g.:
  cd decks/eci-2026-11 && python3 -m http.server 8765 &
  python3 verify-eci-interactions.py http://127.0.0.1:8765
"""
from __future__ import annotations

import sys

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("install: pip install playwright && playwright install chromium", file=sys.stderr)
    raise


def main() -> None:
    base = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:8765"
    url = base + "/index.html"
    errors: list[str] = []
    warnings: list[str] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        def on_console(msg) -> None:  # noqa: ANN001
            t = msg.type
            text = msg.text
            if t == "error":
                errors.append(text)
            elif t == "warning":
                warnings.append(text)

        page.on("console", on_console)
        page.on("pageerror", lambda exc: errors.append(f"pageerror: {exc}"))

        page.goto(url, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(800)

        # Nav: click each section link
        for a in page.locator("#nav a[href^='#']").all():
            a.click()
            page.wait_for_timeout(120)

        page.goto(url + "#clp", wait_until="networkidle")
        page.wait_for_timeout(600)

        # Global filters
        gc = page.locator("#gfCountry")
        if gc.count():
            opt_count = gc.locator("option").count()
            if opt_count > 2:
                gc.select_option(index=2)
            page.wait_for_timeout(200)
            page.locator("#gfReset").click()
            page.wait_for_timeout(200)

        # Chart chips
        for chip in page.locator(".chip-filter:not(.on)").all()[:4]:
            chip.click()
            page.wait_for_timeout(150)

        # Explorer
        page.locator("#exQ").fill("a")
        page.wait_for_timeout(150)
        page.locator("#exQ").fill("")
        page.wait_for_timeout(150)

        ex = page.locator("#exCountry")
        if ex.count() and ex.locator("option").count() > 2:
            ex.select_option(index=2)
            page.wait_for_timeout(200)

        # Datalab tabs
        page.goto(url + "#datalab", wait_until="domcontentloaded")
        page.wait_for_timeout(300)
        for tab in page.locator(".env-tab").all():
            tab.click()
            page.wait_for_timeout(120)

        # Stepper
        page.goto(url + "#work", wait_until="domcontentloaded")
        page.wait_for_timeout(300)
        for btn in page.locator("#workStepper .stepper-btn").all():
            btn.click()
            page.wait_for_timeout(120)

        browser.close()

    log_lines = [
        "url: " + url,
        "console_errors: " + str(len(errors)),
        "console_warnings: " + str(len(warnings)),
    ]
    for e in errors:
        log_lines.append("ERROR: " + e)
    for w in warnings:
        log_lines.append("WARN: " + w)

    out_path = "/opt/cursor/artifacts/eci-deck-interaction-check.log"
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(log_lines) + "\n")
    except OSError:
        out_path = "eci-deck-interaction-check.log"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(log_lines) + "\n")

    print("\n".join(log_lines))
    if errors:
        print("FAIL: console had errors", file=sys.stderr)
        sys.exit(1)
    print("OK — wrote", out_path)


if __name__ == "__main__":
    main()
