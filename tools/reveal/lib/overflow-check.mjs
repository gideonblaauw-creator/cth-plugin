#!/usr/bin/env node
import fs from "fs";
import path from "path";
import puppeteer from "puppeteer-core";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const TOOL_ROOT = path.resolve(__dirname, "..");
const REPO_ROOT = path.resolve(TOOL_ROOT, "../..");

const slug = process.argv[2];
if (!slug) {
  console.error("Usage: overflow-check.mjs <slug>");
  process.exit(1);
}

const distHtml = path.join(REPO_ROOT, "decks", slug, "dist", "index.html");
if (!fs.existsSync(distHtml)) {
  console.error("error: dist/index.html missing — run build.sh first");
  process.exit(1);
}
const stat = fs.statSync(distHtml);
if (stat.size === 0) {
  console.error("error: dist/index.html is empty");
  process.exit(1);
}

const executablePath =
  process.env.CHROME_PATH || "/usr/bin/google-chrome-stable";

const browser = await puppeteer.launch({
  executablePath,
  headless: true,
  args: ["--no-sandbox", "--disable-gpu"],
});

try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });
  await page.goto(`file://${distHtml}`, {
    waitUntil: "networkidle0",
    timeout: 60000,
  });
  const { overflowSlides, lowContentSlides } = await page.evaluate(() => {
    const sections = [
      ...document.querySelectorAll(".reveal .slides section[data-cth-type]"),
    ];
    const bad = [];
    const shallow = [];
    sections.forEach((el, i) => {
      if (el.scrollHeight > el.clientHeight + 2) bad.push(i + 1);
      const slideRect = el.getBoundingClientRect();
      const slideH = slideRect.height || 1;
      let contentBottom = slideRect.top;
      for (const child of el.children) {
        if (child.tagName === "ASIDE") continue;
        const r = child.getBoundingClientRect();
        contentBottom = Math.max(contentBottom, r.bottom);
      }
      const used = (contentBottom - slideRect.top) / slideH;
      if (used < 0.5) shallow.push(i + 1);
    });
    return { overflowSlides: bad, lowContentSlides: shallow };
  });
  console.log(JSON.stringify({ overflowSlides, lowContentSlides }));
} finally {
  await browser.close();
}
