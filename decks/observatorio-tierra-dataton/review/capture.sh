#!/usr/bin/env bash
# Capture 11 Reveal slides (final fragment state) + contact sheet; assert distinct hashes.
set -euo pipefail

SLUG="observatorio-tierra-dataton"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DECK_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$DECK_ROOT/../.." && pwd)"
TOOL_ROOT="$REPO_ROOT/tools/reveal"

if [[ ! -f "$DECK_ROOT/dist/index.html" ]]; then
  echo "Building dist first…" >&2
  bash "$TOOL_ROOT/build.sh" "$SLUG"
fi

# Optional FODESEP read-only compare source (live layer unpack, not in repo)
FODESEP_ROOT="${FODESEP_ROOT:-/tmp/fodesep}"
FODESEP_HTML=""
if [[ -n "$FODESEP_ROOT" && -f "$FODESEP_ROOT/index.html" ]]; then
  mkdir -p "$FODESEP_ROOT/dist"
  cp -a "$TOOL_ROOT/node_modules/reveal.js" "$FODESEP_ROOT/dist/reveal.js" 2>/dev/null || true
  mkdir -p "$FODESEP_ROOT/dist/theme"
  cp "$TOOL_ROOT/theme/cleantechhub.css" "$FODESEP_ROOT/dist/theme/"
  rm -rf "$FODESEP_ROOT/dist"
  mkdir -p "$FODESEP_ROOT/dist"
  for item in index.html deck.css deck-meta.json assets fonts theme; do
    [[ -e "$FODESEP_ROOT/$item" ]] && cp -a "$FODESEP_ROOT/$item" "$FODESEP_ROOT/dist/"
  done
  mkdir -p "$FODESEP_ROOT/dist/theme"
  cp "$TOOL_ROOT/theme/cleantechhub.css" "$FODESEP_ROOT/dist/theme/"
  cp -a "$TOOL_ROOT/node_modules/reveal.js" "$FODESEP_ROOT/dist/reveal.js"
  FODESEP_HTML="$FODESEP_ROOT/dist/index.html"
fi

export FODESEP_HTML
export CHROME_PATH="${CHROME_PATH:-/usr/bin/google-chrome-stable}"

cd "$TOOL_ROOT"
if [[ ! -d node_modules/puppeteer-core ]]; then
  npm ci
fi

node "$SCRIPT_DIR/capture.mjs"

UNIQUE=$(md5sum "$SCRIPT_DIR"/slide-*.png | awk '{print $1}' | sort -u | wc -l)
if [[ "$UNIQUE" -ne 11 ]]; then
  echo "error: expected 11 unique slide hashes, got $UNIQUE" >&2
  exit 2
fi
echo "QA capture: 11 distinct slide PNGs + contact-sheet.png"