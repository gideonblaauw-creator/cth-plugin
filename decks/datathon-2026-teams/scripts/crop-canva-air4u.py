#!/usr/bin/env python3
"""16:9 crops from Canva-cleaned Air4U PNGs → assets/photos/canva-g*-crop.jpg."""
from __future__ import annotations

import os
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "assets" / "photos"
SRC = Path(
    os.environ.get(
        "CANVA_OUT",
        "/opt/cth-decks/archive/air4u-datathon-2026/canva-compare/canva-out",
    )
)
if not SRC.is_dir():
    SRC = REPO / "assets" / "canva-src"

# (source file, crop box x0,y0,x1,y1) on 1080×1350 canvas
CROPS: dict[str, tuple[str, tuple[int, int, int, int]]] = {
    "canva-g2-crop.jpg": ("g2-canva.png", (0, 500, 1080, 1108)),  # slide 6 — technician
    "canva-g3-crop.jpg": ("g3-canva.png", (0, 500, 1080, 1108)),  # slide 1 — Medellín
    "canva-g4-crop.jpg": ("g4-canva.png", (0, 380, 1080, 988)),  # slide 2 — gloved hand
    "canva-g5-crop.jpg": ("g5-canva.png", (0, 680, 1080, 1288)),  # slide 6 — café
    "canva-g6-crop.jpg": ("g6-canva.png", (0, 220, 1080, 828)),  # slide 7 — AHU
    "canva-g7-crop.jpg": ("g7-canva.png", (0, 300, 1080, 908)),  # slide 8 — nurse
}

TARGET_W = 1920
NAVY = (12, 73, 138)


def to_16x9(crop: Image.Image) -> Image.Image:
    w, h = crop.size
    need = 16 / 9
    ar = w / h
    if abs(ar - need) < 0.02:
        return crop
    if ar < need:
        new_w = int(h * need)
        canvas = Image.new("RGB", (new_w, h), NAVY)
        canvas.paste(crop, ((new_w - w) // 2, 0))
        return canvas
    new_h = int(w / need)
    top = (h - new_h) // 2
    return crop.crop((0, top, w, top + new_h))


def save_web(im: Image.Image, path: Path) -> None:
    if im.width != TARGET_W:
        nh = int(im.height * TARGET_W / im.width)
        im = im.resize((TARGET_W, nh), Image.Resampling.LANCZOS)
    for q in (88, 82, 76, 70, 64, 58):
        im.save(path, "JPEG", quality=q, optimize=True, progressive=True)
        if path.stat().st_size <= 400_000:
            print(f"{path.name}: {TARGET_W}x{im.height} q≈{q} bytes={path.stat().st_size}")
            return
    print(f"{path.name}: {path.stat().st_size} bytes (over 400KB)")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    only = os.environ.get("CROP_ONLY")
    crops = CROPS.items()
    if only:
        crops = [(k, v) for k, v in CROPS.items() if k == only]
    for out_name, (src_name, box) in crops:
        src = SRC / src_name
        if not src.is_file():
            print(f"skip {out_name}: missing {src}")
            continue
        im = Image.open(src).convert("RGB")
        crop = to_16x9(im.crop(box))
        save_web(crop, OUT / out_name)
        print(f"  box={box}")


if __name__ == "__main__":
    main()