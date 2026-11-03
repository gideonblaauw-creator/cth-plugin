#!/usr/bin/env python3
"""Render brochure HTML to PDF and verify page count."""
import asyncio
import re
import subprocess
import sys
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent
BROCHURES = [
    ("brochure-es.html", "brochure-es.pdf"),
    ("brochure-en.html", "brochure-en.pdf"),
]
EXPECTED_PAGES = 2


async def html_to_pdf(html_path: Path, pdf_path: Path) -> None:
    abs_html = html_path.resolve()
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True, args=["--no-sandbox", "--disable-gpu"]
        )
        page = await browser.new_page()
        await page.goto(f"file://{abs_html}", wait_until="networkidle")
        await page.wait_for_timeout(1200)
        await page.pdf(
            path=str(pdf_path),
            format="A4",
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            print_background=True,
            prefer_css_page_size=True,
        )
        await browser.close()


def pdf_page_count(pdf_path: Path) -> int:
    try:
        out = subprocess.check_output(
            ["pdfinfo", str(pdf_path)], stderr=subprocess.STDOUT, text=True
        )
        for line in out.splitlines():
            if line.startswith("Pages:"):
                return int(line.split(":", 1)[1].strip())
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
        pass
    raw = pdf_path.read_bytes()
    return len(re.findall(rb"/Type\s*/Page[^s]", raw))


def grep_forbidden_brand(path: Path, needle: bytes) -> list[str]:
    hits = []
    text = path.read_text(encoding="utf-8", errors="replace")
    if needle.decode().lower() in text.lower():
        hits.append(f"{path.name}: text")
    if path.suffix == ".pdf":
        if re.search(needle, path.read_bytes(), re.I):
            hits.append(f"{path.name}: binary/metadata")
    return hits


async def main() -> int:
    errors = []
    for html_name, pdf_name in BROCHURES:
        html_path = ROOT / html_name
        pdf_path = ROOT / pdf_name
        if not html_path.is_file():
            errors.append(f"Missing {html_path}")
            continue
        await html_to_pdf(html_path, pdf_path)
        pages = pdf_page_count(pdf_path)
        print(f"{pdf_name}: {pages} page(s)")
        if pages != EXPECTED_PAGES:
            errors.append(f"{pdf_name}: expected {EXPECTED_PAGES} pages, got {pages}")
        banned = b"pro" + b"migas"
        errors.extend(grep_forbidden_brand(html_path, banned))
        errors.extend(grep_forbidden_brand(pdf_path, banned))

    if errors:
        print("VALIDATION FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("OK: page counts and brand-word grep")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
