#!/usr/bin/env node
/** Acceptance measurements for datathon-maps-2 ticket. */
import fs from "fs";
import path from "path";
import { fileURLToPath, pathToFileURL } from "url";
import { spawnSync } from "child_process";
import { createServer } from "http";
import { execFileSync } from "child_process";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const deckRoot = path.join(__dirname, "..");
const distDir = path.join(deckRoot, "dist");
const toolNode = path.resolve(deckRoot, "../../tools/reveal/node_modules");
const puppeteer = (await import(pathToFileURL(path.join(toolNode, "puppeteer-core/lib/esm/puppeteer/puppeteer-core.js")))).default;
const chrome = process.env.CHROME_PATH || "/usr/bin/google-chrome-stable";

const outLog = path.join("/opt/cursor/artifacts", "datathon-maps-2-acceptance.log");
const lines = [];
const log = (s) => {
  lines.push(s);
  console.log(s);
};

function relLum(hex) {
  const h = hex.replace("#", "");
  const r = parseInt(h.slice(0, 2), 16) / 255;
  const g = parseInt(h.slice(2, 4), 16) / 255;
  const b = parseInt(h.slice(4, 6), 16) / 255;
  const f = (c) => (c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
  return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
}
function contrast(a, b) {
  const l1 = relLum(a);
  const l2 = relLum(b);
  const hi = Math.max(l1, l2);
  const lo = Math.min(l1, l2);
  return (hi + 0.05) / (lo + 0.05);
}

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
    const types = { ".html": "text/html", ".css": "text/css", ".js": "application/javascript", ".png": "image/png", ".svg": "image/svg+xml", ".pdf": "application/pdf" };
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
await page.setViewport({ width: 1280, height: 720 });

async function slideMeasure(lang, idx) {
  await page.goto(`http://127.0.0.1:${port}/index.html?lang=${lang}`, { waitUntil: "networkidle0", timeout: 120000 });
  await page.evaluate((i) => {
    if (typeof Reveal !== "undefined") Reveal.slide(i);
  }, idx);
  await new Promise((r) => setTimeout(r, 400));
  return page.evaluate(() => {
    const scale = typeof Reveal !== "undefined" ? Reveal.getScale() : 1;
    const slide = document.querySelector(".reveal .slides section.present");
    const nodes = slide ? [...slide.querySelectorAll("*")].filter((el) => {
      if (!(el.offsetWidth || el.offsetHeight)) return false;
      if (el.closest(".slide-number, .lang-toggle, .pdf-dl-fixed")) return false;
      const t = (el.innerText || "").trim();
      if (!t && el.tagName !== "IMG" && el.tagName !== "TABLE") return false;
      return true;
    }) : [];
    let minFont = 999;
    const rows = [];
    for (const el of nodes) {
      const st = getComputedStyle(el);
      const fs = parseFloat(st.fontSize) * scale;
      if (fs > 0 && (el.childNodes.length || el.tagName === "TD" || el.tagName === "TH")) {
        const txt = (el.innerText || "").slice(0, 40);
        if (txt) rows.push({ fs: +fs.toFixed(2), tag: el.tagName, txt });
        if (fs < minFont && txt) minFont = fs;
      }
    }
    const foot = slide?.querySelector(".fp-foot__text");
    const footRect = foot ? foot.getBoundingClientRect() : null;
    const tables = slide ? [...slide.querySelectorAll("table")] : [];
    const clips = [];
    for (const tb of tables) {
      let a = tb.parentElement;
      let clip = false;
      const rect = tb.getBoundingClientRect();
      while (a && a !== document.body) {
        const st = getComputedStyle(a);
        if ((st.overflow === "hidden" || st.overflowX === "hidden") && a.getBoundingClientRect().right < rect.right - 1) {
          clip = true;
          break;
        }
        a = a.parentElement;
      }
      clips.push({ right: +rect.right.toFixed(1), clip, x0: +rect.left.toFixed(1) });
    }
    const title = slide?.querySelector(".fp-title");
    const titleLeft = title ? title.getBoundingClientRect().left : null;
    const mapImg = slide?.querySelector(".fp-living-lab-l1__img");
    const mapH = mapImg ? mapImg.getBoundingClientRect().height : null;
    const src = slide?.querySelector(".cth-source.fp-source");
    const srcTop = src ? src.getBoundingClientRect().top : null;
    const footTop = foot ? foot.getBoundingClientRect().top : null;
    return { scale, minFont, rows: rows.sort((a, b) => a.fs - b.fs).slice(0, 8), footTop, footRect, titleLeft, mapH, srcTop, footToSrcGap: footTop && srcTop ? footTop - src.getBoundingClientRect().bottom : null, tableClips: clips };
  });
}

for (const lang of ["es", "en"]) {
  for (const idx of [2, 8, 9, 10, 20]) {
    const m = await slideMeasure(lang, idx);
    log(`[screen ${lang} slide ${idx + 1}] footTop=${m.footTop?.toFixed(1)} titleLeft=${m.titleLeft?.toFixed(1)} minFont=${m.minFont?.toFixed(2)} mapH=${m.mapH?.toFixed(1) ?? "n/a"} gapSrcFoot=${m.footToSrcGap?.toFixed(1) ?? "n/a"} tables=${JSON.stringify(m.tableClips)}`);
  }
}

await page.goto(`http://127.0.0.1:${port}/index.html?lang=es`, { waitUntil: "networkidle0" });
await page.evaluate(() => Reveal.slide(9));
await new Promise((r) => setTimeout(r, 300));
const btn10 = await page.evaluate(() => {
  const fixed = document.querySelector(".pdf-dl-fixed.l-es");
  const footBtn = document.querySelector("section.present .pdf-dl-btn.l-es");
  return { fixedHref: fixed?.getAttribute("href"), fixedDl: fixed?.getAttribute("download"), footHref: footBtn?.getAttribute("href"), footDl: footBtn?.getAttribute("download") };
});
log(`[slide10 ES buttons] ${JSON.stringify(btn10)}`);

await page.emulateMediaType("print");
const hidden = await page.evaluate(() => ({
  fixed: getComputedStyle(document.querySelector(".pdf-dl-fixed")).display,
  foot: getComputedStyle(document.querySelector(".pdf-dl-footer")).display,
}));
log(`[print visibility] ${JSON.stringify(hidden)}`);

for (const idx of [0, 6, 20]) {
  await page.emulateMediaType("screen");
  await page.goto(`http://127.0.0.1:${port}/index.html?lang=es`, { waitUntil: "networkidle0" });
  await page.evaluate((i) => Reveal.slide(i), idx);
  await new Promise((r) => setTimeout(r, 250));
  const c = await page.evaluate(() => {
    const btn = document.querySelector(".pdf-dl-fixed.l-es");
    const st = btn ? getComputedStyle(btn) : null;
    return { bg: st?.backgroundColor, color: st?.color };
  });
  log(`[contrast slide ${idx + 1}] colors ${JSON.stringify(c)}`);
}

await browser.close();
server.close();

const distHtml = path.join(distDir, "index.html");
log(`pdf-dl-btn count: ${(fs.readFileSync(distHtml, "utf8").match(/pdf-dl-btn/g) || []).length}`);
for (const pdf of ["datathon-2026-teams.pdf", "datathon-2026-teams-en.pdf"]) {
  const p = path.join(deckRoot, pdf);
  const txt = spawnSync("pdftotext", [p, "-"], { encoding: "utf8" }).stdout || "";
  const n = (txt.match(/descargar pdf|download pdf/gi) || []).length;
  const pages = spawnSync("pdfinfo", [p], { encoding: "utf8" }).stdout.match(/Pages:\s+(\d+)/)?.[1];
  log(`${pdf}: pages=${pages} grepPdfLabels=${n} sha256=${execFileSync("sha256sum", [p], { encoding: "utf8" }).split(" ")[0]}`);
}

// PDF regression vs 652c4aaf committed PDFs
const baseEs = "/tmp/base-es.pdf";
const baseEn = "/tmp/base-en.pdf";
execFileSync("bash", ["-c", `git -C ${deckRoot}/../.. show 652c4aaf:decks/datathon-2026-teams/datathon-2026-teams.pdf > ${baseEs}`]);
execFileSync("bash", ["-c", `git -C ${deckRoot}/../.. show 652c4aaf:decks/datathon-2026-teams/datathon-2026-teams-en.pdf > ${baseEn}`]);
const tmpDir = "/tmp/pdf-reg-maps2";
fs.mkdirSync(tmpDir, { recursive: true });
const pages = [1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21];
log("\n## PDF regression (max channel diff >40)");
for (const [label, cur, base] of [
  ["ES", path.join(deckRoot, "datathon-2026-teams.pdf"), baseEs],
  ["EN", path.join(deckRoot, "datathon-2026-teams-en.pdf"), baseEn],
]) {
  for (const pg of pages) {
    const cPng = path.join(tmpDir, `${label}-${pg}-cur.png`);
    const bPng = path.join(tmpDir, `${label}-${pg}-base.png`);
    spawnSync("pdftoppm", ["-png", "-f", String(pg), "-l", String(pg), "-scale-to-x", "1280", "-scale-to-y", "720", cur, path.join(tmpDir, `${label}-${pg}-cur`)], { stdio: "ignore" });
    spawnSync("pdftoppm", ["-png", "-f", String(pg), "-l", String(pg), "-scale-to-x", "1280", "-scale-to-y", "720", base, path.join(tmpDir, `${label}-${pg}-base`)], { stdio: "ignore" });
    const actualC = fs.readdirSync(tmpDir).find((f) => f.startsWith(`${label}-${pg}-cur`) && f.endsWith(".png"));
    const actualB = fs.readdirSync(tmpDir).find((f) => f.startsWith(`${label}-${pg}-base`) && f.endsWith(".png"));
    if (!actualC || !actualB) {
      log(`${label} page ${pg}: missing png`);
      continue;
    }
    const py = spawnSync(
      "python3",
      [
        "-c",
        `from PIL import Image
import sys
a,b=sys.argv[1:3]
pg=int(sys.argv[3])
im1=Image.open(a).convert('RGB'); im2=Image.open(b).convert('RGB')
if im1.size!=im2.size: im2=im2.resize(im1.size)
w,h=im1.size
diff=[]
for y in range(h):
  for x in range(w):
    p,q=im1.getpixel((x,y)),im2.getpixel((x,y))
    if max(abs(p[0]-q[0]),abs(p[1]-q[1]),abs(p[2]-q[2]))>40: diff.append((x,y))
pct=100*len(diff)/(w*h)
if diff:
  xs=[d[0] for d in diff]; ys=[d[1] for d in diff]
  bb=(min(xs),min(ys),max(xs),max(ys))
else: bb=None
# optional dy=1 offset check for 16/19
best=pct
if bb and pg in (16,19):
  for dy in (-2,-1,0,1,2):
    cnt=0
    for y in range(h):
      y2=y+dy
      if y2<0 or y2>=h: continue
      for x in range(w):
        p,q=im1.getpixel((x,y)),im2.getpixel((x,y2))
        if max(abs(p[0]-q[0]),abs(p[1]-q[1]),abs(p[2]-q[2]))>40: cnt+=1
    best=min(best,100*cnt/(w*h))
print(f'{pct:.4f}% bbox={bb} dy_best={best:.4f}%')`,
        path.join(tmpDir, actualC),
        path.join(tmpDir, actualB),
        String(pg),
      ],
      { encoding: "utf8" }
    );
    log(`${label} p${String(pg).padStart(2, "0")}: ${(py.stdout || py.stderr).trim()}`);
  }
}

fs.writeFileSync(outLog, lines.join("\n") + "\n");
log(`Wrote ${outLog}`);