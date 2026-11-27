# Run 9 notes

Working head: `72ea013b7b547b9650b6faaf03250cbf1c70a6b6`.
Base ref: `72ea013b7b547b9650b6faaf03250cbf1c70a6b6`.

## prompts.txt SHA checks
- File sha256: `ff7ab27c22b3f03e2a2a0b55d477ccae2ccf637a7b79f946019add64109b5df8` (expect `ff7ab27c22b3f03e2a2a0b55d477ccae2ccf637a7b79f946019add64109b5df8`): **True**
- Nine instruction lines sha: `1b86dee4bf59f9bb155e0e9b9fcd99f4817562eb52490666a950d09b556185c9` (expect `1b86dee4bf59f9bb155e0e9b9fcd99f4817562eb52490666a950d09b556185c9`): **True**
- Deleting Parte 1-B restores `e325f2f5`: verify manually if needed.

## Guía docx wording (formatting-only)
- Multiset after stripping `|`/whitespace, pipe lines split, table headers excluded: **True** (diff count 0)

## Guía PDF
- Pages: **18** (expect 18 ±1)
- pdffonts Open Sans only: **True** (ok)
- PNGs: `_png/run9/guia-p01..04-110dpi.png`

## Prompts-IA sheet
- Pages: **2** (expect ≤2)
- prompts.txt lines missing from PDF: **0** (expect 0)
- Extra PDF lines: **0** (expect 0)
- Sheet docx/pdf sha: `3c8009d3acf0e3812107eb96b2d7b5c1c14f5342cdf71b48abd66c3d09a30a11` / `8397078cbb51d08d7224555059678757b03cab88dd5d86228f10f6c1d10a76a9`

## Byte-identical vs ref (non-delta)
- `hoja-1-mapa-de-calor.pdf`: **True**
- `hoja-2-flujo-de-datos.pdf`: **True**
- `hoja-3-dato-a-valor.pdf`: **True**
- `hoja-4-plantilla-tablero.pdf`: **True**
- `hoja-4b-ejemplo-air4u.pdf`: **True**
- `hoja-5-plantilla-pitch.pdf`: **True**
- `prompts-ia-v2.pdf`: **True**
- `Cuestionario-Dataton-24nov-equipos.pdf`: **True**
- `Cuestionario-ejemplo-Air4U.pdf`: **True**

## Zip delta vs ref
- `Prompts-IA-Dataton-24nov.docx`
- `Prompts-IA-Dataton-24nov.pdf`
- `guia-tecnica-mentores/Guia-tecnica-mentores.docx`
- `guia-tecnica-mentores/Guia-tecnica-mentores.pdf`
- `prompts.txt`
- Zip sha256: `67fceead4a1d3bea774e3576ccd2fd526894bc50f055554a8f624627a4bad94b`

## Artifact SHA256
- prompts.txt: `ff7ab27c22b3f03e2a2a0b55d477ccae2ccf637a7b79f946019add64109b5df8`
- Guía docx: `8a9823a4cae30447a84cf72ca6e05d1fd5d454a6949f343dc9e6d87349cd9c0b`
- Guía pdf: `554ad03f6c6058570ff1eca151ebd61b4dd59b07857cea2c54f783d8e98ff889`
- Prompts sheet docx: `3c8009d3acf0e3812107eb96b2d7b5c1c14f5342cdf71b48abd66c3d09a30a11`
- Prompts sheet pdf: `8397078cbb51d08d7224555059678757b03cab88dd5d86228f10f6c1d10a76a9`
- zip: `67fceead4a1d3bea774e3576ccd2fd526894bc50f055554a8f624627a4bad94b`
