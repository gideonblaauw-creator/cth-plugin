#!/usr/bin/env python3
"""Report computed font-size (pt) for text classes; min must be >= 9.5."""
from __future__ import annotations

import asyncio
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
HTML = ROOT / "panel-0840-dataton-24nov.html"
MIN_PT = 10.0

SELECTORS = [
    ("h1", "h1"),
    (".meta-line", ".meta-line"),
    (".meta-venue", ".meta-venue"),
    (".lead", ".lead"),
    (".section-title", ".section-title"),
    (".bullet-list li", ".bullet-list li"),
    ("ul.questions-list li", "ul.questions-list li"),
    (".body-text", ".body-text"),
    (".closing", ".closing"),
    (".tagline", ".tagline"),
]


async def main() -> int:
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = await browser.new_page(viewport={"width": 794, "height": 1123})
        await page.goto(HTML.as_uri(), wait_until="networkidle")
        rows: list[tuple[str, float]] = []
        for label, sel in SELECTORS:
            pt = await page.locator(sel).first.evaluate(
                """el => {
                  const px = parseFloat(getComputedStyle(el).fontSize);
                  return px * 72 / 96;
                }"""
            )
            rows.append((label, round(pt, 2)))
        await browser.close()

    print("=== computed font sizes (pt) ===")
    ok = True
    min_seen = min(pt for _, pt in rows)
    for label, pt in rows:
        flag = "OK" if pt >= MIN_PT else "FAIL"
        if pt < MIN_PT:
            ok = False
        print(f"{label}: {pt} pt [{flag}]")
    print(f"minimum: {min_seen} pt (required >= {MIN_PT})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))