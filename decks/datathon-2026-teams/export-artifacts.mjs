#!/usr/bin/env node
/** Export 1280px slide PNGs + contact sheet + slide-2 vs FODESEP side-by-side. */
import fs from "fs";
import path from "path";
import { fileURLToPath, pathToFileURL } from "url";
import { spawnSync } from "child_process";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolNode = path.resolve(__dirname, "../../tools/reveal/node_modules");
const puppeteer = (await import(pathToFileURL(path.join(toolNode, "puppeteer-core/lib/esm/puppeteer/puppeteer-core.js")))).default;

const distHtml = path.join(__dirname, "dist", "index.html");
const outDir = path.join(__dirname, "artifacts");
const artDir = "/opt/cursor/artifacts";

fs.mkdirSync(outDir, { recursive: true });
fs.mkdirSync(artDir, { recursive: true });

const chrome = process.env.CHROME_PATH || "/usr/bin/google-chrome-stable";

const browser = await puppeteer.launch({
  executablePath: chrome,
  headless: true,
  args: ["--no-sandbox", "--disable-gpu"],
});

const page = await browser.newPage();
await page.goto(`file://${distHtml}`, { waitUntil: "networkidle0", timeout: 120000 });
const count = await page.evaluate(
  () => document.querySelectorAll(".reveal .slides section[data-cth-type]").length
);

const slidePngs = [];
for (let i = 0; i < count; i++) {
  await page.evaluate((n) => window.Reveal.slide(n), i);
  await new Promise((r) => setTimeout(r, 450));
  const name = `slide-${String(i + 1).padStart(2, "0")}-1280.png`;
  const local = path.join(outDir, name);
  await page.setViewport({ width: 1280, height: 720 });
  await page.screenshot({ path: local, type: "png" });
  const art = path.join(artDir, name);
  fs.copyFileSync(local, art);
  slidePngs.push(art);
  console.log(name);
}

const contactLocal = path.join(outDir, "contact-sheet.png");
const contactArt = path.join(artDir, "datathon-2026-teams-contact-sheet.png");
const montage = spawnSync(
  "montage",
  [...slidePngs, "-tile", "4x", "-geometry", "+8+8", "-background", "white", contactArt],
  { encoding: "utf8" }
);
if (montage.status !== 0) {
  console.error(montage.stderr);
  process.exit(1);
}
fs.copyFileSync(contactArt, contactLocal);

const fodepPage = await browser.newPage();
await fodepPage.setViewport({ width: 1280, height: 720 });
await fodepPage.goto("https://decks.cleantechhub.net/fodesep-partnership/#/2", {
  waitUntil: "networkidle0",
  timeout: 120000,
});
await new Promise((r) => setTimeout(r, 1200));
const fodesepStmt = path.join(artDir, "fodesep-statement-ref.png");
await fodepPage.screenshot({ path: fodesepStmt, type: "png" });

const sidePath = path.join(artDir, "slide-2-vs-fodesep-statement.png");
const sideLocal = path.join(outDir, "slide-2-vs-fodesep-statement.png");
const side = spawnSync(
  "montage",
  [slidePngs[1], fodesepStmt, "-tile", "2x", "-geometry", "+12+12", "-background", "#f0f0f0", sidePath],
  { encoding: "utf8" }
);
if (side.status !== 0) {
  console.error(side.stderr);
  process.exit(1);
}
fs.copyFileSync(sidePath, sideLocal);

await browser.close();
console.log("contact-sheet:", contactArt);
console.log("side-by-side:", sidePath);