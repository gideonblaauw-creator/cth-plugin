#!/usr/bin/env node
/**
 * Decktape print-mode: bounding-box overlap + sampled text contrast per slide.
 * Appends results to review/contrast-check.md
 */
import fs from "fs";
import path from "path";
import http from "http";
import { fileURLToPath } from "url";
import { createRequire } from "module";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DECK_ROOT = path.resolve(__dirname, "..");
const DIST_DIR = path.join(DECK_ROOT, "dist");
const REVIEW = path.join(DECK_ROOT, "review");
const OUT_MD = path.join(REVIEW, "contrast-check.md");

const require = createRequire(path.resolve(DECK_ROOT, "../../tools/reveal/package.json"));
const puppeteer = require("puppeteer-core");

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
  if (filePath.endsWith(".ttf")) return "font/ttf";
  if (filePath.endsWith(".woff2")) return "font/woff2";
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

const executablePath = process.env.CHROME_PATH || "/usr/bin/google-chrome-stable";
const { server, baseUrl } = await startStaticServer(DIST_DIR);
const browser = await puppeteer.launch({
  executablePath,
  headless: true,
  args: ["--no-sandbox", "--disable-gpu"],
});

try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });
  await page.goto(`${baseUrl}index.html?decktape=1`, { waitUntil: "networkidle0", timeout: 120000 });
  await page.waitForFunction(() => typeof Reveal !== "undefined" && Reveal.getTotalSlides() >= 1);
  const total = await page.evaluate(() => Reveal.getTotalSlides());

  const report = [];
  for (let i = 0; i < total; i++) {
    await page.evaluate((idx) => Reveal.slide(idx), i);
    await new Promise((r) => setTimeout(r, 500));
    const slideNum = i + 1;
    const data = await page.evaluate(() => {
      function relLuminance(rgb) {
        const f = (c) => {
          const s = c / 255;
          return s <= 0.04045 ? s / 12.92 : ((s + 0.055) / 1.055) ** 2.4;
        };
        const [r, g, b] = rgb.map(f);
        return 0.2126 * r + 0.7152 * g + 0.0722 * b;
      }
      function contrastRatio(fg, bg) {
        const l1 = relLuminance(fg);
        const l2 = relLuminance(bg);
        const lighter = Math.max(l1, l2);
        const darker = Math.min(l1, l2);
        return (lighter + 0.05) / (darker + 0.05);
      }
      function parseRgb(str) {
        if (!str || str === "transparent") return null;
        const m = str.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
        if (m) return [+m[1], +m[2], +m[3]];
        return null;
      }

      const section = document.querySelector(".reveal .slides section.present") ||
        document.querySelector(".reveal .slides section");
      if (!section) return { overlaps: [], contrastFails: [], overflow: false };

      const skip = new Set();
      section.querySelectorAll(".fp-photo-bg, .fp-photo-scrim, .fp-deco-wrap, script, style").forEach((el) => {
        skip.add(el);
      });

      const boxes = [];
      section.querySelectorAll("*").forEach((el) => {
        if (skip.has(el) || skip.has(el.parentElement)) return;
        const style = getComputedStyle(el);
        if (style.display === "none" || style.visibility === "hidden" || +style.opacity < 0.05) return;
        const rect = el.getBoundingClientRect();
        if (rect.width < 24 || rect.height < 12) return;
        const text = (el.innerText || "").trim();
        if (!text && !el.classList.contains("fp-card") && !el.classList.contains("fp-flip__print-pair")) return;
        boxes.push({
          tag: el.tagName,
          cls: (el.className || "").toString().slice(0, 80),
          left: rect.left,
          top: rect.top,
          right: rect.right,
          bottom: rect.bottom,
          text: text.slice(0, 40),
        });
      });

      const overlaps = [];
      const minArea = 1200;
      for (let a = 0; a < boxes.length; a++) {
        for (let b = a + 1; b < boxes.length; b++) {
          const A = boxes[a];
          const B = boxes[b];
          const dx = Math.min(A.right, B.right) - Math.max(A.left, B.left);
          const dy = Math.min(A.bottom, B.bottom) - Math.max(A.top, B.top);
          if (dx > 2 && dy > 2) {
            const area = dx * dy;
            if (area < minArea) continue;
            const nested =
              A.left <= B.left + 1 &&
              A.top <= B.top + 1 &&
              A.right >= B.right - 1 &&
              A.bottom >= B.bottom - 1;
            const nestedRev =
              B.left <= A.left + 1 &&
              B.top <= A.top + 1 &&
              B.right >= A.right - 1 &&
              B.bottom >= A.bottom - 1;
            if (nested || nestedRev) continue;
            overlaps.push({ a: A.cls || A.tag, b: B.cls || B.tag, px: Math.round(area) });
          }
        }
      }

      const contrastFails = [];
      section.querySelectorAll("p, h1, h2, h3, h4, li, td, span, article").forEach((el) => {
        const t = (el.innerText || "").trim();
        if (!t || t.length < 4) return;
        const rect = el.getBoundingClientRect();
        if (rect.width < 8 || rect.height < 8) return;
        const style = getComputedStyle(el);
        const fg = parseRgb(style.color);
        const bg = parseRgb(style.backgroundColor);
        if (!fg || !bg) return;
        const ratio = contrastRatio(fg, bg);
        const fs = parseFloat(style.fontSize) || 16;
        const large = fs >= 24 || style.fontWeight >= 600;
        const need = large ? 3 : 4.5;
        if (ratio < need - 0.05) {
          contrastFails.push({
            sample: t.slice(0, 50),
            ratio: Math.round(ratio * 100) / 100,
            need,
            fg: style.color,
            bg: style.backgroundColor,
          });
        }
      });

      const overflow = section.scrollHeight > section.clientHeight + 4;
      return { overlaps: overlaps.slice(0, 20), contrastFails: contrastFails.slice(0, 15), overflow };
    });
    report.push({ slide: slideNum, ...data });
  }

  const lines = [
    "",
    "## Automated PDF layout check (Fix-5b)",
    "",
    `Run: \`node review/pdf-layout-check.mjs\` · ${new Date().toISOString().slice(0, 10)} · ${total} slides (decktape print mode)`,
    "",
    "| Slide | Overflow | Overlap pairs | Contrast fails |",
    "|------:|:--------:|--------------:|---------------:|",
  ];
  let anyFail = false;
  for (const row of report) {
    const ov = row.overflow ? "YES" : "no";
    const oc = row.overlaps.length;
    const cf = row.contrastFails.length;
    if (row.overflow || oc > 0 || cf > 0) anyFail = true;
    lines.push(`| ${row.slide} | ${ov} | ${oc} | ${cf} |`);
  }
  lines.push("", "### Overlap detail", "");
  let overlapAny = false;
  for (const row of report) {
    if (!row.overlaps.length) continue;
    overlapAny = true;
    lines.push(`**Slide ${row.slide}**`);
    for (const o of row.overlaps) {
      lines.push(`- \`${o.a}\` × \`${o.b}\` — ~${o.px} px²`);
    }
    lines.push("");
  }
  if (!overlapAny) lines.push("_No non-nested overlap pairs above 1,200 px²._", "");

  lines.push("### Live contrast samples (failing only)", "");
  let cfAny = false;
  for (const row of report) {
    if (!row.contrastFails.length) continue;
    cfAny = true;
    lines.push(`**Slide ${row.slide}**`);
    for (const c of row.contrastFails) {
      lines.push(`- “${c.sample}” — ${c.ratio}:1 (need ${c.need}:1) · fg ${c.fg} on bg ${c.bg}`);
    }
    lines.push("");
  }
  if (!cfAny) lines.push("_No sampled text pairs below WCAG AA thresholds._", "");

  lines.push(`**Summary:** ${anyFail ? "REVIEW — see rows above" : "PASS — no overflow, overlap, or contrast failures detected."}`, "");

  let md = fs.existsSync(OUT_MD) ? fs.readFileSync(OUT_MD, "utf8") : "";
  const marker = "## Automated PDF layout check";
  const idx = md.indexOf(marker);
  if (idx >= 0) md = md.slice(0, idx).trimEnd();
  md = md + "\n" + lines.join("\n");
  fs.writeFileSync(OUT_MD, md, "utf8");
  console.log(OUT_MD);
  console.log(JSON.stringify({ slides: total, anyFail }));
  if (anyFail) process.exitCode = 1;
} finally {
  await browser.close();
  server.close();
}