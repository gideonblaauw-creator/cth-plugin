#!/usr/bin/env node
import fs from "fs";
import path from "path";
import http from "http";
import { fileURLToPath } from "url";
import { createRequire } from "module";
import { execSync } from "child_process";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DECK_ROOT = path.resolve(__dirname, "..");
const REVIEW = path.join(DECK_ROOT, "review");
const DIST_DIR = path.join(DECK_ROOT, "dist");
const SLIDES = 15;

const require = createRequire(
  path.resolve(DECK_ROOT, "../../tools/reveal/package.json")
);
const puppeteer = require("puppeteer-core");
const executablePath = process.env.CHROME_PATH || "/usr/bin/google-chrome-stable";

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
      const port = server.address().port;
      resolve({ server, baseUrl: `http://127.0.0.1:${port}/` });
    });
  });
}

async function gotoSlide(page, idx) {
  await page.evaluate((i) => Reveal.slide(i), idx);
  await new Promise((r) => setTimeout(r, 600));
}

const { server, baseUrl } = await startStaticServer(DIST_DIR);
const browser = await puppeteer.launch({
  executablePath,
  headless: true,
  args: ["--no-sandbox", "--disable-gpu"],
});

try {
  for (const vp of [
    { name: "slide", w: 1920, h: 1080 },
    { name: "1280", w: 1280, h: 800 },
    { name: "390", w: 390, h: 844 },
  ]) {
    const page = await browser.newPage();
    await page.setViewport({ width: vp.w, height: vp.h, deviceScaleFactor: 1 });
    await page.goto(`${baseUrl}index.html`, { waitUntil: "networkidle0", timeout: 120000 });
    await page.waitForFunction(() => typeof Reveal !== "undefined");
    if (vp.name === "slide") {
      const files = [];
      for (let i = 0; i < SLIDES; i++) {
        await gotoSlide(page, i);
        const out = path.join(REVIEW, `slide-${String(i + 1).padStart(2, "0")}.png`);
        await page.screenshot({ path: out, type: "png" });
        files.push(out);
      }
      const contactPath = path.join(REVIEW, "contact-sheet.png");
      if (fs.existsSync("/usr/bin/montage")) {
        execSync(
          `montage ${files.map((f) => `"${f}"`).join(" ")} -tile 4x4 -geometry 480x270+4+4 -background white "${contactPath}"`,
          { stdio: "inherit" }
        );
      }
    }
    for (const idx of [2, 5, 10, 12]) {
      await gotoSlide(page, idx);
      await page.screenshot({
        path: path.join(REVIEW, `viewport-${vp.name}-slide-${idx + 1}.png`),
        type: "png",
      });
    }
    await page.close();
  }

  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });
  await page.goto(`${baseUrl}index.html`, { waitUntil: "networkidle0", timeout: 120000 });
  await page.waitForFunction(() => typeof Reveal !== "undefined");

  const shots = [
    {
      file: "interaction-ladder.png",
      slide: 3,
      async run() {
        await page.click(".fp-ladder-step:nth-child(3)");
        await new Promise((r) => setTimeout(r, 400));
      },
    },
    {
      file: "interaction-charts.png",
      slide: 5,
      async run() {
        await new Promise((r) => setTimeout(r, 800));
      },
    },
    {
      file: "interaction-investor-slider.png",
      slide: 10,
      async run() {
        await page.$eval("#ticket-slider", (el) => {
          el.value = "2";
          el.dispatchEvent(new Event("input", { bubbles: true }));
        });
        await new Promise((r) => setTimeout(r, 400));
      },
    },
    {
      file: "interaction-risk-table.png",
      slide: 12,
      async run() {
        await page.click(".fp-risk-table tbody tr:nth-child(3)");
        await new Promise((r) => setTimeout(r, 400));
      },
    },
  ];

  for (const s of shots) {
    await gotoSlide(page, s.slide);
    await s.run();
    await page.screenshot({ path: path.join(REVIEW, s.file), type: "png" });
  }

  console.log("interaction captures ok");
} finally {
  await browser.close();
  server.close();
}