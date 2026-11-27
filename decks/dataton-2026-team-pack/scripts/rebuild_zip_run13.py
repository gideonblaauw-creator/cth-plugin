#!/usr/bin/env python3
"""Rebuild zip from run 12 head, updating only Prompts-IA sheet docx+pdf (run 13)."""
from __future__ import annotations

import hashlib
import io
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent.parent
ZIP = ROOT / "team-pack-es-pdfs-v0.4.zip"
BASE = "263d7e6fc609981b25735bb78f31c2a3b41ae1ad"


def main() -> None:
    base = subprocess.check_output(
        ["git", "-C", str(REPO), "show", f"{BASE}:decks/dataton-2026-team-pack/team-pack-es-pdfs-v0.4.zip"]
    )
    updates = {
        "Prompts-IA-Dataton-24nov.docx": ROOT / "dist" / "Prompts-IA-Dataton-24nov.docx",
        "Prompts-IA-Dataton-24nov.pdf": ROOT / "dist" / "Prompts-IA-Dataton-24nov.pdf",
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