#!/usr/bin/env python3
"""Measure tagline and logo-row distance from bottom trim (mm)."""
from __future__ import annotations

import sys
from pathlib import Path

import fitz

PT_TO_MM = 25.4 / 72.0


def measure(pdf: Path) -> dict[str, float]:
    doc = fitz.open(pdf)
    page = doc[0]
    page_h_pt = float(page.rect.height)
    page_w_pt = float(page.rect.width)

    tagline_y_max = None
    partner_y_max = 0.0
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            text = "".join(span["text"] for span in line["spans"])
            y_end = max(span["bbox"][3] for span in line["spans"])
            if "Inspira" in text:
                tagline_y_max = max(tagline_y_max or 0, y_end)
            if "Logo CEE" in text or "CleantechHUB" in text or "Universidad" in text:
                partner_y_max = max(partner_y_max, y_end)

    for img in page.get_images(full=True):
        xref = img[0]
        for item in page.get_image_rects(xref):
            partner_y_max = max(partner_y_max, float(item.y1))

    doc.close()
    logo_y_max = partner_y_max

    if tagline_y_max is None:
        raise SystemExit("Tagline text not found")

    tagline_from_bottom_mm = (page_h_pt - tagline_y_max) * PT_TO_MM
    logos_from_bottom_mm = (page_h_pt - logo_y_max) * PT_TO_MM
    logo_gap_mm = logos_from_bottom_mm - tagline_from_bottom_mm

    return {
        "page_h_pt": page_h_pt,
        "page_w_pt": page_w_pt,
        "tagline_bottom_mm": round(tagline_from_bottom_mm, 2),
        "logo_row_bottom_mm": round(logos_from_bottom_mm, 2),
        "logo_above_tagline_mm": round(logo_gap_mm, 2),
    }


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    default = here / "batch/maria-alejandra-rodriguez-de-santamarias-participante.pdf"
    path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else default
    m = measure(path)
    for k, v in m.items():
        print(f"{k}: {v}")