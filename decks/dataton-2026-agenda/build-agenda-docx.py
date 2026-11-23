#!/usr/bin/env python3
"""Build agenda-dataton-24nov-v5.docx from CTH official letterhead template."""
from __future__ import annotations

import pathlib

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Mm, Pt, RGBColor
from docx.text.paragraph import Paragraph

ROOT = pathlib.Path(__file__).resolve().parent
LETTERHEAD = ROOT / "assets" / "letterhead"
TEMPLATE = LETTERHEAD / "CTH_Letterhead_Official.docx"
HEADER_BAND = LETTERHEAD / "CTH_header_band.png"
FOOTER_BAND = LETTERHEAD / "CTH_footer_band.png"
OUT = ROOT / "agenda-dataton-24nov-v5.docx"
LOGOS = ROOT / "logos"
A4_WIDTH = Inches(210 / 25.4)
VENUE = "Auditorio del Bloque I, piso 2 · Av. Circunvalar No. 12B-54"

NAVY = RGBColor(0x0C, 0x49, 0x8A)
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
        "Panel: Innovación y emprendimiento en el territorio a través de los datos (ODS 13), 30 min. Natalia\u00a0Vargas (APC-Colombia), Rector de la Universidad Externado, RAP Pacífico y Óscar (Apix Pharma). \nModera Gideon Blaauw",
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
        "Data Sandbox de Innovación (3/3): conversatorio Air4U y Óscar (Apix Pharma). \nModera Gideon Blaauw",
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


def _set_rfonts(r_pr: OxmlElement) -> None:
    rfonts = r_pr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        r_pr.insert(0, rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), BODY_FONT)


def set_run_font(run, size_pt: float, bold: bool = False, color: RGBColor | None = None) -> None:
    run.font.name = BODY_FONT
    r_pr = run._element.get_or_add_rPr()
    _set_rfonts(r_pr)
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    if color is not None:
        run.font.color.rgb = color


def set_paragraph_mark_font(paragraph: Paragraph, size_pt: float | None = None) -> None:
    p_pr = paragraph._p.get_or_add_pPr()
    r_pr = p_pr.find(qn("w:rPr"))
    if r_pr is None:
        r_pr = OxmlElement("w:rPr")
        p_pr.append(r_pr)
    _set_rfonts(r_pr)
    if size_pt is not None:
        sz = r_pr.find(qn("w:sz"))
        if sz is None:
            sz = OxmlElement("w:sz")
            r_pr.append(sz)
        sz.set(qn("w:val"), str(int(size_pt * 2)))


def configure_opensans_defaults(doc: Document) -> None:
    normal = doc.styles["Normal"]
    normal.font.name = BODY_FONT
    normal.font.size = Pt(9)
    styles = doc.styles.element
    doc_defaults = styles.find(qn("w:docDefaults"))
    if doc_defaults is None:
        doc_defaults = OxmlElement("w:docDefaults")
        styles.insert(0, doc_defaults)
    rpr_default = doc_defaults.find(qn("w:rPrDefault"))
    if rpr_default is None:
        rpr_default = OxmlElement("w:rPrDefault")
        doc_defaults.append(rpr_default)
    r_pr = rpr_default.find(qn("w:rPr"))
    if r_pr is None:
        r_pr = OxmlElement("w:rPr")
        rpr_default.append(r_pr)
    _set_rfonts(r_pr)
    sz = r_pr.find(qn("w:sz"))
    if sz is None:
        sz = OxmlElement("w:sz")
        r_pr.append(sz)
    sz.set(qn("w:val"), "18")


def apply_opensans_all(doc: Document) -> None:
    for section in doc.sections:
        for paragraph in section.header.paragraphs:
            set_paragraph_mark_font(paragraph, 9)
        for paragraph in section.footer.paragraphs:
            set_paragraph_mark_font(paragraph, 9)
    for p_el in doc.element.body.iter(qn("w:p")):
        set_paragraph_mark_font(Paragraph(p_el, doc), 9)


def clear_element_children(element) -> None:
    for child in list(element):
        element.remove(child)


def add_cobrand_color(paragraph) -> None:
    names = (
        "externado-color.png",
        "cleantechhub-color.png",
        "observatorio-color.png",
    )
    for idx, name in enumerate(names):
        if idx:
            paragraph.add_run("      ")
        run = paragraph.add_run()
        run.add_picture(str(LOGOS / name), height=Inches(0.17))


def setup_header_footer(section) -> None:
    header = section.header
    clear_element_children(header._element)
    hp = header.add_paragraph()
    hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    hp.paragraph_format.space_before = Pt(0)
    hp.paragraph_format.space_after = Pt(3)
    hp.add_run().add_picture(str(HEADER_BAND), width=A4_WIDTH)
    set_paragraph_mark_font(hp, 9)

    lp = header.add_paragraph()
    lp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    lp.paragraph_format.space_before = Pt(4)
    lp.paragraph_format.space_after = Pt(6)
    add_cobrand_color(lp)
    set_paragraph_mark_font(lp, 9)

    footer = section.footer
    clear_element_children(footer._element)
    fp = footer.add_paragraph()
    fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    ft = fp.add_run("Observa. Actúa. Transforma.")
    set_run_font(ft, 9, bold=True, color=NAVY)
    fp.add_run("    ")
    add_cobrand_color(fp)
    set_paragraph_mark_font(fp, 9)
    bp = footer.add_paragraph()
    bp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    bp.paragraph_format.space_before = Pt(2)
    bp.paragraph_format.space_after = Pt(0)
    bp.add_run().add_picture(str(FOOTER_BAND), width=A4_WIDTH)
    set_paragraph_mark_font(bp, 9)


def clear_body(doc: Document) -> None:
    body = doc.element.body
    for child in list(body):
        if child.tag != qn("w:sectPr"):
            body.remove(child)


def build() -> None:
    doc = Document(str(TEMPLATE))
    configure_opensans_defaults(doc)
    section = doc.sections[0]
    section.page_height = Mm(297)
    section.page_width = Mm(210)
    section.top_margin = Inches(1.62)
    section.bottom_margin = Inches(0.62)
    section.left_margin = Inches(0.45)
    section.right_margin = Inches(0.45)
    section.header_distance = Inches(0)
    section.footer_distance = Inches(0.12)

    setup_header_footer(section)
    clear_body(doc)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("AGENDA · 24 NOVIEMBRE 2026")
    set_run_font(r, 9, bold=True, color=GREEN)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("Datatón · Lanzamiento suave del Observatorio de la Tierra")
    set_run_font(r, 13, bold=True, color=NAVY)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(
        "Soft launch del Datalab · martes 24 de noviembre de 2026 · Universidad Externado de Colombia"
    )
    set_run_font(r, 9, bold=False, color=NAVY)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(VENUE)
    set_run_font(r, 9, bold=False, color=NAVY)

    head = doc.add_table(rows=1, cols=2)
    head.alignment = WD_TABLE_ALIGNMENT.CENTER
    head.autofit = False
    head.columns[0].width = Inches(3.2)
    head.columns[1].width = Inches(3.0)
    c0, c1 = head.rows[0].cells
    for cell in (c0, c1):
        set_paragraph_mark_font(cell.paragraphs[0], 9)
    r0 = c0.paragraphs[0].add_run("Programa del día")
    set_run_font(r0, 11, bold=True, color=NAVY)
    c1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r1 = c1.paragraphs[0].add_run("HORARIOS ORIENTATIVOS")
    set_run_font(r1, 9, bold=True, color=GREEN)
    set_cell_bottom_border(head)

    table = doc.add_table(rows=1 + len(ROWS), cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(0.72)
    table.columns[1].width = Inches(5.48)

    hdr = table.rows[0].cells
    set_cell_shading(hdr[0], "0C498A")
    set_cell_shading(hdr[1], "0C498A")
    for cell in hdr:
        set_paragraph_mark_font(cell.paragraphs[0], 9)
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
        set_paragraph_mark_font(p0, 9)
        rt = p0.add_run(hora)
        set_run_font(rt, 9, bold=True, color=GREEN)

        p1 = row[1].paragraphs[0]
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after = Pt(0)
        set_paragraph_mark_font(p1, 9)
        lines = actividad.split("\n")
        for j, line in enumerate(lines):
            if j:
                p1.add_run().add_break()
            run = p1.add_run(line)
            if line.strip().startswith("Modera "):
                set_run_font(run, 9, bold=True, color=GREEN)
            else:
                set_run_font(run, 9, bold=False, color=BLUE_TEXT)

    apply_opensans_all(doc)
    doc.save(OUT)
    print(OUT)


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