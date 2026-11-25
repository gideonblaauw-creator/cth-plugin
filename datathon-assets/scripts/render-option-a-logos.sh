#!/usr/bin/env bash
# Rasterize Option A SVG to light/dark PNGs (wordmark: Datalab, one word).
set -euo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
SVG="$REPO/brand/datalab-logo-2026-11/archive/logo/option-a.svg"
OUT="$REPO/brand/datalab-logo-2026-11/archive/logo"
CHROME="${CHROME:-google-chrome-stable}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

svg_body="$(cat "$SVG")"
dark_svg="${svg_body//fill: #0C498A;/fill: #FFFFFF;}"

render() {
  local variant="$1" body="$2" bg="$3" out="$4"
  cat >"$TMP/$variant.html" <<HTML
<!DOCTYPE html><html><head><meta charset="utf-8"/>
<style>
  html,body{margin:0;width:480px;height:120px;background:${bg};overflow:hidden}
  img{display:block;width:480px;height:120px}
</style></head><body>
${body}
</body></html>
HTML
  "$CHROME" --headless=new --no-sandbox --disable-gpu \
    --window-size=480,120 --force-device-scale-factor=1 \
    --screenshot="$out" --hide-scrollbars \
    "file://$TMP/$variant.html" 2>/dev/null
  [[ -s "$out" ]]
}

render light "<img src=\"file://${SVG}\" alt=\"\" />" "#FFFFFF" "$OUT/option-a-light.png"
render dark "$dark_svg" "#0C498A" "$OUT/option-a-dark.png"
echo "OK option-a-light.png option-a-dark.png"
