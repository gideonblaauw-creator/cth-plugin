#!/usr/bin/env python3
"""200 dpi crop of co-brand row."""
from __future__ import annotations

import asyncio
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
HTML = ROOT / "panel-0840-dataton-24nov.html"
OUT = ROOT / "Panel-0840-proof-cobrand-200dpi.png"


async def main() -> None:
    from playwright.async_api import async_playwright

    scale = 200 / 96
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = await browser.new_page(
            viewport={"width": 794, "height": 1123}, device_scale_factor=scale
        )
        await page.goto(HTML.as_uri(), wait_until="networkidle")
        await page.wait_for_timeout(400)
        await page.locator(".cobrand-row").screenshot(path=str(OUT))
        await browser.close()
    print(OUT)


if __name__ == "__main__":
    asyncio.run(main())