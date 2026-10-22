#!/usr/bin/env bash
# Health check for NCUK dataroom (VPS localhost and/or public URL).
set -euo pipefail

PUBLIC_BASE="${1:-}"
MODE="${NCUK_ROOM_MODE:-docmost}"
DOCMOST_PORT="${DOCMOST_HOST_PORT:-3076}"
LOCAL_UPSTREAM="http://127.0.0.1:${DOCMOST_PORT}"

echo "==> Mode: ${MODE}"

if [[ "${MODE}" == "docmost" ]]; then
  code="$(curl -sS -o /dev/null -w '%{http_code}' "${LOCAL_UPSTREAM}/api/health" || true)"
  echo "Docmost upstream ${LOCAL_UPSTREAM}/api/health HTTP ${code}"
  if [[ "${code}" != "200" ]]; then
    exit 1
  fi
else
  root="${NCUK_FALLBACK_ROOT:-}"
  if [[ -n "${root}" && -f "${root}/index.html" ]]; then
    echo "Fallback static root OK: ${root}/index.html"
  elif [[ -n "${NCUK_FALLBACK_UPSTREAM:-}" ]]; then
    code="$(curl -sS -o /dev/null -w '%{http_code}' "http://${NCUK_FALLBACK_UPSTREAM}/ncuk/" || true)"
    echo "Fallback proxy http://${NCUK_FALLBACK_UPSTREAM}/ncuk/ HTTP ${code}"
    if [[ "${code}" != "200" ]]; then
      exit 1
    fi
  else
    echo "WARN: fallback mode but NCUK_FALLBACK_ROOT or NCUK_FALLBACK_UPSTREAM not set" >&2
    exit 1
  fi
fi

if [[ -n "${PUBLIC_BASE}" ]]; then
  echo "==> Public: ${PUBLIC_BASE}"
  if [[ "${MODE}" == "docmost" ]]; then
    pub_code="$(curl -sS -o /dev/null -w '%{http_code}' "${PUBLIC_BASE}/ncuk" || true)"
    echo "${PUBLIC_BASE}/ncuk HTTP ${pub_code} (expect 401 without creds, or 302 after auth)"
  else
    pub_code="$(curl -sS -o /dev/null -w '%{http_code}' "${PUBLIC_BASE}/ncuk/" || true)"
    echo "${PUBLIC_BASE}/ncuk/ HTTP ${pub_code} (expect 401 without creds)"
  fi
fi

echo "OK"
