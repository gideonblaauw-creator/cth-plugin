# Run 8 notes — Guía PDF + tie-break addendum + Prompts-IA sheet

Ticket base: `73885721053aa956b8337f20f39d6baaa7451c6a`. Addendum ticket `b0251ac9`.

## Deliverables
- Guía PDF: docx-sourced front matter, Hoja 5, prompts; merged hojas 1–4b (Open Sans merge renders); embedded Open Sans stamp.
- Hoja 4: mapa section `keep` wrapper (dist + Guía section).
- Tie-break: Guía docx para 26 + Hoja 5 intro only; team `hoja-5-plantilla-pitch.md` unchanged.
- New: `cuestionario/Prompts-IA-Dataton-24nov.docx` + `.pdf`, `dist/` copies, in zip.
- Proofs: `_png/run8/` (pdffonts, paragraph check, contact sheets, hoja-4 110 dpi, prompts sheet 110 dpi, word-bags, SHA256SUMS).
- Script: `scripts/run8_self_check.py` (exit 0).

Working head: see git after push.

## Paragraph check (normalized)
- Missing docx paragraphs in PDF: **0** (expect 0)
- Extra PDF lines vs docx: **0** (expect 0)
- Log: `_png/run8/paragraph-check.txt`

## Tie-break addendum (docx)
- Guía docx paragraph diffs vs pre-addendum (`73885721`): **2** (expect 2)
- Changed paragraphs: M6 finales bullet + Hoja 5 intro (Guía only; team hoja-5.md untouched)

## pdffonts
- Guía embedded Open Sans only: **True** (ok)
- Prompts-IA sheet (Open Sans + emoji ok): **True** (ok)
- Log: `_png/run8/pdffonts.txt`

## Prompts-IA team sheet word check
- prompts.txt lines missing from PDF: **0**
- Extra PDF lines: **0**
- PNGs: `_png/run8/prompts-ia-dataton-24nov-p01-110dpi.png` (+ p02 if present)

## Contact sheets
- `_png/run8/guia-pdf-contact-40dpi.png` (40 dpi, all Guía pages)
- `_png/run8/hoja-4-plantilla-tablero-p01-110dpi.png` (+ p02, p03 @ 110 dpi)

## Word-bag vs ref head
- hoja-2-flujo-de-datos.pdf: word-bag delta **0**
- hoja-3-dato-a-valor.pdf: word-bag delta **0**
- hoja-4-plantilla-tablero.pdf: word-bag delta **0**
- hoja-4b-ejemplo-air4u.pdf: word-bag delta **0**
- prompts-ia-v2.pdf: word-bag delta **0**

## Pinned artifacts
- Guía docx sha256: `3706fe5c463cf7e9c102933efa5f4453c774959bc777b2619a23c617ae179f9d`
- `cuestionario/Cuestionario-Dataton-24nov-equipos.docx` byte-identical: **True**
- `cuestionario/Cuestionario-Dataton-24nov-equipos.pdf` byte-identical: **True**
- `cuestionario/Cuestionario-ejemplo-Air4U.docx` byte-identical: **True**
- `cuestionario/Cuestionario-ejemplo-Air4U.pdf` byte-identical: **True**
- `cuestionario/prompts.txt` byte-identical: **True**

## SHA256SUMS
- Proof: `_png/run8/SHA256SUMS`
- `3706fe5c463cf7e9c102933efa5f4453c774959bc777b2619a23c617ae179f9d  guia-tecnica/Guia-tecnica-mentores.docx`
- `b86dc0bad860ec076493377f394255f693cc2e7ebe73810994f688b94ae2b666  guia-tecnica/Guia-tecnica-mentores.pdf`
- `c0f142f582a3477d73237b0bef831733933d9892bafa90877c74a97fabab28cb  dist/hoja-4-plantilla-tablero.pdf`
- `f07acb87faaf09cfe807034198b944f23305ccf427500d827c3e94726fc30a47  team-pack-es-pdfs-v0.4.zip`
- `dc165fbdb10856bcfcd8b51b435d292b93c474b2dc2529d9ee30e2ea63f123c9  dist/Prompts-IA-Dataton-24nov.docx`
- `82864b976fd68d892aa1743c128a9963407e33b329b1259f288d0a99fc94d8b5  dist/Prompts-IA-Dataton-24nov.pdf`

