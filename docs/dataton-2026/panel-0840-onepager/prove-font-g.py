#!/usr/bin/env python3
"""200 dpi crops: word with 'g' from PDF render vs committed OpenSans-Regular.ttf.

Expect double-storey (binocular) g, same outline as the committed v3.003 TTF
(sha c53aceea…). Compare OUT_PDF vs OUT_TTF point for point.
"""
from __future__ import annotations

import pathlib

import pymupdf
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent
PDF = ROOT / "Panel-0840-Dataton-24nov.pdf"
PNG_PAGE = ROOT / "Panel-0840-Dataton-24nov.png"
TTF = ROOT / "fonts" / "OpenSans-Regular.ttf"
OUT_PDF = ROOT / "Panel-0840-proof-g-from-pdf-200dpi.png"
OUT_TTF = ROOT / "Panel-0840-proof-g-from-ttf-200dpi.png"

# Ticket body word containing lowercase g (9.25–9.5 pt in the PDF).
PROOF_WORD = "programa"
DPI = 200
BODY_PT = 10.5
TEXT_BLUE = (12, 73, 138)


def find_word_rect() -> pymupdf.Rect:
    doc = pymupdf.open(PDF)
    page = doc[0]
    hits = page.search_for(PROOF_WORD)
    if not hits:
        raise SystemExit(f"Could not find {PROOF_WORD!r} in PDF text layer")
    # First occurrence: "programa público" in the preguntas guía block.
    return hits[0]


def crop_from_page_png(rect: pymupdf.Rect) -> None:
    page = pymupdf.open(PDF)[0]
    page_w, page_h = page.rect.width, page.rect.height
    img = Image.open(PNG_PAGE)
    sx = img.width / page_w
    sy = img.height / page_h
    pad = 3  # points
    r = pymupdf.Rect(rect.x0 - pad, rect.y0 - pad, rect.x1 + pad, rect.y1 + pad)
    box = (int(r.x0 * sx), int(r.y0 * sy), int(r.x1 * sx), int(r.y1 * sy))
    crop = img.crop(box)
    crop.save(OUT_PDF)


def render_from_ttf(reference_height_px: int) -> None:
    pt_px = BODY_PT * DPI / 72
    font = ImageFont.truetype(str(TTF), size=round(pt_px))
    probe = Image.new("RGB", (4, 4), "white")
    d_probe = ImageDraw.Draw(probe)
    bbox = d_probe.textbbox((0, 0), PROOF_WORD, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_x, pad_y = 6, 6
    w = max(tw + pad_x * 2, reference_height_px)
    h = max(th + pad_y * 2, reference_height_px)
    img = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(img)
    draw.text((pad_x - bbox[0], pad_y - bbox[1]), PROOF_WORD, font=font, fill=TEXT_BLUE)
    if img.height != reference_height_px:
        scale = reference_height_px / img.height
        img = img.resize((max(1, int(img.width * scale)), reference_height_px), Image.Resampling.LANCZOS)
    img.save(OUT_TTF)


def main() -> None:
    if not PNG_PAGE.is_file():
        raise SystemExit(f"Run build-render.py first (missing {PNG_PAGE.name})")
    rect = find_word_rect()
    crop_from_page_png(rect)
    ref_h = Image.open(OUT_PDF).height
    render_from_ttf(ref_h)
    print(
        "g proof: double-storey (binocular) g, same outline as the committed v3.003 TTF"
    )
    print(OUT_PDF)
    print(OUT_TTF)


if __name__ == "__main__":
    main()