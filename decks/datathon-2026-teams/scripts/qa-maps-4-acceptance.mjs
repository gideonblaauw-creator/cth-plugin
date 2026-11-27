#!/usr/bin/env node
/** maps-4: legend text collision fix acceptance. */
import fs from "fs";
import path from "path";
import { fileURLToPath, pathToFileURL } from "url";
import { spawnSync, execFileSync } from "child_process";
import { createServer } from "http";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const deckRoot = path.join(__dirname, "..");
const repoRoot = path.join(deckRoot, "../..");
const distDir = path.join(deckRoot, "dist");
const artDir = path.join(deckRoot, "artifacts");
const BASE = "663784c3fc079190c62dc171b75a646d465631de";
const outLog = path.join("/opt/cursor/artifacts", "datathon-maps-4-acceptance.log");
const lines = [];
const log = (s) => {
  lines.push(s);
  console.log(s);
};

const toolNode = path.resolve(deckRoot, "../../tools/reveal/node_modules");
const puppeteer = (await import(pathToFileURL(path.join(toolNode, "puppeteer-core/lib/esm/puppeteer/puppeteer-core.js")))).default;
const chrome = process.env.CHROME_PATH || "/usr/bin/google-chrome-stable";

function serveStatic(root) {
  return createServer((req, res) => {
    let p = req.url?.split("?")[0] || "/";
    if (p === "/") p = "/index.html";
    const fp = path.join(root, decodeURIComponent(p));
    if (!fp.startsWith(root) || !fs.existsSync(fp)) {
      res.writeHead(404);
      res.end("not found");
      return;
    }
    const ext = path.extname(fp);
    const types = { ".html": "text/html", ".css": "text/css", ".js": "application/javascript", ".png": "image/png" };
    res.writeHead(200, { "Content-Type": types[ext] || "application/octet-stream" });
    fs.createReadStream(fp).pipe(res);
  });
}

const server = serveStatic(distDir);
const port = await new Promise((resolve) => {
  server.listen(0, "127.0.0.1", () => resolve(server.address().port));
});

const browser = await puppeteer.launch({ executablePath: chrome, headless: true, args: ["--no-sandbox", "--disable-gpu"] });
const page = await browser.newPage();

async function measure(lang, exportMode) {
  const fullUrl =
    exportMode && lang === "en"
      ? `http://127.0.0.1:${port}/index.html?lang=en&export=1`
      : exportMode
        ? `http://127.0.0.1:${port}/index.html?export=1`
        : `http://127.0.0.1:${port}/index.html?lang=${lang}`;
  await page.setViewport({ width: 1280, height: 720 });
  await page.goto(fullUrl, { waitUntil: "networkidle0", timeout: 120000 });
  await page.evaluate(() => Reveal.slide(8));
  await new Promise((r) => setTimeout(r, 500));
  return page.evaluate((lang) => {
    const scale = Reveal.getScale();
    const slide = document.querySelector(".reveal .slides section.present");
    const visible = (el) => {
      const v = el.closest(".l-es, .l-en");
      if (!v) return true;
      const want = lang === "en" ? "l-en" : "l-es";
      return v.classList.contains(want);
    };

    function textRects(el) {
      const rects = [];
      const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
      let n;
      while ((n = walker.nextNode())) {
        if (!n.textContent.trim()) continue;
        if (!visible(n.parentElement)) continue;
        const range = document.createRange();
        range.selectNodeContents(n);
        const r = range.getBoundingClientRect();
        if (r.width > 0 && r.height > 0) rects.push({ rect: r, text: n.textContent.trim().slice(0, 40), el: n.parentElement });
      }
      return rects;
    }

    const allRects = slide ? textRects(slide) : [];
    let overlapCount = 0;
    for (let i = 0; i < allRects.length; i++) {
      for (let j = i + 1; j < allRects.length; j++) {
        const a = allRects[i].rect;
        const b = allRects[j].rect;
        const hOverlap = Math.min(a.right, b.right) - Math.max(a.left, b.left);
        const vOverlap = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
        if (hOverlap > 0.5 && vOverlap > 2) overlapCount++;
      }
    }

    const rows = slide ? [...slide.querySelectorAll(".fp-living-lab-l1__ica-row")] : [];
    const gaps = [];
    for (const row of rows) {
      const rangeEl = row.querySelector(".fp-living-lab-l1__ica-range");
      const labelEl = row.querySelector(".fp-living-lab-l1__ica-label");
      if (!rangeEl || !labelEl) continue;
      const labelSpan = labelEl.querySelector(lang === "en" ? ".l-en" : ".l-es");
      const rangeRects = textRects(rangeEl);
      const labelRects = labelSpan ? textRects(labelSpan) : textRects(labelEl);
      const rRight = Math.max(...rangeRects.map((x) => x.rect.right), -Infinity);
      const lLeft = Math.min(...labelRects.map((x) => x.rect.left), Infinity);
      gaps.push({ range: rangeEl.textContent.trim(), gap: +(lLeft - rRight).toFixed(2) });
    }

    const clipped = [];
    const walk = (el) => {
      for (const ch of el.children) {
        if (!(ch instanceof Element)) continue;
        const cr = ch.getBoundingClientRect();
        if (!(cr.width || cr.height)) continue;
        let a = ch.parentElement;
        while (a && a !== document.body) {
          const ast = getComputedStyle(a);
          if (ast.overflow === "hidden" || ast.overflow === "clip" || ast.overflowY === "hidden" || ast.overflowY === "clip") {
            const ar = a.getBoundingClientRect();
            if (cr.bottom > ar.bottom + 0.5 || cr.right > ar.right + 0.5) {
              const t = (ch.innerText || "").trim().slice(0, 50);
              if (t) clipped.push(t);
            }
            break;
          }
          a = a.parentElement;
        }
      }
      for (const ch of el.children) walk(ch);
    };
    if (slide) walk(slide);

    let minFont = 999;
    let maxRight = 0;
    for (const el of slide.querySelectorAll("*")) {
      if (!(el.innerText || "").trim()) continue;
      const fs = parseFloat(getComputedStyle(el).fontSize) * scale;
      if (fs > 0 && fs < minFont) minFont = fs;
      const r = el.getBoundingClientRect();
      if (r.right > maxRight) maxRight = r.right;
    }

    const tbodyRows = slide ? slide.querySelectorAll("tbody tr").length : 0;
    const body = slide?.innerText || "";
    const markers =
      lang === "en"
        ? body.includes("Red ring") && body.includes("Dashed circle")
        : body.includes("Anillo rojo") && body.includes("Círculo punteado");
    const bands = ["0–12", "13–37", "38–55", "56–150", "151–250", "251–500"].every((b) => body.includes(b));

    return { overlapCount, gaps, clipped: clipped.length, minFont, maxRight, tbodyRows, markers, bands };
  }, lang);
}

log(`BASE=${BASE}`);
log("\n## Step 6 — overlaps + legend gaps");
let totalOverlaps = 0;
for (const lang of ["es", "en"]) {
  for (const mode of [false, true]) {
    const m = await measure(lang, mode);
    totalOverlaps += m.overlapCount;
    log(`[${lang} ${mode ? "export" : "screen"}] overlapPairs=${m.overlapCount} gaps=${JSON.stringify(m.gaps)}`);
    log(`[${lang} ${mode ? "export" : "screen"}] clip=${m.clipped} minFont=${m.minFont.toFixed(2)} maxRight=${m.maxRight.toFixed(1)} rows=${m.tbodyRows} bands=${m.bands} markers=${m.markers}`);
  }
}
log(`total overlap pairs (all modes): ${totalOverlaps}`);

await browser.close();
server.close();

log("\n## Step 9 — PDF");
for (const pdf of ["datathon-2026-teams.pdf", "datathon-2026-teams-en.pdf"]) {
  const p = path.join(deckRoot, pdf);
  const txt = spawnSync("pdftotext", [p, "-"], { encoding: "utf8" }).stdout || "";
  const n = (txt.match(/descargar pdf|download pdf/gi) || []).length;
  const pages = spawnSync("pdfinfo", [p], { encoding: "utf8" }).stdout.match(/Pages:\s+(\d+)/)?.[1];
  log(`${pdf}: pages=${pages} grep=${n} sha256=${execFileSync("sha256sum", [p], { encoding: "utf8" }).split(" ")[0]}`);
}

log("\n## Step 11 — regression vs 663784c");
const baseEs = "/tmp/maps4-base-es.pdf";
const baseEn = "/tmp/maps4-base-en.pdf";
execFileSync("bash", ["-c", `git -C ${repoRoot} show ${BASE}:decks/datathon-2026-teams/datathon-2026-teams.pdf > ${baseEs}`]);
execFileSync("bash", ["-c", `git -C ${repoRoot} show ${BASE}:decks/datathon-2026-teams/datathon-2026-teams-en.pdf > ${baseEn}`]);
const tmpDir = "/tmp/pdf-reg-maps4";
fs.mkdirSync(tmpDir, { recursive: true });

function pageDiff(label, cur, base, pg) {
  spawnSync("pdftoppm", ["-png", "-f", String(pg), "-l", String(pg), "-scale-to-x", "1280", "-scale-to-y", "720", cur, path.join(tmpDir, `${label}-${pg}-cur`)], { stdio: "ignore" });
  spawnSync("pdftoppm", ["-png", "-f", String(pg), "-l", String(pg), "-scale-to-x", "1280", "-scale-to-y", "720", base, path.join(tmpDir, `${label}-${pg}-base`)], { stdio: "ignore" });
  const actualC = fs.readdirSync(tmpDir).find((f) => f.startsWith(`${label}-${pg}-cur`) && f.endsWith(".png"));
  const actualB = fs.readdirSync(tmpDir).find((f) => f.startsWith(`${label}-${pg}-base`) && f.endsWith(".png"));
  const py = spawnSync(
    "python3",
    [
      "-c",
      `from PIL import Image;import sys
a,b=sys.argv[1:3]
im1=Image.open(a).convert('RGB');im2=Image.open(b).convert('RGB')
if im1.size!=im2.size: im2=im2.resize(im1.size)
w,h=im1.size;xs=[];ys=[]
for y in range(h):
 for x in range(w):
  p,q=im1.getpixel((x,y)),im2.getpixel((x,y))
  if max(abs(p[0]-q[0]),abs(p[1]-q[1]),abs(p[2]-q[2]))>40:
   xs.append(x);ys.append(y)
pct=100*len(xs)/(w*h)
bb=(min(xs),min(ys),max(xs),max(ys)) if xs else None
print(f'{pct:.4f}% bbox={bb}')`,
      path.join(tmpDir, actualC),
      path.join(tmpDir, actualB),
    ],
    { encoding: "utf8" }
  );
  return (py.stdout || "").trim();
}

const pagesOther = [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21];
for (const [label, cur, base] of [
  ["ES", path.join(deckRoot, "datathon-2026-teams.pdf"), baseEs],
  ["EN", path.join(deckRoot, "datathon-2026-teams-en.pdf"), baseEn],
]) {
  for (const pg of pagesOther) log(`${label} p${String(pg).padStart(2, "0")}: ${pageDiff(label, cur, base, pg)}`);
  log(`${label} p09: ${pageDiff(label, cur, base, 9)}`);
}

fs.writeFileSync(outLog, lines.join("\n") + "\n");
log(`Wrote ${outLog}`);