# Run 13 notes

Head: `f7878dca38a578a4218302a955ee56818c2c7b97`.
Base: `263d7e6fc609981b25735bb78f31c2a3b41ae1ad`.

## Ticket
- hands-tickets/dataton-teampack-run13-sheet-heading-prefix.md (sha `eb3b999a` — not in repo clone)

## Heading prefix fix
- grep 'Parte: ' in docx: **0** (expect 0)
- grep 'Parte: ' in pdf text: **0** (expect 0)
- printed heading: **True** — `Parte 0. Su proyecto en una página`
- printed heading: **True** — `Parte 1. ¿Qué información tienen y dónde está?`
- printed heading: **True** — `Parte 1-B (opcional)`
- printed heading: **True** — `Parte 2. ¿Cómo nace un dato y qué tan confiable es?`
- printed heading: **True** — `Parte 3. ¿Qué decisión ayudan a tomar?`
- printed heading: **True** — `Parte 4. Su pitch de 5 minutos`

## Layout (unchanged from run 12)
- pages: **3** (expect 3)
- pdffonts Open Sans + emoji: **True** (ok)
- Parte 2 starts on page 2: **True**
- sheet pdf sha256: `db203d6e4e018e2f99c00aa0351301676f4e25975044970ea4de4fac94fc20aa`
- sheet docx sha256: `292db1ddeaabdbfaac39bed6024a4b3d143fdf91c939620f05b20ca512235e97`
- cuestionario/dist pdf identical: **True**
- cuestionario/dist docx identical: **True**
- prompts.txt pinned: **True**

## Zip vs run 12 (`02148d15`)
- zip sha256: `31b7c5fd82f606f490fabc135d6ecb50379085c579bf1a3d63827ee213902cbd` (was `02148d153f243ade2d614d126e9358706624e829fa47883c55c79e27ddb7c610`)
- delta members: `['Prompts-IA-Dataton-24nov.docx', 'Prompts-IA-Dataton-24nov.pdf']`
- `Cuestionario-Dataton-24nov-equipos.docx`: `c0a9cb75`
- `Cuestionario-Dataton-24nov-equipos.pdf`: `8aa336f4`
- `Cuestionario-ejemplo-Air4U.docx`: `91d409c3`
- `Cuestionario-ejemplo-Air4U.pdf`: `7d31c6d2`
- `LEEME.md`: `aa69d4b0`
- `LEEME.pdf`: `5d6efd27`
- `Prompts-IA-Dataton-24nov.docx`: `292db1dd`
- `Prompts-IA-Dataton-24nov.pdf`: `db203d6e`
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
.../_png/run13/pdffonts-sheet.txt                  |   6 +
 .../_png/run13/sheet-p01-110dpi.png                | Bin 0 -> 136580 bytes
 .../_png/run13/sheet-p02-110dpi.png                | Bin 0 -> 248350 bytes
 .../_png/run13/sheet-p03-110dpi.png                | Bin 0 -> 71306 bytes
 .../cuestionario/Prompts-IA-Dataton-24nov.docx     | Bin 100646 -> 100643 bytes
 .../cuestionario/Prompts-IA-Dataton-24nov.pdf      | Bin 156487 -> 156384 bytes
 .../cuestionario/build-prompts-ia-dataton-sheet.py |   4 +-
 .../dist/Prompts-IA-Dataton-24nov.docx             | Bin 100646 -> 100643 bytes
 .../dist/Prompts-IA-Dataton-24nov.pdf              | Bin 156487 -> 156384 bytes
 decks/dataton-2026-team-pack/run13-notes.md        |  58 +++++++
 .../scripts/rebuild_zip_run13.py                   |  35 +++++
 .../scripts/run13_self_check.py                    | 167 +++++++++++++++++++++
 .../team-pack-es-pdfs-v0.4.zip                     | Bin 2940790 -> 2940692 bytes
 13 files changed, 268 insertions(+), 2 deletions(-)
```
