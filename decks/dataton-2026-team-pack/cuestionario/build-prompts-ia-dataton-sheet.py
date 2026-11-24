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
from docx.shared import Mm, Pt, RGBColor

ROOT = Path(__file__).resolve().parent
PACK = ROOT.parent
PROMPTS_TXT = ROOT / "prompts.txt"
OUT_DOCX = ROOT / "Prompts-IA-Dataton-24nov.docx"
OUT_PDF = ROOT / "Prompts-IA-Dataton-24nov.pdf"
LOGO = PACK / "assets" / "cth-logo-color.png"
TOP_LINE = "Suban su cuestionario lleno al chat de IA y copien una instrucción a la vez."
PROMPTS_TXT_SHA = "e325f2f5e8d60547a5ffd1047dbe241b23e071d2e763e7149f5a77f186424015"

NAVY = RGBColor(0x0C, 0x49, 0x8A)
GREY = RGBColor(0x66, 0x66, 0x66)


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
    if len(parts) != 5:
        raise SystemExit(f"prompts.txt: expected 5 parts, got {len(parts)}")
    return parts


def _set_doc_defaults(doc: Document) -> None:
    for name, size in (("Heading 1", 12), ("Heading 2", 9.5), ("Normal", 8.5)):
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
    section.bottom_margin = Mm(11)
    section.left_margin = Mm(13)
    section.right_margin = Mm(13)
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Inspira. Actúa. Transforma. · CleantechHUB · Datatón 24 nov 2026")
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
        doc.add_heading(part["parte_title"], level=2)
        for meta in (part["parte_line"], part["salida_line"], part["forma_line"]):
            p = doc.add_paragraph(meta, style="Normal")
            for run in p.runs:
                run.font.size = Pt(7.8)
        for line in part["body"].split("\n"):
            p = doc.add_paragraph(line, style="Normal")
            for run in p.runs:
                run.font.size = Pt(7.6)

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
    for part in parts:
        chunks.append(f"<h2>{html.escape(part['parte_title'])}</h2>")
        for meta in (part["parte_line"], part["salida_line"], part["forma_line"]):
            chunks.append(f"<p class='meta'>{html.escape(meta)}</p>")
        for line in part["body"].split("\n"):
            chunks.append(f"<p class='body'>{html.escape(line)}</p>")
    chunks.append(
        "<div class='footer'>Inspira. Actúa. Transforma. · CleantechHUB · Datatón 24 nov 2026</div>"
    )
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
            await page.pdf(
                path=str(OUT_PDF),
                format="A4",
                margin={"top": "12mm", "bottom": "14mm", "left": "12mm", "right": "12mm"},
                print_background=True,
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
    if n > 2:
        raise SystemExit(f"Prompts IA sheet must be 1–2 pages, got {n}")
    print("prompts_ia_sheet_docx", OUT_DOCX)
    print("prompts_ia_sheet_pdf", OUT_PDF, "pages", n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())