# bot-events

Tiny SQLite-backed event log for CleantechHUB bot activity (orchestrator, desk, workbench, hands). Ingest via authenticated POST; read via JSON queries or Server-Sent Events (SSE).

> **Deploy gate:** Everything in [Deploy plan](#deploy-plan-needs-gideons-go) needs **Gideon's explicit GO** before execution on the OVH VPS. This README is documentation only; Cloud Hands do not deploy.

## Requirements

- Node.js 22+
- SQLite (via built-in `node:sqlite`)
- Infisical CLI on the VPS for `BOT_EVENTS_TOKEN`

## Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `BOT_EVENTS_DB` | yes | — | Filesystem path to SQLite database file |
| `BOT_EVENTS_TOKEN` | yes (prod ingest) | — | Bearer token for `POST /event` (Infisical secret) |
| `BOT_EVENTS_PORT` | no | `8795` | TCP port |
| `BOT_EVENTS_HOST` | no | `127.0.0.1` | Bind address (keep loopback; Caddy terminates TLS) |

Start locally (token and DB path from your environment):

```bash
cd services/bot-events
export BOT_EVENTS_DB=/tmp/bot-events.db
export BOT_EVENTS_TOKEN='your-dev-token'
infisical run --projectId c84fe8b3 --env prod --path / -- node server.js
```

Never commit secrets. Production token lives in Infisical as **`BOT_EVENTS_TOKEN`**.

## API

### `POST /event`

Bearer auth required. JSON body:

| Field | Required | Notes |
|-------|----------|-------|
| `bot_id` | yes | string |
| `bot_name` | yes | string |
| `layer` | yes | `orchestrator`, `desk`, `workbench`, `hands` |
| `type` | yes | `start`, `finish`, `blocked`, `needs_gideon`, `heartbeat` |
| `task` | yes | string |
| `link` | yes | string (URL or reference) |
| `cause_tag` | no | `unclear_ticket`, `missing_map`, `wrong_model`, `waiting_on_gideon`, `broken_connector`, `other` |
| `ts` | no | ISO 8601; defaults to now |

Returns `201` with `{ "event": { ... } }`. Validation errors return `400`.

### `GET /events`

Query: `since`, `bot_id`, `type`, `limit` (1–1000, default 100). Returns `{ "events": [ ... ] }` newest first.

Protected at the edge by Google gate (Caddy `forward_auth`), not bearer token in the app.

### `GET /stream`

SSE stream of new events (`data: {json}\n\n`). Same edge auth as reads.

### `GET /bots`

Latest event per `bot_id`, plus `silent_over_2h` (true when last event is older than two hours).

### `GET /health`

`{ "ok": true, "service": "bot-events" }` — no auth.

## Tests

```bash
cd services/bot-events
npm test
```

## Deploy plan (needs Gideon's GO)

Do not run these steps until Gideon approves.

1. **Backup** — Snapshot or copy existing VPS state under `/opt/cleantechhub` and Caddy config (`/etc/caddy/Caddyfile` or project path in use).
2. **Infisical** — Ensure secret **`BOT_EVENTS_TOKEN`** exists in project `c84fe8b3`, env `prod`, path `/`. Confirm the VPS Infisical login can read it.
3. **Install tree** — Deploy this `services/bot-events` directory to `/opt/cleantechhub/bot-events` (from merged PR). No secrets in the tree.
4. **Data directory** — Create `/var/lib/cleantechhub/bot-events`, owned by `www-data`, mode `750`.
5. **systemd** — Copy `bot-events.service` to `/etc/systemd/system/bot-events.service`, adjust paths if needed, then `systemctl daemon-reload`, `systemctl enable --now bot-events`, `systemctl status bot-events`.
6. **Caddy** — Merge `Caddy.snippet` into the VPS Caddyfile (hostname confirmed with Gideon). Run `caddy validate --config /etc/caddy/Caddyfile`, then `systemctl reload caddy`.
7. **Smoke** — `curl -s http://127.0.0.1:8795/health` on VPS; test authenticated ingest with bearer token; confirm GET routes via browser after Google auth.

## Security notes

- Service binds **127.0.0.1** only.
- Ingest is **bearer-only** at the app layer; Caddy does not apply `forward_auth` to `POST /event`.
- Read routes rely on **auth.cleantechhub.net** Google gate at Caddy.
