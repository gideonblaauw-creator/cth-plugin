#!/usr/bin/env python3
"""Crop text-free bands from Air4U × Datalab social JPEGs → assets/photos/*-crop.jpg."""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "assets" / "photos"

# Text-free regions only (1080×1350 sources). None = skip file (use navy on slide).
CROPS: dict[str, tuple[int, int, int, int] | None] = {
    "air4u-05.jpg": (0, 0, 1080, 200),
    "air4u-08.jpg": (780, 300, 1080, 980),
    "air4u-13.jpg": None,
    "air4u-04.jpg": (800, 700, 1080, 1150),
    "air4u-11.jpg": (380, 500, 720, 780),
    "air4u-10.jpg": None,
    "air4u-02.jpg": (740, 480, 1060, 880),
}


def main() -> None:
    src_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/air4u-inputs/images")
    OUT.mkdir(parents=True, exist_ok=True)
    min_ar = 1280 / 720
    for name, box in CROPS.items():
        out_name = name.replace(".jpg", "-crop.jpg")
        out_path = OUT / out_name
        if box is None:
            if out_path.is_file():
                out_path.unlink()
            print(f"{out_name}: SKIP (use navy)")
            continue
        src = src_dir / name
        im = Image.open(src).convert("RGB")
        crop = im.crop(box)
        w, h = crop.size
        ar = w / h
        if ar < min_ar:
            new_w = int(h * min_ar)
            pad = (new_w - w) // 2
            canvas = Image.new("RGB", (new_w, h), (12, 73, 138))
            canvas.paste(crop, (pad, 0))
            crop = canvas
        crop.save(out_path, quality=88, optimize=True)
        cw, ch = crop.size
        print(f"{out_name}: box={box} out={cw}x{ch}")


if __name__ == "__main__":
    main()