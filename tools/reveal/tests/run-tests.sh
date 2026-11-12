#!/usr/bin/env bash
set -euo pipefail

TOOL_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$TOOL_ROOT/../.." && pwd)"
FIX="$TOOL_ROOT/tests/fixtures"

cd "$TOOL_ROOT"
npm ci >/dev/null

pass() { echo "PASS: $*"; }
fail() { echo "FAIL: $*"; exit 1; }

cleanup() {
  rm -rf "$REPO_ROOT/decks/reveal-test-valid" \
    "$REPO_ROOT/decks/reveal-test-unknown" \
    "$REPO_ROOT/decks/reveal-test-missing-source" \
    "$REPO_ROOT/decks/reveal-test-off-brand"
}
trap cleanup EXIT
cleanup

echo "=== validate-only: valid deck.yaml ==="
node lib/render-outline.js --validate-only "$FIX/valid-deck.yaml"
pass "valid outline validates"

echo "=== render + build: valid deck.yaml ==="
node lib/render-outline.js --force "$FIX/valid-deck.yaml"
pass "outline + build for reveal-test-valid"

echo "=== lint: valid deck ==="
node lib/lint.js reveal-test-valid
pass "lint valid deck"

echo "=== validate-only: unknown type (expect fail) ==="
if node lib/render-outline.js --validate-only "$FIX/unknown-type-deck.yaml" 2>/dev/null; then
  fail "unknown type should have failed validation"
else
  pass "unknown type rejected"
fi

echo "=== validate-only: missing source (expect fail) ==="
if node lib/render-outline.js --validate-only "$FIX/missing-source-deck.yaml" 2>/dev/null; then
  fail "missing source should have failed validation"
else
  pass "missing source rejected"
fi

echo "=== lint: off-brand colour (expect fail) ==="
mkdir -p "$REPO_ROOT/decks/reveal-test-off-brand/dist"
cp "$FIX/off-brand-deck/index.html" "$REPO_ROOT/decks/reveal-test-off-brand/index.html"
cp "$FIX/off-brand-deck/index.html" "$REPO_ROOT/decks/reveal-test-off-brand/dist/index.html"
if node lib/lint.js --skip-pdf --skip-overflow reveal-test-off-brand 2>/dev/null; then
  fail "off-brand colour should fail lint"
else
  pass "off-brand colour rejected"
fi

echo ""
echo "All outline/lint tests passed."
