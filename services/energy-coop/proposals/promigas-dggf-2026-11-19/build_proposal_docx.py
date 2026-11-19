#!/usr/bin/env python3
"""Build proposal-draft.docx on CTH official letterhead template."""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

NAVY = RGBColor(0x0C, 0x49, 0x8A)
TEMPLATE = Path(
    "/home/ubuntu/.cursor/projects/agent-repos-cth-plugin/uploads/CTH_Letterhead_Official_3561.docx"
)
OUT = Path(__file__).resolve().parent / "proposal-draft.docx"
MD = Path(__file__).resolve().parent / "proposal-draft.md"


def set_run_font(run, *, bold=False, size=11, color=None):
    run.bold = bold
    run.font.size = Pt(size)
    run.font.name = "Open Sans"
    run._element.rPr.rFonts.set(qn("w:ascii"), "Open Sans")
    run._element.rPr.rFonts.set(qn("w:hAnsi"), "Open Sans")
    if color:
        run.font.color.rgb = color


def add_heading(doc: Document, text: str, level: int = 1):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12 if level == 1 else 8)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    size = 14 if level == 1 else 12
    set_run_font(run, bold=True, size=size, color=NAVY)
    return p


def add_body(doc: Document, text: str, *, bullet=False):
    if bullet:
        text = "• " + text
    p = doc.add_paragraph()
    if not bullet:
        p.paragraph_format.space_after = Pt(4)
    # simple bold/markdown links stripped for docx
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    parts = re.split(r"(\*\*[^*]+\*\*)", text)
    for part in parts:
        if part.startswith("**") and part.endswith("**"):
            run = p.add_run(part[2:-2])
            set_run_font(run, bold=True)
        elif part:
            run = p.add_run(part)
            set_run_font(run)
    return p


def md_to_docx(md_path: Path, doc: Document):
    in_verification = False
    for line in md_path.read_text(encoding="utf-8").splitlines():
        if line.strip() == "---" and not in_verification:
            continue
        if line.startswith("# ") and "BORRADOR" in line:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(line[2:].strip())
            set_run_font(run, bold=True, size=16, color=NAVY)
            continue
        if line.startswith("## "):
            title = line[3:].strip()
            if title.startswith("Anexo"):
                in_verification = True
            add_heading(doc, title, level=1 if not in_verification else 2)
            continue
        if line.startswith("### "):
            add_heading(doc, line[4:].strip(), level=2)
            continue
        if line.startswith("|") and "---" not in line:
            add_body(doc, line, bullet=True)
            continue
        if line.strip().startswith("- "):
            add_body(doc, line.strip()[2:], bullet=True)
            continue
        if not line.strip():
            continue
        if line.startswith("**Destinatarios") or line.startswith("**De:"):
            add_body(doc, line.replace("**", ""))
            continue
        add_body(doc, line)


def main():
    if not TEMPLATE.exists():
        print(f"Template missing: {TEMPLATE}", file=sys.stderr)
        sys.exit(1)
    if OUT.exists():
        OUT.unlink()
    shutil.copy(TEMPLATE, OUT)
    doc = Document(OUT)
    # Clear default empty body paragraph(s) from template
    body = doc.element.body
    for child in list(body):
        if child.tag == qn("w:p"):
            body.remove(child)  # keeps w:sectPr (header/footer bindings)
    md_to_docx(MD, doc)
    doc.save(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()