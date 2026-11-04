#!/usr/bin/env python3
"""Generate datathon-assets copy, HTML visuals, INDEX.md (PNG/PDF via render-visuals.sh)."""
from __future__ import annotations

import argparse
import json
import shutil
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
CTH_LOGO_SRC = REPO / "decks/nexus-co2/logos/cleantechhub.png"
OPTION_A_DIR = REPO / "brand/datalab-logo-2026-11/archive/logo"
SHARED_DIR = ROOT / "_shared"
CTH_LOGO_SHARED = SHARED_DIR / "cleantechhub-logo.png"
CTH_LOGO_HTML = "../_shared/cleantechhub-logo.png"
DATALAB_OPTION_A = {
    "svg": SHARED_DIR / "datalab-option-a.svg",
    "light": SHARED_DIR / "datalab-option-a-light.png",
    "dark": SHARED_DIR / "datalab-option-a-dark.png",
}
DATALAB_HTML = {
    "svg": "../_shared/datalab-option-a.svg",
    "light": "../_shared/datalab-option-a-light.png",
    "dark": "../_shared/datalab-option-a-dark.png",
}

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


def ensure_shared_assets() -> None:
    SHARED_DIR.mkdir(parents=True, exist_ok=True)
    if CTH_LOGO_SRC.is_file():
        shutil.copy2(CTH_LOGO_SRC, CTH_LOGO_SHARED)
    if OPTION_A_DIR.is_dir():
        shutil.copy2(OPTION_A_DIR / "option-a.svg", DATALAB_OPTION_A["svg"])
        shutil.copy2(OPTION_A_DIR / "option-a-light.png", DATALAB_OPTION_A["light"])
        shutil.copy2(OPTION_A_DIR / "option-a-dark.png", DATALAB_OPTION_A["dark"])


def datalab_logo_img(variant: str = "dark", height: int = 72) -> str:
    """Option A grid mark (+ wordmark in PNG). dark = on deep fields; light = on pale fields."""
    src = DATALAB_HTML[variant if variant in DATALAB_HTML else "dark"]
    width = int(height * (480 / 120))
    return (
        f'<img class="datalab-logo" src="{src}" height="{height}" '
        f'width="{width}" alt="Datalab" />'
    )


def cth_logo_img(height: int = 52) -> str:
    return (
        f'<img class="cth-logo" src="{CTH_LOGO_HTML}" width="{int(height * 3.8)}" '
        f'height="{height}" alt="CleantechHUB" />'
    )


def partner_placeholders(compact: bool = False) -> str:
    air = "[LOGO AIR4U]" if not compact else "AIR4U"
    ext = "[LOGO EXTERNADO]" if not compact else "EXTERNADO"
    return f"""
    <div class="ph partner">{air}</div>
    <div class="ph partner">{ext}</div>
    """


def logo_footer(linkedin: bool = False) -> str:
    cth_h = 44 if linkedin else 52
    return f"""
    <div class="logo-footer">
      {partner_placeholders()}
      <div class="logo-cth">{cth_logo_img(cth_h)}</div>
    </div>
    """


def base_css(width: int, height: int) -> str:
    return f"""
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&family=Titillium+Web:wght@700&display=swap');
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{
      width: {width}px;
      height: {height}px;
      max-width: {width}px;
      max-height: {height}px;
      overflow: hidden;
      position: relative;
    }}
    body {{ font-family: 'Open Sans', sans-serif; color: {COLORS['deep']}; background: {COLORS['deep']}; }}
    .canvas {{
      position: absolute;
      inset: 0;
      width: {width}px;
      height: {height}px;
      overflow: hidden;
    }}
    .head {{ font-family: 'Titillium Web', sans-serif; font-weight: 700; }}
    .tag {{ color: {COLORS['forest']}; font-weight: 600; }}
    .bullet {{ line-height: 1.35; margin: 0; padding-left: 1.1em; position: relative; }}
    .bullet + .bullet {{ margin-top: 0.55em; }}
    .bullet::before {{ content: '•'; position: absolute; left: 0; color: {COLORS['forest']}; font-weight: 700; }}
    .ph {{
      border: 1.5px dashed {COLORS['deep']};
      background: {COLORS['white']};
      font-size: 11px;
      font-weight: 600;
      padding: 10px 12px;
      border-radius: 6px;
      white-space: nowrap;
    }}
    .logo-footer {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 12px;
    }}
    .logo-cth {{
      background: {COLORS['white']};
      border-radius: 8px;
      padding: 6px 10px;
      margin-left: auto;
    }}
    .cth-logo {{ display: block; width: auto; max-width: 100%; object-fit: contain; }}
    .datalab-logo {{ display: block; width: auto; max-width: 100%; object-fit: contain; }}

    /* LinkedIn 1200×627 */
    .layout-linkedin {{ display: flex; height: 100%; align-items: stretch; }}
    .layout-linkedin .sidebar {{
      width: 34%;
      background: {COLORS['deep']};
      color: {COLORS['white']};
      padding: 28px 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      align-self: stretch;
    }}
    .layout-linkedin .main {{
      flex: 1;
      min-height: 100%;
      background: {COLORS['cyan']};
      padding: 24px 32px 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      align-self: stretch;
    }}
    .layout-linkedin .main-top {{
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 12px;
      padding-bottom: 8px;
    }}
    .layout-linkedin .main-top h1 {{ font-size: 50px; line-height: 1.05; }}
    .layout-linkedin .main-top .sub {{ font-size: 26px; font-weight: 600; }}
    .layout-linkedin .bullet {{ font-size: 21px; }}
    .layout-linkedin .main-bottom .tag {{ font-size: 20px; margin-bottom: 12px; }}
    .layout-linkedin .sidebar .side-note {{
      font-size: 15px; line-height: 1.45; opacity: 0.92; margin-top: 20px;
    }}

    /* Instagram feed 1080×1350 */
    .layout-feed {{ display: flex; flex-direction: column; height: 100%; }}
    .layout-feed .feed-top {{
      flex: 1;
      background: {COLORS['deep']};
      color: {COLORS['white']};
      padding: 48px 44px 36px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 16px;
    }}
    .layout-feed .feed-top h1 {{ font-size: 54px; line-height: 1.05; }}
    .layout-feed .feed-top .sub {{ font-size: 26px; font-weight: 600; color: {COLORS['cyan']}; }}
    .layout-feed .feed-bottom {{
      flex: 1.08;
      min-height: 0;
      background: {COLORS['cyan']};
      display: flex;
      flex-direction: column;
      padding: 0;
    }}
    .layout-feed .card {{
      background: {COLORS['white']};
      border-radius: 14px;
      margin: 28px 40px 0;
      padding: 34px 30px;
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-evenly;
    }}
    .layout-feed .logo-bar {{
      margin-top: auto;
      padding: 22px 40px 26px;
      background: rgba(255, 255, 255, 0.45);
      border-top: 3px solid rgba(12, 73, 138, 0.12);
    }}
    .layout-feed .bullet {{ font-size: 26px; }}

    /* Story 1080×1920 */
    .layout-story {{
      background: {COLORS['deep']};
      color: {COLORS['white']};
      height: 100%;
      padding: 64px 48px 56px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .layout-story header .datalab-logo {{ margin-bottom: 22px; }}
    .layout-story .badge {{
      background: {COLORS['sky']};
      color: {COLORS['deep']};
      display: inline-block;
      padding: 10px 18px;
      border-radius: 999px;
      font-weight: 600;
      font-size: 24px;
    }}
    .layout-story h1 {{ font-size: 62px; line-height: 1.05; margin-top: 28px; }}
    .layout-story .sub {{ font-size: 28px; margin-top: 14px; opacity: 0.95; font-weight: 600; }}
    .layout-story .story-mid {{
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-evenly;
      padding: 20px 0 28px;
    }}
    .layout-story .bullet {{ font-size: 30px; color: {COLORS['white']}; }}
    .layout-story .bullet::before {{ color: {COLORS['green']}; }}
    .layout-story .story-tag {{ font-size: 26px; color: {COLORS['green']}; font-weight: 600; margin-bottom: 16px; }}
    .layout-story .ph {{ color: {COLORS['deep']}; }}
    .layout-story .logo-bar {{
      padding-top: 8px;
      border-top: 2px solid rgba(255,255,255,0.18);
    }}
    """


def visual_html(stream: dict, width: int, height: int, layout: str) -> str:
    bullets_html = "".join(f'<p class="bullet">{b}</p>' for b in stream["bullets"][:4])
    if layout == "linkedin":
        datalab = datalab_logo_img("dark", 78)
        inner = f"""
        <div class="canvas layout-linkedin">
          <aside class="sidebar">
            <div>
              {datalab}
              <p class="side-note">{BRAND_LINE}<br/>{EVENT_SHORT}</p>
            </div>
          </aside>
          <main class="main">
            <div class="main-top">
              <h1 class="head">{stream['headline']}</h1>
              <p class="sub">{stream['sub']}</p>
              {bullets_html}
            </div>
            <div class="main-bottom">
              <p class="tag">Inspira. Actúa. Transforma.</p>
              {logo_footer(linkedin=True)}
            </div>
          </main>
        </div>
        """
    elif layout == "feed":
        datalab = datalab_logo_img("dark", 86)
        inner = f"""
        <div class="canvas layout-feed">
          <section class="feed-top">
            {datalab}
            <h1 class="head">{stream['headline']}</h1>
            <p class="sub">{stream['sub']}</p>
          </section>
          <section class="feed-bottom">
            <div class="card">{bullets_html}</div>
            <div class="logo-bar">{logo_footer()}</div>
          </section>
        </div>
        """
    else:
        datalab = datalab_logo_img("dark", 92)
        inner = f"""
        <div class="canvas layout-story">
          <header>
            {datalab}
            <span class="badge">{EVENT_SHORT}</span>
            <h1 class="head">{stream['headline']}</h1>
            <p class="sub">{stream['sub']}</p>
          </header>
          <div class="story-mid">{bullets_html}</div>
          <footer class="logo-bar">
            <p class="story-tag">{BRAND_LINE}</p>
            {logo_footer()}
          </footer>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<title>{stream['id']} {layout}</title>
<style>{base_css(width, height)}</style>
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
html, body {{
  width: 900px;
  height: 1200px;
  max-width: 900px;
  max-height: 1200px;
  overflow: hidden;
  margin: 0;
}}
body {{
  font-family: 'Open Sans', sans-serif;
  color: {COLORS['text']};
  padding: 44px 48px 36px;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}}
h1 {{ font-family: 'Titillium Web', sans-serif; color: {COLORS['cth_primary']}; font-size: 36px; }}
.sub {{ color: {COLORS['cth_dark']}; margin: 10px 0 22px; font-size: 16px; line-height: 1.45; }}
.table-wrap {{ flex: 1; display: flex; flex-direction: column; justify-content: space-evenly; }}
table {{ width: 100%; border-collapse: collapse; font-size: 15px; }}
td {{ border-bottom: 1px solid #ccc; padding: 20px 8px; vertical-align: top; line-height: 1.45; font-size: 16px; }}
td:first-child {{ width: 110px; font-weight: 600; color: {COLORS['deep']}; }}
.logos {{ margin-top: 8px; display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }}
.ph {{ border: 1px dashed {COLORS['deep']}; padding: 8px; font-size: 11px; }}
.logo-cth {{ background: #fff; border-radius: 8px; padding: 6px 10px; margin-left: auto; }}
.cth-logo {{ height: 52px; width: auto; display: block; }}
</style>
</head>
<body>
<h1>Agenda · Observatorio de la Tierra</h1>
<p class="sub">{EVENT_DATE} · {BRAND_LINE}<br/>Sede: PENDIENTE · Hora de inicio: PENDIENTE</p>
<div class="table-wrap"><table>{rows}</table></div>
<div class="logos">
  <div class="ph">[LOGO AIR4U] · socio de innovación</div>
  <div class="ph">[LOGO EXTERNADO]</div>
  <div class="logo-cth">{cth_logo_img(48)}</div>
</div>
</body>
</html>
"""


def write_visuals(stream: dict) -> list[dict]:
    ensure_shared_assets()
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
    ensure_shared_assets()
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
            f"**Kit logo:** `brand/datalab-logo-2026-11/archive/logo/option-a.*` (Option A grid).",
            "",
            "## WhatsApp kit",
            "",
            "`datathon-kit.zip` — PNGs + `copy.txt` per stream, `agenda-evento.pdf` en la raíz. Regenerar: `scripts/build-kit-zip.sh` (después de `build_assets.py` + `render-visuals.sh`).",
        ]
    )
    (ROOT / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--visuals-only",
        action="store_true",
        help="Regenerate HTML visuals and agenda print only (do not touch copy files).",
    )
    args = parser.parse_args()

    manifest: list[dict] = []
    for stream in STREAMS:
        if not args.visuals_only:
            write_copy(stream)
        manifest.extend(write_visuals(stream))
    manifest.extend(write_agenda_extras())
    if not args.visuals_only:
        write_index(manifest)
    print(json.dumps({"streams": len(STREAMS), "assets": len(manifest)}, indent=2))


if __name__ == "__main__":
    main()
