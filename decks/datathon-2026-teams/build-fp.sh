#!/usr/bin/env bash
# Validate deck.yaml, render FODESEP fp layer, build dist + PDF.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
REVEAL="$(cd "$ROOT/../../tools/reveal" && pwd)"
"$REVEAL/outline.sh" "$ROOT/deck.yaml" --validate-only --skip-build
node "$ROOT/fp-render.mjs"
"$REVEAL/build.sh" datathon-2026-teams
"$REVEAL/lint.sh" datathon-2026-teams