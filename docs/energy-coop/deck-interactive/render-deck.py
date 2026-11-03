#!/usr/bin/env python3
"""Render Energy Coop interactive deck to PDF (16:9) and slide PNG previews."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"
PDF_ES = ROOT / "energy-coop-deck-es.pdf"
PDF_EN = ROOT / "energy-coop-deck-en.pdf"
PREVIEW_DIR = ROOT / "previews"
PREVIEW_SLIDES = (1, 5)
EXPECTED_PAGES = 10
BANNED = re.compile(rb"promigas", re.I)


def ensure_playwright() -> None:
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def pdf_page_count(pdf_path: Path) -> int:
    try:
        out = subprocess.check_output(["pdfinfo", str(pdf_path)], stderr=subprocess.STDOUT, text=True)
        for line in out.splitlines():
            if line.startswith("Pages:"):
                return int(line.split(":", 1)[1].strip())
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
        pass
    raw = pdf_path.read_bytes()
    return len(re.findall(rb"/Type\s*/Page[^s]", raw))


def render_lang(lang: str, pdf_out: Path) -> None:
    from playwright.sync_api import sync_playwright

    url = INDEX.as_uri() + f"?lang={lang}&print"
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(800)
        page.emulate_media(media="screen")
        count = page.locator(".deck .slide").count()
        if count != EXPECTED_PAGES:
            browser.close()
            raise SystemExit(f"Expected {EXPECTED_PAGES} slides, found {count} (lang={lang})")
        png_paths = []
        PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
        for i in range(count):
            slide_no = i + 1
            page.evaluate(
                """(idx) => {
                  document.querySelectorAll('.deck .slide').forEach((s, j) => {
                    s.style.display = j === idx ? 'flex' : 'none';
                    s.style.position = 'relative';
                    s.style.width = '1920px';
                    s.style.height = '1080px';
                  });
                }""",
                i,
            )
            slide = page.locator(".deck .slide").nth(i)
            if lang == "es" and slide_no in PREVIEW_SLIDES:
                preview = PREVIEW_DIR / f"slide-{slide_no:02d}.png"
                slide.screenshot(path=str(preview))
                print("wrote", preview)
            tmp = ROOT / f".tmp-slide-{slide_no}.png"
            slide.screenshot(path=str(tmp))
            png_paths.append(tmp)
        try:
            import img2pdf
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "img2pdf", "-q"])
            import img2pdf
        layout = img2pdf.get_layout_fun((img2pdf.mm_to_pt(508), img2pdf.mm_to_pt(285.75)))
        with open(pdf_out, "wb") as pdf_file:
            pdf_file.write(img2pdf.convert([str(path) for path in png_paths], layout_fun=layout))
        print("wrote", pdf_out, f"({len(png_paths)} pages)")
        for tmp in png_paths:
            tmp.unlink(missing_ok=True)
        browser.close()


def grep_banned(path: Path) -> list[str]:
    hits = []
    if path.suffix == ".html":
        if BANNED.search(path.read_bytes()):
            hits.append(f"{path.name}: forbidden brand string")
    elif path.suffix == ".pdf":
        if BANNED.search(path.read_bytes()):
            hits.append(f"{path.name}: forbidden brand string (binary)")
    return hits


def main() -> int:
    ensure_playwright()
    errors: list[str] = []
    if not INDEX.is_file():
        errors.append(f"Missing {INDEX}")
        return 1
    render_lang("es", PDF_ES)
    render_lang("en", PDF_EN)
    for pdf in (PDF_ES, PDF_EN):
        pages = pdf_page_count(pdf)
        print(f"{pdf.name}: {pages} page(s)")
        if pages != EXPECTED_PAGES:
            errors.append(f"{pdf.name}: expected {EXPECTED_PAGES} pages, got {pages}")
        errors.extend(grep_banned(pdf))
    errors.extend(grep_banned(INDEX))
    if errors:
        print("VALIDATION FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
