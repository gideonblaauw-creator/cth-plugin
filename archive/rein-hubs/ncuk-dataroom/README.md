# NCUK REIN data room (build pack)

Deployable draft for **Docmost** on the OVH VPS at **`https://dataroom.cleantechhub.net/ncuk`**, with **Docusaurus** fallback at the same path.

| Artifact | Purpose |
|----------|---------|
| `PLAN.md` | Research and recommendation (PR #75) |
| `docker-compose.yml` | Docmost + PostgreSQL + Redis (RAM caps) |
| `caddy/Caddyfile.snippet` | TLS site, Basic Auth, `/ncuk` routing |
| `caddy/ROUTING.md` | `APP_URL` vs subpath (Docmost limitation) |
| `scripts/deploy-prep.sh` | Infisical → `caddy.env` + `.env.generated` |
| `scripts/health-check.sh` | Post-deploy smoke |
| `scripts/validate-local.sh` | `docker compose config` + `caddy validate` |
| `seed/` | Space structure, start page, viewer role (placeholders) |
| `fallback/docusaurus/` | Static skeleton (REIN colours) |
| `DEPLOY.md` | Runbook |

**Secrets:** never in git. Basic Auth user `rein`; bcrypt hash generated at deploy from Infisical `NCUK_DATAROOM_BASIC_AUTH_PASSWORD`.

**Brand (REIN):** `#335d4f`, `#ff6633`, `#666666` in fallback theme; Docmost UI theming is limited in OSS — use space names and landing copy only.

**Status:** Draft PR — no VPS deploy, DNS, or sharing in this job.
