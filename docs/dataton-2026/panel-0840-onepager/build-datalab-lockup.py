#!/usr/bin/env python3
"""Rasterize Datalab lockup (#134 layout) and tune cap height vs Externado."""
from __future__ import annotations

import asyncio
import io
import json
import pathlib
import re

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
ASSETS = ROOT / "assets" / "logos"
OUT = ASSETS / "datalab-lockup.png"
SVG_OUT = ASSETS / "datalab-lockup.svg"
CONFIG = ROOT / "lockup-config.json"
HTML = ROOT / "panel-0840-dataton-24nov.html"

PB_FONT = 20
WM_FONT = 42
CTH_W, CTH_H = 148, 40
PARTNER_H_MM = 7.0
VB_H = 118


def make_svg() -> tuple[str, int]:
    s = 1.0
    g = 8 * s
    grid = f"""<g transform="translate({g}, {14*s})">
    <rect x="0" y="0" width="{26*s}" height="{26*s}" rx="{4*s}" fill="#0C498A"/>
    <rect x="{31*s}" y="0" width="{26*s}" height="{26*s}" rx="{4*s}" fill="#69B5FA"/>
    <rect x="{62*s}" y="0" width="{26*s}" height="{26*s}" rx="{4*s}" fill="#0C498A"/>
    <rect x="0" y="{31*s}" width="{26*s}" height="{26*s}" rx="{4*s}" fill="#B2EEFA" stroke="#0C498A" stroke-width="1"/>
    <rect x="{31*s}" y="{31*s}" width="{26*s}" height="{26*s}" rx="{4*s}" fill="#669348"/>
    <rect x="{62*s}" y="{31*s}" width="{26*s}" height="{26*s}" rx="{4*s}" fill="#B2EEFA" stroke="#0C498A" stroke-width="1"/>
    <rect x="0" y="{62*s}" width="{26*s}" height="{26*s}" rx="{4*s}" fill="#B2EEFA" stroke="#0C498A" stroke-width="1"/>
    <rect x="{31*s}" y="{62*s}" width="{26*s}" height="{26*s}" rx="{4*s}" fill="#69B5FA"/>
    <rect x="{62*s}" y="{62*s}" width="{26*s}" height="{26*s}" rx="{4*s}" fill="#0C498A"/>
  </g>"""
    tx = 118 * s
    wm = WM_FONT * s
    pb = PB_FONT * s
    cthw, cthh = CTH_W * s, CTH_H * s
    vb_w = int(tx + cthw + 12 * s)
    vb_h = int((72 * s) + cthh + 8 * s)
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb_w} {vb_h}" width="{vb_w}" height="{vb_h}"
  role="img" aria-label="Datalab powered by CleantechHUB lockup">
  {grid}
  <text x="{tx}" y="{54*s}" font-family="'Titillium Web', sans-serif" font-weight="700"
    font-size="{wm}" fill="#0C498A">Datalab</text>
  <text x="{tx}" y="{70*s}" font-family="'Open Sans', sans-serif" font-weight="600"
    font-size="{pb}" fill="#669348">powered by</text>
  <image href="cleantechhub-official.png" x="{tx}" y="{73*s}" width="{cthw}" height="{cthh}"
    preserveAspectRatio="xMinYMid meet"/>
</svg>"""
    SVG_OUT.write_text(svg, encoding="utf-8")
    return svg, vb_h


def set_lockup_height(mm: float) -> None:
    html = HTML.read_text(encoding="utf-8")
    html = re.sub(
        r"(\.datalab-lockup-wrap img \{\s*height: )[0-9.]+mm;",
        rf"\g<1>{mm:.2f}mm;",
        html,
        count=1,
    )
    HTML.write_text(html, encoding="utf-8")


def caps_from_cobrand_png(png_bytes: bytes, lock_h_mm: float, ext_h_mm: float) -> tuple[float, float]:
    im = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
    w, h = im.size
    mid = int(w * 0.58)
    lock = im.crop((0, 0, mid, h))
    ext = im.crop((int(w * 0.68), 0, w, h))
    lr = lock.crop((int(lock.size[0] * 0.32), 0, lock.size[0], int(lock.size[1] * 0.43)))
    px = lr.load()
    miny, maxy = lr.size[1], 0
    for y in range(lr.size[1]):
        for x in range(lr.size[0]):
            if px[x, y][3] > 48:
                miny = min(miny, y)
                maxy = max(maxy, y)
    dl = lock_h_mm * (maxy - miny + 1) / lr.size[1] if maxy > miny else 0
    ep = ext.load()
    ew, eh = ext.size
    miny, maxy = eh, 0
    for y in range(eh):
        for x in range(ew):
            if ep[x, y][3] > 48:
                miny = min(miny, y)
                maxy = max(maxy, y)
    ex = ext_h_mm * (maxy - miny + 1) / eh * 0.82 if maxy > miny else 0
    return dl, ex


async def rasterize(svg: str) -> None:
    from playwright.async_api import async_playwright

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
        page = await browser.new_page(viewport={"width": 900, "height": 360}, device_scale_factor=3)
        await page.goto(html_path.as_uri(), wait_until="networkidle")
        await page.wait_for_timeout(400)
        await page.locator("#wrap").screenshot(path=str(OUT), omit_background=False)
        await browser.close()


async def measure_externado_cap() -> float:
    from playwright.async_api import async_playwright

    scale = 300 / 96
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = await browser.new_page(
            viewport={"width": 794, "height": 1123}, device_scale_factor=scale
        )
        set_lockup_height(18.0)
        await page.goto(HTML.as_uri(), wait_until="networkidle")
        shot = await page.locator(".cobrand-row").screenshot(type="png")
        await browser.close()
    _, ex = caps_from_cobrand_png(shot, 18.0, PARTNER_H_MM)
    return ex


async def tune_height(svg: str, vb_h: int) -> float:
    ex_cap = await measure_externado_cap()
    h = ex_cap * vb_h / (0.72 * WM_FONT)
    if h * PB_FONT / vb_h * (72 / 25.4) < 7.0:
        h = 7.0 * vb_h / PB_FONT / (72 / 25.4)
    if h * CTH_H / vb_h < 4.5:
        h = 4.5 * vb_h / CTH_H
    set_lockup_height(h)
    await rasterize(svg)
    return h


async def main() -> None:
    svg, vb_h = make_svg()
    h = await tune_height(svg, vb_h)
    cfg = {"lockup_height_mm": round(h, 2), "partner_height_mm": PARTNER_H_MM}
    CONFIG.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
    print(OUT)
    print(json.dumps(cfg))


if __name__ == "__main__":
    asyncio.run(main())