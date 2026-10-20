#!/usr/bin/env bash
# Concatenate shell + slides into one self-contained index.html.
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
  echo '<div class="deck-viewport"><div class="deck-frame"><div class="deck-stage"><div class="deck" id="deck">'
  for f in $(ls -1 "$ROOT/slides/"*.html 2>/dev/null | sort); do
    cat "$f"
  done
  echo '</div></div></div></div>'
  cat << 'CHROME'

<div class="deck-chrome" id="deck-chrome">
  <button type="button" class="chrome-btn" id="btn-menu" aria-expanded="false" aria-controls="deck-menu">Index</button>
  <nav class="slide-dots" id="slide-dots" aria-label="Slide progress"></nav>
  <button type="button" class="chrome-btn" id="btn-questions" aria-pressed="false">Show questions</button>
</div>
<div class="deck-menu" id="deck-menu" hidden>
  <div class="deck-menu-panel" role="dialog" aria-label="Slide index">
    <h2>Index</h2>
    <ul class="deck-menu-list" id="deck-menu-list"></ul>
  </div>
</div>
<div class="lightbox" id="lightbox" hidden role="dialog" aria-label="Enlarged image">
  <button type="button" class="chrome-btn lightbox-close" id="lightbox-close">Close</button>
  <img id="lightbox-img" src="" alt="">
  <p class="lightbox-cap" id="lightbox-cap"></p>
</div>
CHROME
  echo '<p class="nav-hint" aria-hidden="true">arrows · space · click · index · dots</p>'
  echo '<script>'
  cat "$JS"
  echo '</script>'
  echo '</body></html>'
} > "$OUT"

echo "Built $OUT ($(wc -l < "$OUT") lines, $(ls -1 slides/*.html 2>/dev/null | wc -l) slide files)"
