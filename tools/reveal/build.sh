#!/usr/bin/env bash
# Build static dist/ + PDF for decks/<slug>/ using pinned reveal.js.
set -euo pipefail

usage() {
  echo "Usage: $(basename "$0") <slug>" >&2
  exit 1
}

SLUG="${1:-}"
[[ -n "$SLUG" ]] || usage

TOOL_ROOT="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$TOOL_ROOT/../.." && pwd)"
DECK_ROOT="$REPO_ROOT/decks/$SLUG"
DIST="$DECK_ROOT/dist"

if [[ ! -d "$DECK_ROOT" ]]; then
  echo "error: deck not found at decks/$SLUG" >&2
  exit 1
fi

if [[ ! -f "$DECK_ROOT/index.html" ]]; then
  echo "error: missing decks/$SLUG/index.html" >&2
  exit 1
fi

cd "$TOOL_ROOT"
if [[ ! -d node_modules/reveal.js ]]; then
  echo "Installing tools/reveal npm dependencies…"
  npm ci 2>/dev/null || npm install
fi

npm run theme:compile

rm -rf "$DIST"
mkdir -p "$DIST/theme"

cp "$DECK_ROOT/index.html" "$DIST/"
cp "$TOOL_ROOT/theme/cleantechhub.css" "$DIST/theme/"
cp -a "$TOOL_ROOT/node_modules/reveal.js" "$DIST/reveal.js"

if [[ -f "$DECK_ROOT/deck-meta.json" ]]; then
  cp "$DECK_ROOT/deck-meta.json" "$DIST/"
fi

# Optional deck-local assets (logos, data, custom JS)
for sub in assets logos data; do
  if [[ -d "$DECK_ROOT/$sub" ]]; then
    cp -a "$DECK_ROOT/$sub" "$DIST/$sub"
  fi
done

PDF_PATH="$DECK_ROOT/$SLUG.pdf"
INDEX_URL="file://$DIST/index.html"

echo "Exporting PDF to $PDF_PATH …"
npx decktape reveal "$INDEX_URL" "$PDF_PATH" \
  --size 1920x1080 \
  --pause 750 \
  --url-load-timeout 60000 \
  --chrome-arg=--no-sandbox \
  --chrome-arg=--disable-gpu

echo "Built dist/ at decks/$SLUG/dist/"
echo "PDF: decks/$SLUG/$SLUG.pdf"
