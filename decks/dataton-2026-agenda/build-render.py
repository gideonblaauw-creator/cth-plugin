#!/usr/bin/env python3
"""Render agenda-dataton-24nov-v4 HTML to PDF and PNG (one A4 page)."""
from __future__ import annotations

import asyncio
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
VERSION = (sys.argv[1] if len(sys.argv) > 1 else "v4").lstrip("v")
HTML = ROOT / f"agenda-dataton-24nov-v{VERSION}.html"
PDF = ROOT / f"agenda-dataton-24nov-v{VERSION}.pdf"
PNG = ROOT / f"agenda-dataton-24nov-v{VERSION}.png"


async def export() -> None:
    from playwright.async_api import async_playwright

    url = HTML.as_uri()
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = await browser.new_page(viewport={"width": 794, "height": 1123})
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(500)
        await page.pdf(
            path=str(PDF),
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            prefer_css_page_size=True,
        )
        sheet = page.locator("article.sheet")
        await sheet.screenshot(path=str(PNG))
        await browser.close()


def main() -> None:
    if not HTML.is_file():
        raise SystemExit(f"Missing {HTML}")
    asyncio.run(export())
    print(PDF)
    print(PNG)


if __name__ == "__main__":
    main()