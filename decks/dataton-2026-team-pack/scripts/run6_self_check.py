#!/usr/bin/env python3
"""Run 6 self-checks for dataton team pack placeholder fix."""
from __future__ import annotations

import difflib
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dist"
PNG_RUN6 = ROOT / "_png" / "run6"
BASELINE = "c1ee80a66d83c897838832f6bcd27cc6ed504d57"
PACK_PREFIX = "decks/dataton-2026-team-pack"
OFL = ROOT / "fonts" / "open-sans" / "OpenSans-Regular.ttf"
WHITESPACE = {9, 10, 11, 12, 13, 32, 160, 0x202F, 0x2003}
ALLOWED_EMOJI = {0x1F7E5, 0x1F7E7, 0x1F7E6}
ZIP = ROOT / "team-pack-es-pdfs-v0.4.zip"

BYTE_IDENTICAL = [
    ("cuestionario/Cuestionario-Dataton-24nov-equipos.docx", "0ed244fa80725d0c26ace921c08bf243927ddfa916dd4b8ac989ef13d4ae8a5a"),
    ("cuestionario/Cuestionario-Dataton-24nov-equipos.pdf", "df28f7a25159f7dc516fc171329081a6c86fc75aea3d051bf7cb39debadc503d"),
    ("cuestionario/Cuestionario-ejemplo-Air4U.docx", "c0294707fa982d9eee32626797738d34a3d4dff985cdb352b91b8dcf145dfea6"),
    ("cuestionario/Cuestionario-ejemplo-Air4U.pdf", "ea4bfa7a19bdc0e475268e11ac00d3ac0278305b245ec16e71a100fe40d245da"),
    ("guia-tecnica/Guia-tecnica-mentores.docx", "443a9fffa0465aaa9c8434a4f2d78c5a33d355dcd068b4a6f807717f436c91fe"),
    ("guia-tecnica/Guia-tecnica-mentores.pdf", "c680b8a268f45e58e6047c319af9ae7af5f9127ce94a845f42c7a52642656ac6"),
    ("cuestionario/prompts.txt", "e325f2f5e8d60547a5ffd1047dbe241b23e071d2e763e7149f5a77f186424015"),
]

HOJA_TEXT_NEEDLES = {
    "hoja-3-dato-a-valor.pdf": ("LÍNEA BASE", "DELTA", "PAISAJE", "[N1]", "nota breve"),
    "hoja-4-plantilla-tablero.pdf": (
        "Delta: donde el dato se vuelve valor",
        "entradas › salida › línea valor",
        "Línea base del cliente (entrada)",
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pdftotext(pdf: Path) -> str:
    return subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True, check=True).stdout


def baseline_pdftotext(name: str) -> str:
    git_path = f"{PACK_PREFIX}/dist/{name}"
    repo = ROOT.parent.parent
    with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
        proc = subprocess.run(
            ["git", "show", f"{BASELINE}:{git_path}"],
            cwd=str(repo),
            capture_output=True,
            check=True,
        )
        tmp.write(proc.stdout)
        tmp.flush()
        return pdftotext(Path(tmp.name))


def glyph_scan(text: str, cmap: dict[int, str]) -> list[tuple[int, str]]:
    bad: list[tuple[int, str]] = []
    for ch in text:
        code = ord(ch)
        if code in WHITESPACE or code in ALLOWED_EMOJI:
            continue
        if code not in cmap:
            bad.append((code, ch))
    return bad


def main() -> int:
    lines: list[str] = []
    lines.append("# Run 6 notes — placeholder table fix")
    lines.append("")
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=str(ROOT.parent.parent),
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    lines.append(f"Start SHA (ticket): `{BASELINE}`. Working head: `{head}`.")
    lines.append("")
    lines.append("## Build")
    lines.append(
        "- `build-pack.py`: HTML table expansion for `CTH_*_TABLE_INSERT` before `markdown.markdown()`; "
        "`audit_no_table_insert_tokens()`; `enforce_byte_identical_artifacts()` from baseline."
    )
    lines.append(
        "- Non-hoja `dist/*.pdf` binaries restored from baseline after render when pdftotext is unchanged "
        "(zip rebuilt with only hoja-3/4 PDF deltas)."
    )
    lines.append("")

    # Token audit hoja-3/4
    lines.append("## pdftotext hoja-3 / hoja-4")
    for name in ("hoja-3-dato-a-valor.pdf", "hoja-4-plantilla-tablero.pdf"):
        text = pdftotext(OUT / name)
        tokens = len(re.findall(r"_TABLE_INSERT|CTH_\w+_INSERT", text))
        lines.append(f"- `{name}`: token matches **{tokens}** (expect 0)")
        for needle in HOJA_TEXT_NEEDLES[name]:
            ok = needle in text
            lines.append(f"  - contains `{needle}`: **{ok}**")

    # Text diff dist PDFs vs baseline
    lines.append("")
    lines.append("## Text diff vs c1ee80a (pdftotext lines)")
    changed_others: list[str] = []
    hoja_diffs: dict[str, int] = {}
    for pdf in sorted(OUT.glob("*.pdf")):
        new_lines = pdftotext(pdf).splitlines()
        try:
            old_lines = baseline_pdftotext(pdf.name).splitlines()
        except subprocess.CalledProcessError:
            lines.append(f"- `{pdf.name}`: **no baseline in git**")
            continue
        diff = list(difflib.unified_diff(old_lines, new_lines, lineterm=""))
        if pdf.name.startswith("hoja-3") or pdf.name.startswith("hoja-4-plantilla"):
            hoja_diffs[pdf.name] = len([d for d in diff if d.startswith("+") or d.startswith("-")])
            lines.append(f"- `{pdf.name}`: **{hoja_diffs[pdf.name]}** diff lines (expect table swap only)")
        elif diff:
            changed_others.append(pdf.name)
            lines.append(f"- `{pdf.name}`: **FAIL** {len(diff)} diff lines")
        else:
            lines.append(f"- `{pdf.name}`: **0** changed lines")

    # pdffonts
    lines.append("")
    lines.append("## pdffonts hoja-3 / hoja-4")
    for name in ("hoja-3-dato-a-valor.pdf", "hoja-4-plantilla-tablero.pdf"):
        r = subprocess.run(["pdffonts", str(OUT / name)], capture_output=True, text=True, check=True)
        lines.append(f"### {name}")
        lines.append("```")
        lines.append(r.stdout.strip())
        lines.append("```")

    # Glyph scan
    lines.append("")
    lines.append("## Glyph scan (OpenSans-Regular cmap)")
    cmap = TTFont(OFL).getBestCmap()
    all_bad: list[str] = []
    for name in ("hoja-3-dato-a-valor.pdf", "hoja-4-plantilla-tablero.pdf"):
        for i, page in enumerate(pdftotext(OUT / name).split("\f"), 1):
            bad = glyph_scan(page, cmap)
            if bad:
                all_bad.append(f"{name} p{i}: {bad[:5]}")
    if all_bad:
        lines.append("FAIL:\n" + "\n".join(f"- {x}" for x in all_bad))
    else:
        lines.append("Result: **0** out-of-cmap glyphs in hoja-3/hoja-4 text (except emoji + whitespace).")

    # Pages
    lines.append("")
    lines.append("## pdfinfo pages")
    for name in ("hoja-3-dato-a-valor.pdf", "hoja-4-plantilla-tablero.pdf"):
        r = subprocess.run(["pdfinfo", str(OUT / name)], capture_output=True, text=True, check=True)
        pages = next((ln for ln in r.stdout.splitlines() if ln.startswith("Pages:")), "?")
        lines.append(f"- `{name}`: {pages.strip()}")

    # PNG run6
    lines.append("")
    lines.append("## PNG _png/run6/ (110 dpi)")
    for png in sorted(PNG_RUN6.glob("*.png")):
        lines.append(f"- `{png.relative_to(ROOT)}` sha256 `{sha256(png)}`")

    # Zip
    lines.append("")
    lines.append("## Zip")
    lines.append(f"- `{ZIP.name}` sha256 `{sha256(ZIP)}`")
    lines.append("")
    lines.append("| zip entry | sha256 |")
    lines.append("|---|---|")
    with zipfile.ZipFile(ZIP) as zf:
        for name in sorted(zf.namelist()):
            digest = hashlib.sha256(zf.read(name)).hexdigest()
            lines.append(f"| {name} | `{digest}` |")

    # Byte-identical
    lines.append("")
    lines.append("## Byte-identical confirmations (vs ticket)")
    fonts_sums = (ROOT / "fonts/open-sans/SHA256SUMS").read_text(encoding="utf-8")
    baseline_fonts = subprocess.run(
        ["git", "show", f"{BASELINE}:{PACK_PREFIX}/fonts/open-sans/SHA256SUMS"],
        cwd=str(ROOT.parent.parent),
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    fonts_ok = fonts_sums == baseline_fonts
    lines.append(f"- fonts/open-sans/SHA256SUMS unchanged: **{fonts_ok}**")
    for relpath, expected in BYTE_IDENTICAL:
        actual = sha256(ROOT / relpath)
        ok = actual == expected
        lines.append(f"- `{relpath}`: **{ok}** (`{actual}`)")

    # Key dist shas
    lines.append("")
    lines.append("## Key dist sha256")
    for name in sorted(OUT.glob("*.pdf")):
        lines.append(f"- `dist/{name.name}`: `{sha256(name)}`")

    out_path = ROOT / "run6-notes.md"
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out_path)
    fail = bool(changed_others)
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())