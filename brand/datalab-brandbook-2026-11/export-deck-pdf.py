#!/usr/bin/env python3
"""Export brand book PDF: A4 landscape, one slide per page, embedded fonts (Playwright)."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

PREP_JS = """
() => {
  document.body.classList.add('print-all', 'es');
  document.querySelectorAll('.deck .slide').forEach(el => {
    el.classList.add('active');
    el.style.cssText =
      'display:flex!important;position:relative!important;inset:auto!important;width:297mm!important;height:210mm!important;max-width:297mm!important;min-height:210mm!important;page-break-after:always!important;break-after:page!important;box-sizing:border-box!important;';
  });
  document.querySelectorAll('.deck-viewport, .deck-frame, .deck-stage, .deck').forEach(el => {
    el.style.cssText = 'position:static!important;display:block!important;width:297mm!important;max-width:297mm!important;height:auto!important;margin:0!important;padding:0!important;overflow:visible!important;transform:none!important;';
  });
  document.querySelectorAll('.topbar, .site-footer, .pdf-dl-fixed').forEach(el => {
    el.style.display = 'none';
  });
  const svgToPng = {
    'assets/logos/datalab-logo.svg': 'assets/logos/datalab-logo-light.png',
    'assets/logos/datalab-logo-mono.svg': 'assets/logos/datalab-logo-light.png',
    'assets/logos/datalab-logo-stacked.svg': 'assets/logos/datalab-logo-endorsed-light.png',
    'assets/logos/datalab-option-b.svg': 'assets/logos/datalab-option-b.png',
    'assets/templates/chart-example.svg': 'assets/templates/chart-example.png',
  };
  document.querySelectorAll('img').forEach(img => {
    const src = img.getAttribute('src') || '';
    Object.entries(svgToPng).forEach(([from, to]) => {
      if (src.endsWith(from)) img.setAttribute('src', to);
    });
  });
  document.documentElement.style.margin = '0';
  document.documentElement.style.padding = '0';
  document.documentElement.style.width = '297mm';
  document.body.style.margin = '0';
  document.body.style.padding = '0';
  document.body.style.width = '297mm';
  document.querySelectorAll('*').forEach(el => {
    el.style.setProperty('animation', 'none', 'important');
    el.style.setProperty('transition', 'none', 'important');
    const tag = el.tagName;
    if (/^H[1-6]$/.test(tag) || el.classList.contains('brand-book') || el.classList.contains('chapter-num') || el.classList.contains('slide-num-big') || el.classList.contains('manual-title') || el.classList.contains('brand')) {
      el.style.setProperty('font-family', '"Titillium Web", "Open Sans", sans-serif', 'important');
    } else {
      el.style.setProperty('font-family', '"Open Sans", sans-serif', 'important');
    }
    el.style.setProperty('font-synthesis', 'none', 'important');
  });
}
"""


def ensure_playwright() -> None:
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Export HTML brand book to A4 landscape PDF")
    parser.add_argument("--index", type=Path, default=Path("index.html"))
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--mode", choices=("auto", "scroll", "slides"), default="auto")
    args = parser.parse_args()

    index = args.index.resolve()
    pdf_out = args.pdf if args.pdf.is_absolute() else (index.parent / args.pdf)
    pdf_out.parent.mkdir(parents=True, exist_ok=True)

    ensure_playwright()
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-gpu",
                "--font-render-hinting=none",
                "--disable-features=FontSrcLocalMatching",
            ],
        )
        page = browser.new_page(viewport={"width": 1123, "height": 794})
        page.goto(index.as_uri(), wait_until="networkidle")
        page.wait_for_timeout(400)
        page.evaluate(PREP_JS)
        page.wait_for_function("() => document.fonts.status === 'loaded'")
        page.emulate_media(media="print")
        page.pdf(
            path=str(pdf_out),
            format="A4",
            landscape=True,
            print_background=True,
            prefer_css_page_size=True,
            scale=1,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()

    print("wrote", pdf_out, "mode=slides engine=playwright-a4")


if __name__ == "__main__":
    main()
