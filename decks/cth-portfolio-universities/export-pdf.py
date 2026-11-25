#!/usr/bin/env python3
"""Export cth-portfolio-universities index.html to A4 PDF and page PNGs."""
import asyncio
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(ROOT, "index.html")
PDF = os.path.join(ROOT, "portfolio.pdf")


async def main():
    from playwright.async_api import async_playwright

    abs_html = f"file://{HTML}"
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True, args=["--no-sandbox", "--disable-gpu"]
        )
        page = await browser.new_page()
        await page.goto(abs_html, wait_until="networkidle")
        await page.wait_for_timeout(800)
        await page.pdf(
            path=PDF,
            format="A4",
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            print_background=True,
            prefer_css_page_size=True,
        )
        for i in range(1, 5):
            el = page.locator(f"#page-{i}")
            if await el.count():
                await el.screenshot(
                    path=os.path.join(ROOT, f"page-{i}.png"), type="png"
                )
        await browser.close()
    print(PDF)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"playwright failed: {e}", file=sys.stderr)
        sys.exit(1)