#!/usr/bin/env python3
"""Crop PURE photo regions from Canva 1600x900 exports (no slide typography)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image

SRC_ROOT = Path("/tmp/canva-src/canva-src")
OUT = Path(__file__).resolve().parent / "assets" / "canva"
HERO_OUT = Path(__file__).resolve().parent / "assets" / "heroes"
OUT.mkdir(parents=True, exist_ok=True)
HERO_OUT.mkdir(parents=True, exist_ok=True)
HERO_W, HERO_H = 1920, 640


def load(rel: str) -> Image.Image:
    p = SRC_ROOT / rel
    if not p.is_file():
        raise SystemExit(f"missing source {p}")
    return Image.open(p).convert("RGB")


def crop_frac(im: Image.Image, box: tuple[float, float, float, float]) -> Image.Image:
    w, h = im.size
    l, t, r, b = box
    return im.crop((int(w * l), int(h * t), int(w * r), int(h * b)))


def save(im: Image.Image, name: str) -> None:
    path = OUT / name
    im.save(path, "JPEG", quality=90, optimize=True)
    print("wrote", path, im.size)


def card_photo(im: Image.Image, x0: float, x1: float) -> Image.Image:
    return crop_frac(im, (x0, 0.27, x1, 0.515))


def rein_hero(im: Image.Image) -> Image.Image:
    return crop_frac(im, (0.03, 0.30, 0.36, 0.72))


def cover_fit(im: Image.Image, tw: int = HERO_W, th: int = HERO_H) -> Image.Image:
    w, h = im.size
    scale = max(tw / w, th / h)
    nw, nh = int(w * scale), int(h * scale)
    im = im.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - tw) // 2, (nh - th) // 2
    return im.crop((left, top, left + tw, top + th))


def save_hero(im: Image.Image, name: str) -> None:
    path = HERO_OUT / name
    im.save(path, "JPEG", quality=88, optimize=True)
    print("wrote", path, im.size)


def main() -> None:
    crops: list[tuple[str, str, tuple[float, float, float, float]]] = [
        # corporate — photo halves / event shots only
        ("corporate/p03.jpg", "cth-speaker-cop16.jpg", (0.54, 0.03, 0.99, 0.98)),
        ("corporate/p18.jpg", "cth-team-graffiti.jpg", (0.02, 0.38, 0.50, 0.97)),
        ("clp26/p02.jpg", "clp26-stage.jpg", (0.46, 0.0, 1.0, 1.0)),
        ("clp26/p06.jpg", "clp26-field.jpg", (0.62, 0.06, 0.99, 0.50)),
        ("clp26/p06.jpg", "clp26-forest.jpg", (0.62, 0.52, 0.99, 0.98)),
        ("clp26/p07.jpg", "clp26-audience.jpg", (0.40, 0.05, 1.0, 0.95)),
        ("rein/p03.jpg", "rein-externado.jpg", (0.52, 0.12, 0.98, 0.96)),
        ("corporate/p22.jpg", "mubon-ev-charge.jpg", (0.08, 0.36, 0.34, 0.58)),
    ]
    for src, name, box in crops:
        save(crop_frac(load(src), box), name)

    p14 = load("corporate/p14.jpg")
    for x0, x1, name in (
        (0.05, 0.34, "nexus-sunco.jpg"),
        (0.36, 0.65, "nexus-zhana.jpg"),
        (0.66, 0.95, "nexus-glasst.jpg"),
    ):
        save(card_photo(p14, x0, x1), name)

    for src, name in [
        ("rein/p13.jpg", "rein-elastic.jpg"),
        ("rein/p14.jpg", "rein-xiclo.jpg"),
        ("rein/p15.jpg", "rein-weia.jpg"),
        ("rein/p16.jpg", "rein-novatio.jpg"),
        ("rein/p18.jpg", "rein-air4u.jpg"),
    ]:
        save(rein_hero(load(src)), name)

    hero_jobs: list[tuple[str, tuple[float, float, float, float], str]] = [
        ("corporate/p03.jpg", (0.54, 0.03, 0.99, 0.98), "hero-cth.jpg"),
        ("clp26/p07.jpg", (0.40, 0.05, 1.0, 0.95), "hero-clp26.jpg"),
        ("clp26/p06.jpg", (0.62, 0.06, 0.99, 0.50), "hero-solar-field.jpg"),
        ("rein/p03.jpg", (0.52, 0.12, 0.98, 0.96), "hero-rein.jpg"),
        ("corporate/p22.jpg", (0.08, 0.36, 0.34, 0.58), "hero-ev.jpg"),
    ]
    root = Path(__file__).resolve().parent / "assets"
    save_hero(cover_fit(Image.open(root / "hero.jpg").convert("RGB")), "hero-tierra-grata.jpg")
    for src, box, name in hero_jobs:
        save_hero(cover_fit(crop_frac(load(src), box)), name)


if __name__ == "__main__":
    main()
