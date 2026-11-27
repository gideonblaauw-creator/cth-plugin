# CleantechHUB Fleet ↔ Atlassian (lean v2)

**Status:** DRAFT · design-only  
**Version:** v2 · 25 Nov 2026  
**Decision:** Gideon Blaauw · 25 Nov 2026 17:45 COT (lean); **17:47 COT** (traceability); **18:29 COT** (HITL channel)  
**Site:** [cleantechhub.atlassian.net](https://cleantechhub.atlassian.net)  
**Social Impact license · ≤25 seats · zero new bot users**

**Out of scope (v2):** Rovo, Loom, email/Slack message mirroring into Jira, Monday CRM mirroring (link field only).

**Core principle (17:47 COT):** **Traceability** — every Jira issue names the **responsible agent** (registry `bot_id`); **accountability** stays with **Gideon (HITL)**. Service accounts only execute API writes and are never the responsible party.

---

## 1. What Jira tracks

| Class | Project | Contents |
| :--- | :--- | :--- |
| Control + HITL | **CTHORCH** | Orchestrator routing, **“waiting on Gideon yes”** queue, fleet dashboard gadgets |
| Ops / health | **CTHOPS** | Doctor_Bot VPS alerts, Engine Room incidents (revive dead token P0) |
| Execution | **CTHHANDS** | Cloud Hands jobs, PR receipts, `bc-id`, verification status |
| Internal fleet | **CTHINT** | All non-client desks, workbenches, capabilities as **components** + `bot_id` labels |
| Client isolation | **28 projects** | One Jira project per `isolation.kind: client` desk — separate permission scheme each |

**Not in Jira:** Gmail bodies, Slack threads, Monday boards (optional URL custom field on client epic only).

---

## 2. Traceability and RACI (all projects)

| RACI | Role | Jira representation |
| :--- | :--- | :--- |
| **R — Responsible** | Fleet agent (desk/workbench/capability) | Required custom field **`Responsible agent`** — text or single-select validated against `FLEET_REGISTRY.yaml` (`bot_id`, 8-char id) |
| **A — Accountable** | Gideon Blaauw (HITL) | Required **`Accountable / Approver`** — always `Gideon Blaauw`; **`HITL approver`** set only from **`#cth-ops-approvals`** button writeback (not the automation user) |
| **C — Consulted** | Owning Desk when different from agent | Optional `parent_id` / component on issue |
| **I — Informed** | Orchestrator | Label or link to CTHORCH epic when cross-desk |

**Hands / execution fields (CTHHANDS + any receipt-linked issue):**

| Field | Required when |
| :--- | :--- |
| `hands_bc_id` | Cloud Hands job created or completed |
| `pr_url` | GitHub PR opened or merged (HITL before merge) |
| `receipt_status` | `open` / `verified` / `blocked` |

**HITL channel (18:29 COT):** CleantechHUB Slack **`#cth-ops-approvals`** — canonical approval surface (WF4 durable-harness pilot, **22 Nov 2026**). **CTH OPS Bot** (existing workspace app) posts GO/approve **button cards**; proven in pilot — no new Slack apps in v2.

Every **`{Gideon yes}`** gate (send, post, merge, deploy, Done, Released):

1. **n8n** (or CTH OPS Bot workflow) opens or updates the linked Jira issue with **`Responsible agent`**, status **“Waiting on Gideon yes”**, and Hands **`bc-id` / `pr_url`** when present.
2. **CTH OPS Bot** posts an **approval card** to **`#cth-ops-approvals`** carrying **Jira issue key**, **responsible agent ID**, and **Hands bc-id / PR link** (and one-line context).
3. Gideon clicks **GO** or **approve** on the card (in-channel; same pattern as HARNESS.md inline HITL buttons).
4. **Writeback** to the Jira issue: custom fields **`HITL approver`**, **`HITL timestamp`**, **`HITL decision`** (`yes` / `no`); comment with Slack message permalink optional.
5. **Only after step 4** may Jira transition to **Done**, **Released**, or the guarded action execute (send/post/merge/deploy). **`no`** returns the issue to a rework status; no side effects.

Jira dashboard **Awaiting HITL** mirrors open gates; **`#cth-ops-approvals`** is the live queue Gideon works from day to day. No webhook URLs or tokens in this design doc.

**Workflow gate (summary):** accountable party remains **Gideon Blaauw**; service accounts never satisfy the gate.

**Automation users (`cth-automation@`, `cth-ops-receipt@`):** technical **creator/updater** only; validator rejects them as `Responsible agent` or `HITL approver` values.

`space-map.csv` columns **`agent_id`** (same as `bot_id`) and **`accountable`** (always HITL row) map registry bots to default responsible values for provisioned components.

---

## 3. Jira project counts

| Bucket | Count |
| :--- | ---: |
| Core (`CTHORCH`, `CTHOPS`, `CTHHANDS`, `CTHINT`) | 4 |
| Client dedicated (`isolation_flag=client_project` in CSV) | 28 |
| **Total Jira projects** | **32** |

Grant-draft isolated desks (3) and all internal tiers map to **CTHINT** components, not separate projects.

---

## 4. Confluence (small surface)

| Space | When | Contents |
| :--- | :--- | :--- |
| **CTHHUB** | Always (P1+) | Fleet hub: Orchestrator dashboard instructions, HITL runbook, ops index, **child pages per bot** (no 94 spaces) |
| **Dedicated client space** | P2 only if justified | External collaborator needs Confluence (not Monday/Slack). Default: **hub page** `CTHHUB+page:{JIRA_KEY}` per client row in CSV |

**Not created in v2:** Loom library, Rovo indexes, per-internal-desk Confluence spaces.

---

## 5. Seats and service accounts

| Identity | Seats |
| :--- | ---: |
| Gideon Blaauw (admin) | 1 |
| Optional human editor | 0–1 |
| `cth-automation@` (n8n Jira/Confluence API) | 1 |
| `cth-ops-receipt@` (Doctor_Bot → CTHOPS) | 1 |
| **Service accounts** | **2–3** |
| Bot registry entries as users | **0** |
| **Headroom under 25** | **≥20** |

Tokens: Infisical **`cth-agents`** only (Gideon OAuth + paste; never in git).

---

## 6. Inbound flows (lean)

| Source | Target | Notes |
| :--- | :--- | :--- |
| Hands PR done | **CTHHANDS** | Receipt issue with **`Responsible agent`** + `bc-id` + `pr_url`; link to CTHINT component or client project |
| HITL gate (`{Gideon yes}`) | **Slack `#cth-ops-approvals`** → **CTHORCH** / child issue | CTH OPS Bot card → GO → Jira writeback → then Done/Released or send/post/merge |
| Doctor_Bot VPS | **CTHOPS** | P0 new token; GREEN=comment, AMBER/RED=issue |
| Desk action / meeting AI | **CTHINT** or client project | Action-item issue type only; meeting source in description, not full transcript |
| Slack · Workbench | **Slack** (channel) | n8n may open Jira task **only** when desk tickets work — not message mirror |
| Gmail · Workbench | **Gmail** | Same; metadata stub optional, not inbox mirror |
| Monday (Teclogi etc.) | **Monday** | Jira epic may store `monday_board_url` custom field |

---

## 7. Orchestrator dashboard (`CTHORCH`)

**Jira dashboard gadgets (no Rovo):**

1. **Awaiting HITL** — JQL `status = "Waiting on Gideon yes"` (fleet filter); paired with live queue in **`#cth-ops-approvals`**
2. **Jobs by responsible agent** — Two-dimensional filter statistics on custom field **`Responsible agent`** (all core + client projects in saved filter `fleet-open-work`)
3. Hands in flight — `project = CTHHANDS AND status != Done`
4. Ops alerts — `project = CTHOPS AND created >= -7d`
5. Internal desk open work — `project = CTHINT AND "Responsible agent" is not EMPTY`
6. Client slice rollup — `labels = client-desk` across 28 projects (saved filter)
7. Confluence **CTHHUB** — Linked pages gadget → hub home + traceability runbook

**Confluence:** `CTHHUB` home embeds gadget links and weekly audit anchor (report-only).

---

## 8. Permission model

| Scheme | Projects |
| :--- | :--- |
| `CTH-Fleet-Internal` | CTHORCH, CTHOPS, CTHHANDS, CTHINT |
| `CTH-Client-{desk_id}` | Each of 28 client keys — browse for Gideon + automation; client guests only when P2 names them |

Automation account: project-scoped tokens per scheme; no cross-client browse.

---

## 9. Rollout

| Phase | Scope | Exit |
| :--- | :--- | :--- |
| **P0** | Gideon refreshes **CTHOPS** API token → Infisical `cth-agents` | Doctor_Bot test issue then close |
| **P1** | **CTHORCH** + **CTHHUB** + core 4 projects; dashboard pilot **2 weeks** | HITL queue + Hands receipts reliable |
| **P2** | Create client Jira project + hub page (or optional Confluence space) **as each client goes active** | 28 rows in CSV provisioned on demand |

Pilot desks unchanged in intent: Teclogi + Sustenttia (client-facing workload; Monday stays SoT for CRM).

---

## 10. What Gideon does

1. Confirm ≤25 seats on Atlassian Social Impact plan.
2. P0: rotate **CTHOPS** token into Infisical.
3. GO: create 4 core projects + **CTHHUB** (P1).
4. HITL on n8n workflow activation (writes only).
5. P2: approve each client project + optional Confluence space.

---

## 11. Risks

| Risk | Mitigation |
| :--- | :--- |
| CTHOPS still 404 | P0 token before P1 dashboard |
| Client project sprawl | P2 on activation only; CSV pre-generates keys |
| Slack/Gmail creep into Jira | Ticket types allowlisted; checker on n8n nodes |
| Usage billing (3 Dec 2026) | No AI add-ons; no Rovo |
| Missing `Responsible agent` | Required field + n8n validation; report-only audit week 1 P1 |
| Service user listed as R | Field validator blocks automation account ids |

---

## 12. Artifacts

| File | Role |
| :--- | :--- |
| `space-map.csv` | 94 bots → `agent_id`, `accountable`, Jira key, Confluence hub |
| `master.dot` / `master.svg` / `master.png` | Desk-level master wiring; `#cth-ops-approvals` on every HITL gate edge |
| `orchestrator-dashboard.dot` / `.svg` / `.png` | Dashboard data flow |
| `master.mmd` | Pointer — canonical render source is `master.dot` |
| `scripts/generate_atlassian_space_map.py` | Regenerate CSV |

---

## 13. References

`FLEET_REGISTRY.yaml`, `PROTOCOLS.md`, `skills/doctor-bot/SKILL.md`, `skills/infisical/SKILL.md`