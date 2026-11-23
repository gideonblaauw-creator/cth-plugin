# QA check — datathon-2026-teams (QA round 5 fix)

Base: `652c4aaf0faab46a6b89bdba84e8e1fa97e35269`

## F1 — Download PDF

| Check | Result |
|-------|--------|
| Footer `.pdf-dl-footer` + `.pdf-dl-btn` ES/EN | Present on every slide footer via `fp-render.mjs` `foot()` |
| Fixed `.pdf-dl-btn.pdf-dl-fixed` ES/EN | In `index.html` / `dist/index.html` (`right: 168px` to clear slide counter) |
| ES href | `datathon-2026-teams.pdf` (same folder, `download` attribute) |
| EN href | `datathon-2026-teams-en.pdf` |
| `grep -c pdf-dl-btn dist/index.html` | 42 (≥ 4) |
| `pdftotext … \| grep -ciE 'descargar pdf\|download pdf'` | 0 (ES and EN) |
| Print / export hide | `@media print` in `assets/pdf-download.css`; `html.export …` same file |
| Styles | `assets/pdf-download.css` linked in deck shell |

## F2 / F3 / F4 / F5 / F6

- **F2:** L1 tables 18px @1920; ICA legend HTML (Res. 2254/2017) under map; map card fills column; new L1-only map PNG from skeleton capture (`scripts/capture-l1-map.mjs`).
- **F3 Option A:** Capture script sets `state.layers` L1-only, `placed: false` on candidate pins (no Ramo/Bolívar, no A4U triangles).
- **F4:** L2/L3 table 20px; cards 30/24px titles/body.
- **F5:** `deck.yaml` slide 9 `type: map`, 10–11 `type: data-table`; `data-cth-type` `map` / `data-table` in render.
- **F6:** L3 site `Ramo (ejemplo ilustrativo)` / `Ramo (illustrative example)`; L1 `sin dato` cells unchanged; Confidencial footer untouched.