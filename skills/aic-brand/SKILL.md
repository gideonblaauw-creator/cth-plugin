---
name: aic-brand
description: >
  PROPOSAL, not adopted. Records Americas Innovation Council visual tokens
  observed on the live AIC page for later decks and pages. Use when: AIC deck,
  Bravo Bridge visual, joinaic.com brand, Americas Innovation Council slides.
  Do not use when: CleantechHUB decks (cleantechhub-brand, cth-html-deck) or
  REIN Hubs. Unverified tokens stay [PENDIENTE].
license: MIT
metadata:
  version: "0.1.0"
  category: brand
  status: proposal
---

# AIC brand (PROPOSAL)

**Status: PROPOSAL. Not adopted.** Gideon has not locked these tokens. Every value below is unverified against a brand manual and is marked **[PENDIENTE]**. Use the observed values on AIC work, and keep the proposal comment in the CSS until this file is adopted.

This skill exists because `skills/aic-comms/SKILL.md` had no AIC brand skill. Coordination stays in `aic-comms`. This file is visual tokens only.

## What was read (2026-10-19)

- `skills/aic-comms/SKILL.md` (desk protocol on `main`).
- The AIC comms brief: Americas Innovation Council / Bravo Bridge, founder Frank Cabrera, Gideon as LatAm ambassador, Run Up Holdings sub-project, not CleantechHUB. US and Frank in English. LatAm audience in Spanish when that is the live thread. Domain `joinaic.com` DNS writes stay HITL.
- Live page `https://decks.cleantechhub.net/aic-q1-2027-packages/` (HTTP 200, `text/html`). Title: "AIC · Bay Area IA · Q1 2027 · Viajes curados para líderes financieros de América Latina".
- That page's `styles.css` (`:root`) and `favicon.svg`.
- Slug probe on `decks.cleantechhub.net`: `aic`, `aic-deck`, `bravo-bridge`, `americas-innovation`, `aic-bay-area`, `joinaic`, `aic-q1`, `aic-packages`, `aic-2026`, `aic-2027` returned 404. The 19 Oct 2026 migration report lists `aic-q1-2027-packages` as the only AIC slug. No second AIC deck was found.

The live page is a long scroll, not the 1920×1080 deck shell. Mapping these tokens onto a slide stage is itself **[PENDIENTE]**.

## Identity

- Name on the page: **Americas Innovation Council**, wordmark **AIC**.
- Founder named on the page: **Frank Cabrera**.
- Public link on the page: `https://joinaic.com`.
- Bravo Bridge is the partner name in comms. The live header does not show those words. How Bravo Bridge appears in the lockup is **[PENDIENTE]**.
- Not CleantechHUB. No CTH lime (`#95D5B2`), no CTH green (`#2D6A4F`), no Manual de Marca blues as primary.
- Lane A repo: `https://github.com/gideonblaauw-creator/americas-innovation-hub`. Packs park in `https://github.com/gideonblaauw-creator/runupholdings-matters`. Never `cth-matters`.

## Observed tokens [PENDIENTE]

Read from `:root` in `aic-q1-2027-packages/styles.css`. Confirmed by a brand owner: no.

| Token | Observed | Role on the page | Status |
|---|---|---|---|
| `--ink` | `#070c18` | Page background, theme-color, favicon field | [PENDIENTE] |
| `--navy` | `#0c1528` | Deep surface | [PENDIENTE] |
| `--navy2` | `#111d36` | Deep surface | [PENDIENTE] |
| `--ivory` | `#f4efe6` | Body text | [PENDIENTE] |
| `--muted` | `#a9b1c3` | Secondary text | [PENDIENTE] |
| `--dim` | `#7d869a` | Fine print | [PENDIENTE] |
| `--gold` | `#c9a45c` | Eyebrows, primary button | [PENDIENTE] |
| `--champ` | `#e6cf9f` | Links, focus ring, favicon word | [PENDIENTE] |
| `--gold-d` | `#9c7a3c` | Dark gold | [PENDIENTE] |
| `--plat` | `#c9d3e3` | Platinum | [PENDIENTE] |
| `--line` | `rgba(217,192,143,.18)` | Hairline | [PENDIENTE] |
| `--serif` | `"Cormorant Garamond", "Times New Roman", serif` | Wordmark, headlines | [PENDIENTE] |
| `--sans` | `"Inter", system-ui, sans-serif` | UI and body | [PENDIENTE] |
| `--r` | `18px` | Radius | [PENDIENTE] |

Favicon: 64×64, radius 14, fill `#070c18`, the letters AIC in Georgia at 24px, fill `#e6cf9f`. An official logo file was not on the page. **[PENDIENTE]**.

The scroll page sets some labels at 11px and 12px. That size is not a slide rule. An AIC deck follows `skills/cth-html-deck/SKILL.md`: 1920×1080 stage, scale ×0.96, nothing under 24px on the stage.

## Voice

Executive and specific. The Q1 page speaks to banks, insurers, pension managers, asset managers, fintechs, and supervisors in Latin America. Lead with the trip the institution gets, not the production process.

- English for US-facing and Frank threads.
- Spanish (Latin American) when the live audience is LatAm.
- Do not use the CleantechHUB tagline.
- Do not invent package prices, dates, or visa rules. Unknowns are `[PENDIENTE]`.

## Deck and page use

1. Put this comment at the top of the AIC stylesheet until adoption:

```css
/* AIC brand PROPOSAL — tokens [PENDIENTE] */
```

2. Map the table above onto custom properties. Do not add a sixth hue.
3. Wordmark: serif "AIC" plus tracked sans "Americas Innovation Council". Do not redraw or recolor it.
4. EN/ES toggle, as on the live page (`[data-lang="es"]`, `[data-lang="en"]`).
5. Slide decks use the `cth-html-deck` shell. Only the tokens change.
6. Nothing is sent, posted, or paid without Gideon's yes. DNS for `joinaic.com` stays HITL.

## Do not use when

- CleantechHUB voice or colour → `cleantechhub-brand` and, for slides, `cth-html-deck`
- REIN Hubs → `rein-hubs-comms` (no REIN brand skill on `main`)
- AIC scheduling, WhatsApp, or ticket routing → `aic-comms`
- Adopting these tokens → Gideon. This file does not adopt itself.

## Related skills

| Skill | When |
|---|---|
| `aic-comms` | Desk coordination, repo, HITL. |
| `cth-html-deck` | Interactive slide shell when the ticket is an AIC deck. |
| `cleantechhub-brand` | Never on AIC-only materials. |
