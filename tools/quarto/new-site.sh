#!/usr/bin/env bash
# Usage: new-site.sh <slug> <demo|datalab|living-lab> [es|en]
# Copies a template to sites/<slug>/ (never overwrites).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SITES="$ROOT/sites"

usage() {
  echo "Usage: $0 <slug> <demo|datalab|living-lab> [es|en]" >&2
  exit 1
}

[[ $# -ge 2 ]] || usage

SLUG="$1"
TYPE="$2"
LANG="${3:-en}"

if [[ ! "$SLUG" =~ ^[a-z0-9][a-z0-9-]{0,62}$ ]]; then
  echo "Invalid slug: use lowercase letters, digits, hyphens." >&2
  exit 1
fi

case "$TYPE" in
  demo|datalab|living-lab) ;;
  *) echo "Unknown template type: $TYPE" >&2; usage ;;
esac

case "$LANG" in
  en|es) ;;
  *) echo "Language must be en or es" >&2; exit 1 ;;
esac

DEST="$SITES/$SLUG"
if [[ -e "$DEST" ]]; then
  echo "Refusing to overwrite existing site: $DEST" >&2
  exit 1
fi

mkdir -p "$DEST"
cp -a "$ROOT/templates/$TYPE/." "$DEST/"

# Theme path from sites/<slug>/ to tools/quarto/theme/
THEME_REL="../../theme/cleantechhub.scss"
BRAND_REL="../../theme/_brand.yml"

# Pick localized entry pages
for base in index step-01 step-02 step-03 report dashboard; do
  if [[ -f "$DEST/${base}.${LANG}.qmd" ]]; then
    cp "$DEST/${base}.${LANG}.qmd" "$DEST/${base}.qmd"
  fi
done

# Keep only the selected locale on disk (faster renders, no duplicate EN/ES pages).
find "$DEST" -maxdepth 1 \( -name '*.en.qmd' -o -name '*.es.qmd' \) -delete

# Site metadata
if [[ -f "$DEST/_quarto.yml" ]]; then
  sed -i \
    -e "s|__SITE_SLUG__|$SLUG|g" \
    -e "s|__SITE_LANG__|$LANG|g" \
    -e "s|__THEME_SCSS__|$THEME_REL|g" \
    -e "s|__BRAND_YML__|$BRAND_REL|g" \
    "$DEST/_quarto.yml"
fi

# Default gate: noindex until Gideon GO per slug (documented in README + skill)
if [[ -f "$DEST/_metadata.yml" ]]; then
  sed -i "s|__SITE_SLUG__|$SLUG|g" "$DEST/_metadata.yml"
fi

# Replace slug placeholders in localized pages
find "$DEST" -maxdepth 1 -name '*.qmd' -print0 | while IFS= read -r -d '' f; do
  sed -i "s|__SITE_SLUG__|$SLUG|g" "$f"
done

echo "Scaffolded $TYPE site at $DEST (lang=$LANG)."
echo "Next: cd $ROOT && ./build.sh $SLUG"
