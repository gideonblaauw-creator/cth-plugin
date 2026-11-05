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
- [x] Datalab Option A datagrid + endorsement (`datalab-logo-endorsed-light.png` in logo pill)
- [x] EO green lockup (`assets/logos/lockup-horizontal.svg`) on top bar
- [x] Consortium row + OPEN SLOT corporate card
- [x] Page 2 band: En desarrollo / In development (Waste, Energy, Water)
- [x] No unsourced statistics; no em dashes in copy; no prices; no cannabis
- [x] No merge / deploy / send (PR only)

## Regenerate

```bash
cd decks/open-air-sandbox-onepager
python3 export-onepager-pdf.py --html open-air-sandbox-es.html --pdf open-air-sandbox-es.pdf --png-prefix es
python3 export-onepager-pdf.py --html open-air-sandbox-en.html --pdf open-air-sandbox-en.pdf --png-prefix en
```
