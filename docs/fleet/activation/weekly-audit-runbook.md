# Weekly token audit runbook (report-only)

**Status:** Active registry (`FLEET_REGISTRY.yaml`); **enforcement** remains **report-only** until a second Gideon GO.

## Schedule

| Field | Value |
| :--- | :--- |
| When | **Monday 07:00** `America/Bogota` |
| Owner | **Control Tower · Infra** routine (`c656afb9`) |
| Mode | Read-only **Cloud Hands** job (no live profile or n8n writes) |

## Input

1. Export Grok/Cursor usage for the prior week (same column shape as Nov 2026 baseline).
2. Place the latest file in the bot store, e.g. `/cursor/stores/bot/fleet-redesign-2026-11-25/usage-export-YYYY-MM-DD.csv` (or the path Control Tower publishes that week).

## Command

From `cth-plugin` on a machine with the export path:

```bash
python3 scripts/weekly_token_audit.py \
  --csv /path/to/usage-export.csv \
  --registry FLEET_REGISTRY.yaml \
  --out /path/to/audit-report.md
```

**Do not** pass `--enforce`. **Do not** set `ENFORCE_APPROVED=1`. Reporting only.

## Outputs

| Artifact | Destination |
| :--- | :--- |
| Markdown audit report | Job output path; Hands attaches to ticket / PR draft if requested |
| JSON metrics (if `--json-out` set) | Same folder as report |
| Remediation actions | **None** in report-only mode — log lines only |

**Orchestrator** (`5dc64ea4`) receives the summary (KPI table, breaches, top events) via the Infra routine handoff. No automatic merge, profile edit, or schedule pause.

## Turning on enforcement (later)

1. Complete **one clean week** of Monday audits with no data gaps.
2. Gideon issues a **second GO** naming enforcement (auto-pause, circuit breaker, or audit `--enforce`).
3. Control Tower opens a separate ticket to flip `enforce: true` where approved and to enable `--enforce` only after `ENFORCE_APPROVED` is set in the job environment.

Until that GO, `auto_pause` and `circuit_breaker` blocks in `FLEET_REGISTRY.yaml` stay **`enforce: false`**.

## Rollback

See [`ROLLBACK.md`](ROLLBACK.md) for full activation rollback. For the audit routine only: pause or delete the Control Tower Monday trigger; revert any PR that wired enforcement flags.