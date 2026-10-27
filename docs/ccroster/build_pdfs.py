#!/usr/bin/env python3
"""Build A4 PDFs from CC roster HTML sources (Playwright/Chromium)."""
import asyncio
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

PAGES = [
    ("CCRoster_Blaauw_Research.html", "CCRoster_Blaauw_Research.pdf"),
    ("CCRoster_Blaauw_Client.html", "CCRoster_Blaauw_Client.pdf"),
]


async def html_to_pdf(html_name: str, pdf_name: str) -> str:
    from playwright.async_api import async_playwright

    html_path = os.path.join(ROOT, html_name)
    pdf_path = os.path.join(ROOT, pdf_name)
    defaults = {
        "format": "A4",
        "margin": {"top": "10mm", "right": "10mm", "bottom": "10mm", "left": "10mm"},
        "print_background": True,
        "prefer_css_page_size": True,
    }
    abs_html = os.path.abspath(html_path)
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True, args=["--no-sandbox", "--disable-gpu"]
        )
        page = await browser.new_page()
        await page.goto(f"file://{abs_html}", wait_until="networkidle")
        await page.wait_for_timeout(1500)
        await page.pdf(path=pdf_path, **defaults)
        await browser.close()
    return pdf_path


async def main() -> int:
    for html, pdf in PAGES:
        if not os.path.isfile(os.path.join(ROOT, html)):
            print(f"Missing {html}", file=sys.stderr)
            return 1
        out = await html_to_pdf(html, pdf)
        print(f"Wrote {out} ({os.path.getsize(out)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
