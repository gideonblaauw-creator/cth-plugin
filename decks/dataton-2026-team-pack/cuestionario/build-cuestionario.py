#!/usr/bin/env python3
"""Build Cuestionario-Dataton-24nov-equipos.docx + PDF + example images."""
from __future__ import annotations

import re
import subprocess
import sys
import zipfile
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Mm, Pt, RGBColor
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
PACK = ROOT.parent
ASSETS = ROOT / "assets"
OUT_DOCX = ROOT / "Cuestionario-Dataton-24nov-equipos.docx"
OUT_PDF = ROOT / "Cuestionario-Dataton-24nov-equipos.pdf"
LOGO = PACK / "assets/cth-logo-color.png"
HEATMAP_PNG = ASSETS / "ejemplo-mapa-calor-air4u.png"
DASH_PNG = ASSETS / "ejemplo-tablero-air4u.png"

NAVY = RGBColor(0x0C, 0x49, 0x8A)
GREY = RGBColor(0x66, 0x66, 0x66)
AI_MARKER = "INSTRUCCIÓN PARA LA IA (copiar y pegar)"

JARGON_RE = re.compile(
    r"(?i)\b("
    r"REO|Medallion|Delta|ETL|VP1|"
    r"grada|copia maestra|"
    r"A1[0-5]|B[1-7]|S[1-6]|G[1-9]|"
    r"Línea base|Paisaje|Bronce|Plata|Oro"
    r")\b"
)
# Slash-separated rubric tuples only (e.g. "R, H, F" in AI boxes — excluded from readable scan).
RUBRIC_SLASH_RE = re.compile(r"\b[RHFASQGML]\s*/\s*[RHFASQGML]")
FREE_RE = re.compile(r"(?i)\b(gratis|gratuito|sin costo)\b")

# Tables whose first cell starts with AI_MARKER are excluded from jargon grep.
AI_TABLE_IDS: set[int] = set()
_table_counter = 0


def _font_path() -> Path:
    p = ASSETS / "OpenSans-Regular.ttf"
    return p if p.is_file() else Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")


def _set_doc_defaults(doc: Document) -> None:
    for name, size in (("Heading 1", 14), ("Heading 2", 11), ("Normal", 9.5)):
        st = doc.styles[name]
        st.font.name = "Open Sans"
        st.font.size = Pt(size)
        st.font.color.rgb = NAVY if name.startswith("Heading") else RGBColor(0x33, 0x33, 0x33)
    normal = doc.styles["Normal"]
    normal.paragraph_format.space_after = Pt(3)
    normal.paragraph_format.line_spacing = 1.1


def _footer_inspira(doc: Document) -> None:
    section = doc.sections[0]
    section.top_margin = Mm(14)
    section.bottom_margin = Mm(14)
    section.left_margin = Mm(14)
    section.right_margin = Mm(14)
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Inspira. Actúa. Transforma. · CleantechHUB · Datatón 24 nov 2026")
    run.font.size = Pt(7.5)
    run.font.color.rgb = GREY


def _header_logo(doc: Document) -> None:
    if not LOGO.is_file():
        return
    section = doc.sections[0]
    header = section.header
    p = header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run()
    run.add_picture(str(LOGO), width=Mm(32))


def _para(doc: Document, text: str, *, bold: bool = False, size: float | None = None) -> None:
    p = doc.add_paragraph(style="Normal")
    run = p.add_run(text)
    run.bold = bold
    if size:
        run.font.size = Pt(size)


def _example_line(doc: Document, text: str) -> None:
    p = doc.add_paragraph(style="Normal")
    run = p.add_run(f"Ejemplo: {text}")
    run.italic = True
    run.font.color.rgb = GREY
    run.font.size = Pt(8.5)


def _part_meta(
    doc: Document,
    sirve: str,
    entregan: str,
    cuando: str,
    tiempo: str,
) -> None:
    rows = [
        ("Para qué sirve", sirve),
        ("Qué entregan", entregan),
        ("Cuándo", cuando),
        ("Tiempo", tiempo),
    ]
    table = doc.add_table(rows=len(rows), cols=2)
    table.style = "Table Grid"
    for i, (k, v) in enumerate(rows):
        table.rows[i].cells[0].text = k
        table.rows[i].cells[1].text = v
        for c in table.rows[i].cells:
            for para in c.paragraphs:
                para.style = "Normal"
                for run in para.runs:
                    run.font.size = Pt(9)


def _example_in_cell(cell, text: str) -> None:
    p = cell.add_paragraph()
    run = p.add_run(f"Ejemplo: {text}")
    run.italic = True
    run.font.color.rgb = GREY
    run.font.size = Pt(8.5)


def _qa_table(doc: Document, questions: list[tuple[str, str]]) -> None:
    global _table_counter
    table = doc.add_table(rows=1 + len(questions), cols=2)
    table.style = "Table Grid"
    hdr = table.rows[0].cells
    hdr[0].text = "Pregunta"
    hdr[1].text = "Respuesta"
    for i, (q, ex) in enumerate(questions, start=1):
        c0 = table.rows[i].cells[0]
        c0.text = q
        for para in c0.paragraphs:
            for run in para.runs:
                run.font.size = Pt(9)
        if ex:
            _example_in_cell(c0, ex)
        table.rows[i].cells[1].text = ""
        # Taller answer cells
        for para in table.rows[i].cells[1].paragraphs:
            para.add_run("\n\n")
    _table_counter += 1


def _ai_table(doc: Document, body: str) -> None:
    global _table_counter
    table = doc.add_table(rows=1, cols=1)
    table.style = "Table Grid"
    cell = table.rows[0].cells[0]
    cell.text = ""
    p0 = cell.paragraphs[0]
    r0 = p0.add_run(AI_MARKER)
    r0.bold = True
    r0.font.size = Pt(9)
    for line in body.strip().split("\n"):
        p = cell.add_paragraph(line)
        p.style = "Normal"
        for run in p.runs:
            run.font.size = Pt(8)
    AI_TABLE_IDS.add(_table_counter)
    _table_counter += 1


def _rules_box(doc: Document) -> None:
    table = doc.add_table(rows=1, cols=1)
    table.style = "Table Grid"
    cell = table.rows[0].cells[0]
    cell.text = ""
    title = cell.paragraphs[0]
    rt = title.add_run("Reglas para ustedes")
    rt.bold = True
    rules = [
        "Si no saben, escriban «no sé». No inventen cifras.",
        "Usen el rol de la persona, no nombres propios.",
        "No incluyan datos personales de clientes ni pacientes.",
        "Guarden el archivo y súbanlo a su herramienta de inteligencia artificial favorita.",
    ]
    for rule in rules:
        cell.add_paragraph(f"• {rule}", style="Normal")


def _embed_image(doc: Document, path: Path, width_cm: float = 15.0) -> None:
    if path.is_file():
        doc.add_picture(str(path), width=Cm(width_cm))


def render_example_images() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    font = ImageFont.truetype(str(_font_path()), 14)
    font_sm = ImageFont.truetype(str(_font_path()), 11)
    font_lg = ImageFont.truetype(str(ASSETS / "OpenSans-SemiBold.ttf"), 16)

    # Heatmap — no invented metrics; qualitative only (hoja-4b: permissions weak, exports unclear)
    w, h = 820, 520
    img = Image.new("RGB", (w, h), "#FFFFFF")
    dr = ImageDraw.Draw(img)
    dr.rectangle([0, 0, w, 46], fill="#0C498A")
    dr.text((12, 12), "Ejemplo · datos de ejemplo", fill="white", font=font_lg)
    dr.text((12, 62), "Mapa de calor por área del negocio (ilustración Air4U — clínica piloto, Bogotá)", fill="#0C498A", font=font)
    areas = [
        ("Mediciones en el sitio", "tibio"),
        ("Permisos para usar datos", "frío"),
        ("Exportación y respaldos", "frío"),
        ("Operación diaria (filtros)", "tibio"),
        ("Relación con la clínica", "tibio"),
        ("Datos abiertos de la ciudad", "frío"),
    ]
    colors = {"frío": "#B2EEF9", "tibio": "#FFF3CD", "caliente": "#F8D7DA"}
    x0, y0 = 40, 100
    bw, bh, gap = 230, 70, 16
    for i, (label, temp) in enumerate(areas):
        col, row = i % 3, i // 3
        x = x0 + col * (bw + gap)
        y = y0 + row * (bh + gap)
        dr.rectangle([x, y, x + bw, y + bh], fill=colors[temp], outline="#0C498A")
        dr.text((x + 8, y + 8), label, fill="#0C498A", font=font_sm)
        dr.text((x + 8, y + 36), temp.capitalize(), fill="#333333", font=font_sm)
    dr.text((12, h - 32), "Sin cifras inventadas — solo prioridades cualitativas del ejemplo Air4U.", fill="#666666", font=font_sm)
    img.save(HEATMAP_PNG, dpi=(200, 200))

    # Dashboard — only numeric: 5 µg/m³ (hoja-4b Panel 2)
    img2 = Image.new("RGB", (820, 560), "#F8FAFC")
    dr2 = ImageDraw.Draw(img2)
    dr2.rectangle([0, 0, w, 46], fill="#0C498A")
    dr2.text((12, 12), "Ejemplo · datos de ejemplo", fill="white", font=font_lg)
    dr2.rectangle([20, 60, w - 20, 130], fill="white", outline="#669348", width=2)
    dr2.text((28, 68), "Decisión esta semana", fill="#669348", font=font_sm)
    dr2.text(
        (28, 88),
        "¿Activar ventilación extra o revisar filtros por PM₂.₅ en interior?",
        fill="#0C498A",
        font=font,
    )
    panels = [
        ("Aire en interior", "sin dato", "estimado"),
        ("Referencia OMS", "5 µg/m³", "referencia"),
        ("Aire exterior (contexto)", "sin dato", "estimado"),
    ]
    px, py = 20, 150
    pw = (w - 50) // 3
    for i, (title, val, conf) in enumerate(panels):
        x = px + i * (pw + 5)
        dr2.rectangle([x, py, x + pw - 8, py + 160], fill="white", outline="#0C498A")
        dr2.text((x + 8, py + 8), title, fill="#0C498A", font=font_sm)
        dr2.text((x + 8, py + 50), val, fill="#333333", font=font_lg)
        dr2.text((x + 8, py + 100), conf, fill="#666666", font=font_sm)
    dr2.rectangle([20, 330, w - 20, 380], fill="#FFF3CD", outline="#E0A800")
    dr2.text((28, 342), "No publicar tablero: derechos de datos aún abiertos (ejemplo Air4U).", fill="#664D03", font=font)
    img2.save(DASH_PNG, dpi=(200, 200))


AI_P0 = """Lea el documento completo que el equipo subió. Use solo sus respuestas; marque «desconocido» lo que no contestaron. Escriba en español de Colombia.
Arme un resumen de una página con: territorio, comunidad, problema, solución, canales, ingresos, actividades clave, aliados, costos principales e impacto territorial. No invente cifras ni nombres de personas."""

AI_P1 = """Lea el documento subido. Use solo respuestas del equipo. Marque desconocidos. No invente números. Español de Colombia.
Aplique la rúbrica interna REO / mapa de calor (puntuación R, H, F, A, Q, G por conjunto de datos) solo para orientar el análisis; no muestre esas letras al equipo.
Devuelva: (1) mapa de calor por área del negocio (frío / tibio / caliente); (2) lista corta «qué falta» para poder decidir con datos."""

AI_P2 = """Lea el documento subido. Use solo respuestas del equipo. Marque desconocidos. No invente números. Español de Colombia.
Evalúe el flujo con la escalera Medallion / niveles Bronce, Plata, Oro (B1–B7, S1–S6, G1–G9) en sus notas internas; explique al equipo en una línea: Bronce = dato crudo, Plata = limpio y ordenado, Oro = listo para decidir. Aclare que son niveles de confianza, no premios.
Entregue: nivel sugerido, brecha principal y un paso concreto para subir un nivel."""

AI_P3 = """Lea el documento subido. Use solo respuestas del equipo. Marque desconocidos. No invente números. Español de Colombia.
Use marco Delta / Línea base / Paisaje (Hojas 3–4, VP1, grada de confianza) solo en su razonamiento interno.
Entregue boceto de tablero de una pantalla: rol, decisión de la semana, 2–3 números con fuente y firme/estimado. Si los derechos de datos no están claros, escriba «no publicar»."""

AI_P4 = """Lea el documento subido. Use solo respuestas del equipo. Marque desconocidos. No invente números. Español de Colombia.
Redacte guion de pitch de 5 minutos (problema, datos usados, pantalla, beneficio, pasos 30 y 90 días). Marque cualquier cifra sin fuente. Funciona en ChatGPT, Gemini o Grok (cuentas estándar)."""


def build_docx() -> Document:
    global _table_counter, AI_TABLE_IDS
    _table_counter = 0
    AI_TABLE_IDS.clear()

    doc = Document()
    _set_doc_defaults(doc)
    _header_logo(doc)
    _footer_inspira(doc)

    doc.add_heading("Cuestionario del Datatón — su equipo", level=1)
    _para(
        doc,
        "Complete este archivo con sus palabras. Al final del día tendrán un mapa de prioridades de "
        "sus datos, el nivel de confianza de su información principal, un boceto de tablero y, si "
        "pasan a finales, un guion de pitch.",
    )
    _para(doc, "Cómo usarlo (3 pasos):", bold=True)
    for step in (
        "1) Contesten cada pregunta en la columna «Respuesta».",
        "2) Guarden este archivo en Word (.docx).",
        "3) Suban el archivo a ChatGPT, Gemini o Grok y copien la instrucción al final de cada parte.",
    ):
        doc.add_paragraph(step, style="Normal")
    _rules_box(doc)

    # Parte 0
    doc.add_heading("Parte 0. Su proyecto en una página", level=1)
    _part_meta(
        doc,
        "Ubica a su equipo: territorio, problema y cómo ayudan. Es la foto general antes de hablar de datos.",
        "Resumen de una página en sus palabras.",
        "Bloque 1 — mañana",
        "20 min",
    )
    q0 = [
        ("¿Dónde trabajan (ciudad, barrio, región)?", "Bogotá, barrio con clínica piloto de aire interior."),
        ("¿A qué personas o comunidad ayudan?", "Gestores de instalaciones y personal de una clínica."),
        ("¿Qué problema les resuelven?", "No saben si el aire interior es seguro esta semana."),
        ("¿Cómo lo resuelven?", "Sensores y alertas para decidir ventilación o filtros."),
        ("¿Cómo llegan a ellos?", "Instalación en sitio y contacto con el administrador del edificio."),
        ("¿Cómo ganan dinero?", "Contrato piloto con la clínica; modelo aún en prueba."),
        ("¿Qué hacen todos los días para que funcione?", "Revisar lecturas, mantener sensor y responder alertas."),
        ("¿Con quién se apoyan?", "Proveedor de sensores y personal de mantenimiento de la clínica."),
        ("¿Qué les cuesta más?", "Sacar reportes claros sin molestar al personal clínico."),
        ("¿Qué cambia en el territorio si les va bien?", "Menos exposición a aire contaminado en espacios de salud."),
    ]
    _qa_table(doc, q0)
    _ai_table(doc, AI_P0)

    # Parte 1
    doc.add_heading("Parte 1. ¿Qué información tienen y dónde está?", level=1)
    _part_meta(
        doc,
        "Inventaria hasta cinco tipos de información que ya manejan y dónde vive cada una.",
        "Mapa de calor por área del negocio y lista de huecos.",
        "Bloque 1 — mañana",
        "35 min",
    )
    _para(doc, "Liste hasta cinco tipos de información que ya recogen (ventas, clientes, mediciones, fotos, mensajes de WhatsApp, etc.).")
    q1_types = [
        ("Tipo de información 1", "Lecturas del sensor de partículas en la clínica."),
        ("Tipo de información 2", "Mensajes de WhatsApp con el técnico de mantenimiento."),
        ("Tipo de información 3", "Correos con el administrador del edificio."),
        ("Tipo de información 4", "no sé"),
        ("Tipo de información 5", "no sé"),
    ]
    _qa_table(doc, q1_types)
    _para(doc, "Para la información más importante de la lista, responda:", bold=True)
    q1_detail = [
        ("¿Dónde vive hoy (WhatsApp, papel, Excel, un sistema)?", "Base del proveedor del sensor; copias en WhatsApp."),
        ("¿Desde cuándo la llevan?", "Desde que instalaron el piloto este año."),
        ("¿Con qué frecuencia llega un dato nuevo?", "Cada hora en horario laboral; fuera de horario no sé."),
        ("¿Quién la cuida?", "El gestor de instalaciones del sitio."),
        ("¿Pueden descargarla o exportarla?", "Todavía no tenemos exportación simple."),
        ("¿Tienen permiso para usarla en el reto?", "Permiso del sitio piloto en trámite."),
    ]
    _qa_table(doc, q1_detail)
    _embed_image(doc, HEATMAP_PNG, 14)
    _ai_table(doc, AI_P1)

    # Parte 2
    doc.add_heading("Parte 2. ¿Cómo nace un dato y qué tan confiable es?", level=1)
    _part_meta(
        doc,
        "Describe el camino del dato más importante y qué tan ordenado está.",
        "Nivel de confianza sugerido y un paso para mejorarlo.",
        "Bloque 2 — tarde",
        "30 min",
    )
    q2 = [
        ("¿Cuál fue la información más importante de la Parte 1?", "Las lecturas del sensor en la clínica."),
        ("¿Qué pasa para crear un registro nuevo?", "El sensor mide; la plataforma guarda la lectura."),
        ("¿Cuáles son los pasos en orden?", "Medición → guardado en plataforma → aviso al gestor si hay alerta."),
        ("¿Quién participa en cada paso?", "Sensor automático; gestor revisa y avisa a mantenimiento."),
        ("¿Qué herramienta usan?", "Sensor en sitio y aplicación web del proveedor."),
        ("¿Qué anotan aparte del número?", "Comentarios en WhatsApp si hubo intervención."),
        ("¿Revisan errores? ¿Cómo?", "A veces comparan con lecturas manuales; sin rutina fija."),
        ("¿Qué les falta para confiar más?", "Un solo lugar con historial y exportación clara."),
    ]
    _qa_table(doc, q2)
    _para(doc, "Marque sí / no / no sé:", bold=True)
    q2_chk = [
        ("¿Cada registro tiene fecha?", "A veces en la plataforma, no siempre en WhatsApp."),
        ("¿Saben de dónde viene cada dato?", "Sí para el sensor; no siempre para los mensajes."),
        ("¿Lo guardan en un solo lugar?", "No — están repartidos."),
        ("¿Tienen reglas escritas para corregir errores?", "no sé"),
        ("¿Otra persona puede revisar los datos?", "El técnico de mantenimiento mira capturas."),
    ]
    _qa_table(doc, q2_chk)
    _ai_table(doc, AI_P2)

    # Parte 3
    doc.add_heading("Parte 3. ¿Qué decisión ayudan a tomar?", level=1)
    _part_meta(
        doc,
        "Conecta su dato con una decisión concreta de esta semana.",
        "Boceto de tablero de una pantalla.",
        "Bloque 2 — tarde",
        "35 min",
    )
    q3 = [
        ("¿Quién decide (solo el rol)?", "Gestor de instalaciones del sitio."),
        ("¿Qué decisión deben tomar esta semana?", "¿Activar ventilación extra o revisar filtros?"),
        ("Pregunta clave 1 que esa decisión necesita", "¿El PM₂.₅ en interior supera lo aceptable?"),
        ("Pregunta clave 2", "¿Hay alertas repetidas en el mismo horario?"),
        ("Pregunta clave 3", "¿Qué pasó la última vez que intervinieron?"),
        ("Número 1 que tienen (firme o estimado)", "Lecturas recientes del sensor — estimado, sin cifra acordada."),
        ("Número 2 (firme o estimado)", "Referencia OMS: 5 µg/m³ como referencia anual (del material de ejemplo)."),
        ("Número 3 (firme o estimado)", "Contexto de aire exterior en la ciudad — no sé."),
        ("¿Cómo estaba el cliente/sitio antes?", "Sin monitoreo continuo visible para el gestor."),
        ("¿Qué cambia si ustedes actúan?", "Menos tiempo con aire poco saludable en salas de espera."),
        ("¿Qué dato abierto del territorio ayuda como contexto?", "Indicadores públicos de calidad del aire en Bogotá — aún sin enlace."),
    ]
    _qa_table(doc, q3)
    _embed_image(doc, DASH_PNG, 14)
    _ai_table(doc, AI_P3)

    # Parte 4
    doc.add_heading("Parte 4. Su pitch de 5 minutos", level=1)
    _part_meta(
        doc,
        "Solo para los seis finalistas: guion corto con datos y pantalla.",
        "Guion de cinco minutos.",
        "Bloque 2 — finales",
        "15 min",
    )
    q4 = [
        ("¿Problema y persona afectada?", "Personal y pacientes con aire interior incierto."),
        ("¿Qué datos usaron en el reto?", "Lecturas del sensor y referencia de salud OMS."),
        ("¿Qué muestra su pantalla?", "Decisión de ventilación y tres números con fuente."),
        ("¿A quién beneficia?", "Clínica piloto y quienes trabajan en el sitio."),
        ("¿Próximo paso a 30 y 90 días?", "30 días: exportar historial; 90 días: rutina con la clínica."),
    ]
    _qa_table(doc, q4)
    _ai_table(doc, AI_P4)

    doc.save(OUT_DOCX)
    return doc


def convert_pdf() -> None:
    subprocess.run(
        [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(ROOT),
            str(OUT_DOCX),
        ],
        check=True,
        capture_output=True,
    )
    if not OUT_PDF.is_file():
        raise SystemExit("LibreOffice did not produce PDF")


def docx_readable_text(path: Path) -> str:
    """Plain text outside AI instruction tables."""
    from docx import Document as D

    doc = D(path)
    parts: list[str] = []
    for p in doc.paragraphs:
        parts.append(p.text)
    ai_idx = 0
    for table in doc.tables:
        first = table.rows[0].cells[0].text.strip()
        if first.startswith("INSTRUCCIÓN PARA LA IA"):
            ai_idx += 1
            continue
        if "Reglas para ustedes" in first:
            continue
        for row in table.rows:
            for cell in row.cells:
                parts.append(cell.text)
    return "\n".join(parts)


def grep_self_check() -> tuple[list[str], list[str]]:
    text = docx_readable_text(OUT_DOCX)
    jargon = [m.group(0) for m in JARGON_RE.finditer(text)]
    jargon += [m.group(0) for m in RUBRIC_SLASH_RE.finditer(text)]
    free = [m.group(0) for m in FREE_RE.finditer(text)]
    return jargon, free


def main() -> int:
    render_example_images()
    build_docx()
    convert_pdf()
    jargon, free = grep_self_check()
    print("grep_jargon_hits", len(jargon), jargon[:20])
    print("grep_free_hits", len(free), free)
    if jargon or free:
        print("SELF-CHECK FAILED", file=sys.stderr)
        return 1
  # page count
    import fitz

    doc = fitz.open(OUT_PDF)
    n = doc.page_count
    doc.close()
    print("pdf_pages", n)
    if n > 8:
        print("WARNING: PDF exceeds 8 pages", file=sys.stderr)
        return 1
    print("docx", OUT_DOCX)
    print("pdf", OUT_PDF)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())