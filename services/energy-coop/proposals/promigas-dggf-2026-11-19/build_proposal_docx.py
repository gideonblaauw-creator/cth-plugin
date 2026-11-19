#!/usr/bin/env python3
"""Build proposal-draft.docx on CTH official letterhead template."""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

NAVY = RGBColor(0x0C, 0x49, 0x8A)
NAVY_FILL = "0C498A"
ALT_ROW_FILL = "B2EEFA"
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FONT = "Open Sans"
TEMPLATE = Path(
    "/home/ubuntu/.cursor/projects/agent-repos-cth-plugin/uploads/CTH_Letterhead_Official_3561.docx"
)
OUT = Path(__file__).resolve().parent / "proposal-draft.docx"
MD = Path(__file__).resolve().parent / "proposal-draft.md"


def set_run_font(run, *, bold=False, size=11, color=None):
    run.bold = bold
    run.font.size = Pt(size)
    run.font.name = FONT
    run._element.rPr.rFonts.set(qn("w:ascii"), FONT)
    run._element.rPr.rFonts.set(qn("w:hAnsi"), FONT)
    if color:
        run.font.color.rgb = color


def strip_md_heading(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    return text.strip()


def write_runs(paragraph, text: str, *, default_bold=False, default_color=None, size=10):
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    parts = re.split(r"(\*\*[^*]+\*\*)", text)
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            run = paragraph.add_run(part[2:-2])
            set_run_font(run, bold=True, size=size, color=default_color)
        else:
            run = paragraph.add_run(part)
            set_run_font(run, bold=default_bold, size=size, color=default_color)


def shade_cell(cell, fill_hex: str):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill_hex)
    tc_pr.append(shd)


def set_table_borders(table):
    tbl = table._tbl
    tbl_pr = tbl.tblPr
    if tbl_pr is None:
        tbl_pr = OxmlElement("w:tblPr")
        tbl.insert(0, tbl_pr)
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "0C498A")
        borders.append(el)
    tbl_pr.append(borders)


def parse_table_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def is_separator_row(cells: list[str]) -> bool:
    return all(re.fullmatch(r":?-{1,}:?", c.replace(" ", "")) or c == "" for c in cells)


def add_table(doc: Document, rows: list[list[str]]):
    if not rows:
        return
    ncols = max(len(r) for r in rows)
    rows = [r + [""] * (ncols - len(r)) for r in rows]
    table = doc.add_table(rows=len(rows), cols=ncols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table)
    table.autofit = True

    for ri, row_data in enumerate(rows):
        for ci, cell_text in enumerate(row_data):
            cell = table.rows[ri].cells[ci]
            cell.text = ""
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(2)
            if ri == 0:
                shade_cell(cell, NAVY_FILL)
                write_runs(p, cell_text, default_bold=True, default_color=WHITE, size=10)
            else:
                if ri % 2 == 0:
                    shade_cell(cell, ALT_ROW_FILL)
                write_runs(p, cell_text, size=10)

    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(6)


def add_heading(doc: Document, text: str, level: int = 1):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12 if level == 1 else 8)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(strip_md_heading(text))
    size = 14 if level == 1 else 12
    set_run_font(run, bold=True, size=size, color=NAVY)
    return p


def add_body(doc: Document, text: str, *, bullet=False):
    if bullet:
        text = "• " + strip_md_heading(text) if not text.startswith("•") else strip_md_heading(text)
    p = doc.add_paragraph()
    if not bullet:
        p.paragraph_format.space_after = Pt(4)
    write_runs(p, text, size=11)
    return p


def md_to_docx(md_path: Path, doc: Document):
    lines = md_path.read_text(encoding="utf-8").splitlines()
    i = 0
    in_verification = False
    while i < len(lines):
        line = lines[i]
        if line.strip() == "---" and not in_verification:
            i += 1
            continue
        if line.startswith("|"):
            table_rows: list[list[str]] = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = parse_table_row(lines[i])
                if not is_separator_row(cells):
                    table_rows.append(cells)
                i += 1
            add_table(doc, table_rows)
            continue
        if line.startswith("# ") and "BORRADOR" in line:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(strip_md_heading(line[2:]))
            set_run_font(run, bold=True, size=16, color=NAVY)
            i += 1
            continue
        if line.startswith("## "):
            title = line[3:].strip()
            if title.startswith("Anexo"):
                in_verification = True
            add_heading(doc, title, level=1 if not in_verification else 2)
            i += 1
            continue
        if line.startswith("### "):
            add_heading(doc, line[4:].strip(), level=2)
            i += 1
            continue
        if line.strip().startswith("- "):
            add_body(doc, line.strip()[2:], bullet=True)
            i += 1
            continue
        if not line.strip():
            i += 1
            continue
        if line.startswith("**Destinatarios") or line.startswith("**De:") or line.startswith("**Para:") or line.startswith("**Cc"):
            add_body(doc, line)
            i += 1
            continue
        if line.startswith("*") and line.endswith("*") and not line.startswith("**"):
            add_body(doc, line.strip("*"))
            i += 1
            continue
        add_body(doc, line)
        i += 1


def main():
    if not TEMPLATE.exists():
        print(f"Template missing: {TEMPLATE}", file=sys.stderr)
        sys.exit(1)
    if OUT.exists():
        OUT.unlink()
    shutil.copy(TEMPLATE, OUT)
    doc = Document(OUT)
    body = doc.element.body
    for child in list(body):
        if child.tag == qn("w:p"):
            body.remove(child)
    md_to_docx(MD, doc)
    doc.save(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()