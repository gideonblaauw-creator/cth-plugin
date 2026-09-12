# Ticket Template — CTH Harness

Copy this block into a new file (e.g. `tickets/YYYY-MM-DD-short-name.md`) and fill in every field.
`desk:` is free-form — write the Desk name as it exists or will exist.
See `skills/harness/SKILL.md` for lane definitions, gate rules, and the full Desk list.

---

```
desk:
folder:
done-when:
model: gemini-3.7-flash | composer-2.5 (fast=false)
lane: github-pr | drive-folder
tier: 0 | 1 | 2
escalate:
langgraph: yes
lab_notion:
  lab_context_url:
  lab_playground_url:
  lab_shared_decisions_url:
hitl: nothing sent/posted/paid
reviewer:
context:
```

`tier` — Lane A Understanding Lab (Gideon lock 2026-09-12). Omit or `0` = **default Ship**: normal draft PR + short what/why; **no lab; no View Understanding Lab CTA**. `1` = Light Understanding (Context ≤½ page, Playground light, one Shared decision row). `2` = Full Lab + ledger (full five-beat PASS). Escalation to 1 or 2 **requires** `escalate:` one-liner. **Ticket MUST name Tier 2** — never default, never infer from scope. `major: yes` without `tier:` is a miss. Canonical: `docs/understanding-lab-tiers.md`. Footer: `docs/view-understanding-lab-footer.md`.

`langgraph` — optional. Set `langgraph: yes` for a **production / client agent graph**. Hands follows `skills/langgraph-production/SKILL.md` on the owning product repo (`composer-2.5`, `fast=false`). OpenCode is OSS experiments only — never a client deploy path. Omit when the ticket is not a LangGraph build.

`lab_notion` — **required on Tier 1–2.** This build’s / this product’s Understanding Lab Notion URLs. Flat aliases: `lab_context_url` / `lab_playground_url` / `lab_shared_decisions_url`. **Every build gets its own pages** (Gideon 2026-09-12 via FabFloow). Do not reuse Scanner (Dataroom / VertiGreen) URLs for LexiScan, Sustenttia, or other products. If omitted on Tier 1–2: Infra posts Tier label + View PR only and flags missing lab pages — **does not** paste Scanner links. Unused on Tier 0. LangGraph HITL maps `interrupt()` to these URLs — see `skills/langgraph-production/SKILL.md`.

`model` — Cloud Hands only. Allowed: `gemini-3.7-flash` (mechanical) or `composer-2.5` with `fast=false` (repo/code). Review/eval/brand with no model → HOLD and flag Gideon. See Token lock 2026-08-26 in `skills/harness/SKILL.md` §5.
