#!/usr/bin/env python3
"""R6 metrics from rendered layout + 300 dpi co-brand crop."""
from __future__ import annotations

import asyncio
import importlib.util
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
HTML = ROOT / "panel-0840-dataton-24nov.html"
PNG300 = ROOT / "Panel-0840-proof-cobrand-300dpi.png"
OUT = ROOT / "r6-measurements.json"
PX_PER_MM = 96 / 25.4


def load_lockup_mod():
    spec = importlib.util.spec_from_file_location(
        "build_datalab_lockup", ROOT / "build-datalab-lockup.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


async def layout_metrics() -> dict:
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = await browser.new_page(viewport={"width": 794, "height": 1123})
        await page.goto(HTML.as_uri(), wait_until="networkidle")
        data = await page.evaluate(
            f"""() => {{
              const PX = {PX_PER_MM};
              const pt = (px) => px * 72 / 96;
              const mm = (px) => px / PX;
              const lockImg = document.querySelector('.datalab-lockup-wrap img');
              const extImg = document.querySelector('.partner-logos img:nth-child(1)');
              const closing = document.querySelector('.closing');
              const footBand = document.querySelector('.letterhead-bottom');
              return {{
                body_pt: pt(parseFloat(getComputedStyle(document.querySelector('.lead')).fontSize)),
                lockup_display_h_mm: mm(lockImg.getBoundingClientRect().height),
                externado_display_h_mm: mm(extImg.getBoundingClientRect().height),
                footer_gap_mm: mm(footBand.getBoundingClientRect().top - closing.getBoundingClientRect().bottom),
              }};
            }}"""
        )
        await browser.close()
    return data


async def main() -> None:
    mod = load_lockup_mod()
    layout = await layout_metrics()
    h = layout["lockup_display_h_mm"]
    _, ex_cap = mod.caps_from_cobrand_png(
        PNG300.read_bytes(),
        h,
        layout["externado_display_h_mm"],
    )
    wm = mod.WM_FONT
    vb_h = mod.VB_H
    pb = mod.PB_FONT
    cth = mod.CTH_H
    dl_cap = h * (0.72 * wm) / vb_h
    metrics = {
        "datalab_cap_height_mm": round(dl_cap, 2),
        "externado_cap_height_mm": round(ex_cap, 2),
        "powered_by_pt": round(h * pb / vb_h * (72 / 25.4), 2),
        "cth_logo_height_mm": round(h * cth / vb_h, 2),
        "footer_gap_mm": round(layout["footer_gap_mm"], 2),
        "body_pt": round(layout["body_pt"], 2),
        "cap_height_ratio": round(dl_cap / ex_cap, 3) if ex_cap else 0,
    }
    OUT.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    for k, v in metrics.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    asyncio.run(main())