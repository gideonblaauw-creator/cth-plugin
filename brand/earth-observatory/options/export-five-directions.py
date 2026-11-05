#!/usr/bin/env python3
"""Export EO five visual directions (IG + banner composites, PDF, contact sheet)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OPTIONS = Path(__file__).resolve().parent


def ensure_playwright() -> None:
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "playwright", "-q"],
            env={**__import__("os").environ, "PYTHONPATH": ""},
        )
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def main() -> None:
    ensure_playwright()
    from playwright.sync_api import sync_playwright

    meta = json.loads((OPTIONS / "directions-meta.json").read_text(encoding="utf-8"))
    composites = [
        (OPTIONS / f"dir-{i:02d}-composite.html", OPTIONS / f"eo-dir-{i}.png", 2704, 1080)
        for i in range(1, 6)
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = browser.new_page()

        for html, png, w, h in composites:
            page.set_viewport_size({"width": w, "height": h})
            page.goto(html.resolve().as_uri(), wait_until="networkidle")
            page.screenshot(path=str(png), full_page=False)

        pdf_html = OPTIONS / "eo-5-directions-print.html"
        page.goto(pdf_html.resolve().as_uri(), wait_until="networkidle")
        page.emulate_media(media="print")
        page.pdf(
            path=str(OPTIONS / "eo-5-directions.pdf"),
            format="A4",
            landscape=False,
            print_background=True,
            margin={"top": "0.35in", "right": "0.35in", "bottom": "0.35in", "left": "0.35in"},
        )

        page.set_viewport_size({"width": 2800, "height": 3200})
        page.goto((OPTIONS / "contact-sheet.html").resolve().as_uri(), wait_until="networkidle")
        page.screenshot(path=str(OPTIONS / "contact-sheet.png"), full_page=True)

        browser.close()

    print("Wrote options under", OPTIONS)
    for d in meta["directions"]:
        i = d["id"]
        print(f"  eo-dir-{i}.png")


if __name__ == "__main__":
    main()
