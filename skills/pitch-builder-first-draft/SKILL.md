---
name: pitch-builder-first-draft
description: >
  First-draft funder/investor deck narrative via Pitch Builder, then handoff to CTH HTML
  deck build. Use when: grant deck, donor pitch, 10-slide narrative, investor storyline
  before Presentations HTML. Do not use when: commercial client proposals (cth-proposal-build)
  or diagram-only figures without a deck story (diagram-design alone).
license: MIT
metadata:
  version: "1.0.0"
  category: programs
---

# Pitch Builder — first draft (grant / funder deck)

CleantechHUB grant and Presentations workflows start with a **structured 10-slide narrative**, then move to branded HTML deck build.

## AI Apps for Good step (2026-11-04)

1. **Pitch Builder** — Open [Pitch Builder](https://aiappsforgood.org/pitchbuilder.html). Answer the 10 guided questions (voice or text). Complete the sharpen round. Export or copy the **10-slide narrative** (problem, solution, impact, ask).
2. **CTH handoff** — Paste the narrative into the Presentations / grant-deck ticket. Hands build the **CTH HTML deck** using `cleantechhub-brand` tokens and `diagram-design` for figures. No Mermaid deliverables.
3. **Approval** — Donor-facing deck copy remains **Awaiting Gideon's approval** before send.

Done when: ticket includes Pitch Builder slide outline plus CTH-branded HTML deck path or PR.

## Rules

- Do not paste secrets, beneficiary PII, or unreleased funder terms into Pitch Builder.
- Pitch Builder sends input to **Claude (Anthropic)** per AI Apps for Good terms; use only non-confidential draft material.
- This skill does not replace `cth-grant` go/no-go, budget, or MEL design.

## Related skills

| Skill | When |
|---|---|
| `cth-grant` | Full grant lifecycle, MEL, submission |
| `diagram-design` | HTML+SVG figures inside the deck |
| `cleantechhub-brand` | Colors, tone, layout |
