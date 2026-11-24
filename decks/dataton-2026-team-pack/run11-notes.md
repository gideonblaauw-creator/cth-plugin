# Run 11 notes

Head: `e95dd3ae55d723de745f6c305fb13781f4a87e03`.
Base: `e95dd3ae55d723de745f6c305fb13781f4a87e03`.

## Ticket
- `hands-tickets/dataton-teampack-run11-zip-sheet-fix.md` (sha `94eca467` — not in repo clone)

## Fix 1 — zip Guía docx
- zip Guía docx sha256: `04de6140d4b7ed51cffeeea18ac49948e3efdf5fb98fdb010848eebab3c51b01` (expect `04de6140d4b7ed51cffeeea18ac49948e3efdf5fb98fdb010848eebab3c51b01`): **True**
- zip sha256: `c9563ff9624dba740dd961a0ccf3a1b62b36d57556373a1bee23fdcfb3398989` (run 10 was `c4f70884359ea16c1e655f6cd1d11d051a1f6fc16ec09cbc47bb3029a0b99102`)

## Fix 2 — Prompts-IA sheet footer
- sheet pdf pages: **3** (expect ≤3)
- Parte 2 not on page 1 (footer clear): **True**
- Parte 2 starts page 2: **True**
- sheet docx dist=cuestionario: **True**
- prompts.txt pinned: **True**
- sheet pdf sha256: `aa85d9f58c7242feb019a6ab3600e058f0c80833181ed563db5035297e9f2add`
- sheet docx sha256: `b8649f50454b71eb64504d721b482b1d1f5099558a1652679cae9ce6159a74ed`

- equipos page size: `612 x 792 pts (letter)` (expect 612 x 792 pts)
- ejemplo page size: `612 x 792 pts (letter)` (expect 612 x 792 pts)

## Fix 3 — questionnaire INSTRUCCIÓN boxes (single page each)
- equipos docx text = `e95dd3ae`: **True**
- ejemplo docx text = `e95dd3ae`: **True**
- equipos pages: **9**
  - box p0: page **2**, single-page **True**
  - box p1: page **4**, single-page **True**
  - box p1b: page **4**, single-page **True**
  - box p2: page **6**, single-page **True**
  - box p3: page **8**, single-page **True**
  - box p4: page **9**, single-page **True**
- equipos all 6 boxes single-page: **True**
- ejemplo pages: **7**
  - box p0: page **2**, single-page **True**
  - box p1: page **4**, single-page **True**
  - box p1b: page **4**, single-page **True**
  - box p2: page **5**, single-page **True**
  - box p3: page **7**, single-page **True**
  - box p4: page **7**, single-page **True**
- ejemplo all 6 boxes single-page: **True**

## Zip listing (per-entry sha256 first 8)
- `Cuestionario-Dataton-24nov-equipos.docx`: `c0a9cb75`
- `Cuestionario-Dataton-24nov-equipos.pdf`: `8aa336f4`
- `Cuestionario-ejemplo-Air4U.docx`: `91d409c3`
- `Cuestionario-ejemplo-Air4U.pdf`: `7d31c6d2`
- `LEEME.md`: `aa69d4b0`
- `LEEME.pdf`: `5d6efd27`
- `Prompts-IA-Dataton-24nov.docx`: `b8649f50`
- `Prompts-IA-Dataton-24nov.pdf`: `aa85d9f5`
- `agenda-equipos.pdf`: `911f8d5e`
- `guia-tecnica-mentores/Guia-tecnica-mentores.docx`: `04de6140`
- `guia-tecnica-mentores/Guia-tecnica-mentores.pdf`: `9bf595a4`
- `guia-tecnica-mentores/ejemplo-air4u.pdf`: `7c95d7a0`
- `guia-tecnica-mentores/fuentes-datos-abiertos.pdf`: `16bf29e9`
- `guia-tecnica-mentores/hoja-1-mapa-de-calor.pdf`: `a339dc2d`
- `guia-tecnica-mentores/hoja-2-flujo-de-datos.pdf`: `a0dc6e6a`
- `guia-tecnica-mentores/hoja-3-dato-a-valor.pdf`: `e68cc893`
- `guia-tecnica-mentores/hoja-4-plantilla-tablero.pdf`: `c0f142f5`
- `guia-tecnica-mentores/hoja-4b-ejemplo-air4u.pdf`: `c1f78747`
- `guia-tecnica-mentores/hoja-5-plantilla-pitch.pdf`: `5c4c00a4`
- `guia-tecnica-mentores/plantilla-bmc.pdf`: `86b79a64`
- `guia-tecnica-mentores/prompts-ia-v2.pdf`: `3b76e8cc`
- `prompts.txt`: `4cd248ad`

## git diff --stat vs base
```
(empty)
```
