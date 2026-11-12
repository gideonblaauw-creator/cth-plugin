#!/usr/bin/env bash
# Install pinned Quarto CLI (checksum-verified). Idempotent.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERSIONS="$ROOT/versions.json"

if ! command -v jq >/dev/null 2>&1; then
  echo "install-quarto.sh: jq is required" >&2
  exit 1
fi

QVER="$(jq -r '.quarto_version' "$VERSIONS")"
EXPECTED_SHA="$(jq -r '.quarto_deb_sha256' "$VERSIONS")"
DEB_NAME="quarto-${QVER}-linux-amd64.deb"
URL="https://github.com/quarto-dev/quarto-cli/releases/download/v${QVER}/${DEB_NAME}"
CACHE="$ROOT/.cache"
DEB="$CACHE/$DEB_NAME"

if command -v quarto >/dev/null 2>&1; then
  INSTALLED="$(quarto --version 2>/dev/null | head -1 || true)"
  if [[ "$INSTALLED" == "$QVER" ]]; then
    echo "Quarto $QVER already installed."
    exit 0
  fi
  echo "Quarto installed ($INSTALLED) but pin is $QVER — reinstalling."
fi

mkdir -p "$CACHE"
if [[ ! -f "$DEB" ]]; then
  echo "Downloading Quarto $QVER …"
  curl -fsSL -o "$DEB" "$URL"
fi

ACTUAL_SHA="$(sha256sum "$DEB" | awk '{print $1}')"
if [[ "$ACTUAL_SHA" != "$EXPECTED_SHA" ]]; then
  echo "Checksum mismatch for $DEB" >&2
  echo "  expected: $EXPECTED_SHA" >&2
  echo "  actual:   $ACTUAL_SHA" >&2
  rm -f "$DEB"
  exit 1
fi

echo "Checksum OK — installing Quarto $QVER"
sudo dpkg -i "$DEB"
quarto --version
