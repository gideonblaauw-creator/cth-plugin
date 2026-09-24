# Archive note — Hands-ticket HARD into cth-plugin

**Date:** 2026-09-24  
**Ticket:** Plant Hands-ticket HARD into Lane A `cth-plugin` (Gideon / Orch GO)  
**Branch:** `feat/hands-ticket-hard`  
**VPS target (preferred SoT):** `/opt/claude-files/Infrastructure/2026-09-24/hands-ticket-hard/`  
**VPS_PLANT:** `PENDING_INFRA` (Cloud VM could not write `/opt/claude-files` at plant time)

## Summary

Merged **Hands-ticket HARD** into the existing harness SoT — no second rulebook. Builds on PR #42 `harness-engineering` reference (cross-linked, not duplicated).

| Item | Path |
|---|---|
| Rulebook (section + version bump) | `skills/harness/SKILL.md` (v3.8.2) |
| Reference playbook | `skills/harness/references/hands-ticket-hard.md` |
| Skill inventory | `skills/harness/references/skill-toolkit.json` (`harness_references`) |
| Pointers | `HARNESS.md`, `AGENTS.md`, `tickets/TEMPLATE.md` |
| Cross-link | `skills/harness/references/harness-engineering.md` §10 |

## Constraints (ticket)

- Understanding Lab **Tier 0** — no lab CTA on this merge.
- **Buffer** / **WA-Voice** untouched.
- No merge, deploy, send, activate — Gideon merges PR.

## Infra follow-up

Copy this folder (and `receipt.json`) to VPS path when Archive worker is available.
