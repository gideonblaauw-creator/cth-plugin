#!/usr/bin/env python3
"""Export cth-portfolio-universities index.html to A4 PDF and page PNGs."""
import asyncio
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(ROOT, "index.html")
PDF = os.path.join(ROOT, "portfolio.pdf")
A4_HEIGHT_PX_TOLERANCE = 3


async def assert_pages_fit_a4(page) -> None:
    """Fail export if any .page content exceeds fixed A4 sheet height."""
    report = await page.evaluate(
        """() => {
          const pages = [...document.querySelectorAll('.page')];
          return pages.map((el) => ({
            id: el.id || el.className,
            scrollHeight: el.scrollHeight,
            clientHeight: el.clientHeight,
            overflow: el.scrollHeight > el.clientHeight + 2,
          }));
        }"""
    )
    bad = [r for r in report if r["overflow"]]
    if bad:
        details = "; ".join(
            f"{r['id']}: scroll={r['scrollHeight']} client={r['clientHeight']}"
            for r in bad
        )
        raise SystemExit(f"A4 overflow check failed: {details}")
    for r in report:
        print(f"OK {r['id']}: {r['clientHeight']}px")


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
        await assert_pages_fit_a4(page)
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
    except SystemExit:
        raise
    except Exception as e:
        print(f"playwright failed: {e}", file=sys.stderr)
        sys.exit(1)