#!/usr/bin/env bash
# Health check for NCUK dataroom (run on VPS or against public URL after deploy).
set -euo pipefail

BASE_URL="${1:-https://dataroom.cleantechhub.net}"
MODE="${NCUK_ROOM_MODE:-docmost}"

echo "==> Mode: ${MODE}"
echo "==> Base: ${BASE_URL}"

if [[ "${MODE}" == "docmost" ]]; then
  code="$(curl -sS -o /dev/null -w '%{http_code}' "${BASE_URL}/api/health" || true)"
  echo "Docmost /api/health HTTP ${code}"
  if [[ "${code}" != "200" && "${code}" != "401" ]]; then
    echo "WARN: expected 200 (or 401 if basic auth wraps /api — adjust Caddy if needed)" >&2
    exit 1
  fi
else
  code="$(curl -sS -o /dev/null -w '%{http_code}' "${BASE_URL}/ncuk/" || true)"
  echo "Fallback /ncuk/ HTTP ${code}"
  if [[ "${code}" != "200" && "${code}" != "401" ]]; then
    exit 1
  fi
fi

echo "OK"
