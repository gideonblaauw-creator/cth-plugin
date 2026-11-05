#!/usr/bin/env bash
# Pre-crop page-2 screenshot tiles (top-left, tile aspect) for Open Air Sandbox one-pager.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
SRC="$ROOT/assets/renderings"
OUT="$SRC/tiles"
mkdir -p "$OUT"
for f in 01-carga 02-datasets 03-dashboard 04-riesgo; do
  convert "$SRC/${f}.png" -gravity NorthWest -crop 1024x960+0+0 +repage "$OUT/${f}-tile.png"
done
echo "Wrote tiles to $OUT"
