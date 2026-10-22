#!/usr/bin/env bash
# Self-verify compose and Caddy config (safe for CI / Cloud Hands; no secrets).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${ROOT_DIR}"

export APP_SECRET=0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
export POSTGRES_PASSWORD=local-dev-only-not-for-production
export DATABASE_URL="postgresql://docmost:${POSTGRES_PASSWORD}@ncuk-dataroom-db:5432/docmost"
export DOCMOST_HOST_PORT=3076

echo "==> docker compose config (or YAML fallback if Docker absent)"
if command -v docker >/dev/null 2>&1; then
  docker compose config >/dev/null
else
  python3 - <<'PY'
import yaml
from pathlib import Path
data = yaml.safe_load(Path("docker-compose.yml").read_text())
for name, svc in data["services"].items():
    assert svc.get("restart") == "unless-stopped"
    if "mem_limit" in svc:
        assert svc["memswap_limit"] == svc["mem_limit"]
    if name in ("db", "redis"):
        assert "ports" not in svc
doc = data["services"]["docmost"]
ports = doc.get("ports") or []
assert any("127.0.0.1:3076" in str(p) or "127.0.0.1:${DOCMOST_HOST_PORT:-3076}" in str(p) for p in ports)
assert "caddy_edge" not in data.get("networks", {})
assert doc.get("networks") == ["ncuk_internal"]
print("compose YAML OK (docker CLI not available)")
PY
fi

export NCUK_BASIC_AUTH_USER=rein
export NCUK_ROOM_MODE=docmost
export NCUK_DOCMOST_UPSTREAM=127.0.0.1:3076
export NCUK_FALLBACK_ROOT=/tmp/ncuk-fallback-build
export NCUK_FALLBACK_UPSTREAM=

SITE_FILE="caddy/dataroom.cleantechhub.net.caddy"
TMP_CADDY="$(mktemp --suffix=.Caddyfile)"
trap 'rm -f "${TMP_CADDY}"' EXIT
grep -v '^#' "${SITE_FILE}" | sed '/^[[:space:]]*$/d' >"${TMP_CADDY}"

echo "==> caddy validate (${SITE_FILE})"
CADDY_BIN="${CADDY_BIN:-caddy}"
if ! command -v "${CADDY_BIN}" >/dev/null 2>&1; then
  CADDY_BIN="/tmp/caddy"
  if [[ ! -x "${CADDY_BIN}" ]]; then
    curl -fsSL "https://github.com/caddyserver/caddy/releases/download/v2.10.0/caddy_2.10.0_linux_amd64.tar.gz" \
      | tar -xz -C /tmp caddy
  fi
fi
HASH="$("${CADDY_BIN}" hash-password --plaintext 'local-validate-only-not-a-secret')"
export NCUK_BASIC_AUTH_HASH="${HASH}"
"${CADDY_BIN}" validate --config "${TMP_CADDY}"

echo "OK"
