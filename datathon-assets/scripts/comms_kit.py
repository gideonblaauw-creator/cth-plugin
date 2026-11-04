#!/usr/bin/env python3
"""Full multi-channel comms kit generation (formats, carousels, posts.md)."""
from __future__ import annotations

import html
import textwrap
from pathlib import Path

# Import generators from build_assets (same package directory).
from build_assets import (  # type: ignore
    BRAND_LINE,
    COLORS,
    EVENT_DATE,
    EVENT_SHORT,
    ROOT,
    STREAMS,
    agenda_print_html,
    ensure_shared_assets,
    visual_html,
    write_copy,
    write_copy_txt,
)

# channel folder → list of (filename_stem, width, height, layout_key)
CHANNEL_FORMATS: dict[str, list[tuple[str, int, int, str]]] = {
    "linkedin": [
        ("1200x627", 1200, 627, "linkedin"),
        ("1080x1080", 1080, 1080, "square"),
    ],
    "facebook": [
        ("1200x630", 1200, 630, "linkedin"),
        ("1920x1005", 1920, 1005, "banner"),
    ],
    "instagram": [
        ("1080x1080", 1080, 1080, "square"),
        ("1080x1350", 1080, 1350, "feed"),
    ],
    "story": [("1080x1920", 1080, 1920, "story")],
    "x": [("1600x900", 1600, 900, "banner")],
    "whatsapp": [
        ("1080x1080", 1080, 1080, "square"),
        ("1080x1920", 1080, 1920, "story"),
    ],
    "email": [("1200x400", 1200, 400, "banner")],
    "web": [("1920x600", 1920, 600, "banner")],
}

CAROUSEL_CHANNELS = {
    "linkedin-carousel": (1080, 1350, 4),
    "instagram-carousel": (1080, 1080, 4),
}


def carousel_slides(stream: dict) -> list[dict]:
    b = stream["bullets"]
    return [
        {
            "title": stream["headline"],
            "sub": stream["sub"],
            "lines": [EVENT_SHORT, BRAND_LINE],
        },
        {"title": "En el evento", "sub": stream["title"], "lines": b[:2]},
        {"title": "Datos y colaboración", "sub": BRAND_LINE, "lines": b[2:4]},
        {
            "title": "Aliados",
            "sub": "Air4U · CleantechHUB · [LOGO EXTERNADO]",
            "lines": [
                "Sede: PENDIENTE",
                "Hora: PENDIENTE",
                "Registro: PENDIENTE",
            ],
        },
    ]


def carousel_slide_html(stream: dict, slide: dict, w: int, h: int, idx: int, total: int) -> str:
    lines_html = "".join(f'<p class="bullet">{html.escape(x)}</p>' for x in slide["lines"])
    body = f"""
    <div class="canvas layout-carousel">
      <div class="carousel-inner">
        <p class="slide-no">{idx}/{total}</p>
        <h1 class="head">{html.escape(slide['title'])}</h1>
        <p class="sub">{html.escape(slide['sub'])}</p>
        <div class="lines">{lines_html}</div>
        <p class="tag">CleantechHUB · Inspira. Actúa. Transforma.</p>
      </div>
    </div>
    """
    extra_css = f"""
    .layout-carousel {{
      background: {COLORS['cyan']};
      height: 100%;
      padding: 48px 44px;
      display: flex;
      align-items: center;
    }}
    .carousel-inner {{ width: 100%; }}
    .layout-carousel .head {{ font-size: {int(h * 0.07)}px; color: {COLORS['deep']}; line-height: 1.05; }}
    .layout-carousel .sub {{ font-size: {int(h * 0.038)}px; font-weight: 600; margin: 12px 0 20px; color: {COLORS['deep']}; }}
    .layout-carousel .bullet {{ font-size: {int(h * 0.032)}px; color: {COLORS['deep']}; }}
    .layout-carousel .slide-no {{ font-size: 18px; color: {COLORS['forest']}; font-weight: 600; margin-bottom: 16px; }}
    .layout-carousel .tag {{ margin-top: 24px; font-size: 20px; color: {COLORS['forest']}; }}
    """
    return f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"/>
<title>{stream['id']} carousel {idx}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&family=Titillium+Web:wght@700&display=swap');
{extra_css}
html, body {{ width:{w}px; height:{h}px; overflow:hidden; margin:0; }}
</style></head><body>{body}</body></html>
"""


def simplified_svg(stream: dict, w: int, h: int, label: str) -> str:
    """Lightweight SVG (no embedded photos) for desk edit."""
    title = html.escape(stream["headline"][:48])
    sub = html.escape(stream["sub"][:64])
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <rect width="{w}" height="{h}" fill="{COLORS['cyan']}"/>
  <rect width="{int(w*0.34)}" height="{h}" fill="{COLORS['deep']}"/>
  <text x="{int(w*0.04)}" y="{int(h*0.12)}" fill="#FFFFFF" font-family="Titillium Web, sans-serif" font-size="{max(22,int(h*0.08))}" font-weight="700">Datalab</text>
  <text x="{int(w*0.38)}" y="{int(h*0.22)}" fill="{COLORS['deep']}" font-family="Titillium Web, sans-serif" font-size="{max(20,int(h*0.07))}" font-weight="700">{title}</text>
  <text x="{int(w*0.38)}" y="{int(h*0.32)}" fill="{COLORS['deep']}" font-family="Open Sans, sans-serif" font-size="{max(14,int(h*0.045))}">{sub}</text>
  <text x="{int(w*0.38)}" y="{int(h*0.88)}" fill="{COLORS['forest']}" font-family="Open Sans, sans-serif" font-size="14">{html.escape(label)} · {EVENT_SHORT}</text>
</svg>
"""


def write_posts_md(stream: dict, folder: Path) -> None:
    title = stream["title"]
    bullets = stream["bullets"]
    b0 = bullets[0].rstrip(".")
    li_long = textwrap.dedent(
        f"""
        **{stream['headline']}** — {EVENT_DATE}

        • {bullets[0]}
        • {bullets[1]}
        • {bullets[2]}
        • {bullets[3]}

        Air4U es socio de innovación; CleantechHUB actúa como custodio. Colaboración con Universidad Externado.

        Sede, hora y registro: PENDIENTE.

        #CleantechHUB #ClimateAction #Cleantech #ObservatorioDeLaTierra #Datalab #CalidadDelAire
        """
    ).strip()
    li_short = (
        f"{stream['headline']} · {EVENT_SHORT}. {b0}. "
        f"Sede/hora/RSVP: PENDIENTE. #CleantechHUB #Datalab"
    )
    fb_lines = "\n".join(f"• {b}" for b in bullets)
    fb = (
        f"{title} — {EVENT_DATE}\n\n"
        f"{stream['sub']}\n\n"
        f"{fb_lines}\n\n"
        f"Air4U (innovación) + CleantechHUB (custodio) + Universidad Externado.\n"
        f"Confirmación de sede, horario y enlace: PENDIENTE."
    )
    ig_caption = textwrap.dedent(
        f"""
        {stream['headline']} 🌍

        {EVENT_SHORT} · {BRAND_LINE}

        {bullets[0]}
        {bullets[1]}

        Air4U · CleantechHUB · Universidad Externado
        Sede y hora: PENDIENTE.
        """
    ).strip()
    hashtags = "#CleantechHUB #Datalab #ObservatorioDeLaTierra #CalidadDelAire #DatosAmbientales #InnovaciónClimática"
    alt = (
        f"Pieza gráfica CleantechHUB: {stream['headline']}, {EVENT_SHORT}. "
        f"Logos de aliados como placeholders. Sin personas identificadas."
    )
    x_post = (
        f"{stream['headline']} · {EVENT_SHORT}. {bullets[0][:80]}… "
        f"RSVP PENDIENTE. #CleantechHUB #Datalab #ClimateAction"
    )[:280]
    wa = (
        f"Hola — convocatoria *{title}* ({EVENT_SHORT}): {stream['headline']}. "
        f"{bullets[0]} Air4U + CleantechHUB + Universidad Externado. Sede/hora/RSVP: PENDIENTE."
    )
    email = textwrap.dedent(
        f"""
        Asunto sugerido: {stream['headline']} · {EVENT_SHORT}

        {stream['sub']}

        {bullets[0]} {bullets[1]}

        Sede, hora y enlace de registro: PENDIENTE.
        CleantechHUB · Inspira. Actúa. Transforma.
        """
    ).strip()
    ctas = textwrap.dedent(
        """
        ### CTA 1
        Registro: PENDIENTE — escríbenos para confirmar tu interés.

        ### CTA 2
        ¿Tu equipo trabaja datos ambientales? Contáctanos por mensaje directo.

        ### CTA 3
        Guarda la fecha · 24 · 11 · 2026 · Detalles operativos: PENDIENTE.
        """
    ).strip()
    body = f"""# posts.md — {stream['id']}

Estado: borrador · Awaiting Gideon's approval · NO publicar.

## LinkedIn (largo)
{li_long}

## LinkedIn (corto)
{li_short}

## Facebook
{fb}

## Instagram
### Caption
{ig_caption}

### Hashtags
{hashtags}

### Alt text
{alt}

## X (≤280 caracteres)
{x_post}

## WhatsApp (grupo)
{wa}

## Email (blurb)
{email}

## CTAs (variantes)
{ctas}
"""
    (folder / "posts.md").write_text(body, encoding="utf-8")


def write_channel_asset(
    stream: dict, channel_dir: Path, stem: str, w: int, h: int, layout: str
) -> None:
    for sub in ("svg", "png", "jpg"):
        (channel_dir / sub).mkdir(parents=True, exist_ok=True)
    html_path = channel_dir / f"{stem}.html"
    html_path.write_text(visual_html(stream, w, h, layout), encoding="utf-8")
    (channel_dir / "svg" / f"{stem}.svg").write_text(
        simplified_svg(stream, w, h, stem), encoding="utf-8"
    )


def write_carousel(stream: dict, channel: str, w: int, h: int, slides_n: int) -> None:
    folder = ROOT / stream["id"] / channel
    for sub in ("svg", "png", "jpg"):
        (folder / sub).mkdir(parents=True, exist_ok=True)
    slides = carousel_slides(stream)[:slides_n]
    for i, slide in enumerate(slides, start=1):
        stem = f"slide-{i:02d}"
        (folder / f"{stem}.html").write_text(
            carousel_slide_html(stream, slide, w, h, i, len(slides)), encoding="utf-8"
        )
        (folder / "svg" / f"{stem}.svg").write_text(
            simplified_svg(stream, w, h, f"{channel}-{stem}"), encoding="utf-8"
        )


def build_full_comms(*, visuals_only: bool = False) -> None:
    ensure_shared_assets()
    manifest: list[dict] = []
    for stream in STREAMS:
        sid = stream["id"]
        folder = ROOT / sid
        folder.mkdir(parents=True, exist_ok=True)
        if not visuals_only:
            write_copy(stream)
            write_copy_txt(stream, folder)
            write_posts_md(stream, folder)
        for channel, formats in CHANNEL_FORMATS.items():
            ch_dir = folder / channel
            for stem, w, h, layout in formats:
                write_channel_asset(stream, ch_dir, stem, w, h, layout)
                manifest.append(
                    {"file": f"{sid}/{channel}/{stem}.html", "channel": channel, "size": stem}
                )
        for channel, (w, h, n) in CAROUSEL_CHANNELS.items():
            write_carousel(stream, channel, w, h, n)
            manifest.append({"file": f"{sid}/{channel}/", "channel": channel, "size": f"{w}x{h}×{n}"})
    # Agenda printable stays at stream root
    agenda_dir = ROOT / "01-agenda"
    (agenda_dir / "agenda-print-a4.html").write_text(agenda_print_html(), encoding="utf-8")
    manifest.append({"file": "01-agenda/agenda-print-a4.html", "channel": "print", "size": "A4"})
    print(f"comms_kit: streams={len(STREAMS)} manifest_entries={len(manifest)}")
