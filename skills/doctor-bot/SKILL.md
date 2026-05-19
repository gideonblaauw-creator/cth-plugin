---
name: doctor-bot
description: >
  Invoke, interpret, or extend Doctor_Bot — Gideon's infrastructure health agent
  that monitors MCP connectors, the OVH VPS (BookStack, Sustenttia Chroma,
  Caddy, MariaDB, TLS certs, disk, memory), and Pipedream workflows. Use this
  skill whenever the user says "run doctor_bot", "check infra health", "what's
  broken in my stack", "is BookStack up", "are my MCPs healthy", "check the
  VPS", "did the nightly health run fail", or references the doctor-bot
  dashboard / systemd timer. ALSO trigger when Claude is asked to add a new
  check, tweak a threshold, extend to a new service, or interpret a RED/AMBER
  Slack digest. Do NOT attempt to modify Doctor_Bot without reading this skill
  — it documents where the code lives, deploy conventions (VPS /opt/doctor-bot/
  + Cowork artifact), and the non-destructive contract.
---

# Doctor_Bot — Infrastructure Health Agent

Gideon's read-only monitor across three layers of the CleantechHUB stack.
If you're editing checks, adding targets, or interpreting a digest, this is
the entry point.

---

## 1. What Doctor_Bot is (and isn't)

Doctor_Bot is a **two-deployment** health agent:

| Deployment | Where | What it checks | When to use |
|---|---|---|---|
| **Cowork artifact** | `Doctor_Bot — MCP Health` in the Cowork sidebar | All 11 MCP connectors (Drive, Gmail, Notion, Canva, Miro, Buffer, monday, Slack, Composio, QuickBooks, Windsor) | Ad-hoc: before a campaign, after a re-auth, when "a tool feels off" |
| **VPS systemd timer** | `/opt/doctor-bot/` on the OVH VPS (`ssh vps`), fires daily 06:00 COT | BookStack + Chroma containers, disk, memory, TLS cert, Caddy, MariaDB, Pipedream workflow error rates, public HTTP pings | Passive overnight monitor. Posts digest to `#ops-health`. |

**Non-destructive by design.** Doctor_Bot only reads. It never restarts, posts,
deletes, or mutates state. Any "heal" action belongs behind an explicit `--heal`
flag that does not yet exist (Phase 6, deferred).

---

## 2. How to invoke it

### Interactive (Cowork)

1. Open the Cowork sidebar → **Doctor_Bot — MCP Health** artifact.
2. The page live-probes every connector via `window.cowork.callMcpTool`.
3. Cards render green/amber/red. Latency bar chart below.
4. Click *Export JSON* to grab a snapshot for a ticket or a retro.
5. Cowork's built-in **Reload** button in the artifact header re-runs every check.

### Ad-hoc on the VPS

```bash
ssh vps 'cd /opt/doctor-bot && python3 runner.py --dry-run'   # no Slack, no log
ssh vps 'cd /opt/doctor-bot && python3 runner.py --json-only' # just the JSON
ssh vps 'cd /opt/doctor-bot && python3 runner.py'             # full run + Slack + log
```

Skip a layer for one run:

```bash
ssh vps 'cd /opt/doctor-bot && python3 runner.py --skip pipedream'
```

### Check the scheduler

```bash
ssh vps 'systemctl status doctor-bot.timer doctor-bot.service --no-pager'
ssh vps 'journalctl -u doctor-bot.service -n 200 --no-pager'
ssh vps 'tail -50 /opt/doctor-bot/logs/runs.log | jq .'
```

### Skills audit (Phase 2)

Separate one-shot script — scans SKILL.md files anywhere, emits JSON + table:

```bash
# auto-discovers /mnt/skills/user, /mnt/skills/public, ~/.claude/skills, plugin cache
bash skills_audit.sh

# explicit roots, custom thresholds, custom output path:
bash skills_audit.sh --stale-days 60 --min-desc-len 80 --json-out audit.json ~/.claude/skills
```

---

## 3. Status model

| Icon | Label | Meaning | Action |
|---|---|---|---|
| 🟢 | GREEN | All checks pass, latency normal | None |
| 🟡 | AMBER | Reachable but slow, thin frontmatter, stale mtime, or warn threshold breached | Investigate at convenience |
| 🔴 | RED | Unreachable, auth failed, cert < 14d, disk > 85%, error rate > 50% | Investigate **today** |
| ⚫ | UNKNOWN | Check couldn't run (missing API key, module crashed) | Fix the probe, not the service |

Severity across a layer = worst individual status in that layer.
Overall status = worst layer status.

---

## 4. Where things live

```
/Users/gideonblaauw/Documents/Claude/Projects/Claude Infrastructure/doctor-bot/
├── phase-1-dashboard/         # README + pointer — actual artifact lives in Cowork
├── phase-2-skills-audit/
│   └── skills_audit.sh
├── phase-3-vps-runner/         # deploys to vps:/opt/doctor-bot/
│   ├── runner.py
│   ├── checks/                 # vps_checks, pipedream_checks, http_pings
│   ├── reporters/              # slack_reporter
│   ├── systemd/                # .service + .timer units
│   ├── docker-compose.yml      # optional containerised variant
│   ├── .env.example
│   └── README.md
└── phase-5-skill/doctor-bot/
    └── SKILL.md                # this file
```

On the VPS the runner lives at `/opt/doctor-bot/` next to BookStack and
Sustenttia — per the [dual-desktop-macos] §10 convention (every long-running CTH
thing goes on the one VPS, no new hosts).

---

## 5. Extending Doctor_Bot

### Adding a new VPS check

Drop a function in `checks/vps_checks.py` that returns a dict of the shape:

```python
{"layer": "vps", "name": "<name>", "status": "GREEN|AMBER|RED|UNKNOWN",
 "latency_ms": <int or None>, "detail": "<human-readable>"}
```

Append it to the `run()` list at the bottom of the file. No registration,
no decorator — the module-level `run()` is the whole contract.

### Adding a new public HTTP endpoint

Append a `(name, url, expected_status)` tuple to `TARGETS` in
`checks/http_pings.py`. That's it.

### Adding a new MCP connector to the Cowork artifact

Edit the `CONNECTORS` array in the artifact HTML:

```js
{ id: 'foo', name: 'Foo', tool: 'mcp__<server>__<tool>', args: { ... } }
```

**First** call the tool once in a chat to verify its real parameter names
(MCP wrappers often rename params vs the underlying API). Only then add it.
See the `composio` skill for the tool-search/shape-verification pattern.

### Changing a threshold

Edit `.env` on the VPS, not code. The runner re-reads `.env` each run via
`EnvironmentFile=` in the systemd unit.

---

## 6. Interpreting a digest

Typical healthy Slack message:

```
🟢 Doctor_Bot Daily Report — 2026-04-25T11:00:03+00:00
Overall: GREEN  green=11  amber=0  red=0
Layer        Status
─────────────────────
http         🟢 GREEN
pipedream    🟢 GREEN
vps          🟢 GREEN
```

Typical degraded:

```
🟡 Doctor_Bot Daily Report — …
Overall: AMBER  green=9  amber=2  red=0
…
Attention:
• 🟡 `vps/disk:/opt` — 74% used
• 🟡 `pipedream:CLP26 Publisher` — errors 3/42; error-rate 7%; last-run 2.1h ago
```

Rules of thumb:

- `vps/disk:*` AMBER → run the `mac-storage-hygiene` companion playbook on the
  VPS (`du -h --max-depth=1 /opt | sort -h`) to find the growth.
- `vps/tls:*` RED within 14 days → Caddy should auto-renew; check
  `systemctl status caddy` + `journalctl -u caddy -n 200` and
  `curl -I https://wiki.cleantechhub.net`.
- `pipedream:*` RED → open the workflow URL, inspect recent executions in the
  Pipedream UI. Don't clear the queue unless age > 24h (Phase 6 rule).
- `http/bookstack` RED while `vps/docker:bookstack` GREEN → Caddy or DNS issue,
  not the container.

---

## 7. Non-destructive contract (keep this true)

Any PR / edit that adds write-side effects — restart, delete, post, modify —
**must**:

1. Gate the action behind a `--heal` CLI flag (opt-in per run).
2. Dry-run first: log what would happen, then do it on a second pass.
3. Document the safeguard in this SKILL.md before shipping.

This exists because nothing erodes trust in a monitoring tool faster than one
accidental delete.

---

## 8. Related skills

- `dual-desktop-macos` — **why** the runner lives on the CTH VPS and not somewhere else (§10).
- `bookstack` — Doctor_Bot monitors this container; the skill has BookStack-specific ops.
- `slack` — the digest destination; channel ID resolution rules live here.
- `social-media-campaign` — owns the Pipedream workflows Doctor_Bot watches.
- `mac-storage-hygiene` — companion for disk-pressure alerts.
- `composio` / `windsor-ai` / `buffer` / etc. — per-connector reference for MCP calls
  used by the Cowork artifact.

---

*Doctor_Bot v1.0 — April 2026. Owned by Gideon Blaauw, CleantechHUB Desktop 1.
Code lives at `/Users/gideonblaauw/Documents/Claude/Projects/Claude Infrastructure/doctor-bot/`
and deploys to `vps:/opt/doctor-bot/`.*
