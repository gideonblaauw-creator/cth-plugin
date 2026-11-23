# Acceptance checks (Hands run 23 Nov 2026)

Environment: Cloud Agent VM. `pdfinfo` / `pdffonts` (poppler) not installed; dimensions and fonts verified with PyMuPDF.

## Page size (A4 landscape)

All sample PDFs under `review/batch/` and `review/plantilla.pdf`:

| File | Size (pt) | Pages |
| --- | --- | --- |
| Each single sample | 842.88 × 595.92 | 1 |
| `all.pdf` | 842.88 × 595.92 | 5 |

Expected A4 landscape: 841.89 × 595.28 pt — match within rounding.

## Fonts

PyMuPDF `get_page_fonts` on `maria-alejandra-rodriguez-de-santamarias-participante.pdf` (after `base href` fix in `render.py`):

- `TitilliumWeb-Bold` (subset, embedded)
- `OpenSans-SemiBold` (subset, embedded)
- Minor Type3 elements from SVG datagrid (no extra text families)

No Tinos or system fallbacks after path fix.

## Safe margin

Layout uses 12 mm padding on `.certificate` (`certificate.css`). Decorative top rule and footer tagline sit inside the padded area; type and logos respect the 12 mm inset.

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