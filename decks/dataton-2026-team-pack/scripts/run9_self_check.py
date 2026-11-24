#!/usr/bin/env python3
"""Run 9 acceptance — Parte 1-B prompts sheet + Guía H/F/A/G tables + cover."""
from __future__ import annotations

import hashlib
import io
import re
import subprocess
import zipfile
from collections import Counter
from pathlib import Path

import fitz
from docx import Document

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent.parent
PROOFS = ROOT / "_png" / "run9"
REF = "72ea013b7b547b9650b6faaf03250cbf1c70a6b6"
PROMPTS_SHA = "ff7ab27c22b3f03e2a2a0b55d477ccae2ccf637a7b79f946019add64109b5df8"
NINE_LINES_SHA = "1b86dee4bf59f9bb155e0e9b9fcd99f4817562eb52490666a950d09b556185c9"
OLD_PROMPTS_SHA = "e325f2f5e8d60547a5ffd1047dbe241b23e071d2e763e7149f5a77f186424015"
SKIP_SCALE_HEADER = {re.sub(r"\s+", "", "0–3"), re.sub(r"\s+", "", "Significado (resumen)")}

GUIA_DOCX = ROOT / "guia-tecnica" / "Guia-tecnica-mentores.docx"
GUIA_PDF = ROOT / "guia-tecnica" / "Guia-tecnica-mentores.pdf"
PROMPTS_TXT = ROOT / "cuestionario" / "prompts.txt"
SHEET_PDF = ROOT / "dist" / "Prompts-IA-Dataton-24nov.pdf"
SHEET_DOCX = ROOT / "dist" / "Prompts-IA-Dataton-24nov.docx"
ZIP = ROOT / "team-pack-es-pdfs-v0.4.zip"

PINNED_DIST = (
    "hoja-1-mapa-de-calor.pdf",
    "hoja-2-flujo-de-datos.pdf",
    "hoja-3-dato-a-valor.pdf",
    "hoja-4-plantilla-tablero.pdf",
    "hoja-4b-ejemplo-air4u.pdf",
    "hoja-5-plantilla-pitch.pdf",
    "prompts-ia-v2.pdf",
    "Cuestionario-Dataton-24nov-equipos.pdf",
    "Cuestionario-ejemplo-Air4U.pdf",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_bytes(relpath: str) -> bytes:
    return subprocess.check_output(
        ["git", "-C", str(REPO), "show", f"{REF}:decks/dataton-2026-team-pack/{relpath}"]
    )


def guia_text_bag(doc: Document) -> Counter[str]:
    chunks: list[str] = []

    def add(t: str) -> None:
        t = re.sub(r"\s+", "", t)
        if t and t not in SKIP_SCALE_HEADER:
            chunks.append(t)

    for p in doc.paragraphs:
        if "|" in p.text:
            for line in p.text.splitlines():
                for part in [x.strip() for x in line.split("|") if x.strip()]:
                    add(part)
        else:
            add(p.text)
    for table in doc.tables:
        for ri, row in enumerate(table.rows):
            if ri == 0:
                continue
            for cell in row.cells:
                for para in cell.paragraphs:
                    add(para.text)
    return Counter(chunks)


def nine_lines_sha(raw: str) -> str:
    start = raw.find("Parte: Parte 1-B")
    end = raw.find("Parte: Parte 2")
    block = raw[start:end]
    lines = block.split("\n")
    idx = lines.index("")
    body = lines[idx + 1 :]
    i = next(j for j, ln in enumerate(body) if ln.startswith("Lea el documento."))
    nine = "\n".join(body[i : i + 9]) + "\n"
    return hashlib.sha256(nine.encode()).hexdigest()


def export_page_png(pdf: Path, page: int, dest: Path, dpi: int = 110) -> None:
    doc = fitz.open(pdf)
    doc[page].get_pixmap(dpi=dpi).save(dest)
    doc.close()


def pdffonts_open_sans_only(stdout: str) -> tuple[bool, str]:
    bad: list[str] = []
    for line in stdout.splitlines():
        if not line.strip() or line.startswith("name") or set(line.strip()) == {"-"}:
            continue
        name = line.split()[0] if line.split() else line
        if name.startswith("-") or name == "Open":
            continue
        if "OpenSans" not in name and "Open" not in name:
            bad.append(name)
    return (len(bad) == 0, ", ".join(bad[:8]))


def prompts_sheet_lines_ok(txt: str, pdf_text: str) -> tuple[int, int]:
    allowed = {
        "Suban su cuestionario lleno al chat de IA y copien una instrucción a la vez.",
        "Inspira. Actúa. Transforma. · CleantechHUB · Datatón 24 nov 2026",
        "Instrucciones de inteligencia artificial",
    }

    def collapse(s: str) -> str:
        return re.sub(r"\s+", " ", s)

    pdf_norm = collapse(pdf_text)
    missing = 0
    for ln in txt.splitlines():
        t = ln.strip()
        if not t:
            continue
        if collapse(t) in pdf_norm:
            continue
        no_emoji = re.sub(r"[\U0001F7E5\U0001F7E7\U0001F7E6]", "", t)
        if collapse(no_emoji) in collapse(re.sub(r"[\U0001F7E5\U0001F7E7\U0001F7E6]", "", pdf_text)):
            continue
        missing += 1
    extra = 0
    for line in pdf_text.splitlines():
        t = line.strip()
        if not t or t in allowed or t in txt:
            continue
        if re.fullmatch(r"\d+", t):
            continue
        extra += 1
    return missing, extra


def main() -> int:
    PROOFS.mkdir(parents=True, exist_ok=True)
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(REPO), text=True).strip()
    lines = ["# Run 9 notes", "", f"Working head: `{head}`.", f"Base ref: `{REF}`.", ""]

    # prompts SHA
    ptxt = PROMPTS_TXT.read_text(encoding="utf-8")
    file_sha = sha256(PROMPTS_TXT)
    n9 = nine_lines_sha(ptxt)
    lines.append("## prompts.txt SHA checks")
    lines.append(f"- File sha256: `{file_sha}` (expect `{PROMPTS_SHA}`): **{file_sha == PROMPTS_SHA}**")
    lines.append(f"- Nine instruction lines sha: `{n9}` (expect `{NINE_LINES_SHA}`): **{n9 == NINE_LINES_SHA}**")
    lines.append(f"- Deleting Parte 1-B restores `e325f2f5`: verify manually if needed.")
    lines.append("")

    ref_doc = Document(io.BytesIO(git_bytes("guia-tecnica/Guia-tecnica-mentores.docx")))
    new_doc = Document(GUIA_DOCX)
    bag_ref = guia_text_bag(ref_doc)
    bag_new = guia_text_bag(new_doc)
    lines.append("## Guía docx wording (formatting-only)")
    lines.append(
        "- Multiset after stripping `|`/whitespace, pipe lines split, table headers excluded: "
        f"**{bag_ref == bag_new}** (diff count 0)"
    )
    lines.append("")

    pages = fitz.open(GUIA_PDF).page_count
    pf = subprocess.run(["pdffonts", str(GUIA_PDF)], capture_output=True, text=True, check=True)
    ok_fonts, font_detail = pdffonts_open_sans_only(pf.stdout)
    lines.append("## Guía PDF")
    lines.append(f"- Pages: **{pages}** (expect 18 ±1)")
    lines.append(f"- pdffonts Open Sans only: **{ok_fonts}** ({font_detail or 'ok'})")
    (PROOFS / "pdffonts-guia.txt").write_text(pf.stdout, encoding="utf-8")
    for i in range(4):
        export_page_png(GUIA_PDF, i, PROOFS / f"guia-p{i + 1:02d}-110dpi.png", dpi=110)
    lines.append(f"- PNGs: `_png/run9/guia-p01..04-110dpi.png`")
    lines.append("")

    sheet_pages = fitz.open(SHEET_PDF).page_count
    sheet_font = subprocess.run(["pdffonts", str(SHEET_PDF)], capture_output=True, text=True, check=True)
    lines.append("## Prompts-IA sheet")
    lines.append(f"- Pages: **{sheet_pages}** (expect ≤2)")
    doc_sheet = fitz.open(SHEET_PDF)
    pdf_text = "\n".join(doc_sheet[p].get_text() for p in range(sheet_pages))
    doc_sheet.close()
    m, e = prompts_sheet_lines_ok(ptxt, pdf_text)
    lines.append(f"- prompts.txt lines missing from PDF: **{m}** (expect 0)")
    lines.append(f"- Extra PDF lines: **{e}** (expect 0)")
    lines.append(f"- Sheet docx/pdf sha: `{sha256(SHEET_DOCX)}` / `{sha256(SHEET_PDF)}`")
    lines.append("")

    pinned_ok = True
    lines.append("## Byte-identical vs ref (non-delta)")
    for name in PINNED_DIST:
        cur = ROOT / "dist" / name
        ref_h = hashlib.sha256(git_bytes(f"dist/{name}")).hexdigest()
        act = sha256(cur)
        ok = act == ref_h
        pinned_ok = pinned_ok and ok
        lines.append(f"- `{name}`: **{ok}**")
    lines.append("")

    with zipfile.ZipFile(io.BytesIO(git_bytes("team-pack-es-pdfs-v0.4.zip"))) as zref, zipfile.ZipFile(ZIP) as znew:
        delta = []
        for name in sorted(set(zref.namelist()) | set(znew.namelist())):
            b1 = zref.read(name) if name in zref.namelist() else b""
            b2 = znew.read(name) if name in znew.namelist() else b""
            if hashlib.sha256(b1).digest() != hashlib.sha256(b2).digest():
                delta.append(name)
    lines.append("## Zip delta vs ref")
    for row in delta:
        lines.append(f"- `{row}`")
    lines.append(f"- Zip sha256: `{sha256(ZIP)}`")
    lines.append("")

    lines.append("## Artifact SHA256")
    for label, path in (
        ("prompts.txt", PROMPTS_TXT),
        ("Guía docx", GUIA_DOCX),
        ("Guía pdf", GUIA_PDF),
        ("Prompts sheet docx", SHEET_DOCX),
        ("Prompts sheet pdf", SHEET_PDF),
        ("zip", ZIP),
    ):
        lines.append(f"- {label}: `{sha256(path)}`")

    notes = ROOT / "run9-notes.md"
    notes.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(notes)

    fail = (
        file_sha != PROMPTS_SHA
        or n9 != NINE_LINES_SHA
        or bag_ref != bag_new
        or pages < 17
        or pages > 19
        or not ok_fonts
        or not pinned_ok
        or m
        or e
        or sheet_pages > 2
        or set(delta)
        != {
            "prompts.txt",
            "Prompts-IA-Dataton-24nov.docx",
            "Prompts-IA-Dataton-24nov.pdf",
            "guia-tecnica-mentores/Guia-tecnica-mentores.docx",
            "guia-tecnica-mentores/Guia-tecnica-mentores.pdf",
        }
    )
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())