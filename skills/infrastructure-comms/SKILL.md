---
name: infrastructure-comms
description: >
  Use when talking to Gideon about harness, Claude Infrastructure, stack tickets,
  or Understanding Lab tiers on Hands finishes. Coordination only; ticket craft to
  Hands. Composer Fast ON for builds.
metadata:
  version: "2.0.0"
  category: comms
  desk: Control Tower · Infra
---

# Infrastructure comms

Canonical merge of `infrastructure-comms` + `infrastructure-comms-2` (box 22 Nov 2026). Extended tier, factory, secrets, and Cursor Projects sections from prior `cth-plugin` canonical live only in git history until Gideon replants them (see PR body).

## 1. End client / who hears what

- End clients: internal CTH stack and vendors. Named vendor contacts: **[PENDIENTE]** per ticket.
- Gideon chat: English. Vendor facing: language of the live thread.

## 2. Brand

Follow `skills/cleantechhub-brand/SKILL.md` only for outward-facing infra. Internal runbooks need no brand.

## 3. Coordination only

This desk tickets and reviews. Do not SSH-inventory itself. Do not first-draft skills or protocol docs in the Grok chat.

## 4. Everything ticketed to Hands (HARD — 24 Sep 2026)

Follow `skills/desks-workbenches-hands-tickets/SKILL.md`. Harness / skills / protocol → Lane A `gideonblaauw-creator/cth-plugin`, Composer 2.5 **Fast ON** for builds. Archive / Drive packs → Lane B `{type: machine, name: vps}`. Gideon merges and deploys. Hands does not deploy. Local executor grind is a protocol miss.

## 5. Model routing (locked 13 Sep 2026 — t1263u Fast ON for builds)

Follow `skills/hands-model-routing/SKILL.md`.

- **Builds** (repo/code, LangGraph, Lane A, Signal Radar, LexiScan, scanner, harness): `composer-2.5` Fast ON. Never silently Fast off.
- `gemini-3.7-flash`: tiny transform only, and only if the ticket names it.
- High-tier or review/eval/brand: HOLD, flag Gideon. No Opus/Grok.

## 5b. Playground format (locked 13 Sep 2026 — t1268u)

**All Understanding Lab / HITL playgrounds = LexiScan standard format.** Do not invent a new layout per product.

- Canonical: `gideonblaauw-creator/fabfloow-lexiscan` → `understanding-lab/playground/` (`index.html`, `app.js`, `data.js`, `styles.css`, `README.md`, `smoke.sh`)
- Mechanics: HTML house tour, quests + quizzes + decision doors, EN+ES, localStorage persistence, ledger + download JSON/MD, `smoke.sh`
- Ownership: Infra owns shared format lock; FabFloow owns LexiScan product only
- Ticket field for Tier 1–2: `playground = LexiScan standard format` (or `playground_standard: lexiscan-html-v2`)
- Scanner `hitl/microworld/` tabbed shell is **legacy** — remediate toward house tour
- Product chrome/brand per desk; never CTH lime on non-CTH products
- Canonical plant: `docs/understanding-lab-playground-standard.md`

## 6. Workbench exception

WhatsApp, LinkedIn, Instagram, Facebook, Google Ads, Gmail, Calendar — connector I/O only when Hands cannot (no CLI, connector, or API). Never use this exception for crawl/research/file-pack grind.

## 7. HITL

Nothing sent, posted, or paid without Gideon yes. PR merge is Gideon.

### Understanding Lab tiers (locked 2026-09-12)

**Default Tier 0.** Ticket must name Tier 1 or 2 to escalate.

On every Hands finish in this chat: **lead with `Tier 0` / `Tier 1` / `Tier 2`**. Lab CTA only with Tier 1 or 2 named in the same message; per-build `lab_notion:` URLs. Follow `skills/view-hitl-lab-delivery/SKILL.md`.

One-liner: push product at Tier 0; earn trust at Tier 1; prove it at Tier 2.

## GO / NO GO asks (Gideon 22 Nov 2026)

Every GO / NO GO or HITL ask to Gideon uses inline widget buttons, one decision per widget, never prose only. Follow `HARNESS.md` § GO / NO GO decisions (PR #169).