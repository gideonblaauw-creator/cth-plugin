# Shared Google login (oauth2-proxy + Caddy)

Central Google SSO for VPS-hosted Caddy apps via [oauth2-proxy](https://oauth2-proxy.github.io/oauth2-proxy/) on `127.0.0.1:4180` and `forward_auth` in Caddy.

## Scope

- **In scope:** VPS Caddy sites under `*.cleantechhub.net` that you explicitly gate with the snippets.
- **Out of scope:** Vercel-hosted decks, **dataroom**, **decks**, and **mubon** (do not enable shared SSO on those without a separate decision).
- **NCUK data room guests:** If dataroom were gated with this stack, guests would need Google accounts on the allowlist or `@cleantechhub.net` — plan accordingly before any dataroom rollout.

## Prerequisites

1. Google OAuth client with redirect URI `https://auth.cleantechhub.net/oauth2/callback`.
2. Infisical project **cth-agents**, env **prod**, path **`/`**:
   - `OAUTH2_PROXY_CLIENT_ID`
   - `OAUTH2_PROXY_CLIENT_SECRET`
   - `OAUTH2_PROXY_COOKIE_SECRET` (32-byte base64)
3. DNS **A** `auth.cleantechhub.net` → VPS (`51.195.45.77`).
4. Machine identity: `/etc/gideon-tracker/infisical.env` (see `/opt/cth-backups/lib/infisical-runtime.sh`).

## Rollout order

1. Install oauth2-proxy binary (e.g. v7.15.5 linux-amd64) to `/usr/local/bin/oauth2-proxy`.
2. Deploy `/etc/oauth2-proxy/oauth2-proxy.cfg` from `docs/infra/oauth2-proxy/oauth2-proxy.cfg.template` and allowlist from `allowlist.txt.example`.
3. Install `oauth2-proxy-start.sh` → `/usr/local/lib/oauth2-proxy/` and `oauth2-proxy.service` → `/etc/systemd/system/`; `systemctl enable --now oauth2-proxy`.
4. Copy Caddy snippets from `docs/infra/caddy/` to `/etc/caddy/Caddyfile.d/`.
5. In `/etc/caddy/Caddyfile`, **before** the pilot site import, add:
   ```caddy
   import /etc/caddy/Caddyfile.d/oauth2-proxy.snippet.caddy
   import /etc/caddy/Caddyfile.d/auth.cleantechhub.net.caddy
   ```
6. `touch /var/log/caddy/auth.cleantechhub.net.log && chown caddy:caddy` (first deploy only).
7. `caddy validate --config /etc/caddy/Caddyfile` then **`systemctl reload caddy`** (never restart).
8. Pilot: `origo-staging.data.cleantechhub.net` (see `origo-staging.data.cleantechhub.net.caddy`).
9. Roll additional hosts one at a time: site-level `import oauth2_proxy_handle_unauth`, protected `handle` with `import oauth2_proxy_forward_auth`.
- proposals dashboard gated 22 Oct 2026 (slugs stay open); decks pending decision

## Allowlist how-to

1. Edit `/etc/oauth2-proxy/allowlist.txt` (one email per line).
2. `systemctl restart oauth2-proxy` (config reload is enough for allowlist file changes in most cases; restart if unsure).

Domain rule: `email_domains = cleantechhub.net` plus allowlist for non-`@cleantechhub.net` addresses if ever needed.

## Verification

```bash
# DNS
getent hosts auth.cleantechhub.net

# Proxy health (via auth vhost)
curl -sI --resolve auth.cleantechhub.net:443:51.195.45.77 \
  https://auth.cleantechhub.net/oauth2/ping | head -1
# expect HTTP/2 200

# Pilot (needs valid TLS for the pilot hostname)
curl -sI --resolve origo-staging.data.cleantechhub.net:443:51.195.45.77 \
  https://origo-staging.data.cleantechhub.net/
# expect 302 → https://auth.cleantechhub.net/oauth2/start?rd=...
```

Local: `curl -sI http://127.0.0.1:4180/oauth2/ping` → 200.

## Rollback

1. Restore backups under `/root/*.bak-oauth-<UTC>` for `/etc/caddy/Caddyfile`, touched `Caddyfile.d` files, and oauth2-proxy paths.
2. Disable pilot and auth vhost imports in `Caddyfile`; restore prior `origo-staging.data.cleantechhub.net.caddy`.
3. `caddy validate --config /etc/caddy/Caddyfile && systemctl reload caddy`
4. `systemctl disable --now oauth2-proxy`

One-liner after restoring files from a known backup timestamp:

```bash
sudo cp /root/Caddyfile.bak-oauth-<UTC> /etc/caddy/Caddyfile && \
sudo cp /root/origo-staging.data.cleantechhub.net.caddy.bak-oauth-<UTC> \
  /etc/caddy/Caddyfile.d/origo-staging.data.cleantechhub.net.caddy && \
sudo rm -f /etc/caddy/Caddyfile.d/auth.cleantechhub.net.caddy \
  /etc/caddy/Caddyfile.d/oauth2-proxy.snippet.caddy && \
sudo caddy validate --config /etc/caddy/Caddyfile && sudo systemctl reload caddy && \
sudo systemctl disable --now oauth2-proxy
```

Replace `<UTC>` with your backup suffix (e.g. `20261022T193702Z`).
