#!/usr/bin/env python3
"""Build Prompts-IA-Dataton-24nov.docx + PDF from prompts.txt (team-facing sheet)."""
from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor

ROOT = Path(__file__).resolve().parent
PACK = ROOT.parent
PROMPTS_TXT = ROOT / "prompts.txt"
OUT_DOCX = ROOT / "Prompts-IA-Dataton-24nov.docx"
OUT_PDF = ROOT / "Prompts-IA-Dataton-24nov.pdf"
LOGO = PACK / "assets" / "cth-logo-color.png"
TOP_LINE = "Suban su cuestionario lleno al chat de IA y copien una instrucción a la vez."
FOOTER_TEXT = "Inspira. Actúa. Transforma. · CleantechHUB · Datatón 24 nov 2026"
PROMPTS_TXT_SHA = "4cd248ad16227c7cbd6fc33a5b89548920ab978371525a5e57a5de9b95e2fe6a"
CANVAS_PREFIX = "Active Canvas en su chat de IA"

NAVY = RGBColor(0x0C, 0x49, 0x8A)
GREY = RGBColor(0x66, 0x66, 0x66)
COPY_FILL = "E8F6FA"


def _sha256(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_prompts_parts(raw: str) -> list[dict[str, str]]:
    chunks = re.split(r"(?=^Parte: )", raw.strip(), flags=re.MULTILINE)
    parts: list[dict[str, str]] = []
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk.startswith("Parte:"):
            continue
        lines = chunk.split("\n")
        parte_line = lines[0].strip()
        salida_line = next(l.strip() for l in lines if l.startswith("Salida esperada:"))
        forma_line = next(l.strip() for l in lines if l.startswith("Forma esperada:"))
        try:
            blank = lines.index("")
        except ValueError:
            raise SystemExit("prompts.txt: missing blank line after headers") from None
        body = "\n".join(lines[blank + 1 :]).strip()
        parte_title = parte_line.removeprefix("Parte:").strip()
        parts.append(
            {
                "parte_line": parte_line,
                "parte_title": parte_title,
                "salida_line": salida_line,
                "forma_line": forma_line,
                "body": body,
            }
        )
    if len(parts) != 6:
        raise SystemExit(f"prompts.txt: expected 6 parts, got {len(parts)}")
    return parts


def _split_canvas(body: str) -> tuple[str | None, list[str]]:
    lines = [ln for ln in body.split("\n") if ln.strip()]
    if lines and lines[0].startswith(CANVAS_PREFIX):
        return lines[0], lines[1:]
    return None, lines


def _shade_paragraph(paragraph, fill: str = COPY_FILL) -> None:
    p_pr = paragraph._p.get_or_add_pPr()
    shd = p_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        p_pr.append(shd)
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)


def _set_doc_defaults(doc: Document) -> None:
    for name, size in (("Heading 1", 12), ("Heading 2", 9.5), ("Normal", 9)):
        st = doc.styles[name]
        st.font.name = "Open Sans"
        st.font.size = Pt(size)
        st.font.color.rgb = NAVY if name.startswith("Heading") else RGBColor(0x33, 0x33, 0x33)
    normal = doc.styles["Normal"]
    normal.paragraph_format.space_after = Pt(1.5)
    normal.paragraph_format.line_spacing = 1.05


def _header_logo(doc: Document) -> None:
    section = doc.sections[0]
    header = section.header
    p = header.paragraphs[0]
    p.text = ""
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    if LOGO.is_file():
        run = p.add_run()
        run.add_picture(str(LOGO), width=Mm(28))


def _footer_line(doc: Document) -> None:
    section = doc.sections[0]
    section.top_margin = Mm(11)
    section.bottom_margin = Mm(18)
    section.left_margin = Mm(13)
    section.right_margin = Mm(13)
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(FOOTER_TEXT)
    run.font.size = Pt(7.5)
    run.font.color.rgb = GREY


def _patch_open_sans(docx_path: Path) -> None:
    spec = importlib.util.spec_from_file_location("build_cuestionario", ROOT / "build-cuestionario.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("build-cuestionario.py missing")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.patch_docx_theme_open_sans(docx_path)


def build_docx(parts: list[dict[str, str]]) -> None:
    doc = Document()
    _set_doc_defaults(doc)
    _header_logo(doc)
    _footer_line(doc)

    doc.add_heading("Instrucciones de inteligencia artificial", level=1)
    lead = doc.add_paragraph(style="Normal")
    rl = lead.add_run(TOP_LINE)
    rl.bold = True
    rl.font.size = Pt(9)

    for idx, part in enumerate(parts):
        if idx:
            doc.add_paragraph("")
        hp = doc.add_paragraph(part["parte_line"], style="Heading 2")
        if idx == 2:
            hp.paragraph_format.page_break_before = True
        hp.paragraph_format.keep_with_next = True
        for run in hp.runs:
            run.font.size = Pt(9.5)
            run.bold = True
            run.font.color.rgb = NAVY
        part_paras: list = [hp]
        for meta in (part["salida_line"], part["forma_line"]):
            p = doc.add_paragraph(meta, style="Normal")
            p.paragraph_format.keep_with_next = True
            for run in p.runs:
                run.font.size = Pt(8.5)
            part_paras.append(p)
        canvas, lines = _split_canvas(part["body"])
        if canvas:
            cp = doc.add_paragraph(canvas, style="Normal")
            cp.paragraph_format.keep_with_next = True
            for run in cp.runs:
                run.italic = True
                run.font.size = Pt(8.5)
                run.font.color.rgb = GREY
            part_paras.append(cp)
        for line in lines:
            p = doc.add_paragraph(line, style="Normal")
            for run in p.runs:
                run.font.size = Pt(9)
            _shade_paragraph(p)
            p.paragraph_format.keep_together = True
            part_paras.append(p)
        if len(part_paras) > 1:
            part_paras[-1].paragraph_format.keep_with_next = False

    for para in doc.paragraphs:
        for run in para.runs:
            run.font.name = "Open Sans"
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    for run in para.runs:
                        run.font.name = "Open Sans"
    for section in doc.sections:
        for para in section.header.paragraphs + section.footer.paragraphs:
            for run in para.runs:
                run.font.name = "Open Sans"
    doc.save(OUT_DOCX)
    _patch_open_sans(OUT_DOCX)


def _html(parts: list[dict[str, str]]) -> str:
    import html

    logo = html.escape((PACK / "assets/cth-logo-color.png").as_uri())
    css = html.escape((PACK / "print/prompts-ia-dataton-sheet-print.css").as_uri())
    chunks = [
        "<!DOCTYPE html><html lang='es'><head><meta charset='utf-8'/>",
        f"<link rel='stylesheet' href='{css}'/>",
        "</head><body>",
        f"<div class='hdr'><img src='{logo}' alt='CleantechHUB'/></div>",
        "<h1>Instrucciones de inteligencia artificial</h1>",
        f"<p class='lead'>{html.escape(TOP_LINE)}</p>",
    ]
    for idx, part in enumerate(parts):
        block_cls = "parte-block"
        if idx == 2:
            block_cls += " parte-page-start"
        chunks.append(f"<section class='{block_cls}'>")
        chunks.append(f"<h2 class='parte-line'>{html.escape(part['parte_line'])}</h2>")
        for meta in (part["salida_line"], part["forma_line"]):
            chunks.append(f"<p class='meta'>{html.escape(meta)}</p>")
        canvas, lines = _split_canvas(part["body"])
        if canvas:
            chunks.append(f"<p class='canvas-note'>{html.escape(canvas)}</p>")
        if lines:
            chunks.append("<div class='copy-box'>")
            for line in lines:
                chunks.append(f"<p class='body'>{html.escape(line)}</p>")
            chunks.append("</div>")
        chunks.append("</section>")
    chunks.append("</body></html>")
    return "".join(chunks)


async def _render_pdf(html_text: str) -> None:
    import tempfile
    from playwright.async_api import async_playwright

    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "prompts-sheet.html"
        path.write_text(html_text, encoding="utf-8")
        async with async_playwright() as p:
            browser = await p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
            page = await browser.new_page()
            await page.goto(path.as_uri(), wait_until="networkidle")
            footer_tpl = (
                "<div style='font-size:7pt;width:100%;text-align:center;"
                "color:#666;margin:0;font-family:Open Sans,sans-serif'>"
                + FOOTER_TEXT
                + "</div>"
            )
            await page.pdf(
                path=str(OUT_PDF),
                format="A4",
                margin={"top": "12mm", "bottom": "20mm", "left": "12mm", "right": "12mm"},
                print_background=True,
                display_header_footer=True,
                header_template="<span></span>",
                footer_template=footer_tpl,
            )
            await browser.close()


def convert_pdf(parts: list[dict[str, str]]) -> None:
    import asyncio

    asyncio.run(_render_pdf(_html(parts)))


def main() -> int:
    if _sha256(PROMPTS_TXT) != PROMPTS_TXT_SHA:
        raise SystemExit(f"prompts.txt sha drift (expected {PROMPTS_TXT_SHA})")
    parts = parse_prompts_parts(PROMPTS_TXT.read_text(encoding="utf-8"))
    build_docx(parts)
    convert_pdf(parts)
    import fitz

    n = fitz.open(OUT_PDF).page_count
    if n > 3:
        raise SystemExit(f"Prompts IA sheet must be 1–3 pages, got {n}")
    print("prompts_ia_sheet_docx", OUT_DOCX)
    print("prompts_ia_sheet_pdf", OUT_PDF, "pages", n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())