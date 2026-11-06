# Daily usage alerts — operational note (prep only)

**Status:** **Protocol documentation only** (Tier 0). **No** runnable reference implementation, active monitor, merge-by-agent, deploy, schedules, live transports, activation, or Grok Bot usage-polling routines in this PR. **Both apps** (Grok Bot and Cursor) remain **BLOCKED** for official daily metrics in the contract unit; the **weekly included denominator** is **user-unconfirmed** until Infrastructure validates mapping for the target plan and account.

**Authority:** Gideon direct request (Orchestrator relay, 6 Nov 2026, America/Bogota). **Tier 0.** Infrastructure desk reviews; Gideon retains **HITL approval for this protocol merge** and any separate **implementation, scheduling, transports, sends, or activation**. A protocol merge **does not** authorize those.

**Account scope:** **Team/Admin API** availability, **plan eligibility**, **required privileges**, **per-app attribution** (Grok Bot vs Cursor for included consumption), and **denominator compatibility** with the contract unit are **not established** for **Gideon’s account** in this document — **do not** assume existing access or billing shape suffices.

## Metric interpretation (working contract — denominator not user-confirmed)

- **Apps:** **Grok Bot** and **Cursor** (evaluate separately; **no** inference from totals).
- **Unit:** Each app’s consumption on one **local calendar day** expressed as **percentage points of the shared weekly included allowance** (for example, `10` means ten percentage points of that weekly pool, not “10% of a daily sub-cap” unless the source defines it that way). **Confirmation** of that denominator and unit mapping is required before implementation or activation.
- **Day boundary:** **`America/Bogota`**, `[local midnight, next local midnight)` — not a rolling 24h window. Convert source timestamps to this boundary when the source uses another zone.
- **Thresholds (literal, strict):** Grok Bot **>** `10` (10.0 does **not** trigger). Cursor **>** `4` (4.0 does **not** trigger). Use decimal-safe compares on the **same unit the source provides** after any documented normalization — do not round early.

## Prohibitions (non-negotiable)

- **No** deriving Cursor usage by subtracting Grok Bot (or any app) from a shared total; other apps share the allowance.
- **No** Grok Bot usage-polling routines (harness / built-in usage-review lock).
- **No** fake feeds, dashboard scraping, session tokens, credential extraction, private/internal undocumented APIs, new sign-ins, or paid API calls from CI/tests in this repo.
- **Missing or unknown coverage** → **BLOCKED** or **unknown** — **never** treat as zero or “below threshold.”
- **Blocked official feeds do not justify** claiming production-like alerts or hiding gaps; document requirements and gaps honestly. **Do not** claim that no official source can ever exist.

## Official source evidence (feasibility — bounded review only; no new research in this PR)

### Cursor (included allowance, per-event units)

- **Docs:** Cursor **Admin API** — `https://cursor.com/docs/account/teams/admin-api`
- **Relevant endpoints (documented):**
  - `POST /teams/filtered-usage-events` — granular usage events; `requestsCosts` = cost in **request units**; billing `kind` distinguishes included vs usage-based; data aggregated **hourly** (doc recommends polling at most once per hour).
  - `POST /teams/daily-usage-data` — **per user, per calendar `day`** (ISO date) activity — **not** split by Grok Bot vs Cursor IDE for included consumption; `subscriptionIncludedReqs` counts **raw** events and doc states billable request counts need **`requestsCosts` sum** from filtered events for older pricing models.
- **Weekly pool denominator:** Admin API documents **`/teams/spend`** with **`subscriptionCycleStart`** and per-member spend fields for the **current billing cycle** — a **compatibility check** is required to map **sum of included `requestsCosts` over a subscription week** to “weekly included allowance” in the same units. Until that mapping is validated for the target plan and account, **live coverage = BLOCKED** (see readiness table below).
- **Per-app split (Grok Bot vs Cursor):** Audit log text lists `application_type` `grok_bot` vs `cursor` for **audit events**, **not** for `/teams/filtered-usage-events` response fields in the public Admin API page reviewed for this PR. **Do not** assume per-app included consumption without a documented field or confirmed filter on usage events.

### Grok Bot

- **Cursor product:** Same Cursor Admin API doc covers **Grok Bot** management routes; usage-like **included** splits for **Grok Bot vs Cursor** for the metric contract are **not** documented on that page for `filtered-usage-events` in this review.
- **xAI / Grok API (separate product):** **Management API** usage — `https://docs.x.ai/developers/rest-api-reference/management/billing` (daily bucketing, management key) — measures **API** consumption, **not** Grok Bot inside Cursor’s included allowance. **Not** a drop-in source for this contract.

## Readiness (this PR)

| App        | Official daily per-app metric in contract units | Compatible weekly included denominator | Verdict   |
|-----------|---------------------------------------------------|----------------------------------------|-----------|
| Grok Bot  | Not documented in reviewed Cursor Admin API usage endpoints | N/A                                    | **BLOCKED** |
| Cursor    | Hourly aggregated events; weekly cycle fields exist; per-day ISO in `daily-usage-data` is not per-app for included reqs | Needs plan-level mapping + app attribution | **BLOCKED** |

**Freshness:** Cursor docs say hourly aggregation — if an adapter is ever authorized, use **at most hourly** poll cadence; label **freshness unknown** when unknown and **do not** claim instant detection from delayed records.

## Future acceptance — NOT IMPLEMENTED

The following are **requirements for a future implementation**, not delivered by this PR:

- Official source with **compatible app-specific units** and **confirmed denominator**, event time, observation time, source window, cadence, and allowance/reset identity.
- **Explicit input contract:** event increments **versus** cumulative snapshots — **never** double-count snapshots.
- Decimal-safe strict thresholds; boundary **10.0** / **4.0** does **not** trigger.
- **Durable** once-per-app-per-COT-day suppression across **restarts** and **weekly allowance resets**.
- Namespace sample identities by app/source; persist pending/sent state and define transport idempotency/retry semantics.
- **Do not** reset an already-sent app/day alert on a correction, allowance reset, or metric-version change.
- Calendar rollover at **COT midnight**. Preserve compatible pre-reset day segments; otherwise report unavailable.
- Missing, stale, unknown freshness, incomplete baseline, future or out-of-order records **cannot** become false zero or valid totals.
- A documented **freshness gate** based on source cadence; no claim of instant detection from delayed records.
- **Deduplicate** data-quality warnings separately from threshold alerts.
- Late records retain their **event day**, carry a **late** label, and **do not** enter today’s total.
- Corrections replace/reconcile their source reading **without** repeating an issued app/day alert.
- Output includes measurement, threshold, unit/denominator, local day, **source timestamp** and **observation timestamp**.
- Contributors appear only with supported same-app/same-day/same-unit attribution.
- Future synthetic tests cover these cases, including restart/reset within one COT day and iterator-safe ingestion.

## Alert shape (preparation — when an adapter exists)

At most **one** threshold alert per app per **America/Bogota** day; idempotency key includes app, local date, and **metric definition version**; output shows measured usage, threshold, denominator, local date, source timestamp, observation timestamp. **No** live sends in this PR.

## Pointer

Desk playbook: `skills/infrastructure-comms/SKILL.md` § Daily usage alerts.
