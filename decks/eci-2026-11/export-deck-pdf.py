#!/usr/bin/env python3
"""Export `eci-2026-11` scroll deck to A4 landscape PDF via Playwright.

Adds ?export-pdf=1 so `app.js` forces reveals, static Chart.js, and a WebGL snapshot.

Usage (from this directory):
  python3 export-deck-pdf.py --pdf eci-2026-11.pdf --mode scroll

Optional: rasterize pages for QA (requires poppler `pdftoppm`):
  python3 export-deck-pdf.py --pdf eci-2026-11.pdf --raster-dir /opt/cursor/artifacts/eci-2026-11-pdf-pages

Requires: playwright (+ chromium). Installed on demand if missing.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

PREP_JS = """
() => {
  document.querySelectorAll('.reveal').forEach(el => el.classList.add('visible'));
  document.querySelectorAll('.reveal-on-scroll').forEach(el => el.classList.add('is-visible'));
  document.querySelectorAll('[data-count]').forEach(el => {
    const t = el.dataset.count;
    if (t !== undefined && t !== '') el.textContent = t;
  });
  if (document.querySelector('.deck .slide')) {
    document.body.classList.add('print-all');
  }
  document.querySelectorAll('*').forEach(el => {
    el.style.setProperty('animation', 'none', 'important');
    el.style.setProperty('transition', 'none', 'important');
  });
}
"""


def ensure_playwright() -> None:
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        from playwright.sync_api import sync_playwright  # noqa: F401


def build_url(index: Path, mode: str) -> str:
    uri = index.resolve().as_uri()
    q = []
    if mode == "slides":
        q.append("print=1")
    q.append("export-pdf=1")
    sep = "&" if "?" in uri else "?"
    return f"{uri}{sep}{'&'.join(q)}"


def pdf_page_count(pdf_path: Path) -> int:
    pdfinfo_bin = shutil.which("pdfinfo")
    if not pdfinfo_bin:
        return 0
    try:
        out = subprocess.check_output([pdfinfo_bin, str(pdf_path)], text=True, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return 0
    for line in out.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    return 0


def rasterize_pdf(pdf_path: Path, out_dir: Path, prefix: str = "page") -> int:
    pdftoppm = shutil.which("pdftoppm")
    if not pdftoppm:
        raise SystemExit("pdftoppm not found (install poppler-utils)")
    out_dir.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(
        [
            pdftoppm,
            "-png",
            "-r",
            "120",
            str(pdf_path),
            str(out_dir / prefix),
        ]
    )
    return len(list(out_dir.glob(f"{prefix}-*.png")))


def check_pages_not_blank(png_dir: Path, prefix: str, min_std: float = 4.0) -> list[tuple[str, float]]:
    try:
        from PIL import Image  # type: ignore
        from PIL import ImageStat  # type: ignore
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "-q"])
        from PIL import Image  # type: ignore
        from PIL import ImageStat  # type: ignore

    bad: list[tuple[str, float]] = []
    for p in sorted(png_dir.glob(f"{prefix}-*.png")):
        im = Image.open(p).convert("L")
        stat = ImageStat.Stat(im)
        std = float(stat.stddev[0]) if stat.stddev else 0.0
        if std < min_std:
            bad.append((p.name, std))
    return bad


def main() -> None:
    parser = argparse.ArgumentParser(description="Export ECI HELIX deck to PDF")
    parser.add_argument("--index", type=Path, default=Path("index.html"), help="index.html path")
    parser.add_argument("--pdf", type=Path, required=True, help="Output PDF filename")
    parser.add_argument(
        "--mode",
        choices=("auto", "scroll", "slides"),
        default="auto",
        help="scroll: long page; slides: 1920 stage; auto: slides if .deck .slide exists",
    )
    parser.add_argument(
        "--raster-dir",
        type=Path,
        default=None,
        help="If set, run pdftoppm here and check pages are not near-uniform",
    )
    parser.add_argument("--wait-ms", type=int, default=90_000, help="Max wait for deck render flag")
    args = parser.parse_args()

    index = args.index.resolve()
    if not index.is_file():
        raise SystemExit(f"Missing index: {index}")

    ensure_playwright()
    from playwright.sync_api import sync_playwright

    mode = args.mode
    if mode == "auto":
        mode = "slides"  # decided after first load (matches `decks/_templates/export-deck-pdf.py`)

    pdf_out = args.pdf if args.pdf.is_absolute() else (index.parent / args.pdf)
    pdf_out.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        url = build_url(index, "slides" if mode == "slides" else "scroll")
        page.goto(url, wait_until="networkidle")

        has_stage = page.locator(".deck .slide").count() > 0
        if args.mode == "auto":
            mode = "slides" if has_stage else "scroll"
            if mode == "slides" and "?print" not in page.url and "#print" not in page.url:
                page.goto(build_url(index, "slides"), wait_until="networkidle")

        page.evaluate(PREP_JS)

        try:
            page.wait_for_function(
                "typeof window.__eciPdfReady !== 'undefined' && window.__eciPdfReady === true",
                timeout=args.wait_ms,
            )
        except Exception:
            page.wait_for_timeout(3000)

        page.emulate_media(media="print")

        if mode == "slides":
            page.set_viewport_size({"width": 1920, "height": 1080})

        page.pdf(
            path=str(pdf_out),
            format="A4",
            landscape=True,
            print_background=True,
            margin={"top": "0.4in", "right": "0.4in", "bottom": "0.4in", "left": "0.4in"},
        )
        browser.close()

    n_pages = pdf_page_count(pdf_out)
    print("wrote", pdf_out, f"mode={mode}", f"pages={n_pages}")

    if args.raster_dir is not None:
        rdir = args.raster_dir.resolve()
        n_png = rasterize_pdf(pdf_out, rdir)
        print("rasterized", n_png, "png(s) to", rdir)
        bad = check_pages_not_blank(rdir, "page")
        if bad:
            names = ", ".join(f"{n} (std≈{s:.1f})" for n, s in bad)
            raise SystemExit(f"Near-uniform or blank pages suspected: {names}")
        if n_png != n_pages and n_pages > 0:
            print("warning: png count", n_png, "differs from pdfinfo pages", n_pages)


if __name__ == "__main__":
    main()
