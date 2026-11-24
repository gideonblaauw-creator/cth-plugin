#!/usr/bin/env python3
"""Render panel one-pager HTML to PDF and 200 dpi PNG (one A4 page)."""
from __future__ import annotations

import asyncio
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
HTML = ROOT / "panel-0840-dataton-24nov.html"
PDF = ROOT / "Panel-0840-Dataton-24nov.pdf"
PNG = ROOT / "Panel-0840-Dataton-24nov.png"


async def export_pdf() -> None:
    from playwright.async_api import async_playwright

    url = HTML.as_uri()
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = await browser.new_page(viewport={"width": 794, "height": 1123})
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(800)
        await page.pdf(
            path=str(PDF),
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            prefer_css_page_size=True,
        )
        await browser.close()


POPPLER = pathlib.Path("/tmp/poppler-extract/usr/bin")


def poppler_env() -> dict[str, str]:
    import os

    env = os.environ.copy()
    lib = "/tmp/poppler-extract/usr/lib/x86_64-linux-gnu"
    env["PATH"] = f"{POPPLER}:{env.get('PATH', '')}"
    env["LD_LIBRARY_PATH"] = f"{lib}:{env.get('LD_LIBRARY_PATH', '')}"
    return env


def export_png_200dpi() -> None:
    prefix = ROOT / "Panel-0840-Dataton-24nov-ppm"
    subprocess.run(
        ["pdftoppm", "-png", "-r", "200", "-singlefile", str(PDF), str(prefix)],
        check=True,
        env=poppler_env(),
    )
    generated = ROOT / "Panel-0840-Dataton-24nov-ppm.png"
    if generated.is_file():
        generated.rename(PNG)


def prove_font_g() -> None:
    subprocess.run([sys.executable, str(ROOT / "prove-font-g.py")], check=True)


def prove_cobrand() -> None:
    subprocess.run([sys.executable, str(ROOT / "prove-cobrand-crop.py")], check=True)


def build_datalab_lockup() -> None:
    subprocess.run([sys.executable, str(ROOT / "build-datalab-lockup.py")], check=True)


def main() -> None:
    if not HTML.is_file():
        raise SystemExit(f"Missing {HTML}")
    build_datalab_lockup()
    asyncio.run(export_pdf())
    export_png_200dpi()
    prove_font_g()
    prove_cobrand()
    print(PDF)
    print(PNG)


if __name__ == "__main__":
    main()