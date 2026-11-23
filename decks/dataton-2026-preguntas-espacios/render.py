#!/usr/bin/env python3
"""Render A4 PDF and 200-dpi PNGs; fit space pages; DOM clearance check."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"
PDF_OUT = ROOT / "dataton-preguntas-espacios.pdf"
PNG_DIR = ROOT / "_png"
CONTACT_SHEET = ROOT / "_png" / "contact-sheet-200dpi.png"
FIT_REPORT = ROOT / "fit-report.json"

# A4 CSS px at 96dpi reference used in deck.css
PAGE_W = 794
PAGE_H = 1123
PNG_SCALE = 200 / 96  # 200-dpi output from CSS pixel layout


FIT_AND_CHECK_JS = """
() => {
  const LEVELS = [
    { id: "default", className: "" },
    { id: "fit-a", className: "page--fit-a" },
    { id: "fit-b", className: "page--fit-b" },
    { id: "fit-c", className: "page--fit-c" },
    { id: "fit-d", className: "page--fit-d" },
  ];

  const MIN_CLEAR_PX = 8;

  function lastTextEl(turn) {
    const nodes = [...turn.querySelectorAll(".pregunta, .anticipada, .repregunta")];
    return nodes.length ? nodes[nodes.length - 1] : null;
  }

  function clearanceForTurn(turn) {
    const last = lastTextEl(turn);
    if (!last) return { ok: true, clearancePx: 999 };
    const card = turn.getBoundingClientRect();
    const lastRect = last.getBoundingClientRect();
    const clearancePx = card.bottom - lastRect.bottom;
    return { ok: clearancePx >= MIN_CLEAR_PX - 0.5, clearancePx };
  }

  function pageMetrics(pg) {
    const turns = [...pg.querySelectorAll(".turn")];
    let minClear = 9999;
    let minPage = null;
    const turnIssues = [];
    for (const t of turns) {
      const scrollOk = t.scrollHeight <= t.clientHeight + 0.5;
      const { ok, clearancePx } = clearanceForTurn(t);
      if (clearancePx < minClear) minClear = clearancePx;
      if (!scrollOk || !ok) {
        turnIssues.push({
          scrollOk,
          clearancePx,
          scrollH: t.scrollHeight,
          clientH: t.clientHeight,
        });
      }
    }
    const pageOk = pg.scrollHeight <= pg.clientHeight + 0.5 && turnIssues.length === 0;
    return { pageOk, minClearPx: turns.length ? minClear : 9999, turnIssues, turnCount: turns.length };
  }

  const fitReport = [];
  const clearanceReport = { cardsChecked: 0, minClearancePt: 999, minPageId: null, failures: [] };

  document.querySelectorAll(".page--space").forEach((pg) => {
    const pageId = pg.id || pg.getAttribute("data-page") || "?";
    let chosen = null;
  let metrics = null;
    for (const lv of LEVELS) {
      pg.classList.remove("page--fit-a", "page--fit-b", "page--fit-c", "page--fit-d");
      if (lv.className) pg.classList.add(lv.className);
      metrics = pageMetrics(pg);
      if (metrics.pageOk) {
        chosen = lv.id;
        break;
      }
    }
    if (!chosen) chosen = "FAIL";
    const q = getComputedStyle(pg).getPropertyValue("--turn-q").trim() || "12pt";
    const a = getComputedStyle(pg).getPropertyValue("--turn-a").trim() || "10.5pt";
    fitReport.push({ pageId, fitLevel: chosen, questionPt: q, answerPt: a, ...metrics });

    [...pg.querySelectorAll(".turn")].forEach((t, idx) => {
      clearanceReport.cardsChecked += 1;
      const { ok, clearancePx } = clearanceForTurn(t);
      const scrollOk = t.scrollHeight <= t.clientHeight + 0.5;
      const clearPt = clearancePx * (72 / 96);
      if (clearPt < clearanceReport.minClearancePt) {
        clearanceReport.minClearancePt = clearPt;
        clearanceReport.minPageId = `${pageId}#turn${idx + 1}`;
      }
      if (!ok || !scrollOk) {
        clearanceReport.failures.push({
          pageId,
          turn: idx + 1,
          scrollOk,
          clearancePx,
          clearancePt: clearPt,
        });
      }
    });
  });

  if (clearanceReport.failures.length) {
    return { ok: false, fitReport, clearanceReport };
  }
  if (clearanceReport.minClearancePt === 999) clearanceReport.minClearancePt = 0;
  return { ok: true, fitReport, clearanceReport };
}
"""


def ensure_playwright():
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def make_contact_sheet() -> None:
    try:
        from PIL import Image
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "-q"])
        from PIL import Image

    paths = [PNG_DIR / f"p{i:02d}.png" for i in range(1, 18)]
    imgs = [Image.open(p) for p in paths]
    w, h = imgs[0].size
    cols, rows = 3, 6
    sheet = Image.new("RGB", (cols * w, rows * h), (232, 238, 244))
    for i, im in enumerate(imgs):
        x = (i % cols) * w
        y = (i // cols) * h
        sheet.paste(im, (x, y))
    sheet.save(CONTACT_SHEET)
    print("wrote", CONTACT_SHEET)


def main() -> None:
    ensure_playwright()
    from playwright.sync_api import sync_playwright

    if not INDEX.is_file():
        raise SystemExit("Run generate.py first")

    PNG_DIR.mkdir(parents=True, exist_ok=True)
    url = INDEX.as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = browser.new_page(
            viewport={"width": PAGE_W, "height": PAGE_H},
            device_scale_factor=PNG_SCALE,
        )
        page.goto(url, wait_until="networkidle")
        page.emulate_media(media="print")

        result = page.evaluate(FIT_AND_CHECK_JS)
        FIT_REPORT.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print("wrote", FIT_REPORT)

        if not result.get("ok"):
            print(json.dumps(result["clearanceReport"], indent=2), file=sys.stderr)
            for row in result.get("fitReport", []):
                if row.get("fitLevel") == "FAIL":
                    print("FAIL page", row, file=sys.stderr)
            raise SystemExit("DOM clearance / page fit check failed")

        pages = page.locator("section.page")
        count = pages.count()
        if count != 17:
            raise SystemExit(f"Expected 17 pages, got {count}")

        for i in range(count):
            out = PNG_DIR / f"p{i + 1:02d}.png"
            pages.nth(i).scroll_into_view_if_needed()
            pages.nth(i).screenshot(path=str(out))
            print("wrote", out)

        page.pdf(
            path=str(PDF_OUT),
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        print("wrote", PDF_OUT)
        browser.close()

    make_contact_sheet()
    cr = result["clearanceReport"]
    print(
        f"CLEARANCE OK: cards={cr['cardsChecked']} min={cr['minClearancePt']:.2f}pt at {cr['minPageId']}"
    )


if __name__ == "__main__":
    main()