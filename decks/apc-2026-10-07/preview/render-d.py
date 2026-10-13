#!/usr/bin/env python3
"""Build preview HTML and PNGs for Hands D slides."""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
PREVIEW = ROOT / "preview"
SLIDES = [
    ("13", ROOT / "slides/13-growth.html"),
    ("14", ROOT / "slides/14-proplanet.html"),
    ("15", ROOT / "slides/15-mubon-weia-bbns.html"),
    ("16", ROOT / "slides/16-encaje-tdr.html"),
    ("17", ROOT / "slides/17-solicitud.html"),
    ("18", ROOT / "slides/18-fuentes.html"),
]

def _abs_img_urls(html: str) -> str:
    """Rewrite img/ paths to file URIs so Playwright file:// preview shows photos."""
    def repl(m):
        fname = m.group(1)
        return f"url('{ (ROOT / 'img' / fname).as_uri() }')"
    html = re.sub(r"url\(['\"]img/([^'\"]+)['\"]\)", repl, html)
    return html


def build_html():
    parts = []
    for num, path in SLIDES:
        html = path.read_text(encoding="utf-8")
        if 'data-slide=' not in html:
            html = re.sub(
                r"(<section class=\"slide[^\"]*\")",
                rf'\1 data-slide="{num}"',
                html,
                count=1,
            )
        parts.append(_abs_img_urls(html))
    doc = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Hands D preview</title>
<base href="../">
<link rel="stylesheet" href="preview/d.css">
</head>
<body class="preview-print">
{"".join(parts)}
</body>
</html>
"""
    out = PREVIEW / "d-full.html"
    out.write_text(doc, encoding="utf-8")
    return out


def render_pngs(html_path: Path):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        from playwright.sync_api import sync_playwright

    url = html_path.as_uri()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
        for num, _ in SLIDES:
            page.goto(f"{url}#s{num}")
            page.evaluate(
                """(n) => {
                  document.querySelectorAll('.slide').forEach(s => {
                    s.style.display = s.dataset.slide === n ? 'block' : 'none';
                    s.style.position = 'relative';
                    s.style.margin = '0';
                  });
                }""",
                num,
            )
            sel = f'.slide[data-slide="{num}"]'
            page.wait_for_selector(sel, timeout=10000)
            out = PREVIEW / f"d-{num}.png"
            page.locator(sel).screenshot(path=str(out))
            print("wrote", out)
        browser.close()


def main():
    html_path = build_html()
    render_pngs(html_path)


if __name__ == "__main__":
    main()
