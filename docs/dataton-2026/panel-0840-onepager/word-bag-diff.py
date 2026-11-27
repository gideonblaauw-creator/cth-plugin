#!/usr/bin/env python3
"""Word-bag diff: current PDF vs baseline commit PDF (copy unchanged)."""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
BASELINE = "5ac3ed3ced8f9e4cee430b792fb6c6d12a554198"
CURRENT = ROOT / "Panel-0840-Dataton-24nov.pdf"


def word_bag(pdf: pathlib.Path) -> list[str]:
    txt = subprocess.check_output(["pdftotext", str(pdf), "-"], text=True)
    txt = re.sub(r"\s*Observa\.\s*Actúa\.\s*Transforma\.\s*$", "", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt.split() if txt else []


def main() -> int:
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        base_pdf = pathlib.Path(td) / "base.pdf"
        repo = ROOT.parents[2]
        data = subprocess.check_output(
            [
                "git",
                "show",
                f"{BASELINE}:docs/dataton-2026/panel-0840-onepager/Panel-0840-Dataton-24nov.pdf",
            ],
            cwd=repo,
        )
        base_pdf.write_bytes(data)
        bw, cw = word_bag(base_pdf), word_bag(CURRENT)
        if bw == cw:
            print("word-bag diff vs 5ac3ed3c: 0 (match)")
            return 0
        print("word-bag diff vs 5ac3ed3c: MISMATCH")
        print(f"baseline words: {len(bw)}, current words: {len(cw)}")
        import difflib

        for line in difflib.unified_diff(bw, cw, lineterm="", n=1):
            if len(line) > 120:
                continue
            print(line)
        return 1


if __name__ == "__main__":
    sys.exit(main())