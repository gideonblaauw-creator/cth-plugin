#!/usr/bin/env bash
# Render deck.yaml -> decks/<slug>/ and build PDF (tools/reveal/build.sh).
set -euo pipefail

usage() {
  echo "Usage: $(basename "$0") [--force] [--skip-build] [--validate-only] <deck.yaml>" >&2
  exit 1
}

TOOL_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$TOOL_ROOT"

if [[ ! -d node_modules ]]; then
  echo "Installing tools/reveal npm dependencies…"
  npm ci
fi

ARGS=()
for a in "$@"; do ARGS+=("$a"); done
[[ ${#ARGS[@]} -gt 0 ]] || usage

exec node lib/render-outline.js "${ARGS[@]}"
