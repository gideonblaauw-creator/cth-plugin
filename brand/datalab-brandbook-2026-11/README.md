# Datalab brand book (Nov 2026)

Master brand name (exact): **Datalab powered by CleantechHUB** (`Datalab` one word).

**Status:** Draft PR · **Awaiting Gideon's approval** · HITL before use, post, or deploy.

Built from `cursor/datalab-logo-2026-11` @ `197b5ad` (Option B primary). Sub-brand of CleantechHUB: five Manual de Marca colours, Titillium Web + Open Sans, flat fills.

## Contents

| Path | Description |
|------|-------------|
| `index.html` | Twelve-section HTML brand book (CLP26-style scroll layout) |
| `datalab-brandbook.pdf` | A4 landscape print export |
| `styles.css` | Brand tokens and layout |
| `assets/logos/` | Primary + sub-product logos (SVG, light/dark PNG) |
| `assets/icons/` | 12 line icons |
| `assets/palettes/` | JSON palette |
| `assets/social/` | 1080, 1200×627, 1080×1920 story |
| `assets/templates/` | Deck slide master, web hero, chart example |

### Sub-product logos (Option B family)

| Product | Mark source | Files |
|---------|-------------|--------|
| Data Flow | Option C flow (secondary device) | `data-flow.svg`, `-light.png`, `-dark.png` |
| Data Set | Option A grid (secondary device) | `data-set.svg`, `-light.png`, `-dark.png` |
| Data Dashboard | Option B layers + bar tiles | `data-dashboard.svg`, `-light.png`, `-dark.png` |

Regenerate PNGs: `cd scripts && npm install @resvg/resvg-js && node render-logos-png.mjs`

Regenerate PDF: `python3 export-deck-pdf.py --index index.html --pdf datalab-brandbook.pdf --mode scroll`

## PENDIENTE

- Official **CleantechHUB logo** asset (placeholders in endorsed lockups and social)
- **CMYK** values for the five colours (not in brand skill)
- **Adobe ASE** palette export
- Event **time**, **venue**, partner logos and permissions
- Third pre-event post date, final **social copy**
- Any metrics, partner names, or claims beyond approved intro lines
- **Story template PNG** (SVG provided; run resvg if PNG required)
- Deploy to `decks.cleantechhub.net` (out of scope for this ticket)
