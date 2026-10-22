# DEPLOY — NCUK REIN data room (Docmost + fallback)

**Scope:** OVH VPS Docker stack + Caddy snippet. **No deploy in this PR.** Apply only after Gideon GO on DNS and REIN HOLD.

## Host facts (22 Oct 2026)

| Item | Value |
|------|--------|
| VPS IPv4 | `51.195.45.77` |
| RAM | ~47 GB total; ~21.6 GB free at last check |
| Swap | **100% used** — set hard memory caps on this stack |
| Swap pressure note | The crash-looping `sustenttia-mcp` systemd unit adds swap pressure; **out of scope** for this job (Infrastructure tracks separately). |

## DNS (Gideon GO only)

| Type | Name | Target | TTL |
|------|------|--------|-----|
| **A** | `dataroom.cleantechhub.net` (or host `dataroom` in zone `cleantechhub.net`) | `51.195.45.77` | 300 (short until stable) |

Do **not** apply the A record until Gideon approves. After GO: `dig +short dataroom.cleantechhub.net A` must return `51.195.45.77`.

TLS: existing VPS Caddy obtains Let's Encrypt certs once DNS propagates.

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

- `caddy.env` — `NCUK_BASIC_AUTH_HASH` via `caddy hash-password`
- `.env.generated` — Docmost `APP_SECRET`, DB password, `DATABASE_URL`

## Memory limits (compose)

| Service | mem_limit | memswap_limit |
|---------|-----------|---------------|
| docmost | 1g | 1g |
| postgres | 768m | 768m |
| redis | 256m | 256m |

All services: `restart: unless-stopped`.

## Docker

1. Confirm external Caddy network name (`CADDY_DOCKER_NETWORK`, default `caddy`) matches the live VPS.
2. Start stack:

```bash
docker compose --env-file .env.generated up -d
```

3. Docmost setup UI: `https://dataroom.cleantechhub.net/` (after DNS + Caddy), edge login `rein` + Infisical password.

`APP_URL` must be **`https://dataroom.cleantechhub.net`** (root). Public entry path **`/ncuk`** is implemented in Caddy (redirect). See `caddy/ROUTING.md`.

## Caddy

1. Merge `caddy/Caddyfile.snippet` into the host Caddyfile.
2. Export vars from `caddy.env` before reload (or use your Infisical sync pattern).
3. `caddy validate --config /etc/caddy/Caddyfile`
4. `caddy reload --config /etc/caddy/Caddyfile`

## Seed content (operator)

Follow `seed/README.md`: three spaces (Energy, Health, Education), guided start page, viewer read-only. Google Drive source folders are linked in seed templates (view-only URLs, no tokens).

## Health check

```bash
./scripts/health-check.sh https://dataroom.cleantechhub.net
```

Docmost: `GET /api/health` → 200 when healthy (may be 401 if Basic Auth covers `/api`; adjust Caddy matchers if health must be unauthenticated internally).

Entry path: `https://dataroom.cleantechhub.net/ncuk` → Basic Auth → Docmost workspace (via redirect).

## Fallback (deadline 27 Oct 2026 17:00 UTC)

If Docmost is not healthy by then:

1. Build static site: `fallback/docusaurus/` → `npm ci && npm run build`
2. Rsync `build/` to `NCUK_FALLBACK_ROOT` on VPS.
3. Set `NCUK_ROOM_MODE=fallback` in `caddy.env`, reload Caddy.
4. Same Basic Auth on `/ncuk/*`.

## Rollback

1. Set `NCUK_ROOM_MODE=fallback` **or** remove the `dataroom.cleantechhub.net` site block from Caddy and reload.
2. `docker compose --env-file .env.generated down` (keeps volumes unless `-v`).
3. DNS A record can stay; disable by removing site block or pointing to maintenance page.
4. Restore Docmost: `docker compose up -d`, PG data remains in volume `ncuk-dataroom-pg`.

## Backup

- `docker exec ncuk-dataroom-db pg_dump -U docmost docmost > ncuk-docmost-$(date +%F).sql`
- Include volume names in Infrastructure backup job notes.

## Open items (post-merge)

- [ ] Gideon GO on DNS A record
- [ ] Confirm live Docker network name for Caddy
- [ ] Infisical keys populated
- [ ] Docmost workspace setup + seed spaces (Drive exports)
- [ ] REIN HOLD cleared before credentials to Laurence
- [ ] Legal AGPL note if Docmost image is forked (use upstream pin only)
