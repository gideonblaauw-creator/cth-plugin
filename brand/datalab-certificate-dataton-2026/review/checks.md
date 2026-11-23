# Acceptance checks (Hands run 23 Nov 2026, fix round 2)

Environment: Cloud Agent VM. `pdfinfo` / `pdffonts` (poppler) not installed; dimensions and footer clearances verified with PyMuPDF (`review/measure_footer.py`).

## Page size (A4 landscape)

All sample PDFs under `review/batch/` and `review/plantilla.pdf`:

| File | Size (pt) | Pages |
| --- | --- | --- |
| Each single sample | 841.92 × 594.96 | 1 |
| `all.pdf` | 841.92 × 594.96 | 5 |

## Footer clearance (40-char sample)

`python3 review/measure_footer.py` on `maria-alejandra-rodriguez-de-santamarias-participante.pdf`:

- Tagline bottom from trim: **12.05 mm** (≥ 12 mm)
- Partner logo row bottom from trim: **19.39 mm**
- Logo row above tagline: **7.34 mm** (no overlap)

## Fonts

PyMuPDF `get_page_fonts` on `maria-alejandra-rodriguez-de-santamarias-participante.pdf` (after `base href` fix in `render.py`):

- `TitilliumWeb-Bold` (subset, embedded)
- `OpenSans-SemiBold` (subset, embedded)
- Minor Type3 elements from SVG datagrid (no extra text families)

No Tinos or system fallbacks after path fix.

## Safe margin

Layout uses 12 mm padding on `.certificate` (`certificate.css`). Footer uses flex band `.certificate-bottom` (partner row, then tagline); tagline is no longer absolutely positioned at 6 mm.

## Logos

- Datalab Option A datagrid via `logos/datalab-logo-endorsed.svg` (object embed); `cleantechhub-official.png` co-located for SVG `href`.
- CTH lockup in partner row: aspect preserved (`max-height: 11mm`).
- Externado PNG: not stretched (`object-fit: contain`).
- CEE: dashed labelled slot only (`logos/GAPS.md`).

## Copy and roles

- Spanish body lines per ticket for Participante (with/without equipo), Mentor, Jurado.
- 40-character QA name: `María Alejandra Rodríguez de Santamarías` (len=40) fits in name block at 18 pt.
- Signature rules: equal-width grid columns, shared baseline.
- No people photos, no "gratis", no invented credits.

## Contact sheet

`review/contact-sheet.png` — thumbnails (Participante, 40-char, Mentor, Jurado), signature crop, logo row crop.

## Batch

`python3 render.py --csv examples/sample.csv --outdir review/batch/` — five individual PDFs + `all.pdf`.

## Out of scope (confirmed)

No merge, deploy, print, or send. No edits outside `brand/datalab-certificate-dataton-2026/`. PR #134 untouched.