---
name: legal-eval
description: >
  Hands playbook for Legal Desk clause and playbook review — extract, compare, severity
  route, structured memo. Use when: legal-eval on ticket, clause review, MOU/LOI/agreement
  redline, playbook diff, compliance checklist, governance review. Do not use when: Desk
  comms routing (legal-comms), grants (cth-grant), or commercial proposals (cth-proposal-build).
license: MIT
metadata:
  version: "1.0.0"
  category: programs
  desk: "Legal"
  owner: Infrastructure desk 4b96b1e8
---

# Legal — Eval (Hands playbook)

Hands craft skill for Legal tickets: clause review, playbook comparison, and structured risk memos. **Not licensed counsel.** Output is **proposal only**.

Read `skills/harness/SKILL.md` and `skills/legal-comms/SKILL.md` before executing. First live matter pattern: **AURA** agreements (coordinate with AURA Desk).

## Workflow — six-stage loop

1. **Intake** — Capture matter id, doc type, parties, entity, language, `review_mode`, fine mode if named. Done when: intake block is complete and cite-or-stop rules acknowledged.
2. **Extract** — Pull clauses with citations (section/paragraph). **Cite-or-stop:** no uncited legal claims. Done when: every extracted clause has a source anchor or is marked `unknown`.
3. **Playbook compare** — Match against preferred / fallback / forbidden library (`references/playbook-example.yaml` is EXAMPLE ONLY). Done when: each material clause has preferred, fallback, or gap flagged.
4. **Severity route** — Assign canonical severity (below). Apply hard stops. Done when: every finding has severity + firewall label.
5. **HITL** — Deliver structured memo; list Gideon asks. **No sign/send language.** Done when: memo ends with explicit HITL asks.
6. **Audit + archive** — Separate `[INTERNAL]` memo from `[EXTERNAL]` redlines; store per ticket lane. Done when: counterparty-safe artifacts contain zero internal-only content.

## Review modes

### Coarse modes (ticket field `review_mode:`)

| Mode | Bar | Signature candidates |
|---|---|---|
| `strict` | High; flag ambiguity; prefer withhold/escalate | Allowed when explicitly set |
| `moderate` | Default for commercial consulting packs | Allowed when explicitly set |
| `loose` | Exploratory / early draft only | **Never** |

Default **moderate** for named commercial consulting packs. Signature path requires explicit `review_mode` ≠ `loose`.

### Fine modes (optional on ticket)

Name one when the ticket scopes work narrowly:

`intake_triage` · `extract_only` · `playbook_diff` · `redline_suggest` · `risk_only` · `full_memo` · `template_compare` · `compliance_checklist` · `governance_review`

## Severity rubric (canonical)

Canonical enum for Legal eval findings:

| Severity | Meaning | Done when |
|---|---|---|
| `blocker` | Hard stop; do not proceed without Gideon/counsel | Finding cites hard-stop rule; HITL ask present |
| `negotiate` | Material gap vs playbook; redline or fallback needed | Preferred/fallback path named |
| `accept` | Matches playbook or acceptable fallback | Rationale one line |
| `info` | Note for Desk; no block | Labeled `[INTERNAL]` unless counterparty-safe |
| `unknown` | Missing citation or ambiguous text | Cite-or-stop; no invented law |

### Hard stops (always `blocker`)

- Uncapped liability
- IP assignment of **preexisting** IP to counterparty
- Silent auto-renew **>12 months** without notice
- Unknown governing law
- Missing citation / no approved fallback

### Desk coarse label map (optional reporting)

When Desk asks for coarse labels, map without inventing metrics:

| Coarse | Maps from |
|---|---|
| `critical` | `blocker` |
| `high` | `negotiate` (material) |
| `medium` | `negotiate` (minor) or conditional `accept` |
| `low` | `info` |
| `note` | `info` |

## Clause taxonomy (v0)

Cover at minimum these families (full table: `references/clause-taxonomy-v0.md`):

parties/entity · scope/SOW · fees/payment · term/termination · IP/confidentiality · liability/indemnity · governing law/dispute · data/privacy · non-solicit/non-compete · force majeure · boilerplate · compliance/AML/sanctions · employment/contractor · **S.L. entity naming** (Colombia commercial consulting)

## Entity lock — Spanish S.L.

For CTH commercial consulting:

- Canonical entity: **CLEANTECHHUB INTERNATIONAL S.L.** (Sociedad Limitada).
- Flag wrong entity form or invented labels.
- Severity: `negotiate` or `blocker` in `strict` mode depending on mismatch; at least `negotiate` in `moderate`.

Multi-jurisdiction ES/CO → flag; counsel matrix **[PENDIENTE]**.

## Doc-type defaults

| Doc type | Default review_mode | HITL | Notes |
|---|---|---|---|
| NDA | moderate | Low | Entity + confidentiality focus |
| LOI / MOU | moderate | Medium before send | Flag binding vs non-binding |
| Consulting agreement | moderate | Medium–high before send | Full taxonomy |
| Governance | strict | Counsel/directors | `governance_review` fine mode |

## `[INTERNAL]` / `[EXTERNAL]` firewall

**Every finding** and **every exported pack segment** must be labeled.

| Label | Use |
|---|---|
| `[INTERNAL]` | Playbook rationale, severity scores, internal memo, open questions for Gideon |
| `[EXTERNAL]` | Counterparty-safe redlines and house paper |

Rules:

- Never put `[INTERNAL]` content on counterparty channels.
- External redlines must be safe to share (no playbook YAML, no internal scores).
- Counterparty sees redline/house paper only.

## HITL before sign

- Output is **proposal only**. Forbidden: “approved”, “signed”, “executed”, “binding on CTH”.
- Signature candidate packs require **Gideon HITL** + `review_mode` ≠ `loose`.
- Agent does not own legal risk; library-only redlines.

## Output shape — structured memo

Deliver this structure (example: `references/example-memo.md`):

```markdown
# Legal eval memo — {matter_id}

- **review_mode:** {strict|moderate|loose}
- **fine_mode:** {optional}
- **doc_type:** {NDA|LOI|MOU|Agreement|Governance|…}
- **entity:** CLEANTECHHUB INTERNATIONAL S.L. (check result)
- **language:** {ES|EN|bilingual}

## Summary
{2–5 sentences — [INTERNAL] unless marked EXTERNAL-safe}

## Findings

| Clause | Severity | Firewall | Recommendation |
|--------|----------|----------|----------------|
| … | blocker\|negotiate\|accept\|info\|unknown | INTERNAL\|EXTERNAL | … |

## Open questions
- [INTERNAL] …

## HITL asks for Gideon
- …
```

## Model routing

| Job | Model |
|---|---|
| Tiny extract-only (ticket names it) | `gemini-3.7-flash` |
| legal-eval packs, redlines, memos, repo | `composer-2.5` (`fast=true`) |

## Non-goals

- **Not** a substitute for licensed counsel — flag when counsel required.
- **No secrets** in skill outputs or tickets.
- **Do not invent statutes** or binding legal conclusions.
- **Out of scope:** litigation, LexiScan court-file, uncited legal research.

## Related skills

| Skill | When |
|---|---|
| `legal-comms` | Desk coordination, ticket routing, HITL gates |
| `cleantechhub-brand` | CTH-issued pack formatting |
| `cth-grant` | Donor/grant substance (not mixed with eval playbook) |
| `cth-proposal-build` | Commercial proposal substance |
| `harness` | Ticket contract, lanes |

## References

- [clause-taxonomy-v0.md](references/clause-taxonomy-v0.md) — full taxonomy table
- [severity-rubric.md](references/severity-rubric.md) — severity + hard stops detail
- [example-memo.md](references/example-memo.md) — sample structured memo
- [playbook-example.yaml](references/playbook-example.yaml) — **EXAMPLE ONLY — not counsel-approved**
- Research brief (optional): `/workspace/research/2026-09-15-legal-agents-agreements-mou-loi-cth-harness.md`
