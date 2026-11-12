# Claude folder health audit — 2026-10-19

Read-only audit of health-bot, monitoring, watchdog, uptime, heartbeat, and status material. Nothing was disabled, moved, or edited except this new report. `/opt/claude-files/secrets` was not opened.

Target the material is judged against:

- One Infra desk (Grok Bot) writes tickets.
- Maker Hands builds. A separate verifier Hands checks. Maker is not checker.
- A Health workbench (Grok Bot, id `fbc6f772`, reports to Infra) only watches and raises alerts. It never fixes.
- Signals: the `cth-health` status page served by Caddy, 10-minute worker and resource checks, a weekly security drift check, UptimeRobot as the outer layer, workers `vps` and `vps-2`, `n8n-li`, and sites (Datalab, Nexus, and the rest of the public set).

Hands `bc-8ec319df` ("VPS monitoring: inside checks + UptimeRobot outer layer + rulebook PR") was still running during this audit. Its output is the baseline in the next section. Archive items are judged against that baseline.

Granola has no meeting decision that assigns infrastructure watching, fixing, or alert routing. The only nearby note is about installing Sustenttia on a shared server. This audit follows the ticket text. [[3]](https://notes.granola.ai/d/75579702-1b0f-4bb0-b4af-643e144e636c)

## How this was searched

`grep -ril` (case-insensitive, binaries skipped) for `health`, `healthcheck`, `heartbeat`, `monitor`, `watchdog`, `uptime`, `uptimerobot`, `status page`, `alert`, `drift`, `cth-health`, plus the phrases `doctor-bot`, `health bot`, and `health check`.

Scope: `/opt/claude-files` with extra weight on `Infrastructure`, `infrastructure`, `Scheduled`, `rakazo-sync`, `cth`, `grok-agent-data`, and `sessions`. Sessions were searched by filename and by grep. Full session notes were not read. Secrets, `node_modules`, `.git`, virtualenvs, and the vendored Lightdash tree were excluded.

Also checked: debian, root, `clp`, and `cth` crontabs; user and system systemd timers; `/etc/systemd/system` units matching health, monitor, or watch; the live Caddyfile; `cth-plugin` skills.

Noise that is not itemized row by row: mail-finder SQL backups, Rakazo desk log copies repeated inside each daily mirror, ESG and campaign docs that merely contain the word "health", and Lightdash demo files. The Rakazo daily series is one row.

## What Hands bc-8ec319df is building (baseline, not an old item)

Observed on this VPS at 14:29 UTC on 19 Oct 2026. This is the new checker. It is in progress. This audit did not change it.

| Piece | Where | State at audit time |
|---|---|---|
| Checker | `/opt/cth-monitor/monitor.py` (mtime 2026-10-19 14:13 UTC, 746 lines) | Present. `health` and `security` commands. Prints names, not secret values. |
| 10-minute timer | `cth-monitor-health.timer` / `.service` (mtime 14:08 UTC) | **Enabled and active.** Next fire was 14:28 UTC. `OnUnitActiveSec=10min`. |
| Weekly security timer | `cth-monitor-security.timer` / `.service` | **Enabled.** First calendar fire Mon 06:20 UTC. Not yet run on that calendar (`LAST` was blank). |
| Status page | Caddy site `wiki.cleantechhub.net`, handle `/.well-known/cth-health`, file `/var/lib/cth-monitor/public/cth-health.txt` | **Live.** `curl` to `https://wiki.cleantechhub.net/.well-known/cth-health` returned HTTP 200. |
| UptimeRobot notes | `/opt/cth-monitor/uptimerobot-setup.sh` | Documentation only. The script says the API key is not on this VPS and that it does not call the API. |
| Rollback helper | `/opt/cth-monitor/rollback.sh` | Present. Not run. |

Checks already coded:

- Workers: user units `cursor-worker.service` and `cursor-worker-vps-2.service` (the `vps` and `vps-2` workers). Alert if not `active`, or if `NRestarts` rises by more than 3 since the previous tick. Both units were `active` with `NRestarts=0` at audit time.
- Resources, every 10 minutes: disk at or above 85% (any non-virtual filesystem), swap above 80% for 3 consecutive ticks, any failed system or user service, any unit whose restart count jumps by more than 3.
- Security, weekly: sshd `passwordauthentication no` and `permitrootlogin no`, authorized-keys drift, fail2ban, public listeners, secret-looking assignments (names only). The status page marks security stale if that report is older than 8 days.
- Status body: `CTH_HEALTH_OK <time>` or `CTH_HEALTH_FAIL <names>`.
- Alert transport in this code: append `/var/lib/cth-monitor/alerts.log`, then Telegram to the harness allowlist on new and cleared items. The root-only state file that records whether Telegram accepted the send was not opened.

Page body at 14:18:06 UTC:

```
CTH_HEALTH_FAIL disk failed-units restart-loops swap
CHECKED 2026-10-19T14:18:06Z
```

`/mnt/data` was 90% full (167G of 196G) at the start of this audit, which is already past the 85% disk line. The alert log also recorded swap near 100% and restart-loop names `doctor-bot-mcp.service`, `eval-bmc.service`, and `sustenttia-mcp.service`. This audit did not investigate or repair those.

UptimeRobot, as written in the setup script (outer layer, created outside this VPS; keyword monitor still for Infra to add):

- HTTP `https://wiki.cleantechhub.net/`
- HTTP `https://datalab.cleantechhub.net/`
- HTTP `https://mubon.cleantechhub.net/login.html`
- HTTP `https://n8n-li.cleantechhub.net/`
- HTTP `https://appwrite.cleantechhub.net/`
- PING `51.195.45.77`
- Keyword still to add: `https://wiki.cleantechhub.net/.well-known/cth-health` must contain `CTH_HEALTH_OK`, 5-minute interval
- The script says not to add an UptimeRobot heartbeat monitor

Hands also has an unmerged branch `cursor/vps-hands-rule-c822` (commits `b994c62`, `5213cd5`) that adds the VPS Hands rule and this line to the harness: send monitoring alerts to Health workbench `fbc6f772`, which reports to Infra, with a separate read-only verifier Hands. That branch is not `main`. This audit did not touch that checkout.

`monitor.py` also contains `patch-caddy`. The live Caddyfile already has the health handle, so that command is a no-op today.

## Verdicts

`RELEVANT` — reuse as a Health workbench input. `MERGE` — useful idea to fold into the bc-8ec319df output. `STALE` — superseded or a different job. "Still runs" means a timer, cron, or n8n workflow is still scheduled. Nothing in the Still runs column was turned off.

| # | Path | Last modified | What it does | Still runs? | Verdict |
|---|---|---|---|---|---|
| 1 | `/etc/caddy/Caddyfile` handle `/.well-known/cth-health` on `wiki.cleantechhub.net` (Caddyfile mtime 2026-10-17 01:14 UTC; body file mtime 2026-10-19 14:18 UTC) | 2026-10-17 file; body today | Serves `/var/lib/cth-monitor/public/cth-health.txt` as plain text, `Cache-Control: no-store`. Confirmed HTTP 200 from localhost with the wiki host. | Caddy is active. The 10-minute timer now refreshes the body. | **RELEVANT** |
| 2 | `/opt/claude-files/infrastructure/vps-access-audit-2026-10-18.md` | 2026-10-19 13:35 UTC | Yesterday's access audit. Records doctor-bot succeeding as a unit, Rakazo sync succeeding, the `clp` health log empty since 31 Jul 2026, and n8n-li's error pile. Names the doctor-bot env file. Does not print secrets. | No. It is a document. | **RELEVANT** |
| 3 | `/opt/claude-files/infrastructure/n8n-li-cleanup-2026-10-19.md` | 2026-10-19 13:56 UTC | Today's n8n-li cleanup note. `decay_monitor` and `adgrant_monitor` are still active workflows and still aimed at Telegram. Names workflow ids. | No. It is a document. The workflows it names are in rows 13 and 14. | **RELEVANT** |
| 4 | `/opt/atlassian/doctor-bot/checks/vps_checks.py`, `system_health.py`, `http_pings.py` | 2026-07-31, 2026-04-27, 2026-07-15 | The check catalogue the new 10-minute job does not yet cover: TLS under 14 days on `wiki.cleantechhub.net`, disk amber 70% / red 85%, memory red 92%, load, apt, journal errors, and HTTP targets for wiki, Nexus pages, and several localhost `/health` ports. | Yes, because `doctor-bot.timer` calls the runner that imports them. See row 6. | **MERGE** |
| 5 | `/opt/atlassian/doctor-bot/README.md` and `/opt/claude-files/Projects/Claude Infrastructure/doctor-bot/HANDOFF_FINISH.md` | README 2026-04-27; handoff 2026-04-29 | States the original contract: read system state, do not restart services. Also describes a Slack digest and a Mac `rsync` deploy into `/opt/doctor-bot`. The read-only sentence matches the Health workbench. The deploy steps do not. | The README is not what systemd runs. The live runner is row 6. | **MERGE** (the read-only sentence only) |
| 6 | `/etc/systemd/system/doctor-bot.service` + `doctor-bot.timer`, code `/opt/atlassian/doctor-bot/runner.py` | Unit files 2026-05-21; runner 2026-07-03 | Daily infra digest at 11:00 UTC. Last run 2026-10-19 11:00:50 UTC, exit 0, summary RED (60 green, 10 amber, 35 red, 2 unknown). Posts Telegram (`telegram digest posted`, 928 chars) and then tries Jira. `--heal` exists for disk and TLS healers and is **not** in the unit, so today's run did not fix anything. | **Yes. Timer enabled.** Next run 2026-10-20 11:00 UTC. | **STALE** |
| 7 | `/opt/atlassian/doctor-bot/reporters/jira_reporter.py` and `jira_dispatcher.py` | 2026-05-21 / 2026-05-22 | Creates CTH-OPS Jira issues for amber/red findings. Today's run: HTTP 400 on `https://cleantechhub.atlassian.net/rest/api/3/issue` for every finding logged, then `0 created, 0 existing, 62 cleared`. | Yes, called at the end of every doctor-bot run. | **STALE** — dead channel |
| 8 | `/opt/atlassian/doctor-bot/reporters/slack_reporter.py` and `skills/doctor-bot/SKILL.md` Slack section | Reporter 2026-04-24; skill content last committed 2026-10-12 (`7b164e8`) | Skill still says post to Slack `#ops-health`, run `/opt/doctor-bot`, and check a timer at 06:00 UTC. The live runner does not import `slack_reporter`. The live timer is 11:00 UTC and the live code is `/opt/atlassian/doctor-bot`. | The Slack function is not on the daily path. The skill is what an agent will follow if it opens `doctor-bot`. | **STALE** — docs point at a channel the runner no longer posts to |
| 9 | `/opt/doctor-bot/` (second tree, `runner.py` mtime 2026-07-23) | 2026-07-23 | Older copy. Systemd `ExecStart` points at `/opt/atlassian/doctor-bot/runner.py`, not this tree. | No. | **STALE** |
| 10 | `/opt/claude-files/Projects/Claude Infrastructure/doctor-bot/` (`VPS_AUDIT_2026-05-07.md`, `VPS_FIXES_2026-05-07.md`, `phase-5-skill/`, `phase-3-vps-runner/.env.example`) | 2026-04-29 to 2026-05-07 | May 2026 handoff, audit, and fix list. `.env.example` names variables only; values were not copied into this report. | No. | **STALE** |
| 11 | `/etc/cron.d/rakazo-sync` and `/opt/claude-files/rakazo-sync/YYYY-MM-DD/{drift-report.md,babo-health.json}` | Cron file 2026-09-17; newest report 2026-10-18 23:00:03 UTC | Daily Rakazo mirror. Drift report counts desk-profile deltas. Babo probe is `http://127.0.0.1:8788/health` (last snapshot: HTTP 200, status `ok`, WhatsApp and Google `unknown`). This "drift" is desk-mirror drift, not the weekly sshd/keys/ports drift. Series runs 2026-09-17 through 2026-10-18. | **Yes.** Cron `0 23 * * *` America/Bogota, root, `/usr/local/bin/grok-rakazo-sync.sh`. | **STALE** |
| 12 | `clp` crontab → `/opt/clp-bot/scripts/health_check.py` | Script 2026-07-31 18:16 UTC | Wattson bot, OpenRouter, Odoo, BookStack, and cohort checks. Docstring says alert `CTH_OPS_BOT` ops group and DM Gideon, and stay silent when healthy. | **Yes.** `0 */6 * * *` as user `clp`. Journal shows starts at 00:00, 06:00, and 12:00 UTC today. Each cron session opened and closed in the same second. `/var/log/clp-wattson-health.log` is 0 bytes, mtime 2026-07-31 18:15 UTC. | **STALE** — scheduled, produces no log, so the Telegram path is not delivering |
| 13 | n8n-li workflow `bfqWFknxhNaxzLZi` `decay_monitor` | Noted 2026-10-19 in the cleanup doc | Monthly GSC decay compare, Telegram on a real drop. Debian crontab line is commented (`CUTOVER 2026-09-24`). Systemd has no unit. | **Yes in n8n** (`active=1`). Cron copy is off. | **STALE** for this workbench (SEO product check) |
| 14 | n8n-li workflow `o8URahr5QnLxZsdY` `adgrant_monitor`; unit `cth-adgrant_monitor.timer` | Unit 2026-06-26; workflow noted 2026-10-19 | Weekly Google Ad Grant compliance. Unit would run `/opt/cth-agents/agents/adgrant_monitor.py`. | **n8n active** (weekly Mon 12:00 UTC). **systemd timer disabled and inactive.** | **STALE** for this workbench (ads product check) |
| 15 | `/opt/claude-files/Projects/CTH - Social Media/cth-monitoring/` and `clp26_redesign/monitoring/github_actions_buffer_health.yml` | 2026-04-29 and 2026-04-25 | GitHub Action, daily 22:00 UTC, Buffer stuck/errored posts, Slack webhook on failure. | Not a VPS cron. Whether GitHub still runs it was not checked from this host. | **STALE** for this workbench |
| 16 | `cth-plugin` `skills/mac-scan-worker/SKILL.md` | In `main` as of 2026-10-12 | Runbook for the MacBook Air private worker `mac-scan`. "Worker down" means hold the Mac Scan desk. It is not a VPS probe. | No VPS timer. | **STALE** for this workbench (Mac-based) |
| 17 | `/opt/claude-files/Infrastructure/telegram-hitl/2026-09-28/n8n-li-health-after-tg-bridge-receipt.md` (+ `.json`) | 2026-09-28 21:59 UTC | One read-only receipt from `bc-48a31b01`. n8n-li was crash-looping that evening. | No. | **STALE** |
| 18 | `/opt/claude-files/Artifacts/doctor-bot-mcp-health/` and `/opt/claude-files/Artifacts/cth-newsletter-monitor/` | 2026-05-01 and 2026-04-28 | Old HTML dashboards (MCP tiles, newsletter monitor). | No. | **STALE** |
| 19 | `/opt/claude-files/sessions/2026-09-10/inbox.md` (and other session grep hits) | 2026-09-10 | No session filename contains health, heartbeat, watchdog, uptime, or monitor. Infrastructure session notes had no `doctor-bot`, `uptimerobot`, or `cth-health` lines. The 10 Sep inbox note uses "heartbeat" for the morning inbox send. | No. | **STALE** |
| 20 | `/etc/systemd/system/goodstack-watch.timer` | 2026-05-19 | Daily Goodstack grant digest, 13:00 UTC. Not an uptime check. | **Yes, enabled.** | **STALE** for this workbench |
| 21 | `/etc/systemd/system/origo-watcher.timer` | 2026-05-26 | Monthly Origo taxonomy source watcher. | **Yes, enabled.** Next fire 2026-11-01. | **STALE** for this workbench |
| 22 | `/opt/claude-files/Infrastructure/vps-scripts-n8n-audit/2026-09-24/AUDIT.md` | 2026-09-24 | Cutover inventory. Lists doctor-bot as KEEP and describes it as a Slack digest. Lists `decay_monitor` and `adgrant_monitor` as n8n pilots. Useful as a map of what moved to n8n. The Slack sentence is now wrong (row 8). | No. | **MERGE** (the KEEP versus cutover map) |
| 23 | `/opt/claude-files/grok-agent-data/agents/5dc64ea4-b416-4da3-bc8b-12fb507256f7/memory/profile.md` (Orchestrator; same sentence copied through `rakazo-sync/.../desks/rakazo-orch/profile.md`) | Profile memory 2026-09-24; Rakazo copy refreshed 2026-10-18 | One line from 2026-08-17: a loop needs heartbeat, skill, maker≠checker, connectors, verifier. | The Rakazo cron recopies it. The sentence is not itself a job. | **MERGE** |

`Scheduled/` and `/opt/claude-files/cth/` had no health-bot, uptime, or watchdog documents.

Other Caddy `/health` routes are app endpoints, not the workbench page: `cdn.cleantechhub.net /healthz`, `api.cleantechhub.net /health`, `origo.data.cleantechhub.net /health`, `agents.cleantechhub.net /seo/health`, `vps.tail6b9bda.ts.net /health`. Leave them with the apps they front.

Debian's crontab has the old `decay_monitor.py` line commented out. Root's crontab has no health-bot line. No user systemd timers are installed for `debian`.

## Duplicates with bc-8ec319df

Already implemented there, so the old copy should not be wired in again:

- 10-minute worker check for `vps` and `vps-2` (`cursor-worker.service`, `cursor-worker-vps-2.service`).
- 10-minute disk, swap, failed-unit, and restart-loop checks, with the thresholds in the baseline section.
- Weekly security drift (sshd, keys, fail2ban, public ports, secret-name drift) and the 8-day staleness flag on the status page.
- The `cth-health` page and the `CTH_HEALTH_OK` / `CTH_HEALTH_FAIL` words UptimeRobot would match.
- Outer HTTP and ping list in `uptimerobot-setup.sh`. Keyword monitor and API key are still pending, matching the ticket.

Worth folding in (MERGE rows 4, 5, 22, 23), because the new checker does not have them yet:

- TLS days-remaining for `wiki.cleantechhub.net` (doctor uses 14 days).
- Doctor's public URL list for Nexus (`nexus.cleantechhub.net` home, ideas, startups, mentors, investors, funders, mentor API `/health`). UptimeRobot's list covers wiki, Datalab, Mubon login, n8n-li, and Appwrite, and does not cover those Nexus URLs.
- Local service probes doctor still pings (`localhost` ports for Hermes, Paperclip, data-platform, notetaker). Decide per service whether the workbench should watch them or leave them to the app's own `/health`.
- The read-only sentence: watch and report, do not restart. Doctor's `--heal` flag must stay off this workbench.
- The 2026-09-24 map of which old cron lines already moved to n8n, so the workbench does not re-alert on a commented crontab.
- The maker≠checker / heartbeat vocabulary already in the Orchestrator profile.

Doctor-bot and the new checker both look at disk, swap, fail2ban, and wiki reachability. Doctor-bot does it once a day and also files Jira. The 10-minute job does the resource half and writes the status page. Running both will double-report the same disk and swap condition to different places (Telegram ops chat plus Jira errors, versus the status page and the harness Telegram allowlist).

## Alerts that go to a dead or wrong place

| Check | Where it sends | What happened |
|---|---|---|
| `doctor-bot.timer` Jira reporter | `cleantechhub.atlassian.net` issue create | HTTP 400 on every finding at 11:00 UTC today. `0 created`. The channel is dead. The timer is still enabled. |
| `doctor-bot` skill and README | Slack `#ops-health` | Live runner does not call `slack_reporter`. An agent that follows the skill will look in the wrong place. |
| `doctor-bot` Telegram | `TELEGRAM_CHAT_ID` from its env (value not read) | Today's digest **did** post (928 chars). The channel is alive. It is a personal ops chat, not the Infra desk, and it fires on a daily digest even when the page would be the right signal. |
| New `monitor.py` | Harness Telegram allowlist, on alert edges | Coded and logging alert lines. Whether Telegram accepted them is in a root-only state file that this audit did not open. Destination is not the Infra desk ticket path unless that desk reads that chat. |
| `clp` `health_check.py` | `CTH_OPS_BOT` ops group and a Gideon DM | Cron still fires every 6 hours and exits in the same second. Log is empty since 31 Jul 2026. Nothing is being delivered. |
| n8n `decay_monitor` and `adgrant_monitor` | Telegram, per the 2026-10-19 cleanup note | Workflows are active. They are product checks. They do not raise an Infra desk ticket. |
| Buffer `buffer_health.yml` | Slack webhook named in the README | Not confirmed running. The README still points at Slack. |

## Counts

| Verdict | Count | Rows |
|---|---|---|
| RELEVANT | 3 | 1, 2, 3 |
| MERGE | 4 | 4, 5, 22, 23 |
| STALE | 16 | 6–21 |
| Total itemized | 23 | |

The bc-8ec319df baseline is not included in those counts. It is the new structure.

## Top 5 to reuse

1. **The live status page** (`https://wiki.cleantechhub.net/.well-known/cth-health`, keyword `CTH_HEALTH_OK`). It is already the inner signal. UptimeRobot's missing keyword monitor should watch this URL.
2. **Doctor's Nexus URL list and the 14-day TLS check** in `/opt/atlassian/doctor-bot/checks/http_pings.py` and `vps_checks.py`. The new outer list does not include Nexus. Fold the URLs and the TLS day-count into the Hands checker, then let the status page carry the result.
3. **The read-only sentence** in `/opt/atlassian/doctor-bot/README.md`: report, do not restart. That is the Health workbench charter. Leave `--heal` on doctor-bot unused, and do not copy the healers.
4. **`/opt/claude-files/infrastructure/vps-access-audit-2026-10-18.md`** as the list of jobs that are still scheduled beside the new checker (doctor-bot, Rakazo sync, the silent `clp` health cron, n8n-li).
5. **The Orchestrator profile line** (heartbeat, maker≠checker, verifier) plus today's harness edit on branch `cursor/vps-hands-rule-c822`: alerts go to Health workbench `fbc6f772`, which reports to Infra.

## Still running, and stale

Left running on purpose. Do not disable from this audit.

| Job | Schedule | Why it is stale | Dead channel? |
|---|---|---|---|
| `doctor-bot.timer` | Every day 11:00 UTC. Last success today 11:00. Next 2026-10-20 11:00 UTC. | Superseded by the 10-minute status page for disk, swap, and service failure. Also covers Nexus, TLS, docker, and MCP evals the new job does not. | Jira create returns HTTP 400. Telegram digest still posts, to an ops chat rather than the Infra desk. |
| `/etc/cron.d/rakazo-sync` | 23:00 America/Bogota. Last report 2026-10-18 23:00 UTC. | Rakazo desk-mirror drift and Babo `/health`. Not VPS security drift. | No. It writes the archive mirror. Babo reported `ok`. |
| `clp` crontab `health_check.py` | Every 6 hours. Fired 00:00, 06:00, 12:00 UTC today. | Wattson and cohort checks. Process exits in the same second. Log empty since 2026-07-31. | Yes in practice. The ops-group and Gideon DM path has no log output. |
| n8n `decay_monitor` `bfqWFknxhNaxzLZi` | Monthly, active in n8n-li. VPS cron line is commented. | SEO decay, not the Health workbench. | Aimed at Telegram, not Infra. |
| n8n `adgrant_monitor` `o8URahr5QnLxZsdY` | Weekly Monday 12:00 UTC, active in n8n-li. | Ad Grant compliance. The systemd timer of the same name is already disabled. | Aimed at Telegram, not Infra. |
| `goodstack-watch.timer` | Daily 13:00 UTC. | Grant digest. Name matched "watch". | Not an uptime alert. |
| `origo-watcher.timer` | Monthly, next 2026-11-01. | Taxonomy watcher. | Not an uptime alert. |

`cth-monitor-health.timer` and `cth-monitor-security.timer` are the new checker. They are enabled. They are not in the stale list.
