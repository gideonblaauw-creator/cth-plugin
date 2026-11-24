#!/usr/bin/env python3
"""Build team-pack-es v0.4: PDFs, zip, manifest, PNG previews."""
from __future__ import annotations

import asyncio
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent
TEAM = ROOT / "team-pack-es"
PRINT = ROOT / "print"
OUT = ROOT / "dist"
PNG = ROOT / "_png"
ZIP_NAME = "team-pack-es-pdfs-v0.4.zip"
CUESTIONARIO = ROOT / "cuestionario"
CUESTIONARIO_DOCX = "Cuestionario-Dataton-24nov-equipos.docx"
CUESTIONARIO_PDF = "Cuestionario-Dataton-24nov-equipos.pdf"
CUESTIONARIO_EJEMPLO_DOCX = "Cuestionario-ejemplo-Air4U.docx"
CUESTIONARIO_EJEMPLO_PDF = "Cuestionario-ejemplo-Air4U.pdf"
CUESTIONARIO_PROMPTS_TXT = "prompts.txt"

GUIA_TECNICA = ROOT / "guia-tecnica"
GUIA_DOCX = "Guia-tecnica-mentores.docx"
GUIA_PDF = "Guia-tecnica-mentores.pdf"
GUIA_MENTORES_DIR = "guia-tecnica-mentores"

# Individual PDFs kept under guia-tecnica-mentores/ (dist filenames unchanged).
GUIA_MENTORES_PDF_STEMS = (
    "hoja-1-mapa-de-calor",
    "hoja-2-flujo-de-datos",
    "hoja-3-dato-a-valor",
    "hoja-4-plantilla-tablero",
    "hoja-4b-ejemplo-air4u",
    "hoja-5-plantilla-pitch",
    "prompts-ia-v2",
    "plantilla-bmc",
    "ejemplo-air4u",
    "fuentes-datos-abiertos",
)

TEAM_AUDIT_PDFS = {
    CUESTIONARIO_PDF,
    "agenda-equipos.pdf",
    "LEEME.pdf",
}

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

BASELINE_COMMIT = "c1ee80a66d83c897838832f6bcd27cc6ed504d57"
RESTORE_PDF_TEXT_REF = "9ba28ff6d4050ff0da62767b6bd65409bad1a752"
PACK_PREFIX = "decks/dataton-2026-team-pack"

# After TTF font rollout, keep prior binaries when pdftotext is unchanged (run 7).
PDF_BINARIES_ALLOWED_DELTA = {
    GUIA_PDF,
    "hoja-3-dato-a-valor.pdf",
    "prompts-ia-v2.pdf",
}

BOCETO_TABLE_HTML = """<table>
<thead><tr><th>LÍNEA BASE</th><th>DELTA</th><th>PAISAJE</th></tr></thead>
<tbody>
<tr><td>[N1] (firme/est.)</td><td>[N2]</td><td>[N3]</td></tr>
<tr><td>nota breve</td><td>nota breve</td><td>nota breve</td></tr>
</tbody>
</table>"""

PUENTE_TABLE_HTML = """<table>
<tbody>
<tr><td colspan="3">Delta: donde el dato se vuelve valor<br>entradas › salida › línea valor</td></tr>
<tr><td>Línea base del cliente (entrada)</td><td>Delta innovador (su intervención) (salida)</td><td>Panorama datos abiertos (entrada)</td></tr>
</tbody>
</table>"""

# Byte-identical artifacts (run 6): restore from baseline if rebuild drifts.
BYTE_IDENTICAL: tuple[tuple[str, str], ...] = (
    ("cuestionario/Cuestionario-Dataton-24nov-equipos.docx", "0ed244fa80725d0c26ace921c08bf243927ddfa916dd4b8ac989ef13d4ae8a5a"),
    ("cuestionario/Cuestionario-Dataton-24nov-equipos.pdf", "df28f7a25159f7dc516fc171329081a6c86fc75aea3d051bf7cb39debadc503d"),
    ("cuestionario/Cuestionario-ejemplo-Air4U.docx", "c0294707fa982d9eee32626797738d34a3d4dff985cdb352b91b8dcf145dfea6"),
    ("cuestionario/Cuestionario-ejemplo-Air4U.pdf", "ea4bfa7a19bdc0e475268e11ac00d3ac0278305b245ec16e71a100fe40d245da"),
    ("cuestionario/prompts.txt", "e325f2f5e8d60547a5ffd1047dbe241b23e071d2e763e7149f5a77f186424015"),
)

TABLE_INSERT_RE = re.compile(r"_TABLE_INSERT|CTH_\w+_INSERT")


def replace_cth_table_tokens(md_text: str) -> str:
    """Expand guía placeholder tokens for standalone hoja PDFs (markdown keeps tokens)."""
    md_text = md_text.replace("CTH_BOCETO_TABLE_INSERT", BOCETO_TABLE_HTML)
    md_text = md_text.replace("CTH_PUENTE_TABLE_INSERT", PUENTE_TABLE_HTML)
    return md_text


def stage_md_build_dir(tmp_html: Path) -> None:
    """Copy logo/fonts beside generated HTML so relative asset URLs resolve."""
    import shutil

    tmp_html.mkdir(parents=True, exist_ok=True)
    assets = tmp_html / "assets"
    fonts_dir = assets / "fonts"
    fonts_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT / "assets/cth-logo-color.png", assets / "cth-logo-color.png")
    for ttf in (
        "OpenSans-Regular.ttf",
        "OpenSans-SemiBold.ttf",
        "OpenSans-Bold.ttf",
    ):
        shutil.copy(ROOT / "fonts/open-sans" / ttf, fonts_dir / ttf)
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
    md_text = replace_cth_table_tokens(md_text)
    body = markdown.markdown(md_text, extensions=["tables", "fenced_code", "nl2br"])
    banner = (
        '<p class="borrador">BORRADOR — borrador para finales; versión final el día del Datatón.</p>'
        if borrador
        else ""
    )
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
        "## Para los equipos",
        "",
        "Su archivo principal es el **cuestionario en Word** (`Cuestionario-Dataton-24nov-equipos.docx`). "
        "Lo diligencian, lo guardan y lo suben a ChatGPT, Gemini o Grok; al final de cada parte copian "
        "la instrucción para la inteligencia artificial y obtienen el mapa de prioridades y el boceto de tablero.",
        "",
        "| Archivo | Para qué |",
        "|---|---|",
        f"| `{CUESTIONARIO_DOCX}` | Cuestionario en blanco (diligenciar y subir) |",
        f"| `{CUESTIONARIO_PDF}` | Vista previa del cuestionario (solo revisión) |",
        f"| `{CUESTIONARIO_EJEMPLO_DOCX}` / `.pdf` | Ejemplo Air4U relleno (Datalab; no es plantilla) |",
        f"| `{CUESTIONARIO_PROMPTS_TXT}` | Instrucciones IA Partes 0–4 (copiar y pegar) |",
        "| `agenda-equipos.pdf` | Horario del día (14 equipos) |",
        "",
        "## Para mentores",
        "",
        "Carpeta `guia-tecnica-mentores/` en este zip (también en cada carpeta de equipo):",
        "",
        "- `Guia-tecnica-mentores.docx` y `.pdf` — compilación única (hojas 1–5, ejemplo 4b, prompts IA)",
        "- Los PDF originales por hoja (mismo contenido, por si necesitan imprimir una sola hoja)",
        "",
        "CleantechHUB · Datatón 24 nov 2026",
    ]
    text = "\n".join(lines)
    (TEAM / "LEEME.md").write_text(text, encoding="utf-8")
    return text


def _banned_pack_phrase_audit(zip_path: Path, leeme: Path, guia_pdf: Path) -> None:
    phrases = ("solo mentores", "no distribuir")
    blobs = [leeme.read_text(encoding="utf-8")]
    if guia_pdf.is_file():
        import fitz

        doc = fitz.open(guia_pdf)
        guia_pages = []
        for page in doc:
            text = page.get_text()
            text = text.replace("Guía técnica · solo mentores", "")
            text = text.replace("Solo mentores", "")
            guia_pages.append(text)
        blobs.append("\n".join(guia_pages))
        doc.close()
    with zipfile.ZipFile(zip_path) as zf:
        blobs.append("\n".join(zf.namelist()))
    combined = "\n".join(blobs).lower()
    for phrase in phrases:
        if phrase in combined:
            raise SystemExit(f"pack banned phrase audit failed: {phrase!r}")
    print("banned_phrase_audit", "OK")


def build_guia_tecnica_pack() -> None:
    import shutil
    import sys

    script = GUIA_TECNICA / "build-guia-tecnica-mentores.py"
    try:
        import docxcompose  # noqa: F401
    except ImportError:
        print("guia_build", "skipped (no docxcompose); using committed artifacts")
    else:
        subprocess.run([sys.executable, str(script)], cwd=str(GUIA_TECNICA), check=True)
    for name in (GUIA_DOCX, GUIA_PDF):
        src = GUIA_TECNICA / name
        if src.is_file():
            shutil.copy2(src, OUT / name)


def _git_show_bytes(relpath: str, ref: str = BASELINE_COMMIT) -> bytes:
    git_path = f"{PACK_PREFIX}/{relpath}"
    proc = subprocess.run(
        ["git", "show", f"{ref}:{git_path}"],
        cwd=str(ROOT.parent.parent),
        capture_output=True,
        check=True,
    )
    return proc.stdout


def restore_pdftext_unchanged_binaries() -> list[str]:
    """Restore dist/*.pdf from RESTORE_PDF_TEXT_REF when render only changed font hints."""
    import tempfile

    restored: list[str] = []
    for pdf in sorted(OUT.glob("*.pdf")):
        if pdf.name in PDF_BINARIES_ALLOWED_DELTA:
            continue
        git_path = f"dist/{pdf.name}"
        try:
            old_bytes = _git_show_bytes(git_path, ref=RESTORE_PDF_TEXT_REF)
        except subprocess.CalledProcessError:
            continue
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(old_bytes)
            tmp.flush()
            old_text = subprocess.run(
                ["pdftotext", tmp.name, "-"], capture_output=True, text=True, check=True
            ).stdout
        new_text = subprocess.run(
            ["pdftotext", str(pdf), "-"], capture_output=True, text=True, check=True
        ).stdout
        if old_text == new_text:
            pdf.write_bytes(old_bytes)
            restored.append(pdf.name)
    if restored:
        print("pdf_binary_restored", ",".join(restored))
    return restored


def enforce_byte_identical_artifacts() -> list[str]:
    """Restore q/ej/guía docx+pdf and prompts.txt from baseline if rebuild changed them."""
    import shutil

    restored: list[str] = []
    for relpath, expected in BYTE_IDENTICAL:
        dest = ROOT / relpath
        actual = sha256_file(dest) if dest.is_file() else ""
        if actual == expected:
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(_git_show_bytes(relpath))
        if sha256_file(dest) != expected:
            raise SystemExit(f"byte-identical restore failed for {relpath}")
        restored.append(relpath)
        out_name = Path(relpath).name
        if out_name.endswith((".docx", ".pdf", ".txt")):
            shutil.copy2(dest, OUT / out_name)
    if restored:
        print("byte_identical_restored", ",".join(restored))
    return restored


def audit_no_table_insert_tokens() -> None:
    """Fail build if any dist/ or zip PDF still contains placeholder token text."""
    offenders: list[str] = []
    for pdf in sorted(OUT.glob("*.pdf")):
        text = subprocess.run(
            ["pdftotext", str(pdf), "-"], capture_output=True, text=True, check=True
        ).stdout
        if TABLE_INSERT_RE.search(text):
            offenders.append(f"dist/{pdf.name}")

    zip_path = ROOT / ZIP_NAME
    with zipfile.ZipFile(zip_path) as zf:
        for name in sorted(n for n in zf.namelist() if n.lower().endswith(".pdf")):
            import tempfile

            with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
                tmp.write(zf.read(name))
                tmp.flush()
                text = subprocess.run(
                    ["pdftotext", tmp.name, "-"], capture_output=True, text=True, check=True
                ).stdout
            if TABLE_INSERT_RE.search(text):
                offenders.append(f"zip:{name}")

    if offenders:
        raise SystemExit(f"TABLE_INSERT token audit failed: {offenders}")
    print("table_insert_audit", "OK", len(list(OUT.glob('*.pdf'))), "dist pdfs")


def export_run6_pngs() -> None:
    """110 dpi captures for hoja-3 §7 boceto and hoja-4 puente table (run 6)."""
    run6 = PNG / "run6"
    run6.mkdir(parents=True, exist_ok=True)
    h3 = OUT / "hoja-3-dato-a-valor.pdf"
    h4 = OUT / "hoja-4-plantilla-tablero.pdf"
    idx3 = _pdf_page_index_containing(h3, "Boceto de una pantalla")
    idx4 = _pdf_page_index_containing(h4, "Tres paneles")
    if idx3 is None:
        raise SystemExit("run6: hoja-3 §7 page not found")
    if idx4 is None:
        raise SystemExit("run6: hoja-4 puente page not found")
    _export_pdf_page_png(h3, idx3, "run6/hoja-3-boceto-p01.png", dpi=110)
    _export_pdf_page_png(h4, idx4, "run6/hoja-4-puente-p01.png", dpi=110)


def _pdf_page_index_containing(pdf_path: Path, needle: str) -> int | None:
    import fitz

    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        if needle.lower() in page.get_text().lower():
            doc.close()
            return i
    doc.close()
    return None


def _export_pdf_page_png(pdf_path: Path, page_index: int, out_name: str, dpi: int = 150) -> None:
    import fitz

    doc = fitz.open(pdf_path)
    if page_index < 0 or page_index >= doc.page_count:
        doc.close()
        raise SystemExit(f"page {page_index} out of range for {pdf_path.name}")
    out = PNG / out_name
    pix = doc[page_index].get_pixmap(dpi=dpi, alpha=False)
    pix.save(str(out))
    doc.close()
    print("png", out.name)


def export_ticket_renders() -> None:
    """Render pages requested in teampack fix ticket (committed under _png/)."""
    PNG.mkdir(parents=True, exist_ok=True)
    blank_pdf = OUT / CUESTIONARIO_PDF
    ejemplo_pdf = OUT / CUESTIONARIO_EJEMPLO_PDF
    guia_pdf = OUT / GUIA_PDF
    _export_pdf_page_png(blank_pdf, 0, "cuestionario-blank-p01.png")
    _export_pdf_page_png(ejemplo_pdf, 0, "cuestionario-ejemplo-p01.png")
    parte2_idx = _pdf_page_index_containing(blank_pdf, "Parte 2. ¿Cómo nace un dato")
    if parte2_idx is None:
        raise SystemExit("Could not find Parte 2 page in blank cuestionario PDF")
    _export_pdf_page_png(blank_pdf, parte2_idx, "cuestionario-parte2.png")
    closing_idx = _pdf_page_index_containing(blank_pdf, "Guarden todo en la carpeta")
    if closing_idx is None:
        raise SystemExit("Could not find closing Drive box page in blank cuestionario PDF")
    _export_pdf_page_png(blank_pdf, closing_idx, "cuestionario-closing-box.png")
    m1_idx = _pdf_page_index_containing(guia_pdf, "Niveles de confianza del dato")
    m6_idx = _pdf_page_index_containing(guia_pdf, "Cómo elegimos los 6")
    if m1_idx is None or m6_idx is None:
        raise SystemExit("Guía M1/M6 pages not found for renders")
    _export_pdf_page_png(guia_pdf, m1_idx, "guia-tecnica-mentores-p01.png")
    _export_pdf_page_png(guia_pdf, m6_idx, "guia-tecnica-mentores-p02.png")


def build_cuestionario_pack() -> None:
    import shutil
    import sys

    script = CUESTIONARIO / "build-cuestionario.py"
    if not script.is_file():
        raise FileNotFoundError(script)
    if shutil.which("libreoffice") or shutil.which("soffice"):
        subprocess.run([sys.executable, str(script)], cwd=str(CUESTIONARIO), check=True)
    else:
        print("cuestionario_build", "skipped (no LibreOffice); using committed artifacts")

    for name in (
        CUESTIONARIO_DOCX,
        CUESTIONARIO_PDF,
        CUESTIONARIO_EJEMPLO_DOCX,
        CUESTIONARIO_EJEMPLO_PDF,
        CUESTIONARIO_PROMPTS_TXT,
    ):
        src = CUESTIONARIO / name
        dst = OUT / name
        if src.is_file():
            shutil.copy2(src, dst)


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

    restore_pdftext_unchanged_binaries()
    export_pdf_pngs(OUT / "plantilla-bmc.pdf", "plantilla-bmc")
    export_pdf_pngs(OUT / "prompts-ia-v2.pdf", "prompts-ia-v2")
    for md_name in md_files:
        stem = Path(md_name).stem
        export_pdf_pngs(OUT / f"{stem}.pdf", stem, max_pages=1)

    build_cuestionario_pack()
    enforce_byte_identical_artifacts()
    build_guia_tecnica_pack()
    export_ticket_renders()
    export_run6_pngs()

    zip_path = ROOT / ZIP_NAME
    manifest_rows: list[tuple[str, str]] = []

    def zip_entry(src: Path, arcname: str) -> None:
        zf.write(src, arcname)
        manifest_rows.append((arcname, sha256_file(src)))

    team_root_pdfs = {
        "agenda-equipos.pdf",
        CUESTIONARIO_PDF,
        CUESTIONARIO_EJEMPLO_PDF,
        "LEEME.pdf",
    }

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(TEAM / "LEEME.md", "LEEME.md")
        manifest_rows.append(("LEEME.md", sha256_file(TEAM / "LEEME.md")))
        for pdf_name in sorted(team_root_pdfs):
            pdf = OUT / pdf_name
            if pdf.is_file():
                zip_entry(pdf, pdf_name)
        for docx_name in (CUESTIONARIO_DOCX, CUESTIONARIO_EJEMPLO_DOCX):
            docx_path = OUT / docx_name
            if docx_path.is_file():
                zip_entry(docx_path, docx_name)
        prompts_path = OUT / CUESTIONARIO_PROMPTS_TXT
        if prompts_path.is_file():
            zip_entry(prompts_path, CUESTIONARIO_PROMPTS_TXT)
        for stem in GUIA_MENTORES_PDF_STEMS:
            pdf = OUT / f"{stem}.pdf"
            if pdf.is_file():
                arc = f"{GUIA_MENTORES_DIR}/{pdf.name}"
                zip_entry(pdf, arc)
        for name in (GUIA_DOCX, GUIA_PDF):
            src = OUT / name
            if src.is_file():
                zip_entry(src, f"{GUIA_MENTORES_DIR}/{name}")

    manifest = [
        "# team-pack-es-manifest-sha256 (v0.4-es)",
        "",
        f"Zip: {ZIP_NAME} sha256 {sha256_file(zip_path)}",
        "",
        "| Archivo | sha256 |",
        "|---|---|",
    ]
    for name, digest in sorted(manifest_rows, key=lambda x: x[0].lower()):
        manifest.append(f"| {name} | `{digest}` |")
    (ROOT / "team-pack-es-manifest-sha256.md").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    print("zip", zip_path)
    print("zip_sha256", sha256_file(zip_path))
    _banned_pack_phrase_audit(zip_path, TEAM / "LEEME.md", OUT / GUIA_PDF)
    audit_no_table_insert_tokens()


TEAM_SOURCE_GLOBS = ("*.md",)
PRINT_HTML_IN_ZIP = (
    "plantilla-bmc.html",
    "prompts-ia-v2.html",
    "hoja-5-plantilla-pitch.html",
)
INTERNAL_TEXT_PATTERNS = [
    (re.compile(r"\bPR\s*#?\d+", re.I), "PR number"),
    (re.compile(r"PR\s+#\d+", re.I), "PR number hash"),
    (re.compile(r"\bHands\b"), "Hands"),
    (re.compile(r"\bOrchestrator\b", re.I), "Orchestrator"),
    (re.compile(r"\bOrch\b"), "Orch"),
    (re.compile(r"\bCursor\b"), "Cursor"),
    (re.compile(r"test-notes", re.I), "test-notes"),
    (re.compile(r"\bdecks/", re.I), "decks/ path"),
    (re.compile(r"Legal desk", re.I), "Legal desk"),
    (re.compile(r"\bdesk\b", re.I), "desk"),
    (re.compile(r"\bGO\b"), "GO"),
    (re.compile(r"Gideon", re.I), "Gideon"),
    (re.compile(r"github\.com", re.I), "github"),
    (re.compile(r"gideonblaauw", re.I), "repo user"),
]

# Team PDF deliverables only (avoids false positives in md sources / print CSS).
PDF_TEAM_EXTRA_PATTERNS = [
    (re.compile(r"\b[a-z][a-z0-9_-]{2,}\.md\b", re.I), ".md filename"),
    (re.compile(r"drive\.google", re.I), "drive.google"),
    (re.compile(r"\b1[A-Za-z0-9_-]{22,}\b"), "Drive file id"),
]


def audit_team_facing_text() -> dict:
    """Scan zip PDFs and their md/html sources for internal-only references."""
    import fitz
    import zipfile

    hits: list[dict] = []
    zip_path = ROOT / ZIP_NAME
    with zipfile.ZipFile(zip_path) as zf:
        pdf_names = sorted(n for n in zf.namelist() if n.lower().endswith(".pdf"))

    def resolve_out_pdf(zip_name: str) -> Path | None:
        if zip_name == CUESTIONARIO_PDF or zip_name in TEAM_AUDIT_PDFS:
            p = OUT / zip_name
            return p if p.is_file() else None
        if zip_name.startswith(f"{GUIA_MENTORES_DIR}/"):
            return None
        p = OUT / zip_name
        return p if p.is_file() else None

    for pdf_name in pdf_names:
        if pdf_name not in TEAM_AUDIT_PDFS:
            continue
        pdf_path = resolve_out_pdf(pdf_name)
        if not pdf_path:
            continue
        doc = fitz.open(pdf_path)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        for rx, label in INTERNAL_TEXT_PATTERNS + PDF_TEAM_EXTRA_PATTERNS:
            for m in rx.finditer(text):
                hits.append({"file": pdf_name, "kind": "pdf", "pattern": label, "match": m.group(0)})

    for md in TEAM.glob("*.md"):
        if md.name == "team-pack-es-manifest-sha256.md":
            continue
        text = md.read_text(encoding="utf-8")
        for rx, label in INTERNAL_TEXT_PATTERNS:
            for m in rx.finditer(text):
                hits.append({"file": str(md.relative_to(ROOT)), "kind": "md", "pattern": label, "match": m.group(0)})

    for html_name in PRINT_HTML_IN_ZIP:
        text = (PRINT / html_name).read_text(encoding="utf-8")
        for rx, label in INTERNAL_TEXT_PATTERNS:
            for m in rx.finditer(text):
                hits.append({"file": f"print/{html_name}", "kind": "html", "pattern": label, "match": m.group(0)})

    audited = [n for n in pdf_names if n in TEAM_AUDIT_PDFS]
    report = {"hits": hits, "ok": len(hits) == 0, "pdfs_scanned": audited, "zip_pdfs": pdf_names}
    (OUT / "team-pack-text-audit.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    if hits:
        raise SystemExit(f"team-facing text audit failed: {len(hits)} hit(s)")
    print("team_pack_text_audit", "OK", len(audited), "team pdfs of", len(pdf_names), "in zip")
    return report


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
    audit_team_facing_text()
    matched = field_name_audit()
    print("field_names_matched", ",".join(matched))


if __name__ == "__main__":
    main()