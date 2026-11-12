#!/usr/bin/env bash
# Usage: build.sh <slug>
# Renders sites/<slug>/ to sites/<slug>/_site/; fails on any cell error.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SLUG="${1:-}"

if [[ -z "$SLUG" ]]; then
  echo "Usage: $0 <slug>" >&2
  exit 1
fi

SITE="$ROOT/sites/$SLUG"
if [[ ! -d "$SITE" ]]; then
  echo "Site not found: $SITE (run new-site.sh first)" >&2
  exit 1
fi

"$ROOT/install-quarto.sh"
"$ROOT/setup-python.sh"

export QUARTO_PYTHON="$ROOT/.venv/bin/python"
export PATH="$ROOT/.venv/bin:$PATH"

echo "Rendering $SLUG with QUARTO_PYTHON=$QUARTO_PYTHON"
cd "$SITE"
quarto render

echo "OK: $SITE/_site/"
