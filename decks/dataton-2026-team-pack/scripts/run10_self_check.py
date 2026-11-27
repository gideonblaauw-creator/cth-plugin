#!/usr/bin/env python3
"""Run 10 acceptance — prompts v3, optional 1-B in questionnaires, Guía PDF tables."""
from __future__ import annotations

import hashlib
import io
import re
import subprocess
import sys
import tempfile
import zipfile
from collections import Counter
from pathlib import Path

import fitz
from docx import Document

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent.parent
PROOFS = ROOT / "_png" / "run10"
RUN9 = "de1999e5259177ab46469e1a90067d3732ff151e"
RUN9_GUia_REF = "72ea013b7b547b9650b6faaf03250cbf1c70a6b6"
V3_SHA = "4cd248ad16227c7cbd6fc33a5b89548920ab978371525a5e57a5de9b95e2fe6a"

PROMPTS = ROOT / "cuestionario" / "prompts.txt"
Q_DOCX = ROOT / "cuestionario" / "Cuestionario-Dataton-24nov-equipos.docx"
Q_EJ_DOCX = ROOT / "cuestionario" / "Cuestionario-ejemplo-Air4U.docx"
Q_PDF = ROOT / "cuestionario" / "Cuestionario-Dataton-24nov-equipos.pdf"
Q_EJ_PDF = ROOT / "cuestionario" / "Cuestionario-ejemplo-Air4U.pdf"
SHEET_DOCX = ROOT / "cuestionario" / "Prompts-IA-Dataton-24nov.docx"
SHEET_PDF = ROOT / "dist" / "Prompts-IA-Dataton-24nov.pdf"
ZIP = ROOT / "team-pack-es-pdfs-v0.4.zip"
GUIA_DOCX = ROOT / "guia-tecnica" / "Guia-tecnica-mentores.docx"
GUIA_PDF = ROOT / "guia-tecnica" / "Guia-tecnica-mentores.pdf"

EXPECTED_ZIP_DELTA = {
    "prompts.txt",
    "Cuestionario-Dataton-24nov-equipos.docx",
    "Cuestionario-Dataton-24nov-equipos.pdf",
    "Cuestionario-ejemplo-Air4U.docx",
    "Cuestionario-ejemplo-Air4U.pdf",
    "Prompts-IA-Dataton-24nov.docx",
    "Prompts-IA-Dataton-24nov.pdf",
    "guia-tecnica-mentores/Guia-tecnica-mentores.pdf",
}

PARTE2_ENTREGAN = (
    "Tarjeta de flujo de su dato principal, nivel de confianza sugerido y un paso para mejorarlo."
)

import importlib.util


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


bc = _load_module("build_cuestionario", ROOT / "cuestionario" / "build-cuestionario.py")
bg = _load_module("build_guia", ROOT / "guia-tecnica" / "build-guia-tecnica-mentores.py")
OPTIONAL_1B_MARKER = bc.OPTIONAL_1B_MARKER
docx_readable_text = bc.docx_readable_text
extract_ai_instruction_bodies = bc.extract_ai_instruction_bodies
extract_parte_1b_optional_body = bc.extract_parte_1b_optional_body
parse_prompts_instruction_blocks = bc.parse_prompts_instruction_blocks
_guia_text_bag = bg._guia_text_bag
_guia_bag_allowed_vs_ref = bg._guia_bag_allowed_vs_ref
_guia_wording_symmetric_diff = bg._guia_wording_symmetric_diff

SKIP_SCALE_HEADER = {
    re.sub(r"\s+", "", "0–3"),
    re.sub(r"\s+", "", "Significado (resumen)"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_bytes(relpath: str, ref: str = RUN9) -> bytes:
    return subprocess.check_output(
        ["git", "-C", str(REPO), "show", f"{ref}:decks/dataton-2026-team-pack/{relpath}"]
    )


def collapse(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def parte_1b_v3_body() -> str:
    raw = PROMPTS.read_text(encoding="utf-8")
    chunks = re.split(r"(?=^Parte: )", raw.strip(), flags=re.MULTILINE)
    for chunk in chunks:
        if "Parte 1-B (opcional)" in chunk.split("\n", 1)[0]:
            lines = chunk.strip().split("\n")
            return "\n".join(lines[lines.index("") + 1 :]).strip()
    raise RuntimeError("v3 Parte 1-B missing")


def bodies_match_v3(extracted: list[str]) -> bool:
    v3 = parse_prompts_instruction_blocks(PROMPTS.read_text(encoding="utf-8"), questionnaire_only=True)
    if len(extracted) != len(v3):
        return False
    return all(collapse(a) == collapse(b) for a, b in zip(extracted, v3))


def parte2_entregan_ok(path: Path) -> bool:
    for table in Document(path).tables:
        for row in table.rows:
            if row.cells[0].text.strip() == "Qué entregan" and PARTE2_ENTREGAN in row.cells[1].text:
                return True
    return False


def _readable_norm(path: Path) -> str:
    text = collapse(docx_readable_text(path))
    text = text.replace(collapse(PARTE2_ENTREGAN), "")
    text = text.replace(collapse("Nivel de confianza sugerido y un paso para mejorarlo."), "")
    return text


def allowed_docx_diffs(path: Path, ref_bytes: bytes) -> tuple[bool, list[str]]:
    bad: list[str] = []
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
        tmp.write(ref_bytes)
        ref_path = Path(tmp.name)
    if _readable_norm(ref_path) != _readable_norm(path):
        bad.append("readable_outside_ai")
    ref_path.unlink(missing_ok=True)
    return len(bad) == 0, bad


def pdffonts_ok(stdout: str, allow_emoji: bool = False) -> tuple[bool, str]:
    bad: list[str] = []
    for line in stdout.splitlines():
        if not line.strip() or line.startswith("name") or set(line.strip()) == {"-"}:
            continue
        name = line.split()[0] if line.split() else ""
        if name.startswith("-") or name == "Open":
            continue
        if allow_emoji and "NotoColorEmoji" in line:
            continue
        if "OpenSans" not in name:
            bad.append(name)
    return len(bad) == 0, ", ".join(bad)


def find_pages_with_text(pdf: Path, needle: str) -> list[int]:
    doc = fitz.open(pdf)
    hits = [i for i in range(doc.page_count) if needle in doc[i].get_text()]
    doc.close()
    return hits


def export_page(pdf: Path, page: int, dest: Path) -> None:
    doc = fitz.open(pdf)
    doc[page].get_pixmap(dpi=110).save(dest)
    doc.close()


def guia_text_ok() -> tuple[bool, str]:
    ref = Document(io.BytesIO(git_bytes("guia-tecnica/Guia-tecnica-mentores.docx", RUN9_GUia_REF)))
    ref_bag = _guia_text_bag(ref)
    new_bag = _guia_text_bag(Document(GUIA_DOCX))
    ok = _guia_bag_allowed_vs_ref(ref_bag, new_bag)
    if ok:
        return True, "only G table split (4 rows + capitals)"
    only_ref, only_new = _guia_wording_symmetric_diff(ref_bag, new_bag)
    return False, f"only_ref={dict(only_ref)} only_new={dict(only_new)}"


def main() -> int:
    PROOFS.mkdir(parents=True, exist_ok=True)
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(REPO), text=True).strip()
    lines = ["# Run 10 notes", "", f"Head: `{head}`.", f"Base: `{RUN9}`.", ""]

    p_sha = sha256(PROMPTS)
    lines.append("## prompts.txt v3 (locked)")
    lines.append(f"- sha256: `{p_sha}` (expect `{V3_SHA}`): **{p_sha == V3_SHA}**")
    lines.append(f"- bytes: **{PROMPTS.stat().st_size}** (expect 7997)")
    lines.append("")

    q_ok = bodies_match_v3(extract_ai_instruction_bodies(Q_DOCX))
    ej_ok = bodies_match_v3(extract_ai_instruction_bodies(Q_EJ_DOCX))
    v3_1b = collapse(parte_1b_v3_body())
    q1b = collapse(extract_parte_1b_optional_body(Q_DOCX))
    ej1b = collapse(extract_parte_1b_optional_body(Q_EJ_DOCX))
    lines.append("## Questionnaire instruction boxes")
    lines.append(f"- equipos Parte 0–4 bodies = v3: **{q_ok}**")
    lines.append(f"- ejemplo Parte 0–4 bodies = v3: **{ej_ok}**")
    lines.append(f"- equipos Parte 1-B optional box = v3: **{q1b == v3_1b}**")
    lines.append(f"- ejemplo Parte 1-B optional box = v3: **{ej1b == v3_1b}**")
    lines.append(f"- Parte 2 Qué entregan: **{parte2_entregan_ok(Q_DOCX) and parte2_entregan_ok(Q_EJ_DOCX)}**")
    lines.append("")

    ok_q, bad_q = allowed_docx_diffs(Q_DOCX, git_bytes("cuestionario/Cuestionario-Dataton-24nov-equipos.docx"))
    ok_ej, bad_ej = allowed_docx_diffs(Q_EJ_DOCX, git_bytes("cuestionario/Cuestionario-ejemplo-Air4U.docx"))
    lines.append("## Docx diff vs run 9 (AI boxes + optional 1-B + Parte 2 entregan only)")
    lines.append(f"- equipos: **{ok_q}** (stray={len(bad_q)})")
    lines.append(f"- ejemplo: **{ok_ej}** (stray={len(bad_ej)})")
    lines.append("")

    pages_guia = fitz.open(GUIA_PDF).page_count
    pipe_hits = 0
    for p in range(3):
        text = subprocess.run(
            ["pdftotext", "-layout", "-f", str(p + 1), "-l", str(p + 1), str(GUIA_PDF), "-"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        pipe_hits += sum(1 for ln in text.splitlines() if ln.lstrip().startswith("| "))
    pf = subprocess.run(["pdffonts", str(GUIA_PDF)], capture_output=True, text=True, check=True)
    ok_guia_fonts, _ = pdffonts_ok(pf.stdout)
    lines.append("## Guía PDF")
    lines.append(f"- pages: **{pages_guia}** (expect 18 ±1)")
    lines.append(f"- pdftotext pp 1–3 lines starting with '|': **{pipe_hits}** (expect 0)")
    lines.append(f"- pdffonts Open Sans only: **{ok_guia_fonts}**")
    guia_ok, guia_detail = guia_text_ok()
    lines.append(f"- docx wording vs `72ea013b`: **{guia_ok}** ({guia_detail})")
    for i in range(2):
        export_page(GUIA_PDF, i + 1, PROOFS / f"guia-p{i + 2:02d}-110dpi.png")
    lines.append("")

    for label, pdf, emoji in (("equipos", Q_PDF, True), ("ejemplo", Q_EJ_PDF, True), ("sheet", SHEET_PDF, True)):
        r = subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True, check=True)
        ok, det = pdffonts_ok(r.stdout, allow_emoji=emoji)
        lines.append(f"- pdffonts {label}: **{ok}** ({det or 'ok'})")

    for prefix, pdf in (("equipos", Q_PDF), ("ejemplo", Q_EJ_PDF)):
        p1 = find_pages_with_text(pdf, "Parte 1. ¿Qué información tienen")
        p1b = find_pages_with_text(pdf, OPTIONAL_1B_MARKER[:40])
        for pi in sorted(set(p1 + p1b)):
            export_page(pdf, pi, PROOFS / f"{prefix}-p{pi + 1:02d}-parte1-110dpi.png")
    sheet = fitz.open(SHEET_PDF)
    for i in range(sheet.page_count):
        export_page(SHEET_PDF, i, PROOFS / f"sheet-p{i + 1:02d}-110dpi.png")
    sheet.close()
    lines.append("")
    lines.append("## PNGs")
    lines.append("- `_png/run10/guia-p02..03-110dpi.png`")
    lines.append("- `_png/run10/*-parte1-110dpi.png` (equipos + ejemplo)")

    pinned = []
    for name in ("hoja-2-flujo-de-datos.pdf", "prompts-ia-v2.pdf"):
        ok = sha256(ROOT / "dist" / name) == hashlib.sha256(git_bytes(f"dist/{name}", RUN9)).hexdigest()
        pinned.append((name, ok))
    guia_docx_pin = sha256(GUIA_DOCX) == hashlib.sha256(
        git_bytes("guia-tecnica/Guia-tecnica-mentores.docx", RUN9)
    ).hexdigest()
    lines.append("")
    lines.append("## Pinned vs run 9 head")
    for name, ok in pinned:
        lines.append(f"- `{name}`: **{ok}**")
    lines.append(f"- Guía docx unchanged from run 9: **{guia_docx_pin}**")

    with zipfile.ZipFile(io.BytesIO(git_bytes("team-pack-es-pdfs-v0.4.zip"))) as zref, zipfile.ZipFile(ZIP) as znew:
        delta = [
            n
            for n in sorted(set(zref.namelist()) | set(znew.namelist()))
            if hashlib.sha256(zref.read(n) if n in zref.namelist() else b"").digest()
            != hashlib.sha256(znew.read(n) if n in znew.namelist() else b"").digest()
        ]
    lines.append("")
    lines.append("## Zip delta vs run 9")
    lines.append(f"- members: {delta}")
    lines.append(f"- zip sha256: `{sha256(ZIP)}`")

    lines.append("")
    lines.append("## SHA256 (changed)")
    for label, path in [
        ("prompts.txt", PROMPTS),
        ("equipos docx", Q_DOCX),
        ("equipos pdf", Q_PDF),
        ("ejemplo docx", Q_EJ_DOCX),
        ("ejemplo pdf", Q_EJ_PDF),
        ("sheet docx", SHEET_DOCX),
        ("sheet pdf", SHEET_PDF),
        ("Guía pdf", GUIA_PDF),
        ("zip", ZIP),
    ]:
        lines.append(f"- {label}: `{sha256(path)}`")

    (ROOT / "run10-notes.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(ROOT / "run10-notes.md")

    fail = (
        p_sha != V3_SHA
        or not q_ok
        or not ej_ok
        or q1b != v3_1b
        or ej1b != v3_1b
        or not ok_q
        or not ok_ej
        or pipe_hits != 0
        or not ok_guia_fonts
        or pages_guia < 17
        or pages_guia > 19
        or not guia_ok
        or set(delta) != EXPECTED_ZIP_DELTA
    )
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())