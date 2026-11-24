#!/usr/bin/env python3
"""Compare pdftotext words to ticket content block."""
from __future__ import annotations

import difflib
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent


def norm(s: str) -> str:
    s = s.replace("\u00a0", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def words(s: str) -> list[str]:
    return norm(s).split(" ") if norm(s) else []


def main() -> None:
    ticket = (ROOT / "ticket-content.txt").read_text(encoding="utf-8")
    pdf_txt = subprocess.check_output(
        ["pdftotext", str(ROOT / "Panel-0840-Dataton-24nov.pdf"), "-"], text=True
    )
    # Footer tagline is layout chrome, not part of the ticket content block.
    pdf_txt = re.sub(r"\s*Observa\.\s*Actúa\.\s*Transforma\.\s*$", "", pdf_txt)
    tw, pw = words(ticket), words(pdf_txt)
    if tw == pw:
        print("OK: word sequences match")
        return
    print("MISMATCH")
    for i, line in enumerate(difflib.unified_diff(tw, pw, lineterm="", n=2)):
        if i >= 60:
            break
        print(line)


if __name__ == "__main__":
    main()