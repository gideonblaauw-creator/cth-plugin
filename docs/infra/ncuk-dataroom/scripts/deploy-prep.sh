#!/usr/bin/env bash
# Fetch NCUK dataroom secrets from Infisical and write runtime env files on the VPS.
# Do not run in CI; do not commit outputs. Requires: infisical CLI, caddy (hash-password).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
# Infisical project cth-agents (prod). CLI --projectId must be the project UUID.
INFISICAL_PROJECT="${INFISICAL_PROJECT:-c84fe8b3-d64e-485a-82d7-250dc57a6453}"
INFISICAL_ENV="${INFISICAL_ENV:-prod}"
DOCMOST_HOST_PORT="${DOCMOST_HOST_PORT:-3076}"
NCUK_DOCMOST_MAIL_FROM="${NCUK_DOCMOST_MAIL_FROM:-noreply@cleantechhub.net}"

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
if OPTIONAL_USER="$(fetch_secret NCUK_DATAROOM_BASIC_AUTH_USER 2>/dev/null)" && [[ -n "${OPTIONAL_USER}" ]]; then
  BASIC_USER="${OPTIONAL_USER}"
fi
APP_SECRET="$(fetch_secret NCUK_DOCMOST_APP_SECRET)"
DB_PASS="$(fetch_secret NCUK_DOCMOST_DB_PASSWORD)"

if [[ ${#BASIC_PASS} -lt 20 ]]; then
  echo "ERROR: NCUK_DATAROOM_BASIC_AUTH_PASSWORD must be at least 20 characters." >&2
  exit 1
fi

MAIL_DRIVER="log"
MAIL_FROM_ADDRESS=""
MAIL_FROM_NAME="REIN Hubs Data Room"
SMTP_HOST=""
SMTP_PORT="465"
SMTP_SECURE="true"
SMTP_IGNORETLS="false"
SMTP_USERNAME=""
SMTP_PASSWORD=""
POSTMARK_TOKEN=""

if RESEND_KEY="$(fetch_secret RESEND_API_KEY 2>/dev/null)" && [[ -n "${RESEND_KEY}" ]]; then
  echo "==> Configuring Docmost outbound mail via Resend SMTP (Infisical: RESEND_API_KEY)"
  MAIL_DRIVER="smtp"
  MAIL_FROM_ADDRESS="${NCUK_DOCMOST_MAIL_FROM}"
  SMTP_HOST="smtp.resend.com"
  SMTP_PORT="465"
  SMTP_SECURE="true"
  SMTP_USERNAME="resend"
  SMTP_PASSWORD="${RESEND_KEY}"
elif POSTMARK="$(fetch_secret POSTMARK_TOKEN 2>/dev/null)" && [[ -n "${POSTMARK}" ]]; then
  echo "==> Configuring Docmost outbound mail via Postmark (Infisical: POSTMARK_TOKEN)"
  MAIL_DRIVER="postmark"
  MAIL_FROM_ADDRESS="${NCUK_DOCMOST_MAIL_FROM}"
  POSTMARK_TOKEN="${POSTMARK}"
else
  echo "==> No RESEND_API_KEY or POSTMARK_TOKEN in Infisical; MAIL_DRIVER stays log"
fi

echo "==> Generating Caddy bcrypt hash (not printed)"
HASH="$(caddy hash-password --plaintext "${BASIC_PASS}")"

CADDY_ENV="${ROOT_DIR}/caddy.env"
ENV_GEN="${ROOT_DIR}/.env.generated"

cat >"${CADDY_ENV}" <<EOF
NCUK_BASIC_AUTH_USER=${BASIC_USER}
NCUK_BASIC_AUTH_HASH=${HASH}
NCUK_ROOM_MODE=${NCUK_ROOM_MODE:-docmost}
NCUK_DOCMOST_UPSTREAM=127.0.0.1:${DOCMOST_HOST_PORT}
NCUK_FALLBACK_ROOT=${NCUK_FALLBACK_ROOT:-/opt/claude-files/Projects/REIN-Hubs/ncuk-dataroom/fallback/docusaurus/build}
NCUK_FALLBACK_UPSTREAM=${NCUK_FALLBACK_UPSTREAM:-}
EOF
chmod 600 "${CADDY_ENV}"

cat >"${ENV_GEN}" <<EOF
APP_URL=https://dataroom.cleantechhub.net
APP_SECRET=${APP_SECRET}
POSTGRES_PASSWORD=${DB_PASS}
DATABASE_URL=postgresql://docmost:${DB_PASS}@ncuk-dataroom-db:5432/docmost
DOCMOST_HOST_PORT=${DOCMOST_HOST_PORT}
MAIL_DRIVER=${MAIL_DRIVER}
MAIL_FROM_ADDRESS=${MAIL_FROM_ADDRESS}
MAIL_FROM_NAME=${MAIL_FROM_NAME}
SMTP_HOST=${SMTP_HOST}
SMTP_PORT=${SMTP_PORT}
SMTP_SECURE=${SMTP_SECURE}
SMTP_IGNORETLS=${SMTP_IGNORETLS}
SMTP_USERNAME=${SMTP_USERNAME}
SMTP_PASSWORD=${SMTP_PASSWORD}
POSTMARK_TOKEN=${POSTMARK_TOKEN}
EOF
chmod 600 "${ENV_GEN}"

echo "==> Wrote ${CADDY_ENV} and ${ENV_GEN} (MAIL_DRIVER=${MAIL_DRIVER})"
echo "Next: docker compose --env-file .env.generated up -d docmost"
echo "Next: sudo caddy validate --config /etc/caddy/Caddyfile && sudo systemctl reload caddy"
