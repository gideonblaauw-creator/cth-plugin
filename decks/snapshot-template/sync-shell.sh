#!/usr/bin/env bash
# Copy shared shell into a company snapshot folder (keeps data.json and img/ local).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
DEST="${1:?Usage: ./sync-shell.sh ../celsia-snapshot}"
cp "$ROOT/index.html" "$ROOT/render.js" "$DEST/"
echo "Synced index.html and render.js -> $DEST"
