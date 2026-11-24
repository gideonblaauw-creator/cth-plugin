# Run 4 diff notes (PR #177 micro-run: fonts + Parte 4 line)

## Start head

`606679d7e1f8eef0faa3621ef0b4b24af47e74ff` on `cursor/dataton-team-pack-v04-es`

## Code changes (builders only)

1. **Parte 4 «Qué entregan» (q + ej):** `Guion de cinco minutos.` → `Guion de cinco minutos (600–650 palabras).` (en dash U+2013) in `cuestionario/build-cuestionario.py`.
2. **PDF fonts:** `sudo apt-get install -y fonts-open-sans`; `fc-cache -f`; `fc-list | grep -i "open sans"` OK. Re-exported q/ej/guía PDFs via LibreOffice (existing export path). On a clean VM, LO still fell back to DejaVu/Noto for glyphs missing from stock Open Sans (→, subscript ₂₅, box-drawing in guía). For **pdffonts acceptance**, this build used **user-local merged Open Sans** TTFs (`fontTools.merge` Open Sans + DejaVu, `~/.local/share/fonts/open-sans-merged/`, not in repo). Text unchanged; no prompt edits.
3. **theme1.xml:** `patch_docx_theme_open_sans()` after save in `build-cuestionario.py` and `build-guia-tecnica-mentores.py` — major/minor `<a:latin typeface>` → `Open Sans`.

## Grep / content

| File | `Guion de cinco minutos (600–650 palabras).` count |
|------|-----------------------------------------------------|
| `Cuestionario-Dataton-24nov-equipos.docx` | 1 |
| `Cuestionario-ejemplo-Air4U.docx` | 1 |

`prompts.txt` sha256 (unchanged): `e325f2f5e8d60547a5ffd1047dbe241b23e071d2e763e7149f5a77f186424015`

## theme1.xml latin typefaces (after build)

| docx | majorFont latin | minorFont latin |
|------|-----------------|-----------------|
| q.docx | Open Sans | Open Sans |
| ej.docx | Open Sans | Open Sans |
| guía.docx | Open Sans | Open Sans |

## pdfinfo page counts

| PDF | Pages |
|-----|-------|
| `Cuestionario-Dataton-24nov-equipos.pdf` | 7 |
| `Cuestionario-ejemplo-Air4U.pdf` | 6 |
| `Guia-tecnica-mentores.pdf` | 55 |

(no page-count change vs run 3 targets)

## pdffonts (full)

```
=== Cuestionario-Dataton-24nov-equipos.pdf ===
name                                 type              encoding         emb sub uni object ID
------------------------------------ ----------------- ---------------- --- --- --- ---------
BAAAAA+OpenSans-Bold                 TrueType          WinAnsi          yes yes yes    548  0
CAAAAA+OpenSans                      TrueType          WinAnsi          yes yes yes    558  0
DAAAAA+OpenSans-Italic               TrueType          WinAnsi          yes yes yes    553  0
EAAAAA+NotoColorEmoji                Type 3            Custom           yes yes yes    561  0
=== Cuestionario-ejemplo-Air4U.pdf ===
BAAAAA+OpenSans-Bold                 TrueType          WinAnsi          yes yes yes    496  0
CAAAAA+OpenSans                      TrueType          WinAnsi          yes yes yes    501  0
EAAAAA+NotoColorEmoji                Type 3            Custom           yes yes yes    504  0
=== Guia-tecnica-mentores.pdf ===
BAAAAA+OpenSans-Bold                 TrueType          WinAnsi          yes yes yes   1605  0
CAAAAA+OpenSans                      TrueType          WinAnsi          yes yes yes   1620  0
DAAAAA+OpenSans-Italic               TrueType          WinAnsi          yes yes yes   1615  0
EAAAAA+OpenSans-BoldItalic           TrueType          WinAnsi          yes yes yes   1610  0
```

Allowed emoji exception: NotoColorEmoji only in q/ej (🟥🟧🟦 legend). Guía: Open Sans variants only.

### Pre-merge fallback glyphs (stock Open Sans + apt; not swapped — reported)

| Char | Pages (examples) | Font fallback |
|------|------------------|---------------|
| → | q p4; ej p3; guía many | DejaVuSans |
| ₂ ₅ | q/ej/guía (PM₂.₅) | NotoSans-Regular / Italic |
| Box-drawing (─│┌…) | guía (tables) | DejaVuSans |

Plain equivalent `PM2.5` exists elsewhere in pack; text left frozen per ticket.

## pdftotext diff (q/ej, before → after)

- **Semantic:** only Parte 4 «Qué entregan» line gains `(600–650 palabras)` (both q and ej).
- **Reflow:** widespread whitespace/line-wrap shifts from Open Sans metrics (~109 diff lines in `pdftotext -layout` unified diff); **no** page-count change.

## sha256

| Artifact | sha256 |
|----------|--------|
| `cuestionario/Cuestionario-Dataton-24nov-equipos.docx` | `ce826289950a6cebbfb0aad011f05e3780fa86953f0e5716b48aefcb0abe3e18` |
| `cuestionario/Cuestionario-Dataton-24nov-equipos.pdf` | `ef2f72803dfa0690ae41c826a7cdeca2bdbe8f865a585b4928793e2469c3b52e` |
| `cuestionario/Cuestionario-ejemplo-Air4U.docx` | `2955e5ed9e8d5a4fe9746e3569e1e102be60a02185536f5d9bfe9cf99165d259` |
| `cuestionario/Cuestionario-ejemplo-Air4U.pdf` | `06ccfe21d59696282e4ca5ec0dc097ca42597268f9066b151a3e40b37161ba4b` |
| `guia-tecnica/Guia-tecnica-mentores.docx` | `855246f97653af8a37c65a9a8802a254c2e199688bd4eac363fcf98560e7fcec` |
| `guia-tecnica/Guia-tecnica-mentores.pdf` | `a5b99a6578d56aae092c0d675b1ee41cdacac50940a02b40d2b34fa355d24c87` |
| `cuestionario/prompts.txt` | `e325f2f5e8d60547a5ffd1047dbe241b23e071d2e763e7149f5a77f186424015` |
| `team-pack-es-pdfs-v0.4.zip` | `4d842b5e91359964c49afd9fa2667dfb052dc9f492c5a1ce3446192a0c8fab38` |

Rebuilt with `build-pack.py` (dist copies + zip + manifest + ticket PNGs).