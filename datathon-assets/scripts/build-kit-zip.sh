#!/usr/bin/env bash
# Rebuild datathon-kit.zip (~15 MB target; 100 MB hard cap).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT_ZIP="$ROOT/datathon-kit.zip"
TARGET=$((15 * 1024 * 1024))
HARD=$((100 * 1024 * 1024))
STAGING="$(mktemp -d)"
trap 'rm -rf "$STAGING"' EXIT

STREAMS=(01-agenda 02-earth-observatory 03-datalab 04-datathon 05-air4u-demo)

AGENDA_PDF="$ROOT/01-agenda/agenda-print-a4.pdf"
[[ -f "$AGENDA_PDF" ]] || { echo "Missing agenda PDF; run render-comms.sh" >&2; exit 1; }
cp "$AGENDA_PDF" "$STAGING/agenda-evento.pdf"

FOTOS="$ROOT/06-fotos"
mkdir -p "$STAGING/06-fotos"
cp "$FOTOS"/*.jpg "$FOTOS/credits.txt" "$STAGING/06-fotos/"

pack_stream() {
  local include_png=$1
  shopt -s nullglob
  for stream in "${STREAMS[@]}"; do
    src="$ROOT/$stream"
    dest="$STAGING/$stream"
    [[ -d "$src" ]] || continue
    mkdir -p "$dest"
    [[ -f "$src/posts.md" ]] && cp "$src/posts.md" "$dest/" || true
    [[ -f "$src/copy.txt" ]] && cp "$src/copy.txt" "$dest/" || true
    for ch in "$src"/*/; do
      [[ -d "$ch" ]] || continue
      ch_name=$(basename "$ch")
      [[ "$ch_name" == "png" || "$ch_name" == "jpg" || "$ch_name" == "svg" ]] && continue
      out_ch="$dest/$ch_name"
      mkdir -p "$out_ch/svg" "$out_ch/jpg"
      [[ -d "$ch/svg" ]] && cp "$ch/svg"/* "$out_ch/svg/" 2>/dev/null || true
      [[ -d "$ch/jpg" ]] && cp "$ch/jpg"/* "$out_ch/jpg/" 2>/dev/null || true
      if [[ "$include_png" == "1" && -d "$ch/png" ]]; then
        mkdir -p "$out_ch/png"
        cp "$ch/png"/* "$out_ch/png/" 2>/dev/null || true
      fi
      [[ -f "$ch/carousel.pdf" ]] && cp "$ch/carousel.pdf" "$out_ch/" || true
    done
  done
}

zip_it() {
  rm -f "$OUT_ZIP"
  (cd "$STAGING" && zip -9 -q -r "$OUT_ZIP" .)
  stat -c%s "$OUT_ZIP"
}

pack_stream 1
size=$(zip_it)
if (( size > TARGET )); then
  echo "Zip ${size}B > 15MB — repacking without PNG rasters (JPG+SVG only)." >&2
  rm -rf "$STAGING"/*
  mkdir -p "$STAGING/06-fotos"
  cp "$AGENDA_PDF" "$STAGING/agenda-evento.pdf"
  cp "$FOTOS"/*.jpg "$FOTOS/credits.txt" "$STAGING/06-fotos/"
  pack_stream 0
  size=$(zip_it)
fi

echo "Created $OUT_ZIP ($size bytes)"
if (( size > HARD )); then
  echo "ERROR: exceeds 100 MB cap" >&2
  exit 1
fi
if (( size > TARGET )); then
  echo "NOTE: still above 15 MB WhatsApp-friendly target ($size > $TARGET)" >&2
fi
unzip -l "$OUT_ZIP" | tail -5
