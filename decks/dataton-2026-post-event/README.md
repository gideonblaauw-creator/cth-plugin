# Datatón 2026 — post-event (wave 1)

Entregables internos tras el Datatón del 24 nov 2026 (Universidad Externado). No enviar ni publicar sin aprobación.

| Ruta | Contenido |
|------|-----------|
| `source/` | `source-pack.md`, `recipients.csv` (sin correos ni teléfonos) |
| `protocol/` | Protocolo interno CTH (docx, pdf, html, `build_protocol.py`) |
| `monday/` | `board-spec.md`, `board-import.csv` (no crear tablero en esta ola) |
| `thank-yous/` | `thank-yous.md` |
| `render/` | PNG por página del PDF del protocolo |

Regenerar protocolo y CSV:

```bash
python3 protocol/build_protocol.py
```