#!/usr/bin/env bash
# Concatenate shell + slides → self-contained index.html (CSS inlined)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

OUT="$ROOT/index.html"
CSS="$ROOT/shell/deck.css"
HEAD="$ROOT/shell/head.html"
JS="$ROOT/shell/deck.js"

css_content="$(cat "$CSS")"
{
  cat "$HEAD"
  echo "$css_content"
  echo '</style>'
  echo '</head>'
  echo '<body>'
  echo '<div class="deck-viewport"><div class="deck-stage"><div class="deck" id="deck">'
  for f in $(ls -1 "$ROOT/slides/"*.html 2>/dev/null | sort); do
    cat "$f"
  done
  echo '</div></div></div>'
  echo '<p class="nav-hint" aria-hidden="true">← → · espacio · clic</p>'
  echo '<script>'
  cat "$JS"
  echo '</script>'
  echo '</body></html>'
} > "$OUT"

echo "Built $OUT ($(wc -l < "$OUT") lines, $(ls -1 slides/*.html 2>/dev/null | wc -l) slide files)"
