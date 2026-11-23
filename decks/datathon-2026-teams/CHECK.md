# CHECK — datathon-maps-2 (fix round, base `05d716e5`)

Base: `05d716e5d4c4042debc5e50b5dc7da87dff21bf1` · Scope: `decks/datathon-2026-teams/` only.

## G1–G6 fixes applied

- **G1:** Restored `class="cth-source fp-source"` (removed `\\u00a0`). Data-table lint via visually hidden `p.cth-source` (aria-hidden) with plain YAML `source` text only on L2/L3.
- **G2:** Footer PDF button inline (`fp-foot__row` flex); footer button 17px @1920; `body.pdf-dl-on-dark` inverts fixed pill on photo/navy slides.
- **G3:** Single full-width L1 station table; grid `39% / 61%`; type ≥18px @1920 (≥12px @1280); table right edge ≤1210 @1280 (no clip).
- **G4:** Map re-capture 1200×720, zoom 12+, Leaflet controls hidden; map ≥330px tall @1280; HTML ICA + map-key rows; OSM credit in slide 9 source (ES/EN).
- **G5:** L2/L3 table 22px rows/padding; source `margin-top: auto`; screen gap source→footer ~19px @1280 (≤60).
- **G6:** EN kickers `Open-air sandbox · L1/L2/L3` in `deck-en.yaml`; L2/L3 EN links keep workshop credit; `region: colombia` (schema has no `bogota`).

## Acceptance outputs

### 1. Scope and PDFs

| Artifact | sha256 | Pages |
|----------|--------|------:|
| `datathon-2026-teams.pdf` | `15694323a934185fb327dfe0e80c636496202f258e91094cd7163af1c9926735` | 21 |
| `datathon-2026-teams-en.pdf` | `3feb45347817ebdb242e4b78604c6756ec823535ad4b05d364ff1120033b906f` | 21 |

### 2. F1 greps

- `pdftotext … \| grep -ciE 'descargar pdf\|download pdf'` → **0** (ES and EN)
- `grep -c pdf-dl-btn dist/index.html` → **42**

### 3. Screen (1280×720, http served dist)

| Check | Result |
|-------|--------|
| Slide 10 ES footer + fixed `href`/`download` | `datathon-2026-teams.pdf` ✓ |
| Print: `.pdf-dl-btn`, `.pdf-dl-fixed`, `.pdf-dl-footer` | `display: none` ✓ |
| Footer text top @1280 (slides 3,10,21 ES) | **683.5px** (target 685±11) |
| Fixed pill on slides 1, 7, 21 (dark) | inverted **#fff / #0C498A** — contrast **≥8.5:1** vs `#0C498A` |

### 4. Slides 9–11 (post-fix spot checks)

| Slide | min rendered px | map h @1280 | table right @1280 | source→foot gap |
|-------|-----------------|------------|-------------------|------------------|
| 9 ES | 11.33 | 330 | 1209 (unclipped) | 19.5 |
| 10 ES | 11.33 | — | 1213 | 19.0 |
| 11 ES | 11.33 | — | 1213 | 19.0 |

Title left: **64px**. EN kickers: **Open-air sandbox · L1/L2/L3**.

### 5. PDF regression vs `652c4aaf` committed PDFs (`pdftoppm -scale-to-x 1280 -scale-to-y 720`)

Pixels with max channel diff >40 (% of page). Cause when >0.10%: **footer row + inline PDF control** (bbox y≈684–703, x 64–568).

| Page | ES % | EN % | Notes |
|------|-----:|-----:|-------|
| 01 | 0.0000 | 0.0000 | |
| 02 | 0.3126 | 0.3060 | footer band |
| 03 | 0.3130 | 0.3099 | footer band |
| 04 | 0.3130 | 0.3099 | footer band |
| 05 | 0.3130 | 0.3099 | footer band |
| 06 | 0.3073 | 0.2982 | footer band |
| 07 | 0.2812 | 0.2744 | footer band (+ source #B2EEFA restored) |
| 08 | 0.2937 | 0.2870 | footer band (+ source #B2EEFA restored) |
| 12–15, 17–18, 20 | ~0.3130 | ~0.3099 | footer band |
| 16 ES | 1.7381 (dy_best **1.4339**) | 1.6727 (dy_best **1.2372**) | card block + footer |
| 19 ES | 1.8202 (dy_best **1.5851**) | 0.6101 | card block + footer |
| 21 | 0.3078 | 0.3016 | footer band |

### 6. Artifacts

42× `artifacts/slide-NN-1280-{es,en}.png` + contact sheets updated.

### Slide 9–11 PNG paths

- `decks/datathon-2026-teams/artifacts/slide-09-1280-es.png`
- `decks/datathon-2026-teams/artifacts/slide-09-1280-en.png`
- `decks/datathon-2026-teams/artifacts/slide-10-1280-es.png`
- `decks/datathon-2026-teams/artifacts/slide-10-1280-en.png`
- `decks/datathon-2026-teams/artifacts/slide-11-1280-es.png`
- `decks/datathon-2026-teams/artifacts/slide-11-1280-en.png`

Full automation log: `/opt/cursor/artifacts/datathon-maps-2-acceptance.log`