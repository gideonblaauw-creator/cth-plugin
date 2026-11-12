#!/usr/bin/env bash
# Scaffold a new CleantechHUB reveal.js deck under decks/<slug>/.
set -euo pipefail

usage() {
  echo "Usage: $(basename "$0") <slug> [en|es] [\"Deck title\"]" >&2
  exit 1
}

SLUG="${1:-}"
LANG="${2:-en}"
TITLE="${3:-}"

[[ -n "$SLUG" ]] || usage
[[ "$SLUG" =~ ^[a-z0-9][a-z0-9-]*[a-z0-9]$ ]] || {
  echo "error: slug must be lowercase alphanumerics and hyphens" >&2
  exit 1
}

case "$LANG" in
  en|es) ;;
  *) echo "error: language must be en or es" >&2; exit 1 ;;
esac

TOOL_ROOT="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$TOOL_ROOT/../.." && pwd)"
DECK_ROOT="$REPO_ROOT/decks/$SLUG"

if [[ -e "$DECK_ROOT" ]]; then
  echo "error: $DECK_ROOT already exists — not overwriting" >&2
  exit 1
fi

if [[ -z "$TITLE" ]]; then
  TITLE="$(echo "$SLUG" | tr '-' ' ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)} 1')"
fi

mkdir -p "$DECK_ROOT"
cp "$TOOL_ROOT/template/SOURCES.md" "$TOOL_ROOT/template/README.md" "$TOOL_ROOT/template/deck-meta.json" "$DECK_ROOT/"
cp "$TOOL_ROOT/template/$LANG/index.html" "$DECK_ROOT/index.html"

escape_sed() {
  printf '%s' "$1" | sed -e 's/[&/\]/\\&/g'
}

TITLE_ESC="$(escape_sed "$TITLE")"
SLUG_ESC="$(escape_sed "$SLUG")"
LANG_ESC="$(escape_sed "$LANG")"

sed -i "s/__DECK_TITLE__/$TITLE_ESC/g" "$DECK_ROOT/index.html" "$DECK_ROOT/deck-meta.json"
sed -i "s/__SLUG__/$SLUG_ESC/g" "$DECK_ROOT/deck-meta.json"
sed -i "s/__LANG__/$LANG_ESC/g" "$DECK_ROOT/deck-meta.json"

echo "Created deck at decks/$SLUG/ (lang=$LANG, gated=true)"
echo "Title: $TITLE"
echo "Next: tools/reveal/build.sh $SLUG"
