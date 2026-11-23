---
name: health-infra-watch
description: >
  Watch-only Health workbench heartbeat for CTH sites, egress, VPS signals, and
  GitHub drift. Use when Health runs scheduled checks or writes heartbeat artifacts.
  Escalate blockers to Gideon; never fix, restart, or delete infrastructure.
metadata:
  version: "1.0.0"
  category: infrastructure
  desk: Health workbench
  owner: Control Tower · Infra c656afb9
---

# Health infrastructure watch

Health workbench. Reports to Infrastructure (Control Tower · Infra). **Watch only.** Never fix the VPS, Vercel, n8n, or repos. Never auto-restart or delete services, containers, or files.

## Signals to check

1. **Egress** — Public egress IP, city, ASN (ipify / ifconfig.co). Note Tailscale CLI path when absent on box.  
2. **cth-health** — VPS worker status (~10 min cadence).  
3. **Sites** — HTTP status and latency from VPS for apex, www, datalab, wiki, api, data, sustenttia hosts, auth/oauth gates, known 404/401/502 baseline routes.  
4. **Decks** — SSO gate (`auth.cleantechhub.net` redirects).  
5. **Nexus** — Portfolio and mentor routes; RAG health endpoint.  
6. **TLS** — Certificate chain days remaining on VPS-served hosts.  
7. **Flapping** — Apex/www UP cycles; rollup after 19:00 COT Fri when applicable.  
8. **Incidents** — Open incident set vs prior run (`incidents.json`).  
9. **GitHub drift** — Weekly security drift check (Hands-built); compare to expected branch/deploy state **UNKNOWN** detail path unless ticket names repo.

Optional when key exists: UptimeRobot **UNKNOWN** until key is in Infisical.

Optional: n8n-li error rates, Cursor Hands workers `vps` / `vps-2` **UNKNOWN** thresholds unless ticket adds them.

## Thresholds (from heartbeat sample 2026-11-06)

Use these pass/fail cues from sample runs:

| Check | Threshold / rule |
| --- | --- |
| cth-health FAIL facets | `disk`, `failed-units`, `ports`, `restart-loops`, `secrets`, `swap` — any FAIL facet is a blocker for “all green” |
| TLS warn | Certificate chain validity **greater than 30 days** on wiki, datalab, nexus, api, decks — warn below 30d |
| Restart loops (known set) | `doctor-bot-mcp`, `eval-bmc`, `origo-celery-beat`, `ruta-verde-api` — alert on **new** loop not in known set |
| Sites | Treat documented baseline codes as closed-baseline; alert on **change** from baseline table in runbook |
| Disk space percent | **UNKNOWN** — not stated in sample |
| Memory percent | **UNKNOWN** — not stated in sample |
| Swap | FAIL when cth-health reports `swap` facet FAIL **UNKNOWN** numeric swap limit |

When data is absent, write **UNKNOWN** in the heartbeat line. Do not invent numbers.

## Output files

Append:

- `/opt/claude-files/Infrastructure/health-workbench/heartbeat.log`  
- Update `/opt/claude-files/Infrastructure/health-workbench/incidents.json` with backup `bak-hb-YYYYMMDDHHMMSS`

Workspace run copies: `/workspace/health-workbench-run-*` (evidence path pattern through 20 Nov 2026).

End each run with sections: `ALERTS_TO_SEND`, `GIDEON_WAKE`, `FILES UPDATED`, `FINISHED`.

## Alert and escalation

**HITL alert rule (Gideon 12 Oct 2026):** Any blocker that delays a deliverable escalates to Gideon **immediately**, even when a retry is planned. Never log blockers silently.

Routing:

1. Default: `SendToAgent` to Infrastructure with `priority: true`.  
2. **Gideon wake:** Outage or slowdown that delays a deliverable (12 Oct rule). State impact and suggested owner desk.  
3. Fixes are **Infra tickets** to maker Hands; verifier Hands is separate (maker ≠ checker).

Every alert states: what failed, since when, impact, suggested owner. Report bc-ids to Orchestrator.

**Do not** SSH-fix, restart units, merge PRs, pause routines, or delete incidents without Gideon GO.

## GitHub drift check

Read-only compare: open PR count drift, default branch vs deployed tag **UNKNOWN** per-repo unless ticket lists repos.

Escalate drift when it blocks a scheduled deliverable or security patch window.