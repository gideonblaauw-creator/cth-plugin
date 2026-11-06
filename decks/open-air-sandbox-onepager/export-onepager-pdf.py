#!/usr/bin/env python3
"""Export Open Air Sandbox one-pager HTML to A4 portrait PDF (2 pages)."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def ensure_playwright() -> None:
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def ensure_pdftoppm() -> None:
    if shutil.which("pdftoppm"):
        return
    subprocess.check_call(["sudo", "apt-get", "update", "-qq"])
    subprocess.check_call(["sudo", "apt-get", "install", "-y", "-qq", "poppler-utils"])


def export_pdf(html: Path, pdf: Path) -> None:
    ensure_playwright()
    from playwright.sync_api import sync_playwright

    uri = html.resolve().as_uri()
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = browser.new_page(viewport={"width": 794, "height": 1123})
        page.goto(uri, wait_until="networkidle")
        page.emulate_media(media="print")
        page.pdf(
            path=str(pdf),
            format="A4",
            landscape=False,
            print_background=True,
            prefer_css_page_size=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()


def rasterize_pdf_pages(pdf: Path, out_dir: Path, stem: str) -> list[Path]:
    """Rasterize PDF pages with pdftoppm (verification PNGs)."""
    ensure_pdftoppm()
    prefix = out_dir / f"{stem}-pdftoppm"
    subprocess.check_call(
        ["pdftoppm", "-png", "-r", "150", str(pdf.resolve()), str(prefix)],
    )
    paths: list[Path] = []
    for i in range(1, 20):
        src = out_dir / f"{stem}-pdftoppm-{i:02d}.png"
        if not src.is_file():
            src = out_dir / f"{stem}-pdftoppm-{i}.png"
        if not src.is_file():
            break
        dest = out_dir / f"{stem}-page-{i}.png"
        src.replace(dest)
        paths.append(dest)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--html", type=Path, required=True)
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--lang", type=str, default="", help="es or en for output PNG names")
    args = parser.parse_args()

    html = args.html.resolve()
    pdf = args.pdf if args.pdf.is_absolute() else html.parent / args.pdf
    export_pdf(html, pdf)
    print("wrote", pdf)

    lang = args.lang or html.stem.replace("open-air-sandbox-", "")
    stem = f"open-air-sandbox-{lang}"
    pngs = rasterize_pdf_pages(pdf, html.parent, stem)
    for p in pngs:
        print("wrote", p, "(pdftoppm)")


if __name__ == "__main__":
    main()
