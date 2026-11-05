#!/usr/bin/env python3
"""Export EO brand book, agenda, social templates, and contact sheet (Playwright)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out"


def ensure_playwright() -> None:
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def pdf_portrait(page, html: Path, pdf: Path) -> None:
    page.goto(html.resolve().as_uri(), wait_until="networkidle")
    page.emulate_media(media="print")
    page.pdf(
        path=str(pdf),
        format="A4",
        landscape=False,
        print_background=True,
        margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
    )


def screenshot(page, html: Path, png: Path, width: int, height: int) -> None:
    page.set_viewport_size({"width": width, "height": height})
    page.goto(html.resolve().as_uri(), wait_until="networkidle")
    page.screenshot(path=str(png), full_page=False)


def main() -> None:
    ensure_playwright()
    from playwright.sync_api import sync_playwright

    OUT.mkdir(parents=True, exist_ok=True)
    templates_dir = ROOT / "templates" / "social"
    exports: list[tuple[Path, Path, int, int]] = [
        (templates_dir / "linkedin-post-1200x1200.html", OUT / "tpl-linkedin-1200x1200.png", 1200, 1200),
        (templates_dir / "linkedin-post-1200x627.html", OUT / "tpl-linkedin-1200x627.png", 1200, 627),
        (templates_dir / "linkedin-carousel-1080x1350.html", OUT / "tpl-linkedin-carousel-1080x1350.png", 1080, 1350),
        (templates_dir / "instagram-post-1080x1080.html", OUT / "tpl-instagram-1080x1080.png", 1080, 1080),
        (templates_dir / "instagram-post-1080x1350.html", OUT / "tpl-instagram-1080x1350.png", 1080, 1350),
        (templates_dir / "story-reel-1080x1920.html", OUT / "tpl-story-1080x1920.png", 1080, 1920),
        (templates_dir / "x-1600x900.html", OUT / "tpl-x-1600x900.png", 1600, 900),
        (templates_dir / "whatsapp-1080x1080.html", OUT / "tpl-whatsapp-1080x1080.png", 1080, 1080),
        (templates_dir / "youtube-1280x720.html", OUT / "tpl-youtube-1280x720.png", 1280, 720),
        (templates_dir / "event-banner-1584x396.html", OUT / "tpl-event-banner-1584x396.png", 1584, 396),
        (ROOT / "applications" / "one-pager.html", OUT / "tpl-one-pager.png", 794, 1123),
        (ROOT / "applications" / "email-header.html", OUT / "tpl-email-header.png", 600, 200),
    ]

    brand_book = ROOT / "brand-book" / "index.html"
    agenda = ROOT / "applications" / "agenda-24nov-eo.html"
    contact = ROOT / "contact-sheet.html"

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = browser.new_page()

        pdf_portrait(page, brand_book, OUT / "observatorio-de-la-tierra-brand-book-v2.pdf")
        pdf_portrait(page, agenda, OUT / "agenda-24nov-eo.pdf")
        pdf_portrait(page, ROOT / "applications" / "one-pager.html", OUT / "one-pager.pdf")
        slide = ROOT / "applications" / "slide-master" / "index.html"
        if slide.is_file():
            page.goto(slide.resolve().as_uri(), wait_until="networkidle")
            page.emulate_media(media="print")
            page.pdf(
                path=str(OUT / "slide-master.pdf"),
                format="A4",
                landscape=True,
                print_background=True,
                margin={"top": "0.2in", "right": "0.2in", "bottom": "0.2in", "left": "0.2in"},
            )
        screenshot(page, agenda, OUT / "agenda-24nov-eo.png", 794, 1123)

        for html, png, w, h in exports:
            if html.is_file():
                screenshot(page, html, png, w, h)

        page.set_viewport_size({"width": 1400, "height": 2000})
        page.goto(contact.resolve().as_uri(), wait_until="networkidle")
        page.screenshot(path=str(OUT / "contact-sheet-templates.png"), full_page=True)

        browser.close()

    print("Exports written under", OUT)


if __name__ == "__main__":
    main()
