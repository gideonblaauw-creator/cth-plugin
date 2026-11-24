# Run 6 notes — placeholder table fix

Start SHA (ticket): `c1ee80a66d83c897838832f6bcd27cc6ed504d57`. Working head: `c1ee80a66d83c897838832f6bcd27cc6ed504d57`.

## pdftotext hoja-3 / hoja-4
- `hoja-3-dato-a-valor.pdf`: token matches **0** (expect 0)
  - contains `LÍNEA BASE`: **True**
  - contains `DELTA`: **True**
  - contains `PAISAJE`: **True**
  - contains `[N1]`: **True**
  - contains `nota breve`: **True**
- `hoja-4-plantilla-tablero.pdf`: token matches **0** (expect 0)
  - contains `Delta: donde el dato se vuelve valor`: **True**
  - contains `entradas › salida › línea valor`: **True**
  - contains `Línea base del cliente (entrada)`: **True**

## Text diff vs c1ee80a (pdftotext lines)
- `Cuestionario-Dataton-24nov-equipos.pdf`: **0** changed lines
- `Cuestionario-ejemplo-Air4U.pdf`: **0** changed lines
- `Guia-tecnica-mentores.pdf`: **0** changed lines
- `LEEME.pdf`: **0** changed lines
- `agenda-equipos.pdf`: **0** changed lines
- `ejemplo-air4u.pdf`: **0** changed lines
- `fuentes-datos-abiertos.pdf`: **0** changed lines
- `guia-carpeta-drive.pdf`: **0** changed lines
- `hoja-1-mapa-de-calor.pdf`: **0** changed lines
- `hoja-2-flujo-de-datos.pdf`: **0** changed lines
- `hoja-3-dato-a-valor.pdf`: **25** diff lines (expect table swap only)
- `hoja-4-plantilla-tablero.pdf`: **17** diff lines (expect table swap only)
- `hoja-4b-ejemplo-air4u.pdf`: **0** changed lines
- `hoja-5-plantilla-pitch.pdf`: **0** changed lines
- `nota-derechos-datos.pdf`: **0** changed lines
- `plantilla-bmc.pdf`: **0** changed lines
- `prompts-ia-v2.pdf`: **0** changed lines

## pdffonts hoja-3 / hoja-4
### hoja-3-dato-a-valor.pdf
```
name                                 type              encoding         emb sub uni object ID
------------------------------------ ----------------- ---------------- --- --- --- ---------
AAAAAA+OpenSans-SemiBold             CID TrueType      Identity-H       yes yes yes     10  0
BAAAAA+OpenSans-Bold                 CID TrueType      Identity-H       yes yes yes     11  0
CAAAAA+OpenSans-Regular              CID TrueType      Identity-H       yes yes yes     12  0
DAAAAA+Arimo                         CID TrueType      Identity-H       yes yes yes     13  0
```
### hoja-4-plantilla-tablero.pdf
```
name                                 type              encoding         emb sub uni object ID
------------------------------------ ----------------- ---------------- --- --- --- ---------
AAAAAA+OpenSans-SemiBold             CID TrueType      Identity-H       yes yes yes     10  0
BAAAAA+OpenSans-Bold                 CID TrueType      Identity-H       yes yes yes     11  0
CAAAAA+OpenSans-Regular              CID TrueType      Identity-H       yes yes yes     12  0
```

## Glyph scan (OpenSans-Regular cmap)
Result: **0** out-of-cmap glyphs in hoja-3/hoja-4 text (except emoji + whitespace).

## pdfinfo pages
- `hoja-3-dato-a-valor.pdf`: Pages:           2
- `hoja-4-plantilla-tablero.pdf`: Pages:           2

## PNG _png/run6/ (110 dpi)
- `_png/run6/hoja-3-boceto-p01.png` sha256 `691d54777ece96d2e419030408d82a9311b24f0dd9bc3f6e6d31e3f63737ff2f`
- `_png/run6/hoja-4-puente-p01.png` sha256 `914a3ba3b2c81ae0fde8c40f67bbadecc093151733cba856680ada24ff34f7be`

## Zip
- `team-pack-es-pdfs-v0.4.zip` sha256 `72c1fbbf3273e4645a5e8c887cae22a14e8ee9140629db99a5655c25f5073d53`

| zip entry | sha256 |
|---|---|
| Cuestionario-Dataton-24nov-equipos.docx | `0ed244fa80725d0c26ace921c08bf243927ddfa916dd4b8ac989ef13d4ae8a5a` |
| Cuestionario-Dataton-24nov-equipos.pdf | `df28f7a25159f7dc516fc171329081a6c86fc75aea3d051bf7cb39debadc503d` |
| Cuestionario-ejemplo-Air4U.docx | `c0294707fa982d9eee32626797738d34a3d4dff985cdb352b91b8dcf145dfea6` |
| Cuestionario-ejemplo-Air4U.pdf | `ea4bfa7a19bdc0e475268e11ac00d3ac0278305b245ec16e71a100fe40d245da` |
| LEEME.md | `aa69d4b0735df61ea3f7573314b9eca97b6ae12958a5f44797034a8e50727e65` |
| LEEME.pdf | `5d6efd2767a481588159130f04b1261499083da4314deae804ed77402ab18286` |
| agenda-equipos.pdf | `911f8d5ea04baea0519218ef523f8cfe424d0e58c77c750f0a9d882a6d4794d8` |
| guia-tecnica-mentores/Guia-tecnica-mentores.docx | `443a9fffa0465aaa9c8434a4f2d78c5a33d355dcd068b4a6f807717f436c91fe` |
| guia-tecnica-mentores/Guia-tecnica-mentores.pdf | `c680b8a268f45e58e6047c319af9ae7af5f9127ce94a845f42c7a52642656ac6` |
| guia-tecnica-mentores/ejemplo-air4u.pdf | `7c95d7a08c6d3fee6997ae690f9c72c43c07487eab1f6b339aba3dd7f74345bf` |
| guia-tecnica-mentores/fuentes-datos-abiertos.pdf | `16bf29e9fee5e59e2bbae9a7550ea2263d98d6619818b2e6d1f9e35ff9ba5d2c` |
| guia-tecnica-mentores/hoja-1-mapa-de-calor.pdf | `a339dc2db327d5c5e8bba473c5160ec73e218f5de253b03dbc2386fa02430734` |
| guia-tecnica-mentores/hoja-2-flujo-de-datos.pdf | `04976413eb24263c1421e19dffd536bff0e437f143b358b3db28f694b536facd` |
| guia-tecnica-mentores/hoja-3-dato-a-valor.pdf | `443d47834ac6e3ce1f82ed3f82e04f16ad0ea9219c3cc49cc9c084ae010406a0` |
| guia-tecnica-mentores/hoja-4-plantilla-tablero.pdf | `98b45a46afde37bfd0cc3e00c4a2ba36031fa8fc2d585b33c6250928e9559356` |
| guia-tecnica-mentores/hoja-4b-ejemplo-air4u.pdf | `b4059b5274f6032dbbd7ace7815e6a06207b9e52638ef590e883c834b608ee56` |
| guia-tecnica-mentores/hoja-5-plantilla-pitch.pdf | `5c4c00a4e49c2f0a4684960545358dae3f6627e63f6d021bdfd22956c55eccaa` |
| guia-tecnica-mentores/plantilla-bmc.pdf | `86b79a644d03da1028a69bf2ffb3b81f5bace7a9731c78cf2c355d1435a03090` |
| guia-tecnica-mentores/prompts-ia-v2.pdf | `062c37e3f3d71f3de34d99c6480dd3f6882a484ff88109573e3efbc95707a450` |
| prompts.txt | `e325f2f5e8d60547a5ffd1047dbe241b23e071d2e763e7149f5a77f186424015` |

## Byte-identical confirmations (vs ticket)
- fonts/open-sans/SHA256SUMS unchanged: **True**
- `cuestionario/Cuestionario-Dataton-24nov-equipos.docx`: **True** (`0ed244fa80725d0c26ace921c08bf243927ddfa916dd4b8ac989ef13d4ae8a5a`)
- `cuestionario/Cuestionario-Dataton-24nov-equipos.pdf`: **True** (`df28f7a25159f7dc516fc171329081a6c86fc75aea3d051bf7cb39debadc503d`)
- `cuestionario/Cuestionario-ejemplo-Air4U.docx`: **True** (`c0294707fa982d9eee32626797738d34a3d4dff985cdb352b91b8dcf145dfea6`)
- `cuestionario/Cuestionario-ejemplo-Air4U.pdf`: **True** (`ea4bfa7a19bdc0e475268e11ac00d3ac0278305b245ec16e71a100fe40d245da`)
- `guia-tecnica/Guia-tecnica-mentores.docx`: **True** (`443a9fffa0465aaa9c8434a4f2d78c5a33d355dcd068b4a6f807717f436c91fe`)
- `guia-tecnica/Guia-tecnica-mentores.pdf`: **True** (`c680b8a268f45e58e6047c319af9ae7af5f9127ce94a845f42c7a52642656ac6`)
- `cuestionario/prompts.txt`: **True** (`e325f2f5e8d60547a5ffd1047dbe241b23e071d2e763e7149f5a77f186424015`)

## Key dist sha256
- `dist/Cuestionario-Dataton-24nov-equipos.pdf`: `df28f7a25159f7dc516fc171329081a6c86fc75aea3d051bf7cb39debadc503d`
- `dist/Cuestionario-ejemplo-Air4U.pdf`: `ea4bfa7a19bdc0e475268e11ac00d3ac0278305b245ec16e71a100fe40d245da`
- `dist/Guia-tecnica-mentores.pdf`: `c680b8a268f45e58e6047c319af9ae7af5f9127ce94a845f42c7a52642656ac6`
- `dist/LEEME.pdf`: `5d6efd2767a481588159130f04b1261499083da4314deae804ed77402ab18286`
- `dist/agenda-equipos.pdf`: `911f8d5ea04baea0519218ef523f8cfe424d0e58c77c750f0a9d882a6d4794d8`
- `dist/ejemplo-air4u.pdf`: `7c95d7a08c6d3fee6997ae690f9c72c43c07487eab1f6b339aba3dd7f74345bf`
- `dist/fuentes-datos-abiertos.pdf`: `16bf29e9fee5e59e2bbae9a7550ea2263d98d6619818b2e6d1f9e35ff9ba5d2c`
- `dist/guia-carpeta-drive.pdf`: `0f7701d742ed228bf01e94921fd908f2f13ab3c6d352e02e5d3df7a759647c8f`
- `dist/hoja-1-mapa-de-calor.pdf`: `a339dc2db327d5c5e8bba473c5160ec73e218f5de253b03dbc2386fa02430734`
- `dist/hoja-2-flujo-de-datos.pdf`: `04976413eb24263c1421e19dffd536bff0e437f143b358b3db28f694b536facd`
- `dist/hoja-3-dato-a-valor.pdf`: `443d47834ac6e3ce1f82ed3f82e04f16ad0ea9219c3cc49cc9c084ae010406a0`
- `dist/hoja-4-plantilla-tablero.pdf`: `98b45a46afde37bfd0cc3e00c4a2ba36031fa8fc2d585b33c6250928e9559356`
- `dist/hoja-4b-ejemplo-air4u.pdf`: `b4059b5274f6032dbbd7ace7815e6a06207b9e52638ef590e883c834b608ee56`
- `dist/hoja-5-plantilla-pitch.pdf`: `5c4c00a4e49c2f0a4684960545358dae3f6627e63f6d021bdfd22956c55eccaa`
- `dist/nota-derechos-datos.pdf`: `bb631f4bb0815b855aa76d92ecd0571900e3c837844c803e27278edb375d8009`
- `dist/plantilla-bmc.pdf`: `86b79a644d03da1028a69bf2ffb3b81f5bace7a9731c78cf2c355d1435a03090`
- `dist/prompts-ia-v2.pdf`: `062c37e3f3d71f3de34d99c6480dd3f6882a484ff88109573e3efbc95707a450`
