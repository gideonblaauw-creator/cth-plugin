#!/usr/bin/env bash
# Render all comms HTML → png/ + jpg/; build carousel PDFs.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CHROME="${CHROME:-google-chrome-stable}"
SCRIPTS="$(cd "$(dirname "$0")" && pwd)"

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
  [[ -s "$out" ]] || { echo "FAIL $out" >&2; exit 1; }
}

size_from_name() {
  local base="$1"
  if [[ "$base" =~ ([0-9]+)x([0-9]+) ]]; then
    echo "${BASH_REMATCH[1]} ${BASH_REMATCH[2]}"
    return 0
  fi
  return 1
}

carousel_size() {
  case "$1" in
    linkedin-carousel) echo "1080 1350" ;;
    instagram-carousel) echo "1080 1080" ;;
    *) return 1 ;;
  esac
}

while IFS= read -r html; do
  dir=$(dirname "$html")
  base=$(basename "$html" .html)
  parent=$(basename "$dir")

  if [[ "$base" == "agenda-print-a4" ]]; then
    render_png "$html" "$dir/agenda-print-a4.png" 900 1200
    "$CHROME" --headless=new --no-sandbox --disable-gpu \
      --print-to-pdf="$dir/agenda-print-a4.pdf" --no-pdf-header-footer \
      "file://${html}" 2>/dev/null || true
    continue
  fi

  if dims=$(size_from_name "$base"); then
    read -r w h <<< "$dims"
  elif [[ "$base" == slide-* ]] && dims=$(carousel_size "$parent"); then
    read -r w h <<< "$dims"
  else
    continue
  fi

  png_dir="$dir/png"
  jpg_dir="$dir/jpg"
  mkdir -p "$png_dir" "$jpg_dir"
  png_out="$png_dir/${base}.png"
  render_png "$html" "$png_out" "$w" "$h"
  python3 - <<PY
from PIL import Image
im = Image.open("$png_out").convert("RGB")
q = 76 if max(im.size) >= 1400 else 82
im.save("$jpg_dir/${base}.jpg", "JPEG", quality=q, optimize=True)
PY
done < <(find "$ROOT" -name '*.html' | sort)

# Carousel PDFs (LinkedIn 1080×1350 slides)
python3 - <<'PY'
from pathlib import Path
from PIL import Image

root = Path("/agent/repos/cth-plugin/datathon-assets")
for channel in ("linkedin-carousel", "instagram-carousel"):
    for stream in root.glob("[0-9][0-9]-*"):
        ch = stream / channel
        png_dir = ch / "png"
        if not png_dir.is_dir():
            continue
        slides = sorted(png_dir.glob("slide-*.png"))
        if len(slides) < 2:
            continue
        imgs = [Image.open(p).convert("RGB") for p in slides]
        pdf_path = ch / "carousel.pdf"
        imgs[0].save(pdf_path, "PDF", save_all=True, append_images=imgs[1:], resolution=120)
        print("PDF", pdf_path)
PY

echo "Render complete."
