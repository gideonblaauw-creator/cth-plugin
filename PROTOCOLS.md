# CTH Fleet Operational Protocol

**Status: DRAFT — not active until Gideon GO**

This document is the proposed fleet-wide guardrail set for all **93 bots** (Orchestrator, Desks, Workbenches, Capability Agents, Cloud Hands). It adapts the shared Desk and Workbench base mandate from the **25 Nov 2026** fleet redesign build plan. It does **not** replace the harness rulebook until Gideon merges this file after an explicit GO. Until then, canonical locks remain in the linked skills below.

**Source input (read-only):** `/cursor/stores/bot/fleet-redesign-2026-11-25/build-plan-2026-11-25.md` — Parts 0, 1.1, and 3.2.

**Canonical cross-links (do not fork here):**

| Topic | Canonical skill / doc |
| :--- | :--- |
| Harness terms, tickets, token gates, secrets | [`skills/harness/SKILL.md`](skills/harness/SKILL.md) |
| Cloud Hands model launch | [`skills/hands-model-routing/SKILL.md`](skills/hands-model-routing/SKILL.md) |
| Desk / Workbench → Hands ticketing | [`skills/desks-workbenches-hands-tickets/SKILL.md`](skills/desks-workbenches-hands-tickets/SKILL.md) |
| Secrets SoT pointer | [`skills/infisical/SKILL.md`](skills/infisical/SKILL.md) |

---

## 0. North Star KPIs (fleet token governance)

Targets from the Nov 2026 diagnosis. **Enforcement thresholds** apply only after this protocol is **active** (post-Gideon GO) and supporting automation is verified.

| KPI / governance metric | Baseline (Nov 1–25) | Target state | Hard enforcement threshold (when active) |
| :--- | :--- | :--- | :--- |
| Grok Bot share of spend | 65.7% monthly / 76.9% weekly | ≤ 33% of total spend | Alert at 25% weekly cap; throttle at 30% |
| Cursor Hands share of spend | 33.7% monthly / 23.1% weekly | ≥ 67% of total spend | Default target for code, data, scraping, and decks |
| Max context per Grok Bot turn | 321k max (115k avg) | ≤ 60k tokens | See **PROPOSED** Clone-and-Reset (overlaps PR #181 NO GO) |
| Rapid-fire &lt;15s Grok loops | 82.1% of calls | &lt; 20% of calls | Zero local test/lint/scrape/build loops in Grok Bot |
| Browser CUA (`grok-bot-cua`) | 376 calls | &lt; 2% of total spend | Banned across Tier 2 Workbenches; prefer CLI/API/MCP |
| Weekly audit and protocol PR | Manual / ad hoc | Every Monday 08:00 UTC | Automated pipeline + PR to `PROTOCOLS.md` (HITL merge only) |

---

## 1. Five-tier control plane (93 bots)

`Orchestrator` routes. `Control Tower Infra` checks. Desks own subjects. Workbenches own channels. Cloud Hands writes files. **Logical tiers** below describe token share **targets** from the build plan; they do not override harness ticket fields or Understanding Lab tiers in [`docs/understanding-lab-tiers.md`](docs/understanding-lab-tiers.md).

| Governance tier | Org chart layers | Active count | Model tier (plan label) | Token share cap (plan) | Context and execution mandate |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **Tier 0: Control plane and checker** | Orchestrator, Control Tower Infra | 2 | `tier-reasoning` | ≤ 4% | Routing, ticket validation, maker ≠ checker. No multi-file grind or content factory. |
| **Tier 1: Domain and client Desks** | Desks + isolated client Desks | 63 | `tier-reasoning` / `knowledge-work` | ≤ 16% | Domain memory and scoping. Emit WorkOrders to Cursor Hands for file/deck/code/multi-doc work. |
| **Tier 2: I/O and ops Workbenches** | Workbenches | 19 | `tier-routine` | ≤ 8% | Stateless per trigger. Read-only / channel I/O. Browser CUA banned fleet-wide. |
| **Tier 3: Thin capability wrappers** | Capability Agents | 6 | `tier-routine` / `tier-reasoning` (1–2 turns) | ≤ 5% | Structured specs only; heavy work in Tier 4. |
| **Tier 4: Execution Hands** | Cursor Cloud Hands + OpenCode Cloud Hands | Shared pool | `tier-execution` | ≥ 67% | All heavy execution: repos, VPS Archive, scrapers, HTML/PDF, test loops. |

**Org baseline (25 Nov 2026):** 1 Orchestrator, 34 Desks, 31 Isolated Client Desks, 20 Workbenches, 6 Capability Agents, 1 Cloud Hands lane (plus OpenCode when OSS is requested).

---

## 2. Shared operational rules (all Tier 0–3 bots)

Adapted from build plan §3.2. Where a rule below conflicts with a **locked** harness rule, the harness skill wins (see [§6 Decisions for Gideon](#6-decisions-for-gideon)).

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

Every Cursor Cloud Hands launch uses **`composer-2.5`** with **`model_params: { fast: false }`** (Fast OFF, Gideon 17 Nov 2026). Grok models are forbidden in Hands. Sonnet, Opus, Fast ON, and silent upgrades → HOLD and flag Gideon ([`skills/hands-model-routing/SKILL.md`](skills/hands-model-routing/SKILL.md)).

Ticket `model` field example:

```text
model: composer-2.5 (fast=false)
```

### 2.9 Blackboard and state paths (plan alignment)

Durable cross-harness state belongs on the VPS Archive, not in replayed chat context:

- WorkOrders and tickets: per harness `folder:` under `/opt/claude-files/Projects/…`
- Curated memory (when adopted): `/opt/claude-files/memory/<agent_id>.md`
- Desk session handoffs (when adopted): `/opt/claude-files/state/<desk-slug>.md`

`cth-plugin` on GitHub remains the skill and protocol SoT; VPS `/opt/claude-files` is operational Archive SoT ([`CLAUDE.md`](CLAUDE.md)).

---

## 3. Tier-specific caps (from build plan — aspirational until active)

These caps supplement harness tickets. They do **not** auto-tighten bot profiles until Gideon GO and checker-verified registry sync.

| Tier | Max context (plan) | Turn budget (plan) | Notes |
| :--- | :--- | :--- | :--- |
| 0 | 40k–50k | 3–4 | Checker for all Cloud Hands outputs |
| 1 | 50k–60k | 5 | Client desks stricter isolation under `/opt/claude-files/clients/<slug>/` |
| 2 | 25k | 1 per trigger | `stateless: true`; no CUA |
| 3 | Minimal | 1–2 | Spec emitters only |
| 4 | Scoped by ticket | Per ticket `read-budget` | One job = one fresh, small agent with an exact file list and read budget ([`skills/hands-model-routing/SKILL.md`](skills/hands-model-routing/SKILL.md) § Agent size) |

---

## PROPOSED — not active; overlaps PR #181 NO GO

Gideon **NO GO** on PR #181 (fresh context and thread cap) on **25 Nov 2026, 09:01 COT**. The following rules come from the fleet redesign plan and **must not** be enforced, synced to bot profiles, or automated until Gideon issues a separate GO (and any conflict with PR #181 is resolved).

1. **5-turn / 60k–80k Clone-and-Reset:** Do not allow a Grok Bot thread to exceed 60k–80k tokens or five interactive turns; save state to `/opt/claude-files/state/<agent_id>.md`, emit a five-bullet handoff, and reset the thread. Plan also mandates reset at **Turn 5** or **80k** tokens (North Star table).
2. **Mandatory fresh context on reset:** Replacing long thread history with file-backed state only—not active.
3. **Automated weekly tightening:** Monday audit script auto-lowering `max_context_tokens` on offending Desks—not active.
4. **Mid-week circuit breaker:** Pausing Tier 2 schedules when Grok share ≥ 25% before Friday—not active.

When this block is approved, update `FLEET_REGISTRY.yaml` (future) and bot bundles via checker-reviewed PR—never by Hands alone.

---

## 4. Weekly governance loop (future — draft only)

When active, **Autopilot Workbench** runs a stateless **Monday 08:00 UTC** job that ingests usage CSVs from `/opt/claude-files/audits/raw/`, writes `/opt/claude-files/audits/YYYY-WW-audit.md`, and opens a **draft PR** against `PROTOCOLS.md` and registry files. **Control Tower Infra** checks; **Gideon** merges. Scripts referenced by the plan (`scripts/weekly_token_audit.py`, `scripts/sync_fleet.py`) are **not** part of this PR.

---

## 5. Change control

1. Protocol changes ship as PRs to `main` in `cth-plugin` ([`skills/desks-workbenches-hands-tickets/SKILL.md`](skills/desks-workbenches-hands-tickets/SKILL.md)).
2. This file stays **DRAFT** until Gideon GO on merge—not merely "build approved."
3. Do not edit live bot profiles, routines, or n8n workflows in the same change set as activating this protocol unless a separate ticket and GO say so.

---

## 6. Decisions for Gideon

Where the Nov 2026 build plan conflicts with existing locked rules, **the existing rule wins** in this document until Gideon resolves the row and issues GO to activate.

1. **Tier 2 Workbench model names (plan):** The plan assigns Tier 2 I/O Workbenches to **`cursor-grok-4.5-low-fast`** (`tier-routine`), stateless per trigger. Harness token lock forbids **Grok models on Cloud Hands** and does not adopt plan logical tiers as launch IDs. *Winner today:* Workbench channel I/O stays on harness Workbench rules; Tier 2 model names are **not** fleet-enforced until Gideon maps them to allowed runtime configs.

2. **Turn-5 / 60k–80k Clone-and-Reset (plan):** The plan mandates **5 interactive turns** or **60k–80k tokens** (North Star: mandatory reset at Turn 5 or **80k**), saving state to `/opt/claude-files/state/` and resetting the thread. Gideon **NO GO on PR #181** (fresh context + thread cap) on 25 Nov 2026. *Winner today:* Clone-and-Reset is **not active**; rules live only under **PROPOSED — not active; overlaps PR #181 NO GO** above.

3. **Cloud Hands `fast` flag:** Build plan and `skills/harness/SKILL.md` / `docs/hands-model-routing.md` (22 Oct) describe **`composer-2.5` (`fast=true`)** for every Hands job. Gideon lock **17 Nov 2026** in `skills/hands-model-routing/SKILL.md`: **`composer-2.5` with `fast: false`**. *Winner today:* **Fast OFF** on every Hands launch.

4. **Tier 4 execution model list (plan):** Plan lists **`composer-2.5`, `2.5-fast`, OpenCode** for the shared Hands pool. Locked routing allows **composer-2.5 (fast:false)** and OpenCode only when Gideon says OSS—not **`2.5-fast`** as a default. *Winner today:* skill routing table; plan names deferred.

5. **Automated weekly remediation (plan):** Monday audit auto-PR that tightens `max_context_tokens`, edits `MANDATE.md`, and runs mid-week circuit breakers. Conflicts with **HITL before merge/deploy**, **maker≠checker**, and **infra deploy only on Gideon's GO**. *Winner today:* weekly loop described as **future draft** (§4); no auto-merge or profile mutation without checker + Gideon.

6. **67% Cursor Hands spend target vs harness content waves:** Plan targets ≥67% spend on Tier 4. Harness **Token budget protocol** still allows content batching and risk-based self-check on low-risk jobs. *Winner today:* harness protocol for ticket shape; North Star table is aspirational until active.

---

*Awaiting Gideon's approval before this protocol is injected fleet-wide.*