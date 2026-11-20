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
const FODESEP_HTML = process.env.FODESEP_HTML || "";
const SLIDES = 11;
const PHOTO_SLIDES = [1, 2, 7, 9, 11];
const PHOTO_INDICES = PHOTO_SLIDES.map((n) => n - 1);

const require = createRequire(
  path.resolve(DECK_ROOT, "../../tools/reveal/package.json")
);
const puppeteer = require("puppeteer-core");

if (!fs.existsSync(DIST_HTML)) {
  console.error("error: run tools/reveal/build.sh observatorio-tierra-dataton first");
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

async function waitPhotoLayers(page) {
  await page.evaluate(async () => {
    const urls = [...document.querySelectorAll(".fp-photo-bg")].map((el) => {
      const bg = getComputedStyle(el).backgroundImage;
      const m = bg && bg.match(/url\(["']?([^"')]+)["']?\)/);
      return m ? m[1] : null;
    });
    await Promise.all(
      urls.filter(Boolean).map(
        (url) =>
          new Promise((resolve, reject) => {
            const img = new Image();
            img.onload = () => resolve();
            img.onerror = () => reject(new Error(`failed: ${url}`));
            img.src = url;
          })
      )
    );
    if (document.fonts && document.fonts.ready) await document.fonts.ready;
  });
}

async function captureDeck(page, baseUrl, outPrefix, count) {
  await page.goto(`${baseUrl}index.html`, { waitUntil: "networkidle0", timeout: 120000 });
  await page.waitForFunction(
    () => typeof Reveal !== "undefined" && Reveal.getTotalSlides() >= 1
  );
  await waitPhotoLayers(page);

  const computed = {};
  for (const idx of PHOTO_INDICES) {
    await page.evaluate((i) => Reveal.slide(i), idx);
    await new Promise((r) => setTimeout(r, 500));
    computed[idx + 1] = await page.evaluate(() => {
      const bg = document.querySelector("section.present .fp-photo-bg");
      if (!bg) return null;
      const cs = getComputedStyle(bg);
      return {
        position: cs.position,
        height: cs.height,
        heightPx: parseFloat(cs.height) || 0,
      };
    });
  }

  const files = [];
  for (let i = 0; i < count; i++) {
    await page.evaluate((idx) => {
      Reveal.slide(idx);
      document.querySelectorAll(".fragment").forEach((f) => f.classList.add("visible"));
    }, i);
    await new Promise((r) => setTimeout(r, 500));
    const out = path.join(REVIEW, `${outPrefix}${String(i + 1).padStart(2, "0")}.png`);
    await page.screenshot({ path: out, type: "png" });
    files.push(out);
  }
  return { files, computed };
}

const WHITE_RATIO_PY = path.join(__dirname, "white_ratio.py");

function whiteRatioPng(pngPath, opts = {}) {
  const args = [
    WHITE_RATIO_PY,
    pngPath,
    String(opts.y0 ?? 0),
    ...(opts.y1 != null ? [String(opts.y1)] : []),
  ];
  const out = execSync(`python3 ${args.map((a) => JSON.stringify(a)).join(" ")}`, {
    encoding: "utf8",
  }).trim();
  return parseFloat(out);
}

const { server, baseUrl } = await startStaticServer(DIST_DIR);

const browser = await puppeteer.launch({
  executablePath,
  headless: true,
  args: ["--no-sandbox", "--disable-gpu"],
});

let qaReport = { computed: {}, whiteRatios: {}, fileSizes: {} };
let fail = false;

try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });

  const { files: slideFiles, computed } = await captureDeck(page, baseUrl, "slide-", SLIDES);
  qaReport.computed = computed;

  for (const n of PHOTO_SLIDES) {
    const c = computed[n];
    if (!c || c.position !== "absolute" || c.heightPx < 1000) {
      console.error(`error: slide ${n} .fp-photo-bg position=${c?.position} height=${c?.height}`);
      fail = true;
    }
  }

  const hashes = slideFiles.map((f) =>
    execSync(`md5sum "${f}"`, { encoding: "utf8" }).trim().split(/\s+/)[0]
  );
  const unique = new Set(hashes);
  console.log("slide hashes:", hashes.join(" "));
  console.log("unique count:", unique.size);
  if (unique.size !== SLIDES) {
    console.error(`error: expected ${SLIDES} distinct screenshot hashes, got ${unique.size}`);
    fail = true;
  }

  for (const n of PHOTO_SLIDES) {
    const f = path.join(REVIEW, `slide-${String(n).padStart(2, "0")}.png`);
    const size = fs.statSync(f).size;
    qaReport.fileSizes[n] = size;
    let ratio;
    if (n === 7 || n === 9) {
      ratio = whiteRatioPng(f, { y0: 0, y1: 200 });
      if (ratio >= 0.3) {
        console.error(`error: slide ${n} top-band white ratio ${(ratio * 100).toFixed(1)}% >= 30%`);
        fail = true;
      }
    } else {
      ratio = whiteRatioPng(f);
      if (ratio >= 0.25) {
        console.error(`error: slide ${n} white ratio ${(ratio * 100).toFixed(1)}% >= 25%`);
        fail = true;
      }
    }
    qaReport.whiteRatios[n] = ratio;
    console.log(`slide ${n}: white ratio ${(ratio * 100).toFixed(2)}%, size ${size} bytes`);
  }

  const contactPath = path.join(REVIEW, "contact-sheet.png");
  const makeSheet = path.join(__dirname, "make_contact_sheet.py");
  if (fs.existsSync("/usr/bin/montage")) {
    execSync(
      `montage ${slideFiles.map((f) => `"${f}"`).join(" ")} -tile 4x3 -geometry 480x270+4+4 -background white "${contactPath}"`,
      { stdio: "inherit" }
    );
  } else {
    execSync(`python3 "${makeSheet}"`, { stdio: "inherit" });
  }

  const refsDir = path.join(REVIEW, "refs");
  fs.mkdirSync(refsDir, { recursive: true });

  const fodeMap = [
    { type: "cover", fodeIndex: 0 },
    { type: "statement", fodeIndex: 2 },
    { type: "title-bullets", fodeIndex: 11 },
    { type: "ecosystem", fodeIndex: 5 },
    { type: "key-facts", fodeIndex: 19 },
    { type: "partner-cards", fodeIndex: 5 },
    { type: "focus-areas", fodeIndex: 7 },
    { type: "process", fodeIndex: 7 },
    { type: "closing", fodeIndex: 22 },
  ];

  if (FODESEP_HTML && fs.existsSync(FODESEP_HTML)) {
    await page.goto(`file://${FODESEP_HTML}`, { waitUntil: "networkidle0", timeout: 120000 });
    await page.waitForFunction(() => typeof Reveal !== "undefined");
    for (const { type, fodeIndex } of fodeMap) {
      await page.evaluate((idx) => Reveal.slide(idx), fodeIndex);
      await new Promise((r) => setTimeout(r, 300));
      const ref = path.join(refsDir, `fodesep-${type}.png`);
      await page.screenshot({ path: ref, type: "png" });
      const eoIdx = {
        cover: 1,
        statement: 2,
        "title-bullets": 3,
        ecosystem: 4,
        "partner-cards": 5,
        "key-facts": 6,
        "focus-areas": 7,
        process: 9,
        closing: 11,
      }[type];
      if (!eoIdx) continue;
      const eo = path.join(REVIEW, `slide-${String(eoIdx).padStart(2, "0")}.png`);
      const cmp = path.join(refsDir, `compare-${type}.png`);
      if (fs.existsSync("/usr/bin/montage")) {
        execSync(
          `montage "${eo}" "${ref}" -tile 2x1 -geometry 960x540+8+8 -label "${type}" -background "#f5f5f5" "${cmp}"`,
          { stdio: "inherit" }
        );
      }
    }
  }

  fs.writeFileSync(
    path.join(REVIEW, "hashes.txt"),
    slideFiles.map((f, i) => `${hashes[i]}  ${path.basename(f)}`).join("\n") + "\n"
  );
  fs.writeFileSync(path.join(REVIEW, "qa-metrics.json"), JSON.stringify(qaReport, null, 2) + "\n");

  if (fail) {
    console.error("capture finished with QA assertion failures");
    process.exit(2);
  }
  console.log("capture ok");
} finally {
  await browser.close();
  server.close();
}