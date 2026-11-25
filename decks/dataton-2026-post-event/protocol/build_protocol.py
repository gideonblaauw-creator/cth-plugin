#!/usr/bin/env python3
"""Build Protocolo Datatón CTH docx, PDF, Monday CSV, and PNG page renders."""

from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROTO = Path(__file__).resolve().parent
MONO = ROOT / "monday"
RENDER = ROOT / "render"
FONTS = (
    Path(__file__).resolve().parents[2]
    / "observatorio-tierra-dataton"
    / "assets"
    / "fonts"
)

PHASES = [
    {
        "id": "t8",
        "group": "T-8 semanas",
        "rel": "T-8",
        "title": "Concepto y aliados",
        "role": "Coordinación CTH + Coordinación académica (Externado)",
        "objective": "Definir el propósito del Datatón, el Observatorio de la Tierra como marco temático, y el mapa de aliados (academia, sector productivo, agencia).",
        "deliverables": "Brief de concepto; lista de aliados objetivo; criterios de premio (p. ej. sandbox Datalab 2027); borrador de narrativa para convocatoria.",
        "checklist": [
            "Acordar título público y co-branding CleantechHUB–Universidad Externado.",
            "Confirmar premio simbólico/operativo (entrada sandbox Datalab 2027) y alcance de certificados.",
            "Identificar conversatorios y casos de demostración (p. ej. Air4U) [por validar repetición edición 2].",
            "Definir capacidad objetivo (150 en persona; livestream prometido en invitación calendario nov 2026).",
            "Alinear expectativa de equipos (14 núcleo Externado CEE; briefing mencionó hasta 20 equipos startup).",
        ],
        "risks": [
            "Premio o narrativa poco clara → baja convocatoria.",
            "Aliados confirmados tarde → panel o sandbox sin sustituto.",
        ],
    },
    {
        "id": "t6",
        "group": "T-6 semanas",
        "rel": "T-6",
        "title": "Sede y agenda",
        "role": "Logística/eventos + Coordinación académica",
        "objective": "Bloquear sede, horario 08:00–17:00, y agenda v publicable con roles y tiempos.",
        "deliverables": "Agenda versionada (v4/v7); reserva Auditorio Bloque I piso 2; bloqueo en calendarios internos.",
        "checklist": [
            "Reservar Universidad Externado, Auditorio del Bloque I, piso 2.",
            "Publicar agenda con apertura 08:30, panel 08:40, Observatorio, conversatorios, bloques de trabajo y finales.",
            "Documentar asientos panel (APC, RAP Pacífico, rector o respaldo académico) y moderador CTH.",
            "Reconciliar nombres en agenda (p. ej. Cortés vs Henao Constructora Bolívar) antes de imprimir.",
            "Planear aula modular Bloque I para trabajo con mentores (~11:00).",
        ],
        "risks": [
            "Deriva de nombres entre versiones de agenda (lección 24 nov).",
            "Rector u orador ancla sin confirmar hasta T-1.",
        ],
    },
    {
        "id": "t4",
        "group": "T-4 semanas",
        "rel": "T-4",
        "title": "Luma y convocatoria",
        "role": "Comunicaciones + Coordinación CTH",
        "objective": "Abrir registro Luma, difundir convocatoria y enlazar descripción con YouTube en vivo.",
        "deliverables": "Evento Luma publicado; textos de confirmación; piezas para redes y lista Externado.",
        "checklist": [
            "Publicar evento Luma (enlace gestión en fuentes pre-evento nov 2026).",
            "Incluir en descripción capacidad 150 y promesa de transmisión.",
            "Solicitar listado completo equipos Externado con nombres (compromiso logística — no encontrado pre 24 nov).",
            "Monitorear conteos «going» vía avisos Luma (último dato antes del día: 111 going, 3 not going, 08:26 24 nov).",
            "Coordinar cancelaciones de última hora en la mañana del evento.",
        ],
        "risks": [
            "Sin export Luma/check-in instalado → asistencia real desconocida.",
            "Listado equipos incompleto → carpetas Drive desalineadas con personas.",
        ],
    },
    {
        "id": "t3",
        "group": "T-3 semanas",
        "rel": "T-3",
        "title": "Reclutamiento y briefing de mentores",
        "role": "Coordinación académica + Profesor coordinador mentores",
        "objective": "Reclutar monitores de ciencias de datos, briefing y cobertura de paneles matutinos.",
        "deliverables": "Lista de mentores; sesión briefing (p. ej. 23 nov 16:00); fotos para apertura.",
        "checklist": [
            "Convocar estudiantes mentores Externado (meta ~5 según logística; briefing Read.ai mencionó cuatro).",
            "Briefing: filtro a finalistas, expectativa hasta 20 equipos, paneles 08:40 en adelante.",
            "Confirmar asistencia de cada mentor (Tomás citado en seguimiento — por validar mismo Tomás Calle Luma).",
            "Recoger foto de perfil por mentor para deck de apertura (acción Angélica CTH).",
            "Incluir al profesor/coordinador en jurado planificado si aplica.",
        ],
        "risks": [
            "Mentor ausente el día D → equipos sin acompañamiento en preselección.",
            "Confusión de nombres/handles en listas Granola.",
        ],
    },
    {
        "id": "t2",
        "group": "T-2 semanas",
        "rel": "T-2",
        "title": "Paquete de equipos",
        "role": "Coordinación CTH (contenidos) + Hands/archivo",
        "objective": "Entregar cuestionario, guía técnica, prompts IA, plantilla de pitch y ejemplo de referencia.",
        "deliverables": "Starter pack en repo/Drive; cuestionario; guía; prompts; plantilla pitch.",
        "checklist": [
            "Subir paquete base a carpeta raíz Drive del Datatón.",
            "Incluir cuestionario Datatón 24 nov, guía técnica, prompts IA, hojas BMC/mapa de calor.",
            "Publicar plantilla pitch 3 minutos CleantechHUB.",
            "Incluir ejemplo Air4U como referencia de entregable.",
            "Pre-crear carpetas Equipos 01–14 antes del día D.",
        ],
        "risks": [
            "Equipos nuevos el mismo día → carpeta y número fuera de secuencia (7 creados 24 nov).",
            "Nombres de carpeta truncados (Equipo 14 «Ki Natural Scienc»).",
        ],
    },
    {
        "id": "t1",
        "group": "T-1 semana",
        "rel": "T-1",
        "title": "Drive, WhatsApp, run-of-show, certificados",
        "role": "Operaciones evento + Soporte técnico",
        "objective": "Dejar carpetas, grupos, cronograma minuto a minuto y certificados listos para imprimir o entregar.",
        "deliverables": "Run-of-show; grupos WhatsApp participantes y MentorXs; diseño certificados; decisión streaming.",
        "checklist": [
            "Verificar permisos Drive en todas las carpetas de equipo.",
            "Crear o validar grupos WhatsApp (participantes y mentores) — medios del evento aún no centralizados.",
            "Resolver límite StreamYard/Zoom (40 min plan gratuito) o licencia [pendiente Gideon].",
            "Confirmar conteo almuerzos con sede (0 a la carta reportado 23 nov — por validar día D).",
            "Enviar panel one-pager 08:40 a panelistas confirmados (Natalia APC, Viviana RAP, asiento académico).",
            "Preparar plantillas certificado equipos y mentores (no público general).",
            "Coordinar fotógrafo para certificados y anuncio ganadores [sin álbum encontrado post 24 nov].",
            "Imprimir o preparar badges (propuesta 100: startup, corporativo, CTH, CEE, staff, invitado).",
        ],
        "risks": [
            "Streaming cortado a los 40 minutos.",
            "Fotografía del evento solo en teléfonos/WhatsApp.",
            "Cambios de panelistas de última hora.",
        ],
    },
    {
        "id": "d0",
        "group": "Día D",
        "rel": "Día D",
        "title": "Ejecución — run-of-show",
        "role": "Director de escena CTH + Coordinación CTH/Externado",
        "objective": "Ejecutar el 24 nov 2026 08:00–17:00: registro, paneles, lanzamiento Observatorio, sandbox, bloques, preselección, 6 finalistas, jurado y cierre.",
        "deliverables": "Evento realizado; entregables en Drive; acta de jurado [no encontrada en fuentes]; transmisión.",
        "checklist": [
            "08:30 — Apertura (Gideon Blaauw y Marlene Díaz planificados; rector alternativa por validar).",
            "08:40 — Panel tierra/agenda con Natalia Vargas (APC), Viviana Obando (RAP Pacífico), moderador CTH.",
            "09:10–09:40 — Presentación Observatorio (Gideon + Alejandro Díaz Externado) y conversatorio Constructora Bolívar (Alejandro Henao planificado; asistencia por validar).",
            "09:45 — Conversatorio Agrometers (Enrique Medina).",
            "10:05–10:40 — Data Sandbox Air4U (Miguel Ángel Rozo, Sebastián Forero).",
            "11:00 en adelante — Trabajo en bloques con mentores en aula modular.",
            "Crear carpetas adicionales si llegan equipos (7 carpetas nuevas 24 nov; total 21 carpetas, sin Equipo 17).",
            "Monitores apoyan preselección hacia 6 finalistas antes de 16:00 (planificado).",
            "Jurado planificado: Enrique Medina, Alejandro Díaz, Gideon Blaauw; utilidad y honestidad 0–5; desempate por historia.",
            "Ocho equipos subieron pitch ~16:00–16:42 — no equivale a lista oficial de 6 finalistas [por validar].",
            "Cierre, certificados y anuncio de tres ganadores [resultados no encontrados en fuentes].",
            "Toma de asistencia en entrada y sala tarde (planeada; resultado no documentado).",
        ],
        "risks": [
            "Sin acta de jurado ni correo de resultados post-evento.",
            "Rosters de equipo no consolidados pese a 21 carpetas.",
            "Sin check-ins Luma disponibles.",
        ],
    },
    {
        "id": "tp1",
        "group": "T+1",
        "rel": "T+1",
        "title": "Agradecimientos, biblioteca de imágenes, informe",
        "role": "Comunicaciones + Coordinación CTH",
        "objective": "Cerrar el ciclo inmediato: agradecer a participantes, centralizar fotos y redactar informe post-evento.",
        "deliverables": "Plantillas thank-you; carpeta biblioteca de imágenes; borrador informe lecciones.",
        "checklist": [
            "Enviar agradecimientos a equipos, monitores y equipo de apoyo (plantillas en thank-yous/).",
            "Agradecimientos personalizados a panelistas, jurado y aliados (roles del día según agenda v7).",
            "Recopilar fotos (fotógrafo, WhatsApp, teléfonos) — en Drive solo poster equipo Kuo, no álbum evento.",
            "Publicar o archivar transmisión YouTube [por validar].",
            "Redactar informe con asistencia, finalistas, ganadores y puntajes — datos faltantes marcar [por validar].",
            "Actualizar protocolo con lecciones del 24 nov.",
        ],
        "risks": [
            "Retraso en fotos → comunicación post-evento sin visuales.",
            "Sin ganadores confirmados → mensajes con placeholder {resultado/ganadores}.",
        ],
    },
    {
        "id": "tp2",
        "group": "T+2 semanas",
        "rel": "T+2",
        "title": "Seguimiento",
        "role": "Coordinación CTH + Datalab desk",
        "objective": "Convertir equipos y aliados en pipeline Datalab 2027 y seguimiento académico Externado.",
        "deliverables": "Plan de seguimiento por equipo; compromisos sandbox; retrospectiva con sede.",
        "checklist": [
            "Priorizar equipos con entregables completos en Drive para invitación sandbox.",
            "Reunión retrospectiva CTH–Externado (Marlene / Alejandro).",
            "Incorporar lecciones en segunda edición (listas Luma, jurado, fotografía, streaming).",
            "Cerrar ítems Monday importados como Hecho o documentar bloqueos.",
            "[pendiente Gideon] — definir ganadores oficiales y comunicación pública.",
        ],
        "risks": [
            "Oportunidad Datalab sin dueño claro por falta de resultados oficiales.",
        ],
    },
]

LESSONS = [
    "[pendiente Gideon] — Resumen ejecutivo cualitativo del día (qué funcionó / qué no).",
    "[pendiente Gideon] — Lista oficial de seis finalistas y tres ganadores con puntajes.",
    "[pendiente Gideon] — Asistencia en sala y check-ins Luma.",
    "Drive mostró 21 carpetas de equipo (14 pre-armadas + 7 creadas el 24 nov); no hay carpeta Equipo 17.",
    "Rosters de miembros no consolidados; listado completo prometido por Externado no hallado en Gmail.",
    "Sin registro de check-ins ni export Luma en conectores disponibles.",
    "Sin álbum de fotógrafo en Drive; solo assets de equipo (p. ej. poster Kuo).",
    "Cambios de última hora en panelistas y nombres en agenda (APC, Constructora Bolívar, Apix fuera del one-pager 08:40).",
    "Ocho pitches subidos ~16:00; no reemplazan acta de finalistas.",
    "Problemas pre-evento documentados: límite StreamYard/Zoom, almuerzos, mentor Tomás ausente en briefing.",
]

ANNEX = [
    ("Paquete equipos (starter pack)", "decks/dataton-2026-team-pack"),
    ("Plantilla pitch Datatón", "decks/datathon-2026-pitch-template"),
    ("Guía panel 08:40", "decks/dataton-2026-panel-guide"),
    ("Preguntas por espacio / conversatorios", "decks/dataton-2026-preguntas-espacios"),
    ("Plantilla certificado", "decks/dataton-2026-certificate"),
    ("Deck Observatorio (contexto)", "decks/observatorio-tierra-dataton"),
]


def build_monday_csv() -> None:
    MONO.mkdir(parents=True, exist_ok=True)
    path = MONO / "board-import.csv"
    rows = []
    for ph in PHASES:
        for item in ph["checklist"]:
            rows.append(
                {
                    "Tarea": item,
                    "Fase": ph["group"],
                    "Responsable (rol)": ph["role"],
                    "Fecha relativa (T-x)": ph["rel"],
                    "Fecha": "",
                    "Estado": "Por hacer",
                    "Entregable/link": ph["deliverables"].split(";")[0].strip()[:120],
                    "Dependencia": "",
                    "Notas": "; ".join(ph["risks"][:1]) if ph["risks"] else "",
                }
            )
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def html_body() -> str:
    css_font = ""
    if (FONTS / "open-sans-latin-400-normal.woff2").exists():
        css_font = f"""
@font-face {{
  font-family: 'Open Sans';
  src: url('file://{FONTS}/open-sans-latin-400-normal.woff2') format('woff2');
  font-weight: 400;
}}
@font-face {{
  font-family: 'Open Sans';
  src: url('file://{FONTS}/open-sans-latin-600-normal.woff2') format('woff2');
  font-weight: 600;
}}
@font-face {{
  font-family: 'Open Sans';
  src: url('file://{FONTS}/open-sans-latin-700-normal.woff2') format('woff2');
  font-weight: 700;
}}
"""
    parts = [
        f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<title>Protocolo Datatón CTH</title>
<style>
{css_font}
:root {{
  --cth-primary: #2D6A4F;
  --cth-dark: #1B4332;
  --cth-accent: #95D5B2;
  --cth-light: #D8F3DC;
  --cth-text: #333333;
}}
* {{ box-sizing: border-box; }}
body {{
  font-family: 'Open Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-size: 11pt;
  line-height: 1.45;
  color: var(--cth-text);
  margin: 0;
  padding: 0;
}}
@page {{
  size: A4;
  margin: 22mm 18mm 24mm 18mm;
}}
@media print {{
  body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  .page-break {{ page-break-before: always; }}
  .running-header, .running-footer {{
    position: fixed;
    left: 0; right: 0;
    font-size: 9pt;
    color: var(--cth-dark);
  }}
  .running-header {{
    top: 0;
    border-bottom: 2px solid var(--cth-primary);
    padding: 6mm 18mm 3mm;
    display: flex;
    justify-content: space-between;
    font-weight: 600;
  }}
  .running-footer {{
    bottom: 0;
    border-top: 1px solid var(--cth-accent);
    padding: 3mm 18mm;
    display: flex;
    justify-content: space-between;
  }}
}}
.cover {{
  min-height: 250mm;
  padding: 40mm 18mm;
  background: linear-gradient(160deg, var(--cth-light) 0%, #fff 55%);
}}
.cover h1 {{
  color: var(--cth-primary);
  font-size: 26pt;
  margin-bottom: 0.2em;
}}
.cover .sub {{
  color: var(--cth-dark);
  font-size: 14pt;
  font-weight: 600;
}}
.cover .meta {{
  margin-top: 2em;
  font-size: 10pt;
}}
h2.phase {{
  color: var(--cth-primary);
  font-size: 14pt;
  border-left: 4px solid var(--cth-accent);
  padding-left: 8px;
  margin-top: 1.2em;
}}
h3 {{ font-size: 11pt; color: var(--cth-dark); margin-bottom: 0.3em; }}
ul {{ margin: 0.3em 0 0.8em 1.2em; }}
li {{ margin-bottom: 0.25em; }}
.risk {{ color: #6b2c2c; }}
.meta-block {{ background: var(--cth-light); padding: 8px 12px; margin: 8px 0; border-radius: 4px; }}
</style>
</head>
<body>
<div class="running-header"><span>CleantechHUB</span><span>Protocolo Datatón CTH — interno</span></div>
<div class="running-footer"><span>© 2026 CleantechHUB Foundation</span><span>Documento de trabajo</span></div>
<section class="cover page-break">
  <p class="sub">CleantechHUB · Documento interno</p>
  <h1>Protocolo Datatón CTH</h1>
  <p class="sub">Edición referencia: Datatón Observatorio de la Tierra · 24 nov 2026</p>
  <p class="meta">Universidad Externado de Colombia · Co-organización CEE / CleantechHUB<br/>
  Uso exclusivo equipo CTH. No distribuir sin aprobación.</p>
  <div class="meta-block">
    <strong>Alcance:</strong> línea de tiempo T-8 a T+2, roles operativos (sin nombres en responsabilidades),
    checklists, riesgos y anexos de plantillas en repo.
  </div>
</section>
<section class="page-break">
  <h2 class="phase">Introducción</h2>
  <p>Este protocolo captura el ciclo operativo del Datatón CleantechHUB en co-branding con Universidad Externado,
  a partir de la primera edición del 24 de noviembre de 2026 (08:00–17:00, Auditorio Bloque I). Integra el plan
  pre-evento y las evidencias post-evento disponibles al 25 nov 2026. Donde las fuentes no confirman un dato,
  se marca <strong>[por validar]</strong> o <strong>[pendiente Gideon]</strong>.</p>
  <p><strong>Premio planificado:</strong> entrada al sandbox Datalab CleantechHUB 2027 y conexiones de mercado;
  certificados para equipos y mentores. <strong>Jurado planificado:</strong> utilidad e honestidad (0–5); desempate
  por historia si empatan ambos criterios.</p>
</section>
"""
    ]
    for ph in PHASES:
        parts.append(f'<section class="page-break">\n')
        parts.append(
            f'<h2 class="phase">{ph["rel"]} — {ph["title"]}</h2>\n'
        )
        parts.append(
            f'<div class="meta-block"><strong>Responsable (rol):</strong> {ph["role"]}</div>\n'
        )
        parts.append(f"<h3>Objetivo</h3><p>{ph['objective']}</p>\n")
        parts.append(f"<h3>Entregables</h3><p>{ph['deliverables']}</p>\n")
        parts.append("<h3>Checklist</h3><ul>\n")
        for c in ph["checklist"]:
            parts.append(f"<li>{c}</li>\n")
        parts.append("</ul>\n")
        parts.append("<h3>Riesgos</h3><ul class=\"risk\">\n")
        for r in ph["risks"]:
            parts.append(f"<li>{r}</li>\n")
        parts.append("</ul>\n</section>\n")

    parts.append('<section class="page-break">\n')
    parts.append('<h2 class="phase">Lecciones del 24 nov 2026</h2><ul>\n')
    for le in LESSONS:
        parts.append(f"<li>{le}</li>\n")
    parts.append("</ul>\n</section>\n")

    parts.append('<section class="page-break">\n')
    parts.append("<h2 class=\"phase\">Anexo — Plantillas y rutas en repo</h2><ul>\n")
    for label, pth in ANNEX:
        parts.append(f"<li><strong>{label}:</strong> <code>{pth}</code></li>\n")
    parts.append("</ul>\n</section>\n</body></html>")
    return "".join(parts)


def build_docx() -> Path:
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt, RGBColor

    out = PROTO / "protocolo-dataton-cth.docx"
    doc = Document()
    section = doc.sections[0]
    section.page_height = Cm(29.7)
    section.page_width = Cm(21.0)
    section.top_margin = Cm(2.2)
    section.bottom_margin = Cm(2.4)
    section.left_margin = Cm(1.8)
    section.right_margin = Cm(1.8)

    def set_run_font(run, bold=False, size=11, color=None):
        run.font.name = "Open Sans"
        run._element.rPr.rFonts.set(qn("w:eastAsia"), "Open Sans")
        run.font.size = Pt(size)
        run.bold = bold
        if color:
            run.font.color.rgb = RGBColor(*color)

    def add_heading(text, level=1):
        p = doc.add_paragraph()
        run = p.add_run(text)
        sizes = {0: 22, 1: 16, 2: 13}
        set_run_font(run, bold=True, size=sizes.get(level, 11), color=(0x2D, 0x6A, 0x4F))
        p.paragraph_format.space_after = Pt(6)

    add_heading("Protocolo Datatón CTH", 0)
    p = doc.add_paragraph()
    set_run_font(p.add_run("CleantechHUB · Documento interno · A4"), size=12, color=(0x1B, 0x43, 0x32))
    doc.add_paragraph(
        "Edición referencia: Datatón Observatorio de la Tierra, 24 nov 2026, Universidad Externado."
    )
    doc.add_paragraph(
        "Responsables citados por rol, no por nombre. Datos no confirmados: [por validar] / [pendiente Gideon]."
    )

    for ph in PHASES:
        doc.add_page_break()
        add_heading(f'{ph["rel"]} — {ph["title"]}', 1)
        for label, text in [
            ("Responsable (rol)", ph["role"]),
            ("Objetivo", ph["objective"]),
            ("Entregables", ph["deliverables"]),
        ]:
            p = doc.add_paragraph()
            set_run_font(p.add_run(f"{label}: "), bold=True)
            set_run_font(p.add_run(text))
        p = doc.add_paragraph()
        set_run_font(p.add_run("Checklist:"), bold=True)
        for item in ph["checklist"]:
            doc.add_paragraph(item, style="List Bullet")
        p = doc.add_paragraph()
        set_run_font(p.add_run("Riesgos:"), bold=True)
        for r in ph["risks"]:
            doc.add_paragraph(r, style="List Bullet")

    doc.add_page_break()
    add_heading("Lecciones del 24 nov 2026", 1)
    for le in LESSONS:
        doc.add_paragraph(le, style="List Bullet")

    doc.add_page_break()
    add_heading("Anexo — Plantillas y rutas en repo", 1)
    for label, pth in ANNEX:
        doc.add_paragraph(f"{label}: {pth}", style="List Bullet")

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run_font(p.add_run("© 2026 CleantechHUB Foundation"), size=9, color=(0x1B, 0x43, 0x32))

    doc.save(out)
    return out


def build_pdf(html_path: Path, pdf_path: Path) -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"], stdout=subprocess.DEVNULL)
        from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(html_path.as_uri(), wait_until="networkidle")
        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            margin={"top": "22mm", "bottom": "24mm", "left": "18mm", "right": "18mm"},
        )
        browser.close()


def pdf_to_pngs(pdf_path: Path, out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    renamed: list[Path] = []
    try:
        import pymupdf as fitz
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pymupdf", "-q"])
        import pymupdf as fitz

    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc, start=1):
        dest = out_dir / f"protocolo-dataton-cth-page-{i:02d}.png"
        pix = page.get_pixmap(matrix=fitz.Matrix(150 / 72, 150 / 72))
        pix.save(dest)
        renamed.append(dest)
    doc.close()
    return renamed


def page_count_pdf(pdf_path: Path) -> int:
    try:
        out = subprocess.check_output(["pdfinfo", str(pdf_path)], text=True)
        m = re.search(r"Pages:\s+(\d+)", out)
        return int(m.group(1)) if m else 0
    except (FileNotFoundError, subprocess.CalledProcessError):
        return len(list(RENDER.glob("protocolo-dataton-cth-page-*.png")))


def main() -> dict:
    build_monday_csv()
    html = PROTO / "protocolo-dataton-cth.html"
    html.write_text(html_body(), encoding="utf-8")
    docx_path = build_docx()
    pdf_path = PROTO / "protocolo-dataton-cth.pdf"
    build_pdf(html, pdf_path)
    pngs = pdf_to_pngs(pdf_path, RENDER)
    meta = {
        "docx": str(docx_path.relative_to(ROOT)),
        "pdf": str(pdf_path.relative_to(ROOT)),
        "pages": page_count_pdf(pdf_path),
        "pngs": [str(p.relative_to(ROOT)) for p in pngs],
        "monday_rows": sum(len(p["checklist"]) for p in PHASES),
    }
    (PROTO / "build-meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return meta


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))