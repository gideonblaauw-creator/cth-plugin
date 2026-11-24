#!/usr/bin/env python3
"""Run 7 acceptance checks — Guía layout rebuild (PR #177)."""
from __future__ import annotations

import hashlib
import math
import re
import shutil
import subprocess
import tempfile
import zipfile
from collections import Counter
from pathlib import Path

from docx import Document
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dist"
PROOFS = ROOT / "_png" / "run7"
REPO = ROOT.parent.parent
START_HEAD = "9ba28ff6d4050ff0da62767b6bd65409bad1a752"
BASELINE_DOCX_SHA = "443a9fffa0465aaa9c8434a4f2d78c5a33d355dcd068b4a6f807717f436c91fe"
OLD_GUia_PDF_SHA = "c680b8a268f45e58e6047c319af9ae7af5f9127ce94a845f42c7a52642656ac6"
ZIP = ROOT / "team-pack-es-pdfs-v0.4.zip"
OFL = ROOT / "fonts" / "open-sans" / "OpenSans-Regular.ttf"
GUia_DOCX = ROOT / "guia-tecnica" / "Guia-tecnica-mentores.docx"
GUia_PDF = ROOT / "guia-tecnica" / "Guia-tecnica-mentores.pdf"
ALLOWED_EMOJI = {0x1F7E5, 0x1F7E7, 0x1F7E6}
WHITESPACE = {9, 10, 11, 12, 13, 32, 160, 0x202F, 0x2003}

BYTE_IDENTICAL = [
    ("cuestionario/Cuestionario-Dataton-24nov-equipos.docx", "0ed244fa80725d0c26ace921c08bf243927ddfa916dd4b8ac989ef13d4ae8a5a"),
    ("cuestionario/Cuestionario-Dataton-24nov-equipos.pdf", "df28f7a25159f7dc516fc171329081a6c86fc75aea3d051bf7cb39debadc503d"),
    ("cuestionario/Cuestionario-ejemplo-Air4U.docx", "c0294707fa982d9eee32626797738d34a3d4dff985cdb352b91b8dcf145dfea6"),
    ("cuestionario/Cuestionario-ejemplo-Air4U.pdf", "ea4bfa7a19bdc0e475268e11ac00d3ac0278305b245ec16e71a100fe40d245da"),
    ("cuestionario/prompts.txt", "e325f2f5e8d60547a5ffd1047dbe241b23e071d2e763e7149f5a77f186424015"),
]

EXTRA_WORDS = {
    "guía",
    "técnica",
    "solo",
    "mentores",
    "índice",
    "niveles",
    "confianza",
    "dato",
    "metodología",
    "v0.3",
    "cómo",
    "elegimos",
    "jurado",
    "datatón",
    "nov",
    "2026",
    "compilación",
    "hojas",
    "metodológicas",
    "rúbrica",
    "prompts",
    "documento",
    "trabajo",
    "technical",
    "guide",
    "for",
    "cleantechhub",
    "mapa",
    "calor",
    "flujo",
    "plantilla",
    "tablero",
    "ejemplo",
    "air4u",
    "pitch",
    "puntuación",
    "desempata",
    "empatan",
    "qa",
    "qb",
    "qc",
    "es",
    "v0",
    "4",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def word_bag_docx(path: Path) -> Counter:
    doc = Document(path)
    words: list[str] = []
    for para in doc.paragraphs:
        words.extend(re.findall(r"\w+", para.text.lower(), flags=re.UNICODE))
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                words.extend(re.findall(r"\w+", cell.text.lower(), flags=re.UNICODE))
    return Counter(words)


def word_bag_pdf_text(text: str) -> Counter:
    words = re.findall(r"\w+", text.lower(), flags=re.UNICODE)
    return Counter(words)


def pdftotext(pdf: Path) -> str:
    return subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True, check=True).stdout


def glyph_scan(text: str, cmap: dict[int, str]) -> list[tuple[int, str]]:
    bad: list[tuple[int, str]] = []
    for ch in text:
        code = ord(ch)
        if code in WHITESPACE or code in ALLOWED_EMOJI:
            continue
        if code not in cmap:
            bad.append((code, ch))
    return bad


def contact_sheet(pdf: Path, out: Path, dpi: int = 40) -> None:
    import fitz

    doc = fitz.open(pdf)
    cols = min(5, doc.page_count)
    rows = math.ceil(doc.page_count / cols)
    w = int(8.27 * dpi / 2.54)
    h = int(11.69 * dpi / 2.54)
    sheet = fitz.open()
    for i in range(doc.page_count):
        pix = doc[i].get_pixmap(dpi=dpi, alpha=False)
        page = sheet.new_page(width=w, height=h)
        page.insert_image(page.rect, pixmap=pix)
    # mosaic pages
    mosaic = fitz.open()
    page_w = w * cols
    page_h = h * rows
    cp = mosaic.new_page(width=page_w, height=page_h)
    for i in range(doc.page_count):
        r = i // cols
        c = i % cols
        rect = fitz.Rect(c * w, r * h, (c + 1) * w, (r + 1) * h)
        pix = doc[i].get_pixmap(dpi=dpi, alpha=False)
        cp.insert_image(rect, pixmap=pix)
    mosaic.save(out)
    doc.close()
    mosaic.close()
    sheet.close()


def libreoffice_pdf(docx: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", str(out_dir), str(docx)],
        check=True,
        capture_output=True,
    )
    return out_dir / (docx.stem + ".pdf")


def main() -> int:
    PROOFS.mkdir(parents=True, exist_ok=True)
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=str(REPO), capture_output=True, text=True, check=True
    ).stdout.strip()
    lines: list[str] = []
    lines.append("# Run 7 notes — Guía técnica layout rebuild")
    lines.append("")
    lines.append(f"Start head (ticket): `{START_HEAD}`.")
    lines.append(f"Working head after build: `{head}`.")
    lines.append("")

    # Contact sheets
    guia_pdf = OUT / "Guia-tecnica-mentores.pdf"
    if not guia_pdf.is_file():
        guia_pdf = GUia_PDF
    contact_sheet(guia_pdf, PROOFS / "guia-pdf-contact-40dpi.png", dpi=40)
    lo_dir = PROOFS / "lo-render"
    lo_pdf = libreoffice_pdf(GUia_DOCX, lo_dir)
    contact_sheet(lo_pdf, PROOFS / "guia-docx-lo-contact-40dpi.png", dpi=40)
    lines.append("## Contact sheets (40 dpi)")
    lines.append(f"- `{PROOFS.relative_to(ROOT)}/guia-pdf-contact-40dpi.png`")
    lines.append(f"- `{PROOFS.relative_to(ROOT)}/guia-docx-lo-contact-40dpi.png`")
    lines.append("")

    # Word bags
    with tempfile.TemporaryDirectory() as td:
        baseline_docx = Path(td) / "base.docx"
        proc = subprocess.run(
            ["git", "show", f"{START_HEAD}:decks/dataton-2026-team-pack/guia-tecnica/Guia-tecnica-mentores.docx"],
            cwd=str(REPO),
            capture_output=True,
            check=True,
        )
        baseline_docx.write_bytes(proc.stdout)
        bag_base = word_bag_docx(baseline_docx)
    bag_new_docx = word_bag_docx(GUia_DOCX)
    bag_new_pdf = word_bag_pdf_text(pdftotext(guia_pdf))

    docx_only_base = set(bag_base.keys())
    docx_only_new = set(bag_new_docx.keys())
    docx_word_delta = sorted(docx_only_new - docx_only_base) + sorted(docx_only_base - docx_only_new)

    pdf_minus_docx = set(bag_new_pdf.keys()) - set(bag_new_docx.keys())
    unexpected_pdf = sorted(w for w in pdf_minus_docx if w not in EXTRA_WORDS and not w.isdigit())

    diff_path = PROOFS / "word-diff.txt"
    diff_path.write_text(
        "\n".join(
            [
                f"docx vs baseline 443a9fff word delta ({len(docx_word_delta)}):",
                *docx_word_delta[:200],
                "",
                f"pdf minus new docx ({len(pdf_minus_docx)} words), unexpected ({len(unexpected_pdf)}):",
                *unexpected_pdf[:200],
            ]
        ),
        encoding="utf-8",
    )
    lines.append("## Word-bag checks")
    lines.append(f"- New docx vs baseline docx word delta: **{len(docx_word_delta)}** (expect 0)")
    lines.append(f"- PDF minus docx unexpected words: **{len(unexpected_pdf)}**")
    lines.append(f"- Proof: `{diff_path.relative_to(ROOT)}`")
    lines.append("")

    # pdffonts
    font_log = PROOFS / "pdffonts.txt"
    chunks = []
    for name in ("Guia-tecnica-mentores.pdf", "hoja-3-dato-a-valor.pdf"):
        p = OUT / name
        r = subprocess.run(["pdffonts", str(p)], capture_output=True, text=True, check=True)
        chunks.append(f"=== {name} ===\n{r.stdout.strip()}\n")
    font_log.write_text("\n".join(chunks), encoding="utf-8")
    font_text = font_log.read_text()
    arimo_h3 = "Arimo" in font_text.split("=== hoja-3")[1] if "=== hoja-3" in font_text else True
    arimo_guia = "Arimo" in font_text.split("=== Guia")[1].split("===")[0] if "=== Guia" in font_text else True
    arimo = arimo_h3 or arimo_guia
    lines.append("## pdffonts")
    lines.append(f"- Arimo present: **{arimo}** (expect False)")
    lines.append(f"- Log: `{font_log.relative_to(ROOT)}`")
    lines.append("")

    # Glyph scan
    cmap = TTFont(OFL).getBestCmap()
    glyph_bad: list[str] = []
    for name in ("hoja-3-dato-a-valor.pdf", "Guia-tecnica-mentores.pdf"):
        for pi, page in enumerate(pdftotext(OUT / name).split("\f"), 1):
            bad = glyph_scan(page, cmap)
            if bad:
                glyph_bad.append(f"{name} p{pi}: {bad[:5]}")
    lines.append("## Glyph scan (OpenSans-Regular)")
    lines.append(f"- Out-of-cmap hits: **{len(glyph_bad)}**")
    if glyph_bad:
        for hit in glyph_bad[:10]:
            lines.append(f"  - {hit}")
    lines.append("")

    # Page count
    info = subprocess.run(["pdfinfo", str(guia_pdf)], capture_output=True, text=True, check=True).stdout
    pages_line = next((ln for ln in info.splitlines() if ln.startswith("Pages:")), "Pages: ?")
    lines.append("## Guía PDF page count")
    lines.append(f"- {pages_line.strip()}")
    lines.append("")

    # SHAs
    sums_path = PROOFS / "SHA256SUMS"
    sum_rows: list[str] = []
    targets = [
        GUia_DOCX,
        GUia_PDF,
        OUT / "Guia-tecnica-mentores.docx",
        OUT / "Guia-tecnica-mentores.pdf",
        OUT / "hoja-3-dato-a-valor.pdf",
        ZIP,
        ROOT / "fonts/open-sans/SHA256SUMS",
    ]
    for t in targets:
        if t.is_file():
            sum_rows.append(f"{sha256(t)}  {t.relative_to(ROOT)}")
    sums_path.write_text("\n".join(sum_rows) + "\n", encoding="utf-8")
    lines.append("## SHA256SUMS")
    lines.append(f"Proof: `{sums_path.relative_to(ROOT)}`")
    for row in sum_rows:
        lines.append(f"- `{row.split()[-1]}`: `{row.split()[0]}`")
    lines.append("")

    # Byte identical
    lines.append("## Byte-identical (q/ej/prompts/fonts)")
    base_fonts = subprocess.run(
        ["git", "show", f"{START_HEAD}:decks/dataton-2026-team-pack/fonts/open-sans/SHA256SUMS"],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    fonts_ok = (ROOT / "fonts/open-sans/SHA256SUMS").read_text() == base_fonts
    lines.append(f"- fonts/open-sans/SHA256SUMS unchanged: **{fonts_ok}**")
    for relpath, expected in BYTE_IDENTICAL:
        actual = sha256(ROOT / relpath)
        lines.append(f"- `{relpath}`: **{actual == expected}** (`{actual}`)")
    lines.append("")

    # Zip delta note
    lines.append("## Zip")
    lines.append(f"- `{ZIP.name}` sha256 `{sha256(ZIP)}`")
    lines.append("- Expected zip deltas: Guía docx/pdf, hoja-3 PDF (Arimo fix); other entries unchanged.")
    lines.append("")

    notes = ROOT / "run7-notes.md"
    notes.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(notes)
    fail = bool(docx_word_delta) or arimo or glyph_bad or unexpected_pdf
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())