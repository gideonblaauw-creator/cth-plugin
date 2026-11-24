#!/usr/bin/env python3
"""Run 8 acceptance checks — Guía PDF wording/fonts + hoja-4 mapa layout."""
from __future__ import annotations

import hashlib
import math
import re
import subprocess
import tempfile
from collections import Counter
from pathlib import Path

import fitz
from docx import Document

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dist"
PROOFS = ROOT / "_png" / "run8"
REPO = ROOT.parent.parent
REF_HEAD = "73885721053aa956b8337f20f39d6baaa7451c6a"
BASELINE_DOCX_SHA = "443a9fffa0465aaa9c8434a4f2d78c5a33d355dcd068b4a6f807717f436c91fe"
PRE_ADDENDUM_DOCX_REF = "73885721053aa956b8337f20f39d6baaa7451c6a"
BASELINE_DOCX_REF = "443a9fff"
PROMPTS_IA_SHEET_PDF = ROOT / "dist" / "Prompts-IA-Dataton-24nov.pdf"
PROMPTS_IA_SHEET_DOCX = ROOT / "dist" / "Prompts-IA-Dataton-24nov.docx"
PROMPTS_SHEET_TOP = "Suban su cuestionario lleno al chat de IA y copien una instrucción a la vez."
ZIP = ROOT / "team-pack-es-pdfs-v0.4.zip"
GUia_DOCX = ROOT / "guia-tecnica" / "Guia-tecnica-mentores.docx"
GUia_PDF = ROOT / "guia-tecnica" / "Guia-tecnica-mentores.pdf"
RUN_HEADER = "Guía técnica · solo mentores"

BYTE_IDENTICAL = [
    ("cuestionario/Cuestionario-Dataton-24nov-equipos.docx", "0ed244fa80725d0c26ace921c08bf243927ddfa916dd4b8ac989ef13d4ae8a5a"),
    ("cuestionario/Cuestionario-Dataton-24nov-equipos.pdf", "df28f7a25159f7dc516fc171329081a6c86fc75aea3d051bf7cb39debadc503d"),
    ("cuestionario/Cuestionario-ejemplo-Air4U.docx", "c0294707fa982d9eee32626797738d34a3d4dff985cdb352b91b8dcf145dfea6"),
    ("cuestionario/Cuestionario-ejemplo-Air4U.pdf", "ea4bfa7a19bdc0e475268e11ac00d3ac0278305b245ec16e71a100fe40d245da"),
    ("cuestionario/prompts.txt", "e325f2f5e8d60547a5ffd1047dbe241b23e071d2e763e7149f5a77f186424015"),
]

HOJA_WORD_BAG_REF = (
    "hoja-2-flujo-de-datos.pdf",
    "hoja-3-dato-a-valor.pdf",
    "hoja-4-plantilla-tablero.pdf",
    "hoja-4b-ejemplo-air4u.pdf",
    "prompts-ia-v2.pdf",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm_text(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", s.lower(), flags=re.UNICODE)


def pdftotext(pdf: Path) -> str:
    return subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True, check=True).stdout


def docx_paragraph_blobs(doc: Document) -> list[str]:
    blobs: list[str] = []
    for p in doc.paragraphs:
        t = p.text.strip()
        if t:
            blobs.append(norm_text(t))
    for table in doc.tables:
        seen: set[str] = set()
        for row in table.rows:
            for cell in row.cells:
                t = cell.text.strip()
                if not t:
                    continue
                n = norm_text(t)
                if n in seen:
                    continue
                seen.add(n)
                blobs.append(n)
    return blobs


def _pdf_line_norm_variants(raw: str) -> list[str]:
    variants = [norm_text(raw)]
    stripped = raw.strip()
    m = re.match(r"^\d+\.\s+", stripped)
    if m:
        variants.append(norm_text(stripped[m.end() :]))
    if stripped.startswith("•"):
        variants.append(norm_text(stripped.lstrip("•").strip()))
    return variants


def paragraph_check(docx: Path, pdf: Path) -> tuple[list[str], list[str]]:
    doc = Document(docx)
    docx_norm_full = norm_text(
        "\n".join(p.text for p in doc.paragraphs)
        + "\n"
        + "\n".join(
            cell.text
            for table in doc.tables
            for row in table.rows
            for cell in row.cells
        )
    )
    pdf_text = pdftotext(pdf)
    pdf_norm_full = norm_text(pdf_text)
    missing: list[str] = []
    for blob in docx_paragraph_blobs(doc):
        if blob and blob not in pdf_norm_full:
            missing.append(blob[:120])
    extra: list[str] = []
    for line in pdf_text.splitlines():
        raw = line.strip()
        stripped = raw
        if not raw:
            continue
        if raw == RUN_HEADER:
            continue
        if re.fullmatch(r"\d+", raw):
            continue
        if re.fullmatch(r"#+", stripped):
            continue
        if re.fullmatch(r"[_:\s·]+", stripped):
            continue
        if re.match(r"^:\s*_+\s*$", stripped):
            continue
        if any(v and v in docx_norm_full for v in _pdf_line_norm_variants(raw)):
            continue
        extra.append(raw[:120])
    return missing, extra


def contact_sheet(pdf: Path, out: Path, dpi: int = 40) -> None:
    doc = fitz.open(pdf)
    cols = min(5, doc.page_count)
    rows = math.ceil(doc.page_count / cols)
    w = int(8.27 * dpi / 2.54)
    h = int(11.69 * dpi / 2.54)
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


def export_page_png(pdf: Path, page_index: int, out: Path, dpi: int) -> None:
    doc = fitz.open(pdf)
    pix = doc[page_index].get_pixmap(dpi=dpi, alpha=False)
    pix.save(str(out))
    doc.close()


def word_bag_pdf(path: Path) -> Counter:
    doc = fitz.open(path)
    text = "".join(page.get_text() for page in doc)
    doc.close()
    words = re.findall(r"\w+", text.lower(), flags=re.UNICODE)
    return Counter(words)


def docx_paragraph_diff_count(ref_path: bytes, new_path: Path) -> int:
    import io

    base = Document(io.BytesIO(ref_path))
    new = Document(new_path)
    n = 0
    for a, b in zip(base.paragraphs, new.paragraphs):
        if a.text != b.text:
            n += 1
    if len(base.paragraphs) != len(new.paragraphs):
        n += 1
    return n


def prompts_sheet_word_check(prompts_txt: Path, pdf: Path) -> tuple[list[str], list[str]]:
    raw = prompts_txt.read_text(encoding="utf-8")
    pdf_text = pdftotext(pdf)
    def _collapse_ws(s: str) -> str:
        return re.sub(r"\s+", " ", s)

    pdf_norm = _collapse_ws(pdf_text)
    missing = []
    for ln in raw.splitlines():
        t = ln.strip()
        if not t:
            continue
        if _collapse_ws(t) in pdf_norm:
            continue
        # Emoji squares may rasterize; verify prose without emoji glyphs.
        no_emoji = re.sub(r"[\U0001F7E5\U0001F7E7\U0001F7E6]", "", t)
        if _collapse_ws(no_emoji) in _collapse_ws(re.sub(r"[\U0001F7E5\U0001F7E7\U0001F7E6]", "", pdf_text)):
            continue
        missing.append(t)
    allowed_extra = {
        PROMPTS_SHEET_TOP,
        "Inspira. Actúa. Transforma. · CleantechHUB · Datatón 24 nov 2026",
        "Instrucciones de inteligencia artificial",
    }
    extra: list[str] = []
    for line in pdf_text.splitlines():
        t = line.strip()
        if not t or t in allowed_extra:
            continue
        if t in raw:
            continue
        if re.match(r"^\d+$", t):
            continue
        extra.append(t[:120])
    return missing, extra


def pdffonts_ok_open_sans(stdout: str, allow_emoji: bool = False) -> tuple[bool, str]:
    forbidden = ("Helvetica", "DejaVu", "Cascadia", "Arimo", "NotoSans", "Liberation")
    bad: list[str] = []
    for line in stdout.splitlines():
        if not line.strip() or line.startswith("name") or set(line.strip()) == {"-"}:
            continue
        if allow_emoji and "NotoColorEmoji" in line:
            continue
        if any(tok in line for tok in forbidden):
            bad.append(line.split()[0] if line.split() else line[:40])
        if "OpenSans" in line or "Open Sans" in line:
            if " yes " in f" {line} " or line.rstrip().endswith(" yes"):
                continue
        if any(tok in line for tok in forbidden):
            continue
        if "Type 3" in line and allow_emoji:
            continue
    return (len(bad) == 0, "; ".join(bad[:12]))


def pdffonts_ok_guia(stdout: str) -> tuple[bool, str]:
    bad: list[str] = []
    for line in stdout.splitlines():
        if not line.strip() or line.startswith("name") or set(line.strip()) == {"-"}:
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        name, emb = parts[0], parts[1]
        if name.startswith("-") or name == "Open":
            continue
        if emb != "yes":
            bad.append(f"{name} not embedded")
        if "OpenSans" not in name and "Open Sans" not in name:
            bad.append(f"non-OpenSans: {name}")
    return (len(bad) == 0, "; ".join(bad[:12]))


def main() -> int:
    PROOFS.mkdir(parents=True, exist_ok=True)
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=str(REPO), capture_output=True, text=True, check=True
    ).stdout.strip()
    lines: list[str] = ["# Run 8 notes — Guía PDF wording/fonts", "", f"Working head: `{head}`.", ""]

    guia_pdf = GUia_PDF if GUia_PDF.is_file() else OUT / "Guia-tecnica-mentores.pdf"
    missing, extra = paragraph_check(GUia_DOCX, guia_pdf)
    para_path = PROOFS / "paragraph-check.txt"
    para_path.write_text(
        "\n".join(
            [
                f"missing ({len(missing)}):",
                *missing[:100],
                "",
                f"extra ({len(extra)}):",
                *extra[:100],
            ]
        ),
        encoding="utf-8",
    )
    lines.append("## Paragraph check (normalized)")
    lines.append(f"- Missing docx paragraphs in PDF: **{len(missing)}** (expect 0)")
    lines.append(f"- Extra PDF lines vs docx: **{len(extra)}** (expect 0)")
    lines.append(f"- Log: `{para_path.relative_to(ROOT)}`")
    lines.append("")

    proc_pre = subprocess.run(
        ["git", "show", f"{PRE_ADDENDUM_DOCX_REF}:decks/dataton-2026-team-pack/guia-tecnica/Guia-tecnica-mentores.docx"],
        cwd=str(REPO),
        capture_output=True,
        check=True,
    )
    tiebreak_diffs = docx_paragraph_diff_count(proc_pre.stdout, GUia_DOCX)
    lines.append("## Tie-break addendum (docx)")
    lines.append(f"- Guía docx paragraph diffs vs pre-addendum (`73885721`): **{tiebreak_diffs}** (expect 2)")
    lines.append("- Changed paragraphs: M6 finales bullet + Hoja 5 intro (Guía only; team hoja-5.md untouched)")
    lines.append("")

    font_log = PROOFS / "pdffonts.txt"
    chunks: list[str] = []
    for name in ("Guia-tecnica-mentores.pdf", "hoja-4-plantilla-tablero.pdf"):
        p = OUT / name if (OUT / name).is_file() else ROOT / "guia-tecnica" / name
        if name == "hoja-4-plantilla-tablero.pdf":
            p = OUT / name
        r = subprocess.run(["pdffonts", str(p)], capture_output=True, text=True, check=True)
        chunks.append(f"=== {name} ===\n{r.stdout.strip()}\n")
    font_log.write_text("\n".join(chunks), encoding="utf-8")
    guia_r = subprocess.run(["pdffonts", str(guia_pdf)], capture_output=True, text=True, check=True)
    ok_guia, guia_font_detail = pdffonts_ok_open_sans(guia_r.stdout)
    lines.append("## pdffonts")
    lines.append(f"- Guía embedded Open Sans only: **{ok_guia}** ({guia_font_detail or 'ok'})")
    sheet_font_ok = True
    if PROMPTS_IA_SHEET_PDF.is_file():
        sheet_r = subprocess.run(["pdffonts", str(PROMPTS_IA_SHEET_PDF)], capture_output=True, text=True, check=True)
        chunks.append(f"=== Prompts-IA-Dataton-24nov.pdf ===\n{sheet_r.stdout.strip()}\n")
        sheet_font_ok, sheet_detail = pdffonts_ok_open_sans(sheet_r.stdout, allow_emoji=True)
        lines.append(
            f"- Prompts-IA sheet (Open Sans + emoji ok): **{sheet_font_ok}** ({sheet_detail or 'ok'})"
        )
    lines.append(f"- Log: `{font_log.relative_to(ROOT)}`")
    lines.append("")

    p_missing: list[str] = []
    p_extra: list[str] = []
    if PROMPTS_IA_SHEET_PDF.is_file():
        p_missing, p_extra = prompts_sheet_word_check(ROOT / "cuestionario/prompts.txt", PROMPTS_IA_SHEET_PDF)
        (PROOFS / "prompts-sheet-word-check.txt").write_text(
            f"missing ({len(p_missing)}):\n" + "\n".join(p_missing[:50]) + f"\n\nextra ({len(p_extra)}):\n" + "\n".join(p_extra[:50]),
            encoding="utf-8",
        )
        lines.append("## Prompts-IA team sheet word check")
        lines.append(f"- prompts.txt lines missing from PDF: **{len(p_missing)}**")
        lines.append(f"- Extra PDF lines: **{len(p_extra)}**")
        sheet_pdf = fitz.open(PROMPTS_IA_SHEET_PDF)
        for i in range(sheet_pdf.page_count):
            export_page_png(PROMPTS_IA_SHEET_PDF, i, PROOFS / f"prompts-ia-dataton-24nov-p{i + 1:02d}-110dpi.png", dpi=110)
        sheet_pdf.close()
        lines.append(
            f"- PNGs: `{PROOFS.relative_to(ROOT)}/prompts-ia-dataton-24nov-p01-110dpi.png` (+ p02 if present)"
        )
        lines.append("")

    contact_sheet(guia_pdf, PROOFS / "guia-pdf-contact-40dpi.png", dpi=40)
    h4 = OUT / "hoja-4-plantilla-tablero.pdf"
    for i in range(3):
        export_page_png(h4, i, PROOFS / f"hoja-4-plantilla-tablero-p{i + 1:02d}-110dpi.png", dpi=110)
    lines.append("## Contact sheets")
    lines.append(f"- `{PROOFS.relative_to(ROOT)}/guia-pdf-contact-40dpi.png` (40 dpi, all Guía pages)")
    lines.append(f"- `{PROOFS.relative_to(ROOT)}/hoja-4-plantilla-tablero-p01-110dpi.png` (+ p02, p03 @ 110 dpi)")
    lines.append("")

    bag_lines: list[str] = []
    bag_fail = False
    with tempfile.TemporaryDirectory() as td:
        for pdf_name in HOJA_WORD_BAG_REF:
            old_pdf = Path(td) / pdf_name
            proc = subprocess.run(
                ["git", "show", f"{REF_HEAD}:decks/dataton-2026-team-pack/dist/{pdf_name}"],
                cwd=str(REPO),
                capture_output=True,
                check=True,
            )
            old_pdf.write_bytes(proc.stdout)
            b_old = word_bag_pdf(old_pdf)
            b_new = word_bag_pdf(OUT / pdf_name)
            delta = sorted(w for w in set(b_old) | set(b_new) if b_old[w] != b_new[w])
            if pdf_name in ("hoja-2-flujo-de-datos.pdf", "prompts-ia-v2.pdf") and sha256(OUT / pdf_name) != sha256(old_pdf):
                bag_lines.append(f"{pdf_name}: BYTE DRIFT vs {REF_HEAD[:8]}")
                bag_fail = True
            bag_lines.append(f"{pdf_name}: word-bag delta **{len(delta)}**")
            if delta and pdf_name not in ("hoja-2-flujo-de-datos.pdf", "prompts-ia-v2.pdf"):
                bag_fail = True
    (PROOFS / "word-bag.txt").write_text("\n".join(bag_lines), encoding="utf-8")
    lines.append("## Word-bag vs ref head")
    for row in bag_lines:
        lines.append(f"- {row}")
    lines.append("")

    lines.append("## Pinned artifacts")
    lines.append(f"- Guía docx sha256: `{sha256(GUia_DOCX)}`")
    for relpath, expected in BYTE_IDENTICAL:
        actual = sha256(ROOT / relpath)
        lines.append(f"- `{relpath}` byte-identical: **{actual == expected}**")
    lines.append("")

    sums_path = PROOFS / "SHA256SUMS"
    sum_rows = [
        f"{sha256(GUia_DOCX)}  guia-tecnica/Guia-tecnica-mentores.docx",
        f"{sha256(guia_pdf)}  guia-tecnica/Guia-tecnica-mentores.pdf",
        f"{sha256(h4)}  dist/hoja-4-plantilla-tablero.pdf",
        f"{sha256(ZIP)}  team-pack-es-pdfs-v0.4.zip",
    ]
    if PROMPTS_IA_SHEET_DOCX.is_file():
        sum_rows.append(f"{sha256(PROMPTS_IA_SHEET_DOCX)}  dist/Prompts-IA-Dataton-24nov.docx")
    if PROMPTS_IA_SHEET_PDF.is_file():
        sum_rows.append(f"{sha256(PROMPTS_IA_SHEET_PDF)}  dist/Prompts-IA-Dataton-24nov.pdf")
    sums_path.write_text("\n".join(sum_rows) + "\n", encoding="utf-8")
    lines.append("## SHA256SUMS")
    lines.append(f"- Proof: `{sums_path.relative_to(ROOT)}`")
    for row in sum_rows:
        lines.append(f"- `{row}`")
    lines.append("")

    notes = ROOT / "run8-notes.md"
    notes.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(notes)
    tiebreak_docx = tiebreak_diffs
    fail = bool(
        missing
        or extra
        or not ok_guia
        or bag_fail
        or tiebreak_docx != 2
        or p_missing
        or p_extra
        or not sheet_font_ok
    )
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())