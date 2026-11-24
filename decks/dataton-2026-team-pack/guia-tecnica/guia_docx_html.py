#!/usr/bin/env python3
"""Render Guía docx body ranges to HTML (wording source of truth for PDF tail/front)."""
from __future__ import annotations

import html
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

FRONT_PARA_END = 31
TAIL_PARA_START = 197


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


def body_html(doc: Document, para_start: int, para_end: int | None) -> str:
    return "\n".join(_iter_blocks(doc, para_start, para_end))


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