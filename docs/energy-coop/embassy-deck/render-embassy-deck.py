#!/usr/bin/env python3
"""Render embassy deck PDFs (16:9), contact sheet, banned-word checks."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ES_HTML = ROOT / "index.html"
EN_HTML = ROOT / "index-en.html"
PDF_ES = ROOT / "CleantechHUB-energy-coop-embassy-es.pdf"
PDF_EN = ROOT / "CleantechHUB-energy-coop-embassy-en.pdf"
CONTACT = ROOT / "embassy-deck-es-contact.png"
ART = Path("/opt/cursor/artifacts")
EXPECTED = 16
JPEG_QUALITY = 85
MAX_PDF_BYTES = 6 * 1024 * 1024
BANNED_HTML = re.compile(
    r"promigas|piloto|\bpilot\b|\bgrp\b|holanda|países bajos|netherlands|\bdutch\b|\beuropa\b|escuela mou",
    re.I,
)


def ensure_playwright() -> None:
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def render_pdf(html: Path, pdf_out: Path) -> list[Path]:
    from playwright.sync_api import sync_playwright

    pngs: list[Path] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(html.as_uri(), wait_until="networkidle")
        page.wait_for_timeout(600)
        slides = page.locator("section.slide")
        count = slides.count()
        if count != EXPECTED:
            browser.close()
            raise SystemExit(f"{html.name}: expected {EXPECTED} slides, found {count}")
        for i in range(count):
            page.evaluate(
                """(idx) => {
                  document.querySelectorAll('section.slide').forEach((s, j) => {
                    s.style.display = j === idx ? 'flex' : 'none';
                    s.style.position = 'relative';
                    s.style.width = '1920px';
                    s.style.height = '1080px';
                  });
                }""",
                i,
            )
            tmp = ROOT / f".tmp-slide-{html.stem}-{i+1:02d}.png"
            slides.nth(i).screenshot(path=str(tmp))
            pngs.append(tmp)
        from PIL import Image
        import img2pdf

        jpegs: list[Path] = []
        for png in pngs:
            jpg = png.with_suffix(".jpg")
            Image.open(png).convert("RGB").save(jpg, "JPEG", quality=JPEG_QUALITY, optimize=True)
            jpegs.append(jpg)
        layout = img2pdf.get_layout_fun((img2pdf.mm_to_pt(508), img2pdf.mm_to_pt(285.75)))
        pdf_out.write_bytes(img2pdf.convert([str(x) for x in jpegs], layout_fun=layout))
        for j in jpegs:
            j.unlink(missing_ok=True)
        mb = pdf_out.stat().st_size / (1024 * 1024)
        print("wrote", pdf_out, len(jpegs), "pages", f"{mb:.2f} MB")
        if pdf_out.stat().st_size > MAX_PDF_BYTES:
            print(f"WARN: {pdf_out.name} exceeds 6 MB", file=sys.stderr)
        browser.close()
    return pngs


def contact_sheet(pngs: list[Path], out: Path) -> None:
    from PIL import Image

    cols, rows = 4, 5
    w, h = 480, 270
    canvas = Image.new("RGB", (cols * w, rows * h), (178, 238, 250))
    for i, p in enumerate(pngs[: EXPECTED]):
        im = Image.open(p).convert("RGB")
        im = im.resize((w, h), Image.LANCZOS)
        r, c = divmod(i, cols)
        canvas.paste(im, (c * w, r * h))
    canvas.save(out, optimize=True)
    print("wrote", out)


def grep_html(path: Path) -> list[str]:
    if not path.is_file():
        return [f"missing {path.name}"]
    text = path.read_text(encoding="utf-8", errors="replace")
    hits = []
    for m in BANNED_HTML.finditer(text):
        hits.append(f"{path.name}: banned '{m.group(0)}'")
    return hits


def grep_pdf(path: Path) -> list[str]:
    hits = []
    try:
        txt = subprocess.check_output(["pdftotext", str(path), "-"], text=True)
    except FileNotFoundError:
        txt = path.read_bytes().decode("latin-1", errors="ignore")
    except subprocess.CalledProcessError:
        return [f"{path.name}: pdftotext failed"]
    for pat in BANNED_HTML.findall(txt):
        hits.append(f"{path.name}: pdftotext banned '{pat}'")
    return hits


def main() -> int:
    ensure_playwright()
    errors: list[str] = []
    errors.extend(grep_html(ES_HTML))
    errors.extend(grep_html(EN_HTML))
    pngs_es = render_pdf(ES_HTML, PDF_ES)
    pngs_en = render_pdf(EN_HTML, PDF_EN)
    contact_sheet(pngs_es, CONTACT)
    en_contact = ROOT / "embassy-deck-en-contact.png"
    contact_sheet(pngs_en, en_contact)
    ART.mkdir(parents=True, exist_ok=True)
    for src in (PDF_ES, PDF_EN, CONTACT, en_contact):
        dest = ART / src.name
        dest.write_bytes(src.read_bytes())
        print("copied", dest)
    for p in pngs_es + pngs_en:
        p.unlink(missing_ok=True)
    pdf_hits = grep_pdf(PDF_ES) + grep_pdf(PDF_EN)
    if pdf_hits:
        print("PDF_TEXT_BANNED (likely demo screenshot UI / source links):", file=sys.stderr)
        for e in pdf_hits:
            print(" ", e, file=sys.stderr)
    if errors:
        print("BANNED / ERRORS:", file=sys.stderr)
        for e in errors:
            print(" ", e, file=sys.stderr)
        return 1
    print("BANNED_WORD_CHECK: HTML OK; PDF see PDF_TEXT_BANNED if any")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
