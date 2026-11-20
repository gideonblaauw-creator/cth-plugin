#!/usr/bin/env node
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { createRequire } from "module";
import { execSync } from "child_process";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DECK_ROOT = path.resolve(__dirname, "..");
const REVIEW = path.join(DECK_ROOT, "review");
const DIST_HTML = path.join(DECK_ROOT, "dist", "index.html");
const FODESEP_HTML = process.env.FODESEP_HTML || "";
const SLIDES = 11;

const require = createRequire(
  path.resolve(DECK_ROOT, "../../tools/reveal/package.json")
);
const puppeteer = require("puppeteer-core");

if (!fs.existsSync(DIST_HTML)) {
  console.error("error: run tools/reveal/build.sh observatorio-tierra-dataton first");
  process.exit(1);
}

const executablePath = process.env.CHROME_PATH || "/usr/bin/google-chrome-stable";

async function captureDeck(page, htmlPath, outPrefix, count) {
  await page.goto(`file://${htmlPath}`, { waitUntil: "networkidle0", timeout: 120000 });
  await page.waitForFunction(
    () => typeof Reveal !== "undefined" && Reveal.getTotalSlides() >= 1
  );
  const files = [];
  for (let i = 0; i < count; i++) {
    await page.evaluate((idx) => {
      Reveal.slide(idx);
      document.querySelectorAll(".fragment").forEach((f) => f.classList.add("visible"));
    }, i);
    await new Promise((r) => setTimeout(r, 400));
    const out = path.join(REVIEW, `${outPrefix}${String(i + 1).padStart(2, "0")}.png`);
    await page.screenshot({ path: out, type: "png" });
    files.push(out);
  }
  return files;
}

const browser = await puppeteer.launch({
  executablePath,
  headless: true,
  args: ["--no-sandbox", "--disable-gpu"],
});

try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });

  const slideFiles = await captureDeck(page, DIST_HTML, "slide-", SLIDES);

  const hashes = slideFiles.map((f) =>
    execSync(`md5sum "${f}"`, { encoding: "utf8" }).trim().split(/\s+/)[0]
  );
  const unique = new Set(hashes);
  console.log("slide hashes:", hashes.join(" "));
  console.log("unique count:", unique.size);
  if (unique.size !== SLIDES) {
    console.error(`error: expected ${SLIDES} distinct screenshot hashes, got ${unique.size}`);
    process.exit(2);
  }

  const contactPath = path.join(REVIEW, "contact-sheet.png");
  execSync(
    `montage ${slideFiles.map((f) => `"${f}"`).join(" ")} -tile 4x3 -geometry 480x270+4+4 -background white "${contactPath}"`,
    { stdio: "inherit" }
  );

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
      execSync(
        `montage "${eo}" "${ref}" -tile 2x1 -geometry 960x540+8+8 -label "${type}" -background "#f5f5f5" "${cmp}"`,
        { stdio: "inherit" }
      );
    }
  }

  fs.writeFileSync(
    path.join(REVIEW, "hashes.txt"),
    slideFiles.map((f, i) => `${hashes[i]}  ${path.basename(f)}`).join("\n") + "\n"
  );
  console.log("capture ok");
} finally {
  await browser.close();
}