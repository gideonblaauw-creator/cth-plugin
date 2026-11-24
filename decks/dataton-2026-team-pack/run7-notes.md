# Run 7 notes — Guía técnica layout rebuild

Start head (ticket): `9ba28ff6d4050ff0da62767b6bd65409bad1a752`.
Working head after build: `8fdf69e8ca41d78ffe29f995a8fcf21cd6923c5a`.

## Contact sheets (40 dpi)
- `_png/run7/guia-pdf-contact-40dpi.png`
- `_png/run7/guia-docx-lo-contact-40dpi.png`

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
- Pages:           25

## SHA256SUMS
Proof: `_png/run7/SHA256SUMS`
- `guia-tecnica/Guia-tecnica-mentores.docx`: `79d8bb715d8ed6a6c71869ccc3481ce6f3e375555f6b4ff441671f1edbb1d306`
- `guia-tecnica/Guia-tecnica-mentores.pdf`: `8744cc28ebf1e19e6b0e1f42766cad14842d3b8d3e6c45ca16832d7b8595c08c`
- `dist/Guia-tecnica-mentores.docx`: `79d8bb715d8ed6a6c71869ccc3481ce6f3e375555f6b4ff441671f1edbb1d306`
- `dist/Guia-tecnica-mentores.pdf`: `8744cc28ebf1e19e6b0e1f42766cad14842d3b8d3e6c45ca16832d7b8595c08c`
- `dist/hoja-3-dato-a-valor.pdf`: `086b1c40d5ca2ecad56c18259dabf51c25cc9606eb237397ca0ee56ae2da5b05`
- `team-pack-es-pdfs-v0.4.zip`: `cdbdacad8f75264459ea5357c88aa820a41b514234969bda58621959fb867d6a`
- `fonts/open-sans/SHA256SUMS`: `9549ad13703830523905857d37b674e849e22514af8f061567a4323f13f09287`

## Byte-identical (q/ej/prompts/fonts)
- fonts/open-sans/SHA256SUMS unchanged: **True**
- `cuestionario/Cuestionario-Dataton-24nov-equipos.docx`: **True** (`0ed244fa80725d0c26ace921c08bf243927ddfa916dd4b8ac989ef13d4ae8a5a`)
- `cuestionario/Cuestionario-Dataton-24nov-equipos.pdf`: **True** (`df28f7a25159f7dc516fc171329081a6c86fc75aea3d051bf7cb39debadc503d`)
- `cuestionario/Cuestionario-ejemplo-Air4U.docx`: **True** (`c0294707fa982d9eee32626797738d34a3d4dff985cdb352b91b8dcf145dfea6`)
- `cuestionario/Cuestionario-ejemplo-Air4U.pdf`: **True** (`ea4bfa7a19bdc0e475268e11ac00d3ac0278305b245ec16e71a100fe40d245da`)
- `cuestionario/prompts.txt`: **True** (`e325f2f5e8d60547a5ffd1047dbe241b23e071d2e763e7149f5a77f186424015`)

## Zip
- `team-pack-es-pdfs-v0.4.zip` sha256 `cdbdacad8f75264459ea5357c88aa820a41b514234969bda58621959fb867d6a`
- Zip entries changed vs `9ba28ff` (4 only): `Guia-tecnica-mentores.docx`, `Guia-tecnica-mentores.pdf`, `hoja-3-dato-a-valor.pdf`, `prompts-ia-v2.pdf`.

