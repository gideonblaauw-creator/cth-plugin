#!/usr/bin/env python3
"""Generate index.html for Datatón preguntas por espacio (17 pages)."""
from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "index.html"

from spaces import SPACES  # noqa: E402

def esc(s: str) -> str:
    return html.escape(s, quote=True)


def turn_html(turns: list[tuple[str, str, str]]) -> str:
    parts = []
    for p, a, r in turns:
        parts.append(
            f'<div class="turn"><p class="pregunta">Pregunta: {esc(p)}</p>'
            f'<p class="anticipada">[{esc(a)}]</p>'
            f'<p class="repregunta">Repregunta: {esc(r)}</p></div>'
        )
    return "\n".join(parts)


def space_page(sp: dict, n: int) -> str:
    nota = sp.get("nota", "").strip()
    nota_html = (
        f'<p class="nota-moderacion"><span class="nota-label">Nota para moderación:</span> {esc(nota)}</p>'
        if nota
        else ""
    )
    return f"""<section class="page page--space" id="p{n:02d}" data-page="{n}">
  <header class="page-head">
    <div class="title-block">
      <span class="time-badge">{esc(sp['time'])}</span>
      <h1>{esc(sp['title'])}</h1>
      <p class="meta-row"><strong>Participan:</strong> {esc(sp['participants'])}</p>
      <p class="meta-row"><strong>Quién pregunta:</strong> {esc(sp['asks'])}</p>
    </div>
    <img class="logo" src="assets/cth-logo.png" alt="CleantechHUB">
  </header>
  <div class="strip-row">
    <div class="strip"><div class="label">Viene de</div>{esc(sp['viene'])}</div>
    <div class="strip"><div class="label">Lleva a</div>{esc(sp['lleva'])}</div>
  </div>
  <div class="page-main">
    <div class="turns">
      {turn_html(sp['turns'])}
    </div>
    {nota_html}
  </div>
  <div class="page-foot">
    <p class="puente"><strong>Puente</strong>{esc(sp['puente'])}</p>
    <p class="fuente">{esc(sp['fuente'])}</p>
  </div>
</section>"""


THREAD_HTML = """
<div class="thread-grid">
  <div class="thread-col">
    <h3>Paisaje a programa</h3>
    <span class="thread-pill">08:30 Palabras de apertura</span>
    <span class="thread-pill">08:40 Panel ODS 13</span>
    <span class="thread-pill thread-pill--prog">09:10 Observatorio y Datalab</span>
    <span class="thread-pill">09:40 Conversatorio régimen corporativo</span>
    <span class="thread-pill">09:55 Digitalización (Agrometers)</span>
    <h3 style="margin-top:2mm">Nicho y método</h3>
    <span class="thread-pill thread-pill--nicho">10:05 Air4U presentación</span>
    <span class="thread-pill thread-pill--nicho">10:10 Demo capas en vivo</span>
    <span class="thread-pill thread-pill--nicho">10:20 Air4U y adoptante</span>
    <span class="thread-pill thread-pill--work">10:45 Instrucciones y mentores</span>
    <span class="thread-pill thread-pill--work">11:00 Bloque 1 con monitores</span>
    <span class="thread-pill">12:30 Almuerzo y mesa hélice</span>
    <span class="thread-pill thread-pill--work">13:30 Bloque 2 y pitch</span>
    <span class="thread-pill thread-pill--prog">16:00 Pitches (6 equipos)</span>
    <span class="thread-pill">16:40 Deliberación jurado</span>
    <span class="thread-pill thread-pill--prog">16:50 Cierre y certificados</span>
  </div>
  <div class="thread-col">
    <h3>Lentes MLP</h3>
    <article class="thread-note"><strong>Paisaje</strong>Presiones territoriales y cooperación (panel).</article>
    <article class="thread-note"><strong>Programa</strong>Observatorio, Carapulica y motor Datalab.</article>
    <article class="thread-note"><strong>Régimen</strong>Constructora Bolívar como adoptante potencial, sin piloto firmado.</article>
    <article class="thread-note"><strong>Sector</strong>Agrometers: competitividad y trazabilidad exportable.</article>
    <article class="thread-note"><strong>Nicho</strong>Air4U: lente urbana, hacer visible lo invisible.</article>
    <article class="thread-note"><strong>Método</strong>Bronce, Plata, Oro = confianza del dato.</article>
    <article class="thread-note"><strong>Equipos</strong>Catorce equipos: lienzo, mapa, tablero, pitch.</article>
    <article class="thread-note"><strong>Selección</strong>Embudo a seis finalistas y tres ganadores 2027.</article>
    <article class="thread-note"><strong>Vuelta macro</strong>Fase piloto del Observatorio y Earth Data Week.</article>
  </div>
</div>
<p class="thread-macro">Hilo: paisaje y territorio, programa Observatorio y Datalab, régimen corporativo, sector digital, nicho Air4U, método con equipos, selección y regreso al motor en 2027.</p>
"""


COVER = """<section class="page page--cover" id="p01" data-page="1">
  <div class="cover-bg"></div>
  <div class="cover-scrim"></div>
  <img class="logo" src="assets/cth-logo.png" alt="CleantechHUB">
  <div class="cover-inner">
    <p class="tagline">OBSERVA. ACTÚA. TRANSFORMA.</p>
    <h1>Datatón · preguntas por espacio</h1>
    <p class="cover-meta">Martes 24 de noviembre de 2026<br>Universidad Externado de Colombia · Auditorio Bloque I</p>
    <p class="cover-meta" style="margin-top:6mm;font-size:9.5pt;opacity:.9">Documento interno de preparación para moderación y jurado</p>
  </div>
</section>"""

THREAD_PAGE = f"""<section class="page page--thread" id="p02" data-page="2">
  <header class="page-head">
    <div class="title-block">
      <h1>Hilo conductor del día</h1>
      <p class="meta-row">De paisaje y territorio al nicho Air4U, método con equipos y vuelta al Observatorio y Datalab 2027.</p>
    </div>
    <img class="logo" src="assets/cth-logo.png" alt="CleantechHUB">
  </header>
  <div class="diagram-wrap">
    {THREAD_HTML}
  </div>
  <p class="fuente">Fuente: agenda v7, síntesis contexto 23 nov</p>
</section>"""


def main() -> None:
    css = (ROOT / "deck.css").read_text(encoding="utf-8")
    space_sections = "\n".join(space_page(sp, i + 3) for i, sp in enumerate(SPACES))
    doc = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Datatón · preguntas por espacio</title>
  <style>
{css}
  </style>
</head>
<body class="print-mode">
{COVER}
{THREAD_PAGE}
{space_sections}
</body>
</html>
"""
    OUT.write_text(doc, encoding="utf-8")
    print(f"Wrote {OUT} ({len(SPACES) + 2} pages)")


if __name__ == "__main__":
    main()