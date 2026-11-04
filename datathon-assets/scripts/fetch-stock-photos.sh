#!/usr/bin/env bash
# Download free-licensed stock for datathon kit (Unsplash + Pexels, commercial use).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/06-fotos"
mkdir -p "$OUT"

fetch() {
  local url="$1" dest="$2"
  curl -fsSL "$url" -o "$dest"
  echo "OK $dest"
}

# Pexels — Los Muertos Crew (Bogotá, Colombia solar installs)
fetch "https://images.pexels.com/photos/8853505/pexels-photo-8853505.jpeg?auto=compress&cs=tinysrgb&w=1600" \
  "$OUT/solar-bogota-8853505.jpg"
fetch "https://images.pexels.com/photos/8853502/pexels-photo-8853502.jpeg?auto=compress&cs=tinysrgb&w=1600" \
  "$OUT/solar-install-8853502.jpg"
fetch "https://images.pexels.com/photos/8853507/pexels-photo-8853507.jpeg?auto=compress&cs=tinysrgb&w=1600" \
  "$OUT/solar-worker-8853507.jpg"

# Pexels — engineer / data work (This Is Engineering, field engineer)
fetch "https://images.pexels.com/photos/19895882/pexels-photo-19895882.jpeg?auto=compress&cs=tinysrgb&w=1600" \
  "$OUT/engineer-cad-19895882.jpg"
fetch "https://images.pexels.com/photos/442152/pexels-photo-442152.jpeg?auto=compress&cs=tinysrgb&w=1600" \
  "$OUT/field-engineer-laptop-442152.jpg"

# Pexels — Mexico City skyline (urban cleantech context)
fetch "https://images.pexels.com/photos/21383930/pexels-photo-21383930.jpeg?auto=compress&cs=tinysrgb&w=1600" \
  "$OUT/city-mexico-21383930.jpg"

# Unsplash License — solar rooftop install
fetch "https://images.unsplash.com/photo-1635424825057-7fb6dcd651ef?auto=format&fit=crop&w=1600&q=80" \
  "$OUT/solar-roof-unsplash-ACnFSTBlnts.jpg"

ls -lh "$OUT"/*.jpg
