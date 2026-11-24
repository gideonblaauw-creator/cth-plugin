#!/usr/bin/env python3
"""Assemble Guia-tecnica-mentores.docx from hojas + prompts (layout only)."""
from __future__ import annotations

import difflib
import hashlib
import re
import subprocess
import sys
import tempfile
import zipfile
from html.parser import HTMLParser
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.oxml.ns import qn as oxml_qn
from docx.shared import Mm, Pt, RGBColor
from docxcompose.composer import Composer

ROOT = Path(__file__).resolve().parent.parent
GUIA_DIR = Path(__file__).resolve().parent
TEAM = ROOT / "team-pack-es"
PRINT = ROOT / "print"
ASSETS = ROOT / "cuestionario" / "assets"
OUT_DOCX = GUIA_DIR / "Guia-tecnica-mentores.docx"
OUT_PDF = GUIA_DIR / "Guia-tecnica-mentores.pdf"
BASELINE_DOCX_SHA = "443a9fffa0465aaa9c8434a2d78c5a33d355dcd068b4a6f807717f436c91fe"
PRE_ADDENDUM_DOCX_REF = "73885721053aa956b8337f20f39d6baaa7451c6a"
LOGO = ROOT / "assets/cth-logo-color.png"
HEADER_TEXT = "Guía técnica — para mentores"
NAVY = RGBColor(0x0C, 0x49, 0x8A)
M1_LEVEL_LINES = (
    "ninguno: el dato está solo en chats o en la memoria, sin permiso o sin poder descargarlo. "
    "Empezar aquí es normal.",
    "bronce: guardado en un lugar con responsable, con permiso escrito y se puede descargar como archivo.",
    "plata: limpio, con reglas de limpieza escritas y calidad revisada.",
    "oro: listo para una decisión y un público con nombre.",
)

SOURCES: list[tuple[str, Path, str]] = [
    ("Hoja 1 — mapa de calor", TEAM / "hoja-1-mapa-de-calor.md", "markdown"),
    ("Hoja 2 — flujo de datos", TEAM / "hoja-2-flujo-de-datos.md", "markdown"),
    ("Hoja 3 — dato a valor", TEAM / "hoja-3-dato-a-valor.md", "markdown"),
    ("Hoja 4 — plantilla tablero", TEAM / "hoja-4-plantilla-tablero.md", "markdown"),
    ("Hoja 4b — ejemplo Air4U", TEAM / "hoja-4b-ejemplo-air4u.md", "markdown"),
    ("Hoja 5 — plantilla pitch", TEAM / "hoja-5-plantilla-pitch.md", "markdown"),
    ("Prompts IA v2 — rúbrica de puntuación", PRINT / "prompts-ia-v2.html", "html"),
]


def _table_borders(table) -> None:
    tbl = table._tbl
    tbl_pr = tbl.tblPr
    if tbl_pr is None:
        tbl_pr = OxmlElement("w:tblPr")
        tbl.insert(0, tbl_pr)
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(oxml_qn("w:val"), "single")
        el.set(oxml_qn("w:sz"), "4")
        el.set(oxml_qn("w:space"), "0")
        el.set(oxml_qn("w:color"), "000000")
        borders.append(el)
    old = tbl_pr.find(oxml_qn("w:tblBorders"))
    if old is not None:
        tbl_pr.remove(old)
    tbl_pr.append(borders)


def _insert_table_after_paragraph(doc: Document, paragraph, rows: int, cols: int):
    table = doc.add_table(rows=rows, cols=cols)
    tbl_el = table._tbl
    body = tbl_el.getparent()
    body.remove(tbl_el)
    paragraph._p.addnext(tbl_el)
    return table


def _remove_paragraph(paragraph) -> None:
    element = paragraph._element
    element.getparent().remove(element)


def _fill_boceto_cells(table) -> None:
    r0 = ("LÍNEA BASE", "DELTA", "PAISAJE")
    r1 = ("[N1] (firme/est.)", "[N2]", "[N3]")
    r2 = ("nota breve", "nota breve", "nota breve")
    for ri, row_data in enumerate((r0, r1, r2)):
        for ci, text in enumerate(row_data):
            table.rows[ri].cells[ci].text = text


def _fill_puente_cells(table) -> None:
    merged = table.rows[0].cells[0]
    for c in table.rows[0].cells[1:]:
        merged = merged.merge(c)
    merged.text = "Delta: donde el dato se vuelve valor\nentradas › salida › línea valor"
    row2 = (
        "Línea base del cliente (entrada)",
        "Delta innovador (su intervención) (salida)",
        "Panorama datos abiertos (entrada)",
    )
    for ci, text in enumerate(row2):
        table.rows[1].cells[ci].text = text


def _fix_autocontrol_checkboxes(doc: Document) -> None:
    for para in doc.paragraphs:
        if "\u2610" not in para.text:
            continue
        for run in para.runs:
            if "\u2610" in run.text:
                run.text = run.text.replace("\u2610", "[ ]")


TEXT_WIDTH_TWIPS = 9026
MIN_COL_TWIPS = 1440
HEADER_FILL = "0C498A"


def _set_cell_width(cell, width_twips: int) -> None:
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcW = tcPr.find(qn("w:tcW"))
    if tcW is None:
        tcW = OxmlElement("w:tcW")
        tcPr.append(tcW)
    tcW.set(qn("w:type"), "dxa")
    tcW.set(qn("w:w"), str(width_twips))


def _set_table_full_width(table) -> None:
    tbl = table._tbl
    tblPr = tbl.tblPr
    if tblPr is None:
        tblPr = OxmlElement("w:tblPr")
        tbl.insert(0, tblPr)
    tblW = tblPr.find(qn("w:tblW"))
    if tblW is None:
        tblW = OxmlElement("w:tblW")
        tblPr.append(tblW)
    tblW.set(qn("w:type"), "pct")
    tblW.set(qn("w:w"), "5000")
    layout = tblPr.find(qn("w:tblLayout"))
    if layout is None:
        layout = OxmlElement("w:tblLayout")
        tblPr.append(layout)
    layout.set(qn("w:type"), "fixed")
    _table_borders(table)


def _set_table_col_widths(table, widths: list[int]) -> None:
    tbl = table._tbl
    tblGrid = tbl.find(qn("w:tblGrid"))
    if tblGrid is None:
        tblGrid = OxmlElement("w:tblGrid")
        tbl.append(tblGrid)
    else:
        for grid_col in list(tblGrid):
            tblGrid.remove(grid_col)
    for w in widths:
        grid_col = OxmlElement("w:gridCol")
        grid_col.set(qn("w:w"), str(w))
        tblGrid.append(grid_col)
    ncols = len(widths)
    for row in table.rows:
        for ci, cell in enumerate(row.cells):
            _set_cell_width(cell, widths[ci % ncols])


def _shade_header_row(table) -> None:
    if not table.rows:
        return
    row = table.rows[0]
    for cell in row.cells:
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        shd = tcPr.find(qn("w:shd"))
        if shd is None:
            shd = OxmlElement("w:shd")
            tcPr.append(shd)
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), HEADER_FILL)
        for para in cell.paragraphs:
            for run in para.runs:
                run.bold = True
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)


def _table_column_widths(ncols: int) -> list[int]:
    if ncols < 1:
        return []
    if ncols * MIN_COL_TWIPS <= TEXT_WIDTH_TWIPS:
        base = max(MIN_COL_TWIPS, TEXT_WIDTH_TWIPS // ncols)
        widths = [base] * ncols
        widths[-1] += TEXT_WIDTH_TWIPS - sum(widths)
        return widths
    # More columns than 1" minimum allows on one line: equal split to full text width.
    base = TEXT_WIDTH_TWIPS // ncols
    rem = TEXT_WIDTH_TWIPS - base * ncols
    widths = [base] * ncols
    for i in range(rem):
        widths[i] += 1
    return widths


def fix_guia_tables(doc: Document) -> None:
    for table in doc.tables:
        ncols = len(table.columns)
        if ncols < 1:
            continue
        widths = _table_column_widths(ncols)
        _set_table_full_width(table)
        _set_table_col_widths(table, widths)
        _shade_header_row(table)


TWIPS_12MM = 680
TWIPS_25MM = 1417
HOJA4_WRITE_HEADERS = (
    "Usuario (rol, no nombre personal)",
    "Decisión (una frase: ¿debe [acción] antes de [cuándo]?)",
    "Línea de valor (una frase: dinero, riesgo, tiempo o salud)",
)


def _set_row_height_exact(row, twips: int) -> None:
    tr = row._tr
    trPr = tr.get_or_add_trPr()
    old = trPr.find(qn("w:trHeight"))
    if old is not None:
        trPr.remove(old)
    tr_height = OxmlElement("w:trHeight")
    tr_height.set(qn("w:val"), str(twips))
    tr_height.set(qn("w:hRule"), "exact")
    trPr.append(tr_height)


def _merge_row_single_col(row) -> None:
    if len(row.cells) < 2:
        return
    merged = row.cells[0]
    for cell in row.cells[1:]:
        merged = merged.merge(cell)


def fix_hoja4_docx_write_tables(doc: Document) -> None:
    """Mirror hoja-4 PDF writing boxes in Word (layout only)."""
    for table in doc.tables:
        if not table.rows:
            continue
        label = table.rows[0].cells[0].text.strip()
        if label in HOJA4_WRITE_HEADERS and len(table.columns) >= 2:
            for row in table.rows:
                _merge_row_single_col(row)
            if len(table.rows) > 1:
                _set_row_height_exact(table.rows[1], TWIPS_12MM)
            continue
        if table.rows[0].cells[0].text.strip() == "Antes / sitio A" and len(table.rows) > 1:
            _set_row_height_exact(table.rows[1], TWIPS_25MM)


HOJA5_TIE_OLD = "Si hay empate, gana la mayor nota de honestidad."
HOJA5_TIE_NEW = "Si empatan en utilidad y honestidad, desempata la historia."


HOJA1_SCALE_MARKERS = (
    "Historia (H)",
    "Frecuencia (F)",
    "Acceso técnico (A)",
    "Acceso legal / ético (G)",
)
SCALE_TABLE_HEADER = ("0–3", "Significado (resumen)")


def _paragraph_has_image(paragraph) -> bool:
    return bool(paragraph._p.xpath(".//a:blip"))


def _parse_pipe_scale_block(text: str) -> tuple[list[tuple[str, str]], str]:
    table_rows: list[tuple[str, str]] = []
    tail_lines: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if "|" not in line:
            tail_lines.append(line.rstrip("|").strip())
            continue
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) >= 2 and (parts[0] in {"0", "1", "2", "3", "0–3"} or parts[0].startswith("0")):
            table_rows.append((parts[0], parts[1]))
        else:
            tail_lines.append(" ".join(parts).rstrip("|").strip())
    tail = " ".join(t for t in tail_lines if t).strip().rstrip("|").strip()
    return table_rows, tail


def _fill_scale_table(table, rows: list[tuple[str, str]]) -> None:
    table.rows[0].cells[0].text = SCALE_TABLE_HEADER[0]
    table.rows[0].cells[1].text = SCALE_TABLE_HEADER[1]
    for ri, (left, right) in enumerate(rows, start=1):
        table.rows[ri].cells[0].text = left
        table.rows[ri].cells[1].text = right
    _table_borders(table)
    _set_table_full_width(table)
    _set_table_col_widths(table, _table_column_widths(2))
    _shade_header_row(table)


def _insert_paragraph_after_element(doc: Document, after_el, text: str) -> None:
    new_p = OxmlElement("w:p")
    after_el.addnext(new_p)
    para = Paragraph(new_p, doc)
    para.add_run(text)


def fix_guia_hoja1_pipe_scales(doc: Document) -> None:
    """Turn H/F/A/G pipe paragraphs into 2-col tables (layout only, same words)."""
    paras = list(doc.paragraphs)
    for i, para in enumerate(paras):
        heading = para.text.strip()
        if not any(marker in heading for marker in HOJA1_SCALE_MARKERS):
            continue
        style = para.style.name if para.style else ""
        if "Heading" not in style:
            continue
        if i + 1 >= len(paras):
            continue
        nxt = paras[i + 1]
        if "|" not in nxt.text:
            continue
        rows, tail = _parse_pipe_scale_block(nxt.text)
        if not rows:
            continue
        table = _insert_table_after_paragraph(doc, para, 1 + len(rows), 2)
        _fill_scale_table(table, rows)
        _remove_paragraph(nxt)
        if tail:
            _insert_paragraph_after_element(doc, table._tbl, tail)


def fix_guia_cover_layout(doc: Document) -> None:
    """Restore cover logo + title styling lost during docxcompose merge."""
    if len(doc.paragraphs) < 3:
        return
    if doc.paragraphs[1].text.strip() != "Guía técnica para mentores":
        return
    logo_p = doc.paragraphs[0]
    if LOGO.is_file() and not _paragraph_has_image(logo_p):
        logo_p.text = ""
        logo_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        logo_p.add_run().add_picture(str(LOGO), width=Mm(40))
    title = doc.paragraphs[1]
    try:
        title.style = doc.styles["Title"]
    except KeyError:
        pass
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in title.runs:
        run.bold = True
        run.font.name = "Open Sans"
        run.font.size = Pt(22)
        run.font.color.rgb = NAVY
    sub = doc.paragraphs[2]
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in sub.runs:
        run.italic = True
        run.font.name = "Open Sans"
        run.font.size = Pt(12)
        run.font.color.rgb = NAVY


def fix_guia_hoja5_tiebreak_wording(doc: Document) -> None:
    """Guía-only tie-break (team hoja-5.md unchanged)."""
    for para in doc.paragraphs:
        text = para.text
        if "Complete cada bloque" in text and HOJA5_TIE_OLD in text:
            for run in para.runs:
                run.text = ""
            para.add_run(text.replace(HOJA5_TIE_OLD, HOJA5_TIE_NEW))


def fix_guia_paragraph_layout(doc: Document) -> None:
    for para in doc.paragraphs:
        style = para.style.name if para.style else ""
        if style in ("Heading 1", "Heading 2", "Heading 3") and para.alignment == WD_ALIGN_PARAGRAPH.CENTER:
            para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    to_remove: list = []
    streak = 0
    for para in doc.paragraphs:
        if not para.text.strip():
            streak += 1
            if streak > 1:
                to_remove.append(para)
        else:
            streak = 0
    for para in to_remove:
        _remove_paragraph(para)


def postprocess_guia_docx(doc: Document) -> None:
    for para in list(doc.paragraphs):
        if "CTH_BOCETO_TABLE_INSERT" in para.text:
            table = _insert_table_after_paragraph(doc, para, 3, 3)
            _fill_boceto_cells(table)
            _table_borders(table)
            _remove_paragraph(para)
            break
    else:
        raise SystemExit("Guía: CTH_BOCETO_TABLE_INSERT missing")

    for para in list(doc.paragraphs):
        if "CTH_PUENTE_TABLE_INSERT" in para.text:
            table = _insert_table_after_paragraph(doc, para, 2, 3)
            _fill_puente_cells(table)
            _table_borders(table)
            _remove_paragraph(para)
            break
    else:
        raise SystemExit("Guía: CTH_PUENTE_TABLE_INSERT missing")

    _fix_autocontrol_checkboxes(doc)
    fix_hoja4_docx_write_tables(doc)
    fix_guia_hoja1_pipe_scales(doc)
    fix_guia_tables(doc)
    fix_guia_hoja5_tiebreak_wording(doc)
    fix_guia_cover_layout(doc)
    fix_guia_paragraph_layout(doc)


def patch_docx_theme_open_sans(docx_path: Path) -> None:
    """Set theme major/minor latin typefaces to Open Sans in word/theme/theme1.xml."""
    theme = "word/theme/theme1.xml"
    major = re.compile(r"(<a:majorFont>\s*<a:latin typeface=\")[^\"]+(\")", re.DOTALL)
    minor = re.compile(r"(<a:minorFont>\s*<a:latin typeface=\")[^\"]+(\")", re.DOTALL)
    with zipfile.ZipFile(docx_path, "r") as zin:
        if theme not in zin.namelist():
            raise SystemExit(f"Missing {theme} in {docx_path}")
        raw = zin.read(theme).decode("utf-8")
        patched = major.sub(r"\1Open Sans\2", raw, count=1)
        patched = minor.sub(r"\1Open Sans\2", patched, count=1)
        if patched == raw:
            raise SystemExit(f"theme1.xml latin fonts not patched in {docx_path}")
        import io

        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = patched.encode("utf-8") if item.filename == theme else zin.read(item.filename)
                zout.writestr(item, data)
    docx_path.write_bytes(buf.getvalue())


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
    t = doc.add_heading("Guía técnica para mentores", level=0)
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = sub.add_run("Technical Guide for mentors")
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
    doc.add_paragraph("1. Niveles de confianza del dato (metodología v0.3)", style="Normal")
    doc.add_paragraph("2. Cómo elegimos los 6 y cómo decide el jurado", style="Normal")
    for i, (title, _, _) in enumerate(SOURCES, start=3):
        doc.add_paragraph(f"{i}. {title}", style="Normal")
    doc.add_page_break()


def _build_m1_page(doc: Document) -> None:
    doc.add_heading("Niveles de confianza del dato", level=1)
    doc.add_paragraph(
        "Use esta redacción con los equipos. Son niveles de confianza, no premios.",
        style="Normal",
    )
    for line in M1_LEVEL_LINES:
        doc.add_paragraph(line, style="Normal")
    doc.add_page_break()


def _build_m6_page(doc: Document) -> None:
    doc.add_heading("Cómo elegimos los 6 y cómo decide el jurado", level=1)
    bullets = [
        "Puntaje del mentor: utilidad 0–5 más honestidad 0–5, más 1 por cada número firme en plata u oro (máximo +3). "
        "En empate gana honestidad.",
        "Los mentores contrastan 2–3 números con la carpeta del equipo en Drive.",
        "Las finales a las 16:00 usan las mismas dos notas (utilidad, honestidad). "
        "Si empatan en utilidad y honestidad, desempata la historia.",
        "14 equipos › 6 finalistas › 3 ganadores, quienes entran al Datalab CTH en 2027. "
        "Todos reciben certificado.",
        "Ningún equipo queda fuera después del Bloque 1: las etiquetas advierten, no excluyen.",
        "La lista de los 6 finalistas se anuncia antes de las 16:00.",
    ]
    for item in bullets:
        doc.add_paragraph(f"• {item}", style="Normal")
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
        _build_m1_page(master)
        _build_m6_page(master)

        composer = Composer(master)
        for i, part in enumerate(part_paths):
            frag = Document(part)
            if i < len(part_paths) - 1:
                frag.add_page_break()
            composer.append(frag)

        composer.save(OUT_DOCX)

    final = Document(OUT_DOCX)
    postprocess_guia_docx(final)
    _apply_headers(final)
    final.save(OUT_DOCX)
    patch_docx_theme_open_sans(OUT_DOCX)


def _set_doc_defaults(doc: Document) -> None:
    for name in ("Heading 1", "Heading 2", "Normal"):
        st = doc.styles[name]
        st.font.name = "Open Sans"
        try:
            st._element.rPr.rFonts.set(qn("w:eastAsia"), "Open Sans")
        except Exception:
            pass


def build_styled_pdf() -> int:
    from render_guia_mentores_pdf import build_guia_pdf

    return build_guia_pdf()


def _ban_check(text: str, label: str) -> None:
    low = text.lower()
    for phrase in ("solo mentores", "no distribuir"):
        if phrase in low:
            raise SystemExit(f"{label}: banned phrase {phrase!r}")


def _grep_banned_guia(text: str) -> list[str]:
    found: list[str] = []
    for pat in (r"(?i)microcredencial", r"hasta\s+20"):
        for m in re.finditer(pat, text):
            found.append(m.group(0))
    return found


def _docx_from_git(ref: str) -> Document:
    import io

    proc = subprocess.run(
        ["git", "show", f"{ref}:decks/dataton-2026-team-pack/guia-tecnica/Guia-tecnica-mentores.docx"],
        cwd=str(ROOT.parent.parent),
        capture_output=True,
        check=True,
    )
    return Document(io.BytesIO(proc.stdout))


def _paragraph_diffs(base: Document, new: Document) -> list[tuple[int, str, str]]:
    changed: list[tuple[int, str, str]] = []
    for i, (a, b) in enumerate(zip(base.paragraphs, new.paragraphs)):
        if a.text != b.text:
            changed.append((i, a.text.strip(), b.text.strip()))
    if len(base.paragraphs) != len(new.paragraphs):
        changed.append((-1, str(len(base.paragraphs)), str(len(new.paragraphs))))
    return changed


RUN9_TEXT_REF = "72ea013b7b547b9650b6faaf03250cbf1c70a6b6"


SKIP_SCALE_HEADER = {
    re.sub(r"\s+", "", "0–3"),
    re.sub(r"\s+", "", "Significado (resumen)"),
}


def _guia_text_bag(doc: Document):
    """Multiset of wording units: pipe lines split; table body rows (skip header row)."""
    from collections import Counter

    chunks: list[str] = []

    def add(t: str) -> None:
        t = re.sub(r"\s+", "", t)
        if t and t not in SKIP_SCALE_HEADER:
            chunks.append(t)

    for p in doc.paragraphs:
        if "|" in p.text:
            for line in p.text.splitlines():
                for part in [x.strip() for x in line.split("|") if x.strip()]:
                    add(part)
        else:
            add(p.text)
    for table in doc.tables:
        for ri, row in enumerate(table.rows):
            if ri == 0:
                continue
            for cell in row.cells:
                for para in cell.paragraphs:
                    add(para.text)
    return Counter(chunks)


def _verify_guia_run9_text_unchanged() -> None:
    ref = _docx_from_git(RUN9_TEXT_REF)
    new = Document(OUT_DOCX)
    if _guia_text_bag(ref) != _guia_text_bag(new):
        raise SystemExit(f"guia docx text drift vs {RUN9_TEXT_REF[:8]} (wording multiset)")
    print("guia_docx_run9_text_diff", 0)


def main() -> int:
    build_docx()
    _verify_guia_run9_text_unchanged()
    from docx import Document as D

    parts = []
    doc = D(OUT_DOCX)
    for p in doc.paragraphs:
        parts.append(p.text)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                parts.append(cell.text)
    for section in doc.sections:
        parts.append(section.header.paragraphs[0].text if section.header.paragraphs else "")
    blob = "\n".join(parts)
    _ban_check(blob, "docx")
    bad = _grep_banned_guia(blob)
    if bad:
        raise SystemExit(f"guia banned tokens: {bad}")
    if not all(line in blob for line in M1_LEVEL_LINES):
        raise SystemExit("guia: M1 level definitions missing or altered")
    pages = build_styled_pdf()
    print("guia_docx", OUT_DOCX)
    print("guia_pdf", OUT_PDF)
    print("guia_pdf_pages", pages)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())