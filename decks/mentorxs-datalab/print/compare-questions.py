#!/usr/bin/env python3
"""Diff numbered question labels: Forms markdown vs PDF extract (pdftotext)."""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
md_path = ROOT / "part3-google-forms-question-list.md"
pdf_path = ROOT / "part3-cuestionario-mentor.pdf"

md_items = []
for line in md_path.read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if line and line[0].isdigit() and ". " in line:
        n, text = line.split(". ", 1)
        md_items.append((int(n), text))

text = subprocess.check_output(["pdftotext", "-layout", str(pdf_path), "-"], text=True)
pdf_items = []
for line in text.splitlines():
    m = re.match(r"^(\d+)\.\s+(.+)$", line.strip())
    if m:
        pdf_items.append((int(m.group(1)), m.group(2).strip()))

md_map = dict(md_items)
pdf_map = dict(pdf_items)
all_nums = sorted(set(md_map) | set(pdf_map))
diffs = []
for n in all_nums:
    a = md_map.get(n)
    b = pdf_map.get(n)
    if a != b:
        diffs.append((n, a, b))

print(f"md={len(md_items)} pdf={len(pdf_items)}")
if diffs:
    print("MISMATCHES:")
    for n, a, b in diffs:
        print(f"  {n}:")
        print(f"    md:  {a}")
        print(f"    pdf: {b}")
    sys.exit(1)
print("OK: all 55 labels match (pdftotext line extract)")