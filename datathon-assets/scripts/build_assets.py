#!/usr/bin/env python3
"""Generate datathon-assets copy, HTML visuals, INDEX.md (PNG/PDF via render-visuals.sh)."""
from __future__ import annotations

import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
LOGO_SVG = REPO / "brand/datalab-logo-2026-11/logo/datalab-logo.svg"

COLORS = {
    "deep": "#0C498A",
    "cyan": "#B2EEFA",
    "green": "#9DC384",
    "forest": "#669348",
    "sky": "#69B5FA",
    "white": "#FFFFFF",
    "cth_primary": "#2D6A4F",
    "cth_dark": "#1B4332",
    "cth_accent": "#95D5B2",
    "cth_light": "#D8F3DC",
    "text": "#333333",
}

EVENT_DATE = "martes 24 de noviembre de 2026"
EVENT_SHORT = "24 · 11 · 2026"
BRAND_LINE = "Datalab powered by CleantechHUB"

STREAMS = [
    {
        "id": "01-agenda",
        "title": "Agenda del evento",
        "headline": "Agenda · Observatorio de la Tierra",
        "sub": "Soft launch de Datalab · " + EVENT_SHORT,
        "bullets": [
            "Panel de apertura — PENDIENTE (hora y panelistas)",
            "Anuncio de Datalab (sandboxes + gobernanza de datos)",
            "Demostración en vivo Air4U (~10–15 min) + Q&A (~15 min)",
            "Breakouts tipo datathon — PENDIENTE (reglas y premios)",
        ],
    },
    {
        "id": "02-earth-observatory",
        "title": "Lanzamiento Observatorio de la Tierra",
        "headline": "Observatorio de la Tierra",
        "sub": "Lanzamiento · " + EVENT_DATE,
        "bullets": [
            "Datos ambientales accionables para decisiones locales",
            "CleantechHUB como custodio del ecosistema",
            "Colaboración académica — [LOGO EXTERNADO]",
            "Hora y sede: PENDIENTE",
        ],
    },
    {
        "id": "03-datalab",
        "title": "Datalab soft launch",
        "headline": "Datalab",
        "sub": BRAND_LINE,
        "bullets": [
            "Sandboxes para probar flujos reales de datos ambientales",
            "Gobernanza de datos desde el diseño",
            "Fase inicial: cargas manuales (CSV/SQLite)",
            "Registro y sede: PENDIENTE",
        ],
    },
    {
        "id": "04-datathon",
        "title": "Datathon",
        "headline": "Datathon",
        "sub": "Breakouts colaborativos · " + EVENT_SHORT,
        "bullets": [
            "Construir sobre datos del Observatorio y Datalab",
            "Equipos multidisciplinarios — PENDIENTE (formato)",
            "Premios y criterios: PENDIENTE",
            "Inscripción: PENDIENTE",
        ],
    },
    {
        "id": "05-air4u-demo",
        "title": "Demo en vivo Air4U",
        "headline": "Demo en vivo · Air4U",
        "sub": "Socio de innovación · CleantechHUB custodio",
        "bullets": [
            "Recorrido: flujo de datos → conjuntos → tablero",
            "Capas de madurez de datos (sin metáforas de metales)",
            "Métrica compartida: partículas por metro cúbico",
            "Duración demo ~10–15 min + Q&A ~15 min — horario PENDIENTE",
        ],
    },
]

COPY_FOOTER = textwrap.dedent("""
---
**Estado:** Borrador — *Awaiting Gideon's approval* · NO publicar desde este PR.

**Créditos:** Air4U = socio de innovación · CleantechHUB = custodio · [LOGO EXTERNADO] = aliado académico (placeholder).

**PENDIENTE operativo:** sede, hora de inicio, enlace RSVP, panelistas confirmados, reglas/premios del datathon, logos finales.
""").strip()


def write_copy(stream: dict) -> None:
    sid = stream["id"]
    folder = ROOT / sid
    folder.mkdir(parents=True, exist_ok=True)
    title = stream["title"]
    bullets = "\n".join(f"- {b}" for b in stream["bullets"])

    linkedin = textwrap.dedent(f"""
    ## LinkedIn (página CleantechHUB)

    **{title}** — {EVENT_DATE}

    {stream["headline"]}: {stream["sub"]}

    {bullets.replace('- ', '')}

    Trabajamos con **[LOGO AIR4U]** como socio de innovación; **CleantechHUB** actúa como custodio del enfoque y del ecosistema. Aliado académico: **[LOGO EXTERNADO]**.

    Sede, hora y registro: **PENDIENTE**.

    #CleantechHUB #ClimateAction #Cleantech #ObservatorioDeLaTierra #Datalab #CalidadDelAire
    """).strip()

    instagram = textwrap.dedent(f"""
    ## Instagram (caption)

    {stream["headline"]} 🌍

    {EVENT_SHORT} · {BRAND_LINE}

    {stream["bullets"][0]}
    {stream["bullets"][1]}

    Air4U · CleantechHUB · [LOGO EXTERNADO]

    Sede y hora: PENDIENTE. Más info en bio — PENDIENTE.

    #CleantechHUB #Datalab #ObservatorioDeLaTierra #CalidadDelAire #DatosAmbientales #InnovaciónClimática
    """).strip()

    facebook = textwrap.dedent(f"""
    ## Facebook

    {title} — {EVENT_DATE}

    {stream["sub"]}

    {bullets}

    **Air4U** (innovación) + **CleantechHUB** (custodio). **[LOGO EXTERNADO]**

    Confirmación de sede, horario y enlace: PENDIENTE.

    #CleantechHUB #ClimateAction #Datalab
    """).strip()

    whatsapp = textwrap.dedent(f"""
    ## WhatsApp / email (corto)

    Hola — te compartimos la convocatoria *{title}* ({EVENT_SHORT}): {stream["headline"]}. {stream["bullets"][0]}. Air4U + CleantechHUB + [LOGO EXTERNADO]. Sede/hora/RSVP: PENDIENTE. ¿Te interesa asistir? Responde y te enviamos detalles cuando estén confirmados.
    """).strip()

    body = f"# Copy ES — {sid}\n\n{linkedin}\n\n---\n\n{instagram}\n\n---\n\n{facebook}\n\n---\n\n{whatsapp}\n\n---\n\n{COPY_FOOTER}\n"
    (folder / "copy-es.md").write_text(body, encoding="utf-8")
    write_copy_txt(stream, folder)


def write_copy_txt(stream: dict, folder: Path) -> None:
    """Plain Spanish share copy for WhatsApp kit (no internal desk notes)."""
    title = stream["title"]
    bullets = "\n".join(f"• {b}" for b in stream["bullets"])
    text = textwrap.dedent(
        f"""
        {title}
        {EVENT_DATE} · {BRAND_LINE}

        {stream["headline"]}
        {stream["sub"]}

        {bullets}

        Air4U — socio de innovación
        CleantechHUB — custodio
        [LOGO EXTERNADO] — aliado académico

        Sede, hora y registro: confirmar con el equipo (pendiente de publicación).

        CleantechHUB · Inspira. Actúa. Transforma.
        """
    ).strip()
    (folder / "copy.txt").write_text(text + "\n", encoding="utf-8")


def logo_markup(fill_wordmark: str = "#FFFFFF") -> str:
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 120" width="200" height="50" aria-hidden="true">
      <g transform="translate(4, 8) scale(0.85)">
        <path d="M8 52 L52 72 L96 52 L52 32 Z" fill="#69B5FA"/>
        <path d="M8 38 L52 58 L96 38 L52 18 Z" fill="#9DC384"/>
        <path d="M8 24 L52 44 L96 24 L52 4 Z" fill="#0C498A"/>
        <rect x="44" y="74" width="16" height="6" rx="2" fill="#669348"/>
      </g>
      <text x="118" y="52" font-family="Titillium Web, sans-serif" font-weight="700" font-size="32" fill="{fill_wordmark}">Datalab</text>
    </svg>
    """


def base_css() -> str:
    return f"""
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&family=Titillium+Web:wght@700&display=swap');
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'Open Sans', sans-serif; color: {COLORS['deep']}; background: {COLORS['cyan']}; }}
    .canvas {{ position: relative; overflow: hidden; background: {COLORS['cyan']}; }}
    .sidebar {{ background: {COLORS['deep']}; color: {COLORS['white']}; }}
    .head {{ font-family: 'Titillium Web', sans-serif; font-weight: 700; }}
    .tag {{ color: {COLORS['forest']}; font-weight: 600; }}
    .bullet {{ font-size: 22px; line-height: 1.35; margin: 8px 0; padding-left: 18px; position: relative; }}
    .bullet::before {{ content: '•'; position: absolute; left: 0; color: {COLORS['forest']}; }}
    .ph {{ border: 1.5px dashed {COLORS['deep']}; background: {COLORS['white']}; font-size: 11px; font-weight: 600; padding: 8px 10px; border-radius: 6px; }}
    .logos {{ display: flex; gap: 12px; flex-wrap: wrap; }}
    """


def visual_html(stream: dict, width: int, height: int, layout: str) -> str:
    bullets_html = "".join(f'<p class="bullet">{b}</p>' for b in stream["bullets"][:4])
    logo = logo_markup("#FFFFFF" if layout != "story-light" else "#0C498A")

    if layout == "linkedin":
        inner = f"""
        <div class="canvas" style="width:{width}px;height:{height}px;display:flex;">
          <div class="sidebar" style="width:360px;padding:48px 32px;">{logo}
            <p style="margin-top:24px;font-size:14px;opacity:.9;">CleantechHUB · custodio</p>
          </div>
          <div style="flex:1;padding:48px 40px;">
            <h1 class="head" style="font-size:52px;line-height:1.05;">{stream['headline']}</h1>
            <p style="font-size:28px;margin:12px 0 24px;font-weight:600;">{stream['sub']}</p>
            {bullets_html}
            <p class="tag" style="margin-top:20px;font-size:20px;">Inspira. Actúa. Transforma.</p>
            <div class="logos" style="margin-top:28px;">
              <div class="ph">[LOGO AIR4U]</div>
              <div class="ph">[LOGO EXTERNADO]</div>
              <div class="ph">CleantechHUB logo PENDIENTE</div>
            </div>
          </div>
        </div>
        """
    elif layout == "feed":
        inner = f"""
        <div class="canvas" style="width:{width}px;height:{height}px;padding:56px 48px;background:linear-gradient(180deg,{COLORS['deep']} 0%, {COLORS['deep']} 42%, {COLORS['cyan']} 42%);">
          <div style="color:{COLORS['white']};">{logo.replace('fill="#FFFFFF"', 'fill="#FFFFFF"')}</div>
          <h1 class="head" style="color:{COLORS['white']};font-size:56px;margin-top:32px;line-height:1.05;">{stream['headline']}</h1>
          <p style="color:{COLORS['cyan']};font-size:26px;margin-top:12px;font-weight:600;">{stream['sub']}</p>
          <div style="margin-top:36px;background:{COLORS['white']};border-radius:12px;padding:28px;">
            {bullets_html}
          </div>
          <div class="logos" style="margin-top:28px;">
            <div class="ph">[LOGO AIR4U]</div>
            <div class="ph">[LOGO EXTERNADO]</div>
          </div>
        </div>
        """
    else:  # story
        inner = f"""
        <div class="canvas" style="width:{width}px;height:{height}px;padding:64px 48px;background:{COLORS['deep']};color:{COLORS['white']};">
          <div style="background:{COLORS['sky']};color:{COLORS['deep']};display:inline-block;padding:8px 16px;border-radius:999px;font-weight:600;font-size:22px;">{EVENT_SHORT}</div>
          <h1 class="head" style="font-size:64px;margin-top:40px;line-height:1.05;">{stream['headline']}</h1>
          <p style="font-size:28px;margin-top:16px;opacity:.95;">{stream['sub']}</p>
          <div style="margin-top:48px;">{bullets_html.replace('class="bullet"', 'class="bullet" style="color:#fff;"')}</div>
          <p class="tag" style="margin-top:40px;font-size:24px;color:{COLORS['green']};">Datalab powered by CleantechHUB</p>
          <div class="logos" style="margin-top:48px;">
            <div class="ph" style="color:{COLORS['deep']};">[LOGO AIR4U]</div>
            <div class="ph" style="color:{COLORS['deep']};">[LOGO EXTERNADO]</div>
          </div>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<title>{stream['id']} {layout}</title>
<style>{base_css()}
html, body {{ width: {width}px; height: {height}px; overflow: hidden; }}
</style>
</head>
<body>{inner}</body>
</html>
"""


def agenda_print_html() -> str:
    blocks = [
        ("PENDIENTE", "Registro y bienvenida", "PENDIENTE (instrucciones de acceso)"),
        ("PENDIENTE", "Panel de apertura", "Representantes académicos, territorio y aliados — panelistas PENDIENTE"),
        ("PENDIENTE", "Lanzamiento Observatorio de la Tierra", "Marco del observatorio y datos ambientales accionables"),
        ("PENDIENTE", "Anuncio Datalab", "Sandboxes + gobernanza · Datalab powered by CleantechHUB"),
        ("PENDIENTE", "Demo en vivo Air4U", "~10–15 min · flujo de datos → tablero · [LOGO AIR4U]"),
        ("PENDIENTE", "Q&A demo", "~15 min"),
        ("PENDIENTE", "Breakouts datathon", "Reglas y premios PENDIENTE"),
        ("PENDIENTE", "Cierre", "Próximos pasos PENDIENTE"),
    ]
    rows = "".join(
        f"<tr><td>{t}</td><td><strong>{title}</strong><br/><span>{detail}</span></td></tr>"
        for t, title, detail in blocks
    )
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<title>Agenda imprimible</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&family=Titillium+Web:wght@700&display=swap');
body {{ font-family: 'Open Sans', sans-serif; color: {COLORS['text']}; padding: 40px; max-width: 900px; margin: 0 auto; }}
h1 {{ font-family: 'Titillium Web', sans-serif; color: {COLORS['cth_primary']}; font-size: 32px; }}
.sub {{ color: {COLORS['cth_dark']}; margin: 8px 0 24px; }}
table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
td {{ border-bottom: 1px solid #ccc; padding: 10px 8px; vertical-align: top; }}
td:first-child {{ width: 110px; font-weight: 600; color: {COLORS['deep']}; }}
.logos {{ margin-top: 24px; display: flex; gap: 10px; }}
.ph {{ border: 1px dashed {COLORS['deep']}; padding: 8px; font-size: 11px; }}
.footer {{ margin-top: 20px; font-size: 12px; color: #666; }}
</style>
</head>
<body>
<h1>Agenda · Observatorio de la Tierra</h1>
<p class="sub">{EVENT_DATE} · {BRAND_LINE}<br/>Sede: PENDIENTE · Hora de inicio: PENDIENTE</p>
<table>{rows}</table>
<div class="logos">
  <div class="ph">[LOGO AIR4U] · socio de innovación</div>
  <div class="ph">[LOGO EXTERNADO]</div>
  <div class="ph">CleantechHUB · custodio</div>
</div>
</body>
</html>
"""


def write_visuals(stream: dict) -> list[dict]:
    folder = ROOT / stream["id"]
    specs = [
        ("linkedin-1200x627", 1200, 627, "linkedin"),
        ("instagram-feed-1080x1350", 1080, 1350, "feed"),
        ("story-1080x1920", 1080, 1920, "story"),
    ]
    manifest = []
    for name, w, h, layout in specs:
        html_path = folder / f"{name}.html"
        png_path = folder / f"{name}.png"
        html_path.write_text(visual_html(stream, w, h, layout), encoding="utf-8")
        manifest.append(
            {
                "file": f"{stream['id']}/{name}.html",
                "png": f"{stream['id']}/{name}.png",
                "channel": name.split("-")[0],
                "size": f"{w}x{h}",
            }
        )
    return manifest


def write_agenda_extras() -> list[dict]:
    folder = ROOT / "01-agenda"
    html = agenda_print_html()
    (folder / "agenda-print-a4.html").write_text(html, encoding="utf-8")
    return [
        {
            "file": "01-agenda/agenda-print-a4.html",
            "png": "01-agenda/agenda-print-a4.png",
            "pdf": "01-agenda/agenda-print-a4.pdf",
            "channel": "printable",
            "size": "A4",
        }
    ]


def write_index(all_files: list[dict]) -> None:
    pendientes = [
        "Hora de inicio del evento",
        "Sede / venue",
        "Enlace RSVP / registro",
        "Panelistas del panel de apertura",
        "Reglas y premios del datathon",
        "Logos finales CleantechHUB, Air4U, Externado",
        "Mapa o foto de sede",
        "Contacto / CTA final",
        "Tercera fecha de pre-evento (si aplica fuera de este pack)",
    ]
    lines = [
        "# Datathon / Earth Observatory — asset index",
        "",
        f"**Marca:** {BRAND_LINE} (`Datalab` una palabra).",
        f"**Evento ancla:** {EVENT_DATE}.",
        "**Estado:** borrador PR — NO publicar.",
        "",
        "## Archivos",
        "",
        "| Archivo | PNG/PDF | Canal | Tamaño |",
        "|---------|---------|-------|--------|",
    ]
    for row in sorted(all_files, key=lambda r: r["file"]):
        png = row.get("png", "—")
        pdf = row.get("pdf", "—")
        extra = pdf if pdf != "—" else png
        lines.append(f"| `{row['file']}` | `{extra}` | {row['channel']} | {row['size']} |")

    for stream in STREAMS:
        lines.append(f"| `{stream['id']}/copy-es.md` | — | copy | ES |")

    lines.extend(["", "## PENDIENTE (global)", ""])
    for p in pendientes:
        lines.append(f"- {p}")

    lines.extend(
        [
            "",
            "## Reglas aplicadas",
            "",
            "- Copy CTH en español latinoamericano.",
            "- Sin ángulo cannabis; sin precios Phase 2; sin nombre Comapán.",
            "- Capas de datos descritas en lenguaje llano (no metáforas bronze/silver/gold).",
            "- Air4U = socio de innovación; CleantechHUB = custodio.",
            "- Placeholders de logo hasta archivo aprobado.",
            "",
            f"**Kit logo:** `brand/datalab-logo-2026-11/` (Option B).",
            "",
            "## WhatsApp kit",
            "",
            "`datathon-kit.zip` — PNGs + `copy.txt` per stream, `agenda-evento.pdf` en la raíz. Regenerar: `scripts/build-kit-zip.sh` (después de `build_assets.py` + `render-visuals.sh`).",
        ]
    )
    (ROOT / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    manifest: list[dict] = []
    for stream in STREAMS:
        write_copy(stream)
        manifest.extend(write_visuals(stream))
    manifest.extend(write_agenda_extras())
    write_index(manifest)
    print(json.dumps({"streams": len(STREAMS), "assets": len(manifest)}, indent=2))


if __name__ == "__main__":
    main()
