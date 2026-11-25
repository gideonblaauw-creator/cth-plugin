# Seven org-chart gaps — proposed registry/profile changes (draft)

**Date:** 2026-11-25  
**Source:** `build-plan-2026-11-25.md` Part 1.2  
**Scope:** Text-only proposals for `FLEET_REGISTRY.yaml` / future `bots/<id>/profile.yaml` sync. **No live Grok Bot profiles were edited.**

All enforcement fields remain `off` until Gideon merges governance PRs and activates sync.

---

## Gap 1 — Explicit parents for 36 `parent not stated` bots

| | |
|---|---|
| **Before** | Org chart v1 marks 36 bots with `parent_stated: false`. Routing falls back through Orchestrator hops; cached context inflates on every turn. |
| **After (proposed)** | `FLEET_REGISTRY.yaml` sets an explicit `parent.id` for each orphan (mostly `5dc64ea4` Orchestrator; workbenches report owning desks per §3.1D). Each carries `parent.proposed: true` and `enforcement: off` until profile metadata is updated in Grok. |

---

## Gap 2 — Archive parked Chamber Bucaramanga (`e68ca92f`)

| | |
|---|---|
| **Before** | Two Chamber bots: active `67e509f7` and parked duplicate `e68ca92f`. Risk of split state and double triggers. |
| **After (proposed)** | Registry `status: parked` on `e68ca92f`; plan target is `archived` with triggers disabled on merge. All Chamber work routes to `67e509f7` only. |

---

## Gap 3 — Teclogi ← Monday Teclogi fold-in (`2592cf74` → `27bd8324`)

| | |
|---|---|
| **Before** | Teclogi profile claims Monday board fold-in (22 Nov 2026), but `Monday · Teclogi` remains a standalone isolated desk. |
| **After (proposed)** | Registry parent for `2592cf74` is `27bd8324` with `fold_in.into` and decommission note. Monday mutations become a Hands-invoked sub-skill, not a second desk thread. |

---

## Gap 4 — Sustenttia ← Sustenttia Fillout (`49495613` → `7ffbe815`)

| | |
|---|---|
| **Before** | Sustenttia profile claims Fillout fold-in; Fillout workbench still reports to Orchestrator as orphan. |
| **After (proposed)** | Registry parent `7ffbe815`, tier-2 stateless Fillout I/O only; scoring and HTML stay on Sustenttia + Cursor Hands. |

---

## Gap 5 — Health reporting chain (`fbc6f772`)

| | |
|---|---|
| **Before** | Health workbench profile lists Control Tower · Infra; Engine Room and plan disagree on first-hop routing. |
| **After (proposed)** | Health `parent.id: 85949e8a` (Engine Room · Workbench) with `proposed: true`. Engine Room escalates verified fix tickets to Control Tower Infra for Maker ≠ Checker. |

---

## Gap 6 — Normalize `isolated` metadata tags

| | |
|---|---|
| **Before** | Profiles use a single `isolated` flag without distinguishing client, workstream, and personal desks. |
| **After (proposed)** | Registry adds `isolation.kind` per bot: `client` (29 partner desks), `workstream` (CTH Grants, GTM, Strategy, Advisory Board), `personal` (Ruben, GINA, Natalia, Careers, Travel, Markets, Mac Scan). `enforcement: off`. |

---

## Gap 7 — Slack/Telegram vs Autopilot vs X trio boundaries

| | |
|---|---|
| **Before** | Watch-item overlap: human Slack/Telegram I/O, n8n-li automation, and X editorial/API work lack hard registry separation. |
| **After (proposed)** | Registry documents: `6b334caf` Slack and `7df0969f` Telegram under Orchestrator (read-only I/O); `f8b4b4c2` Autopilot under Control Tower for n8n-li alerts only; `22eef082` owns CTH social strategy, `f1a2eba2` owns @BlaauwGideon editorial, `25fc96f0` emits Hands tickets for X API code (no keys in chat). |

---

**Awaiting Gideon's approval:** merging this draft or activating profile sync still requires a separate GO.