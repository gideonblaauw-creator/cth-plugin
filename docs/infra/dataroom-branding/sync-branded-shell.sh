#!/usr/bin/env bash
# Build branded Docmost SPA shell (title/favicon refs + debrand script). No secrets.
set -euo pipefail

UPSTREAM="${DOCMOST_UPSTREAM:-http://127.0.0.1:3076}"
BRAND_ROOT="${BRAND_ROOT:-/opt/cth-dataroom-branding}"
WWW_DIR="$BRAND_ROOT/www"
ICON_DIR="$BRAND_ROOT/icons"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REIN_LOGO="${REIN_LOGO:-$SCRIPT_DIR/icons/rein-white-orange.png}"

mkdir -p "$WWW_DIR" "$ICON_DIR"
curl -fsS "$UPSTREAM/" -o "$WWW_DIR/index.raw.html"

python3 - "$WWW_DIR/index.raw.html" "$WWW_DIR/index.html" <<'PY'
import re, sys
raw = open(sys.argv[1], encoding="utf-8").read()
raw = raw.replace("<title>Docmost</title>", "<title>REIN Hubs Data Room</title>")
raw = re.sub(
    r'content="Docmost"',
    'content="REIN Hubs Data Room"',
    raw,
)
if "/rein-debrand.js" not in raw:
    raw = raw.replace("</head>", '  <script src="/rein-debrand.js" defer></script>\n  </head>')
open(sys.argv[2], "w", encoding="utf-8").write(raw)
PY

if [[ -f "$REIN_LOGO" ]]; then
  cp "$REIN_LOGO" "$ICON_DIR/favicon-32x32.png"
  cp "$REIN_LOGO" "$ICON_DIR/favicon-16x16.png"
fi

if [[ "$(readlink -f "$SCRIPT_DIR/rein-debrand.js")" != "$(readlink -f "$BRAND_ROOT/rein-debrand.js")" ]]; then
  cp "$SCRIPT_DIR/rein-debrand.js" "$BRAND_ROOT/rein-debrand.js"
fi
echo "Branded shell written to $WWW_DIR/index.html"
