#!/usr/bin/env python3
"""Assemble Guia-tecnica-mentores.pdf from docx front/tail HTML + dist hoja PDFs."""
from __future__ import annotations

import asyncio
import re
import tempfile
from pathlib import Path

import fitz

from guia_docx_html import FRONT_PARA_END, TAIL_PARA_START, full_html

ROOT = Path(__file__).resolve().parent.parent
GUIA_DIR = Path(__file__).resolve().parent
DIST = ROOT / "dist"
OUT_PDF = GUIA_DIR / "Guia-tecnica-mentores.pdf"
OUT_DOCX = GUIA_DIR / "Guia-tecnica-mentores.docx"
FONT_REG = ROOT / "fonts/open-sans/OpenSans-Regular.ttf"
RUN_HEADER = "Guía técnica · solo mentores"
FONT_PDF_NAME = "OpenSansGuia"

HOJA_MIDDLE_MD: tuple[tuple[str, str], ...] = (
    ("hoja-1-mapa-de-calor", "hoja-1-mapa-de-calor.md"),
    ("hoja-2-flujo-de-datos", "hoja-2-flujo-de-datos.md"),
    ("hoja-3-dato-a-valor", "hoja-3-dato-a-valor.md"),
    ("hoja-4-plantilla-tablero", "hoja-4-plantilla-tablero.md"),
    ("hoja-4b-ejemplo-air4u", "hoja-4b-ejemplo-air4u.md"),
)

DOCX_CSS = ROOT / "print" / "guia-docx-print.css"
TEAM = ROOT / "team-pack-es"


def _load_build_pack():
    import importlib.util

    bp_path = ROOT / "build-pack.py"
    spec = importlib.util.spec_from_file_location("dataton_build_pack", bp_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load build-pack.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


async def _render_guia_middle_hoja_pdf(build_pack, title: str, md_name: str, dest: Path, work: Path) -> None:
    from playwright.async_api import async_playwright

    md_text = (TEAM / md_name).read_text(encoding="utf-8")
    html_text = build_pack.md_to_guia_merge_html(md_text, title, borrador=False)
    html_path = work / f"{title}.html"
    html_path.write_text(html_text, encoding="utf-8")
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = await browser.new_page()
        await page.goto(html_path.as_uri(), wait_until="networkidle")
        await page.pdf(
            path=str(dest),
            format="A4",
            margin={"top": "12mm", "bottom": "12mm", "left": "12mm", "right": "12mm"},
            print_background=True,
        )
        await browser.close()


async def _render_html_pdf(html_text: str, dest: Path) -> None:
    from playwright.async_api import async_playwright

    with tempfile.TemporaryDirectory() as td:
        html_path = Path(td) / "slice.html"
        html_path.write_text(html_text, encoding="utf-8")
        async with async_playwright() as p:
            browser = await p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
            page = await browser.new_page()
            await page.goto(html_path.as_uri(), wait_until="networkidle")
            await page.pdf(
                path=str(dest),
                format="A4",
                margin={"top": "16mm", "bottom": "14mm", "left": "12mm", "right": "12mm"},
                print_background=True,
            )
            await browser.close()


def _strip_hoja_print_header(page: fitz.Page) -> None:
    """Remove dist hoja HTML header bar (not in Guía docx wording)."""
    rect = fitz.Rect(0, 0, page.rect.width, 46)
    page.add_redact_annot(rect, fill=(1, 1, 1))
    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)


def _merge_pdfs(parts: list[Path], dest: Path, strip_hdr_from: set[int] | None = None) -> int:
    """Merge PDFs; optionally strip print hdr on parts whose index is in strip_hdr_from."""
    doc = fitz.open()
    pages = 0
    for part_index, part in enumerate(parts):
        src = fitz.open(part)
        for page_num, page in enumerate(src):
            if strip_hdr_from and part_index in strip_hdr_from and page_num == 0:
                _strip_hoja_print_header(page)
            doc.insert_pdf(src, from_page=page_num, to_page=page_num)
            pages += 1
        src.close()
    dest.parent.mkdir(parents=True, exist_ok=True)
    doc.save(dest, garbage=4, deflate=True)
    doc.close()
    return pages


def _stamp_running_header(pdf_path: Path) -> None:
    doc = fitz.open(pdf_path)
    color = (12 / 255, 73 / 255, 138 / 255)
    for i, page in enumerate(doc):
        rect = page.rect
        page.insert_font(fontname=FONT_PDF_NAME, fontfile=str(FONT_REG))
        page.insert_text(
            (36, 22),
            RUN_HEADER,
            fontsize=7.5,
            fontname=FONT_PDF_NAME,
            color=color,
        )
        num = str(i + 1)
        box = fitz.Rect(rect.width - 48, rect.height - 28, rect.width - 34, rect.height - 14)
        page.insert_textbox(
            box,
            num,
            fontsize=8,
            fontname=FONT_PDF_NAME,
            color=color,
            align=fitz.TEXT_ALIGN_RIGHT,
        )
    stamped = pdf_path.with_name(pdf_path.stem + ".stamped.pdf")
    doc.save(stamped, garbage=4, deflate=True)
    doc.close()
    stamped.replace(pdf_path)


def verify_sections(pdf_path: Path) -> int:
    doc = fitz.open(pdf_path)
    text = re.sub(r"\s+", " ", " ".join(p.get_text() for p in doc))
    markers = [
        "Hoja 1 — Mapa de calor de datos",
        "Hoja 2 — Flujo que genera datos",
        "Hoja 3 — De dato a valor",
        "Hoja 4 — Plantilla de tablero",
        "Hoja 4b — Ejemplo Air4U (relleno)",
        "Hoja 5 — Plantilla pitch",
        "Prompts de IA v2 — Datatón CTH",
    ]
    pos = 0
    for title in markers:
        idx = text.find(title, pos)
        if idx < 0:
            doc.close()
            raise SystemExit(f"PDF section missing: {title}")
        pos = idx + len(title)
    plain = text.replace(RUN_HEADER, "")
    banned = (
        "Metodología Datatón CTH",
        "Datatón v0.4-es",
    )
    low = plain.lower()
    for phrase in banned:
        if phrase.lower() in low:
            doc.close()
            raise SystemExit(f"Banned phrase in PDF: {phrase!r}")
    n = doc.page_count
    for page in doc:
        if RUN_HEADER not in page.get_text():
            doc.close()
            raise SystemExit("Running header missing on at least one PDF page")
        if "no distribuir" in page.get_text().lower():
            doc.close()
            raise SystemExit("Banned phrase in PDF: 'no distribuir'")
    doc.close()
    return n


async def build_guia_pdf_async() -> int:
    if not OUT_DOCX.is_file():
        raise FileNotFoundError(f"Missing guía docx: {OUT_DOCX}")

    build_pack = _load_build_pack()
    front_html = full_html(OUT_DOCX, 0, FRONT_PARA_END, DOCX_CSS, "Guía técnica — front")
    tail_html = full_html(OUT_DOCX, TAIL_PARA_START, None, DOCX_CSS, "Guía técnica — hoja 5 + prompts")

    with tempfile.TemporaryDirectory() as td:
        work = Path(td) / "html"
        build_pack.stage_md_build_dir(work)
        front = Path(td) / "guia-front.pdf"
        tail = Path(td) / "guia-tail.pdf"
        merged = Path(td) / "guia-merged.pdf"
        middle: list[Path] = []
        for title, md_name in HOJA_MIDDLE_MD:
            part = Path(td) / f"{title}.pdf"
            await _render_guia_middle_hoja_pdf(build_pack, title, md_name, part, work)
            middle.append(part)
        await _render_html_pdf(front_html, front)
        await _render_html_pdf(tail_html, tail)
        parts = [front, *middle, tail]
        # Middle parts: strip HTML hdr bar on first page only (not in docx Guía wording).
        _merge_pdfs(parts, merged, strip_hdr_from={1, 2, 3, 4, 5})
        _stamp_running_header(merged)
        OUT_PDF.write_bytes(merged.read_bytes())

    pages = verify_sections(OUT_PDF)
    print("guia_styled_pdf", OUT_PDF, "pages", pages)
    return pages


def build_guia_pdf() -> int:
    return asyncio.run(build_guia_pdf_async())


if __name__ == "__main__":
    raise SystemExit(build_guia_pdf())