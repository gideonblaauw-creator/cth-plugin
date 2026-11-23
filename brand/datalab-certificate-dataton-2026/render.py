#!/usr/bin/env python3
"""Render Datatón 2026 participation certificates (A4 landscape PDF)."""
from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "template.html"
DEFAULT_FECHA = "24 de noviembre de 2026"
ROLES = frozenset({"Participante", "Mentor", "Jurado"})

EVENT_NAME = "el Datatón · Lanzamiento del Observatorio de la Tierra"


def ensure_playwright() -> None:
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def body_for_role(rol: str, fecha: str, equipo: str | None) -> str:
    lugar = f"celebrado el {fecha} en la Universidad Externado de Colombia, Bogotá."
    if rol == "Participante" and equipo:
        return (
            f"por su participación en {EVENT_NAME}, como integrante del equipo «{equipo}», {lugar}"
        )
    if rol == "Participante":
        return f"por su participación en {EVENT_NAME}, {lugar}"
    if rol == "Mentor":
        return f"por su participación como mentor en {EVENT_NAME}, {lugar}"
    if rol == "Jurado":
        return f"por su participación como jurado en {EVENT_NAME}, {lugar}"
    raise ValueError(f"rol must be one of {sorted(ROLES)}: {rol!r}")


def fill_template(nombre: str, rol: str, fecha: str, equipo: str | None) -> str:
    html = TEMPLATE.read_text(encoding="utf-8")
    body = body_for_role(rol, fecha, equipo)
    html = html.replace("{{NOMBRE}}", nombre)
    html = html.replace("{{NOMBRE_LENGTH}}", str(len(nombre)))
    html = html.replace("{{BODY}}", body)
    html = html.replace("{{FECHA}}", fecha)
    return html


def slugify(nombre: str, rol: str) -> str:
    nfkd = unicodedata.normalize("NFKD", nombre)
    ascii_name = nfkd.encode("ascii", "ignore").decode("ascii")
    ascii_name = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_name).strip("-").lower()
    ascii_rol = rol.lower()
    return f"{ascii_name}-{ascii_rol}"


def write_pdf(html: str, out: Path) -> None:
    ensure_playwright()
    from playwright.sync_api import sync_playwright

    out.parent.mkdir(parents=True, exist_ok=True)
    base_href = ROOT.as_uri().rstrip("/") + "/"
    if "<base " not in html:
        html = html.replace("<head>", f'<head>\n  <base href="{base_href}" />', 1)
    tmp = ROOT / ".render-tmp.html"
    tmp.write_text(html, encoding="utf-8")

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = browser.new_page(viewport={"width": 1123, "height": 794})
        page.goto(tmp.resolve().as_uri(), wait_until="networkidle")
        page.evaluate("() => document.fonts.ready")
        page.wait_for_timeout(300)
        page.emulate_media(media="print")
        page.pdf(
            path=str(out),
            format="A4",
            landscape=True,
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            prefer_css_page_size=True,
        )
        browser.close()
    tmp.unlink(missing_ok=True)


def render_one(nombre: str, rol: str, fecha: str, equipo: str | None, out: Path) -> None:
    if rol not in ROLES:
        raise SystemExit(f"Invalid --rol {rol!r}")
    html = fill_template(nombre, rol, fecha or DEFAULT_FECHA, equipo)
    write_pdf(html, out)
    print("wrote", out)


def merge_pdfs(paths: list[Path], out: Path) -> None:
    try:
        from pypdf import PdfWriter
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf", "-q"])
        from pypdf import PdfWriter

    writer = PdfWriter()
    for path in paths:
        writer.append(str(path))
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("wb") as fh:
        writer.write(fh)
    print("wrote", out)


def run_csv(csv_path: Path, outdir: Path) -> list[Path]:
    paths: list[Path] = []
    with csv_path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            nombre = (row.get("nombre") or "").strip()
            rol = (row.get("rol") or "").strip()
            equipo = (row.get("equipo") or "").strip() or None
            fecha = (row.get("fecha") or "").strip() or DEFAULT_FECHA
            if not nombre or not rol:
                raise SystemExit(f"Missing nombre/rol in row: {row}")
            out = outdir / f"{slugify(nombre, rol)}.pdf"
            render_one(nombre, rol, fecha, equipo, out)
            paths.append(out)
    if paths:
        merge_pdfs(paths, outdir / "all.pdf")
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Render Datalab Datatón certificates")
    parser.add_argument("--nombre", help="Participant name")
    parser.add_argument("--rol", choices=sorted(ROLES))
    parser.add_argument("--equipo", default=None, help="Team name (Participante only)")
    parser.add_argument("--fecha", default=DEFAULT_FECHA)
    parser.add_argument("--out", type=Path, help="Output PDF path")
    parser.add_argument("--csv", type=Path, help="Batch CSV path")
    parser.add_argument("--outdir", type=Path, help="Batch output directory")
    args = parser.parse_args()

    if args.csv:
        outdir = args.outdir or ROOT / "review" / "batch"
        run_csv(args.csv, outdir)
        return

    if not args.nombre or not args.rol or not args.out:
        parser.error("Single mode needs --nombre, --rol, and --out")

    render_one(args.nombre, args.rol, args.fecha, args.equipo, args.out)


if __name__ == "__main__":
    main()