#!/usr/bin/env python3
"""List PDF text chars missing from OpenSans-Regular.ttf cmap."""
from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent


def load_cmap_chars(ttf_path: pathlib.Path) -> set[str]:
    from fontTools.ttLib import TTFont

    font = TTFont(str(ttf_path))
    cmap = font.getBestCmap() or {}
    return {chr(cp) for cp in cmap.keys()}


def main() -> int:
    pdf = ROOT / "Panel-0840-Dataton-24nov.pdf"
    ttf = ROOT / "fonts" / "OpenSans-Regular.ttf"
    text = subprocess.check_output(["pdftotext", str(pdf), "-"], text=True)
    allowed = load_cmap_chars(ttf)
    missing = sorted(
        {
            ch
            for ch in text
            if ch not in allowed and ch not in "\n\r\t\f\v"
            and not (ord(ch) < 32)
        }
    )
    if missing:
        print("Glyphs outside OpenSans-Regular cmap:")
        for ch in missing:
            print(repr(ch), hex(ord(ch)))
        return 1
    print("(empty) — all pdftotext chars in OpenSans-Regular cmap")
    return 0


if __name__ == "__main__":
    sys.exit(main())