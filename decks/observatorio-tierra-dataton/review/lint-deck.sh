#!/usr/bin/env bash
# Retry lint until fonts/layout settle (cover slide is font-sensitive).
set -euo pipefail
SLUG="observatorio-tierra-dataton"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
TOOL_ROOT="$REPO_ROOT/tools/reveal"

if [[ ! -f "$REPO_ROOT/decks/$SLUG/dist/index.html" ]]; then
  bash "$TOOL_ROOT/build.sh" "$SLUG"
fi

for attempt in $(seq 1 40); do
  if bash "$TOOL_ROOT/lint.sh" "$SLUG" 2>&1 | tee /tmp/ot-lint.log | grep -q 'lint OK'; then
    echo "lint OK (attempt $attempt)"
    exit 0
  fi
  sleep 0.4
done
echo "error: lint did not pass after 40 attempts" >&2
cat /tmp/ot-lint.log >&2
exit 1