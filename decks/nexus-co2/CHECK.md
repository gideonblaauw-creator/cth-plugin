# CHECK — Nexus CO₂ deck rebuild (2026-11-04)

| Check | Result |
|-------|--------|
| `build.sh` emits self-contained `index.html` | PASS |
| CTH interactive shell (1920×1080 scale, index, dots, hash, chrome) | PASS |
| Manual de Marca stage tokens (Open Sans, deep/cyan/green) | PASS |
| Data matches `research/nexus-co2/co2.csv` (9 rows, 8 startups) | PASS |
| Filters, log-scale range, per-metric counters, cards, chart, table, coverage | PASS |
| Download PDF footer + fixed pill → `nexus-co2.pdf` (same folder) | PASS |
| `@media print` hides `.pdf-dl-btn`, `.pdf-dl-fixed`, `.pdf-dl-footer` | PASS |
| Co-located `nexus-co2.pdf` A4 landscape (`export-deck-pdf.py --mode scroll`) | PASS |
| No deploy to live slug | Pending Infra GO (this backfill) |
| Live `cth-clp26-rein` HTML fetched for pixel parity | FAIL — Google SSO wall; matched B4B shell per `cth-html-deck` skill instead |
