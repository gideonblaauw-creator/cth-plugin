---
name: html-to-pdf
description: >
  Convert single-file HTML proposals, reports, or documents to high-quality PDF.
  Trigger on "generate a PDF", "export to PDF", "convert the HTML to PDF",
  "create a PDF from the proposal", or any variation. Also trigger proactively
  after building HTML files that the user will likely want as PDF.
metadata:
  version: "2.0.0"
  category: infrastructure
---

# HTML to PDF Conversion

You are responsible for converting self-contained HTML documents into high-quality PDF files. This skill covers proposals, reports, one-pagers, invoices, and any document the user needs as a printable or shareable PDF. Follow this protocol exactly to avoid the rendering failures that plague headless browser PDF generation.

## Supported Method

Use Playwright with Chromium for all HTML-to-PDF conversions. This gives the most accurate rendering for complex CSS layouts, multi-page documents, and branded content. Do not use wkhtmltopdf, WeasyPrint, or other tools unless Playwright is explicitly unavailable and the user approves the fallback.

### Environment Setup

Before the first conversion in a session, verify Playwright is installed and Chromium is available:

```bash
pip install playwright 2>/dev/null || pip3 install playwright
playwright install chromium 2>/dev/null || python -m playwright install chromium
```

If Playwright is unavailable, fall back to `google-chrome --headless --print-to-pdf` or `chromium-browser --headless --print-to-pdf`. If neither is available, notify the user.

## Standard Workflow

Follow these steps in order for every conversion. Do not skip steps.

### Step 1: Validate the HTML

Before converting, verify the HTML file is complete and self-contained:

- Proper `<!DOCTYPE html>`, `<html>`, `<head>`, and `<body>` tags.
- All CSS inline (`<style>` tags) — no external stylesheet links.
- All JavaScript inline if needed — no external script references.
- All images as base64 data URIs or absolute URLs. Relative paths will break.
- All fonts as system fonts or embedded via `@font-face` with base64 data URIs.

If external resources are found, inline them before proceeding.

### Step 2: Inject Print CSS

Add print-specific CSS to the document if not already present. Insert this block inside the existing `<style>` tag or add a new `<style>` tag before `</head>`:

```css
@media print {
  html, body {
    width: 210mm;
    min-height: 297mm;
  }
  body {
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
    color-adjust: exact !important;
  }
  .no-print {
    display: none !important;
  }
  .page-break {
    page-break-before: always;
  }
  .avoid-break {
    page-break-inside: avoid;
  }
  * {
    animation: none !important;
    transition: none !important;
  }
  @page {
    margin: 0;
  }
}
```

Key points about this CSS:
- `print-color-adjust: exact` forces background colors and images to render. Without this, colored sections appear white.
- `animation: none` and `transition: none` prevent unfinished animations from affecting the snapshot.
- `@page { margin: 0 }` removes default browser margins — control margins via Playwright's PDF options instead for consistency.

### Step 3: Generate the PDF

Use this Playwright script as the canonical conversion method:

```python
import asyncio
from playwright.async_api import async_playwright
import os

async def html_to_pdf(html_path, pdf_path, options=None):
    """Convert an HTML file to PDF using Playwright/Chromium."""
    defaults = {
        "format": "A4",
        "margin": {
            "top": "15mm",
            "right": "15mm",
            "bottom": "15mm",
            "left": "15mm"
        },
        "print_background": True,
        "prefer_css_page_size": True
    }
    if options:
        defaults.update(options)

    abs_html_path = os.path.abspath(html_path)

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-gpu"]
        )
        page = await browser.new_page()

        # Load the HTML file
        await page.goto(
            f"file://{abs_html_path}",
            wait_until="networkidle"
        )

        # Wait for fonts and images to load
        await page.wait_for_timeout(1000)

        # Generate PDF
        await page.pdf(
            path=pdf_path,
            format=defaults["format"],
            margin=defaults["margin"],
            print_background=defaults["print_background"],
            prefer_css_page_size=defaults["prefer_css_page_size"]
        )

        await browser.close()

    return pdf_path

# Usage
asyncio.run(html_to_pdf("input.html", "output.pdf"))
```

### Step 4: Validate the Output

After generating the PDF:

1. Verify the file exists and has a non-zero size.
2. Check the file is a valid PDF (starts with `%PDF-`).
3. If possible, verify page count matches expectations.
4. Deliver the PDF to the user via SendUserFile.

## Page Size and Margin Options

| Format | Dimensions | Common Use |
|--------|-----------|------------|
| A4 | 210mm x 297mm | Default for most documents, standard outside US |
| Letter | 8.5in x 11in | US standard |
| Legal | 8.5in x 14in | Legal documents |

Standard margins: 15mm on all sides for body text documents. For full-bleed designs (proposals with edge-to-edge color), set margins to 0 and handle spacing in the HTML/CSS itself.

## Critical Points and Failure Modes

### Font Rendering

Fonts are the most common PDF rendering failure. Follow this hierarchy:

1. **Preferred**: system fonts available in headless Chromium — Arial, Helvetica, Times New Roman, sans-serif, serif, monospace.
2. **Brand fonts**: embed via `@font-face` with base64 `woff2` data URIs. Guarantees availability regardless of environment.
3. **Never**: reference Google Fonts or external CDNs — headless Chromium may lack network access.

If fonts look wrong, verify `@font-face` has correct `font-weight`/`font-style` and CSS references the exact `font-family` name.

### Background Colors and Gradients

Background colors will not appear in the PDF unless `print_background: True` is set in the Playwright PDF options AND `print-color-adjust: exact` is set in the CSS. Both are required. Gradients work but may show banding in some cases — test with the specific gradient.

### SVG and Images

- **Inline SVG**: works reliably. Always include an explicit `viewBox` attribute and set `width`/`height` in the SVG element or its container.
- **External SVG files** (`<img src="logo.svg">`): may not render in headless mode. Convert to inline SVG or base64 data URI before conversion.
- **Raster images**: use base64 data URIs for guaranteed rendering. If using URLs, they must be absolute and accessible from the conversion environment.
- **Image resolution**: for print quality, use images at 2x the display size (e.g., a 300px-wide image should be 600px source). Standard screen-resolution images will appear blurry when printed.

### Page Breaks

Control where pages break to avoid awkward splits:

- `page-break-before: always` — force a new page before an element (use for section headers).
- `page-break-inside: avoid` — prevent an element from being split across pages (use for tables, cards, key-value blocks).
- `page-break-after: avoid` — prevent a break immediately after an element (use for headings to keep them with their content).

Add the utility class `.page-break` to any element that should start a new page, and `.avoid-break` to any element that should not be split.

### Multi-Page Documents

For documents longer than one page, test with realistic content length, add page numbers via CSS `@page` counters if appropriate, and verify headers/footers repeat correctly.

## Common Document Types

- **Proposals and one-pagers**: A4, 15mm margins. Full-bleed headers use `calc(100% + 30mm)` width and negative margins. Brand colors require `print-color-adjust: exact`.
- **Reports and data documents**: A4, 20mm margins. Tables need `page-break-inside: avoid`. Charts must be inline SVG, not canvas.
- **Invoices**: A4 or Letter by locale. Right-align numeric columns. Keep totals section intact with `page-break-inside: avoid`.

## Post-Conversion Delivery

After generating the PDF:

1. Send the PDF file to the user via SendUserFile with display set to "attach".
2. If the user is on a connected device, offer to commit the file to their local filesystem via device_commit_files.
3. If the PDF is a deliverable for an external party, confirm the file name follows the user's naming convention before delivery.

For Playwright PDF configuration options, print CSS templates, and document type presets, see references/.
