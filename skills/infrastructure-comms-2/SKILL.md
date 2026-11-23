---
name: infrastructure-comms-2
description: >-
  DEPRECATED duplicate of infrastructure-comms. Do not use; pending Gideon GO to delete.
---
# Infrastructure comms (duplicate — deprecated)

> **Superseded by `skills/infrastructure-comms/SKILL.md` (pending Gideon GO to delete).**

## 1. End client / who hears what
- End clients: internal CTH stack and vendors. Named vendor contacts: [PENDIENTE] per ticket.
- Gideon chat: English. Vendor facing: language of the live thread.

## 2. Brand
Follow [cleantechhub-brand](sand-workflow:cleantechhub-brand) only for outward-facing infra. Internal runbooks need no brand.

## 3. Coordination only
This desk tickets and reviews. Does not SSH-inventory itself. Does not first-draft skills or protocol docs in the Grok chat.

## 4. Everything ticketed to Hands
Harness / skills / protocol → Lane A `gideonblaauw-creator/cth-plugin`, Composer 2.5 Fast off. Archive / Drive packs → Lane B `{type: machine, name: vps}`. Gideon merges and deploys. Hands does not deploy.

## 5. Model routing (locked 28 Aug 2026)
Follow [hands-model-routing](sand-workflow:hands-model-routing).
- Default / empty ticket: `composer-2.5` Fast off. Not Flash.
- `gemini-3.7-flash`: tiny transform only, and only if the ticket names it.
- High-tier or review/eval/brand: HOLD, flag Gideon.

## 6. Workbench exception
WhatsApp, LinkedIn, Instagram, Facebook, Google Ads, Gmail, Calendar — this desk only, and only when Hands cannot (no CLI, connector, or API).

## 7. HITL
Nothing sent, posted, or paid without Gideon yes. PR merge is Gideon.

### Understanding Lab tiers (locked 2026-09-12)
**Default Tier 0** — ship with PR what/why; no lab CTA.
**Tier 1 / Tier 2** — ticket must name the tier (or one-line escalate). Then follow [View Understanding Lab delivery](sand-workflow:view-understanding-lab-delivery): View PR card **plus** View Understanding Lab. CTA only Tier 1–2.
One-liner: push product at Tier 0; earn trust at Tier 1; prove it at Tier 2.


## GO / NO GO asks (Gideon 22 Nov 2026)
Every GO / NO GO or HITL ask to Gideon uses inline widget buttons, one decision per widget, never prose only. Follow the go-no-go-buttons skill (cth-plugin HARNESS.md, PR #169).