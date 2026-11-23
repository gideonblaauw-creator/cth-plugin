#!/usr/bin/env python3
"""Build editable agenda-dataton-24nov-v5.docx (CTH letterhead fallback)."""
from __future__ import annotations

import pathlib

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Mm, Pt, RGBColor

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "agenda-dataton-24nov-v5.docx"
LOGOS = ROOT / "logos"

NAVY = RGBColor(0x0C, 0x49, 0x8A)
CYAN = RGBColor(0xB2, 0xEE, 0xFA)
GREEN = RGBColor(0x66, 0x93, 0x48)
BLUE_TEXT = RGBColor(0x0C, 0x49, 0x8A)
SANDBOX = "D9F4FC"
BODY_FONT = "Open Sans"

ROWS: list[tuple[str, str, bool]] = [
    ("08:00", "Registro y bienvenida", False),
    (
        "08:30",
        "Palabras de apertura (Gideon Blaauw, CleantechHUB, y Marlene Díaz, Universidad Externado)",
        False,
    ),
    (
        "08:40",
        "Panel: Innovación y emprendimiento en el territorio a través de los datos (ODS 13), 30 min. Natalia Vargas (APC-Colombia), Rector de la Universidad Externado, RAP Pacífico y Óscar (Apix Pharma).\nModera Gideon Blaauw",
        False,
    ),
    (
        "09:10",
        "Lanzamiento del Observatorio de la Tierra y presentación del Datalab",
        False,
    ),
    ("09:25", "Pausa de café", False),
    (
        "09:40",
        "Conversatorio: Alejandro Díaz (Universidad Externado), el Sr. Cortés (Constructora Bolívar) y Gideon Blaauw",
        False,
    ),
    (
        "09:55",
        "Conversatorio: Digitalización como habilitador para la competitividad del territorio. Presentación de Enrique Medina (Agrometers) y conversación con Gideon Blaauw",
        False,
    ),
    (
        "10:05",
        "Data Sandbox de Innovación (1/3): presentación de Air4U",
        True,
    ),
    ("10:10", "Data Sandbox de Innovación (2/3): demo en vivo Air4U", True),
    (
        "10:20",
        "Data Sandbox de Innovación (3/3): conversatorio Air4U y Óscar (Apix Pharma).\nModera Gideon Blaauw",
        True,
    ),
    ("10:45", "Instrucciones y arranque del datatón", False),
    ("11:00", "Trabajo de equipos con monitores (bloque 1)", False),
    ("12:30", "Almuerzo y networking", False),
    (
        "13:30",
        "Trabajo de equipos y preparación del pitch (bloque 2)",
        False,
    ),
    ("15:30", "Refrigerio", False),
    (
        "16:00",
        "Pitches finales: 6 equipos preseleccionados por los monitores",
        False,
    ),
    ("16:40", "Deliberación del jurado", False),
    ("16:50", "Cierre: anuncio de 3 ganadores y entrega de certificados", False),
    ("17:00", "Fin", False),
]


def set_cell_shading(cell, fill_hex: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill_hex)
    tc_pr.append(shd)


def set_run_font(run, size_pt: float, bold: bool = False, color: RGBColor | None = None) -> None:
    run.font.name = BODY_FONT
    run._element.rPr.rFonts.set(qn("w:ascii"), BODY_FONT)
    run._element.rPr.rFonts.set(qn("w:hAnsi"), BODY_FONT)
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    if color is not None:
        run.font.color.rgb = color


def add_header_logos(paragraph) -> None:
    for idx, name in enumerate(
        ("externado-white.png", "cleantechhub-white.png", "observatorio-white.png")
    ):
        path = LOGOS / name
        if idx:
            paragraph.add_run("   ")
        run = paragraph.add_run()
        run.add_picture(str(path), height=Inches(0.22))


def build() -> None:
    doc = Document()
    section = doc.sections[0]
    section.page_height = Mm(297)
    section.page_width = Mm(210)
    section.top_margin = Inches(0.35)
    section.bottom_margin = Inches(0.32)
    section.left_margin = Inches(0.45)
    section.right_margin = Inches(0.45)

    header = section.header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    set_cell_shading_table_paragraph(hp, "0C498A")
    add_header_logos(hp)

    # Title block (body)
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(0)
    r = p.add_run("AGENDA · 24 NOVIEMBRE 2026")
    set_run_font(r, 8, bold=True, color=GREEN)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("Datatón · Lanzamiento suave del Observatorio de la Tierra")
    set_run_font(r, 14, bold=True, color=NAVY)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(
        "Soft launch del Datalab · martes 24 de noviembre de 2026 · Universidad Externado de Colombia"
    )
    set_run_font(r, 9, bold=False, color=NAVY)

    head = doc.add_table(rows=1, cols=2)
    head.alignment = WD_TABLE_ALIGNMENT.CENTER
    head.autofit = False
    head.columns[0].width = Inches(3.2)
    head.columns[1].width = Inches(3.0)
    c0, c1 = head.rows[0].cells
    r0 = c0.paragraphs[0].add_run("Programa del día")
    set_run_font(r0, 11, bold=True, color=NAVY)
    c1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r1 = c1.paragraphs[0].add_run("HORARIOS ORIENTATIVOS")
    set_run_font(r1, 8, bold=True, color=GREEN)
    set_cell_bottom_border(head)

    table = doc.add_table(rows=1 + len(ROWS), cols=2)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(0.72)
    table.columns[1].width = Inches(5.48)

    hdr = table.rows[0].cells
    set_cell_shading(hdr[0], "0C498A")
    set_cell_shading(hdr[1], "0C498A")
    rh = hdr[0].paragraphs[0].add_run("Hora")
    set_run_font(rh, 9, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))
    ra = hdr[1].paragraphs[0].add_run("Actividad")
    set_run_font(ra, 9, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))

    for i, (hora, actividad, sandbox) in enumerate(ROWS, start=1):
        row = table.rows[i].cells
        for cell in row:
            if sandbox:
                set_cell_shading(cell, SANDBOX)
        p0 = row[0].paragraphs[0]
        p0.paragraph_format.space_before = Pt(0)
        p0.paragraph_format.space_after = Pt(0)
        rt = p0.add_run(hora)
        set_run_font(rt, 9, bold=True, color=GREEN)

        p1 = row[1].paragraphs[0]
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after = Pt(0)
        lines = actividad.split("\n")
        for j, line in enumerate(lines):
            if j:
                p1.add_run().add_break()
            run = p1.add_run(line)
            if line.startswith("Modera "):
                set_run_font(run, 9, bold=True, color=GREEN)
            else:
                set_run_font(run, 9, bold=False, color=BLUE_TEXT)

    footer = section.footer
    fp = footer.paragraphs[0]
    set_cell_shading_table_paragraph(fp, "0C498A")
    ft = fp.add_run("Observa. Actúa. Transforma.")
    set_run_font(ft, 10, bold=True, color=CYAN)
    fp.add_run("    ")
    add_header_logos(fp)

    doc.save(OUT)
    print(OUT)


def set_cell_shading_table_paragraph(paragraph, fill_hex: str) -> None:
    p_pr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill_hex)
    p_pr.append(shd)


def set_cell_bottom_border(table) -> None:
    for cell in table.rows[0].cells:
        tc_pr = cell._tc.get_or_add_tcPr()
        borders = OxmlElement("w:tcBorders")
        bottom = OxmlElement("w:bottom")
        bottom.set(qn("w:val"), "single")
        bottom.set(qn("w:sz"), "12")
        bottom.set(qn("w:color"), "B2EEFA")
        borders.append(bottom)
        tc_pr.append(borders)


if __name__ == "__main__":
    build()