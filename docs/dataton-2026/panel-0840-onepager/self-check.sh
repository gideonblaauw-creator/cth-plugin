#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
export PATH="/tmp/poppler-extract/usr/bin:${PATH:-}"
export LD_LIBRARY_PATH="/tmp/poppler-extract/usr/lib/x86_64-linux-gnu:${LD_LIBRARY_PATH:-}"
PDF="$ROOT/Panel-0840-Dataton-24nov.pdf"
TICKET="$ROOT/ticket-content.txt"
OUT="$ROOT/self-check-output.txt"

mkdir -p "$ROOT"

cat > "$TICKET" <<'TICKET_EOF'
Panel: Innovación y emprendimiento en el territorio a través de los datos (ODS 13)
Martes 24 de noviembre de 2026, de 08:40 a 09:10 (30 minutos)
Universidad Externado de Colombia, Auditorio del Bloque I, piso 2 (Av. Circunvalar No. 12B-54)

El panel abre el Datatón y el lanzamiento suave del Observatorio de la Tierra. Catorce equipos de estudiantes pasarán el día trabajando con datos de sus territorios, y este panel les da el punto de partida: cómo el emprendimiento local puede ofrecer soluciones a desafíos climáticos concretos, como inundaciones, erosión costera, agua o calidad del aire.

Participan
- Natalia Vargas, APC-Colombia
- Rector de la Universidad Externado
- Viviana Obando, RAP Pacífico
- Modera: Gideon Blaauw, CleantechHUB

Formato
Conversación moderada. Cada panelista recibe una o dos preguntas y una repregunta. Les pedimos respuestas cortas, de uno a dos minutos, con un ejemplo real del territorio. Cerramos con una ronda en la que cada uno nombra en una frase el desafío climático que le entregaría hoy a los equipos.

Preguntas guía
- Natalia: desde la cooperación, ¿qué desafío climático en los territorios ya están apoyando con soluciones, y dónde puede entrar un emprendedor local?
- Viviana: en el Pacífico, ¿qué problema climático resuelve o podría resolver un emprendimiento local?
- Rector: ¿qué puede ofrecer en concreto la universidad a quien emprende frente a un problema climático?
- Natalia y Viviana: ¿por qué esa solución debería salir de un emprendedor del territorio y no solo de un programa público?
- Todos: en una frase, ¿qué desafío climático le entregarían hoy a los equipos?

A las 09:10, justo después del panel, presentamos el Observatorio de la Tierra y el Datalab: cómo poner datos a estos desafíos.
TICKET_EOF

{
  echo "=== pdfinfo ==="
  pdfinfo "$PDF"
  echo ""
  echo "=== pdffonts ==="
  pdffonts "$PDF"
  echo ""
  echo "=== banned terms ==="
  pdftotext "$PDF" - | rg -n 'Óscar|Apix|gratis' || echo "(none)"
  echo ""
  echo "=== text diff (whitespace-normalised) ==="
  python3 "$ROOT/text-diff.py"
  echo ""
  echo "=== glyph scan ==="
  python3 "$ROOT/glyph-scan.py"
  echo ""
  echo "=== computed font sizes ==="
  python3 "$ROOT/check-font-sizes.py"
} | tee "$OUT"