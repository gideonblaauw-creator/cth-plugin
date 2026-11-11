#!/usr/bin/env python3
"""Crop photo regions from Canva 1600x900 exports into assets/canva/."""
from __future__ import annotations

from pathlib import Path

from PIL import Image

SRC_ROOT = Path("/tmp/canva-src/canva-src")
OUT = Path(__file__).resolve().parent / "assets" / "canva"
OUT.mkdir(parents=True, exist_ok=True)


def load(rel: str) -> Image.Image:
    return Image.open(SRC_ROOT / rel).convert("RGB")


def crop_frac(im: Image.Image, box: tuple[float, float, float, float]) -> Image.Image:
    w, h = im.size
    l, t, r, b = box
    return im.crop((int(w * l), int(h * t), int(w * r), int(h * b)))


def save(im: Image.Image, name: str) -> None:
    path = OUT / name
    im.save(path, "JPEG", quality=90, optimize=True)
    print("wrote", path, im.size)


def crop_photo_region(im: Image.Image, side: str = "right") -> Image.Image:
    if side == "right":
        return crop_frac(im, (0.48, 0, 1.0, 1.0))
    if side == "left":
        return crop_frac(im, (0.0, 0, 0.52, 1.0))
    if side == "photos_top":
        return crop_frac(im, (0.0, 0.08, 1.0, 0.92))
    return im


def montage(images: list[Image.Image], cols: int, out_w: int = 920, out_h: int = 1080) -> Image.Image:
    rows = (len(images) + cols - 1) // cols
    cell_w = out_w // cols
    cell_h = out_h // rows
    canvas = Image.new("RGB", (out_w, out_h), (12, 73, 138))
    for i, im in enumerate(images):
        r, c = divmod(i, cols)
        im = Image.Image.resize(im, (cell_w, cell_h), Image.Resampling.LANCZOS)
        canvas.paste(im, (c * cell_w, r * cell_h))
    return canvas


def startup_photo(im: Image.Image) -> Image.Image:
    """Crop hero photo from REIN startup profile slide (left column)."""
    return crop_frac(im, (0.02, 0.18, 0.42, 0.88))


def clp26_photo(im: Image.Image) -> Image.Image:
    """Winner / event slides — use visible crowd strips, avoid center text box."""
    w, h = im.size
    left = crop_frac(im, (0.0, 0.0, 0.38, 1.0))
    right = crop_frac(im, (0.62, 0.0, 1.0, 1.0))
    # stack left and right for collage piece
    piece = Image.new("RGB", (w // 2, h))
    piece.paste(left.resize((w // 4, h)), (0, 0))
    piece.paste(right.resize((w // 4, h)), (w // 4, 0))
    return piece


def main() -> None:
    # Individual crops (used in HTML grids)
    crops: list[tuple[str, str, tuple[float, float, float, float] | str]] = [
        ("corporate/p03.jpg", "cth-speaker-cop16.jpg", (0.5, 0.02, 1.0, 0.98)),
        ("corporate/p18.jpg", "cth-team-graffiti.jpg", (0.0, 0.22, 0.52, 0.95)),
        ("corporate/p17.jpg", "cth-leadership-panel.jpg", (0.12, 0.15, 0.98, 0.92)),
        ("corporate/p21.jpg", "cth-partnership-event.jpg", (0.0, 0.08, 0.38, 0.52)),
        ("rein/p03.jpg", "rein-externado.jpg", (0.48, 0.05, 0.98, 0.95)),
        ("rein/p05.jpg", "rein-pipeline.jpg", (0.0, 0.0, 1.0, 1.0)),
        ("rein/p09.jpg", "rein-program.jpg", (0.0, 0.0, 1.0, 1.0)),
        ("corporate/p22.jpg", "mubon-ev-charge.jpg", (0.02, 0.14, 0.44, 0.58)),
        ("clp26/p02.jpg", "clp26-stage.jpg", (0.42, 0.0, 1.0, 1.0)),
        ("clp26/p06.jpg", "clp26-gideon.jpg", (0.38, 0.05, 1.0, 0.95)),
        ("clp26/p07.jpg", "clp26-crowd.jpg", (0.0, 0.0, 1.0, 1.0)),
        ("clp26/p06.jpg", "clp26-field.jpg", (0.58, 0.04, 1.0, 0.52)),
        ("clp26/p06.jpg", "clp26-forest.jpg", (0.58, 0.48, 1.0, 0.98)),
    ]
    for src, name, box in crops:
        im = load(src)
        if isinstance(box, tuple):
            save(crop_frac(im, box), name)
        else:
            save(im, name)

    for src, name in [
        ("clp26/p47.jpg", "clp26-winner-1.jpg"),
        ("clp26/p48.jpg", "clp26-winner-2.jpg"),
        ("clp26/p49.jpg", "clp26-winner-3.jpg"),
    ]:
        save(clp26_photo(load(src)), name)

    # Success story card photos from p14
    p14 = load("corporate/p14.jpg")
    w = p14.size[0]
    third = w // 3
    for i, (label, x0, x1) in enumerate(
        [
            ("nexus-sunco.jpg", 0.04, 0.35),
            ("nexus-zhana.jpg", 0.36, 0.66),
            ("nexus-glasst.jpg", 0.67, 0.96),
        ]
    ):
        card = crop_frac(p14, (x0, 0.22, x1, 0.58))
        save(card, label)

    rein_startups = [
        ("rein/p13.jpg", "rein-elastic.jpg"),
        ("rein/p14.jpg", "rein-xiclo.jpg"),
        ("rein/p15.jpg", "rein-weia.jpg"),
        ("rein/p16.jpg", "rein-novatio.jpg"),
        ("rein/p17.jpg", "rein-zhana.jpg"),
        ("rein/p18.jpg", "rein-air4u.jpg"),
    ]
    for src, name in rein_startups:
        save(startup_photo(load(src)), name)

    # Pre-built collages for visual panes
    save(
        montage(
            [
                crop_frac(load("corporate/p03.jpg"), (0.5, 0, 1, 1)),
                crop_frac(load("corporate/p18.jpg"), (0, 0.25, 0.55, 1)),
                crop_frac(load("corporate/p21.jpg"), (0, 0.1, 0.4, 0.55)),
            ],
            cols=1,
        ),
        "collage-cth.jpg",
    )
    clp_imgs = [
        crop_frac(load("clp26/p02.jpg"), (0.42, 0, 1, 1)),
        crop_frac(load("clp26/p06.jpg"), (0.35, 0, 1, 1)),
        clp26_photo(load("clp26/p47.jpg")),
        clp26_photo(load("clp26/p48.jpg")),
    ]
    save(montage(clp_imgs, cols=2), "collage-clp26.jpg")

    nexus_imgs = [
        crop_frac(p14, (0.04, 0.22, 0.35, 0.58)),
        crop_frac(p14, (0.36, 0.22, 0.66, 0.58)),
        startup_photo(load("rein/p13.jpg")),
        startup_photo(load("rein/p14.jpg")),
        startup_photo(load("rein/p15.jpg")),
        startup_photo(load("rein/p16.jpg")),
    ]
    save(montage(nexus_imgs, cols=2), "collage-nexus.jpg")

    rein_imgs = [
        crop_frac(load("rein/p03.jpg"), (0.48, 0, 1, 1)),
        startup_photo(load("rein/p13.jpg")),
        startup_photo(load("rein/p14.jpg")),
        startup_photo(load("rein/p17.jpg")),
    ]
    save(montage(rein_imgs, cols=2), "collage-rein.jpg")

    save(crop_frac(load("corporate/p22.jpg"), (0.02, 0.12, 0.5, 0.6)), "collage-p4g-mubon.jpg")


if __name__ == "__main__":
    main()
