#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CHROME="${CHROME:-google-chrome-stable}"
shopt -s nullglob

render_png() {
  local html="$1" out="$2" w="$3" h="$4"
  "$CHROME" --headless=new --no-sandbox --disable-gpu \
    --force-device-scale-factor=1 \
    --hide-scrollbars \
    --window-size="${w},${h}" \
    --screenshot="$out" \
    --run-all-compositor-stages-before-draw \
    --virtual-time-budget=5000 \
    "file://${html}" 2>/dev/null || true
  if [[ ! -s "$out" ]]; then
    echo "FAIL png: $out" >&2
    exit 1
  fi
  python3 - <<PY
import struct
with open("$out", "rb") as f:
    f.seek(16)
    w, h = struct.unpack(">II", f.read(8))
print("$out", w, h)
assert (w, h) == ($w, $h), (w, h)
PY
}

render_pdf() {
  local html="$1" out="$2"
  "$CHROME" --headless --no-sandbox --disable-gpu \
    --print-to-pdf="$out" --no-pdf-header-footer \
    "file://${html}" 2>/dev/null || true
  [[ -s "$out" ]] || { echo "FAIL pdf: $out" >&2; exit 1; }
}

for html in "$ROOT"/*/*.html; do
  base="${html%.html}"
  name="$(basename "$base")"
  if [[ "$name" == "agenda-print-a4" ]]; then
    render_png "$html" "${base}.png" 900 1200
    render_pdf "$html" "${base}.pdf"
    continue
  fi
  if [[ "$name" == linkedin-* ]]; then
    render_png "$html" "${base}.png" 1200 627
  elif [[ "$name" == instagram-feed-* ]]; then
    render_png "$html" "${base}.png" 1080 1350
  elif [[ "$name" == story-* ]]; then
    render_png "$html" "${base}.png" 1080 1920
  fi
done

echo "Render complete."
