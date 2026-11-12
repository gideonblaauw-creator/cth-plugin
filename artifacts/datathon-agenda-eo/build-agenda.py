#!/usr/bin/env python3
"""Build agenda-24nov-eo HTML, PDF, and PNG preview (one A4 page)."""
from __future__ import annotations

import asyncio
import base64
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
OUT_HTML = ROOT / "agenda-24nov-eo.html"
OUT_PDF = ROOT / "agenda-24nov-eo.pdf"
OUT_PNG = ROOT / "agenda-24nov-eo.png"

TIMELINE = [
    ("~08:00", "Registro y bienvenida"),
    ("~08:30", "Palabras de apertura (Rector, por confirmar)"),
    ("~08:45", "Conversatorio inspiracional (Enrique Medina, Agrometers, por confirmar)"),
    ("~09:15", "Observatorio de la Tierra y piloto Bolívar (Diego Díaz, Gideon Blaauw)"),
    ("~09:45", "Panel: territorio, cooperación y datos (por confirmar)"),
    ("por confirmar", "Anuncio del Datalab: sandboxes + gobernanza de datos"),
    ("por confirmar", "Demo en vivo Air4U (10–15 min) + preguntas (~15 min)"),
    ("~10:45", "Instrucciones y arranque del datatón"),
    ("por confirmar", "Trabajo de equipos y almuerzo"),
    ("Tarde", "Pitches finales"),
    ("por confirmar", "Deliberación del jurado"),
    (
        "por confirmar",
        "Cierre: top 5 (acceso al Living Lab + mentoría CTH, paso al piloto 2027)",
    ),
]


def b64(path: pathlib.Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def timeline_rows() -> str:
    rows = []
    for time, text in TIMELINE:
        rows.append(
            f"""      <li class="tl-row avoid-break">
        <span class="tl-time">{time}</span>
        <span class="tl-text">{text}</span>
      </li>"""
        )
    return "\n".join(rows)


def html_document(logo_rev: str, logo_blue: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Datatón · Lanzamiento suave del Observatorio de la Tierra</title>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700;800&family=PT+Sans:wght@400;700&display=swap" rel="stylesheet"/>
  <style>
    :root {{
      --blue: #0C498A;
      --cyan: #B2EEFA;
      --lgreen: #9DC384;
      --green: #669348;
      --sky: #69B5FA;
      --white: #fff;
      --font: 'Open Sans', 'PT Sans', sans-serif;
    }}
    * {{ box-sizing: border-box; }}
    html, body {{
      margin: 0;
      padding: 0;
      font-family: var(--font);
      color: var(--blue);
      background: var(--white);
      -webkit-font-smoothing: antialiased;
    }}
    .sheet {{
      width: 210mm;
      min-height: 297mm;
      max-height: 297mm;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      position: relative;
      background: var(--white);
    }}
    .hero {{
      position: relative;
      background: var(--blue);
      color: #fff;
      padding: 11mm 14mm 10mm;
      overflow: hidden;
    }}
    .hero-block {{
      position: absolute;
      right: -48mm;
      top: -22mm;
      width: 95mm;
      height: 95mm;
      background: var(--green);
      transform: rotate(18deg);
      opacity: 0.88;
      border-radius: 10mm;
      z-index: 0;
    }}
    .hero-block::after {{
      content: "";
      position: absolute;
      left: -26mm;
      bottom: -12mm;
      width: 52mm;
      height: 52mm;
      background: var(--sky);
      border-radius: 8mm;
    }}
    .hero-inner {{ position: relative; z-index: 1; }}
    .hero-logos {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8mm;
      margin-bottom: 6mm;
      flex-wrap: wrap;
    }}
    .hero-logos img.eo-rev {{
      height: 11mm;
      width: auto;
      display: block;
    }}
    .partner-slot {{
      border: 1.5px dashed rgba(255,255,255,0.55);
      border-radius: 6px;
      padding: 2.5mm 4mm;
      font-size: 7pt;
      font-weight: 700;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: rgba(255,255,255,0.92);
      white-space: nowrap;
    }}
    .eyebrow {{
      text-transform: uppercase;
      letter-spacing: 0.14em;
      font-weight: 700;
      font-size: 7.5pt;
      color: var(--cyan);
      margin: 0 0 3mm;
    }}
    h1 {{
      margin: 0 0 3mm;
      font-size: 22pt;
      font-weight: 800;
      line-height: 1.12;
      max-width: 165mm;
    }}
    .subtitle {{
      margin: 0;
      font-size: 10.5pt;
      font-weight: 600;
      line-height: 1.35;
      color: var(--cyan);
      max-width: 168mm;
    }}
    .main {{
      flex: 1;
      padding: 7mm 14mm 4mm;
      display: flex;
      flex-direction: column;
      gap: 4mm;
    }}
    .agenda-head {{
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 6mm;
      border-bottom: 3px solid var(--cyan);
      padding-bottom: 2.5mm;
    }}
    .agenda-head h2 {{
      margin: 0;
      font-size: 13pt;
      font-weight: 800;
    }}
    .agenda-head .note {{
      font-size: 8pt;
      font-weight: 700;
      color: var(--green);
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}
    .timeline {{
      list-style: none;
      margin: 0;
      padding: 0;
      display: flex;
      flex-direction: column;
      gap: 2.2mm;
    }}
    .tl-row {{
      display: grid;
      grid-template-columns: 28mm 1fr;
      gap: 4mm;
      align-items: start;
      padding: 1.8mm 0;
      border-bottom: 1px solid rgba(12, 73, 138, 0.12);
    }}
    .tl-row:last-child {{ border-bottom: 0; }}
    .tl-time {{
      font-size: 8.5pt;
      font-weight: 800;
      color: var(--green);
      line-height: 1.25;
    }}
    .tl-text {{
      font-size: 9.2pt;
      font-weight: 600;
      line-height: 1.32;
    }}
    .footer {{
      margin-top: auto;
      background: var(--blue);
      color: #fff;
      padding: 5mm 14mm 6mm;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8mm;
    }}
    .tagline {{
      font-weight: 800;
      font-size: 13pt;
      color: var(--cyan);
      letter-spacing: 0.02em;
    }}
    .footer img.eo-blue {{
      height: 9mm;
      width: auto;
      display: block;
    }}
    @media print {{
      html, body {{
        width: 210mm;
        min-height: 297mm;
      }}
      body {{
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
        color-adjust: exact !important;
      }}
      .sheet {{
        max-height: none;
        page-break-after: avoid;
        page-break-inside: avoid;
      }}
      * {{
        animation: none !important;
        transition: none !important;
      }}
      @page {{
        size: A4 portrait;
        margin: 0;
      }}
    }}
  </style>
</head>
<body>
  <article class="sheet" role="document">
    <header class="hero">
      <div class="hero-block" aria-hidden="true"></div>
      <div class="hero-inner">
        <div class="hero-logos">
          <img class="eo-rev" src="data:image/png;base64,{logo_rev}" alt="Universidad Externado de Colombia · CleantechHUB · Observatorio de la Tierra"/>
          <span class="partner-slot" aria-label="Logo Air4U pendiente">Logo Air4U · pendiente</span>
        </div>
        <p class="eyebrow">Agenda · por confirmar</p>
        <h1>Datatón · Lanzamiento suave del Observatorio de la Tierra</h1>
        <p class="subtitle">Soft launch del Datalab · martes 24 de noviembre de 2026 · Universidad Externado de Colombia</p>
      </div>
    </header>
    <section class="main" aria-labelledby="agenda-title">
      <div class="agenda-head">
        <h2 id="agenda-title">Programa del día</h2>
        <span class="note">Horarios por confirmar</span>
      </div>
      <ol class="timeline">
{timeline_rows()}
      </ol>
    </section>
    <footer class="footer">
      <p class="tagline">Inspira. Actúa. Transforma.</p>
      <img class="eo-blue" src="data:image/png;base64,{logo_blue}" alt="Observatorio de la Tierra · co-brand"/>
    </footer>
  </article>
</body>
</html>
"""


async def export_pdf_png(html_path: pathlib.Path) -> None:
    from playwright.async_api import async_playwright

    url = html_path.as_uri()
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 794, "height": 1123})
        await page.goto(url, wait_until="networkidle")
        await page.pdf(
            path=str(OUT_PDF),
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            prefer_css_page_size=True,
        )
        await page.screenshot(path=str(OUT_PNG), full_page=False)
        await browser.close()


def main() -> None:
    logo_rev = b64(ASSETS / "eo-cobrand-reverse-transparent.png")
    logo_blue = b64(ASSETS / "eo-cobrand-blue-transparent.png")
    OUT_HTML.write_text(html_document(logo_rev, logo_blue), encoding="utf-8")
    asyncio.run(export_pdf_png(OUT_HTML))
    print(OUT_HTML)
    print(OUT_PDF)
    print(OUT_PNG)


if __name__ == "__main__":
    main()
