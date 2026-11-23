#!/usr/bin/env python3
"""Banned-word audit on rendered PDF text."""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PDF = ROOT / "dataton-preguntas-espacios.pdf"

BANNED = [
    r"\bPR\b",
    r"\bHands\b",
    r"\bOrchestrator\b",
    r"\bOrch\b",
    r"\bCursor\b",
    r"\bdesk\b",
    r"\bGO\b",
    r"\bticket\b",
    r"\bgithub\b",
    r"decks/",
    r"\.md\b",
    r"gratis",
    r"gratuito",
    r"drive\.google",
    r"->",
    r"\bdos\s+mil\b",
    r"\bloop\b",
    r"cit-able",
    r"sin\s+costo",
]


def main() -> int:
    if not PDF.is_file():
        print("PDF missing", file=sys.stderr)
        return 1
    text = subprocess.check_output(["pdftotext", str(PDF), "-"], text=True, errors="replace")
    hits = []
    for pat in BANNED:
        for m in re.finditer(pat, text, re.IGNORECASE):
            line = text[max(0, text.rfind("\n", 0, m.start()) + 1) : text.find("\n", m.start())]
            hits.append((pat, line.strip()[:120]))
    if hits:
        print(f"BANNED HITS: {len(hits)}")
        for pat, line in hits:
            print(f"  [{pat}] {line}")
        return 2
    print("BANNED HITS: 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())