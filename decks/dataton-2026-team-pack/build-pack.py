#!/usr/bin/env python3
"""Build team-pack-es v0.4: PDFs, zip, manifest, PNG previews."""
from __future__ import annotations

import asyncio
import hashlib
import json
import re
import zipfile
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent
TEAM = ROOT / "team-pack-es"
PRINT = ROOT / "print"
OUT = ROOT / "dist"
PNG = ROOT / "_png"
ZIP_NAME = "team-pack-es-pdfs-v0.4.zip"

MD_TO_PDF = [
    "agenda-equipos.md",
    "hoja-1-mapa-de-calor.md",
    "hoja-2-flujo-de-datos.md",
    "hoja-3-dato-a-valor.md",
    "hoja-4-plantilla-tablero.md",
    "hoja-4b-ejemplo-air4u.md",
    "hoja-5-plantilla-pitch.md",
    "ejemplo-air4u.md",
    "fuentes-datos-abiertos.md",
    "nota-derechos-datos.md",
    "guia-carpeta-drive.md",
]

HTML_TO_PDF = [
    ("plantilla-bmc.html", "plantilla-bmc.pdf", {"landscape": True, "format": "A4"}),
    ("prompts-ia-v2.html", "prompts-ia-v2.pdf", {"format": "A4"}),
    ("hoja-5-plantilla-pitch.html", "hoja-5-plantilla-pitch.pdf", {"format": "A4"}),
]

EXCLUDE_ZIP = {"test-notes.md", "test-notes.pdf", "prompts-ia.pdf", "team-pack-es-manifest-sha256.md"}


def stage_md_build_dir(tmp_html: Path) -> None:
    """Copy logo/fonts beside generated HTML so relative asset URLs resolve."""
    import shutil

    tmp_html.mkdir(parents=True, exist_ok=True)
    assets = tmp_html / "assets"
    fonts_dir = assets / "fonts"
    fonts_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT / "assets/cth-logo-color.png", assets / "cth-logo-color.png")
    for woff in (ROOT / "assets/fonts").glob("*.woff2"):
        shutil.copy(woff, fonts_dir / woff.name)
    (tmp_html / "md-print.css").write_text(
        (PRINT / "md-print.css").read_text(encoding="utf-8"), encoding="utf-8"
    )


def export_pdf_pngs(
    pdf_path: Path, prefix: str, dpi: int = 150, max_pages: int | None = None
) -> int:
    """Rasterize each PDF page to _png/{prefix}-pNN.png; return page count."""
    import fitz

    if not pdf_path.is_file():
        raise FileNotFoundError(pdf_path)
    for old in PNG.glob(f"{prefix}-p*.png"):
        old.unlink()
    doc = fitz.open(pdf_path)
    n_render = doc.page_count if max_pages is None else min(max_pages, doc.page_count)
    for i in range(n_render):
        out = PNG / f"{prefix}-p{i + 1:02d}.png"
        pix = doc[i].get_pixmap(dpi=dpi, alpha=False)
        pix.save(str(out))
        if prefix == "plantilla-bmc" and i == 0:
            alias = PNG / "plantilla-bmc-p1.png"
            pix.save(str(alias))
        print("png", out.name)
    n = doc.page_count
    doc.close()
    return n


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def md_to_html_body(md_text: str, title: str, borrador: bool = False) -> str:
    body = markdown.markdown(md_text, extensions=["tables", "fenced_code", "nl2br"])
    banner = '<p class="borrador">BORRADOR — pendiente GO de Gideon en PR #172</p>' if borrador else ""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <title>{title}</title>
  <link rel="stylesheet" href="md-print.css" />
</head>
<body>
  <header class="hdr-bar">
    <img src="assets/cth-logo-color.png" alt="CleantechHUB" />
    <span>Datatón v0.4-es</span>
  </header>
  {banner}
  <main>{body}</main>
</body>
</html>"""


def write_leeme() -> str:
    lines = [
        "# LEEME — Paquete equipo Datatón v0.4-es",
        "",
        "| Archivo | Propósito | Estado |",
        "|---|---|---|",
        "| `plantilla-bmc.pdf` | Lienzo BMC en blanco (A4 apaisado) | Listo v0.4 |",
        "| `prompts-ia-v2.pdf` | Prompts copiar/pegar (BMC, Hojas 1–5, transversal) | Listo v0.4 |",
        "| `agenda-equipos.pdf` | Run-of-show (14 equipos, horas v5) | Listo v0.4 |",
        "| `hoja-1-mapa-de-calor.pdf` | Mapa de calor ¿DÓNDE? | v0.3-es → v0.4 pack |",
        "| `hoja-2-flujo-de-datos.pdf` | Flujo + escalera Medallion | v0.3-es → v0.4 pack |",
        "| `hoja-3-dato-a-valor.pdf` | De dato a valor | v0.3-es → v0.4 pack |",
        "| `hoja-4-plantilla-tablero.pdf` | Plantilla tablero una pantalla | v0.3-es → v0.4 pack |",
        "| `hoja-4b-ejemplo-air4u.pdf` | Ejemplo Air4U (Hoja 4) | Ilustrativo |",
        "| `hoja-5-plantilla-pitch.pdf` | Pitch 5 min finales | **BORRADOR** (PR #172) |",
        "| `ejemplo-air4u.pdf` | Ejemplo Hojas 1–3 Air4U | Ilustrativo |",
        "| `fuentes-datos-abiertos.pdf` | Fuentes verificadas (aire) | v0.3-es |",
        "| `nota-derechos-datos.pdf` | Reglas derechos de datos | Borrador Legal |",
        "| `guia-carpeta-drive.pdf` | Plantilla carpeta por equipo | Plantilla |",
        "",
        "`test-notes` **no** va en el zip de mesa.",
        "",
        "CleantechHUB · Datatón Observatorio de la Tierra · 24 nov 2026",
    ]
    text = "\n".join(lines)
    (TEAM / "LEEME.md").write_text(text, encoding="utf-8")
    return text


async def render_all() -> None:
    from playwright.async_api import async_playwright

    OUT.mkdir(parents=True, exist_ok=True)
    PNG.mkdir(parents=True, exist_ok=True)
    tmp_html = PRINT / "_build"
    stage_md_build_dir(tmp_html)

    write_leeme()
    md_files = [*MD_TO_PDF, "LEEME.md"]

    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])

        for md_name in md_files:
            md_path = TEAM / md_name
            pdf_name = md_path.stem + ".pdf"
            borrador = "hoja-5" in md_name
            html_text = md_to_html_body(
                md_path.read_text(encoding="utf-8"), md_path.stem, borrador=borrador
            )
            html_path = tmp_html / (md_path.stem + ".html")
            html_path.write_text(html_text, encoding="utf-8")
            page = await browser.new_page()
            await page.goto(html_path.as_uri(), wait_until="networkidle")
            await page.pdf(
                path=str(OUT / pdf_name),
                format="A4",
                margin={"top": "12mm", "bottom": "12mm", "left": "12mm", "right": "12mm"},
                print_background=True,
            )
            await page.close()
            print("pdf", pdf_name)

        for html_name, pdf_name, opts in HTML_TO_PDF:
            html_path = PRINT / html_name
            page = await browser.new_page()
            await page.goto(html_path.as_uri(), wait_until="networkidle")
            pdf_opts = {
                "path": str(OUT / pdf_name),
                "format": opts.get("format", "A4"),
                "margin": {"top": "10mm", "bottom": "10mm", "left": "10mm", "right": "10mm"},
                "print_background": True,
            }
            if html_name == "prompts-ia-v2.html":
                pdf_opts["margin"] = {"top": "14mm", "bottom": "14mm", "left": "12mm", "right": "12mm"}
            if opts.get("landscape"):
                pdf_opts["landscape"] = True
                pdf_opts["margin"] = {"top": "0", "bottom": "0", "left": "0", "right": "0"}
                pdf_opts["prefer_css_page_size"] = True
                pdf_opts["scale"] = 1.0
            await page.pdf(**pdf_opts)
            await page.close()
            print("pdf", pdf_name)

        await browser.close()

    export_pdf_pngs(OUT / "plantilla-bmc.pdf", "plantilla-bmc")
    export_pdf_pngs(OUT / "prompts-ia-v2.pdf", "prompts-ia-v2")
    for md_name in md_files:
        stem = Path(md_name).stem
        export_pdf_pngs(OUT / f"{stem}.pdf", stem, max_pages=1)

    zip_path = ROOT / ZIP_NAME
    manifest_rows = []
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(TEAM / "LEEME.md", "LEEME.md")
        for pdf in sorted(OUT.glob("*.pdf")):
            if pdf.stem in {"test-notes"}:
                continue
            zf.write(pdf, pdf.name)
            manifest_rows.append((pdf.name, sha256_file(pdf)))

    manifest = [
        "# team-pack-es-manifest-sha256 (v0.4-es)",
        "",
        f"Zip: {ZIP_NAME} sha256 {sha256_file(zip_path)}",
        "",
        "| PDF | sha256 |",
        "|---|---|",
    ]
    for name, digest in manifest_rows:
        manifest.append(f"| {name} | `{digest}` |")
    (ROOT / "team-pack-es-manifest-sha256.md").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    print("zip", zip_path)
    print("zip_sha256", sha256_file(zip_path))


def field_name_audit() -> list[str]:
    """Return field tokens quoted in prompts that appear in hoja sources."""
    prompts_html = (PRINT / "prompts-ia-v2.html").read_text(encoding="utf-8")
    tokens = set(re.findall(r"\b(A1[0-5]|B[1-7]|S[1-6]|G[1-9]|[SQRFAGML]\b|VP1|Q-a|Q-b|Q-c|ABIERTO|REO)\b", prompts_html))
    sources = ""
    for name in ["hoja-1-mapa-de-calor.md", "hoja-2-flujo-de-datos.md", "hoja-3-dato-a-valor.md", "hoja-4-plantilla-tablero.md"]:
        sources += (TEAM / name).read_text(encoding="utf-8")
    matched = sorted(t for t in tokens if t in sources or (t == "VP1" and "VP1" in sources))
    report_path = OUT / "field-name-audit.json"
    OUT.mkdir(exist_ok=True)
    report_path.write_text(json.dumps({"matched": matched, "checked": sorted(tokens)}, indent=2), encoding="utf-8")
    return matched


def main() -> None:
    asyncio.run(render_all())
    matched = field_name_audit()
    print("field_names_matched", ",".join(matched))


if __name__ == "__main__":
    main()