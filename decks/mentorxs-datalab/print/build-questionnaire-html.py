#!/usr/bin/env python3
"""Emit part3-cuestionario.html from part3-google-forms-question-list.md (labels 1–55)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
items = []
for line in (ROOT / "part3-google-forms-question-list.md").read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    if line[0].isdigit() and ". " in line:
        items.append(line.split(". ", 1)[1])

assert len(items) == 55, len(items)

CSS = """
@page { size: A4; margin: 0; }
@font-face {
  font-family: "Open Sans";
  src: url("../assets/fonts/open-sans-latin-400-normal.woff2") format("woff2");
  font-weight: 400;
}
@font-face {
  font-family: "Open Sans";
  src: url("../assets/fonts/open-sans-latin-600-normal.woff2") format("woff2");
  font-weight: 600;
}
@font-face {
  font-family: "Open Sans";
  src: url("../assets/fonts/open-sans-latin-700-normal.woff2") format("woff2");
  font-weight: 700;
}
html, body { margin: 0; padding: 0; font-family: "Open Sans", sans-serif; font-size: 8.75pt; color: #0C498A; }
h1, h2, label { font-family: "Open Sans", sans-serif; font-weight: 400; }
h1, h2 { font-size: 13pt; text-transform: uppercase; letter-spacing: 0.04em; }
.letter-page {
  position: relative;
  min-height: 297mm;
  box-sizing: border-box;
  padding: 40mm 13mm 26mm 13mm;
  page-break-after: always;
  background-image: url("letterhead/CTH_header.png"), url("letterhead/CTH_footer.png");
  background-position: left top, left bottom;
  background-size: 100% auto, 100% auto;
  background-repeat: no-repeat;
}
.letter-page:last-child { page-break-after: auto; }
.addr {
  position: fixed;
  left: 13mm;
  right: 13mm;
  bottom: 5.5mm;
  font-size: 8pt;
  color: #0C498A;
  z-index: 2;
  line-height: 1.2;
}
h1 { font-size: 13pt; margin: 0 0 3mm; }
h2 { font-size: 10pt; margin: 3mm 0 1.5mm; border-bottom: 1px solid #B2EEFA; }
.field { margin: 0 0 2.2mm; }
.field label { display: block; font-weight: 700; margin-bottom: 0.5mm; }
.line { border-bottom: 1px solid #69B5FA; min-height: 5mm; }
.line.tall { min-height: 7mm; }
.note { font-size: 8pt; margin: 0 0 2mm; }
.cb { display: inline-block; width: 3.5mm; height: 3.5mm; border: 1px solid #0C498A; margin-right: 1.5mm; vertical-align: middle; }
.small { font-size: 7.5pt; color: #669348; margin-top: 2mm; }
"""

# Page splits: 1-13, 14-29, 30-42, 43-55
splits = [(0, 13), (13, 29), (29, 42), (42, 55)]
titles = [
    "Cuestionario Parte 3 — Tarjeta valor + juzgamiento finales",
    None,
    None,
    "Hoja finales — mentor / juez (cont.)",
]

def field_html(n: int, text: str) -> str:
    label = f"{n}. {text}"
    if n == 29:
        return (
            f'<div class="field"><label>{label}</label>'
            f'<p><span class="cb"></span> No &nbsp; <span class="cb"></span> Sí</p></div>'
        )
    if n == 41:
        return (
            f'<div class="field"><label>{label}</label>'
            f'<p><span class="cb"></span> S &nbsp; <span class="cb"></span> N</p></div>'
        )
    if 30 <= n <= 34:
        return f'<p><span class="cb"></span> {label}</p>'
    tall = n in (4, 26, 39)
    cls = "line tall" if tall else "line"
    return f'<div class="field"><label>{label}</label><div class="{cls}"></div></div>'

pages = []
for idx, (start, end) in enumerate(splits):
    chunk = items[start:end]
    parts = ['<div class="letter-page">']
    if idx == 0:
        parts.append(
            f"<h1>{titles[0]}</h1>"
            '<p class="note">Metodología v0.3.1 · Solo Parte 3 · Imprimir y llenar a mano. '
            "Mismas preguntas que part3-google-forms-question-list.md. "
            "Herramienta en línea por defecto: Google Forms; alternativas Tally, LimeSurvey.</p>"
        )
        parts.append("<h2>Bloque A — Tarjeta datos → valor (Q3)</h2>")
    elif idx == 3:
        parts.append(f"<h2>{titles[3]}</h2>")
    elif idx == 2:
        parts.append("<h2>Bloque B — Hoja finales</h2>")
    for i, text in enumerate(chunk):
        qnum = start + i + 1
        parts.append(field_html(qnum, text))
    if idx == 3:
        parts.append(
            '<p class="small">Desempate: si el total empata, ordenar con Parte B (honestidad) antes que Parte A '
            "(finals-judging-sheet.md v0.3.1, Combined score). Ítem 55 solo si A y B también empatan.</p>"
        )
    parts.append("</div>")
    pages.append("\n".join(parts))

html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <title>Cuestionario Parte 3 — Datatón</title>
  <style>{CSS}</style>
</head>
<body>
<div class="addr">Fundación CleantechHUB · NIT 901.523.941-9 · Cl 90 No. 19-41 Of 801, Bogotá, Colombia<br />
www.cleantechhub.net · +57 313 715 5965</div>
{"".join(pages)}
</body>
</html>
"""
(ROOT / "part3-cuestionario.html").write_text(html, encoding="utf-8")
print("wrote", ROOT / "part3-cuestionario.html")