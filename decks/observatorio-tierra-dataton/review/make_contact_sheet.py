#!/usr/bin/env python3
"""Build contact sheet without ImageMagick montage."""
import sys
from pathlib import Path
from PIL import Image

review = Path(__file__).resolve().parent
slides = [review / f"slide-{i:02d}.png" for i in range(1, 12)]
tile_w, tile_h = 480, 270
cols, rows = 4, 3
gap = 4
canvas = Image.new("RGB", (cols * (tile_w + gap) + gap, rows * (tile_h + gap) + gap), "white")
for i, path in enumerate(slides):
    im = Image.open(path).convert("RGB")
    im = im.resize((tile_w, tile_h), Image.Resampling.LANCZOS)
    c, r = i % cols, i // cols
    x = gap + c * (tile_w + gap)
    y = gap + r * (tile_h + gap)
    canvas.paste(im, (x, y))
out = review / "contact-sheet.png"
canvas.save(out)
print(out)