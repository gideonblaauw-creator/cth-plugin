#!/usr/bin/env python3
"""Render A4 PDF and 200-dpi PNGs; fit space pages; stack + card DOM audit."""
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

PAGE_W = 794
PAGE_H = 1123
PNG_SCALE = 200 / 96


FIT_AND_CHECK_JS = """
() => {
  const LEVELS = [
    { id: "default", className: "" },
    { id: "fit-a", className: "page--fit-a" },
    { id: "fit-b", className: "page--fit-b" },
    { id: "fit-c", className: "page--fit-c" },
    { id: "fit-d", className: "page--fit-d" },
    { id: "fit-e", className: "page--fit-e" },
  ];
  const FIT_CLASSES = LEVELS.map((l) => l.className).filter(Boolean);

  const MIN_CLEAR_PX = 8;
  const MIN_GAP_PX = 8;
  const GAP_TOL = 0.75;

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

  function stackElements(pg) {
    const els = [
      pg.querySelector(".page-head"),
      pg.querySelector(".strip-row"),
      ...pg.querySelectorAll(".turn"),
      pg.querySelector(".nota-moderacion"),
      pg.querySelector(".puente"),
      pg.querySelector(".fuente"),
    ];
    return els.filter(Boolean);
  }

  function stackCheck(pg) {
    const pageRect = pg.getBoundingClientRect();
    const padBottom = parseFloat(getComputedStyle(pg).paddingBottom) || 0;
    const innerBottom = pageRect.bottom - padBottom;
    const chain = stackElements(pg);
    const issues = [];
    let minGapPx = 9999;
    let minGapLabel = "";

    for (let i = 1; i < chain.length; i++) {
      const prev = chain[i - 1];
      const next = chain[i];
      const a = prev.getBoundingClientRect();
      const b = next.getBoundingClientRect();
      const gapPx = b.top - a.bottom;
      const label = `${prev.className.split(" ")[0]}→${next.className.split(" ")[0]}`;
      if (gapPx < minGapPx) {
        minGapPx = gapPx;
        minGapLabel = label;
      }
      if (gapPx < -0.5) {
        issues.push({ type: "overlap", label, gapPx });
      } else if (gapPx < MIN_GAP_PX - GAP_TOL) {
        issues.push({ type: "gap", label, gapPx, requiredPx: MIN_GAP_PX });
      }
    }

    const nota = pg.querySelector(".nota-moderacion");
    const puente = pg.querySelector(".puente");
    const fuente = pg.querySelector(".fuente");
    if (nota && puente) {
      const nr = nota.getBoundingClientRect();
      const pr = puente.getBoundingClientRect();
      if (nr.bottom > pr.top + 0.5) {
        issues.push({ type: "order", label: "nota-over-puente", gapPx: pr.top - nr.bottom });
      }
    }
    if (puente && fuente) {
      const pr = puente.getBoundingClientRect();
      const fr = fuente.getBoundingClientRect();
      if (pr.bottom > fr.top + 0.5) {
        issues.push({ type: "order", label: "puente-over-fuente", gapPx: fr.top - pr.bottom });
      }
    }
    if (fuente) {
      const fr = fuente.getBoundingClientRect();
      if (fr.bottom > innerBottom + 0.5) {
        issues.push({
          type: "fuente-overflow",
          label: "fuente-bottom",
          gapPx: innerBottom - fr.bottom,
        });
      }
    }

    if (minGapPx === 9999) minGapPx = 0;
    return {
      ok: issues.length === 0,
      issues,
      minGapPx,
      minGapPt: (minGapPx * 72) / 96,
      minGapLabel,
    };
  }

  function pageMetrics(pg) {
    const stack = stackCheck(pg);
    const turns = [...pg.querySelectorAll(".turn")];
    const turnIssues = [];
    let minClear = 9999;
    for (const t of turns) {
      const scrollOk = t.scrollHeight <= t.clientHeight + 0.5;
      const { ok, clearancePx } = clearanceForTurn(t);
      if (clearancePx < minClear) minClear = clearancePx;
      if (!scrollOk || !ok) {
        turnIssues.push({ scrollOk, clearancePx });
      }
    }
    const pageOk = stack.ok && turnIssues.length === 0;
    return {
      pageOk,
      stack,
      minClearPx: turns.length ? minClear : 9999,
      turnIssues,
      turnCount: turns.length,
    };
  }

  const fitReport = [];
  const stackReport = { pages: [], failures: [] };
  const clearanceReport = { cardsChecked: 0, minClearancePt: 999, minPageId: null, failures: [] };

  document.querySelectorAll(".page--space").forEach((pg) => {
    const pageId = pg.id || "?";
    let chosen = null;
    let metrics = null;
    for (const lv of LEVELS) {
      pg.classList.remove(...FIT_CLASSES);
      if (lv.className) pg.classList.add(lv.className);
      metrics = pageMetrics(pg);
      if (metrics.pageOk) {
        chosen = lv.id;
        break;
      }
    }
    if (!chosen) {
      chosen = "FAIL";
      pg.classList.remove(...FIT_CLASSES);
      pg.classList.add("page--fit-e");
      metrics = pageMetrics(pg);
    }
    const q = getComputedStyle(pg).getPropertyValue("--turn-q").trim() || "12pt";
    const a = getComputedStyle(pg).getPropertyValue("--turn-a").trim() || "10.5pt";
    const row = {
      pageId,
      fitLevel: chosen,
      questionPt: q,
      answerPt: a,
      stackOk: metrics.stack.ok,
      minStackGapPt: metrics.stack.minGapPt,
      minStackGapLabel: metrics.stack.minGapLabel,
      ...metrics,
    };
    fitReport.push(row);
    stackReport.pages.push({
      pageId,
      fitLevel: chosen,
      stackOk: metrics.stack.ok,
      minGapPt: metrics.stack.minGapPt,
      minGapLabel: metrics.stack.minGapLabel,
      issueCount: metrics.stack.issues.length,
    });
    if (!metrics.stack.ok) {
      stackReport.failures.push({ pageId, issues: metrics.stack.issues });
    }
    if (chosen === "FAIL") {
      stackReport.failures.push({ pageId, issues: [{ type: "fit-fail" }] });
    }

    [...pg.querySelectorAll(".turn")].forEach((t, idx) => {
      clearanceReport.cardsChecked += 1;
      const { ok, clearancePx } = clearanceForTurn(t);
      const scrollOk = t.scrollHeight <= t.clientHeight + 0.5;
      const clearPt = (clearancePx * 72) / 96;
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

  const fitFail = fitReport.some((r) => r.fitLevel === "FAIL");
  const ok =
    !fitFail && stackReport.failures.length === 0 && clearanceReport.failures.length === 0;
  if (clearanceReport.minClearancePt === 999) clearanceReport.minClearancePt = 0;
  return { ok, fitReport, stackReport, clearanceReport };
}
"""


def ensure_playwright():
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def verify_pdftotext_fuente(pdf: Path) -> list[str]:
    """Return offending page numbers if last line on pages 3–17 does not start with Fuente:"""
    bad: list[str] = []
    for n in range(3, 18):
        text = subprocess.check_output(
            ["pdftotext", "-layout", "-f", str(n), "-l", str(n), str(pdf), "-"],
            text=True,
            errors="replace",
        )
        lines = [ln for ln in text.splitlines() if ln.strip()]
        if not lines or not lines[-1].strip().startswith("Fuente:"):
            bad.append(f"p{n:02d}: {lines[-1][:80] if lines else '(empty)'}")
    return bad


def make_contact_sheet() -> None:
    try:
        from PIL import Image
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "-q"])
        from PIL import Image

    paths = [PNG_DIR / f"p{i:02d}.png" for i in range(1, 18)]
    imgs = [Image.open(p) for p in paths]
    w, h = imgs[0].size
    sheet = Image.new("RGB", (3 * w, 6 * h), (232, 238, 244))
    for i, im in enumerate(imgs):
        sheet.paste(im, ((i % 3) * w, (i // 3) * h))
    sheet.save(CONTACT_SHEET)


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
            print(json.dumps(result.get("stackReport", {}), indent=2), file=sys.stderr)
            print(json.dumps(result.get("clearanceReport", {}), indent=2), file=sys.stderr)
            raise SystemExit("DOM stack / clearance / fit check failed")

        pages = page.locator("section.page")
        if pages.count() != 17:
            raise SystemExit("Expected 17 pages")

        for i in range(17):
            out = PNG_DIR / f"p{i + 1:02d}.png"
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

    bad_fuente = verify_pdftotext_fuente(PDF_OUT)
    if bad_fuente:
        for line in bad_fuente:
            print("PDFTOTEXT FAIL", line, file=sys.stderr)
        raise SystemExit("pdftotext last-line Fuente: check failed")

    make_contact_sheet()
    sr = result["stackReport"]
    cr = result["clearanceReport"]
    print(
        f"STACK OK: {len(sr['pages'])} pages, failures={len(sr['failures'])}; "
        f"CARDS={cr['cardsChecked']} minClear={cr['minClearancePt']:.2f}pt @ {cr['minPageId']}"
    )


if __name__ == "__main__":
    main()