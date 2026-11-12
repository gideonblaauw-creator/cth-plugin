#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cp -f "$ROOT/www/i18n.js" "$ROOT/www/app.js" "$ROOT/_site/"
echo "post-render: copied www JS to _site/"
