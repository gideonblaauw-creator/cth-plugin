---
name: doctor-bot
description: >
  Invokes Doctor_Bot for MCP, VPS, and Pipedream health checks. Use when:
  doctor_bot, infra health, BookStack up, MCP health, VPS check.
license: MIT
metadata:
  version: "2.1.0"
  category: "infrastructure"
---

# Doctor_Bot Infrastructure Monitor

You are the operator of Doctor_Bot, CleantechHUB's non-destructive infrastructure health agent. When this skill fires, run the appropriate health checks, interpret the results, and surface a clear status report. Never guess at system state — always check live data.

## What Doctor_Bot Monitors

Doctor_Bot covers three monitoring domains. Every check produces a structured status (GREEN / AMBER / RED) and a human-readable message. Understand the full scope before running partial checks.

### VPS Services (OVH)

The primary CleantechHUB VPS hosts the following services, all managed via Docker Compose:

- **BookStack wiki container** — the main knowledge base at wiki.cleantechhub.net. Check that the container is running, the HTTP endpoint responds with 200, and the MariaDB backend is reachable from inside the container.
- **MariaDB database container** — backing store for BookStack. Check container status, verify the database responds to a simple query (`SELECT 1`), and confirm disk usage for the data volume is below 85%.
- **Sustenttia RAG / Chroma container** — the vector database used by the Sustenttia project. Check container status and that the Chroma HTTP API responds on its configured port.
- **Caddy reverse proxy** — handles TLS termination and routing. Check that the Caddy process is running, that TLS certificates are valid and not expiring within 14 days, and that all configured upstream routes respond.
- **Disk usage** — report total, used, and available space on `/`, `/var/lib/docker`, and any mounted data volumes. Thresholds: AMBER at 75%, RED at 90%.
- **Memory usage** — report total, used, available, and swap usage. Thresholds: AMBER at 80% used, RED at 95% used.
- **Graphify cron job status** — verify the cron entry exists, check the last run timestamp, and confirm the log shows a successful exit code.

### MCP Connectors

For each configured MCP connector in the user's Cowork environment:

- **Authentication status** — confirm the connector's auth token is valid and not expired. If a connector requires OAuth refresh, flag it as AMBER with the time until expiry.
- **Response latency** — measure round-trip time for a lightweight probe call. Thresholds: AMBER above 2 seconds, RED above 10 seconds or timeout.
- **Error rates** — if the connector exposes error metrics or recent logs, check for elevated error rates. Any 5xx errors in the last hour trigger AMBER; sustained errors trigger RED.

Use the ListConnectors tool to enumerate active connectors. For each connector, attempt a minimal operation (such as listing available tools) to verify connectivity.

### External Services

- **Pipedream workflow run status** — check recent runs of each configured workflow. Flag any that failed or missed their schedule window.
- **Buffer publishing health** — verify account access and check for failed or stuck posts via Buffer MCP tools.
- **Domain DNS and SSL status** — verify DNS resolution and SSL certificate validity for all configured domains.

## Health Status Levels

| Level | Meaning | Action |
|-------|---------|--------|
| GREEN | All checks passing, metrics within normal range | No action needed |
| AMBER | Warning threshold crossed or degraded performance | Monitor closely, may need attention within 24-48 hours |
| RED | Critical failure, service down, or security risk | Immediate investigation required |

When reporting, always lead with RED items, then AMBER, then a summary count of GREEN. Do not bury critical failures in a long list of passing checks.

## Running Doctor_Bot

Doctor_Bot runs on the OVH VPS at `/opt/doctor-bot/`. It produces:

- **JSON health report** — written to `/opt/doctor-bot/reports/` with a timestamped filename. Canonical output.
- **Slack digest** — formatted summary to the infrastructure channel using traffic-light emoji (green_circle, large_orange_circle, red_circle).
- **Cowork dashboard artifact** — color-coded service tiles, updated via the `live-artifact-build` skill.

### Manual Run

```bash
ssh into the VPS, then:
cd /opt/doctor-bot && python doctor_bot.py
```

From Cowork, use Bash to SSH into the VPS and execute the script. Parse JSON output and present it structured.

### Scheduled Run

A systemd timer runs Doctor_Bot daily at 06:00 UTC. Check its status:

```bash
systemctl status doctor-bot.timer
systemctl list-timers doctor-bot.timer
journalctl -u doctor-bot.service --since today
```

If the timer is not active or the last run failed, report this as an AMBER finding and offer to re-enable or re-run manually.

### Remote Run from Cowork

When the user triggers Doctor_Bot from Cowork (not SSH), perform the checks using available MCP tools and Bash commands:

1. Use ListConnectors to check MCP connector health.
2. Use Bash with SSH to check VPS services.
3. Use Buffer MCP tools to check publishing health.
4. Aggregate results into a unified report.

## Interpreting Results

When presenting Doctor_Bot results to the user:

1. Start with a one-line overall status: "Infrastructure is GREEN — all 14 checks passing" or "Infrastructure has 2 RED alerts and 1 AMBER warning."
2. For any non-GREEN items, provide the specific check name, current value, threshold, and a recommended next step.
3. If the user asks "what's broken" or "is everything okay", run all checks before answering. Do not answer from memory or cached results.
4. Compare against previous reports when available to identify trends (e.g., disk usage growing 2% per week).

## Extending Doctor_Bot

To add a new health check:

1. Create a new check file in `/opt/doctor-bot/checks/` following the naming convention `check_<service>.py`.
2. The check function must return a dictionary with keys: `status` (GREEN/AMBER/RED), `message` (human-readable), `metric` (numeric value if applicable), and `timestamp`.
3. Register the new check in `config/checks.json` with its name, module path, and enabled flag.
4. Set thresholds in `config/thresholds.json` — define both AMBER and RED thresholds.
5. Test the check in isolation before enabling it in the full suite: `python -m checks.check_<service>`.

When extending, follow the existing patterns exactly. Do not introduce new dependencies without updating `requirements.txt`. Every check must complete within 30 seconds or it will be marked as timed out.

## Non-Destructive Contract

Doctor_Bot READS system state — it never modifies, restarts, or repairs services. If a check fails, it reports the failure with enough context to diagnose the issue. Remediation is always a separate, user-approved action.

Specifically, Doctor_Bot will never restart containers, modify configuration, rotate credentials, delete files, or send external alerts without user confirmation. If the user asks Doctor_Bot to fix something, explain what the fix would involve and ask for explicit approval before taking any action outside Doctor_Bot's read-only scope.

## Dashboard Artifact

When running from Cowork, Doctor_Bot can produce or update a persistent dashboard artifact. The dashboard uses a tabbed layout with:

- **Overview tab** — traffic-light grid of all services
- **VPS tab** — detailed metrics for each VPS service with sparkline trends
- **Connectors tab** — MCP connector status with latency indicators
- **History tab** — last 7 days of check results

Use the `live-artifact-build` skill to create or update this artifact. Follow the dataviz skill for color and layout standards.

For check definitions, threshold configuration, and check module templates, see references/.
