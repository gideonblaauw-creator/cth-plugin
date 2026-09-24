# Harness engineering (CTH-adapted)

**Status:** reference under the harness SoT — not a second rulebook.  
**Canonical rulebook:** `skills/harness/SKILL.md`  
**Upstream patterns (adapted, not copied):** [jonzarecki/harness-engineering-skill](https://github.com/jonzarecki/harness-engineering-skill) — Hashimoto “fix the harness once”, verification loops, context map, multi-session progress, debug catalog.  
**Planted:** 2026-09-24 (Gideon GO, Lane A `cth-plugin`).

**Agent = model + harness.** At CleantechHUB the expensive model is Grok Bot (Orchestrator). Reliability comes from the harness around Cloud Hands: tickets, skills, connectors, verifiers, and Desk review — not from swapping models.

---

## 1. CTH topology (map upstream “harness” to live terms)

| Upstream idea | CTH term | Role |
|---|---|---|
| Router / planner | **Orchestrator** (Grok Bot) | Route, HITL, go/no-go. **Coordination only** — no craft grind (Token lock 2026-08-26). |
| Subject owner | **Desk** | Writes tickets, reviews output, escalates. **No login.** Does not first-draft file packs. |
| Channel I/O | **Workbench** | WhatsApp, Gmail, Calendar, LinkedIn, etc. HITL before send/post/spend. |
| File writer | **Cloud Hands** | Lane A PRs, Lane B Drive packs (bc-id). Not a Desk, not a chat. |
| Invoked APIs | **Tools / connectors** | Composio, Drive, `gh`, MCP — not staffed chats. **Buffer is dead/inactive** — do not restore or route social scheduling through Buffer. |
| Context + rules | **Skills + pointers** | `skills/<name>/SKILL.md`, `AGENTS.md`, `HARNESS.md` (setup only), this rulebook. |
| Human approval | **HITL (band 4)** | Send, post, pay, activate, cutover — Gideon yes in the owning chat. |

**WA-Voice:** untouched by this reference. Do not modify `/opt/cth-voice`, voice desk flows, or WA-Voice automation as part of harness-engineering work.

---

## 2. Graph first → loops

CTH runs **graph-first** orchestration (LangGraph on product repos; Grok + tickets in the org layer), then closes reliability with **loops**:

| Loop | What it does | CTH anchor |
|---|---|---|
| **Heartbeat** | Periodic health / stall detection (Doctor_Bot, Infra pings, automation watch) | `skills/doctor-bot/SKILL.md`; Desk ready-ping after Hands PR |
| **Skill** | Domain playbook loaded when the task matches | `skills/harness/references/skill-toolkit.json`; read `skills/harness/SKILL.md` before every Hands ticket |
| **Maker ≠ checker** | Hands plants; Desk (or Infra) reviews; Gideon merges | Never merge on Hands self-approval alone |
| **Connectors** | Tools with clear schemas; escalate auth to Desk | Tools-session lock — NEED_LOGIN → Desk HITL, same bc-id continues |
| **Verifier** | Mechanical proof before “done” | See §4 — repo validation, Software Factory Prove/Ship, n8n-li on live pilots |

Fix failures by **strengthening the loop**, not by re-prompting the same mistake (Hashimoto principle — §6).

---

## 3. Autonomy bands (1–4)

Use the band on every outbound or irreversible action. When in doubt, **step down** one band.

| Band | Name | Who acts | Typical scope |
|---|---|---|---|
| **1** | **Silent** | Automation / Hands / scripts | Read-only, repo commits on branch, draft PR, internal file plant, validation commands — **no** external send/post/pay/activate |
| **2** | **Desk** | Desk commits subject, tickets Hands, reviews PR/pack | Ticket write, review, escalate, channel draft prep — still **no** send/post/pay without band 4 |
| **3** | **Orch** | Orchestrator routing | Lane/repo choice, model lock, GO/HOLD, HITL gate selection, ready-ping to Gideon |
| **4** | **HITL** | Gideon explicit yes | **Send**, **post**, **pay**, **activate**, **cutover** (production promote, failover flip, live n8n enable, credential rotation go-live) |

Cloud Hands tickets default to **band 1–2** work product; band **4** stays on Desks/Orchestrator/Gideon. Hands do **not** merge, deploy, send, or activate.

---

## 4. Verification loops (highest ROI)

Adapted from upstream verification-loops patterns; mapped to CTH stores.

### 4.1 Lane A — `cth-plugin` (content harness)

“Valid” means **loads** — the harness parses Markdown/JSON:

```bash
jq empty .claude-plugin/plugin.json .mcp.json
# Skill frontmatter + stub/canonical parity (exclude skills/secrets from stub check)
```

See `AGENTS.md` § Cursor Cloud specific instructions.

### 4.2 Lane A — product repos (Software Factory v0)

When `factory: yes` on the ticket:

1. **Prove (eng):** pytest + smoke; UI PRs add before/after evidence.  
2. **Ship:** PR-Agent + visual CI → Infra PASS before Understanding Lab (Tier 1–2).  
3. **Merge:** Gideon only — Hands never merges.

Canonical: `docs/software-factory.md`, `skills/software-factory/SKILL.md`.

### 4.3 Levels (conceptual)

| Level | Check | CTH example |
|---|---|---|
| Schema | Required fields, types, non-empty | Ticket seven-field contract; `jq` on manifests |
| Semantic | Output matches `done-when` | Desk review (maker ≠ checker) |
| Behavioral | End-to-end smoke | Factory smoke, headless Chrome on HTML artifacts, LangGraph eval hooks |

### 4.4 SMART goals + n8n-li verifiers (18 live pilots)

**18 live automation pilots** run with **SMART** `done-when` goals on their Desk tickets and **n8n-li** (lightweight n8n) **verifiers** where Infra has wired them — e.g. webhook receipt, row check, or status node after Hands plants a draft.

**Hands role:** satisfy the ticket and open the PR/pack; attach evidence in the PR body. **Do not** activate n8n, flip production cutover, or treat verifier green as merge authority — Desk review and Gideon merge remain band 4 for outbound/live activation.

**Out of scope for Hands:** enabling n8n from this repo, restoring Buffer, touching WA-Voice.

---

## 5. Context engineering (map, not encyclopedia)

Upstream AGENTS.md “table of contents” rule maps to CTH pointers:

| Surface | Purpose | Max depth |
|---|---|---|
| `skills/harness/SKILL.md` | **Rulebook SoT** — five terms, locks, lanes | Full text (do not duplicate elsewhere) |
| `HARNESS.md` | Cowork/CLI/Cursor **setup** + routing table | Points at rulebook — not a second copy |
| `AGENTS.md` / `CLAUDE.md` | Harness-specific pointers + Skip list | Short |
| `skills/<name>/SKILL.md` | Domain playbooks | Progressive disclosure via `references/` |
| `skills/harness/references/skill-toolkit.json` | Machine-readable skill inventory | Paths only |

**Do not** create `skills/harness-engineering/SKILL.md` as a competing harness. This file is a **reference** under `skills/harness/references/`.

For app repos, Eve (`docs/eve-convention.md`) and product `AGENTS.md` follow the same “map not encyclopedia” rule.

---

## 6. Fix the harness once (Hashimoto)

When Cloud Hands or a Desk sees a **repeatable** mistake:

1. **Classify** — context, tool/connector, verification, scope, session, cost, or architecture (§7).  
2. **Encode at the lowest durable layer:**  
   - Mechanical → script, `jq` check, CI, or ticket `done-when`  
   - Policy → `skills/harness/SKILL.md` or domain skill (minimal diff)  
   - Workflow → Desk ticket template tip or Infra automation (not ad-hoc chat rules)  
3. **Do not** add speculative rules — only after observed failure.  
4. **Maker ≠ checker:** Hands patches; Desk/Infra confirms; Gideon merges rulebook changes on Lane A.

---

## 7. Multi-session progress (Cloud Hands)

Long Hands work spans sessions (bc-id). Bridge sessions with:

| Artifact | Use |
|---|---|
| **Ticket** `context:` + `done-when:` | Single source for scope |
| **Git branch + commits** | Descriptive commits; one PR per ticket when possible |
| **PR description** | What/why, test evidence, blockers |
| **Archive note** (Infra) | VPS `/opt/claude-files/Infrastructure/YYYY-MM-DD/…` when worker exists; else `docs/archive/…` in repo |

Initializer/coder split from upstream applies to **multi-hour product builds** (`factory: yes`), not to every skill edit.

---

## 8. Debug catalog (CTH-flavored)

| Symptom | Likely class | First fix |
|---|---|---|
| Desk wrote the docx/pack itself | Scope / org | Seven-field ticket to Hands; Desk reviews only |
| Hands PR on wrong repo | Context | Lane A repo lock table in `skills/harness/SKILL.md` §5 |
| Grok drafted the grant pack | Token lock | Remap to Cloud Hands; Grok coordinates only |
| Empty bc-id on Drive pack | Verification | Miss — Hands must return bc-id |
| Build launched Flash or Fast off | Model | `composer-2.5` (`fast=true`) for builds; flag miss |
| Review ticket with no model | Policy | HOLD — flag Gideon (no auto-Sonnet) |
| Agent merged or sent mail | Autonomy | Band 4 violation — revert; HITL only |
| Silent JSON/skill breakage | Verification | Run `jq` + YAML frontmatter parity (`AGENTS.md`) |
| “Done” but UI untested | Behavioral | Factory before/after or headless screenshot |
| Buffer / social schedule assumed live | Context | Buffer **dead** — use Socials Desk + Workbench path |
| Touched voice stack | Scope | **WA-Voice untouched** — stop and escalate Infra |
| Local executor crawl/research/pack grind | Hands-ticket HARD | Re-ticket Cloud Hands — `skills/harness/references/hands-ticket-hard.md` |

Full upstream symptom table lives in the source repo’s `reference/debugging-guide.md`; use it for generic agent failures, **plus** this table for CTH org mistakes.

---

## 9. When to read this reference

- Planting or updating **harness** reliability (verification, context pointers, multi-session Handoffs).  
- Writing **Infrastructure** tickets that mention graph loops, autonomy bands, or n8n-li verifiers.  
- **After** reading `skills/harness/SKILL.md` — this doc does not replace the rulebook.

---

## 10. Related paths

| Path | Role |
|---|---|
| `skills/harness/SKILL.md` | Harness SoT |
| `skills/harness/references/hands-ticket-hard.md` | **Desks + Workbenches → Hands** lock (24 Sep 2026); Mail Finder pattern; no local executor grind |
| `tickets/TEMPLATE.md` | Seven-field ticket contract |
| `docs/hands-model-routing.md` | Model fill-in |
| `docs/understanding-lab-tiers.md` | Tier 0 default |
| `skills/infrastructure-comms/SKILL.md` | Infra ready-ping, View PR |
