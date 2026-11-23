# Self-verify — Datatón panel guide

| Criterio | Resultado |
|----------|-----------|
| Todo en español | Sí |
| Cada nombre/rol con «por confirmar» | Sí (guía, PDF, title card) |
| PDF exactamente 1 página | Sí (`pypdf`: 1 página) |
| Sin archivos existentes modificados | Solo `decks/datathon-2026-panel/**` nuevo |
| PNG title card 1920×1080 | Sí — `proof/title-card-1920x1080.png` (1920×1080) |

## Comandos de prueba

```bash
pdfinfo decks/datathon-2026-panel/guia-moderador.pdf | grep Pages
file decks/datathon-2026-panel/proof/title-card-1920x1080.png
git diff --name-only origin/main
```