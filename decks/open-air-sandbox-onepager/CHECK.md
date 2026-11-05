# Open Air Sandbox one-pager · verifier checklist

**Ticket:** `tickets/ticket-open-air-sandbox-onepager.md` (Hands unpack)  
**Amendment:** EN + ES, same layout, separate HTML/PDF each.

## Artifacts

| Lang | HTML | PDF | Page PNGs |
|------|------|-----|-----------|
| ES | `open-air-sandbox-es.html` | `open-air-sandbox-es.pdf` | `open-air-sandbox-es-page-1.png`, `open-air-sandbox-es-page-2.png` |
| EN | `open-air-sandbox-en.html` | `open-air-sandbox-en.pdf` | `open-air-sandbox-en-page-1.png`, `open-air-sandbox-en-page-2.png` |

## Acceptance

- [x] PDF page count: 2 (ES and EN), verified via `pypdf` after `export-onepager-pdf.py`
- [x] Download PDF: footer `.pdf-dl-footer` + fixed `.pdf-dl-fixed`; `@media print` hides controls (`pdf-download.css`)
- [x] Datalab Option A datagrid SVG ≥48px + live `powered by CleantechHUB` text ≥11px
- [x] Top bar: Datalab Option A + live powered-by (left); CTH logo (right); **no EO**
- [x] Page 1: intro + steward + Air4U + consortium only (scaled); page 2: single 2×2 grid to dev band
- [x] Air4U full-color logo; blank-band scan ≤40px on pdftoppm PNGs
- [x] Hero/showcase `object-fit: cover`; page 2 side-by-side screenshots
- [x] Render caption (ES/EN); footer text link + single fixed Download PDF button
- [x] Hero full-width rendering + max 3 legible showcase shots (page 1)
- [x] Page 2 uncropped `object-fit: contain` screenshots; flex fill (no white gap)
- [x] Consortium partner logos + stronger open-slot card (+ icon, dashed border)
- [x] Footer Download PDF stacked (no overlap with brand line)
- [x] Consortium row + OPEN SLOT corporate card
- [x] Page 2 band: En desarrollo / In development (Waste, Energy, Water)
- [x] No unsourced statistics; no em dashes in copy; no prices; no cannabis
- [x] No merge / deploy / send (PR only)

## Regenerate

```bash
cd decks/open-air-sandbox-onepager
python3 export-onepager-pdf.py --html open-air-sandbox-es.html --pdf open-air-sandbox-es.pdf --lang es
python3 export-onepager-pdf.py --html open-air-sandbox-en.html --pdf open-air-sandbox-en.pdf --lang en
```

Page PNGs are rasterized from the PDF via **pdftoppm** (150 DPI), not HTML screenshots.
