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
major: yes | no
hitl: nothing sent/posted/paid
reviewer:
context:
```

`major` — Lane A only. `yes` = plant Notion Understanding Lab + mandatory View Understanding Lab PR footer (`docs/view-understanding-lab-footer.md`). `no` or omit when scope is tiny/mechanical. Infer from scope if omitted — see `skills/harness/SKILL.md` § View Understanding Lab.

`model` — Cloud Hands only. Allowed: `gemini-3.7-flash` (mechanical) or `composer-2.5` with `fast=false` (repo/code). Review/eval/brand with no model → HOLD and flag Gideon. See Token lock 2026-08-26 in `skills/harness/SKILL.md` §5.
