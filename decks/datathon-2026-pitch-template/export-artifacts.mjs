#!/usr/bin/env node
/** Export 1920×1080 slide PNGs + contact sheet (ES only). */
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
w,h=480,270
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

async function exportSlides(width, height, suffix) {
  const browser = await puppeteer.launch({
    executablePath: chrome,
    headless: true,
    args: ["--no-sandbox", "--disable-gpu"],
  });
  const page = await browser.newPage();
  const url = `file://${distHtml}?export=1`;
  await page.goto(url, { waitUntil: "networkidle0", timeout: 120000 });
  await page.evaluate(() => document.documentElement.classList.add("export"));
  const count = await page.evaluate(
    () => document.querySelectorAll(".reveal .slides section[data-cth-type]").length
  );
  const slidePngs = [];
  await page.setViewport({ width, height, deviceScaleFactor: 1 });
  for (let i = 0; i < count; i++) {
    await page.evaluate((n) => window.Reveal.slide(n), i);
    await new Promise((r) => setTimeout(r, 400));
    const name = `slide-${String(i + 1).padStart(2, "0")}-${width}x${height}.png`;
    const local = path.join(outDir, name);
    await page.screenshot({ path: local, type: "png" });
    const art = path.join(artDir, name);
    fs.copyFileSync(local, art);
    slidePngs.push(art);
    console.log(name);
  }
  await browser.close();
  return { slidePngs, suffix, count };
}

if (!fs.existsSync(distHtml)) {
  console.error("missing dist/index.html — run build.sh first");
  process.exit(1);
}

const hi = await exportSlides(1920, 1080, "1920");
const lo = await exportSlides(1280, 720, "1280");

const contactName = "datathon-pitch-template-contact-sheet.png";
const contactArt = path.join(artDir, contactName);
contactSheet(hi.slidePngs, contactArt);
fs.copyFileSync(contactArt, path.join(outDir, contactName));

const manifest = {
  slides: hi.count,
  contact: contactArt,
  png1920: hi.slidePngs,
  png1280: lo.slidePngs,
};
const manifestPath = path.join(artDir, "datathon-pitch-template-export-manifest.json");
fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));
fs.writeFileSync(path.join(outDir, "datathon-pitch-template-export-manifest.json"), JSON.stringify(manifest, null, 2));
console.log("contact-sheet:", contactArt);
console.log("manifest:", manifestPath);