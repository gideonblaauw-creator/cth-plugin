#!/usr/bin/env node
/**
 * Fix-6c: per-slide computed font sizes in ?print-pdf + deck-static (decktape path).
 */
import fs from "fs";
import path from "path";
import http from "http";
import { fileURLToPath } from "url";
import { createRequire } from "module";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DECK_ROOT = path.resolve(__dirname, "..");
const DIST_DIR = path.join(DECK_ROOT, "dist");
const OUT_MD = path.join(DECK_ROOT, "review", "contrast-check.md");

const require = createRequire(path.resolve(DECK_ROOT, "../../tools/reveal/package.json"));
const puppeteer = require("puppeteer-core");

const ROLES = [
  { role: "body / bullets", sel: ".fp-bullets li", floor: 36 },
  { role: "card title", sel: ".fp-card__title", floor: 34 },
  { role: "card text", sel: ".fp-card__text", floor: 34 },
  { role: "flip print body", sel: ".fp-flip__print-pair article", floor: 34 },
  { role: "flip print label", sel: ".fp-flip__print-pair h4", floor: 24 },
  { role: "risk table td", sel: ".fp-risk-table td", floor: 34 },
  { role: "risk cell note", sel: ".fp-risk-table td .fp-risk-cell-note", floor: 22 },
  { role: "Q6 lens body", sel: ".fp-lens-print-both p, .fp-lens-body", floor: 36 },
  { role: "source line", sel: ".cth-source", floor: 22 },
  { role: "eyebrow", sel: ".fp-eyebrow", floor: 24 },
  { role: "giz action", sel: ".fp-giz-action", floor: 28 },
];

if (!fs.existsSync(path.join(DIST_DIR, "index.html"))) {
  console.error("error: run tools/reveal/build.sh zidi-meg-2026-12-01 first");
  process.exit(1);
}

function contentType(filePath) {
  if (filePath.endsWith(".html")) return "text/html";
  if (filePath.endsWith(".css")) return "text/css";
  if (filePath.endsWith(".js")) return "application/javascript";
  if (filePath.endsWith(".jpg")) return "image/jpeg";
  if (filePath.endsWith(".png")) return "image/png";
  if (filePath.endsWith(".woff2")) return "font/woff2";
  if (filePath.endsWith(".ttf")) return "font/ttf";
  return "application/octet-stream";
}

function startStaticServer(rootDir) {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      const rel = decodeURIComponent(req.url.split("?")[0]).replace(/^\//, "") || "index.html";
      const safe = path.normalize(rel).replace(/^(\.\.(\/|\\|$))+/, "");
      const filePath = path.join(rootDir, safe);
      if (!filePath.startsWith(rootDir) || !fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
        res.statusCode = 404;
        res.end("not found");
        return;
      }
      res.setHeader("Content-Type", contentType(filePath));
      fs.createReadStream(filePath).pipe(res);
    });
    server.listen(0, "127.0.0.1", () => {
      resolve({ server, baseUrl: `http://127.0.0.1:${server.address().port}/` });
    });
  });
}

function measuredPx(page, slideIndex, selector) {
  return page.evaluate(
    (idx, sel) => {
      const sections = document.querySelectorAll(".reveal .slides section.fp");
      const section = sections[idx];
      if (!section) return null;
      const el = section.querySelector(sel);
      if (!el) return null;
      return Math.round(parseFloat(getComputedStyle(el).fontSize) || 0);
    },
    slideIndex,
    selector
  );
}

const executablePath = process.env.CHROME_PATH || "/usr/bin/google-chrome-stable";
const { server, baseUrl } = await startStaticServer(DIST_DIR);
const browser = await puppeteer.launch({
  executablePath,
  headless: true,
  args: ["--no-sandbox", "--disable-gpu"],
});

const perSlide = [];
let fail = false;

try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });
  await page.goto(`${baseUrl}index.html?decktape=1&print-pdf`, {
    waitUntil: "networkidle0",
    timeout: 120000,
  });
  await page.waitForFunction(() => typeof Reveal !== "undefined");
  const total = await page.evaluate(() => document.querySelectorAll("section.fp").length);

  for (let i = 0; i < total; i++) {
    const row = { slide: i + 1, roles: {} };
    for (const { role, sel, floor } of ROLES) {
      const px = await measuredPx(page, i, sel);
      if (px === null) continue;
      row.roles[role] = px;
      if (px < floor - 1) fail = true;
    }
    perSlide.push(row);
  }
} finally {
  await browser.close();
  server.close();
}

const lines = [
  "",
  "## Computed font sizes — print-pdf mode (Fix-6c)",
  "",
  `Run: \`node review/font-size-check.mjs\` · ${new Date().toISOString().slice(0, 10)} · viewport 1920×1080`,
  "",
  "Values are **getComputedStyle** effective px (post-Reveal scale), not declared CSS.",
  "",
];

for (const { role, floor } of ROLES) {
  const header = `### ${role} (floor ≥${floor}px)`;
  lines.push(header, "");
  lines.push("| Slide | Computed (px) |");
  lines.push("|------:|--------------:|");
  for (const row of perSlide) {
    const px = row.roles[role];
    if (px === undefined) continue;
    const ok = px >= floor - 1;
    if (!ok) fail = true;
    lines.push(`| ${row.slide} | ${px}${ok ? "" : " **LOW**"} |`);
  }
  lines.push("");
}

let md = fs.existsSync(OUT_MD) ? fs.readFileSync(OUT_MD, "utf8") : "";
const marker = "## Computed font sizes";
const idx = md.indexOf(marker);
if (idx >= 0) md = md.slice(0, idx).trimEnd();
md = `${md}\n${lines.join("\n")}\n`;
fs.writeFileSync(OUT_MD, md, "utf8");

const summaryPath = path.join(DECK_ROOT, "review", "font-size-by-slide.json");
fs.writeFileSync(summaryPath, JSON.stringify({ perSlide, fail }, null, 2));

console.log(OUT_MD);
console.log(JSON.stringify({ slideCount: perSlide.length, fail }));
if (fail) process.exitCode = 1;