# desks-workbenches-hands-tickets — Proof before READY

**Status:** reference under the harness SoT — not a second rulebook.  
**Canonical rulebook:** `skills/harness/SKILL.md`  
**Locked:** Gideon **2 Nov 2026**  
**Related:** `skills/harness/references/hands-ticket-hard.md`, `skills/harness/references/harness-engineering.md`, `tickets/TEMPLATE.md`

---

## Scope

Desks and Workbenches write tickets. Cloud Hands executes. A ticket is **READY** for Desk review and Orchestrator ready-ping only when the **Proof** section is complete and a **checker** (not the maker) has verified it.

**READY without proof is invalid.** Treat it as still in progress. Do not ready-ping Gideon on it.

Before launch, read **FEATURE-MAP.md** for the ticket’s area (repo root or area folder). When Hands changes that area, update **FEATURE-MAP.md** in the same PR.

---

## Required Proof section (every ticket)

Fill `proof:` on the ticket (see `tickets/TEMPLATE.md`). Attach artifacts in the PR body, Archive path, or `/opt/cursor/artifacts/` on the Hands run.

| Job kind | Required evidence |
|---|---|
| **Decks** | Per-slide screenshots; logged-out page checks (document URL, HTTP 200 on page, HTTP 200 on linked assets) |
| **Data jobs** | CSV row counts **before** and **after**; schema (column names + types or header row) |
| **Deploys** | Logged-out HTTP 200 on the served URL; **sha** of the file or bundle the edge serves |
| **Other** | Hash, HTTP status, or test output that matches `done-when` |

### Maker ≠ checker

The agent or model that **made** the change does **not** sign off alone. A **different** Cloud Hands run, subagent, or model (**checker**) re-runs the checks and records its **bc-id** (or agent id) in `proof.checker`. Low-risk self-check from Token budget protocol (22 Oct 2026) does **not** satisfy READY — it only reduces launch cost; READY still needs a separate checker line in Proof.

---

## Ready-ping checklist

1. Ticket `proof:` complete for the job kind.  
2. Checker identity recorded (not the maker bc-id).  
3. PR / URL + maker **bc-id** + paths (Hands-ticket HARD).  
4. FEATURE-MAP updated when the area changed.

Protocol changes ship as a PR to `cth-plugin` (HITL merge by Gideon). Hands does not merge.
