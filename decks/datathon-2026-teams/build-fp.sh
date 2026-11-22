#!/usr/bin/env bash
# Validate deck.yaml, render FODESEP fp layer, build dist + PDF.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
REVEAL="$(cd "$ROOT/../../tools/reveal" && pwd)"
export PUPPETEER_EXECUTABLE_PATH="${PUPPETEER_EXECUTABLE_PATH:-/usr/bin/google-chrome-stable}"
export CHROME_PATH="${CHROME_PATH:-$PUPPETEER_EXECUTABLE_PATH}"
"$REVEAL/outline.sh" "$ROOT/deck.yaml" --validate-only --skip-build
node "$ROOT/fp-render.mjs"
"$REVEAL/build.sh" datathon-2026-teams
PDF_ES="$ROOT/datathon-2026-teams.pdf"
PDF_EN="$ROOT/datathon-2026-teams-en.pdf"
INDEX_URL="file://$ROOT/dist/index.html"
echo "Exporting EN PDF to $PDF_EN …"
npx --prefix "$REVEAL" decktape reveal "${INDEX_URL}?lang=en" "$PDF_EN" \
  --size 1920x1080 \
  --pause 750 \
  --url-load-timeout 60000 \
  --chrome-arg=--no-sandbox \
  --chrome-arg=--disable-gpu
"$REVEAL/lint.sh" datathon-2026-teams
node "$ROOT/export-artifacts.mjs"