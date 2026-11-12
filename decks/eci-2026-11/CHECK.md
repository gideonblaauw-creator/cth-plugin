# Verificación · ECI HELIX-A 2026-11

| Comprobación | Estado |
|--------------|--------|
| `jq empty` en manifiestos del repo raíz (si aplica a cambios) | Pendiente en CI del PR |
| Footer + fijo `Descargar PDF` → `eci-2026-11.pdf` | Verificar tras generar PDF |
| `@media print` oculta botones PDF | Heredado de `pdf-download.css` |
| PDF A4 horizontal · `export-deck-pdf.py --mode scroll` | Ver comando en `verified` del handoff |
