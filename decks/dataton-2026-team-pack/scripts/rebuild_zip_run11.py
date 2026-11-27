#!/usr/bin/env python3
"""Rebuild team-pack zip from run-10 archive with updated members (run 11)."""
from __future__ import annotations

import hashlib
import io
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent.parent
ZIP = ROOT / "team-pack-es-pdfs-v0.4.zip"
RUN10 = "e95dd3ae55d723de745f6c305fb13781f4a87e03"


def main() -> None:
    base = subprocess.check_output(
        ["git", "-C", str(REPO), "show", f"{RUN10}:decks/dataton-2026-team-pack/team-pack-es-pdfs-v0.4.zip"]
    )
    updates = {
        "guia-tecnica-mentores/Guia-tecnica-mentores.docx": ROOT / "guia-tecnica" / "Guia-tecnica-mentores.docx",
        "Prompts-IA-Dataton-24nov.docx": ROOT / "dist" / "Prompts-IA-Dataton-24nov.docx",
        "Prompts-IA-Dataton-24nov.pdf": ROOT / "dist" / "Prompts-IA-Dataton-24nov.pdf",
        "Cuestionario-Dataton-24nov-equipos.docx": ROOT / "dist" / "Cuestionario-Dataton-24nov-equipos.docx",
        "Cuestionario-Dataton-24nov-equipos.pdf": ROOT / "dist" / "Cuestionario-Dataton-24nov-equipos.pdf",
        "Cuestionario-ejemplo-Air4U.docx": ROOT / "dist" / "Cuestionario-ejemplo-Air4U.docx",
        "Cuestionario-ejemplo-Air4U.pdf": ROOT / "dist" / "Cuestionario-ejemplo-Air4U.pdf",
    }
    with zipfile.ZipFile(io.BytesIO(base)) as zin, zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename in updates:
                data = updates[info.filename].read_bytes()
            zout.writestr(info, data)
    print("zip_sha256", hashlib.sha256(ZIP.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()