# Caddy routing — `/ncuk` and Docmost

## Docmost subpath limitation

Docmost **does not support** installation behind a URL subpath ([issue #966](https://github.com/docmost/docmost/issues/966)). `APP_URL` must be the **site root** (for this host: `https://dataroom.cleantechhub.net`), not `https://dataroom.cleantechhub.net/ncuk`.

## Public URL contract

Reviewers bookmark **`https://dataroom.cleantechhub.net/ncuk`**. Caddy implements that path as follows.

| Mode (`NCUK_ROOM_MODE`) | `/ncuk` behaviour | Docmost app |
|-------------------------|-------------------|-------------|
| `docmost` (primary) | HTTP Basic Auth, then **302 redirect** to `/` (same host, same auth session) | `reverse_proxy` on `/`, `/api/*`, `/socket.io/*`, and static asset paths Docmost needs |
| `fallback` | Basic Auth, then **Docusaurus static** under `/ncuk/` (`handle_path`) | Containers stopped or not routed |

Local verification (22 Oct 2026): subpath `reverse_proxy` with `handle_path` was **not** used for Docmost because asset URLs break. Redirect + root proxy is the supported pattern.

## Prefix handling checklist

1. Set `APP_URL=https://dataroom.cleantechhub.net` in `.env.generated`.
2. Reload Caddy after changing `caddy.env` (bcrypt hash from Infisical password).
3. Confirm WebSockets: Caddy forwards `Upgrade` and `Connection` by default on `reverse_proxy`.
4. Hit `https://dataroom.cleantechhub.net/ncuk` → login → lands on Docmost setup or workspace.
5. Health: `GET https://dataroom.cleantechhub.net/api/health` (through the same site block, authed).

## Fallback

Build Docusaurus with `baseUrl: '/ncuk/'`, rsync `build/` to `NCUK_FALLBACK_ROOT` on the VPS, set `NCUK_ROOM_MODE=fallback`, reload Caddy.
