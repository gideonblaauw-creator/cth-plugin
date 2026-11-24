#!/usr/bin/env python3
"""Run 13 — Prompts-IA sheet headings without duplicate 'Parte:' prefix."""
from __future__ import annotations

import hashlib
import io
import subprocess
import sys
import zipfile
from pathlib import Path

import fitz
from docx import Document

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent.parent
PROOFS = ROOT / "_png" / "run13"
BASE = "263d7e6fc609981b25735bb78f31c2a3b41ae1ad"
RUN12_ZIP_SHA = "02148d153f243ade2d614d126e9358706624e829fa47883c55c79e27ddb7c610"
V3_SHA = "4cd248ad16227c7cbd6fc33a5b89548920ab978371525a5e57a5de9b95e2fe6a"

ZIP = ROOT / "team-pack-es-pdfs-v0.4.zip"
SHEET_PDF = ROOT / "dist" / "Prompts-IA-Dataton-24nov.pdf"
SHEET_C = ROOT / "cuestionario" / "Prompts-IA-Dataton-24nov.pdf"
SHEET_DOCX = ROOT / "dist" / "Prompts-IA-Dataton-24nov.docx"
PROMPTS = ROOT / "cuestionario" / "prompts.txt"

EXPECTED_HEADINGS = (
    "Parte 0. Su proyecto en una página",
    "Parte 1. ¿Qué información tienen y dónde está?",
    "Parte 1-B (opcional)",
    "Parte 2. ¿Cómo nace un dato y qué tan confiable es?",
    "Parte 3. ¿Qué decisión ayudan a tomar?",
    "Parte 4. Su pitch de 5 minutos",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_bytes(relpath: str, ref: str = BASE) -> bytes:
    return subprocess.check_output(
        ["git", "-C", str(REPO), "show", f"{ref}:decks/dataton-2026-team-pack/{relpath}"]
    )


def pdffonts_ok(stdout: str) -> tuple[bool, str]:
    bad: list[str] = []
    for line in stdout.splitlines():
        if not line.strip() or line.startswith("name") or set(line.strip()) == {"-"}:
            continue
        name = line.split()[0]
        if name.startswith("-") or name == "Open":
            continue
        if "NotoColorEmoji" in line:
            continue
        if "OpenSans" not in name:
            bad.append(name)
    return len(bad) == 0, ", ".join(bad)


def export_page(pdf: Path, page: int, dest: Path) -> None:
    doc = fitz.open(pdf)
    doc[page].get_pixmap(dpi=110).save(dest)
    doc.close()


def docx_text(path: Path) -> str:
    doc = Document(path)
    parts: list[str] = []
    for p in doc.paragraphs:
        parts.append(p.text)
    return "\n".join(parts)


def zip_delta_members() -> list[str]:
    ref = zipfile.ZipFile(io.BytesIO(git_bytes("team-pack-es-pdfs-v0.4.zip")))
    with ref, zipfile.ZipFile(ZIP) as new:
        delta = []
        for name in sorted(set(ref.namelist()) | set(new.namelist())):
            b1 = ref.read(name) if name in ref.namelist() else b""
            b2 = new.read(name) if name in new.namelist() else b""
            if hashlib.sha256(b1).digest() != hashlib.sha256(b2).digest():
                delta.append(name)
    ref.close()
    return delta


def main() -> int:
    PROOFS.mkdir(parents=True, exist_ok=True)
    head = subprocess.check_output(["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True).strip()
    lines = ["# Run 13 notes", "", f"Head: `{head}`.", f"Base: `{BASE}`.", ""]
    lines.append("## Ticket")
    lines.append("- hands-tickets/dataton-teampack-run13-sheet-heading-prefix.md (sha `eb3b999a` — not in repo clone)")
    lines.append("")

    pdf_text = fitz.open(SHEET_PDF)
    full_pdf = "\n".join(pdf_text[i].get_text() for i in range(pdf_text.page_count))
    pdf_text.close()
    dx = docx_text(SHEET_DOCX)
    grep_docx = dx.count("Parte: ")
    grep_pdf = full_pdf.count("Parte: ")
    lines.append("## Heading prefix fix")
    lines.append(f"- grep 'Parte: ' in docx: **{grep_docx}** (expect 0)")
    lines.append(f"- grep 'Parte: ' in pdf text: **{grep_pdf}** (expect 0)")
    for h in EXPECTED_HEADINGS:
        lines.append(f"- printed heading: **{h in full_pdf and h in dx}** — `{h}`")
    lines.append("")

    pf = subprocess.run(["pdffonts", str(SHEET_PDF)], capture_output=True, text=True, check=True)
    ok_fonts, det = pdffonts_ok(pf.stdout)
    (PROOFS / "pdffonts-sheet.txt").write_text(pf.stdout, encoding="utf-8")
    pages = fitz.open(SHEET_PDF).page_count
    p2 = "Parte 2. ¿Cómo nace un dato" in fitz.open(SHEET_PDF)[1].get_text()
    lines.append("## Layout (unchanged from run 12)")
    lines.append(f"- pages: **{pages}** (expect 3)")
    lines.append(f"- pdffonts Open Sans + emoji: **{ok_fonts}** ({det or 'ok'})")
    lines.append(f"- Parte 2 starts on page 2: **{p2}**")
    lines.append(f"- sheet pdf sha256: `{sha256(SHEET_PDF)}`")
    lines.append(f"- sheet docx sha256: `{sha256(SHEET_DOCX)}`")
    lines.append(f"- cuestionario/dist pdf identical: **{sha256(SHEET_C) == sha256(SHEET_PDF)}**")
    lines.append(f"- cuestionario/dist docx identical: **{sha256(ROOT / 'cuestionario' / SHEET_DOCX.name) == sha256(SHEET_DOCX)}**")
    lines.append(f"- prompts.txt pinned: **{sha256(PROMPTS) == V3_SHA}**")
    lines.append("")

    for i in range(pages):
        export_page(SHEET_PDF, i, PROOFS / f"sheet-p{i + 1:02d}-110dpi.png")

    lines.append("## Zip vs run 12 (`02148d15`)")
    lines.append(f"- zip sha256: `{sha256(ZIP)}` (was `{RUN12_ZIP_SHA}`)")
    delta = zip_delta_members()
    lines.append(f"- delta members: `{delta}`")
    with zipfile.ZipFile(ZIP) as zf:
        for name in sorted(zf.namelist()):
            lines.append(f"- `{name}`: `{hashlib.sha256(zf.read(name)).hexdigest()[:8]}`")
    lines.append("")

    diff = subprocess.check_output(
        ["git", "-C", str(REPO), "diff", "--stat", f"{BASE}..HEAD", "--", "decks/dataton-2026-team-pack/"],
        text=True,
    ).strip()
    lines.append("## git diff --stat vs base")
    lines.append("```")
    lines.append(diff or "(empty)")
    lines.append("```")

    (ROOT / "run13-notes.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(ROOT / "run13-notes.md")

    headings_ok = all(h in full_pdf and h in dx for h in EXPECTED_HEADINGS)
    fail = (
        grep_docx != 0
        or grep_pdf != 0
        or not headings_ok
        or not ok_fonts
        or pages != 3
        or not p2
        or sha256(PROMPTS) != V3_SHA
        or sha256(SHEET_C) != sha256(SHEET_PDF)
        or delta != ["Prompts-IA-Dataton-24nov.docx", "Prompts-IA-Dataton-24nov.pdf"]
    )
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())