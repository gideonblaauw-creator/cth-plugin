# Archive note — harness-engineering into cth-plugin

**Date:** 2026-09-24  
**Ticket:** Adapt harness-engineering into Lane A `cth-plugin` (Gideon GO)  
**Branch:** `feat/harness-engineering-skill`  
**VPS target (preferred SoT):** `/opt/claude-files/Infrastructure/2026-09-24/harness-engineering/`  
**VPS_PLANT:** `PENDING_INFRA` (Cloud VM could not write `/opt/claude-files` at plant time)

## Summary

Merged **adapted** harness-engineering patterns into the existing harness SoT — no second rulebook.

| Item | Path |
|---|---|
| Rulebook (section + version bump) | `skills/harness/SKILL.md` (v3.8.1) |
| CTH-adapted reference | `skills/harness/references/harness-engineering.md` |
| Skill inventory | `skills/harness/references/skill-toolkit.json` (`harness_references`) |
| Pointers | `HARNESS.md`, `AGENTS.md`, `tickets/TEMPLATE.md` |

## Upstream

Patterns adapted from https://github.com/jonzarecki/harness-engineering-skill — not blind-copied.

## Constraints (ticket)

- Understanding Lab **Tier 0** — no lab CTA on this merge.
- **Buffer** dead/inactive — not restored.
- **WA-Voice** untouched.
- No n8n activate, no send/post/pay, no deploy — Gideon merges PR.

## Infra follow-up

Copy this folder (and `receipt.json`) to VPS path when Archive worker is available.
