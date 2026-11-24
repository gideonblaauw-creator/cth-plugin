#!/usr/bin/env python3
"""Assemble Guia-tecnica-mentores.pdf from styled front matter + dist hoja PDFs."""
from __future__ import annotations

import asyncio
import re
import tempfile
from pathlib import Path

import fitz
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parent.parent
GUIA_DIR = Path(__file__).resolve().parent
DIST = ROOT / "dist"
OUT_PDF = GUIA_DIR / "Guia-tecnica-mentores.pdf"
FONT_REG = ROOT / "fonts/open-sans/OpenSans-Regular.ttf"
RUN_HEADER = "Guía técnica · solo mentores"
LOGO = ROOT / "assets/cth-logo-color.png"

HOJA_PDFS = (
    "hoja-1-mapa-de-calor.pdf",
    "hoja-2-flujo-de-datos.pdf",
    "hoja-3-dato-a-valor.pdf",
    "hoja-4-plantilla-tablero.pdf",
    "hoja-4b-ejemplo-air4u.pdf",
    "hoja-5-plantilla-pitch.pdf",
    "prompts-ia-v2.pdf",
)

M1_LEVEL_LINES = (
    "ninguno: el dato está solo en chats o en la memoria, sin permiso o sin poder descargarlo. "
    "Empezar aquí es normal.",
    "bronce: guardado en un lugar con responsable, con permiso escrito y se puede descargar como archivo.",
    "plata: limpio, con reglas de limpieza escritas y calidad revisada.",
    "oro: listo para una decisión y un público con nombre.",
)

M6_BULLETS = [
    "Puntaje del mentor: utilidad 0–5 más honestidad 0–5, más 1 por cada número firme en plata u oro (máximo +3). "
    "En empate gana honestidad.",
    "Los mentores contrastan 2–3 números con la carpeta del equipo en Drive.",
    "Las finales a las 16:00 usan las mismas dos notas (utilidad, honestidad). "
    "Si hay empate, gana la mayor nota de honestidad.",
    "14 equipos › 6 finalistas › 3 ganadores, quienes entran al Datalab CTH en 2027. "
    "Todos reciben certificado.",
    "Ningún equipo queda fuera después del Bloque 1: las etiquetas advierten, no excluyen.",
    "La lista de los 6 finalistas se anuncia antes de las 16:00.",
]

INDEX_LINES = [
    "1. Niveles de confianza del dato (metodología v0.3)",
    "2. Cómo elegimos los 6 y cómo decide el jurado",
    "3. Hoja 1 — mapa de calor",
    "4. Hoja 2 — flujo de datos",
    "5. Hoja 3 — dato a valor",
    "6. Hoja 4 — plantilla tablero",
    "7. Hoja 4b — ejemplo Air4U",
    "8. Hoja 5 — plantilla pitch",
    "9. Prompts IA v2 — rúbrica de puntuación",
]


def _front_matter_html() -> str:
  import html

  logo_uri = LOGO.as_uri()
  m1_items = "".join(f"<p>{html.escape(line)}</p>" for line in M1_LEVEL_LINES)
  m6_items = "".join(f"<p>• {html.escape(item)}</p>" for item in M6_BULLETS)
  idx_items = "".join(f"<p>{html.escape(line)}</p>" for line in INDEX_LINES)
  css_uri = (ROOT / "print" / "guia-front-print.css").as_uri()
  return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <title>Guía técnica para mentores</title>
  <link rel="stylesheet" href="{css_uri}" />
</head>
<body>
  <section class="guia-page cover">
    <header class="hdr-bar">
      <img src="{logo_uri}" alt="CleantechHUB" />
      <span>Datatón v0.4-es</span>
    </header>
    <h1 class="cover-title">Guía técnica para mentores</h1>
    <p class="cover-badge">Solo mentores</p>
    <p class="cover-date">Datatón 24 nov 2026</p>
    <p class="cover-lead">Compilación de las hojas metodológicas y la rúbrica de prompts IA. Documento de trabajo para mentores del Datatón.</p>
  </section>
  <section class="guia-page index">
    <h1>Índice</h1>
    {idx_items}
  </section>
  <section class="guia-page section">
    <h1>Niveles de confianza del dato</h1>
    <p>Use esta redacción con los equipos. Son niveles de confianza, no premios.</p>
    {m1_items}
  </section>
  <section class="guia-page section">
    <h1>Cómo elegimos los 6 y cómo decide el jurado</h1>
    {m6_items}
  </section>
</body>
</html>"""


async def _render_front_matter_pdf(dest: Path) -> None:
  from playwright.async_api import async_playwright

  html_text = _front_matter_html()
  with tempfile.TemporaryDirectory() as td:
    html_path = Path(td) / "guia-front.html"
    html_path.write_text(html_text, encoding="utf-8")
    async with async_playwright() as p:
      browser = await p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
      page = await browser.new_page()
      await page.goto(html_path.as_uri(), wait_until="networkidle")
      await page.pdf(
        path=str(dest),
        format="A4",
        margin={"top": "16mm", "bottom": "14mm", "left": "12mm", "right": "12mm"},
        print_background=True,
      )
      await browser.close()


def _merge_pdfs(parts: list[Path], dest: Path) -> int:
  writer = PdfWriter()
  pages = 0
  for part in parts:
    reader = PdfReader(str(part))
    for page in reader.pages:
      writer.add_page(page)
      pages += 1
  dest.parent.mkdir(parents=True, exist_ok=True)
  with dest.open("wb") as fh:
    writer.write(fh)
  return pages


def _stamp_running_header(pdf_path: Path) -> None:
  doc = fitz.open(pdf_path)
  color = (12 / 255, 73 / 255, 138 / 255)
  for i, page in enumerate(doc):
    rect = page.rect
    page.insert_text(
      (36, 22),
      RUN_HEADER,
      fontsize=7.5,
      fontfile=str(FONT_REG),
      color=color,
    )
    num = str(i + 1)
    tw = fitz.get_text_length(num, fontname="helv", fontsize=8)
    page.insert_text(
      (rect.width - 36 - tw, rect.height - 22),
      num,
      fontsize=8,
      fontfile=str(FONT_REG),
      color=color,
    )
  stamped = pdf_path.with_name(pdf_path.stem + ".stamped.pdf")
  doc.save(stamped)
  doc.close()
  stamped.replace(pdf_path)


def verify_sections(pdf_path: Path) -> int:
  doc = fitz.open(pdf_path)
  text = re.sub(r"\s+", " ", " ".join(p.get_text() for p in doc))
  markers = [
    "Hoja 1 — Mapa de calor de datos",
    "Hoja 2 — Flujo que genera datos",
    "Hoja 3 — De dato a valor",
    "Hoja 4 — Plantilla de tablero",
    "Hoja 4b — Ejemplo Air4U (relleno)",
    "Hoja 5 — Plantilla pitch",
    "Prompts de IA para el Datatón",
  ]
  pos = 0
  for title in markers:
    idx = text.find(title, pos)
    if idx < 0:
      doc.close()
      raise SystemExit(f"PDF section missing: {title}")
    pos = idx + len(title)
  n = doc.page_count
  for page in doc:
    if RUN_HEADER not in page.get_text():
      doc.close()
      raise SystemExit("Running header missing on at least one PDF page")
    if "no distribuir" in page.get_text().lower():
      doc.close()
      raise SystemExit("Banned phrase in PDF: 'no distribuir'")
  doc.close()
  return n


async def build_guia_pdf_async() -> int:
  for name in HOJA_PDFS:
    p = DIST / name
    if not p.is_file():
      raise FileNotFoundError(f"Missing dist PDF for guía merge: {p}")

  with tempfile.TemporaryDirectory() as td:
    front = Path(td) / "guia-front.pdf"
    merged = Path(td) / "guia-merged.pdf"
    await _render_front_matter_pdf(front)
    parts = [front, *[DIST / n for n in HOJA_PDFS]]
    _merge_pdfs(parts, merged)
    _stamp_running_header(merged)
    OUT_PDF.write_bytes(merged.read_bytes())

  pages = verify_sections(OUT_PDF)
  print("guia_styled_pdf", OUT_PDF, "pages", pages)
  return pages


def build_guia_pdf() -> int:
  return asyncio.run(build_guia_pdf_async())


if __name__ == "__main__":
  raise SystemExit(build_guia_pdf())