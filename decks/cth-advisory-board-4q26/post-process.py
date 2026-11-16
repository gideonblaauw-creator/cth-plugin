#!/usr/bin/env python3
"""Deck-level HTML patches after outline.sh (no library template edits)."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

DECK_DIR = Path(__file__).resolve().parent
INDEX = DECK_DIR / "index.html"
ASSETS = DECK_DIR / "assets"
QR_PATH = ASSETS / "qr-cleantechhub.png"
QR_URL = "https://cleantechhub.net"
LINK_CTH = "https://cleantechhub.net"
LINK_DRIVE_REPORT = (
    "https://docs.google.com/document/d/1cWHBm-W_MKruqRM24Y13OKJpRx95ZDrNxOc8quKrrfU/edit"
)


def ensure_qr() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    try:
        import qrcode

        qrcode.make(QR_URL).save(QR_PATH)
        return
    except ImportError:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--user", "qrcode[pil]"],
            check=True,
        )
        import qrcode  # noqa: F401 — retry after install

        import qrcode as qr

        qr.make(QR_URL).save(QR_PATH)


def strip_empty_columns(html: str) -> str:
    html = re.sub(
        r'(<div class="cth-cover">.*?<div>.*?</div>)\s*<div>\s*</div>',
        r"\1",
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = re.sub(
        r'(<div class="cth-contents">.*?<ol class="cth-contents__list">.*?</ol>\s*</div>)\s*<div>\s*</div>',
        r"\1",
        html,
        count=1,
        flags=re.DOTALL,
    )
    return html


def patch_html(html: str) -> str:
    html = re.sub(r'\s*<span class="cth-badge-example">Example</span>', "", html)
    html = re.sub(r'<p class="cth-eyebrow">Example</p>\s*', "", html)
    html = re.sub(r'<div class="cth-ph-img"[^>]*>Example</div>', "", html)

    html = html.replace(
        '<h2 class="cth-title">Contents</h2>', '<h2 class="cth-title">Contenido</h2>'
    )
    html = re.sub(r'(<p class="cth-source">)Source:', r"\1Fuente:", html)

    html = html.replace(
        '<div class="cth-fact__icon">€</div>',
        '<div class="cth-fact__icon">$</div>',
    )
    html = html.replace(
        "cohortes documentados en informes previos",
        "cohortes documentadas en informes previos",
    )

    html = html.replace(
        'class="cth-slide cth-slide--cover"',
        'class="cth-slide cth-slide--cover cth-cover--no-image"',
    )
    html = html.replace(
        'class="cth-slide cth-slide--contents"',
        'class="cth-slide cth-slide--contents cth-contents--no-image"',
    )
    html = strip_empty_columns(html)

    html = html.replace(
        'class="cth-slide cth-slide--showcase"',
        'class="cth-slide cth-slide--showcase cth-showcase--no-img"',
    )
    html = re.sub(
        r'\s*<div class="cth-showcase-imgs[^"]*"[^>]*>\s*(?:<img[^>]*>|<div class="cth-ph-img"[^>]*>[^<]*</div>)\s*</div>',
        "",
        html,
    )

    qr_img = (
        f'<img class="cth-qr" src="assets/qr-cleantechhub.png" '
        f'alt="QR — cleantechhub.net" width="200" height="200" />'
    )
    html = html.replace('<div class="cth-qr">Example QR</div>', qr_img)

    if "deck-overrides.css" not in html:
        html = html.replace(
            '<link rel="stylesheet" href="theme/cleantechhub.css" id="theme" />',
            '<link rel="stylesheet" href="theme/cleantechhub.css" id="theme" />\n'
            '  <link rel="stylesheet" href="assets/deck-overrides.css" />',
        )

    html = html.replace(
        'class="cth-slide cth-slide--ecosystem"',
        'class="cth-slide cth-slide--ecosystem cth-ecosystem--board"',
    )
    html = re.sub(
        r"(<section class=\"cth-slide cth-slide--ecosystem cth-ecosystem--board\"[^>]*>\s*"
        r"<div class=\"cth-slide__head\"><h2 class=\"cth-title\">Nexus — portfolio y ecosistema</h2></div>\s*)"
        r'<div class="cth-slide__body">',
        r'\1<div class="cth-slide__body">'
        r'<p class="cth-eco-intro">nexus.cleantechhub.net — portfolio de startups y mapa del ecosistema; '
        r"despliegue documentado con prioridad de publicación desde GitHub.</p>",
        html,
        count=1,
    )

    html = html.replace(
        "<div class=\"cth-stat-tile__label\">Capital levantado</div>",
        '<div class="cth-stat-tile__label">Capital levantado'
        '<span class="cth-stat-tile__label-sub">acumulado, no solo 2026</span></div>',
    )

    html = html.replace(
        "<span class=\"cth-link-chip\">Fundación CleantechHUB</span>",
        f'<a class="cth-link-chip" href="{LINK_CTH}">Fundación CleantechHUB</a>',
    )
    html = html.replace(
        "<span class=\"cth-link-chip\">Informe borrador (Drive)</span>",
        f'<a class="cth-link-chip" href="{LINK_DRIVE_REPORT}">Informe borrador (Drive)</a>',
    )

    if re.search(r">Example(?:\s|<)", html):
        print("warn: Example text still present in index.html", file=sys.stderr)

    return html


def main() -> None:
    if not INDEX.is_file():
        raise SystemExit(f"missing {INDEX} — run outline.sh first")
    ensure_qr()
    INDEX.write_text(patch_html(INDEX.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"post-process OK → {INDEX}")


if __name__ == "__main__":
    main()