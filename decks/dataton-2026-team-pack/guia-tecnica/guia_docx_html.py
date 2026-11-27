#!/usr/bin/env python3
"""Render Guía docx body ranges to HTML (wording source of truth for PDF tail/front)."""
from __future__ import annotations

import html
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

ROOT = Path(__file__).resolve().parent.parent
LOGO = ROOT / "assets" / "cth-logo-color.png"
COVER_TITLE = "Guía técnica para mentores"

FRONT_PARA_END = 31
TAIL_PARA_START_LEGACY = 197
TAIL_HOJA5_PREFIX = "Hoja 5 — Plantilla pitch"


def tail_para_start(doc: Document) -> int:
    for i, paragraph in enumerate(doc.paragraphs):
        if paragraph.text.strip().startswith(TAIL_HOJA5_PREFIX):
            return i
    return TAIL_PARA_START_LEGACY


def _para_html(paragraph: Paragraph) -> str:
    parts: list[str] = []
    for run in paragraph.runs:
        chunk = html.escape(run.text)
        if run.bold and chunk:
            chunk = f"<strong>{chunk}</strong>"
        if run.italic and chunk:
            chunk = f"<em>{chunk}</em>"
        parts.append(chunk)
    inner = "".join(parts)
    style = (paragraph.style.name or "").lower()
    text = paragraph.text.strip()
    if not text and not inner.strip():
        return ""
    if style == "title":
        return f'<p class="title-es">{inner or html.escape(text)}</p>'
    if "heading 1" in style:
        return f"<h1>{inner or html.escape(text)}</h1>"
    if "heading 2" in style:
        return f"<h2>{inner or html.escape(text)}</h2>"
    if "heading 3" in style:
        return f"<h3>{inner or html.escape(text)}</h3>"
    return f"<p>{inner or html.escape(text)}</p>"


def _table_html(table: Table) -> str:
    rows_html: list[str] = []
    for row in table.rows:
        cells: list[str] = []
        for cell in row.cells:
            bits = [html.escape(p.text) for p in cell.paragraphs if p.text.strip()]
            cells.append(f"<td>{'<br/>'.join(bits) if bits else '&nbsp;'}</td>")
        rows_html.append("<tr>" + "".join(cells) + "</tr>")
    return '<table class="docx-table">' + "".join(rows_html) + "</table>"


def _iter_blocks(doc: Document, para_start: int, para_end: int | None):
    """Yield HTML fragments for paragraphs [para_start, para_end) and interleaved tables."""
    para_idx = 0
    hi = para_end if para_end is not None else 10**9
    for child in doc.element.body:
        if child.tag == qn("w:p"):
            if para_idx >= hi:
                break
            if para_idx >= para_start:
                p = Paragraph(child, doc)
                frag = _para_html(p)
                if frag:
                    yield frag
            para_idx += 1
        elif child.tag == qn("w:tbl"):
            if para_start <= para_idx < hi:
                yield _table_html(Table(child, doc))


def _cover_open() -> list[str]:
    chunks: list[str] = []
    if LOGO.is_file():
        uri = html.escape(LOGO.as_uri())
        chunks.append(f'<div class="guia-logo-hdr"><img src="{uri}" alt="CleantechHUB" /></div>')
    chunks.append('<div class="cover-block">')
    return chunks


def body_html(doc: Document, para_start: int, para_end: int | None) -> str:
    if para_start != 0:
        return "\n".join(_iter_blocks(doc, para_start, para_end))
    chunks = _cover_open()
    in_cover = True
    para_idx = 0
    hi = para_end if para_end is not None else 10**9
    for child in doc.element.body:
        if child.tag == qn("w:p"):
            if para_idx >= hi:
                break
            if para_idx >= para_start:
                p = Paragraph(child, doc)
                text = p.text.strip()
                style = (p.style.name or "").lower()
                if text == "Índice" or (style == "heading 1" and text and text != COVER_TITLE):
                    if in_cover:
                        in_cover = False
                        if chunks and chunks[-1] != "</div>":
                            chunks.append("</div>")
                if in_cover and para_idx == 0 and not text:
                    para_idx += 1
                    continue
                if in_cover and text == COVER_TITLE:
                    inner = "".join(
                        html.escape(run.text) for run in p.runs if run.text
                    ) or html.escape(text)
                    chunks.append(f'<p class="title-es">{inner}</p>')
                elif in_cover and text == "Technical Guide for mentors":
                    chunks.append(f'<p class="title-en"><em>{html.escape(text)}</em></p>')
                elif in_cover and text:
                    frag = _para_html(p)
                    if frag:
                        chunks.append(frag.replace("<p>", '<p class="lead">', 1))
                else:
                    frag = _para_html(p)
                    if frag:
                        chunks.append(frag)
            para_idx += 1
        elif child.tag == qn("w:tbl"):
            if para_start <= para_idx < hi and not in_cover:
                chunks.append(_table_html(Table(child, doc)))
    if chunks and chunks[-1] != "</div>" and any(c == '<div class="cover-block">' for c in chunks):
        chunks.append("</div>")
    return "\n".join(chunks)


def full_html(doc_path: Path, para_start: int, para_end: int | None, css_path: Path, title: str) -> str:
    doc = Document(doc_path)
    main = body_html(doc, para_start, para_end)
    css_uri = css_path.as_uri()
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" href="{css_uri}" />
</head>
<body class="guia-docx-body">
  <main>{main}</main>
</body>
</html>"""