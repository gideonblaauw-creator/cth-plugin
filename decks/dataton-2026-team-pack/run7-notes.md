# Run 7 notes — Guía técnica layout rebuild

Start head (ticket): `9ba28ff6d4050ff0da62767b6bd65409bad1a752`.
Working head after build: `71b4fc82c5e8de20c5bcbd8a01e0c3a6d6c9d15c`.

## Contact sheets (40 dpi)
- `_png/run7/guia-pdf-contact-40dpi.png`
- `_png/run7/guia-docx-lo-contact-40dpi.png`
- `_png/run7/hoja-3-contact-40dpi.png`
- `_png/run7/hoja-4-contact-40dpi.png`
- `_png/run7/hoja-4-plantilla-tablero-p01-110dpi.png` (+ p02, p03)

## Hoja PDF word-bags (addendum 2)
- `hoja-3-dato-a-valor.pdf` word-bag delta vs pre–addendum-2: **0**
- `hoja-4-plantilla-tablero.pdf` word-bag delta vs pre–addendum-2: **0**

## Word-bag checks
- New docx vs baseline docx word delta: **0** (expect 0)
- PDF minus docx unexpected words: **0**
- Proof: `_png/run7/word-diff.txt`

## pdffonts
- Arimo present: **False** (expect False)
- Log: `_png/run7/pdffonts.txt`

## Glyph scan (OpenSans-Regular)
- Out-of-cmap hits: **0**

## Guía PDF page count
- Pages:           26

## SHA256SUMS
Proof: `_png/run7/SHA256SUMS`
- `guia-tecnica/Guia-tecnica-mentores.docx`: `e5e0bac8e1ded222159aa218da9b9e4cb53c6a9fe83454a0837f884165d37d10`
- `guia-tecnica/Guia-tecnica-mentores.pdf`: `b13608c43c23aa1aa9c3b00e87753b4fafd7366e02a05a22d97ead077aa43ef6`
- `dist/Guia-tecnica-mentores.docx`: `e5e0bac8e1ded222159aa218da9b9e4cb53c6a9fe83454a0837f884165d37d10`
- `dist/Guia-tecnica-mentores.pdf`: `b13608c43c23aa1aa9c3b00e87753b4fafd7366e02a05a22d97ead077aa43ef6`
- `dist/hoja-3-dato-a-valor.pdf`: `e68cc8932601fc12e7444c8af83a2adfd753d196815cf748ff0c1efc105b2a82`
- `team-pack-es-pdfs-v0.4.zip`: `1cf85e7dc74707b9743ce37085db0b7ade9a6735b8b0d62fbf353db7b3b08efd`
- `fonts/open-sans/SHA256SUMS`: `9549ad13703830523905857d37b674e849e22514af8f061567a4323f13f09287`

## Byte-identical (q/ej/prompts/fonts)
- fonts/open-sans/SHA256SUMS unchanged: **True**
- `cuestionario/Cuestionario-Dataton-24nov-equipos.docx`: **True** (`0ed244fa80725d0c26ace921c08bf243927ddfa916dd4b8ac989ef13d4ae8a5a`)
- `cuestionario/Cuestionario-Dataton-24nov-equipos.pdf`: **True** (`df28f7a25159f7dc516fc171329081a6c86fc75aea3d051bf7cb39debadc503d`)
- `cuestionario/Cuestionario-ejemplo-Air4U.docx`: **True** (`c0294707fa982d9eee32626797738d34a3d4dff985cdb352b91b8dcf145dfea6`)
- `cuestionario/Cuestionario-ejemplo-Air4U.pdf`: **True** (`ea4bfa7a19bdc0e475268e11ac00d3ac0278305b245ec16e71a100fe40d245da`)
- `cuestionario/prompts.txt`: **True** (`e325f2f5e8d60547a5ffd1047dbe241b23e071d2e763e7149f5a77f186424015`)

## Zip
- `team-pack-es-pdfs-v0.4.zip` sha256 `1cf85e7dc74707b9743ce37085db0b7ade9a6735b8b0d62fbf353db7b3b08efd`
- Expected zip deltas: Guía docx/pdf, hoja-3 PDF (Arimo fix); other entries unchanged.

