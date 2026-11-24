#!/usr/bin/env python3
"""Run 5 self-checks for dataton team pack (glyphs, counts, cmap)."""
from __future__ import annotations

import hashlib
import io
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from docx import Document
from fontTools.ttLib import TTFont
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
OFL = ROOT / "fonts" / "open-sans" / "OpenSans-Regular.ttf"
ALLOWED_EMOJI = {0x1F7E5, 0x1F7E7, 0x1F7E6}
WHITESPACE = {9, 10, 11, 12, 13, 32, 160, 0x202F, 0x2003}

FILES = {
    "q_docx": ROOT / "cuestionario/Cuestionario-Dataton-24nov-equipos.docx",
    "ej_docx": ROOT / "cuestionario/Cuestionario-ejemplo-Air4U.docx",
    "guia_docx": ROOT / "guia-tecnica/Guia-tecnica-mentores.docx",
    "q_pdf": ROOT / "cuestionario/Cuestionario-Dataton-24nov-equipos.pdf",
    "ej_pdf": ROOT / "cuestionario/Cuestionario-ejemplo-Air4U.pdf",
    "guia_pdf": ROOT / "guia-tecnica/Guia-tecnica-mentores.pdf",
    "prompts": ROOT / "cuestionario/prompts.txt",
    "zip": ROOT / "team-pack-es-pdfs-v0.4.zip",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def docx_text(path: Path) -> str:
    doc = Document(path)
    parts: list[str] = []
    for p in doc.paragraphs:
        parts.append(p.text)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                parts.append(cell.text)
    return "\n".join(parts)


def count_chars(blob: str) -> dict[str, int]:
    return {
        "arrow": blob.count("\u2192"),
        "checkbox": blob.count("\u2610"),
        "sgl": blob.count("\u203a"),
        "boxdraw": sum(1 for c in blob if 0x2500 <= ord(c) <= 0x257F),
        "tri": blob.count("\u25b2") + blob.count("\u25ba"),
    }


def pdftotext_pages(pdf: Path) -> list[str]:
    out = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True, check=True)
    # per-page via layout
    pages = subprocess.run(
        ["pdftotext", "-f", "1", "-l", "9999", str(pdf), "-"],
        capture_output=True,
        text=True,
        check=True,
    )
    return pages.stdout.split("\f")


def glyph_scan_cmap(cmap: dict[int, str], texts: list[str], label: str) -> list[tuple[str, int, str]]:
    bad: list[tuple[str, int, str]] = []
    for text in texts:
        for ch in text:
            code = ord(ch)
            if code in WHITESPACE or code in ALLOWED_EMOJI:
                continue
            if code not in cmap:
                bad.append((label, code, ch))
    return bad


def main() -> int:
  report: list[str] = []
  cmap = TTFont(OFL).getBestCmap()

  for key in ("q_pdf", "ej_pdf", "guia_pdf"):
      r = subprocess.run(["pdffonts", str(FILES[key])], capture_output=True, text=True, check=True)
      report.append(f"## pdffonts {key}\n```\n{r.stdout.strip()}\n```\n")

  glyph_script = Path(__file__).read_text(encoding="utf-8")

  all_bad: list[tuple[str, int, str]] = []
  for pdf_key in ("q_pdf", "ej_pdf", "guia_pdf"):
      pages = pdftotext_pages(FILES[pdf_key])
      for i, page in enumerate(pages, 1):
          all_bad.extend(glyph_scan_cmap(cmap, [page], f"{pdf_key} p{i}"))

  for doc_key in ("q_docx", "ej_docx", "guia_docx"):
      all_bad.extend(glyph_scan_cmap(cmap, [docx_text(FILES[doc_key])], doc_key))

  report.append("## Glyph scan (OpenSans-Regular cmap)\n")
  report.append("Script: `scripts/run5_self_check.py` (this file).\n")
  if all_bad:
      report.append(f"FAIL: {len(all_bad)} out-of-cmap glyphs\n")
      for item in all_bad[:50]:
          report.append(f"- {item}\n")
      return 1
  report.append("Result: 0 out-of-cmap glyphs in all PDF pages and docx (except emoji + whitespace).\n")

  # embedded font proof
  reader = PdfReader(str(FILES["guia_pdf"]))
  embedded = None
  for page in reader.pages:
      res = page.get("/Resources")
      if not res:
          continue
      fonts = res.get("/Font", {})
      for name, fref in fonts.items():
          fobj = fref.get_object()
          base = fobj.get("/BaseFont", "")
          if "OpenSans" in str(base) and "Regular" in str(base):
              ff2 = fobj.get("/FontDescriptor", {}).get("/FontFile2")
              if ff2:
                  embedded = ff2.get_data()
                  break
      if embedded:
          break
  if not embedded:
      report.append("## Embedded font proof: FAIL no FontFile2\n")
      return 1

  with tempfile.NamedTemporaryFile(suffix=".ttf") as tmp:
      tmp.write(embedded)
      tmp.flush()
      emb = TTFont(tmp.name)

  committed = TTFont(OFL)
  ref_g = committed["glyf"]["g"]
  emb_matches = [
      gn
      for gn in emb.getGlyphOrder()
      if gn != ".notdef"
      and emb["glyf"][gn].numberOfContours == ref_g.numberOfContours
      and emb["glyf"][gn].endPtsOfContours == ref_g.endPtsOfContours
  ]
  same_outline = len(emb_matches) >= 1
  dejavu = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
  deja_match = False
  if dejavu.is_file():
      dj_g = TTFont(dejavu)["glyf"]["g"]
      deja_match = any(
          gn != ".notdef"
          and emb["glyf"][gn].numberOfContours == dj_g.numberOfContours
          and emb["glyf"][gn].endPtsOfContours == dj_g.endPtsOfContours
          for gn in emb.getGlyphOrder()
      )

  report.append("## Embedded font proof (guia.pdf OpenSans-Regular 'g')\n")
  report.append(f"- Font name table: `{emb['name'].getDebugName(4)}`\n")
  report.append(
      f"- Subset glyph(s) with same contour topology as committed `g`: **{emb_matches[:3]}** (match={same_outline})\n"
  )
  report.append(f"- Any subset glyph matching DejaVu `g` topology: **{deja_match}** (expect False)\n")

  import fitz

  doc = fitz.open(FILES["guia_pdf"])
  for i, page in enumerate(doc):
      if "gradas" in page.get_text().lower() or "guía técnica" in page.get_text():
          if "g" in page.get_text():
              clip = page.search_for("gradas")
              if not clip:
                  clip = page.search_for("Ninguno / Bronce")
              if clip:
                  rect = clip[0]
                  rect = fitz.Rect(rect.x0 - 10, rect.y0 - 5, rect.x1 + 200, rect.y1 + 20)
                  pix = page.get_pixmap(dpi=200, clip=rect)
                  out = ROOT / "_png/run5/glyph-g-line-200dpi.png"
                  pix.save(str(out))
                  report.append(f"- 200 dpi crop: `_png/run5/glyph-g-line-200dpi.png` (page {i+1})\n")
                  break
  doc.close()

  counts_report = []
  total_sgl = 0
  for key in ("q_docx", "ej_docx", "guia_docx"):
      c = count_chars(docx_text(FILES[key]))
      counts_report.append(f"{key} docx: {c}")
      total_sgl += c["sgl"]
  for key in ("q_pdf", "ej_pdf", "guia_pdf"):
      t = subprocess.run(["pdftotext", str(FILES[key]), "-"], capture_output=True, text=True).stdout
      c = count_chars(t)
      counts_report.append(f"{key} pdf text: {c}")
  report.append("## Character counts\n```\n" + "\n".join(counts_report) + f"\ntotal › in docx: {total_sgl}\n```\n")

  fc = subprocess.run(["fc-match", "Open Sans"], capture_output=True, text=True).stdout.strip()
  fcb = subprocess.run(["fc-match", "Open Sans:bold"], capture_output=True, text=True).stdout.strip()
  report.append(f"## fc-match\n```\n{fc}\n{fcb}\n```\n")

  shas = []
  for label, path in FILES.items():
      if path.is_file():
          shas.append((label, path.name, sha256(path)))
  for ttf in sorted((ROOT / "fonts/open-sans").glob("OpenSans-*.ttf")):
      shas.append((ttf.name, ttf.name, sha256(ttf)))

  report.append("## sha256\n| id | file | sha256 |\n|---|---|---|\n")
  for label, name, digest in shas:
      report.append(f"| {label} | {name} | `{digest}` |\n")

  head = subprocess.run(["git", "-C", str(ROOT.parent.parent), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
  report.insert(0, f"# Run 5 diff notes\n\nHead SHA (post-edits pending commit): `{head}`\n\n")

  out_path = ROOT / "run5-diff-notes.md"
  out_path.write_text("".join(report), encoding="utf-8")
  print("wrote", out_path)
  return 0


if __name__ == "__main__":
  raise SystemExit(main())