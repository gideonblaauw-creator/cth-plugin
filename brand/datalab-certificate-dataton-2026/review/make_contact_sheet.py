#!/usr/bin/env python3
"""Build review/contact-sheet.png from sample PDFs and HTML crops."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = Path(__file__).resolve().parent


def ensure_deps() -> None:
    try:
        from PIL import Image, ImageDraw, ImageFont  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "-q", "pymupdf", "-q"])


def pdf_page_png(pdf: Path, scale: float = 2.0) -> Image.Image:
    import fitz
    from PIL import Image

    doc = fitz.open(pdf)
    page = doc[0]
    mat = fitz.Matrix(scale, scale)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    doc.close()
    return img


def main() -> None:
    ensure_deps()
    from PIL import Image, ImageDraw, ImageFont

    batch = REVIEW / "batch"
    samples = [
        ("Participante (equipo)", batch / "tomas-hernandez-quintero-participante.pdf"),
        ("40 caracteres", batch / "maria-alejandra-rodriguez-de-santamarias-participante.pdf"),
        ("Mentor", batch / "lucia-mendez-ocampo-mentor.pdf"),
        ("Jurado", batch / "diego-julian-rios-bustamante-jurado.pdf"),
    ]
    thumbs: list[tuple[Image.Image, str]] = []
    for label, path in samples:
        if not path.is_file():
            raise SystemExit(f"Missing sample PDF: {path}")
        img = pdf_page_png(path)
        w, h = img.size
        thumb = img.resize((int(w * 0.22), int(h * 0.22)), Image.Resampling.LANCZOS)
        thumbs.append((thumb, label))

    full = pdf_page_png(samples[0][1])
    fw, fh = full.size
    sig_crop = full.crop((int(fw * 0.18), int(fh * 0.58), int(fw * 0.82), int(fh * 0.78)))
    sig_crop = sig_crop.resize((sig_crop.width // 2, sig_crop.height // 2), Image.Resampling.LANCZOS)
    logo_crop = full.crop((int(fw * 0.05), int(fh * 0.78), int(fw * 0.95), int(fh * 0.95)))
    logo_crop = logo_crop.resize((logo_crop.width // 2, logo_crop.height // 2), Image.Resampling.LANCZOS)

    pad = 24
    cols = 2
    row_h = max(t[0].height for t in thumbs) + 40
    sheet_w = pad * 3 + thumbs[0][0].width * cols + thumbs[1][0].width * cols
    sheet_h = pad * 4 + row_h * 2 + sig_crop.height + logo_crop.height + 80
    sheet = Image.new("RGB", (sheet_w, sheet_h), "#ffffff")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype(str(ROOT / "fonts" / "OpenSans-SemiBold.ttf"), 18)
        title_font = ImageFont.truetype(str(ROOT / "fonts" / "TitilliumWeb-Bold.ttf"), 22)
    except OSError:
        font = ImageFont.load_default()
        title_font = font

    draw.text((pad, pad), "Datalab · Certificado Datatón 2026 — contact sheet", fill="#0C498A", font=title_font)

    y = pad + 36
    x = pad
    for i, (thumb, label) in enumerate(thumbs):
        col = i % cols
        row = i // cols
        tx = pad + col * (thumb.width + pad)
        ty = y + row * row_h
        sheet.paste(thumb, (tx, ty))
        draw.text((tx, ty + thumb.height + 6), label, fill="#0C498A", font=font)

    y2 = y + row_h * 2 + pad
    draw.text((pad, y2), "Bloque de firmas", fill="#669348", font=font)
    sheet.paste(sig_crop, (pad, y2 + 28))
    draw.text((pad + sig_crop.width + pad, y2), "Fila de logos (CEE pendiente)", fill="#669348", font=font)
    sheet.paste(logo_crop, (pad + sig_crop.width + pad, y2 + 28))

    out = REVIEW / "contact-sheet.png"
    sheet.save(out, dpi=(150, 150))
    print("wrote", out)


if __name__ == "__main__":
    # Late import typing for pdf_page_png hint
    from PIL import Image  # noqa: E402

    main()