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
hitl: nothing sent/posted/paid
reviewer:
context:
```

`tier` — Lane A Understanding Lab (Gideon lock 2026-09-12). Omit or `0` = **default Ship**: normal draft PR + short what/why; **no lab; no View Understanding Lab CTA**. `1` = Light Understanding (Context ≤½ page, Playground light, one Shared decision row). `2` = Full Lab + ledger (full five-beat PASS). Escalation to 1 or 2 **requires** `escalate:` one-liner. **Ticket MUST name Tier 2** — never default, never infer from scope. `major: yes` without `tier:` is a miss. Canonical: `docs/understanding-lab-tiers.md`. Footer: `docs/view-understanding-lab-footer.md`.

`model` — Cloud Hands only. Allowed: `gemini-3.7-flash` (mechanical) or `composer-2.5` with `fast=false` (repo/code). Review/eval/brand with no model → HOLD and flag Gideon. See Token lock 2026-08-26 in `skills/harness/SKILL.md` §5.
