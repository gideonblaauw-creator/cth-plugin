# Run 10 notes

Head: `de1999e5259177ab46469e1a90067d3732ff151e`.
Base: `de1999e5259177ab46469e1a90067d3732ff151e`.

## prompts.txt v3 (locked)
- sha256: `4cd248ad16227c7cbd6fc33a5b89548920ab978371525a5e57a5de9b95e2fe6a` (expect `4cd248ad16227c7cbd6fc33a5b89548920ab978371525a5e57a5de9b95e2fe6a`): **True**
- bytes: **7997** (expect 7997)

## Questionnaire instruction boxes
- equipos Parte 0–4 bodies = v3: **True**
- ejemplo Parte 0–4 bodies = v3: **True**
- equipos Parte 1-B optional box = v3: **True**
- ejemplo Parte 1-B optional box = v3: **True**
- Parte 2 Qué entregan: **True**

## Docx diff vs run 9 (AI boxes + optional 1-B + Parte 2 entregan only)
- equipos: **True** (stray=0)
- ejemplo: **True** (stray=0)

## Guía PDF
- pages: **18** (expect 18 ±1)
- pdftotext pp 1–3 lines starting with '|': **0** (expect 0)
- pdffonts Open Sans only: **True**
- docx wording vs `72ea013b`: **True** (only G table split (4 rows + capitals))

- pdffonts equipos: **True** (ok)
- pdffonts ejemplo: **True** (ok)
- pdffonts sheet: **True** (ok)

## PNGs
- `_png/run10/guia-p02..03-110dpi.png`
- `_png/run10/*-parte1-110dpi.png` (equipos + ejemplo)

## Pinned vs run 9 head
- `hoja-2-flujo-de-datos.pdf`: **True**
- `prompts-ia-v2.pdf`: **True**
- Guía docx unchanged from run 9: **False**

## Zip delta vs run 9
- members: ['Cuestionario-Dataton-24nov-equipos.docx', 'Cuestionario-Dataton-24nov-equipos.pdf', 'Cuestionario-ejemplo-Air4U.docx', 'Cuestionario-ejemplo-Air4U.pdf', 'Prompts-IA-Dataton-24nov.docx', 'Prompts-IA-Dataton-24nov.pdf', 'guia-tecnica-mentores/Guia-tecnica-mentores.pdf', 'prompts.txt']
- zip sha256: `c4f70884359ea16c1e655f6cd1d11d051a1f6fc16ec09cbc47bb3029a0b99102`

## SHA256 (changed)
- prompts.txt: `4cd248ad16227c7cbd6fc33a5b89548920ab978371525a5e57a5de9b95e2fe6a`
- equipos docx: `fd8faa3d2d164ef6b5363c6d262ae41ae63d9ca5704eab3667dfd5d2dc1fa732`
- equipos pdf: `f734bd8ffeac5f24415ef40e8eb98f0dc7516362316dea31a8ca4db5b7ec24bc`
- ejemplo docx: `8d25c7d3844699a76f86bcc9a93e74cec3765bde120c370a4b98b7e4b5e88bdc`
- ejemplo pdf: `b2a8898678d70e365350274969ffd5357bb9a49c0b6c145e2f6aa72539bad403`
- sheet docx: `b286bcd5ad29d3716f25f6b7b97d51f82ca6bcf644272f9c464f864b16623cf0`
- sheet pdf: `adfbb8bf081ee08fb9e9f97624f6ae47ee4693822d3d824c236d8d9b897e9aaa`
- Guía pdf: `9bf595a44608c5466a850ef0dd046c9e4669c668d2a9d663e1f43e3a1cc0ae33`
- zip: `c4f70884359ea16c1e655f6cd1d11d051a1f6fc16ec09cbc47bb3029a0b99102`
