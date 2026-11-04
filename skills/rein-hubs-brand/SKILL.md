---
name: rein-hubs-brand
description: >
  REIN Hubs colors, typography, and HTML deck PDF controls for partner-facing
  scroll decks. Use when: REIN Hubs deck, REIN long-page HTML, rein-hubs visual,
  Download PDF on REIN deck. Do not use when: CleantechHUB-only artifacts
  (cleantechhub-brand), grant packs (cth-grant), or citing REIN dollar amounts.
license: MIT
metadata:
  version: "1.0.0"
  category: brand
---

# REIN Hubs brand (HTML decks)

Operational comms and HOLD rules: `skills/rein-hubs-comms/SKILL.md`. **Never cite REIN Hubs dollar amounts** in any deck or PDF.

Credit line (footer): **REIN Hubs · PVBLIC × CleantechHUB**.

## Color palette

| Role | Hex | Usage |
|---|---|---|
| REIN Green | `#335D4F` | Headings, nav, primary surfaces |
| REIN Orange | `#FF6633` | CTAs, accents, Download PDF pill |
| Text | `#222A27` | Body on light backgrounds |
| Gray | `#5F6663` | Secondary text |
| Line | `#C9D6D1` | Borders, dividers |
| Background | `#F1F5F3` | Page / card backgrounds |

Do not use CleantechHUB blues (`#2D6A4F` stage palette) as the primary REIN deck identity unless the ticket is an explicit co-brand.

## Typography

- **Headings:** Poppins 600–700.
- **Body:** Lora or Open Sans 15–16px; line-height ~1.6.
- Do not load Arial as a primary face.

## Download PDF (HARD — Gideon 4 Nov 2026)

REIN scroll decks follow the same contract as `docs/html-deck-protocol.md`:

- Co-located `<slug>.pdf` beside `index.html`.
- Footer `.pdf-dl-footer` and fixed `.pdf-dl-fixed` with class `pdf-dl-btn`.
- Orange pill styling (reference: `https://decks.cleantechhub.net/rein/externado-ncuk/`).

Template CSS defaults:

```css
:root {
  --green: #335d4f;
  --orange: #ff6633;
  --pdf-dl-bg: var(--orange);
  --pdf-dl-focus: var(--green);
}
```

Import or paste `decks/_templates/pdf-download.css`. Generate with `decks/_templates/export-deck-pdf.py`.

## Checklist

1. REIN hexes only (no off-brand primaries).
2. Poppins + Lora/Open Sans pairing.
3. Download PDF in footer and bottom-right; hidden in `@media print`.
4. PDF A4 landscape with reveals and counters finalized.
5. No REIN dollar amounts; no confidential partner content in git copies.
