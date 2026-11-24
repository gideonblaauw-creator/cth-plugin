#!/usr/bin/env python3
"""Assemble Guia-tecnica-solo-mentores.docx from hojas + prompts (layout only)."""
from __future__ import annotations

import difflib
import re
import subprocess
import sys
import tempfile
import zipfile
from html.parser import HTMLParser
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor
from docxcompose.composer import Composer

ROOT = Path(__file__).resolve().parent.parent
GUIA_DIR = Path(__file__).resolve().parent
TEAM = ROOT / "team-pack-es"
PRINT = ROOT / "print"
ASSETS = ROOT / "cuestionario" / "assets"
OUT_DOCX = GUIA_DIR / "Guia-tecnica-solo-mentores.docx"
OUT_PDF = GUIA_DIR / "Guia-tecnica-solo-mentores.pdf"
LOGO = ROOT / "assets/cth-logo-color.png"
HEADER_TEXT = "Solo mentores — no distribuir a equipos"
NAVY = RGBColor(0x0C, 0x49, 0x8A)

SOURCES: list[tuple[str, Path, str]] = [
    ("Hoja 1 — mapa de calor", TEAM / "hoja-1-mapa-de-calor.md", "markdown"),
    ("Hoja 2 — flujo de datos", TEAM / "hoja-2-flujo-de-datos.md", "markdown"),
    ("Hoja 3 — dato a valor", TEAM / "hoja-3-dato-a-valor.md", "markdown"),
    ("Hoja 4 — plantilla tablero", TEAM / "hoja-4-plantilla-tablero.md", "markdown"),
    ("Hoja 4b — ejemplo Air4U", TEAM / "hoja-4b-ejemplo-air4u.md", "markdown"),
    ("Hoja 5 — plantilla pitch", TEAM / "hoja-5-plantilla-pitch.md", "markdown"),
    ("Prompts IA v2 — rúbrica de puntuación", PRINT / "prompts-ia-v2.html", "html"),
]


def _make_reference_doc(path: Path) -> None:
    doc = Document()
    for name, size in (("Title", 22), ("Heading 1", 14), ("Heading 2", 12), ("Normal", 10)):
        st = doc.styles[name]
        st.font.name = "Open Sans"
        st._element.rPr.rFonts.set(qn("w:eastAsia"), "Open Sans")
        st.font.size = Pt(size)
        if name.startswith("Heading") or name == "Title":
            st.font.color.rgb = NAVY
    doc.save(path)


def _pandoc_to_docx(src: Path, fmt: str, dest: Path, reference: Path) -> None:
    subprocess.run(
        [
            "pandoc",
            str(src),
            f"--from={fmt}",
            "--to=docx",
            f"--reference-doc={reference}",
            "-o",
            str(dest),
        ],
        check=True,
        capture_output=True,
    )


def _norm_text(t: str) -> str:
    t = re.sub(r"<[^>]+>", " ", t)
    t = t.replace("\r\n", "\n")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip().lower()


def _docx_plain(path: Path) -> str:
    doc = Document(path)
    parts: list[str] = []
    for p in doc.paragraphs:
        parts.append(p.text)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                parts.append(cell.text)
    return _norm_text("\n".join(parts))


class _StripHTML(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.chunks: list[str] = []

    def handle_data(self, data: str) -> None:
        self.chunks.append(data)


def _html_plain(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    stripper = _StripHTML()
    stripper.feed(raw)
    return _norm_text(" ".join(stripper.chunks))


def _md_plain(path: Path) -> str:
    return _norm_text(path.read_text(encoding="utf-8"))


def _verify_section(src: Path, fmt: str, part_docx: Path) -> None:
    if fmt == "markdown":
        src_n = _md_plain(src)
    else:
        src_n = _html_plain(src)
    out_n = _docx_plain(part_docx)
    src_tokens = set(re.findall(r"[a-záéíóúñ0-9]{4,}", src_n, flags=re.I))
    out_tokens = set(re.findall(r"[a-záéíóúñ0-9]{4,}", out_n, flags=re.I))
    if not src_tokens:
        return
    missing = src_tokens - out_tokens
    drop = 0.12 if fmt == "html" else 0.06
    if len(missing) / len(src_tokens) > drop:
        sample = sorted(missing)[:25]
        raise SystemExit(
            f"Content drift in {src.name}: {len(missing)}/{len(src_tokens)} tokens absent, e.g. {sample}"
        )


def _set_header(section, text: str) -> None:
    header = section.header
    if not header.paragraphs:
        header.add_paragraph()
    p = header.paragraphs[0]
    p.text = ""
    run = p.add_run(text)
    run.font.size = Pt(8)
    run.font.color.rgb = NAVY
    run.bold = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER


def _apply_headers(doc: Document) -> None:
    for section in doc.sections:
        _set_header(section, HEADER_TEXT)


def _build_cover(doc: Document) -> None:
    if LOGO.is_file():
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(str(LOGO), width=Mm(40))
    t = doc.add_heading("Guía técnica (solo mentores)", level=0)
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = sub.add_run("Technical Guide (mentors only)")
    r.italic = True
    r.font.size = Pt(12)
    r.font.color.rgb = NAVY
    doc.add_paragraph(
        "Compilación de las hojas metodológicas y la rúbrica de prompts IA. "
        "Documento de trabajo para mentores del Datatón.",
        style="Normal",
    )
    doc.add_page_break()


def _build_index(doc: Document) -> None:
    doc.add_heading("Índice", level=1)
    for i, (title, _, _) in enumerate(SOURCES, start=1):
        doc.add_paragraph(f"{i}. {title}", style="Normal")
    doc.add_page_break()


def build_docx() -> None:
    with tempfile.TemporaryDirectory() as td:
        ref = Path(td) / "reference.docx"
        _make_reference_doc(ref)
        part_paths: list[Path] = []
        for title, src, fmt in SOURCES:
            if not src.is_file():
                raise FileNotFoundError(src)
            part = Path(td) / f"{src.stem}.docx"
            pandoc_fmt = fmt if fmt == "html" else "markdown"
            _pandoc_to_docx(src, pandoc_fmt, part, ref)
            _verify_section(src, fmt, part)
            part_paths.append(part)

        master = Document()
        _set_doc_defaults(master)
        _set_header(master.sections[0], HEADER_TEXT)
        _build_cover(master)
        _build_index(master)

        composer = Composer(master)
        for i, part in enumerate(part_paths):
            frag = Document(part)
            if i < len(part_paths) - 1:
                frag.add_page_break()
            composer.append(frag)

        composer.save(OUT_DOCX)

    final = Document(OUT_DOCX)
    _apply_headers(final)
    final.save(OUT_DOCX)


def _set_doc_defaults(doc: Document) -> None:
    for name in ("Heading 1", "Heading 2", "Normal"):
        st = doc.styles[name]
        st.font.name = "Open Sans"
        try:
            st._element.rPr.rFonts.set(qn("w:eastAsia"), "Open Sans")
        except Exception:
            pass


def convert_pdf() -> None:
    subprocess.run(
        ["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", str(GUIA_DIR), str(OUT_DOCX)],
        check=True,
        capture_output=True,
    )
    if not OUT_PDF.is_file():
        raise SystemExit("LibreOffice PDF missing")


def verify_pdf_sections() -> int:
    import fitz

    doc = fitz.open(OUT_PDF)
    text = re.sub(r"\s+", " ", " ".join(p.get_text() for p in doc))
    markers = [
        "Hoja 1 — Mapa de calor de datos",
        "Hoja 2 — Flujo que genera datos",
        "Hoja 3 — De dato a valor",
        "Hoja 4 — Plantilla de tablero",
        "Hoja 4b — Ejemplo Air4U (relleno)",
        "Hoja 5 — Plantilla pitch",
        "Prompts de IA para el Datatón",
    ]
    pos = 0
    for title in markers:
        idx = text.find(title, pos)
        if idx < 0:
            raise SystemExit(f"PDF section missing: {title}")
        pos = idx + len(title)
    for page in doc:
        if HEADER_TEXT not in page.get_text():
            raise SystemExit("Mentor header missing on at least one PDF page")
    n = doc.page_count
    doc.close()
    return n


def main() -> int:
    build_docx()
    convert_pdf()
    pages = verify_pdf_sections()
    print("guia_docx", OUT_DOCX)
    print("guia_pdf", OUT_PDF)
    print("guia_pdf_pages", pages)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())