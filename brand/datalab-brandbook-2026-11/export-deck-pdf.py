#!/usr/bin/env python3
"""Export a co-located print-ready PDF for CTH HTML decks (HARD 4 Nov 2026).

Forces reveal/animation final states and [data-count] values, then prints with
Chromium (Playwright) or Chrome headless (one slide per page for .deck .slide).

Usage:
  python3 export-deck-pdf.py --pdf my-deck.pdf
  python3 export-deck-pdf.py --index /path/to/index.html --pdf out.pdf --mode slides

Requires: playwright (+ chromium) or google-chrome-stable for slide decks.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PREP_JS = """
() => {
  document.querySelectorAll('.reveal').forEach(el => el.classList.add('visible'));
  document.querySelectorAll('[data-count]').forEach(el => {
    const t = el.dataset.count;
    if (t !== undefined && t !== '') el.textContent = t;
  });
  document.querySelectorAll('*').forEach(el => {
    el.style.setProperty('animation', 'none', 'important');
    el.style.setProperty('transition', 'none', 'important');
  });
}
"""

SLIDE_COUNT_JS = "() => document.querySelectorAll('.deck .slide').length"


def ensure_playwright() -> None:
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def chrome_bin() -> str | None:
    for name in ("google-chrome-stable", "google-chrome", "chromium", "chromium-browser"):
        path = shutil.which(name)
        if path:
            return path
    return None


def chrome_screenshot(html_uri: str, out_png: Path) -> None:
    chrome = chrome_bin()
    if not chrome:
        raise RuntimeError("google-chrome-stable not found for slide PDF export")
    cmd = [
        chrome,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--window-size=1920,1080",
        f"--screenshot={out_png}",
        html_uri,
    ]
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def export_slides_chrome(index: Path, pdf_out: Path, slide_count: int) -> None:
    try:
        import img2pdf
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "img2pdf", "-q"])
        import img2pdf

    base_uri = index.resolve().as_uri()
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        pngs: list[Path] = []
        for i in range(slide_count):
            uri = f"{base_uri}?exportSlide={i}"
            one = tmp_path / f"slide-{i:03d}.png"
            chrome_screenshot(uri, one)
            if one.stat().st_size < 4000:
                raise RuntimeError(f"Slide {i} PNG too small ({one.stat().st_size} B); export failed")
            pngs.append(one)
        with open(pdf_out, "wb") as out_f:
            out_f.write(img2pdf.convert([str(p) for p in pngs]))


def build_url(index: Path, mode: str) -> str:
    uri = index.resolve().as_uri()
    if mode == "slides":
        sep = "&" if "?" in uri else "?"
        return f"{uri}{sep}print"
    return uri


def main() -> None:
    parser = argparse.ArgumentParser(description="Export HTML deck to print-ready PDF")
    parser.add_argument("--index", type=Path, default=Path("index.html"), help="Deck index.html")
    parser.add_argument("--pdf", type=Path, required=True, help="Output PDF filename (same folder recommended)")
    parser.add_argument(
        "--mode",
        choices=("auto", "scroll", "slides"),
        default="auto",
        help="scroll: long page; slides: one 1920×1080 page per .slide; auto: slides if .deck .slide exists",
    )
    args = parser.parse_args()

    index = args.index.resolve()
    if not index.is_file():
        raise SystemExit(f"Missing index: {index}")

    pdf_out = args.pdf if args.pdf.is_absolute() else (index.parent / args.pdf)
    pdf_out.parent.mkdir(parents=True, exist_ok=True)

    ensure_playwright()
    from playwright.sync_api import sync_playwright

    mode = args.mode
    slide_count = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(index.as_uri(), wait_until="networkidle")
        slide_count = page.evaluate(SLIDE_COUNT_JS)
        if args.mode == "auto":
            mode = "slides" if slide_count else "scroll"
        browser.close()

    if mode == "slides" and slide_count > 0:
        export_slides_chrome(index, pdf_out, slide_count)
        print("wrote", pdf_out, f"mode=slides pages={slide_count} engine=chrome")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto(build_url(index, "scroll"), wait_until="networkidle")
        page.evaluate(PREP_JS)
        page.emulate_media(media="print")
        page.pdf(
            path=str(pdf_out),
            format="A4",
            landscape=True,
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()

    print("wrote", pdf_out, f"mode={mode}")


if __name__ == "__main__":
    main()
