#!/usr/bin/env bash
# Install committed Open Sans 3.x TTFs for LibreOffice / fontconfig (no merge, no apt package).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
DEST="${HOME}/.local/share/fonts/cth-open-sans"
if dpkg -l fonts-open-sans 2>/dev/null | grep -q '^ii'; then
  sudo apt-get remove -y fonts-open-sans
fi
rm -rf "${HOME}/.local/share/fonts/open-sans-merged"
mkdir -p "$DEST"
cp "$ROOT"/open-sans/OpenSans-*.ttf "$DEST/"
fc-cache -f
echo "fc-match Open Sans: $(fc-match 'Open Sans')"
echo "fc-match Open Sans:bold: $(fc-match 'Open Sans:bold')"