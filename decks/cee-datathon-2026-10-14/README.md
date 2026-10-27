# CEE Externado × CleantechHUB · 14 oct 2026

Deck en español (13 diapositivas, 1920×1080) para la reunión con el CEE y la Coordinación de Innovación
de la Universidad Externado. Mismo shell que `decks/apc-2026-10-07`.

- Fuente de diapositivas: `tools/gen.py` → `slides/*.html` → `build.sh` → `index.html` (autocontenido salvo `img/`).
- Vista de revisión con etiquetas PENDIENTE: `index.html?review`. Imprimir todo: `?print`.
- Render + QA + PDF: `NODE_PATH=<node_modules con playwright-core> node tools/render.js`
  (PNG por diapositiva en `png/`, versión `-review`, chequeo de desborde y PDF con `printBackground` + `print-color-adjust: exact`).
- `PENDIENTES.md` y `SOURCES.md` documentan lo que falta confirmar y de dónde sale cada dato.
