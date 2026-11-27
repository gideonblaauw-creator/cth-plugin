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
const DIST_HTML = path.join(DIST_DIR, "index.html");
const SLIDES = 19;
const PHOTO_SLIDES = [9];
const PHOTO_INDICES = PHOTO_SLIDES.map((n) => n - 1);

const require = createRequire(
  path.resolve(DECK_ROOT, "../../tools/reveal/package.json")
);
const puppeteer = require("puppeteer-core");

if (!fs.existsSync(DIST_HTML)) {
  console.error("error: run tools/reveal/build.sh zidi-meg-2026-12-01 first");
  process.exit(1);
}

const executablePath = process.env.CHROME_PATH || "/usr/bin/google-chrome-stable";

function contentType(filePath) {
  if (filePath.endsWith(".html")) return "text/html";
  if (filePath.endsWith(".css")) return "text/css";
  if (filePath.endsWith(".js")) return "application/javascript";
  if (filePath.endsWith(".jpg")) return "image/jpeg";
  if (filePath.endsWith(".png")) return "image/png";
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

async function captureDeck(page, baseUrl, outPrefix, count) {
  await page.goto(`${baseUrl}index.html`, { waitUntil: "networkidle0", timeout: 120000 });
  await page.waitForFunction(
    () => typeof Reveal !== "undefined" && Reveal.getTotalSlides() >= 1
  );
  const files = [];
  for (let i = 0; i < count; i++) {
    await page.evaluate((idx) => Reveal.slide(idx), i);
    await new Promise((r) => setTimeout(r, 400));
    const out = path.join(REVIEW, `${outPrefix}${String(i + 1).padStart(2, "0")}.png`);
    await page.screenshot({ path: out, type: "png" });
    files.push(out);
  }
  return { files };
}

const { server, baseUrl } = await startStaticServer(DIST_DIR);
const browser = await puppeteer.launch({
  executablePath,
  headless: true,
  args: ["--no-sandbox", "--disable-gpu"],
});

try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });
  const { files: slideFiles } = await captureDeck(page, baseUrl, "slide-", SLIDES);
  const contactPath = path.join(REVIEW, "contact-sheet.png");
  if (fs.existsSync("/usr/bin/montage")) {
    execSync(
      `montage ${slideFiles.map((f) => `"${f}"`).join(" ")} -tile 4x4 -geometry 480x270+4+4 -background white "${contactPath}"`,
      { stdio: "inherit" }
    );
  } else {
    console.warn("montage not installed; individual slides in review/");
  }
  console.log("capture ok:", slideFiles.length, "slides");
} finally {
  await browser.close();
  server.close();
}