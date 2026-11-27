#!/usr/bin/env python3
"""Contact sheet from v6 REVIEW PDF pages."""
from __future__ import annotations

import subprocess
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    subprocess.check_call(["pip", "install", "pypdf", "-q"])
    from pypdf import PdfReader

from PIL import Image

review = Path(__file__).resolve().parent
deck = review.parent
pdf = deck / "ZidiCircle-MEG-Gideon-Blaauw-MubOn-1Dec2026-v6-REVIEW.pdf"
if not pdf.exists():
    pdf = deck / "zidi-meg-2026-12-01.pdf"

prefix = review / "pdf-page"
reader = PdfReader(str(pdf))
n = len(reader.pages)
paths = []
for i in range(1, n + 1):
    out = review / f"pdf-page-{i:02d}.png"
    paths.append(out)

# Render with pdftoppm if pages missing
if not paths or not paths[0].exists():
    subprocess.run(
        [
            "pdftoppm",
            "-png",
            "-r",
            "120",
            str(pdf),
            str(review / "pdf-page"),
        ],
        check=True,
    )
    paths = sorted(review.glob("pdf-page-*.png"))

tile_w, tile_h = 480, 270
cols = 4
rows = (len(paths) + cols - 1) // cols
gap = 4
canvas = Image.new(
    "RGB",
    (cols * (tile_w + gap) + gap, rows * (tile_h + gap) + gap),
    "white",
)
for i, path in enumerate(paths):
    im = Image.open(path).convert("RGB")
    im = im.resize((tile_w, tile_h), Image.Resampling.LANCZOS)
    c, r = i % cols, i // cols
    x = gap + c * (tile_w + gap)
    y = gap + r * (tile_h + gap)
    canvas.paste(im, (x, y))
out = review / "contact-sheet.png"
canvas.save(out)
print(out, f"({len(paths)} tiles)")