#!/usr/bin/env python3
"""Build Plan B ES pitch deck (16:9) — facts from brochure-es.html only."""
from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

OUT_DIR = Path(__file__).resolve().parent
OUT_PPTX = OUT_DIR / "energy-coop-planb-es.pptx"

# CleantechHUB tokens (brochure-es.html / services/energy-coop demo UI)
CTH_PRIMARY = RGBColor(0x2D, 0x6A, 0x4F)
CTH_DARK = RGBColor(0x1B, 0x43, 0x32)
CTH_ACCENT = RGBColor(0x95, 0xD5, 0xB2)
CTH_LIGHT = RGBColor(0xD8, 0xF3, 0xDC)
CTH_TEXT = RGBColor(0x33, 0x33, 0x33)
CTH_MUTED = RGBColor(0x55, 0x55, 0x55)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

FONT = "Inter"
IMPE_FOOT = (
    "Fuente: Índice Multidimensional de Pobreza Energética (IMPE) 2025, "
    "III edición (año base 2024)."
)
ICEE_FOOT = "Fuente: UPME, Boletín ICEE 2024; noticia UPME cobertura 93,12% (2024)."


def _rgb(fill, color: RGBColor) -> None:
    fill.solid()
    fill.fore_color.rgb = color


def set_slide_bg(slide, color: RGBColor) -> None:
    bg = slide.background
    _rgb(bg.fill, color)


def add_brand_bar(slide, prs, subtitle: str | None = None) -> None:
    bar_h = Inches(0.55)
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE.RECTANGLE
        0,
        0,
        prs.slide_width,
        bar_h,
    )
    shape.line.fill.background()
    _rgb(shape.fill, CTH_PRIMARY)
    tf = shape.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = "CleantechHUB"
    p.font.name = FONT
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = WHITE
    if subtitle:
        p2 = tf.add_paragraph()
        p2.text = subtitle
        p2.font.name = FONT
        p2.font.size = Pt(11)
        p2.font.color.rgb = CTH_ACCENT


def add_footer(slide, prs, text: str) -> None:
    box = slide.shapes.add_textbox(
        Inches(0.45),
        prs.slide_height - Inches(0.55),
        prs.slide_width - Inches(0.9),
        Inches(0.45),
    )
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.name = FONT
    p.font.size = Pt(9)
    p.font.color.rgb = CTH_MUTED
    p.alignment = PP_ALIGN.LEFT


def add_title_block(
    slide,
    title: str,
    *,
    top: float = 0.85,
    size: int = 32,
    color: RGBColor = CTH_DARK,
) -> None:
    box = slide.shapes.add_textbox(Inches(0.6), Inches(top), Inches(12.1), Inches(1.4))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT
    p.font.size = Pt(size)
    p.font.bold = True
    p.font.color.rgb = color
    p.line_spacing = 1.1


def add_bullets(
    slide,
    lines: list[str],
    *,
    top: float,
    height: float = 4.5,
    size: int = 20,
) -> None:
    box = slide.shapes.add_textbox(Inches(0.75), Inches(top), Inches(11.8), Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.name = FONT
        p.font.size = Pt(size)
        p.font.color.rgb = CTH_TEXT
        p.space_after = Pt(10)
        p.level = 0


def add_big_stats(slide, stats: list[tuple[str, str]], top: float = 2.0) -> None:
    w = Inches(2.85)
    h = Inches(1.35)
    gap = Inches(0.25)
    start_x = Inches(0.6)
    for i, (val, lbl) in enumerate(stats):
        col = i % 2
        row = i // 2
        x = start_x + col * (w + gap)
        y = Inches(top) + row * (h + Inches(0.2))
        card = slide.shapes.add_shape(1, x, y, w, h)
        card.line.color.rgb = CTH_PRIMARY
        _rgb(card.fill, CTH_LIGHT)
        tf = card.text_frame
        tf.margin_left = Inches(0.12)
        tf.margin_top = Inches(0.08)
        p = tf.paragraphs[0]
        p.text = val
        p.font.name = FONT
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = CTH_DARK
        p2 = tf.add_paragraph()
        p2.text = lbl
        p2.font.name = FONT
        p2.font.size = Pt(11)
        p2.font.color.rgb = CTH_MUTED


def add_notes(slide, text: str) -> None:
    notes = slide.notes_slide
    tf = notes.notes_text_frame
    tf.text = text


def blank_layout(prs: Presentation):
    return prs.slide_layouts[6]


def build() -> None:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # --- Slide 1: Title ---
    s1 = prs.slides.add_slide(blank_layout(prs))
    set_slide_bg(s1, WHITE)
    add_brand_bar(s1, prs, "Energy Coop · Pitch Plan B · Nov 2026")
    accent = s1.shapes.add_shape(1, 0, Inches(0.55), prs.slide_width, Inches(0.08))
    accent.line.fill.background()
    _rgb(accent.fill, CTH_ACCENT)
    add_title_block(
        s1,
        "Cooperativas energéticas",
        top=1.35,
        size=40,
    )
    sub = s1.shapes.add_textbox(Inches(0.6), Inches(2.15), Inches(11.5), Inches(1.2))
    sp = sub.text_frame.paragraphs[0]
    sp.text = "CleantechHUB como socio contra la pobreza energética"
    sp.font.name = FONT
    sp.font.size = Pt(26)
    sp.font.color.rgb = CTH_PRIMARY
    sp.font.bold = True
    meta = s1.shapes.add_textbox(Inches(0.6), Inches(5.6), Inches(8), Inches(0.5))
    mp = meta.text_frame.paragraphs[0]
    mp.text = "Embajada · 11 nov 2026 · 15 min · ES"
    mp.font.name = FONT
    mp.font.size = Pt(14)
    mp.font.color.rgb = CTH_MUTED
    add_notes(
        s1,
        "Apertura: presentar a CleantechHUB como socio técnico y territorial, no como utility. "
        "En 15 minutos: brecha IMPE, ritmo hacia 2030, por qué el cuello de botella es OPEX, "
        "y la cooperativa energética como vehículo con PASO Colombia y aliados de financiación.",
    )

    # --- Slide 2: La brecha ---
    s2 = prs.slides.add_slide(blank_layout(prs))
    set_slide_bg(s2, WHITE)
    add_brand_bar(s2, prs)
    add_title_block(s2, "La brecha nacional", top=0.75, size=34)
    add_big_stats(
        s2,
        [
            ("15,4%", "IMPE 2024 · ~8,1 M personas"),
            ("9,5%", "Escenario 2030 · ~5,17 M (−2,9 M)"),
            ("75,92% / 93,12%", "ICEE rural vs nacional (2024)"),
            ("63,1% / 52,8%", "IMPE La Guajira / Chocó (2024)"),
        ],
    )
    body = s2.shapes.add_textbox(Inches(0.75), Inches(4.35), Inches(11.5), Inches(1.5))
    bp = body.text_frame.paragraphs[0]
    bp.text = (
        "Cerrar ~2,9 millones de personas en pobreza energética es el salto entre "
        "la línea base 2024 y el escenario de un dígito en 2030."
    )
    bp.font.name = FONT
    bp.font.size = Pt(18)
    bp.font.color.rgb = CTH_TEXT
    add_footer(s2, prs, f"{IMPE_FOOT} · {ICEE_FOOT}")
    add_notes(
        s2,
        "Datos verificados en IMPE 2025 (incidencia 15,4%, meta 9,5%, deptos.). "
        "ICEE muestra la brecha de acceso: rural 75,92% frente a 93,12% nacional. "
        "No mezclar con IPEM de MinEnergía.",
    )

    # --- Slide 3: El ritmo ---
    s3 = prs.slides.add_slide(blank_layout(prs))
    set_slide_bg(s3, WHITE)
    add_brand_bar(s3, prs)
    add_title_block(s3, "El ritmo hacia 2030", top=0.75, size=34)
    cards = [
        ("~300 k pers./año", "Ritmo observado", "~2034", CTH_MUTED),
        ("~490 k pers./año", "Escenario IMPE 2030", "2030", CTH_PRIMARY),
    ]
    for i, (rate, lbl, year, accent_c) in enumerate(cards):
        x = Inches(0.9 + i * 6.2)
        card = s3.shapes.add_shape(1, x, Inches(2.0), Inches(5.5), Inches(2.8))
        card.line.color.rgb = CTH_PRIMARY
        _rgb(card.fill, CTH_LIGHT if i else WHITE)
        tf = card.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = rate
        p.font.name = FONT
        p.font.size = Pt(30)
        p.font.bold = True
        p.font.color.rgb = CTH_DARK
        p.alignment = PP_ALIGN.CENTER
        p2 = tf.add_paragraph()
        p2.text = lbl
        p2.font.name = FONT
        p2.font.size = Pt(14)
        p2.font.color.rgb = CTH_MUTED
        p2.alignment = PP_ALIGN.CENTER
        p3 = tf.add_paragraph()
        p3.text = year
        p3.font.name = FONT
        p3.font.size = Pt(36)
        p3.font.bold = True
        p3.font.color.rgb = accent_c
        p3.alignment = PP_ALIGN.CENTER
    cap = s3.shapes.add_textbox(Inches(0.75), Inches(5.1), Inches(11.8), Inches(0.9))
    cp = cap.text_frame.paragraphs[0]
    cp.text = "490 k × 6 años ≈ 2,94 M personas · ≥1,0 p.p./año de incidencia"
    cp.font.name = FONT
    cp.font.size = Pt(17)
    cp.font.color.rgb = CTH_TEXT
    add_footer(s3, prs, f"{IMPE_FOOT} pp. 12, 33.")
    add_notes(
        s3,
        "El informe IMPE contrasta el ritmo ~300 mil personas/año (llegada ~2034) "
        "con el escenario que anticipa la meta a 2030 (~490 mil/año). "
        "Mensaje: acelerar es política de ritmo, no solo de inversión inicial.",
    )

    # --- Slide 4: OPEX ---
    s4 = prs.slides.add_slide(blank_layout(prs))
    set_slide_bg(s4, WHITE)
    add_brand_bar(s4, prs)
    add_title_block(s4, "No es solo CAPEX: el riesgo es OPEX", top=0.75, size=32)
    add_bullets(
        s4,
        [
            "Contraloría: falta remunerar operación y administración de microredes y SFVI; "
            "fallas en mantenimiento y monitoreo.",
            "Amazonas: ~$30.000 millones (regalías) en fotovoltaico sin operar; "
            "baterías dañadas — sostenibilidad crítica.",
            "CREG: miles de SFV rurales sin gestión → abandonados; norma, instaladores "
            "certificados y AOM insuficientes.",
        ],
        top=1.85,
        size=19,
    )
    add_footer(
        s4,
        prs,
        "Fuentes: El Colombiano (Contraloría); Seguimiento.co/Procuraduría (Amazonas); "
        "CREG Circular 005-13; Concepto CREG 4022/2019 (AOM).",
    )
    add_notes(
        s4,
        "Reencuadre para la sala: los activos existen, pero sin O&M remunerado y gobernanza "
        "local se repite el patrón de abandono. CleantechHUB entra en operación y modelo "
        "cooperativo, no solo en megavatios instalados.",
    )

    # --- Slide 5: Cooperativa ---
    s5 = prs.slides.add_slide(blank_layout(prs))
    set_slide_bg(s5, WHITE)
    add_brand_bar(s5, prs)
    add_title_block(s5, "La cooperativa como herramienta", top=0.75, size=34)
    badge = s5.shapes.add_shape(1, Inches(0.75), Inches(1.65), Inches(2.2), Inches(0.45))
    badge.line.fill.background()
    _rgb(badge.fill, CTH_ACCENT)
    btf = badge.text_frame
    btf.paragraphs[0].text = "PROPUESTA CTH"
    btf.paragraphs[0].font.name = FONT
    btf.paragraphs[0].font.size = Pt(11)
    btf.paragraphs[0].font.bold = True
    btf.paragraphs[0].font.color.rgb = CTH_DARK
    box = s5.shapes.add_shape(1, Inches(0.75), Inches(2.25), Inches(11.8), Inches(3.2))
    box.line.color.rgb = CTH_PRIMARY
    box.line.dash_style = 3
    _rgb(box.fill, CTH_LIGHT)
    tf = box.text_frame
    tf.margin_left = Inches(0.2)
    tf.margin_top = Inches(0.15)
    p = tf.paragraphs[0]
    p.text = (
        "O&M comunitario + ingresos + propiedad local complementan CAPEX con contratos OPEX "
        "(FV, baterías, monitoreo; CREG/SSPD) y gobernanza comunitaria."
    )
    p.font.name = FONT
    p.font.size = Pt(22)
    p.font.color.rgb = CTH_DARK
    p2 = tf.add_paragraph()
    p2.text = "KPIs: acceso y calidad en IMPE — no sustituye ICEE ni IPEM."
    p2.font.name = FONT
    p2.font.size = Pt(18)
    p2.font.color.rgb = CTH_TEXT
    p2.space_before = Pt(14)
    add_notes(
        s5,
        "Dejar claro que es propuesta de diseño CleantechHUB: cooperativa energética como "
        "contraparte de OPEX y licencia social, alineada a indicadores IMPE.",
    )

    # --- Slide 6: Talento ---
    s6 = prs.slides.add_slide(blank_layout(prs))
    set_slide_bg(s6, WHITE)
    add_brand_bar(s6, prs)
    add_title_block(s6, "Talento local y empleos verdes", top=0.75, size=34)
    add_bullets(
        s6,
        [
            "Escuela Colombiana de Ingeniería Julio Garavito — colaboración en formación "
            "y empleos verdes.",
            "CLSA y retos energéticos; 3.er lugar Solucionatón 10X (2026).",
            "Diplomado y cursos en renovables + laboratorio 101,76 kWp.",
        ],
        top=1.85,
        size=20,
    )
    add_footer(s6, prs, "Fuente: escuelaing.edu.co — CLSA, Solucionatón 10X, lab renovables.")
    add_notes(
        s6,
        "Mencionar colaboración con la Escuela sin afirmar ni negar convenios marco. "
        "Énfasis en pipeline de talento para O&M, monitoreo y gestión cooperativa.",
    )

    # --- Slide 7: Comunidades ---
    s7 = prs.slides.add_slide(blank_layout(prs))
    set_slide_bg(s7, WHITE)
    add_brand_bar(s7, prs, "PASO Colombia · socio territorial")
    add_title_block(s7, "Comunidades productivas (PASO)", top=0.72, size=30)
    lead = s7.shapes.add_textbox(Inches(0.75), Inches(1.45), Inches(11.5), Inches(0.55))
    lp = lead.text_frame.paragraphs[0]
    lp.text = "Proyectos productivos y cooperativos — PASO no ejecuta proyectos de energía."
    lp.font.name = FONT
    lp.font.size = Pt(16)
    lp.font.color.rgb = CTH_MUTED
    territories = [
        "Fonseca, La Guajira — COOMPAZCOL, ASMUPERIJA (IMPE 63,1%)",
        "Puerto Asís / Puerto Guzmán, Putumayo (IMPE 58,7%)",
        "Istmina, Chocó — Bioconversión Chocó, Aserrío Continental (52,8%)",
        "San José del Guaviare (IMPE 38,9%)",
        "Arauca — COOPCACAO, COMPROCAR, Filimarpaz (27,9%)",
    ]
    add_bullets(s7, territories, top=2.05, height=2.8, size=15)
    cand = s7.shapes.add_shape(1, Inches(0.75), Inches(5.05), Inches(11.5), Inches(0.65))
    _rgb(cand.fill, CTH_LIGHT)
    cand.line.color.rgb = CTH_PRIMARY
    ctf = cand.text_frame
    ctf.paragraphs[0].text = (
        "Comunidad candidata Energy Coop: Corozal, Sucre (IMPE 43,1%) — no es proyecto PASO."
    )
    ctf.paragraphs[0].font.name = FONT
    ctf.paragraphs[0].font.size = Pt(14)
    ctf.paragraphs[0].font.bold = True
    ctf.paragraphs[0].font.color.rgb = CTH_DARK
    add_footer(s7, prs, f"{IMPE_FOOT} deptos. · CTH/PASO brief 2026.")
    add_notes(
        s7,
        "Mapa mental Colombia: foco en territorios PASO con IMPE departamental donde está "
        "publicado. Corozal es candidata de filtrado Energy Coop, no piloto. "
        "PASO aporta tejido productivo; CTH aporta capa energética cooperativa.",
    )

    # --- Slide 8: Data lab ---
    s8 = prs.slides.add_slide(blank_layout(prs))
    set_slide_bg(s8, WHITE)
    add_brand_bar(s8, prs)
    add_title_block(s8, "Data lab: embudo de candidatas", top=0.75, size=32)
    funnel_y = Inches(1.85)
    steps = ["~1.000", "100", "20", "10"]
    x = Inches(1.0)
    for i, step in enumerate(steps):
        sh = s8.shapes.add_shape(1, x, funnel_y, Inches(2.4), Inches(0.75))
        _rgb(sh.fill, CTH_LIGHT)
        sh.line.color.rgb = CTH_PRIMARY
        sh.text_frame.paragraphs[0].text = step
        sh.text_frame.paragraphs[0].font.name = FONT
        sh.text_frame.paragraphs[0].font.size = Pt(22)
        sh.text_frame.paragraphs[0].font.bold = True
        sh.text_frame.paragraphs[0].font.color.rgb = CTH_DARK
        sh.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        x += Inches(2.65)
        if i < len(steps) - 1:
            arr = s8.shapes.add_textbox(x - Inches(2.15), funnel_y + Inches(0.15), Inches(0.4), Inches(0.4))
            arr.text_frame.paragraphs[0].text = "→"
            arr.text_frame.paragraphs[0].font.size = Pt(24)
            arr.text_frame.paragraphs[0].font.color.rgb = CTH_PRIMARY
    add_bullets(
        s8,
        [
            "Base: ~1.000 comunidades priorizadas (MinEnergía).",
            "Filtros: pobreza energética, ZNI/off-grid (UPME), recurso solar, "
            "personería jurídica/NIT, licencia social.",
            "Candidatas, no pilotos — sin publicar puntajes.",
        ],
        top=3.0,
        size=18,
    )
    add_footer(s8, prs, "Fuente: CTH/PASO brief 2026; IMPE/ZNI/UPME públicos.")
    add_notes(
        s8,
        "Explicar el embudo 1000→10 como método transparente: priorización territorial, "
        "viabilidad solar y capacidad jurídica comunitaria antes de comprometer CAPEX.",
    )

    # --- Slide 9: Socios ---
    s9 = prs.slides.add_slide(blank_layout(prs))
    set_slide_bg(s9, WHITE)
    add_brand_bar(s9, prs)
    add_title_block(s9, "Red de socios potenciales", top=0.75, size=34)
    partners = [
        ("FMO", "Financiación solar a escala en Colombia"),
        ("RVO", "Facilitación y cooperación empresarial"),
        ("Green Choice", "Financiación en comunidades energéticas"),
        ("Energie Samen", "Aprendizaje entre pares en cooperativas"),
    ]
    for i, (name, desc) in enumerate(partners):
        col = i % 2
        row = i // 2
        px = Inches(0.75 + col * 6.1)
        py = Inches(1.85 + row * 2.1)
        card = s9.shapes.add_shape(1, px, py, Inches(5.7), Inches(1.75))
        _rgb(card.fill, WHITE)
        card.line.color.rgb = CTH_PRIMARY
        tf = card.text_frame
        tf.margin_left = Inches(0.15)
        p = tf.paragraphs[0]
        p.text = name
        p.font.name = FONT
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = CTH_PRIMARY
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT
        p2.font.size = Pt(14)
        p2.font.color.rgb = CTH_TEXT
    disclaimer = s9.shapes.add_textbox(Inches(0.75), Inches(6.15), Inches(11.5), Inches(0.45))
    dp = disclaimer.text_frame.paragraphs[0]
    dp.text = "Socios potenciales — sin acuerdos firmados en esta fase."
    dp.font.name = FONT
    dp.font.size = Pt(13)
    dp.font.italic = True
    dp.font.color.rgb = CTH_MUTED
    add_footer(s9, prs, "Fuentes: fmo.nl (Colombia); CTH brief 2026 (Green Choice, Energie Samen).")
    add_notes(
        s9,
        "Presentar FMO, RVO, Green Choice y Energie Samen como conversaciones de "
        "financiación y peer learning, sin afirmar MOU firmados ni encuadre país.",
    )

    # --- Slide 10: Próximos pasos ---
    s10 = prs.slides.add_slide(blank_layout(prs))
    set_slide_bg(s10, WHITE)
    add_brand_bar(s10, prs)
    add_title_block(s10, "Próximos pasos", top=0.85, size=36)
    steps_box = s10.shapes.add_textbox(Inches(0.9), Inches(2.0), Inches(11.2), Inches(3.2))
    stf = steps_box.text_frame
    items = [
        "Sesión de trabajo con el equipo completo y Juan Fernando Lucio (PASO Colombia).",
        "Alinear embudo de candidatas, rol cooperativo y necesidades de financiación.",
        "Contacto: cleantechhub.net",
    ]
    for i, item in enumerate(items):
        p = stf.paragraphs[0] if i == 0 else stf.add_paragraph()
        p.text = f"{i + 1}. {item}"
        p.font.name = FONT
        p.font.size = Pt(22)
        p.font.color.rgb = CTH_TEXT
        p.space_after = Pt(16)
    cta = s10.shapes.add_shape(1, Inches(0.75), Inches(5.5), Inches(5.5), Inches(0.7))
    _rgb(cta.fill, CTH_PRIMARY)
    cta.line.fill.background()
    ctf = cta.text_frame
    ctf.paragraphs[0].text = "cleantechhub.net"
    ctf.paragraphs[0].font.name = FONT
    ctf.paragraphs[0].font.size = Pt(20)
    ctf.paragraphs[0].font.bold = True
    ctf.paragraphs[0].font.color.rgb = WHITE
    ctf.paragraphs[0].alignment = PP_ALIGN.CENTER
    add_notes(
        s10,
        "Cierre operativo: proponer mesa de trabajo con PASO (Juan Fernando Lucio) "
        "y definir calendario post-Embajada. Agradecer los 15 minutos y dejar contacto web.",
    )

    # Metadata — no banned strings
    prs.core_properties.title = "Cooperativas energéticas — Plan B ES"
    prs.core_properties.subject = "Energy Coop pitch CleantechHUB"
    prs.core_properties.author = "CleantechHUB Foundation"
    prs.core_properties.comments = "Nov 2026 · datos IMPE 2025"

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    prs.save(OUT_PPTX)
    print(f"Wrote {OUT_PPTX} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    build()
