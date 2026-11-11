#!/usr/bin/env python3
"""Build slide visual PNGs (no login pages)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VIS = ROOT / "assets" / "visuals"
SRC = VIS / "source"
SIZE = {"width": 920, "height": 1080}


def ensure_playwright() -> None:
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def shot_html(html: Path, out: Path) -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = browser.new_page(viewport=SIZE)
        page.goto(html.as_uri(), wait_until="networkidle")
        page.wait_for_timeout(400)
        page.screenshot(path=str(out), full_page=False)
        browser.close()
    print("wrote", out)


def main() -> int:
    ensure_playwright()
    shot_html(SRC / "clp26-panel.html", VIS / "clp26-panel.png")
    shot_html(SRC / "nexus-grid-panel.html", VIS / "nexus-grid.png")
    shot_html(SRC / "p4g-panel.html", VIS / "p4g-panel.png")
    shot_html(SRC / "rein-panel.html", VIS / "rein-hubs.png")
    # legacy filenames used in index
    for src, dest in (
        ("clp26-panel.png", "clp26-slide.png"),
        ("nexus-grid.png", "nexus-home.png"),
        ("rein-hubs.png", "rein-hubs.png"),
        ("p4g-panel.png", "p4g-panel.png"),
    ):
        p = VIS / src
        if src != dest:
            (VIS / dest).write_bytes(p.read_bytes())
            print("copied", dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
