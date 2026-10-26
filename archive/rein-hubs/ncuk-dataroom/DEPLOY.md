# DEPLOY — NCUK REIN data room (Docmost + fallback)

**Scope:** OVH VPS Docker stack + **host** Caddy (`systemd`). **No deploy in this PR.** Apply only after Gideon GO on DNS and REIN HOLD.

## Host facts (22 Oct 2026)

| Item | Value |
|------|--------|
| VPS IPv4 | `51.195.45.77` |
| RAM | ~47 GB total; ~21.6 GB free at last check |
| Swap | **100% used** — set hard memory caps on this stack |
| Swap pressure note | The crash-looping `sustenttia-mcp` systemd unit adds swap pressure; **out of scope** for this job (Infrastructure tracks separately). |
| Caddy | **Host systemd** `caddy.service` — **not** in Docker |
| Docmost upstream | `127.0.0.1:3076` → container `:3000` (change port only if 3076 is taken) |

## DNS (Gideon GO only)

| Type | Name | Target | TTL |
|------|------|--------|-----|
| **A** | `dataroom.cleantechhub.net` (or host `dataroom` in zone `cleantechhub.net`) | `51.195.45.77` | 300 (short until stable) |

Do **not** apply the A record until Gideon approves. After GO: `dig +short dataroom.cleantechhub.net A` must return `51.195.45.77`.

TLS: host Caddy obtains Let's Encrypt certs once DNS propagates.

## VPS paths (Lane B — not this git repo on disk)

Suggested deploy root on VPS:

`/opt/claude-files/Projects/REIN-Hubs/ncuk-dataroom/`

Copy or rsync `docker-compose.yml`, `scripts/`, `caddy/`, and `fallback/` from this archive after merge.

## Infisical (`cth-agents`, prod)

Create or confirm these **key names only** (values never in git):

| Key | Purpose |
|-----|---------|
| `NCUK_DATAROOM_BASIC_AUTH_PASSWORD` | Caddy Basic Auth passphrase (≥20 chars; not the string `rein`) |
| `NCUK_DATAROOM_BASIC_AUTH_USER` | Optional; default `rein` |
| `NCUK_DOCMOST_APP_SECRET` | `openssl rand -hex 32` |
| `NCUK_DOCMOST_DB_PASSWORD` | PostgreSQL password for `docmost` user |
| `NCUK_DOCMOST_VIEWER_PASSWORD` | Docmost viewer account (operator sets in UI) |

### Deploy-time secret pull

On the VPS (machine identity or Infisical login):

```bash
cd /opt/claude-files/Projects/REIN-Hubs/ncuk-dataroom
chmod +x scripts/deploy-prep.sh
./scripts/deploy-prep.sh
```

Outputs (gitignored pattern):

- `caddy.env` — `NCUK_BASIC_AUTH_HASH`, `NCUK_DOCMOST_UPSTREAM=127.0.0.1:3076`, mode and fallback paths
- `.env.generated` — Docmost `APP_SECRET`, DB password, `DATABASE_URL`, `DOCMOST_HOST_PORT`

## Memory limits (compose)

| Service | mem_limit | memswap_limit |
|---------|-----------|---------------|
| docmost | 1g | 1g |
| postgres | 768m | 768m |
| redis | 256m | 256m |

All services: `restart: unless-stopped`.

## Docker

Docmost, PostgreSQL, and Redis use a **private** bridge (`ncuk-dataroom-internal`). Only Docmost publishes **`127.0.0.1:3076:3000`**. Postgres and Redis expose **no** host ports.

```bash
docker compose --env-file .env.generated up -d
curl -sf http://127.0.0.1:3076/api/health
```

Docmost setup UI (after DNS + Caddy): `https://dataroom.cleantechhub.net/` with edge login `rein` + Infisical password.

`APP_URL` must be **`https://dataroom.cleantechhub.net`** (root). Public entry **`/ncuk`** redirects to `/`. See `caddy/ROUTING.md`.

## Caddy (host systemd)

1. Copy site file:

```bash
sudo cp caddy/dataroom.cleantechhub.net.caddy /etc/caddy/Caddyfile.d/
```

2. Add an explicit import to `/etc/caddy/Caddyfile` (there is no glob import on this host):

```
import /etc/caddy/Caddyfile.d/dataroom.cleantechhub.net.caddy
```
3. Point `caddy.service` at `caddy.env` (from `deploy-prep.sh`), e.g. `EnvironmentFile=/opt/claude-files/Projects/REIN-Hubs/ncuk-dataroom/caddy.env`.
4. Validate and reload:

```bash
sudo caddy validate --config /etc/caddy/Caddyfile
sudo systemctl reload caddy
```

## Seed content (operator)

Follow `seed/README.md`: three spaces (Energy, Health, Education), guided start page, viewer read-only. Google Drive source folders are linked in seed templates (view-only URLs, no tokens).

## Health check

On VPS (direct upstream):

```bash
./scripts/health-check.sh
```

Public URL (after TLS + DNS):

```bash
./scripts/health-check.sh https://dataroom.cleantechhub.net
```

Docmost upstream: `GET http://127.0.0.1:3076/api/health` → 200. Public `/api/health` may return 401 when Basic Auth wraps the site.

Entry path: `https://dataroom.cleantechhub.net/ncuk` → Basic Auth → redirect → Docmost workspace.

## Fallback (deadline 27 Oct 2026 17:00 UTC)

If Docmost is not healthy by then:

1. Build static site: `fallback/docusaurus/` → `npm ci && npm run build`
2. Set `NCUK_FALLBACK_ROOT` in `caddy.env` to the `build/` directory **or** run `npm run serve -- --host 127.0.0.1 --port 3077` and set `NCUK_FALLBACK_UPSTREAM=127.0.0.1:3077`
3. Set `NCUK_ROOM_MODE=fallback` in `caddy.env`
4. `sudo caddy validate --config /etc/caddy/Caddyfile && sudo systemctl reload caddy`

Same Basic Auth on `/ncuk/*`.

## Rollback

1. Set `NCUK_ROOM_MODE=fallback` **or** remove `/etc/caddy/Caddyfile.d/dataroom.cleantechhub.net.caddy` and reload Caddy.
2. `docker compose --env-file .env.generated down` (keeps volumes unless `-v`).
3. DNS A record can stay; disable by removing site file or maintenance respond.
4. Restore Docmost: `docker compose up -d`, PG data remains in volume `ncuk-dataroom-pg`.

## Backup

- `docker exec ncuk-dataroom-db pg_dump -U docmost docmost > ncuk-docmost-$(date +%F).sql`
- Include volume names in Infrastructure backup job notes.

## Open items (post-merge)

- [ ] Gideon GO on DNS A record
- [ ] Confirm port `3076` is free on VPS (or set `DOCMOST_HOST_PORT` + `NCUK_DOCMOST_UPSTREAM`)
- [ ] Infisical keys populated
- [ ] `caddy.service` EnvironmentFile wired to `caddy.env`
- [ ] Docmost workspace setup + seed spaces (Drive exports)
- [ ] REIN HOLD cleared before credentials to Laurence
- [ ] Legal AGPL note if Docmost image is forked (use upstream pin only)
