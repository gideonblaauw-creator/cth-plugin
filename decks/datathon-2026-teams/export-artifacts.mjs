#!/usr/bin/env node
/** Export 1280px slide PNGs + contact sheets (ES + EN). */
import fs from "fs";
import path from "path";
import { fileURLToPath, pathToFileURL } from "url";
import { spawnSync } from "child_process";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolNode = path.resolve(__dirname, "../../tools/reveal/node_modules");
const puppeteer = (await import(pathToFileURL(path.join(toolNode, "puppeteer-core/lib/esm/puppeteer/puppeteer-core.js")))).default;

const distHtml = path.join(__dirname, "dist", "index.html");
const outDir = path.join(__dirname, "artifacts");
let artDir = "/opt/cursor/artifacts";

fs.mkdirSync(outDir, { recursive: true });
try {
  fs.mkdirSync(artDir, { recursive: true });
  fs.accessSync(artDir, fs.constants.W_OK);
} catch {
  artDir = outDir;
}

const chrome = process.env.CHROME_PATH || "/usr/bin/google-chrome-stable";

function contactSheet(paths, dest) {
  const py = spawnSync(
    "python3",
    [
      "-c",
      `from PIL import Image
import sys
paths=sys.argv[1:-1]
dest=sys.argv[-1]
cols=4
pad=8
w,h=320,180
rows=(len(paths)+cols-1)//cols
W=cols*w+(cols+1)*pad
H=rows*h+(rows+1)*pad
out=Image.new("RGB",(W,H),"white")
for i,p in enumerate(paths):
  im=Image.open(p).resize((w,h))
  c,r=i%cols,i//cols
  out.paste(im,(pad+c*(w+pad),pad+r*(h+pad)))
out.save(dest)`,
      ...paths,
      dest,
    ],
    { encoding: "utf8" }
  );
  if (py.status !== 0) {
    throw new Error(py.stderr || py.stdout || "contact sheet failed");
  }
}

async function exportLang(lang) {
  const browser = await puppeteer.launch({
    executablePath: chrome,
    headless: true,
    args: ["--no-sandbox", "--disable-gpu"],
  });
  const page = await browser.newPage();
  const url = `file://${distHtml}?lang=${lang}`;
  await page.goto(url, { waitUntil: "networkidle0", timeout: 120000 });
  await page.evaluate(() => {
    document.documentElement.classList.add("export");
  });
  await page.evaluate((l) => {
    document.body.setAttribute("data-lang", l);
    document.documentElement.setAttribute("lang", l);
    document.querySelectorAll(".lang-toggle button").forEach((b) => {
      b.setAttribute("aria-pressed", b.getAttribute("data-set-lang") === l ? "true" : "false");
    });
  }, lang);
  const count = await page.evaluate(
    () => document.querySelectorAll(".reveal .slides section[data-cth-type]").length
  );
  const slidePngs = [];
  for (let i = 0; i < count; i++) {
    await page.evaluate((n) => window.Reveal.slide(n), i);
    await new Promise((r) => setTimeout(r, 500));
    const name = `slide-${String(i + 1).padStart(2, "0")}-1280-${lang}.png`;
    const local = path.join(outDir, name);
    await page.setViewport({ width: 1280, height: 720 });
    await page.screenshot({ path: local, type: "png" });
    const art = path.join(artDir, name);
    fs.copyFileSync(local, art);
    slidePngs.push(art);
    console.log(name);
  }
  const contactName = `datathon-2026-teams-contact-sheet-${lang}.png`;
  const contactArt = path.join(artDir, contactName);
  contactSheet(slidePngs, contactArt);
  fs.copyFileSync(contactArt, path.join(outDir, contactName));
  console.log("contact-sheet:", contactArt);
  await browser.close();
  return { slidePngs, contactArt };
}

const es = await exportLang("es");
const en = await exportLang("en");
const manifest = {
  es: { contact: es.contactArt, slides: es.slidePngs },
  en: { contact: en.contactArt, slides: en.slidePngs },
};
const manifestPath = path.join(artDir, "datathon-2026-teams-export-manifest.json");
fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));
console.log("manifest:", manifestPath);

const { runExportSlideChecks } = await import("./pixel-bleed-check.mjs");
const checks = runExportSlideChecks({
  artDir,
  distHtml,
  outDir: artDir,
});
console.log(
  `\nPixel bleed check: ${checks.bleed.pass ? "PASS" : "FAIL"} (${checks.bleed.rows.length} navy/photo samples)`
);
console.log(`Content check: ${checks.content.pass ? "PASS" : "FAIL"} (${checks.content.rows.length} slide/lang samples)`);
if (!checks.pass) {
  for (const row of checks.bleed.rows.filter((r) => !r.pass)) {
    console.error(
      `BLEED FAIL slide ${row.slide} ${row.lang}: y100=(${row.y100.r},${row.y100.g},${row.y100.b}) y360=(${row.y360.r},${row.y360.g},${row.y360.b}) y620=(${row.y620.r},${row.y620.g},${row.y620.b})`
    );
  }
  for (const row of checks.content.rows.filter((r) => !r.pass)) {
    console.error(
      `CONTENT FAIL slide ${row.slide} ${row.lang}: dominantShare=${row.dominantShare.toFixed(4)} unique=${row.uniqueColors}`
    );
  }
  process.exit(1);
}