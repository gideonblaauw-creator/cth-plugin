#!/usr/bin/env bash
# Rebuild datathon-kit.zip for WhatsApp sharing (~15 MB cap).
# Includes PNGs + copy.txt per stream; agenda PDF at zip root. No INDEX or desk markdown.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT_ZIP="$ROOT/datathon-kit.zip"
MAX_BYTES=$((15 * 1024 * 1024))
STAGING="$(mktemp -d)"
trap 'rm -rf "$STAGING"' EXIT

STREAMS=(
  01-agenda
  02-earth-observatory
  03-datalab
  04-datathon
  05-air4u-demo
)

AGENDA_PDF="$ROOT/01-agenda/agenda-print-a4.pdf"
if [[ ! -f "$AGENDA_PDF" ]]; then
  echo "Missing $AGENDA_PDF — run render-visuals.sh first." >&2
  exit 1
fi

cp "$AGENDA_PDF" "$STAGING/agenda-evento.pdf"

for stream in "${STREAMS[@]}"; do
  src="$ROOT/$stream"
  dest="$STAGING/$stream"
  [[ -d "$src" ]] || { echo "Missing stream folder: $src" >&2; exit 1; }
  mkdir -p "$dest"
  [[ -f "$src/copy.txt" ]] || { echo "Missing $src/copy.txt — run build_assets.py first." >&2; exit 1; }
  cp "$src/copy.txt" "$dest/"
  shopt -s nullglob
  for png in "$src"/*.png; do
    cp "$png" "$dest/"
  done
done

rm -f "$OUT_ZIP"
(
  cd "$STAGING"
  zip -9 -r "$OUT_ZIP" .
)

size=$(stat -c%s "$OUT_ZIP")
echo "Created $OUT_ZIP ($size bytes)"
if (( size > MAX_BYTES )); then
  echo "WARNING: zip exceeds 15 MB WhatsApp-friendly limit ($size > $MAX_BYTES)" >&2
  exit 1
fi

unzip -l "$OUT_ZIP"
