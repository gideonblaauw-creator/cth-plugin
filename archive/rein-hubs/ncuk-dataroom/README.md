# NCUK REIN data room (build pack)

Deployable draft for **Docmost** on the OVH VPS at **`https://dataroom.cleantechhub.net/ncuk`**, with **Docusaurus** fallback at the same path.

| Artifact | Purpose |
|----------|---------|
| `PLAN.md` | Research and recommendation (PR #75) |
| `docker-compose.yml` | Docmost + PostgreSQL + Redis; Docmost on `127.0.0.1:3076` only |
| `caddy/dataroom.cleantechhub.net.caddy` | Host site file → `/etc/caddy/Caddyfile.d/` |
| `caddy/ROUTING.md` | `APP_URL` vs subpath; host Caddy + localhost upstream |
| `scripts/deploy-prep.sh` | Infisical → `caddy.env` + `.env.generated` |
| `scripts/health-check.sh` | Localhost upstream + optional public URL |
| `scripts/validate-local.sh` | Compose YAML + `caddy validate` on site file |
| `seed/` | Space structure, start page, viewer role (placeholders) |
| `fallback/docusaurus/` | Static skeleton (REIN colours) |
| `DEPLOY.md` | Runbook |

**Caddy:** runs on the **host** as `systemd caddy.service` — not in Docker. Reload with `caddy validate --config /etc/caddy/Caddyfile` then `systemctl reload caddy`.

**Secrets:** never in git. Basic Auth user `rein`; bcrypt hash from Infisical `NCUK_DATAROOM_BASIC_AUTH_PASSWORD`.

**Brand (REIN):** `#335d4f`, `#ff6633`, `#666666` in fallback theme; Docmost UI theming is limited in OSS — use space names and landing copy only.

**Status:** Draft PR — no VPS deploy, DNS, or sharing in this job.
