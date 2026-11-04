---
name: cth-html-deck-visual
description: >
  Visual rules for scroll-style and long-page HTML decks (REIN partner layouts,
  metrics, reveal sections) plus Download PDF HARD standard. Use when: scroll
  deck, long-page deck, REIN visual deck, externado-style HTML, backfill PDF
  buttons. Do not use when: 1920×1080 stage shell (use cth-html-deck when on
  main), Nexus one-pagers, grant packs, or diagram-design SVG deliverables.
license: MIT
metadata:
  version: "1.1.0"
  category: programs
---

# CTH HTML deck (visual / scroll)

**Superseded for the 1920×1080 stage** by `skills/cth-html-deck/SKILL.md` (Presentations desk, 19 Oct 2026). Keep using this skill for **long-page / scroll** decks (section `.slide`, `.reveal`, fixed nav) such as the live reference `https://decks.cleantechhub.net/rein/externado-ncuk/`.

Protocol index: `docs/html-deck-protocol.md`. Harness owner rule: `skills/harness/references/hands-ticket-hard.md` § HTML decks.

## Download PDF (HARD — Gideon 4 Nov 2026)

Every HTML deck this skill covers must ship:

1. **Print-ready PDF** in the same folder as `index.html` (A4 landscape, backgrounds on, all `.reveal` visible, `[data-count]` at final values).
2. **Two Download PDF controls** — same `href` and `download` attribute:
   - Footer: `.pdf-dl-footer` → `.pdf-dl-btn`
   - Fixed bottom-right: `.pdf-dl-btn.pdf-dl-fixed`
3. **Print CSS** hides both controls: `@media print { .pdf-dl-btn, .pdf-dl-fixed, .pdf-dl-footer { display: none !important; } }`

Copy from `decks/_templates/pdf-download.css` and `decks/_templates/pdf-download.html`. Generate PDF with `decks/_templates/export-deck-pdf.py` (copy into the deck folder). Do not embed confidential REIN content in the public repo.

## Visual baseline (scroll REIN)

- Typography: body Lora or Open Sans; headings Poppins (see `skills/rein-hubs-brand/SKILL.md`).
- Sections: `.reveal` with IntersectionObserver → `.visible` on screen; PDF export must force `.visible` on every reveal.
- Metrics: `[data-count]` animate on screen; PDF export must set text to the final `data-count` value.
- Photo / gradient covers and orange accent CTAs match REIN tokens, not CleantechHUB Inter-green defaults.

## Acceptance

Verifier rows (add to `CHECK.md`):

| Check | Pass |
|---|---|
| PDF co-located | `basename.pdf` beside `index.html`; both links use that basename. |
| Print hide | Buttons absent in print preview / exported PDF. |
| PDF fidelity | A4 landscape; at least one reveal and one counter match final state. |
| HITL | Footer still shows approval line for working copies; no deploy without Gideon. |
