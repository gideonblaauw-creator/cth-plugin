#!/usr/bin/env python3
"""Near-white pixel ratio for screenshot QA."""
import sys
from PIL import Image

path = sys.argv[1]
y0 = int(sys.argv[2]) if len(sys.argv) > 2 else 0
y1 = int(sys.argv[3]) if len(sys.argv) > 3 else None

im = Image.open(path).convert("RGB")
w, h = im.size
if y1 is None:
    y1 = h
pixels = im.crop((0, y0, w, min(y1, h))).getdata()
total = 0
near = 0
for r, g, b in pixels:
    total += 1
    if r > 245 and g > 245 and b > 245:
        near += 1
print(near / total if total else 1.0)