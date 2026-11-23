#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
REVEAL="$(cd "$ROOT/../../tools/reveal" && pwd)"
export PUPPETEER_EXECUTABLE_PATH="${PUPPETEER_EXECUTABLE_PATH:-/usr/bin/google-chrome-stable}"
export CHROME_PATH="${CHROME_PATH:-$PUPPETEER_EXECUTABLE_PATH}"

"$REVEAL/build.sh" datathon-2026-pitch-template

HOJA="$ROOT/hojas/hoja-5-pitch-print.html"
HOJA_PDF="$ROOT/hoja-5-pitch.pdf"
CHROME="${CHROME_PATH:-/usr/bin/google-chrome-stable}"

echo "A4 PDF (hoja 5a+5b) → $HOJA_PDF"
if "$CHROME" --headless --disable-gpu --no-sandbox --print-to-pdf="$HOJA_PDF" \
  --no-pdf-header-footer \
  "file://$HOJA" 2>/dev/null; then
  :
elif python3 "$ROOT/scripts/print-hoja-pdf.py"; then
  :
else
  echo "warning: hoja PDF export failed" >&2
  exit 1
fi

node "$ROOT/export-artifacts.mjs"