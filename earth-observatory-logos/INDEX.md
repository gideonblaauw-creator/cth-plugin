# Earth Observatory / Observatorio de la Tierra — logo concepts

**Status:** Draft · **INTERNAL REVIEW ONLY** · Awaiting Gideon's approval. No posting, sharing, or deploy.

**Partnership:** CleantechHUB × Universidad Externado (Externado shown as text placeholder only; no unofficial Externado logo).

**Tagline (context):** *La colaboración es la lente. El conocimiento orienta las decisiones. El dato es la infraestructura.*

## Concepts (5)

| ID | ES | EN | Rationale |
|----|----|----|-----------|
| `01-lente-global` | Lente Global | Global Lens | Collaboration as a lens focusing the planet for shared decisions. |
| `02-grilla-territorio` | Grilla Territorio | Terrain Grid | Data as infrastructure — a grid that lifts territory into view. |
| `03-orbita-datos` | Órbita de Datos | Data Orbit | International cooperation as orbits linking data nodes around Earth. |
| `04-brujula-norte` | Brújula Norte | North Compass | Knowledge orients — a compass aligning cooperation, startups, and land. |
| `05-mapas-capas` | Mapas en Capas | Layered Maps | Stacked map layers: data infrastructure under collaboration and place. |

## Per-concept files

Each folder under `concepts/<id>/` contains:

| File | Description |
|------|-------------|
| `RATIONALE.md` | One-line concept rationale |
| `lockup-square.svg` | Square lockup (ES + EN names) |
| `lockup-horizontal.svg` | Horizontal lockup |
| `lockup-endorsed.svg` | Horizontal + *powered by CleantechHUB* + CTH logo |
| `lockup-cobrand.svg` | Co-brand with **Universidad Externado** placeholder |
| `lockup-mono.svg` | Single-colour horizontal lockup |
| `*-transparent.png` | PNG on transparent background |
| `*-white.png` | PNG on white background |

## Kit root

| Path | Use |
|------|-----|
| `contact-sheet.png` | Compare all concepts (horizontal lockups) |
| `contact-sheet.svg` | Editable contact sheet source |
| `assets/cleantechhub.png` | Official CTH logo (from `decks/nexus-co2/logos/`) |
| `scripts/generate.mjs` | Regenerate SVGs + PNGs |

## Brand tokens

CleantechHUB Manual de Marca (via `cleantechhub-brand` skill): Primary `#2D6A4F`, Dark `#1B4332`, Accent `#95D5B2`, Light `#D8F3DC`, White `#FFFFFF`, Text `#333333`. Typography: Titillium Web Bold (titles), Open Sans (supporting type); PNG renders use OFL fonts in `scripts/fonts/`.

Family consistency reference only: `brand/datalab-logo-2026-11/` (Option A grid archived there — not copied).

## Regenerate

```bash
cd earth-observatory-logos/scripts
npm install @resvg/resvg-js
node generate.mjs
```
