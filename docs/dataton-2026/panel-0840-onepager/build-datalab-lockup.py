#!/usr/bin/env python3
"""Rasterize Datalab endorsed lockup (SVG layout + cleantechhub-official.png)."""
from __future__ import annotations

import asyncio
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
ASSETS = ROOT / "assets" / "logos"
OUT = ASSETS / "datalab-lockup.png"


async def main() -> None:
    from playwright.async_api import async_playwright

    svg = (ASSETS / "datalab-lockup.svg").read_text(encoding="utf-8")
    html_path = ASSETS / "_lockup-render.html"
    html_path.write_text(
        f"""<!DOCTYPE html>
<html><head>
<style>
@font-face {{
  font-family: 'Titillium Web';
  font-weight: 700;
  src: url('TitilliumWeb-Bold.ttf') format('truetype');
}}
@font-face {{
  font-family: 'Open Sans';
  font-weight: 600;
  src: url('../../fonts/OpenSans-SemiBold.ttf') format('truetype');
}}
body {{ margin: 0; background: #fff; }}
#wrap {{ display: inline-block; line-height: 0; }}
</style>
</head>
<body><div id="wrap">{svg}</div></body></html>""",
        encoding="utf-8",
    )

    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = await browser.new_page(viewport={"width": 600, "height": 200}, device_scale_factor=3)
        await page.goto(html_path.as_uri(), wait_until="networkidle")
        await page.wait_for_timeout(500)
        wrap = page.locator("#wrap")
        await wrap.screenshot(path=str(OUT), omit_background=False)
        await browser.close()
    print(OUT)


if __name__ == "__main__":
    asyncio.run(main())