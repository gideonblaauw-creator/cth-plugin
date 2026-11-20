#!/usr/bin/env node
/** Present-mode cover motion QA: animation names, transforms, timed stills, RMS. */
import fs from "fs";
import path from "path";
import http from "http";
import { fileURLToPath } from "url";
import { createRequire } from "module";
import { execSync } from "child_process";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DECK_ROOT = path.resolve(__dirname, "..");
const DIST_DIR = path.join(DECK_ROOT, "dist");
const REVIEW = path.join(DECK_ROOT, "review");
const MOTION = path.join(REVIEW, "motion");
const TIMES_MS = [0, 2500, 5000, 8000];

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

function rmsBetweenPngs(a, b) {
  const py = path.join(__dirname, "png_rms.py");
  return parseFloat(
    execSync(`python3 "${py}" "${a}" "${b}"`, { encoding: "utf8" }).trim()
  );
}

if (!fs.existsSync(path.join(DIST_DIR, "index.html"))) {
  console.error("error: run build.sh first");
  process.exit(1);
}

fs.mkdirSync(MOTION, { recursive: true });

const { server, baseUrl } = await startStaticServer(DIST_DIR);
const browser = await puppeteer.launch({
  executablePath,
  headless: true,
  args: ["--no-sandbox", "--disable-gpu"],
});

let fail = false;

try {
  const page = await browser.newPage();
  await page.emulateMediaFeatures([{ name: "prefers-reduced-motion", value: "no-preference" }]);
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });
  await page.goto(`${baseUrl}index.html`, { waitUntil: "networkidle0", timeout: 120000 });
  await page.waitForFunction(() => typeof Reveal !== "undefined");

  const computed = await page.evaluate(() => {
    const kb = document.querySelector("section.present .fp-kenburns");
    const orb = document.querySelector("section.present .fp-orbit-drift");
    const styleOf = (el) => {
      if (!el) return null;
      const cs = getComputedStyle(el);
      const tr = cs.transform;
      let scale = 1;
      if (tr && tr !== "none") {
        const m = tr.match(/matrix\\(([^)]+)\\)/);
        if (m) {
          const parts = m[1].split(",").map((x) => parseFloat(x.trim()));
          if (parts.length >= 1) scale = parts[0];
        }
      }
      return {
        animationName: cs.animationName,
        animationDuration: cs.animationDuration,
        transform: tr,
        scale,
      };
    };
    return {
      url: location.href,
      reducedMotion: false,
      bodyClass: document.body.className,
      printPdf: document.body.classList.contains("print-pdf"),
      exportClass: document.body.classList.contains("export"),
      kenburns: styleOf(kb),
      orbit: styleOf(orb),
    };
  });

  fs.writeFileSync(
    path.join(MOTION, "present-mode-computed.json"),
    JSON.stringify(computed, null, 2) + "\n"
  );

  if (computed.kenburns?.animationName !== "eo-kenburns") {
    console.error(`error: cover kenburns animation-name ${computed.kenburns?.animationName}`);
    fail = true;
  }
  if (computed.orbit?.animationName !== "eo-orbit-drift") {
    console.error(`error: cover orbit animation-name ${computed.orbit?.animationName}`);
    fail = true;
  }

  const stillPaths = [];
  const transforms = [];
  for (const t of TIMES_MS) {
    if (t > 0) await new Promise((r) => setTimeout(r, t - (TIMES_MS[TIMES_MS.indexOf(t) - 1] ?? 0)));
    const snap = await page.evaluate(() => {
      const kb = document.querySelector("section.present .fp-kenburns");
      const orb = document.querySelector("section.present .fp-orbit-drift");
      const tr = (el) => (el ? getComputedStyle(el).transform : null);
      return { kenburns: tr(kb), orbit: tr(orb) };
    });
    transforms.push({ t, ...snap });
    const out = path.join(MOTION, `cover-t${String(t).padStart(4, "0")}ms.png`);
    await page.screenshot({ path: out, type: "png" });
    stillPaths.push(out);
  }

  const rmsPairs = [];
  for (let i = 1; i < stillPaths.length; i++) {
    const rms = rmsBetweenPngs(stillPaths[0], stillPaths[i]);
    rmsPairs.push({ from: 0, to: TIMES_MS[i], rms });
  }
  const maxRms = Math.max(...rmsPairs.map((p) => p.rms));

  if (maxRms < 1) {
    console.error(`error: cover motion RMS max ${maxRms} < 1`);
    fail = true;
  }

  const summary = {
    timesMs: TIMES_MS,
    transforms,
    rmsFromT0: rmsPairs,
    maxRmsFromT0: maxRms,
    computed,
  };
  fs.writeFileSync(path.join(MOTION, "motion-summary.json"), JSON.stringify(summary, null, 2) + "\n");

  if (fs.existsSync("/usr/bin/montage")) {
    execSync(
      `montage ${stillPaths.map((p) => `"${p}"`).join(" ")} -tile 4x1 -geometry 480x270+4+4 -background white "${path.join(MOTION, "cover-timed-contact.png")}"`,
      { stdio: "inherit" }
    );
  }

  console.log(JSON.stringify(summary, null, 2));
  if (fail) process.exit(2);
  console.log("motion-check ok");
} finally {
  await browser.close();
  server.close();
}