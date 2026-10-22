#!/usr/bin/env bash
# Fetch NCUK dataroom secrets from Infisical and write runtime env files on the VPS.
# Do not run in CI; do not commit outputs. Requires: infisical CLI, caddy (hash-password).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
INFISICAL_PROJECT="${INFISICAL_PROJECT:-cth-agents}"
INFISICAL_ENV="${INFISICAL_ENV:-prod}"

fetch_secret() {
  local key="$1"
  infisical secrets get "${key}" \
    --projectId="${INFISICAL_PROJECT}" \
    --env="${INFISICAL_ENV}" \
    --path="/" \
    --plain
}

echo "==> Fetching secrets from Infisical (${INFISICAL_PROJECT} / ${INFISICAL_ENV})"
BASIC_PASS="$(fetch_secret NCUK_DATAROOM_BASIC_AUTH_PASSWORD)"
BASIC_USER="rein"
if OPTIONAL_USER="$(fetch_secret NCUK_DATAROOM_BASIC_AUTH_USER 2>/dev/null)"; then
  BASIC_USER="${OPTIONAL_USER}"
fi
APP_SECRET="$(fetch_secret NCUK_DOCMOST_APP_SECRET)"
DB_PASS="$(fetch_secret NCUK_DOCMOST_DB_PASSWORD)"

if [[ ${#BASIC_PASS} -lt 20 ]]; then
  echo "ERROR: NCUK_DATAROOM_BASIC_AUTH_PASSWORD must be at least 20 characters." >&2
  exit 1
fi

echo "==> Generating Caddy bcrypt hash (not printed)"
HASH="$(caddy hash-password --plaintext "${BASIC_PASS}")"

CADDY_ENV="${ROOT_DIR}/caddy.env"
ENV_GEN="${ROOT_DIR}/.env.generated"

cat >"${CADDY_ENV}" <<EOF
NCUK_BASIC_AUTH_USER=${BASIC_USER}
NCUK_BASIC_AUTH_HASH=${HASH}
NCUK_ROOM_MODE=${NCUK_ROOM_MODE:-docmost}
NCUK_FALLBACK_ROOT=${NCUK_FALLBACK_ROOT:-/opt/claude-files/Projects/REIN-Hubs/ncuk-dataroom/fallback/build}
EOF
chmod 600 "${CADDY_ENV}"

cat >"${ENV_GEN}" <<EOF
APP_URL=https://dataroom.cleantechhub.net
APP_SECRET=${APP_SECRET}
POSTGRES_PASSWORD=${DB_PASS}
DATABASE_URL=postgresql://docmost:${DB_PASS}@ncuk-dataroom-db:5432/docmost
EOF
chmod 600 "${ENV_GEN}"

echo "==> Wrote ${CADDY_ENV} and ${ENV_GEN}"
echo "Next: docker compose --env-file .env.generated up -d"
echo "Next: export \$(grep -v '^#' caddy.env | xargs) && caddy reload --config /etc/caddy/Caddyfile"
