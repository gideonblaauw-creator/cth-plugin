# Earth Observatory / Observatorio de la Tierra — logo concepts

**Status:** Draft · **INTERNAL REVIEW ONLY** · Awaiting Gideon's approval. No posting, sharing, or deploy.

**Selected concept (Gideon 4 Nov 2026):** `03-orbita-datos` · final lockups in `final/` (Externado first, then CleantechHUB).

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

## Final lockups (`final/`)

| Path | Use |
|------|-----|
| `final/preview.png` | Compare key final lockups (green + blue) |
| `final/<es\|en>/<green\|blue>/` | Locale + colour variant |
| `final/.../lockup-square.svg` | Square mark + locale title |
| `final/.../lockup-horizontal.svg` | Horizontal mark + locale title |
| `final/.../lockup-cobrand.svg` | **Universidad Externado** (`PENDIENTE logo`) then official CTH PNG |
| `final/.../lockup-mono.svg` | Single-colour horizontal |
| `*-transparent.png` / `*-white.png` | PNG exports per lockup |

**Palettes:** `green` (CTH primary `#2D6A4F`) and `blue` (compare `#0C498A`).

## Kit root

| Path | Use |
|------|-----|
| `contact-sheet.png` | Compare all concepts (horizontal lockups) |
| `contact-sheet.svg` | Editable contact sheet source |
| `assets/cleantechhub.png` | Official CTH logo (from `decks/nexus-co2/logos/`) |
| `scripts/generate.mjs` | Regenerate concept SVGs + PNGs |
| `scripts/generate-final.mjs` | Regenerate `final/` only (concept 03) |

## Brand tokens

CleantechHUB Manual de Marca (via `cleantechhub-brand` skill): Primary `#2D6A4F`, Dark `#1B4332`, Accent `#95D5B2`, Light `#D8F3DC`, White `#FFFFFF`, Text `#333333`. Typography: Titillium Web Bold (titles), Open Sans (supporting type); PNG renders use OFL fonts in `scripts/fonts/`.

Family consistency reference only: `brand/datalab-logo-2026-11/` (Option A grid archived there — not copied).

## Regenerate

```bash
cd earth-observatory-logos/scripts
npm install @resvg/resvg-js
node generate.mjs
node generate-final.mjs
```
