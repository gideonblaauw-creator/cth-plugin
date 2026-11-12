#!/usr/bin/env bash
# Brand lint for a built deck slug under decks/<slug>/.
set -euo pipefail

usage() {
  echo "Usage: $(basename "$0") [--skip-pdf] [--skip-overflow] <slug>" >&2
  exit 1
}

SLUG="${1:-}"
[[ -n "$SLUG" ]] || usage

TOOL_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$TOOL_ROOT"

if [[ ! -d node_modules ]]; then
  npm ci
fi

shift || true
exec node lib/lint.js "$SLUG" "$@"
