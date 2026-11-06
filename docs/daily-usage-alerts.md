# Daily usage alerts — operational note (prep only)

**Status:** Protocol and dormant evaluator only. **No** merge-by-agent, deploy, schedules, live transports, activation, or Grok Bot usage-polling routines.

**Authority:** Gideon direct request (Orchestrator relay, 6 Nov 2026, America/Bogota). **Tier 0.** Infrastructure desk reviews; Gideon retains merge and activation.

## Metric interpretation (working contract — not user-confirmed)

- **Apps:** **Grok Bot** and **Cursor** (evaluate separately; no inference from totals).
- **Unit:** Each app’s consumption on one **local calendar day** expressed as **percentage points of the shared weekly included allowance** (for example, `10` means ten percent of that weekly pool, not “10% of a daily sub-cap” unless the source defines it that way).
- **Day boundary:** **`America/Bogota`**, `[local midnight, next local midnight)` — not a rolling 24h window. Convert source timestamps to this boundary when the source uses another zone.
- **Thresholds (literal, strict):** Grok Bot **>** `10` (10.0 does **not** trigger). Cursor **>** `4` (4.0 does **not** trigger). Use decimal-safe compares on the **same unit the source provides** after any documented normalization — do not round early.

## Prohibitions (non-negotiable)

- **No** deriving Cursor usage by subtracting Grok Bot (or any app) from a shared total; other apps share the allowance.
- **No** Grok Bot usage-polling routines (harness / built-in usage-review lock).
- **No** fake feeds, dashboard scraping, session tokens, credential extraction, private/internal undocumented APIs, new sign-ins, or paid API calls from CI/tests in this repo.
- **Missing or unknown coverage** → **BLOCKED** or **unknown** — **never** treat as zero or “below threshold.”

## Official source evidence (feasibility)

### Cursor (included allowance, per-event units)

- **Docs:** Cursor **Admin API** — `https://cursor.com/docs/account/teams/admin-api`
- **Relevant endpoints (documented):**
  - `POST /teams/filtered-usage-events` — granular usage events; `requestsCosts` = cost in **request units**; billing `kind` distinguishes included vs usage-based; data aggregated **hourly** (doc recommends polling at most once per hour).
  - `POST /teams/daily-usage-data` — **per user, per calendar `day`** (ISO date) activity — **not** split by Grok Bot vs Cursor IDE for included consumption; `subscriptionIncludedReqs` counts **raw** events and doc states billable request counts need **`requestsCosts` sum** from filtered events for older pricing models.
- **Weekly pool denominator:** Admin API documents **`/teams/spend`** with **`subscriptionCycleStart`** and per-member spend fields for the **current billing cycle** — a **compatibility check** is required to map **sum of included `requestsCosts` over a subscription week** to “weekly included allowance” in the same units. Until that mapping is validated for the target plan, **live coverage = BLOCKED** (see readiness table below).
- **Per-app split (Grok Bot vs Cursor):** Audit log text lists `application_type` `grok_bot` vs `cursor` for **audit events**, **not** for `/teams/filtered-usage-events` response fields in the public Admin API page reviewed for this PR. **Do not** assume per-app included consumption without a documented field or confirmed filter on usage events.

### Grok Bot

- **Cursor product:** Same Cursor Admin API doc covers **Grok Bot** management routes; usage-like **included** splits for **Grok Bot vs Cursor** for the metric contract are **not** documented on that page for `filtered-usage-events` in this review.
- **xAI / Grok API (separate product):** **Management API** usage — `https://docs.x.ai/developers/rest-api-reference/management/billing` (daily bucketing, management key) — measures **API** consumption, **not** Grok Bot inside Cursor’s included allowance. **Not** a drop-in source for this contract.

## Readiness (this PR)

| App        | Official daily per-app metric in contract units | Compatible weekly included denominator | Verdict   |
|-----------|---------------------------------------------------|----------------------------------------|-----------|
| Grok Bot  | Not documented in reviewed Cursor Admin API usage endpoints | N/A                                    | **BLOCKED** |
| Cursor    | Hourly aggregated events; weekly cycle fields exist; per-day ISO in `daily-usage-data` is not per-app for included reqs | Needs plan-level mapping + app attribution | **BLOCKED** |

**Freshness:** Cursor docs say hourly aggregation — use **at most hourly** poll cadence if an adapter is ever authorized; otherwise label **freshness unknown** and do not claim instant detection.

## Dormant evaluator

Reference implementation (synthetic tests only): `services/daily_usage_alerts/evaluator.py`. **Disabled** until Infrastructure maps a supported source and Gideon approves activation.

## Alert shape (preparation)

When an adapter exists: at most **one** threshold alert per app per **America/Bogota** day; idempotency key includes app, local date, and **metric definition version**; output shows measured usage, threshold, denominator, local date, source timestamp, observation timestamp. **No** live sends in this PR.

## Pointer

Desk playbook: `skills/infrastructure-comms/SKILL.md` § Daily usage alerts.
