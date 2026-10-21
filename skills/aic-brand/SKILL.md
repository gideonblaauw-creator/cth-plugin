---
name: aic-brand
description: >
  PROPOSAL, not adopted. Records Americas Innovation Council tokens. The A1
  block (Cormorant Garamond, Inter, ink, gold, type-only mark, 7-section
  configurator) is OBSERVED. Use when: AIC deck, Bravo Bridge visual,
  joinaic.com brand, Americas Innovation Council slides. Do not use when:
  CleantechHUB decks (cleantechhub-brand, cth-html-deck) or REIN Hubs.
  Pending rows are --navy, --navy2, --ivory, --muted, --dim, --champ,
  --gold-d, --plat, --line, and --r.
license: MIT
metadata:
  version: "0.1.0"
  category: brand
  status: proposal
---

# AIC brand (PROPOSAL)

**Status: PROPOSAL. Not adopted.** Gideon has not locked these tokens. This proposal marks one block OBSERVED. A1 copied the values from the live page and did not use that label. Rows that stay `[PENDIENTE]` are `--navy`, `--navy2`, `--ivory`, `--muted`, `--dim`, `--champ`, `--gold-d`, `--plat`, `--line`, and `--r`. OBSERVED rows are the favicon, the seven-section shape, the type-only mark, and the second-table rows `--ink`, `--gold`, `--serif`, and `--sans` (ink `#070c18`, gold `#c9a45c`, Cormorant Garamond, Inter). The proposal is still not adopted. Use the observed values on AIC work, and keep the proposal comment in the CSS until this file is adopted.

This skill exists because `skills/aic-comms/SKILL.md` had no AIC brand skill. Coordination stays in `aic-comms`. This file is visual tokens only.

## What was read (2026-10-19)

- `skills/aic-comms/SKILL.md` (desk protocol on `main`).
- The AIC comms brief: Americas Innovation Council / Bravo Bridge, founder Frank Cabrera, Gideon as LatAm ambassador, Run Up Holdings sub-project, not CleantechHUB. US and Frank in English. LatAm audience in Spanish when that is the live thread. Domain `joinaic.com` DNS writes stay HITL.
- Live page `https://decks.cleantechhub.net/aic-q1-2027-packages/` (HTTP 200, `text/html`). Title: "AIC · Bay Area IA · Q1 2027 · Viajes curados para líderes financieros de América Latina".
- That page's `styles.css` (`:root`) and `favicon.svg`.
- Slug probe on `decks.cleantechhub.net`: `aic`, `aic-deck`, `bravo-bridge`, `americas-innovation`, `aic-bay-area`, `joinaic`, `aic-q1`, `aic-packages`, `aic-2026`, `aic-2027` returned 404. The 19 Oct 2026 migration report lists `aic-q1-2027-packages` as the only AIC slug. No second AIC deck was found.

The live page is a 7-section configurator, not a 16:9 deck. That shape is **OBSERVED** (A1). Mapping the tokens onto a 1920×1080 slide stage is still **[PENDIENTE]**.

## Identity

- Name on the page: **Americas Innovation Council**, wordmark **AIC**.
- Founder named on the page: **Frank Cabrera**.
- Public link on the page: `https://joinaic.com`.
- Bravo Bridge is the partner name in comms. The live header does not show those words. How Bravo Bridge appears in the lockup is **[PENDIENTE]**.
- Not CleantechHUB. No CTH lime (`#95D5B2`), no CTH green (`#2D6A4F`), no Manual de Marca blues as primary.
- Lane A repo: `https://github.com/gideonblaauw-creator/americas-innovation-hub`. Packs park in `https://github.com/gideonblaauw-creator/runupholdings-matters`. Never `cth-matters`.

## Observed on the live page (A1)

A1 (`docs/deck-audit/A1-decks-cleantechhub.md`, `deck-skill-audit-a1` @ `0c39db1`, 19 Oct 2026) read `https://decks.cleantechhub.net/aic-q1-2027-packages/`. These rows are **OBSERVED**. The proposal is still not adopted.

| Fact | Observed value | Status |
|---|---|---|
| Display | Cormorant Garamond, weights 500, 600, 700, italic 500 and 600. Fallback Times New Roman, then serif. CSS `--serif`. | OBSERVED |
| Body | Inter, weights 300, 400, 500, and 600. CSS `--sans`: `"Inter", system-ui, -apple-system, "Segoe UI", sans-serif`. | OBSERVED |
| Ink | `#070c18` (`--ink`). Page background, theme-color, and favicon fill. | OBSERVED |
| Gold | `#c9a45c` (`--gold`). Eyebrows, selected border, and step numbers. | OBSERVED |
| Mark | Type only. No image logo. Header lockup: “AIC” in Cormorant Garamond, a gold-tint rule, then “Americas Innovation Council” in tracked Inter. | OBSERVED |
| Favicon | `favicon.svg`. 64×64 rounded rectangle, radius 14, fill `#070c18`. Letters AIC in Georgia, 24px, weight 600, fill `#e6cf9f`. | OBSERVED |
| Product | Seven scroll sections: hero, why, event picker, tier picker, city picker, visa and timing, close. Not a 16:9 deck. No `.deck-frame`. | OBSERVED |

Footer links on that page: `joinaic.com` and `americasinnovationcouncil.com`. **OBSERVED**. Language is an EN | ES pill, Spanish by default, copy in `data-i18n`. The choice is not stored. **OBSERVED**.

## Other tokens [PENDIENTE]

Also read from `:root` in `aic-q1-2027-packages/styles.css`. A brand owner has not locked them.

| Token | Observed | Role on the page | Status |
|---|---|---|---|
| `--ink` | `#070c18` | Page background, theme-color, favicon fill | OBSERVED |
| `--navy` | `#0c1528` | Event cards | [PENDIENTE] |
| `--navy2` | `#111d36` | Second navy | [PENDIENTE] |
| `--ivory` | `#f4efe6` | Body text | [PENDIENTE] |
| `--muted` | `#a9b1c3` | Secondary text, brand name | [PENDIENTE] |
| `--dim` | `#7d869a` | Fine print | [PENDIENTE] |
| `--gold` | `#c9a45c` | Eyebrows, selected border, step numbers | OBSERVED |
| `--champ` | `#e6cf9f` | Links, italic emphasis, favicon letters. The live page also uses it for the `:focus-visible` outline. | [PENDIENTE] |
| `--gold-d` | `#9c7a3c` | Deep gold | [PENDIENTE] |
| `--plat` | `#c9d3e3` | Platinum, premium tier | [PENDIENTE] |
| `--line` | `rgba(217,192,143,.18)` | Hairline on the gold hue | [PENDIENTE] |
| `--serif` | `"Cormorant Garamond", "Times New Roman", serif` | Wordmark, headlines | OBSERVED |
| `--sans` | `"Inter", system-ui, -apple-system, "Segoe UI", sans-serif` | UI and body | OBSERVED |
| `--r` | `18px` | Radius | [PENDIENTE] |

The favicon file is `favicon.svg`, described in the observed block. An official logo image was not on the page. **[PENDIENTE]**.

The scroll page sets some labels at 11px and 12px. That size belongs to the configurator. It is not a 16:9 slide rule. A ticket that asks for an AIC slide deck follows `skills/cth-html-deck/SKILL.md` (1920×1080, scale ×0.96, nothing under 24px on the stage). Do not force the Q1 configurator onto that stage.

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

2. Map the table above onto custom properties. Use only the custom properties listed in this file. Do not add a CleantechHUB green, a Manual de Marca blue, or a new hue.
3. Wordmark: serif "AIC" plus tracked sans "Americas Innovation Council". Do not redraw or recolor it.
4. The live configurator keeps `data-i18n`, Spanish as the default, and does not store the choice. An AIC slide deck uses the `cth-html-deck` EN/ES contract (`cth-deck-lang`, room language from the ticket). Only the colour and type tokens change.
5. The live product is the 7-section configurator. A slide deck is a separate ticket and uses the `cth-html-deck` shell.
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
