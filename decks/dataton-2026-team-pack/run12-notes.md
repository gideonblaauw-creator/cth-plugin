# Run 12 notes

Head: `a8269f6f3f3aa40bba564ef6d0fe22f043e57353`.
Base: `59e987145b5ab3e09c2575d64296abdde59057d9`.

## Ticket
- `hands-tickets/dataton-teampack-run12-sheet-header.md` (sha `cd151258` — not in repo clone)

## Prompts-IA PDF header fix
- pages: **3** (expect 3)
- pdffonts Open Sans + emoji only: **True** (ok)
- pdf sha256: `0d6ffa5717b985ddbce07d754a6f64db443e47a8b2e8b63fd4c0e6b3d64aef51`
- cuestionario/dist pdf identical: **True**
- sheet docx unchanged (`b8649f50454b71eb64504d721b482b1d1f5099558a1652679cae9ce6159a74ed`): **True**
- Parte 2 on page 2: **True**

## Timestamp grep (must be empty)
- hits: **none**

## Zip vs run 11 (`c9563ff9`)
- zip sha256: `02148d153f243ade2d614d126e9358706624e829fa47883c55c79e27ddb7c610` (was `c9563ff9624dba740dd961a0ccf3a1b62b36d57556373a1bee23fdcfb3398989`)
- delta members: `['Prompts-IA-Dataton-24nov.pdf']`
- `Cuestionario-Dataton-24nov-equipos.docx`: `c0a9cb75`
- `Cuestionario-Dataton-24nov-equipos.pdf`: `8aa336f4`
- `Cuestionario-ejemplo-Air4U.docx`: `91d409c3`
- `Cuestionario-ejemplo-Air4U.pdf`: `7d31c6d2`
- `LEEME.md`: `aa69d4b0`
- `LEEME.pdf`: `5d6efd27`
- `Prompts-IA-Dataton-24nov.docx`: `b8649f50`
- `Prompts-IA-Dataton-24nov.pdf`: `0d6ffa57`
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

## Pinned
- prompts.txt: **True**
- Prompts-IA docx: **True**

## git diff --stat vs base
```
.../_png/run12/pdffonts-sheet.txt                  |   6 +
 .../_png/run12/sheet-p01-110dpi.png                | Bin 0 -> 137022 bytes
 .../_png/run12/sheet-p02-110dpi.png                | Bin 0 -> 249849 bytes
 .../_png/run12/sheet-p03-110dpi.png                | Bin 0 -> 71881 bytes
 .../_png/run12/timestamp-grep.txt                  |   1 +
 .../cuestionario/Prompts-IA-Dataton-24nov.pdf      | Bin 161794 -> 156487 bytes
 .../cuestionario/build-prompts-ia-dataton-sheet.py |   1 +
 .../dist/Prompts-IA-Dataton-24nov.pdf              | Bin 161794 -> 156487 bytes
 decks/dataton-2026-team-pack/run12-notes.md        |  53 +++++++
 .../scripts/rebuild_zip_run12.py                   |  32 +++++
 .../scripts/run12_self_check.py                    | 153 +++++++++++++++++++++
 .../team-pack-es-pdfs-v0.4.zip                     | Bin 2945384 -> 2940790 bytes
 12 files changed, 246 insertions(+)
```
