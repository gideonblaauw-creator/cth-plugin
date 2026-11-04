# Datalab brand book (Nov 2026)

Master brand name (exact): **Datalab powered by CleantechHUB** (`Datalab` one word).

**Primary mark:** Option A (datagrid) · **Secondary mark:** Option B (layers), documented in `index.html` §02 variations.

**Status:** Draft PR · **Awaiting Gideon's approval** · HITL before use, post, or deploy.

Framed after **MANUAL DE MARCA ACTUAL** (CleantechHUB): apaisado 1920×1080 on screen; **PDF print base 21.333 px (~16 pt CSS; body copy targets ≥14 pt in print)**, captions ≥ ~11 pt, A4 landscape 297×210 mm, secciones 01–05 en español, paleta Manual de Marca (full **cth-clp26-story** `site/styles.css` vendored in `assets/clp26-story/site-styles.css`, 23 037 bytes), Titillium Web + Open Sans. HTML components use **`clp26-manual-tokens.css`** (`.stat`, `.tbl`, `.story`).

**Official CleantechHUB PNG (no redraw):** `assets/logos/cleantechhub-official.png` (byte-identical to `decks/nexus-co2/logos/cleantechhub.png`).

## Contents

| Path | Description |
|------|-------------|
| `index.html` | Manual de marca (deck · one slide per section) |
| `manual-deck.css` | Slide framing + print (`print-all`) |
| `datalab-brandbook.pdf` | A4 landscape export (one slide per page) |
| `assets/logos/` | Option A master, Option B secondary, sub-product logos |
| `assets/social/` | Square, landscape, story (SVG + PNG) |

Regenerate logo PNGs: `cd scripts && npm install @resvg/resvg-js && node render-logos-png.mjs && node render-social-png.mjs`

Regenerate PDF: `python3 export-deck-pdf.py --index index.html --pdf datalab-brandbook.pdf --mode slides`

## PENDIENTE

- **CMYK** values · **Adobe ASE** palette file
- **Merchandising** applications
- Event **time**, **venue**, **partner logos**
- Deploy to `decks.cleantechhub.net` (out of scope for this PR)
