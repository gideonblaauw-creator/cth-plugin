# CleantechHUB AI Apps (`apps.cleantechhub.net`)

Self-hosted copies of four [AI Apps for Good](https://aiappsforgood.org/) tools, gated behind Google SSO, with a same-origin LLM proxy (OpenRouter).

## Repo layout

| Path | Role |
| --- | --- |
| `pitch-builder/`, `mel-builder/`, `compass/`, `tough-conversations/` | Static `index.html` + agent `rubric.json` |
| `llm-proxy/` | Node 22 proxy (`127.0.0.1:8796`) |
| `LICENCES.md` | In-page licence audit |
| `scripts/prepare-apps.py` | Regenerate HTML from upstream tarball (HITL) |

VPS static roots: `/opt/cth-apps/<slug>/` (rsync from this tree, excluding `llm-proxy` and `scripts`).

## Deploy steps (OVH VPS — Gideon / Infrastructure)

1. **DNS** — `apps.cleantechhub.net` **A** record → same OVH VPS IP as `decks.cleantechhub.net`.
2. **Static apps** — from a machine with repo access:
   ```bash
   rsync -av --delete \
     services/cth-apps/pitch-builder/ \
     services/cth-apps/mel-builder/ \
     services/cth-apps/compass/ \
     services/cth-apps/tough-conversations/ \
     USER@VPS:/opt/cth-apps/
   ```
   (Run four rsyncs into `/opt/cth-apps/<slug>/`, or one rsync of the parent with excludes for `llm-proxy`, `scripts`, `*.md`.)
3. **LLM proxy** — copy `llm-proxy/server.js` to `/opt/cleantechhub/cth-apps-llm-proxy/`, install `llm-proxy/cth-apps-llm-proxy.service` under `/etc/systemd/system/`, `systemctl daemon-reload`, `systemctl enable --now cth-apps-llm-proxy`. Secret: `OPENROUTER_API_KEY` via `infisical run` (project `c84fe8b3`, env `prod`, path `/`).
4. **Caddy** — merge `deploy/caddy/apps.cleantechhub.net.caddy` into the VPS Caddyfile; `caddy validate --config /etc/caddy/Caddyfile`; `systemctl reload caddy`.
5. **Smoke** — authenticate via Google gate, open each app path, confirm `/api/llm` returns JSON (not CORS errors).

## Local verification (no secrets)

```bash
node --check services/cth-apps/llm-proxy/server.js
# Mock upstream + proxy test — see llm-proxy/README snippet in commit scripts or run test script in CI.
```

## Regenerate from upstream HTML

Place tarball files under `/tmp/ai-apps-src/ai-apps-src/` and run:

```bash
python3 services/cth-apps/scripts/prepare-apps.py
```
