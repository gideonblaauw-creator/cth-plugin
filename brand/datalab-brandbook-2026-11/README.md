# Datalab brand book (Nov 2026)

Master brand name (exact): **Datalab powered by CleantechHUB** (`Datalab` one word).

**Status:** Draft PR · **Awaiting Gideon's approval** · HITL before use, post, or deploy.

Framed after **MANUAL DE MARCA ACTUAL** (CleantechHUB): apaisado 1920×1080 slides, secciones en español, paleta Manual de Marca (cinco colores), Titillium Web + Open Sans. HTML components reuse **`decks/_templates/clp26-rein-shell/styles.css`** (`.stat`, `.tbl`, `.story`) with tokens in `clp26-manual-tokens.css`.

## Contents

| Path | Description |
|------|-------------|
| `index.html` | Manual de marca (deck · one slide per section) |
| `manual-deck.css` | Slide framing + print (`print-all`) |
| `datalab-brandbook.pdf` | Landscape export (1920×1080 per page) |
| `assets/logos/` | Primary + sub-product logos |
| `assets/social/` | Square, landscape, story (SVG + PNG) |

Regenerate logo PNGs: `cd scripts && npm install @resvg/resvg-js && node render-logos-png.mjs && node render-social-png.mjs`

Regenerate PDF: `python3 export-deck-pdf.py --index index.html --pdf datalab-brandbook.pdf --mode slides`

## PENDIENTE

- Official **CleantechHUB logo** vector asset (labelled placeholders only)
- **CMYK** values · **Adobe ASE**
- Event time, venue, partner logos
- Deploy to `decks.cleantechhub.net` (out of scope)
