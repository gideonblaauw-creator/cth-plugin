---
name: legal-comms
description: >
  Communications protocol for the Legal Desk. Trigger on Legal Desk comms, agreements,
  MOUs, LOIs, compliance packs, or governance packs. Grok Bot coordination only;
  clause/playbook evals → Cloud Hands via legal-eval (Token lock 2026-08-26).
  Do not use when: executing clause review (legal-eval) or grant/proposal playbooks.
license: MIT
metadata:
  version: "1.0.0"
  category: comms
  desk: "Legal"
  owner: Infrastructure desk 4b96b1e8
---

# Legal — Comms

Desk communications playbook. Grok Bot = **coordination only** (Token lock 2026-08-26). Read `skills/harness/SKILL.md` before any ticket.

**Scope:** Agreements, MOUs, LOIs, compliance packs, governance packs. **Out of scope:** litigation, court-file work, LexiScan court-file flows.

## 1. End client / who hears what

- **End clients / counterparties:** Commercial consulting counterparties (Colombian packs default **Spanish** unless the live thread is English). Grant, proposal, and program counterparties per owning Desk language.
- **Who hears what:** Counterparty-facing packs → language of the live thread (Colombian commercial consulting → **Spanish** default). Gideon ↔ Desk → **English** unless Spanish thread.
- **Internal:** Gideon Blaauw (HITL). Owner profile: Legal desk **4b96b1e8**. Desk **reviews** Hands output (maker ≠ checker). Reports to **Orchestrator**.
- **First live matter:** **AURA** agreements — coordinate with **AURA Desk** (`skills/aura-comms/SKILL.md`). Also coordinates **Grants**, **Proposals**, and **CEE Externado** when Legal is named reviewer.

## 2. Brand skill to follow

`cleantechhub-brand` for CTH-issued packs and outward-facing Legal comms. No client-brand leak.

No brand leak across clients. Co-brand only when Gideon explicitly approves.

## 3. Coordination only — never invent law

Grok Bot on this Desk is **coordination only** (Token lock 2026-08-26). Route, HITL, go/no-go, and channel I/O escalation.

- Desk **tickets** Cursor Cloud Hands.
- Desk **reviews** output (maker ≠ checker).
- **Never invent law**, statutes, entity labels, or counsel conclusions in the Grok chat.
- Clause/playbook evaluation → ticket Hands with skill **`legal-eval`** (not this comms skill).
- No first-draft packs, research grind, inventory, or code in the Grok chat.
- Do not write Grok Bot box workflows in this skill.

## 4. Everything file/research/code/copy is ticketed to Cursor Cloud Hands

All agreement packs, clause reviews, redlines, inventories, HTML/docx, and repo work → **seven-field ticket** to Cursor Cloud Hands. No bc-id = miss.

- Lane A (this repo and other owning repos): `lane: github-pr`
- Lane B (grant/client packs on Drive): `lane: drive-folder`
- **Lane A repo / store for this Desk:** Legal playbooks → `cth-plugin`; matter packs → Drive folder on ticket.
- Ticket template: `tickets/TEMPLATE.md`
- Read `skills/harness/SKILL.md` before launching Hands.

### Ticket fields (Legal)

| Field | Rule |
|---|---|
| `review_mode:` | Coarse: `strict` \| `moderate` \| `loose`. Default **moderate** for named commercial consulting packs. **`loose` never** for signature candidates. Signature path requires explicit mode ≠ `loose`. |
| Fine mode (optional) | `intake_triage`, `extract_only`, `playbook_diff`, `redline_suggest`, `risk_only`, `full_memo`, `template_compare`, `compliance_checklist`, `governance_review` — name on ticket when needed. |
| `skill:` | Clause/playbook eval → **`legal-eval`**. Comms-only routing stays on this skill. |

### Doc-type HITL defaults

| Doc type | Default HITL | Notes |
|---|---|---|
| NDA | Low | Still firewall + entity check |
| LOI / MOU | Medium — HITL before send | Flag **binding vs non-binding** |
| Consulting agreement | Medium–high — HITL before send | Default `review_mode: moderate` |
| Governance pack | Always counsel/directors | Escalate; agent proposes only |

## 5. Lowest-tier model

| Job | Model | Notes |
|-----|-------|-------|
| Tiny extract-only (ticket names it) | `gemini-3.7-flash` | Flash only when ticket names tiny extract |
| Repo / code / build Hands, legal-eval packs | `composer-2.5` (`fast=true`) | Fast ON for builds (t1263u) |
| Review / eval / brand with no model | **HOLD** | Flag Gideon. No auto-Sonnet/Opus/Grok |

Never silently use Sonnet, Haiku, Opus, or Grok on Cloud Hands. Legal desk **builds** use Composer 2.5 Fast ON (t1263u); mechanical/tiny stay Flash when ticket names them.

## 6. Workbench exception

Gmail ingest only via **Inbox Desk** Workbench; this Desk tickets Hands for drafts.

Shared across Desks: **WhatsApp** reports to Orchestrator (not this Desk). Drive, GitHub, Buffer, Monday, Notion are **Tools**, not Workbenches.

Workbench is **not** a default and **not** a second Hands. Use only when Hands cannot do the step (no CLI, no connector, no API). HITL before send/post/pay/sign.

## 7. HITL — hard before sign / send / pay

Nothing **signed**, **sent**, or **paid** without **Gideon Blaauw** yes in the owning chat.

- Agent output is **proposal only**. No “approved”, “signed”, or “executed” language from Hands.
- Signature candidate packs require **Gideon HITL** + `review_mode` ≠ `loose`.
- Agent does **not** own legal risk; library-only redlines; no counterparty send without firewall pass.

## 8. Entity lock — Spanish S.L.

For CTH **commercial consulting** entity naming:

- Canonical full name: **CLEANTECHHUB INTERNATIONAL S.L.** (Sociedad Limitada).
- Entity form lock: Spanish **S.L.** — no invented entity labels without Gideon lock.
- ES+EN clause library preferred/fallback. Multi-jurisdiction ES/CO → flag; counsel matrix **[PENDIENTE]**.

## 9. `[INTERNAL]` / `[EXTERNAL]` firewall

Every finding and every exported pack segment must be labeled **`[INTERNAL]`** or **`[EXTERNAL]`**.

- Counterparty never sees playbook YAML, severity scores, or internal memo content — only redline/house paper marked **`[EXTERNAL]`**.
- Never put **`[INTERNAL]`** content on counterparty channels.
- External redlines must be safe to share.

## 10. Six-stage Hands loop (Legal eval tickets)

Bounded first-pass loop for **`legal-eval`** tickets (Hands executes; Desk reviews):

1. **Intake** — matter id, doc type, review_mode, entity, language.
2. **Extract** — cite-or-stop; no uncited claims.
3. **Playbook compare** — preferred / fallback / forbidden vs library.
4. **Severity route** — canonical enum (see `legal-eval`).
5. **HITL** — proposal to Gideon; no sign/send.
6. **Audit + archive** — labeled segments; Drive or repo per ticket.

Done when: each stage output is labeled and Desk can review without guessing channel.

## 11. Secrets (Infisical SoT — Gideon 2026-09-07)

Service secrets → **Infisical** (`skills/secrets/SKILL.md`). Never paste token values in tickets, PRs, or chat. Hands fetch by project / environment / key name only.

## Related skills

| Skill | When |
|---|---|
| `legal-eval` | Clause review, playbook diff, redline suggest, risk memo |
| `aura-comms` | AURA agreement coordination (first live matter) |
| `cth-grants-comms` | Donor/grant agreement threads owned by Grants |
| `cth-proposals-comms` | Commercial proposal agreement threads |
| `cleantechhub-brand` | CTH-issued pack visual/copy |
| `harness` | Tickets, lanes, Cloud Hands boundary |

## References

- Research brief (optional): `/workspace/research/2026-09-15-legal-agents-agreements-mou-loi-cth-harness.md` — may be absent on Hands VM; locks above are authoritative.
- `skills/legal-eval/SKILL.md` — eval playbook, severity, output shape.
- `skills/legal-eval/references/playbook-example.yaml` — EXAMPLE ONLY skeleton (not counsel-approved).
