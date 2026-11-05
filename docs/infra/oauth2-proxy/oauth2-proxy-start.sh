#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${INFISICAL_TOKEN:-}" && -r /etc/gideon-tracker/infisical.env ]]; then
  set -a
  # shellcheck disable=SC1091
  source /etc/gideon-tracker/infisical.env
  set +a
fi

INFISICAL_PROJECT_ID="${INFISICAL_PROJECT_ID:-c84fe8b3-d64e-485a-82d7-250dc57a6453}"
INFISICAL_ENV="${INFISICAL_ENV:-prod}"
INFISICAL_PATH="${INFISICAL_PATH:-/}"

exec infisical run \
  --env="$INFISICAL_ENV" \
  --path="$INFISICAL_PATH" \
  --projectId="$INFISICAL_PROJECT_ID" \
  -- /usr/local/bin/oauth2-proxy --config=/etc/oauth2-proxy/oauth2-proxy.cfg
