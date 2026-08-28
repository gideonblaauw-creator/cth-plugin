# Ticket Template — CTH Harness

Copy this block into a new file (e.g. `tickets/YYYY-MM-DD-short-name.md`) and fill in every field.
`desk:` is free-form — write the Desk name as it exists or will exist.
See `skills/harness/SKILL.md` for lane definitions, gate rules, and the full Desk list.

---

```
desk:
folder:
done-when:
model: composer-2.5 (fast=false) | gemini-3.7-flash (tiny only, must be named)
lane: github-pr | drive-folder
hitl: nothing sent/posted/paid
reviewer:
context:
```

`model` — Cloud Hands only. Default: `composer-2.5` with `fast=false`. `gemini-3.7-flash` only for tiny jobs and only when the ticket names Flash. Review/eval/brand with no model → HOLD and flag Gideon. See Token lock 2026-08-28 in `skills/harness/SKILL.md` §5.
