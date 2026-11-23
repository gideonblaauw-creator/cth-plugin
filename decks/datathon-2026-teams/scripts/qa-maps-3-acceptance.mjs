#!/usr/bin/env node
/** maps-3 acceptance: slide 9 only (steps 11–19). */
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
const toolNode = path.resolve(deckRoot, "../../tools/reveal/node_modules");
const puppeteer = (await import(pathToFileURL(path.join(toolNode, "puppeteer-core/lib/esm/puppeteer/puppeteer-core.js")))).default;
const chrome = process.env.CHROME_PATH || "/usr/bin/google-chrome-stable";
const BASE = "ccd4f011fe3872456f1bd20c5ab15f6744ad6053";

const outLog = path.join("/opt/cursor/artifacts", "datathon-maps-3-acceptance.log");
const lines = [];
const log = (s) => {
  lines.push(s);
  console.log(s);
};

const head = execFileSync("git", ["-C", repoRoot, "rev-parse", "HEAD"], { encoding: "utf8" }).trim();
log(`HEAD=${head} (baseline for regression PDFs: ${BASE})`);

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

async function auditSlide9(lang, exportMode) {
  const fullUrl =
    exportMode && lang === "en"
      ? `http://127.0.0.1:${port}/index.html?lang=en&export=1`
      : exportMode
        ? `http://127.0.0.1:${port}/index.html?export=1`
        : `http://127.0.0.1:${port}/index.html?lang=${lang}`;
  await page.setViewport({ width: 1280, height: 720 });
  await page.goto(fullUrl, { waitUntil: "networkidle0", timeout: 120000 });
  await page.evaluate(() => {
    if (typeof Reveal !== "undefined") Reveal.slide(8);
  });
  await new Promise((r) => setTimeout(r, 600));
  return page.evaluate((lang) => {
    const scale = typeof Reveal !== "undefined" ? Reveal.getScale() : 1;
    const slide = document.querySelector(".reveal .slides section.present");
    const clipped = [];
    const walk = (el) => {
      if (!el || el.nodeType !== 1) return;
      const st = getComputedStyle(el);
      const overflowClip =
        st.overflow === "hidden" ||
        st.overflow === "clip" ||
        st.overflowY === "hidden" ||
        st.overflowY === "clip";
      const rect = el.getBoundingClientRect();
      for (const ch of el.children) {
        if (!(ch instanceof Element)) continue;
        const cr = ch.getBoundingClientRect();
        if (!(cr.width || cr.height)) continue;
        let a = ch.parentElement;
        while (a && a !== document.body) {
          const ast = getComputedStyle(a);
          const clip =
            ast.overflow === "hidden" ||
            ast.overflow === "clip" ||
            ast.overflowY === "hidden" ||
            ast.overflowY === "clip";
          if (clip) {
            const ar = a.getBoundingClientRect();
            if (cr.bottom > ar.bottom + 0.5 || cr.right > ar.right + 0.5 || cr.top < ar.top - 0.5 || cr.left < ar.left - 0.5) {
              const text = (ch.innerText || ch.alt || "").trim().slice(0, 80);
              if (text) clipped.push({ text, tag: ch.tagName, clipParent: a.className?.slice(0, 60) });
            }
            break;
          }
          a = a.parentElement;
        }
      }
      for (const ch of el.children) walk(ch);
    };
    if (slide) walk(slide);

    const textNodes = slide ? [...slide.querySelectorAll("*")].filter((el) => (el.innerText || "").trim()) : [];
    let minFont = 999;
    let maxRight = 0;
    for (const el of textNodes) {
    const st = getComputedStyle(el);
    const fs = parseFloat(st.fontSize) * scale;
    if (fs > 0 && fs < minFont) minFont = fs;
    const r = el.getBoundingClientRect();
    if (r.right > maxRight) maxRight = r.right;
  }
  const imgs = slide ? [...slide.querySelectorAll("img, table, .fp-living-lab-l1__source, .fp-living-lab-l1__notes, .fp-living-lab-l1__ica, .fp-foot")].map((el) => {
    const r = el.getBoundingClientRect();
    return { cls: el.className?.slice(0, 40) || el.tagName, l: r.left, t: r.top, r: r.right, b: r.bottom };
  }) : [];
  const overlaps = [];
  for (let i = 0; i < imgs.length; i++) {
    for (let j = i + 1; j < imgs.length; j++) {
      const a = imgs[i];
      const b = imgs[j];
      if (a.l < b.r && a.r > b.l && a.t < b.b && a.b > b.t) overlaps.push([a.cls, b.cls]);
    }
  }
  const body = slide?.innerText || "";
  const need = ["Colina", "Fontibón", "Mochuelo", "0–12", "251–500", "Anillo", "Círculo", "Fuente:"];
  const missing = need.filter((k) => !body.includes(k) && !(lang === "en" && k === "Anillo" && body.includes("Red ring")));
  return { scale, clipped, minFont, maxRight, overlaps, missing, imgs };
  }, lang);
}

log("\n## Step 11 — clipped text (slide 9)");
for (const lang of ["es", "en"]) {
  for (const mode of [false, true]) {
    const m = await auditSlide9(lang, mode);
    log(`[${lang} ${mode ? "export" : "screen"}] clipped=${m.clipped.length} ${JSON.stringify(m.clipped)}`);
    log(`[${lang} ${mode ? "export" : "screen"}] minFont=${m.minFont.toFixed(2)} maxRight=${m.maxRight.toFixed(1)} overlaps=${m.overlaps.length} missing=${JSON.stringify(m.missing)}`);
    if (m.imgs?.length) log(`[${lang} ${mode ? "export" : "screen"}] boxes=${JSON.stringify(m.imgs)}`);
  }
}

await browser.close();
server.close();

log("\n## Step 17 — PDF grep");
for (const pdf of ["datathon-2026-teams.pdf", "datathon-2026-teams-en.pdf"]) {
  const p = path.join(deckRoot, pdf);
  const txt = spawnSync("pdftotext", [p, "-"], { encoding: "utf8" }).stdout || "";
  const n = (txt.match(/descargar pdf|download pdf/gi) || []).length;
  const pages = spawnSync("pdfinfo", [p], { encoding: "utf8" }).stdout.match(/Pages:\s+(\d+)/)?.[1];
  log(`${pdf}: pages=${pages} grepPdfLabels=${n} sha256=${execFileSync("sha256sum", [p], { encoding: "utf8" }).split(" ")[0]}`);
}

log("\n## Step 18 — pdftoppm page 9");
for (const [lang, pdf] of [
  ["es", "datathon-2026-teams.pdf"],
  ["en", "datathon-2026-teams-en.pdf"],
]) {
  const p = path.join(deckRoot, pdf);
  const out = path.join(artDir, `slide-09-pdf-${lang}`);
  spawnSync("pdftoppm", ["-png", "-f", "9", "-l", "9", "-scale-to-x", "1280", "-scale-to-y", "720", p, out], { stdio: "inherit" });
  const png = fs.readdirSync(artDir).find((f) => f.startsWith(`slide-09-pdf-${lang}`) && f.endsWith(".png"));
  log(`${lang} page9: ${path.join(artDir, png || "")}`);
}

log("\n## Step 19 — regression vs ccd4f011 (pages 1–8, 10–21)");
const baseEs = "/tmp/maps3-base-es.pdf";
const baseEn = "/tmp/maps3-base-en.pdf";
execFileSync("bash", ["-c", `git -C ${repoRoot} show ${BASE}:decks/datathon-2026-teams/datathon-2026-teams.pdf > ${baseEs}`]);
execFileSync("bash", ["-c", `git -C ${repoRoot} show ${BASE}:decks/datathon-2026-teams/datathon-2026-teams-en.pdf > ${baseEn}`]);
const tmpDir = "/tmp/pdf-reg-maps3";
fs.mkdirSync(tmpDir, { recursive: true });
const pages = [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21];
for (const [label, cur, base] of [
  ["ES", path.join(deckRoot, "datathon-2026-teams.pdf"), baseEs],
  ["EN", path.join(deckRoot, "datathon-2026-teams-en.pdf"), baseEn],
]) {
  for (const pg of pages) {
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
w,h=im1.size;diff=0
for y in range(h):
 for x in range(w):
  p,q=im1.getpixel((x,y)),im2.getpixel((x,y))
  if max(abs(p[0]-q[0]),abs(p[1]-q[1]),abs(p[2]-q[2]))>40: diff+=1
print(f'{100*diff/(w*h):.4f}%')`,
        path.join(tmpDir, actualC),
        path.join(tmpDir, actualB),
      ],
      { encoding: "utf8" }
    );
    log(`${label} p${String(pg).padStart(2, "0")}: ${(py.stdout || "").trim()}`);
  }
}

log("\n## Step 20 — section byte-compare");
const curHtml = fs.readFileSync(path.join(deckRoot, "index.html"), "utf8");
const baseHtml = execFileSync("git", ["-C", repoRoot, "show", `${BASE}:decks/datathon-2026-teams/index.html`], { encoding: "utf8" });
const secRe = /<section[\s\S]*?<\/section>/g;
const curSecs = curHtml.match(secRe) || [];
const baseSecs = baseHtml.match(secRe) || [];
let only9 = true;
for (let i = 0; i < Math.max(curSecs.length, baseSecs.length); i++) {
  if ((curSecs[i] || "") !== (baseSecs[i] || "")) {
    log(`section ${i + 1} differs (${i === 8 ? "slide 9 expected" : "UNEXPECTED"})`);
    if (i !== 8) only9 = false;
  }
}
log(`only slide 9 section changed: ${only9}`);

fs.writeFileSync(outLog, lines.join("\n") + "\n");
log(`Wrote ${outLog}`);