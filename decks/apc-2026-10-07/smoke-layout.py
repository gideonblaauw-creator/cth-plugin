#!/usr/bin/env python3
"""Smoke: deck letterbox at laptop viewports — slides 01, 07, 13."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"
OUT_DIR = Path("/opt/cursor/artifacts")
OUT_DIR.mkdir(parents=True, exist_ok=True)

VIEWPORTS = [
    ("1366x768", 1366, 768),
    ("1512x982", 1512, 982),
]
SLIDES = [1, 7, 11, 16]


def ensure_playwright():
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def main():
    ensure_playwright()
    from playwright.sync_api import sync_playwright

    url_base = INDEX.as_uri()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for vp_name, w, h in VIEWPORTS:
            page = browser.new_page(viewport={"width": w, "height": h})
            for slide_num in SLIDES:
                page.goto(url_base + f"#{slide_num}", wait_until="networkidle")
                page.wait_for_timeout(200)
                frame = page.locator(".deck-frame")
                box = frame.bounding_box()
                if not box:
                    raise SystemExit(f"No .deck-frame at {vp_name} slide {slide_num}")
                margin = 2
                if box["x"] < -margin or box["y"] < -margin:
                    raise SystemExit(f"Frame off-screen: {box} at {vp_name} #{slide_num}")
                if box["x"] + box["width"] > w + margin:
                    raise SystemExit(f"Frame overflows right: {box} vw={w}")
                if box["y"] + box["height"] > h + margin:
                    raise SystemExit(f"Frame overflows bottom: {box} vh={h}")
                out = OUT_DIR / f"apc-fix-layout-{vp_name}-slide{slide_num:02d}.png"
                page.screenshot(path=str(out), full_page=False)
                print("OK", out, f"frame={box['width']:.0f}x{box['height']:.0f} @ ({box['x']:.0f},{box['y']:.0f})")
                if slide_num == 11:
                    epic_out = OUT_DIR / f"apc-epic-angels-slide11-{vp_name}.png"
                    page.screenshot(path=str(epic_out), full_page=False)
                    print("OK", epic_out)
            page.close()
        browser.close()


if __name__ == "__main__":
    main()
