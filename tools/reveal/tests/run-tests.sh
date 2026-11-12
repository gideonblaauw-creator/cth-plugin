#!/usr/bin/env bash
set -euo pipefail

TOOL_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$TOOL_ROOT/../.." && pwd)"
FIX="$TOOL_ROOT/tests/fixtures"

cd "$TOOL_ROOT"
npm ci >/dev/null
npm run theme:compile >/dev/null
pip3 install -q pypdf 2>/dev/null || pip install -q pypdf 2>/dev/null || true

pass() { echo "PASS: $*"; }
fail() { echo "FAIL: $*"; exit 1; }

cleanup() {
  rm -rf "$REPO_ROOT/decks/reveal-test-valid" \
    "$REPO_ROOT/decks/reveal-test-unknown" \
    "$REPO_ROOT/decks/reveal-test-missing-source" \
    "$REPO_ROOT/decks/reveal-test-off-brand" \
    "$REPO_ROOT/decks/reveal-test-integration" \
    "$REPO_ROOT/decks/slide-type-catalog"
}
trap cleanup EXIT
cleanup

echo "=== unit: palette pass ==="
node -e "
const { lintColours } = require('./lib/lint');
const html = '<style>body{color:#0c498a;background:#b2eefa;}</style>';
const err = lintColours(html);
if (err.length) { console.error(err); process.exit(1); }
"
pass "CTH palette colours accepted"

echo "=== unit: palette fail #2d6a4f ==="
if node -e "
const { lintColours } = require('./lib/lint');
const html = '<style>body{color:#2d6a4f;}</style>';
process.exit(lintColours(html).length ? 0 : 1);
" 2>/dev/null; then
  pass "legacy #2d6a4f rejected"
else
  fail "legacy #2d6a4f should fail lint"
fi

echo "=== unit: countSlides leaf only ==="
node -e "
const { countSlides } = require('./lib/lint');
const html = '<section data-cth-type=\"a\"></section><section><section data-cth-type=\"b\"></section></section>';
if (countSlides(html) !== 2) process.exit(1);
"
pass "countSlides ignores wrapper sections"

echo "=== overflow: missing dist (expect fail) ==="
if node lib/overflow-check.mjs reveal-test-no-such-deck 2>/dev/null; then
  fail "overflow-check should fail when dist missing"
else
  pass "overflow-check fails without dist"
fi

echo "=== validate-only: valid deck.yaml ==="
node lib/render-outline.js --validate-only "$FIX/valid-deck.yaml"
pass "valid outline validates"

echo "=== render + build + lint + overflow: valid deck (7 types) ==="
node lib/render-outline.js --force "$FIX/valid-deck.yaml"
node lib/lint.js reveal-test-valid
node lib/overflow-check.mjs reveal-test-valid >/dev/null
pass "outline → build → lint → overflow (7 types)"

echo "=== integration: library catalog.yaml (26 types) ==="
node lib/render-outline.js --force --skip-build "$TOOL_ROOT/library/catalog.yaml"
SLIDES=$(node -e "const fs=require('fs');const h=fs.readFileSync('$REPO_ROOT/decks/slide-type-catalog/index.html','utf8'); console.log((h.match(/data-cth-type=/g)||[]).length);")
if [[ "$SLIDES" -lt 26 ]]; then
  fail "catalog render expected 26 leaf slides, got $SLIDES"
fi
node lib/render-outline.js --force "$TOOL_ROOT/library/catalog.yaml"
node lib/lint.js slide-type-catalog
pass "catalog outline full pipeline"

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
mkdir -p "$REPO_ROOT/decks/reveal-test-off-brand/dist/theme"
cp "$FIX/off-brand-deck/index.html" "$REPO_ROOT/decks/reveal-test-off-brand/index.html"
cp "$FIX/off-brand-deck/index.html" "$REPO_ROOT/decks/reveal-test-off-brand/dist/index.html"
cp "$TOOL_ROOT/theme/cleantechhub.css" "$REPO_ROOT/decks/reveal-test-off-brand/dist/theme/"
if node lib/lint.js --skip-pdf --skip-overflow reveal-test-off-brand 2>/dev/null; then
  fail "off-brand colour should fail lint"
else
  pass "off-brand colour rejected"
fi

echo "=== lint: remote font URLs (expect fail) ==="
if node -e "
const { lintRemoteFontUrls } = require('./lib/lint');
process.exit(lintRemoteFontUrls('<link href=\"https://fonts.googleapis.com/css?family=Open+Sans\">') .length ? 0 : 1);
" 2>/dev/null; then
  pass "remote Google Fonts URL rejected"
else
  fail "remote font URL should fail lint"
fi

echo ""
echo "All outline/lint tests passed."
