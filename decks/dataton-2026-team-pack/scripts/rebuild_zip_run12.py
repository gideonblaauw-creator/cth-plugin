#!/usr/bin/env python3
"""Rebuild zip from run 11 archive, updating only Prompts-IA sheet PDF (run 12)."""
from __future__ import annotations

import hashlib
import io
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent.parent
ZIP = ROOT / "team-pack-es-pdfs-v0.4.zip"
BASE = "59e987145b5ab3e09c2575d64296abdde59057d9"


def main() -> None:
    base = subprocess.check_output(
        ["git", "-C", str(REPO), "show", f"{BASE}:decks/dataton-2026-team-pack/team-pack-es-pdfs-v0.4.zip"]
    )
    pdf = (ROOT / "dist" / "Prompts-IA-Dataton-24nov.pdf").read_bytes()
    with zipfile.ZipFile(io.BytesIO(base)) as zin, zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "Prompts-IA-Dataton-24nov.pdf":
                data = pdf
            zout.writestr(info, data)
    print("zip_sha256", hashlib.sha256(ZIP.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()