# Health workbench charter (draft)

Draft for review. Do not treat this as adopted until Infra accepts it. The evidence is the 19 Oct 2026 archive audit in `claude-folder-health-audit-2026-10-19.md`.

Granola has no meeting that assigns who watches infrastructure. This charter follows the Infra ticket: one desk writes tickets, maker Hands builds, a different verifier Hands checks, and Health only watches.

## Role

Health is a Grok Bot workbench. Its id is `fbc6f772`. It reports to the Infra desk.

It watches signals and raises alerts. It does not restart services, edit Caddy, change units, rotate keys, or clear disk. Repair is an Infra ticket. Maker Hands builds that ticket. A separate verifier Hands is read-only and writes PASS or FAIL. The maker is not the checker. Health is neither the maker nor the verifier.

## Signals

| Signal | Source | How often |
|---|---|---|
| Status page | `https://wiki.cleantechhub.net/.well-known/cth-health` served by Caddy from `/var/lib/cth-monitor/public/cth-health.txt` | Rewritten every 10 minutes. Body is `CTH_HEALTH_OK <UTC time>` or `CTH_HEALTH_FAIL <names>`. |
| Workers `vps` and `vps-2` | User units `cursor-worker.service` and `cursor-worker-vps-2.service` | Every 10 minutes. |
| Resources | Disk, swap, failed systemd units, restart jumps | Every 10 minutes. |
| Security drift | sshd password and root login, authorized-keys set, fail2ban, public listeners, secret-name drift (names only, never values) | Mondays 06:20 UTC. The status page carries `security-stale` if that report is older than 8 days. |
| Outer HTTP and ping | UptimeRobot: wiki, Datalab, Mubon login, n8n-li, Appwrite, and ping `51.195.45.77` | 5 minutes once the account is in place. The API key is not stored on this VPS. |
| Keyword on the status page | UptimeRobot keyword monitor, still to be added by Infra | 5 minutes. URL above. Keyword `CTH_HEALTH_OK`. Alert when the keyword is missing. |
| Nexus | Not on the UptimeRobot list yet. Doctor-bot still pings `nexus.cleantechhub.net` (home, ideas, startups, mentors, investors, funders, mentor API `/health`). | Add these URLs to the outer list or to the 10-minute job before doctor-bot is retired. |
| Heartbeat | The timestamp on the status page, plus the UptimeRobot keyword | A missing keyword or a timestamp older than 20 minutes is a missed heartbeat. Do not add a separate UptimeRobot heartbeat monitor. |

`n8n-li` is watched as a site (`https://n8n-li.cleantechhub.net/`) and as a host the Infra desk already operates. Product workflows inside n8n (Ad Grant monitor, SEO decay) stay with their own desks. Health reports the site being down. It does not grade campaign posts.

## Alert thresholds

These match the checker Hands `bc-8ec319df` has already coded, except the Nexus and TLS lines, which are proposed additions from the doctor-bot catalogue.

| Check | Alert when |
|---|---|
| Worker | `cursor-worker.service` or `cursor-worker-vps-2.service` is not `active`. |
| Worker restarts | `NRestarts` for either worker rises by more than 3 since the previous 10-minute tick. |
| Disk | Any real filesystem is at or above **85%**. `/mnt/data` was at 90% when the audit ran, and the status page was already `CTH_HEALTH_FAIL`. |
| Swap | Swap used stays above **80%** for **3** consecutive 10-minute ticks. |
| Failed unit | Any system or user service is in `failed`. |
| Restart loop | Any other unit's `NRestarts` rises by more than 3 in one tick, or the unit hits the start limit. |
| Security | sshd allows password auth or root login, authorized keys change, fail2ban is down, a new public listener appears, or a new secret-looking assignment appears. The page names the variable, never the value. |
| Security report age | The weekly report is older than **8 days**. |
| TLS (proposed) | `wiki.cleantechhub.net` certificate has **14 days** or fewer left. |
| Heartbeat | Status timestamp is older than **20 minutes**, or the UptimeRobot keyword `CTH_HEALTH_OK` is absent. |
| Outer site | UptimeRobot marks wiki, Datalab, Mubon login, n8n-li, Appwrite, or the VPS ping down. |

One page word is enough. Doctor-bot's extra amber band (disk 70%, swap 50%) stays in the old daily job until that job is retired. The workbench alerts at the lines above.

## Where alerts go

1. Health workbench `fbc6f772` receives the alert.
2. That workbench reports it to the Infra desk.
3. Infra writes a ticket if someone must change the machine. Maker Hands and verifier Hands stay different sessions.
4. Gideon is told directly only when the outage delays a deliverable he is waiting on. A red disk or a failed unit goes to Infra first.

The daily doctor-bot digest still posts to a Telegram ops chat and then fails to create Jira issues (HTTP 400 on 19 Oct 2026). The new checker can also send Telegram to the harness allowlist. Telegram is a transport only if the Infra desk actually reads that chat. It is not a second destination, and it is not a Gideon DM. Slack `#ops-health` is described in `skills/doctor-bot/SKILL.md` and is not where the live runner posts.

## What Health does not take over

- Rakazo mirror drift and the Babo `/health` probe (still a daily cron).
- The Wattson `clp` health cron (still scheduled, log empty since 31 Jul 2026).
- n8n Ad Grant and SEO decay workflows.
- Goodstack grant digest and the Origo taxonomy watcher.
- The Mac `mac-scan` worker runbook.
- Doctor-bot's optional disk and TLS healers.

Those jobs were still scheduled at audit time. This charter does not turn them off. Infra retires them with a ticket after the status page and the UptimeRobot keyword monitor cover the same signal.

## Open points for Infra

- Confirm UptimeRobot's keyword monitor on the status URL, and keep the API key off this VPS.
- Add Nexus URLs, or explicitly leave Nexus on doctor-bot until that timer is retired.
- Say whether the harness Telegram allowlist is the Infra desk's inbox. If it is not, point the 10-minute alerter at the desk and stop treating the doctor-bot ops chat as the record.
- The status page was `CTH_HEALTH_FAIL` for disk, failed units, restart loops, and swap at 14:18 UTC on 19 Oct 2026. That is a live alert for the workbench, not a fix for this document.
