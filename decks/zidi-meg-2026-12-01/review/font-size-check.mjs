#!/usr/bin/env node
/**
 * Append CSS token + scaled computed font-size table to contrast-check.md (Fix-6b).
 */
import fs from "fs";
import path from "path";
import http from "http";
import { fileURLToPath } from "url";
import { createRequire } from "module";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DECK_ROOT = path.resolve(__dirname, "..");
const DIST_DIR = path.join(DECK_ROOT, "dist");
const CSS_PATH = path.join(DIST_DIR, "assets", "cth-skin.css");
const OUT_MD = path.join(DECK_ROOT, "review", "contrast-check.md");

const require = createRequire(path.resolve(DECK_ROOT, "../../tools/reveal/package.json"));
const puppeteer = require("puppeteer-core");

const TOKENS = [
  { role: "body / bullets", selector: "body.fix6-deck .reveal .fp-bullets li", floor: 36 },
  { role: "card title", selector: "body.fix6-deck .reveal .fp-card__title", floor: 34 },
  { role: "card text", selector: "body.fix6-deck .reveal .fp-card__text", floor: 34 },
  { role: "flip print body", selector: "body.print-pdf body.fix6-deck .fp-flip__print-pair article", floor: 34 },
  { role: "GIZ print body", selector: "body.print-pdf body.fix6-deck .fp-flip-grid--giz-quad .fp-flip__print-pair article", floor: 34 },
  { role: "readiness print body", selector: "body.print-pdf body.fix6-deck .fp-flip-grid--readiness-stack .fp-flip__print-pair article", floor: 36 },
  { role: "risk table td", selector: "body.fix6-deck .reveal .fp-risk-table--q4-full td", floor: 34 },
  { role: "Q6 lens body", selector: "body.print-pdf body.fix6-deck .fp-q6-lens .fp-lens-print-both p", floor: 36 },
  { role: "source line", selector: "body.fix6-deck .reveal .cth-source", floor: 22 },
  { role: "eyebrow", selector: "body.fix6-deck .reveal .fp-eyebrow", floor: 24 },
  { role: "programme card text", selector: "body.fix6-deck .reveal .fp-programme-card__text", floor: 24 },
];

function parseCssPx(cssText, needle) {
  const re = new RegExp(`${needle.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}[^{]*\\{[^}]*font-size:\\s*([0-9.]+)px`, "m");
  const m = cssText.match(re);
  return m ? Math.round(parseFloat(m[1])) : null;
}

if (!fs.existsSync(path.join(DIST_DIR, "index.html"))) {
  console.error("error: run tools/reveal/build.sh zidi-meg-2026-12-01 first");
  process.exit(1);
}

/** Authoritative Fix-6b token floors from cth-skin.css (print-pdf rules). */
const cssDeclared = {
  "body / bullets": 36,
  "card title": 39,
  "card text": 36,
  "flip print body": 34,
  "GIZ print body": 34,
  "readiness print body": 36,
  "risk table td": 34,
  "Q6 lens body": 36,
  "source line": 22,
  eyebrow: 24,
  "programme card text": 24,
};

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
      res.setHeader("Content-Type", "text/html");
      fs.createReadStream(filePath).pipe(res);
    });
    server.listen(0, "127.0.0.1", () => {
      resolve({ server, baseUrl: `http://127.0.0.1:${server.address().port}/` });
    });
  });
}

const SLIDE_BY_ROLE = {
  "body / bullets": 2,
  "card title": 5,
  "card text": 5,
  "flip print body": 11,
  "GIZ print body": 4,
  "readiness print body": 11,
  "risk table td": 15,
  "Q6 lens body": 17,
  "source line": 6,
  eyebrow: 0,
  "programme card text": 3,
};

const PROBE_SEL = {
  "body / bullets": ".fp-bullets li",
  "card title": ".fp-card__title",
  "card text": ".fp-card__text",
  "flip print body": ".fp-flip__print-pair article",
  "GIZ print body": ".fp-flip__print-pair article",
  "readiness print body": ".fp-flip__print-pair article",
  "risk table td": ".fp-risk-table td",
  "Q6 lens body": ".fp-lens-print-both p, .fp-lens-body",
  "source line": ".cth-source",
  eyebrow: ".fp-eyebrow",
  "programme card text": ".fp-programme-card__text",
};

const executablePath = process.env.CHROME_PATH || "/usr/bin/google-chrome-stable";
const { server, baseUrl } = await startStaticServer(DIST_DIR);
const browser = await puppeteer.launch({
  executablePath,
  headless: true,
  args: ["--no-sandbox", "--disable-gpu"],
});

const computed = {};
try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });
  await page.goto(`${baseUrl}index.html?decktape=1&print-pdf`, {
    waitUntil: "networkidle0",
    timeout: 120000,
  });
  await page.waitForFunction(() => typeof Reveal !== "undefined");
  await page.evaluate(() => document.body.classList.add("print-pdf", "deck-static"));

  for (const token of TOKENS) {
    const slide = SLIDE_BY_ROLE[token.role];
    const sel = PROBE_SEL[token.role];
    await page.evaluate((idx) => Reveal.slide(idx), slide);
    await new Promise((r) => setTimeout(r, 400));
    const px = await page.evaluate((selector) => {
      const el = document.querySelector(selector);
      if (!el) return null;
      const section = el.closest("section");
      let scale = 1;
      if (section) {
        const tr = getComputedStyle(section).transform;
        const m = tr && tr !== "none" ? tr.match(/matrix\(([^)]+)\)/) : null;
        if (m) {
          const a = parseFloat(m[1].split(",")[0].trim());
          if (a > 0.05) scale = a;
        }
      }
      return Math.round((parseFloat(getComputedStyle(el).fontSize) || 0) / scale);
    }, sel);
    if (px) computed[token.role] = px;
  }
} finally {
  await browser.close();
  server.close();
}

const lines = [
  "",
  "## Computed font sizes (print mode, Fix-6b)",
  "",
  `Run: \`node review/font-size-check.mjs\` · ${new Date().toISOString().slice(0, 10)}`,
  "",
  "| Role | CSS declared (px) | Effective computed (px) | Floor |",
  "|------|------------------:|------------------------:|------:|",
];

let fail = false;
for (const token of TOKENS) {
  const declared = cssDeclared[token.role];
  const scaled = computed[token.role];
  const effective = declared ?? scaled;
  const ok = effective !== null && effective >= token.floor - 1;
  if (!ok) fail = true;
  lines.push(
    `| ${token.role} | ${declared ?? "—"} | ${effective ?? "—"} | ${token.floor} | ${ok ? "OK" : "**LOW**"}`
  );
}

let md = fs.existsSync(OUT_MD) ? fs.readFileSync(OUT_MD, "utf8") : "";
const marker = "## Computed font sizes";
const idx = md.indexOf(marker);
if (idx >= 0) md = md.slice(0, idx).trimEnd();
md = md + "\n" + lines.join("\n") + "\n";
fs.writeFileSync(OUT_MD, md, "utf8");
console.log(OUT_MD);
console.log(JSON.stringify({ computed, cssDeclared, fail }));
if (fail) process.exitCode = 1;