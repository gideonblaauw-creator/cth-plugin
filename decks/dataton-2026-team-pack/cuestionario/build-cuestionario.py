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
OUT_EJEMPLO_DOCX = ROOT / "Cuestionario-ejemplo-Air4U.docx"
OUT_EJEMPLO_PDF = ROOT / "Cuestionario-ejemplo-Air4U.pdf"
PROMPTS_TXT = ROOT / "prompts.txt"
EJEMPLO_HEADER = "Ejemplo · datos de ejemplo Air4U"
LOGO = PACK / "assets/cth-logo-color.png"
HEATMAP_PNG = ASSETS / "ejemplo-mapa-calor-air4u.png"
DASH_PNG = ASSETS / "ejemplo-tablero-air4u.png"

NAVY = RGBColor(0x0C, 0x49, 0x8A)
GREY = RGBColor(0x66, 0x66, 0x66)
AI_MARKER = "INSTRUCCIÓN PARA LA IA (copiar y pegar)"

JARGON_RE = re.compile(
    r"(?i)\b("
    r"REO|Medallion|Delta|ETL|VP1|"
    r"grada|dato crudo|copia maestra|microcredencial|"
    r"A1[0-5]|B[1-7]|S[1-6]|G[1-9]|"
    r"Línea base|Paisaje"
    r")\b"
)
TEAM_BAN_RE = re.compile(
    r"(?i)\b("
    r"REO|Medallion|B1|S1|G1|VP1|Delta|"
    r"Línea base|Paisaje|grada|dato crudo|hasta 20|microcredencial"
    r")\b"
)
M1_LEVEL_LINES = (
    "ninguno: el dato está solo en chats o en la memoria, sin permiso o sin poder descargarlo. "
    "Empezar aquí es normal.",
    "bronce: guardado en un lugar con responsable, con permiso escrito y se puede descargar como archivo.",
    "plata: limpio, con reglas de limpieza escritas y calidad revisada.",
    "oro: listo para una decisión y un público con nombre.",
)
M1_LEVEL_BLOCK = "\n".join(M1_LEVEL_LINES)
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
    section = doc.sections[0]
    header = section.header
    p = header.paragraphs[0]
    p.text = ""
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    if LOGO.is_file():
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


def _qa_table(
    doc: Document,
    questions: list[tuple[str, str]],
    answers: list[str] | None = None,
) -> None:
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
        if ex and answers is None:
            _example_in_cell(c0, ex)
        c1 = table.rows[i].cells[1]
        c1.text = ""
        if answers is not None:
            ans = answers[i - 1]
            c1.paragraphs[0].add_run(ans)
            for run in c1.paragraphs[0].runs:
                run.font.size = Pt(9)
        else:
            for para in c1.paragraphs:
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


def _closing_drive_box(doc: Document) -> None:
    table = doc.add_table(rows=1, cols=1)
    table.style = "Table Grid"
    cell = table.rows[0].cells[0]
    cell.text = ""
    p = cell.paragraphs[0]
    run = p.add_run("Guarden todo en la carpeta de su equipo en Drive antes de las 15:30.")
    run.bold = True
    run.font.size = Pt(9)


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
Arme un resumen de una página con: territorio, comunidad, problema, solución, canales, ingresos, actividades clave, aliados, costos principales e impacto territorial. No invente cifras ni nombres de personas. No agregue grupos de personas ni datos que el equipo no escribió."""

AI_P1 = """Lea el documento. Solo respuestas del equipo; marque desconocido; no invente números; español de Colombia.
Tabla de tres columnas: Área | Nivel | Qué tienen (máx. 8 palabras). Nueve filas con estos nombres fijos: Socios clave, Actividades clave, Recursos clave, Propuestas de valor, Relaciones con clientes, Canales, Segmentos de clientes, Estructura de costos, Flujos de ingreso. Nivel con cuadrado 🟥 caliente, 🟧 tibio o 🟦 frío y leyenda breve. Sin marcas X. «Qué falta» (máx. 5) y 1–2 fuentes para la Parte 2."""

AI_P2 = """Lea el documento subido. Solo respuestas del equipo; marque desconocido; no invente números; español de Colombia.
Escriba las cuatro definiciones, cada una en su línea: ninguno: el dato está solo en chats o en la memoria, sin permiso o sin poder descargarlo. Empezar aquí es normal. bronce: guardado en un lugar con responsable, con permiso escrito y se puede descargar como archivo. plata: limpio, con reglas de limpieza escritas y calidad revisada. oro: listo para una decisión y un público con nombre. Son niveles de confianza, no premios. Luego tres líneas separadas: Nivel sugerido: / Lo que falta para subir: / Un paso concreto para esta tarde:"""

AI_P3 = """Lea el documento subido. Solo respuestas del equipo; marque desconocido; no invente números; español de Colombia.
Boceto de tablero en bloque de código (máx. 60 caracteres de ancho) con tres bloques: «Cómo está hoy», «Qué cambia con ustedes», «Contexto de datos abiertos». Cada número es firme solo si sus datos están en plata u oro; si no, estimado. Incluya rol, decisión de la semana y 2–3 números con fuente. Si los derechos de datos no están claros, escriba «no publicar». Sin citas ni marcas como [cite]."""

AI_P4 = """Lea el documento subido. Solo respuestas del equipo; marque desconocido; no invente números; español de Colombia.
Guion de 600–700 palabras (~5 min en voz alta), cinco secciones con minutos aproximados: problema; datos que usamos; la pantalla; beneficio; próximos pasos. Párrafos cortos. Marque cifras sin fuente como [sin fuente]. Si en próximos pasos escribieron «no sé», proponga 2 opciones etiquetadas «sugerencia, validar con su mentor»."""


PROMPTS_META = [
    (
        "Parte 0. Su proyecto en una página",
        "Resumen de una página en sus palabras.",
        "Texto continuo de una página.",
    ),
    (
        "Parte 1. ¿Qué información tienen y dónde está?",
        "Mapa de calor por área del negocio y lista «qué falta».",
        "Tabla Área | Nivel | Qué tienen; viñetas «Qué falta» y fuentes para la Parte 2.",
    ),
    (
        "Parte 2. ¿Cómo nace un dato y qué tan confiable es?",
        "Cuatro niveles de confianza y lectura del dato principal del equipo.",
        "Cuatro definiciones, luego Nivel sugerido / Lo que falta / Un paso concreto.",
    ),
    (
        "Parte 3. ¿Qué decisión ayudan a tomar?",
        "Boceto de tablero de una pantalla (rol, decisión, números con firme/estimado).",
        "Boceto en bloque de código (máx. 60 caracteres de ancho).",
    ),
    (
        "Parte 4. Su pitch de 5 minutos",
        "Guion de pitch de cinco minutos (600–700 palabras).",
        "Cinco secciones con encabezados y minutos aproximados.",
    ),
]


def build_docx(*, filled_air4u: bool = False, out_path: Path | None = None) -> Document:
    global _table_counter, AI_TABLE_IDS
    _table_counter = 0
    AI_TABLE_IDS.clear()

    doc = Document()
    _set_doc_defaults(doc)
    _header_logo(doc)
    _footer_inspira(doc)

    doc.add_heading("Cuestionario del Datatón — su equipo", level=1)
    if filled_air4u:
        banner = doc.add_paragraph()
        banner.alignment = WD_ALIGN_PARAGRAPH.CENTER
        br = banner.add_run(EJEMPLO_HEADER)
        br.bold = True
        br.font.color.rgb = NAVY
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
    _para(
        doc,
        "Las instrucciones para la inteligencia artificial funcionan en ChatGPT, Gemini o Grok (cuentas estándar).",
    )
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
    if filled_air4u:
        _qa_table(
            doc,
            q0,
            [
                "Bogotá — una clínica piloto (sin nombre propio del sitio).",
                "Gestor de instalaciones y personal de una clínica piloto.",
                "No saben con certeza si el PM₂.₅ en interior es seguro esta semana.",
                "Sensores en sitio y monitoreo del aire interior (piloto Air4U).",
                "Instalación en el sitio piloto de la clínica.",
                "no sé",
                "Revisar lecturas del sensor y responder alertas.",
                "Proveedor del sensor y personal de mantenimiento de la clínica.",
                "Exportar historial y permisos del piloto aún sin cerrar.",
                "Menos tiempo con aire interior poco saludable en espacios de salud.",
            ],
        )
    else:
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
    if filled_air4u:
        _qa_table(
            doc,
            q1_types,
            [
                "Lecturas del sensor de partículas (PM₂.₅) en la clínica — sin cifra exportable.",
                "Mensajes de WhatsApp con mantenimiento cuando hay intervención.",
                "Correos o acuerdos con el administrador del sitio piloto.",
                "no sé",
                "no sé",
            ],
        )
    else:
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
    if filled_air4u:
        _qa_table(
            doc,
            q1_detail,
            [
                "Plataforma del proveedor del sensor; copias en WhatsApp.",
                "no sé",
                "no sé",
                "Gestor de instalaciones del sitio piloto.",
                "Todavía no hay exportación simple almacenada.",
                "Permiso del sitio piloto en trámite.",
            ],
        )
    else:
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
    if filled_air4u:
        _qa_table(
            doc,
            q2,
            [
                "Lecturas del sensor en la clínica piloto.",
                "El sensor mide y la plataforma registra la lectura.",
                "Medición → guardado en plataforma → aviso al gestor si hay alerta.",
                "Sensor automático; gestor revisa y avisa a mantenimiento.",
                "Sensor en sitio y aplicación del proveedor.",
                "Comentarios en WhatsApp cuando hubo intervención.",
                "A veces comparan con lecturas manuales; sin rutina fija.",
                "Un solo lugar con historial y exportación clara.",
            ],
        )
    else:
        _qa_table(doc, q2)
    _para(
        doc,
        "Niveles de confianza del dato (no son premios). Use la misma redacción al leer su flujo:",
        bold=True,
    )
    for line in M1_LEVEL_LINES:
        doc.add_paragraph(f"• {line}", style="Normal")
    _para(doc, "Empezar en nivel ninguno es normal.", bold=True)
    _para(
        doc,
        "Si no tienen datos propios: usen datos abiertos o el ejemplo del Datatón y márchenlos como «estimado».",
    )
    _para(doc, "Marque sí / no / no sé:", bold=True)
    q2_chk = [
        ("¿Cada registro tiene fecha?", "A veces en la plataforma, no siempre en WhatsApp."),
        ("¿Saben de dónde viene cada dato?", "Sí para el sensor; no siempre para los mensajes."),
        ("¿Lo guardan en un solo lugar?", "No — están repartidos."),
        ("¿Tienen reglas escritas para corregir errores?", "no sé"),
        ("¿Otra persona puede revisar los datos?", "El técnico de mantenimiento mira capturas."),
    ]
    if filled_air4u:
        _qa_table(
            doc,
            q2_chk,
            [
                "A veces en la plataforma; no siempre en WhatsApp.",
                "Sí para el sensor; no siempre para los mensajes.",
                "No — están repartidos.",
                "no sé",
                "El técnico de mantenimiento revisa capturas.",
            ],
        )
    else:
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
    _para(
        doc,
        "Un número es firme solo cuando sus datos están en nivel plata u oro; en ninguno o bronce márchenlo como estimado.",
        bold=True,
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
    if filled_air4u:
        _qa_table(
            doc,
            q3,
            [
                "Gestor de instalaciones / sitio en la clínica piloto (Bogotá).",
                "¿Debe activar ventilación extra o revisión de filtros esta semana porque el PM₂.₅ en interior podría superar la referencia OMS?",
                "¿El PM₂.₅ en interior supera la referencia OMS?",
                "no sé",
                "no sé",
                "sin dato (estimado; lecturas no exportadas).",
                "Referencia OMS: 5 µg/m³ (media anual PM₂.₅).",
                "no sé",
                "Sin monitoreo continuo visible para el gestor antes del piloto.",
                "Menos tiempo con aire interior poco saludable; protege pacientes y personal.",
                "Calidad del aire exterior en Bogotá — fuente pública por definir.",
            ],
        )
    else:
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
    if filled_air4u:
        _qa_table(
            doc,
            q4,
            [
                "Personal y pacientes con aire interior incierto en la clínica piloto.",
                "Lecturas del sensor (sin cifra exportada) y referencia OMS 5 µg/m³.",
                "Decisión de ventilación/filtros y tres paneles sin brecha calculable.",
                "Clínica piloto y quienes trabajan en el sitio.",
                "no sé",
            ],
        )
    else:
        _qa_table(doc, q4)
    _ai_table(doc, AI_P4)
    _closing_drive_box(doc)

    target = out_path or (OUT_EJEMPLO_DOCX if filled_air4u else OUT_DOCX)
    doc.save(target)
    return doc


def convert_pdf(docx_path: Path, pdf_path: Path) -> None:
    subprocess.run(
        [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(docx_path.parent),
            str(docx_path),
        ],
        check=True,
        capture_output=True,
    )
    produced = docx_path.with_suffix(".pdf")
    if produced != pdf_path and produced.is_file():
        produced.replace(pdf_path)
    if not pdf_path.is_file():
        raise SystemExit(f"LibreOffice did not produce PDF: {pdf_path}")


def extract_ai_instruction_bodies(docx_path: Path) -> list[str]:
    """Return AI bodies for Partes 0–4 in order."""
    from docx import Document as D

    doc = D(docx_path)
    bodies: list[str] = []
    for table in doc.tables:
        cell = table.rows[0].cells[0]
        if not cell.text.strip().startswith(AI_MARKER):
            continue
        lines: list[str] = []
        past_marker = False
        for para in cell.paragraphs:
            if AI_MARKER in para.text:
                past_marker = True
                continue
            if past_marker:
                lines.append(para.text)
        bodies.append("\n".join(lines))
    if len(bodies) < 5:
        raise SystemExit(f"Expected 5 AI boxes, found {len(bodies)} in {docx_path}")
    return bodies[:5]


def write_prompts_txt(docx_path: Path, dest: Path = PROMPTS_TXT) -> None:
    bodies = extract_ai_instruction_bodies(docx_path)
    chunks: list[str] = []
    for meta, body in zip(PROMPTS_META, bodies, strict=True):
        chunks.extend(
            [
                f"Parte: {meta[0]}",
                f"Salida esperada: {meta[1]}",
                f"Forma esperada: {meta[2]}",
                "",
                body,
                "",
            ]
        )
    text = "\n".join(chunks).rstrip() + "\n"
    dest.write_text(text, encoding="utf-8")


def parse_prompts_instruction_blocks(raw: str) -> list[str]:
    """Extract the five instruction bodies from prompts.txt (after header triplets)."""
    chunks = re.split(r"(?=^Parte: )", raw.strip(), flags=re.MULTILINE)
    bodies: list[str] = []
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk.startswith("Parte:"):
            continue
        lines = chunk.split("\n")
        try:
            blank = lines.index("")
        except ValueError:
            raise SystemExit("prompts.txt: missing blank line after headers") from None
        bodies.append("\n".join(lines[blank + 1 :]).rstrip("\n"))
    return bodies


def verify_prompts_txt(docx_path: Path, prompts_path: Path = PROMPTS_TXT) -> None:
    from_docx = extract_ai_instruction_bodies(docx_path)
    raw = prompts_path.read_text(encoding="utf-8")
    instruction_blocks = parse_prompts_instruction_blocks(raw)
    if instruction_blocks != from_docx:
        raise SystemExit("prompts.txt instruction blocks do not match blank docx byte-for-byte")
    print("prompts_txt_verify", "OK", len(instruction_blocks), "blocks")


def audit_air4u_numbers(docx_path: Path) -> None:
    from docx import Document as D

    doc = D(docx_path)
    text_parts: list[str] = []
    for table in doc.tables:
        if table.rows[0].cells[0].text.strip().startswith(AI_MARKER):
            continue
        if "Reglas para ustedes" in table.rows[0].cells[0].text:
            continue
        if len(table.rows) > 0 and table.rows[0].cells[0].text == "Pregunta":
            for row in table.rows[1:]:
                if len(row.cells) > 1:
                    text_parts.append(row.cells[1].text)
    text = "\n".join(text_parts).replace("Air4U", "AirU").replace("PM₂.₅", "PM")
    for m in re.finditer(r"(?<![A-Za-z])\d+(?:[.,]\d+)?", text):
        snippet = text[max(0, m.start() - 20) : m.end() + 15]
        if m.group(0) == "5" and ("µg" in snippet or "OMS" in snippet):
            continue
        if m.group(0) in {"24", "2026", "21", "11", "14"}:
            continue  # dates in footer not in answers
        raise SystemExit(f"Invented number in Air4U ejemplo answers: {m.group(0)!r} near {snippet!r}")
    print("air4u_number_audit", "OK")


def grep_free_docx(path: Path) -> list[str]:
    from docx import Document as D

    text = "\n".join(p.text for p in D(path).paragraphs)
    for table in D(path).tables:
        for row in table.rows:
            for cell in row.cells:
                text += "\n" + cell.text
    return [m.group(0) for m in FREE_RE.finditer(text)]


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
    jargon += [m.group(0) for m in TEAM_BAN_RE.finditer(text)]
    free = [m.group(0) for m in FREE_RE.finditer(text)]
    return jargon, free


def _docx_full_text(path: Path) -> str:
    from docx import Document as D

    doc = D(path)
    parts = [p.text for p in doc.paragraphs]
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                parts.append(cell.text)
    return "\n".join(parts)


def _ai_instruction_text(docx_path: Path) -> str:
    from docx import Document as D

    chunks: list[str] = []
    for table in D(docx_path).tables:
        cell = table.rows[0].cells[0]
        if cell.text.strip().startswith(AI_MARKER):
            chunks.append(cell.text)
    return "\n".join(chunks)


def grep_team_facing_bans() -> dict[str, list[str]]:
    """Grep blank/ejemplo docx and prompts.txt for mentor-only codes (expect 0 in team files)."""
    hits: dict[str, list[str]] = {}
    prompts = PROMPTS_TXT.read_text(encoding="utf-8") if PROMPTS_TXT.is_file() else ""
    prompts_instr = (
        "\n\n".join(parse_prompts_instruction_blocks(prompts)) if prompts.strip() else ""
    )
    for label, blob in (
        ("blank_docx_readable", docx_readable_text(OUT_DOCX)),
        ("ejemplo_docx_readable", docx_readable_text(OUT_EJEMPLO_DOCX)),
        ("prompts_txt", prompts),
    ):
        hits[label] = sorted({m.group(0) for m in TEAM_BAN_RE.finditer(blob)})
    for label, blob in (
        ("blank_docx_ai", _ai_instruction_text(OUT_DOCX)),
        ("ejemplo_docx_ai", _ai_instruction_text(OUT_EJEMPLO_DOCX)),
        ("prompts_txt_instructions", prompts_instr),
    ):
        found = sorted({m.group(0) for m in TEAM_BAN_RE.finditer(blob)})
        if "Funciona en ChatGPT" in blob:
            found.append("Funciona en ChatGPT")
        if re.search(r"(?i)\blínea base\b", blob):
            found.append("Línea base")
        hits[label] = found
    return hits


def word_count_per_instruction(docx_path: Path) -> list[tuple[str, int]]:
    bodies = extract_ai_instruction_bodies(docx_path)
    labels = [meta[0] for meta in PROMPTS_META]
    return [(labels[i], len(re.findall(r"\S+", bodies[i]))) for i in range(5)]


def main() -> int:
    render_example_images()
    build_docx(filled_air4u=False)
    convert_pdf(OUT_DOCX, OUT_PDF)
    write_prompts_txt(OUT_DOCX)
    verify_prompts_txt(OUT_DOCX)
    build_docx(filled_air4u=True, out_path=OUT_EJEMPLO_DOCX)
    convert_pdf(OUT_EJEMPLO_DOCX, OUT_EJEMPLO_PDF)
    audit_air4u_numbers(OUT_EJEMPLO_DOCX)
    jargon, free = grep_self_check()
    free_ej = grep_free_docx(OUT_EJEMPLO_DOCX)
    print("grep_jargon_hits", len(jargon), jargon[:20])
    print("grep_free_hits", len(free), free)
    print("grep_free_ejemplo_hits", len(free_ej), free_ej)
    ban_hits = grep_team_facing_bans()
    for label, found in ban_hits.items():
        print("grep_team_ban", label, len(found), found)
    wc = word_count_per_instruction(OUT_DOCX)
    for parte, n in wc:
        print("instruction_word_count", parte, n)
    if jargon or free or free_ej or any(ban_hits.values()):
        print("SELF-CHECK FAILED", file=sys.stderr)
        return 1
    full = _docx_full_text(OUT_DOCX)
    if not all(line in full for line in M1_LEVEL_LINES):
        print("SELF-CHECK FAILED: M1 wording missing in blank docx", file=sys.stderr)
        return 1
    ai2 = extract_ai_instruction_bodies(OUT_DOCX)[2]
    if not all(line in ai2 for line in M1_LEVEL_LINES):
        print("SELF-CHECK FAILED: M1 wording missing in Parte 2 AI instruction", file=sys.stderr)
        return 1
    import fitz

    for label, pdf in (("blank", OUT_PDF), ("air4u", OUT_EJEMPLO_PDF)):
        doc = fitz.open(pdf)
        n = doc.page_count
        doc.close()
        print(f"pdf_pages_{label}", n)
        if n > 8:
            print(f"WARNING: {label} PDF exceeds 8 pages", file=sys.stderr)
            return 1
    print("docx", OUT_DOCX)
    print("pdf", OUT_PDF)
    print("ejemplo_docx", OUT_EJEMPLO_DOCX)
    print("ejemplo_pdf", OUT_EJEMPLO_PDF)
    print("prompts_txt", PROMPTS_TXT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())