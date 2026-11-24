#!/usr/bin/env python3
"""Print rendered logo heights in mm (Playwright, A4 viewport)."""
from __future__ import annotations

import asyncio
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
HTML = ROOT / "panel-0840-dataton-24nov.html"
OUT = ROOT / "logo-heights-mm.json"

PX_PER_MM = 96 / 25.4

ITEMS = [
    (".datalab-lockup-wrap img", "datalab_lockup_mm"),
    (".partner-logos img:nth-child(1)", "externado_mm"),
    (".partner-logos img:nth-child(2)", "observatorio_mm"),
]


async def main() -> None:
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = await browser.new_page(viewport={"width": 794, "height": 1123})
        await page.goto(HTML.as_uri(), wait_until="networkidle")
        out: dict[str, float] = {}
        for sel, key in ITEMS:
            h_px = await page.locator(sel).evaluate(
                "el => el.getBoundingClientRect().height"
            )
            out[key] = round(h_px / PX_PER_MM, 2)
        await browser.close()

    OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    for k, v in out.items():
        print(f"{k}: {v} mm")


if __name__ == "__main__":
    asyncio.run(main())