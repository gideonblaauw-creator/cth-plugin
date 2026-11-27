#!/usr/bin/env python3
"""Run 11 acceptance — zip Guía docx, Prompts-IA footer, questionnaire box pagination."""
from __future__ import annotations

import hashlib
import io
import re
import subprocess
import sys
import zipfile
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent.parent
PROOFS = ROOT / "_png" / "run11"
BASE = "e95dd3ae55d723de745f6c305fb13781f4a87e03"
RUN10_ZIP_SHA = "c4f70884359ea16c1e655f6cd1d11d051a1f6fc16ec09cbc47bb3029a0b99102"
V3_SHA = "4cd248ad16227c7cbd6fc33a5b89548920ab978371525a5e57a5de9b95e2fe6a"
GUIA_DOCX_SHA = "04de6140d4b7ed51cffeeea18ac49948e3efdf5fb98fdb010848eebab3c51b01"

ZIP = ROOT / "team-pack-es-pdfs-v0.4.zip"
SHEET_PDF = ROOT / "dist" / "Prompts-IA-Dataton-24nov.pdf"
SHEET_DOCX = ROOT / "dist" / "Prompts-IA-Dataton-24nov.docx"
PROMPTS = ROOT / "cuestionario" / "prompts.txt"
Q_PDF = ROOT / "cuestionario" / "Cuestionario-Dataton-24nov-equipos.pdf"
Q_EJ_PDF = ROOT / "cuestionario" / "Cuestionario-ejemplo-Air4U.pdf"

AI_MARKER = "INSTRUCCIÓN PARA LA IA (copiar y pegar)"
OPT_MARKER = "INSTRUCCIÓN OPCIONAL PARA LA IA"

BOX_SPECS: tuple[tuple[str, str, str], ...] = (
    ("p0", AI_MARKER, "No agregue grupos de personas ni datos que el equipo no escribió."),
    ("p1", AI_MARKER, "4) Debajo de la tabla:"),
    ("p1b", OPT_MARKER, "No invente datos ni nombres de personas."),
    ("p2", AI_MARKER, "cuatro palabras"),
    ("p3", AI_MARKER, "las tildes"),
    ("p4", AI_MARKER, "sugerencia, validar con su mentor»."),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_bytes(relpath: str, ref: str = BASE) -> bytes:
    return subprocess.check_output(
        ["git", "-C", str(REPO), "show", f"{ref}:decks/dataton-2026-team-pack/{relpath}"]
    )


def docx_all_text(path: Path) -> str:
    from docx import Document

    doc = Document(path)
    parts: list[str] = []
    for p in doc.paragraphs:
        parts.append(p.text)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    parts.append(p.text)
    return "\n".join(parts)


def docx_text_match_base(path: Path, relpath: str) -> bool:
    with __import__("tempfile").NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
        tmp.write(git_bytes(relpath))
        ref = Path(tmp.name)
    try:
        return docx_all_text(ref) == docx_all_text(path)
    finally:
        ref.unlink(missing_ok=True)


def page_texts(pdf: Path) -> list[str]:
    doc = fitz.open(pdf)
    texts = [doc[i].get_text() for i in range(doc.page_count)]
    doc.close()
    return texts


def _norm_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s)


def box_on_single_page(pdf: Path) -> list[tuple[str, int | None, bool]]:
    pages = page_texts(pdf)
    norm_pages = [_norm_ws(t) for t in pages]
    sequence: list[tuple[str, int]] = []
    for page_i, text in enumerate(pages):
        hits: list[tuple[int, str]] = []
        at = 0
        while True:
            idx = text.find(AI_MARKER, at)
            if idx < 0:
                break
            hits.append((idx, "ai"))
            at = idx + len(AI_MARKER)
        idx = text.find(OPT_MARKER)
        if idx >= 0:
            hits.append((idx, "opt"))
        for _, kind in sorted(hits):
            sequence.append((kind, page_i))
    rows: list[tuple[str, int | None, bool]] = []
    seq_i = 0
    for key, _title, tail in BOX_SPECS:
        want = "opt" if key == "p1b" else "ai"
        title_page: int | None = None
        while seq_i < len(sequence):
            kind, pg = sequence[seq_i]
            seq_i += 1
            if kind == want:
                title_page = pg
                break
        if title_page is None:
            rows.append((key, None, False))
            continue
        ok = _norm_ws(tail) in norm_pages[title_page]
        rows.append((key, title_page + 1, ok))
    return rows


def export_page(pdf: Path, page: int, dest: Path) -> None:
    doc = fitz.open(pdf)
    doc[page].get_pixmap(dpi=110).save(dest)
    doc.close()


def zip_entry_shas() -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    with zipfile.ZipFile(ZIP) as zf:
        for name in sorted(zf.namelist()):
            out.append((name, sha256_bytes(zf.read(name))[:8]))
    return out


def main() -> int:
    PROOFS.mkdir(parents=True, exist_ok=True)
    head = subprocess.check_output(["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True).strip()
    lines = ["# Run 11 notes", "", f"Head: `{head}`.", f"Base: `{BASE}`.", ""]

    lines.append("## Ticket")
    lines.append("- `hands-tickets/dataton-teampack-run11-zip-sheet-fix.md` (sha `94eca467` — not in repo clone)")
    lines.append("")

    lines.append("## Fix 1 — zip Guía docx")
    with zipfile.ZipFile(ZIP) as zf:
        guia_docx = sha256_bytes(zf.read("guia-tecnica-mentores/Guia-tecnica-mentores.docx"))
    lines.append(f"- zip Guía docx sha256: `{guia_docx}` (expect `{GUIA_DOCX_SHA}`): **{guia_docx == GUIA_DOCX_SHA}**")
    lines.append(f"- zip sha256: `{sha256(ZIP)}` (run 10 was `{RUN10_ZIP_SHA}`)")
    lines.append("")

    lines.append("## Fix 2 — Prompts-IA sheet footer")
    sheet_pages = fitz.open(SHEET_PDF).page_count
    lines.append(f"- sheet pdf pages: **{sheet_pages}** (expect ≤3)")
    p1 = page_texts(SHEET_PDF)[0]
    footer_ok = "Parte: Parte 2" not in p1
    p2_on_p2 = len(page_texts(SHEET_PDF)) > 1 and "Parte: Parte 2" in page_texts(SHEET_PDF)[1]
    lines.append(f"- Parte 2 not on page 1 (footer clear): **{footer_ok}**")
    lines.append(f"- Parte 2 starts page 2: **{p2_on_p2}**")
    lines.append(f"- sheet docx dist=cuestionario: **{sha256(SHEET_DOCX) == sha256(ROOT / 'cuestionario' / SHEET_DOCX.name)}**")
    for i in range(fitz.open(SHEET_PDF).page_count):
        export_page(SHEET_PDF, i, PROOFS / f"sheet-p{i + 1:02d}-110dpi.png")
    lines.append(f"- prompts.txt pinned: **{sha256(PROMPTS) == V3_SHA}**")
    lines.append(f"- sheet pdf sha256: `{sha256(SHEET_PDF)}`")
    lines.append(f"- sheet docx sha256: `{sha256(SHEET_DOCX)}`")
    lines.append("")

    for label, pdf in (("equipos", Q_PDF), ("ejemplo", Q_EJ_PDF)):
        info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, check=True).stdout
        size = next((ln.split(":", 1)[1].strip() for ln in info.splitlines() if ln.startswith("Page size:")), "")
        lines.append(f"- {label} page size: `{size}` (expect 612 x 792 pts)")
    lines.append("")

    lines.append("## Fix 3 — questionnaire INSTRUCCIÓN boxes (single page each)")
    q_ok = docx_text_match_base(
        ROOT / "cuestionario" / "Cuestionario-Dataton-24nov-equipos.docx",
        "cuestionario/Cuestionario-Dataton-24nov-equipos.docx",
    )
    ej_ok = docx_text_match_base(
        ROOT / "cuestionario" / "Cuestionario-ejemplo-Air4U.docx",
        "cuestionario/Cuestionario-ejemplo-Air4U.docx",
    )
    lines.append(f"- equipos docx text = `{BASE[:8]}`: **{q_ok}**")
    lines.append(f"- ejemplo docx text = `{BASE[:8]}`: **{ej_ok}**")
    for label, pdf in (("equipos", Q_PDF), ("ejemplo", Q_EJ_PDF)):
        n = fitz.open(pdf).page_count
        lines.append(f"- {label} pages: **{n}**")
        box_rows = box_on_single_page(pdf)
        all_ok = True
        for key, pg, ok in box_rows:
            all_ok = all_ok and ok
            lines.append(f"  - box {key}: page **{pg}**, single-page **{ok}**")
        lines.append(f"- {label} all 6 boxes single-page: **{all_ok}**")
        pages_needed = sorted({pg - 1 for _, pg, ok in box_rows if ok and pg})
        for pi in pages_needed:
            export_page(pdf, pi, PROOFS / f"{label}-box-p{pi + 1:02d}-110dpi.png")
    lines.append("")

    lines.append("## Zip listing (per-entry sha256 first 8)")
    for name, digest8 in zip_entry_shas():
        lines.append(f"- `{name}`: `{digest8}`")
    lines.append("")

    diff = subprocess.check_output(
        ["git", "-C", str(REPO), "diff", "--stat", f"{BASE}..HEAD", "--", "decks/dataton-2026-team-pack/"],
        text=True,
    ).strip()
    lines.append("## git diff --stat vs base")
    lines.append("```")
    lines.append(diff or "(empty)")
    lines.append("```")

    (ROOT / "run11-notes.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(ROOT / "run11-notes.md")

    fail = (
        guia_docx != GUIA_DOCX_SHA
        or sha256(PROMPTS) != V3_SHA
        or not q_ok
        or not ej_ok
        or fitz.open(SHEET_PDF).page_count > 3
    )
    for _, pdf in (("equipos", Q_PDF), ("ejemplo", Q_EJ_PDF)):
        for _, _, ok in box_on_single_page(pdf):
            fail = fail or not ok
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())