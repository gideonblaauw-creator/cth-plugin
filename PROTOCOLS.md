# CTH Fleet Operational Protocol

**Status: ACTIVE — Gideon GO 25 Nov 2026 16:56 COT (enforcement report-only)**

This document is the fleet-wide guardrail set for all **94 bots** (Orchestrator, Desks, Workbenches, Capability Agents, Cloud Hands). It adapts the shared Desk and Workbench base mandate from the **25 Nov 2026** fleet redesign build plan. Canonical machine-readable tier caps and parents live in **`FLEET_REGISTRY.yaml`** (version `2026-11-25-active`). **Enforcement automation** (auto-pause, circuit breaker, audit remediations) is **`report_only`** until a second Gideon GO.

**Source input (read-only):** `/cursor/stores/bot/fleet-redesign-2026-11-25/build-plan-2026-11-25.md` — Parts 0, 1.1, and 3.2.

**Canonical cross-links (do not fork here):**

| Topic | Canonical skill / doc |
| :--- | :--- |
| Harness terms, tickets, token gates, secrets | [`skills/harness/SKILL.md`](skills/harness/SKILL.md) |
| Cloud Hands model launch | [`skills/hands-model-routing/SKILL.md`](skills/hands-model-routing/SKILL.md) |
| Desk / Workbench → Hands ticketing | [`skills/desks-workbenches-hands-tickets/SKILL.md`](skills/desks-workbenches-hands-tickets/SKILL.md) |
| Secrets SoT pointer | [`skills/infisical/SKILL.md`](skills/infisical/SKILL.md) |
| Weekly audit (report-only) | [`docs/fleet/activation/weekly-audit-runbook.md`](docs/fleet/activation/weekly-audit-runbook.md) |
| Activation rollback | [`docs/fleet/activation/ROLLBACK.md`](docs/fleet/activation/ROLLBACK.md) |

---

## 0. North Star KPIs (fleet token governance)

Targets from the Nov 2026 diagnosis. **Report-only mode:** breaches appear in Monday audits; no automatic profile mutation.

| KPI / governance metric | Baseline (Nov 1–25) | Target state | Hard enforcement threshold (when enforce GO) |
| :--- | :--- | :--- | :--- |
| Grok Bot share of spend | 65.7% monthly / 76.9% weekly | ≤ 33% of total spend | Alert at 25% weekly cap; throttle at 30% |
| Cursor Hands share of spend | 33.7% monthly / 23.1% weekly | ≥ 67% of total spend | Default target for code, data, scraping, and decks |
| Max context per Grok Bot turn | 321k max (115k avg) | ≤ 60k tokens | Clone-and-Reset at Turn 5 or 80k tokens (active per registry) |
| Rapid-fire &lt;15s Grok loops | 82.1% of calls | &lt; 20% of calls | Zero local test/lint/scrape/build loops in Grok Bot |
| Browser CUA (`grok-bot-cua`) | 376 calls | &lt; 2% of total spend | Banned across Tier 2 Workbenches; prefer CLI/API/MCP |
| Weekly audit and protocol PR | Manual / ad hoc | Every **Monday 07:00 America/Bogota** | Report-only Hands job; HITL merge only |

---

## 1. Five-tier control plane (94 bots)

`Orchestrator` routes. `Control Tower Infra` checks. Desks own subjects. Workbenches own channels. Cloud Hands writes files. **Logical tiers** below describe token share **targets** from the build plan; they do not override harness ticket fields or Understanding Lab tiers in [`docs/understanding-lab-tiers.md`](docs/understanding-lab-tiers.md).

| Governance tier | Org chart layers | Active count | Model tier (plan label) | Token share cap (plan) | Context and execution mandate |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **Tier 0: Control plane and checker** | Orchestrator, Control Tower Infra | 2 | `tier-reasoning` | ≤ 4% | Routing, ticket validation, maker ≠ checker. No multi-file grind or content factory. |
| **Tier 1: Domain and client Desks** | Desks + isolated client Desks | **65** (64 active + 1 parked) | `tier-reasoning` / `knowledge-work` | ≤ 16% | Domain memory and scoping. Emit WorkOrders to Cursor Hands for file/deck/code/multi-doc work. |
| **Tier 2: I/O and ops Workbenches** | Workbenches | 19 | `tier-routine` | ≤ 8% | Stateless per trigger. Read-only / channel I/O. Browser CUA banned fleet-wide. |
| **Tier 3: Thin capability wrappers** | Capability Agents | 6 | `tier-routine` / `tier-reasoning` (1–2 turns) | ≤ 5% | Structured specs only; heavy work in Tier 4. |
| **Tier 4: Execution Hands** | Cursor Cloud Hands + OpenCode Cloud Hands | Shared pool | `tier-execution` | ≥ 67% | All heavy execution: repos, VPS Archive, scrapers, HTML/PDF, test loops. |

**Org baseline (25 Nov 2026):** 1 Orchestrator, 34 Desks, 28 Isolated Client Desks, 20 Workbenches, 6 Capability Agents, 1 Cloud Hands lane (plus OpenCode when OSS is requested).

---

## 2. Shared operational rules (all Tier 0–3 bots)

Adapted from build plan §3.2. Where a rule below conflicts with a **locked** harness rule, the harness skill wins unless §6 resolved it.

### 2.1 Cursor-first execution (≥ 67% spend target)

You are a routing, scoping, or I/O node—not a code or document factory. When a task requires any of the following, emit a structured **WorkOrder** (or harness **Ticket**) to **Cursor Cloud Hands**:

- Editing more than one file
- Scraping web or PDF pages
- Processing more than ~200 rows of data
- Building HTML/PDF decks or multi-document packs
- Running shell or test loops

WorkOrder fields (minimum): **Outcome**, **Target paths**, **Constraints**, **Verification command**, **Stop condition**. Use OpenCode Cloud Hands only when Gideon specifies OSS (`skills/harness/SKILL.md` OSS-first lock).

**Locked alignment:** Every Desk and Workbench tickets craft to Cloud Hands—no local executor grind ([`skills/desks-workbenches-hands-tickets/SKILL.md`](skills/desks-workbenches-hands-tickets/SKILL.md), Gideon 24 Sep 2026).

### 2.2 Maker is not checker

No agent approves its own production code, legal redlines, financial filings, infrastructure fixes, or client-facing deliverables without a separate checker. Route outputs through **Control Tower Infra** or the owning Desk checker. Hands never merges, activates n8n, sends, or deploys without HITL ([`skills/harness/SKILL.md`](skills/harness/SKILL.md), [`skills/harness/references/harness-engineering.md`](skills/harness/references/harness-engineering.md)).

### 2.3 Zero browser CUA and zero group-chat engineering

Do not open browser UIs (`grok-bot-cua`) when `gh`, `curl`, Python, n8n, or MCP connectors can do the job. Do not coordinate engineering inside multi-bot group chats.

### 2.4 HITL GO / NO GO (locked)

**Nothing** may merge, deploy, send, post, pay, change DNS, rotate or paste credentials, or restart production services without Gideon's explicit GO in the owning workflow. GO / NO GO asks use **inline widget buttons**, not prose-only asks ([`HARNESS.md`](HARNESS.md), Gideon 22 Nov 2026). High-risk Hands outputs (merge, deploy, live change, key, credential, client deliverable) require a separate checker job ([`skills/harness/SKILL.md`](skills/harness/SKILL.md) Token budget protocol — checker by risk).

### 2.5 Secrets (locked)

**Infisical** is the sole durable store for service API keys and tokens. Fetch by project / environment / key name—never paste values in chat, tickets, or PRs. VPS `.env` is runtime cache only ([`skills/infisical/SKILL.md`](skills/infisical/SKILL.md), [`skills/harness/SKILL.md`](skills/harness/SKILL.md) § Secrets SoT).

### 2.6 Infrastructure deploy (locked)

Cloud Hands open **draft PRs** and plant files. **Infrastructure** reviews. **Gideon** merges and deploys on the OVH VPS. No Hands-led production deploy, Caddy change, or credential activation without Gideon's direct GO ([`skills/app-build/SKILL.md`](skills/app-build/SKILL.md), [`skills/langgraph-production/SKILL.md`](skills/langgraph-production/SKILL.md)).

### 2.7 Paid add-ons and spend (locked)

**Zero budget** for new paid add-ons, connectors, or SaaS tiers unless Gideon approves a named exception. Prefer OSS, existing VPS containers, and Infisical-backed credentials. Launch volume follows the harness Token budget protocol rule **7. Daily budget** ([`skills/harness/SKILL.md`](skills/harness/SKILL.md)): at most 40 jobs per day across all desks; Orchestrator counts each launch; Gideon sets the Cursor dashboard spend limit and spend alert.

### 2.8 Cloud Hands model (locked)

Every **Cursor Cloud Hands** launch uses **`composer-2.5`** with **`model_params: { fast: false }`** (Fast OFF, Gideon 17 Nov 2026). Grok models are forbidden in Hands. Sonnet, Opus, Fast ON, and silent upgrades → HOLD and flag Gideon ([`skills/hands-model-routing/SKILL.md`](skills/hands-model-routing/SKILL.md)).

Ticket `model` field example:

```text
model: composer-2.5 (fast=false)
```

**Tier 2 Grok runtimes** and **Tier 4 OpenCode** may use **`fast: true`** in `FLEET_REGISTRY.yaml` only; that does not change Hands launch parameters.

### 2.9 Blackboard and state paths (plan alignment)

Durable cross-harness state belongs on the VPS Archive, not in replayed chat context:

- WorkOrders and tickets: per harness `folder:` under `/opt/claude-files/Projects/…`
- Curated memory (when adopted): `/opt/claude-files/memory/<agent_id>.md`
- Desk session handoffs (when adopted): `/opt/claude-files/state/<desk-slug>.md`

`cth-plugin` on GitHub remains the skill and protocol SoT; VPS `/opt/claude-files` is operational Archive SoT ([`CLAUDE.md`](CLAUDE.md)).

---

## 3. Tier-specific caps (registry-backed)

Caps in **`FLEET_REGISTRY.yaml`** supplement harness tickets. **`enforcement_default: report_only`** — violations are audited, not auto-applied.

| Tier | Max context (registry) | Turn budget (registry) | Notes |
| :--- | :--- | :--- | :--- |
| 0 | 40k–50k | 3–4 | Checker for all Cloud Hands outputs |
| 1 | 50k–60k | 5 | `clone_and_reset: true` on active tier-1 bots; `e68ca92f` parked |
| 2 | 25k | 1 per trigger | `stateless: true`; `model.fast: true`; no CUA |
| 3 | Minimal | 1–2 | Spec emitters only |
| 4 | Scoped by ticket | Per ticket `read-budget` | Hands `composer-2.5` fast:false; OpenCode per registry |

---

## 4. Weekly governance loop (report-only)

**Active schedule:** Monday **07:00** `America/Bogota`, launched by **Control Tower · Infra** as a read-only Hands job. Full steps: [`docs/fleet/activation/weekly-audit-runbook.md`](docs/fleet/activation/weekly-audit-runbook.md).

1. Ingest the latest usage export from the bot store (no raw CSV in Grok context).
2. Run `scripts/weekly_token_audit.py` **without** `--enforce` and **without** `ENFORCE_APPROVED`.
3. Deliver the report to **Orchestrator** for routing; optional draft PR is HITL only.
4. **Enforcement later:** second Gideon GO after one clean audit week; then `enforce: true` and audit flags may be enabled in a follow-up PR.

`auto_pause` and `circuit_breaker` in `FLEET_REGISTRY.yaml` are **defined**, **`status: active`**, and **`enforce: false`**.

---

## 5. Change control

1. Protocol and registry changes ship as PRs to `main` in `cth-plugin`.
2. Profile text updates from activation **B** use `docs/fleet/activation/profile-diff.json`; apply only after checker + Gideon GO (not in the registry-only activation PR).
3. Do not edit live bot profiles, routines, or n8n workflows from Hands without a separate ticket and GO.

---

## 6. Decisions for Gideon (resolved 25 Nov 2026 16:56 COT)

| # | Topic | Resolution (active) |
| :--- | :--- | :--- |
| 1 | Tier 2 Workbench fast models | **`fast: true` allowed** only for **Tier 2** and **Tier 4** bot runtime entries in `FLEET_REGISTRY.yaml`. Tier 2 uses `tier-routine` / `cursor-grok-4.5-low-fast`. **Cursor Cloud Hands** remain **`composer-2.5` / `fast: false`**. |
| 2 | Turn-5 / 60k–80k Clone-and-Reset | **PR #181 merged** (25 Nov 2026). Fresh context / clone-and-reset is **adopted** in harness + registry `reset.clone_and_reset: true` for active Tier 0–1 bots. Enforcement of caps is **report-only** until second GO. |
| 3 | Cloud Hands `fast` flag | **Fast OFF** on every **Cursor Cloud Hands** launch (17 Nov lock). Tier 2/4 registry `fast` does not override Hands. |
| 4 | Tier 1 desk count | **65** bots in tier **1a + 1b** (including **one parked**: `e68ca92f`; **`57c40771` UCompensar** added at activation). |
| 5 | Automated weekly remediation | **Report-only** until second GO. Audits flag breaches; no auto-merge, profile mutation, or circuit-breaker **enforce** without approval. |
| 6 | 67% Cursor Hands spend target | Aspirational North Star; harness ticket shape and daily job budget remain authoritative for launches. |

---

*Protocol active; enforcement automation remains report-only until Gideon's second GO.*
