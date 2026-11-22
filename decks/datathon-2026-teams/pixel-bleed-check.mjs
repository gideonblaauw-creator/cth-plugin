#!/usr/bin/env node
/** Fail build if navy/photo slide PNGs show white at x=2, or any slide is a flat fill. */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { spawnSync } from "child_process";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SAMPLE_Y = [100, 360, 620];
const SAMPLE_X = 2;
const WHITE_FLOOR = 240;
const FLAT_DOMINANT_SHARE = 0.99;
const CONTENT_STEP = 12;

function slideCount(distHtml) {
  const html = fs.readFileSync(distHtml, "utf8");
  return (html.match(/<section class="fp /g) || []).length;
}

function isNavyOrPhotoSection(html) {
  return /data-background-color="#0C498A"/i.test(html);
}

function loadSlideFlags(distHtml) {
  const html = fs.readFileSync(distHtml, "utf8");
  const parts = html.split('<section class="fp ');
  const flags = [];
  for (let i = 1; i < parts.length; i++) {
    const chunk = '<section class="fp ' + parts[i];
    const end = chunk.indexOf("</section>");
    flags.push(isNavyOrPhotoSection(chunk.slice(0, end > 0 ? end : chunk.length)));
  }
  return flags;
}

function sampleRgb(pngPath, x, y) {
  const py = spawnSync(
    "python3",
    [
      "-c",
      `from PIL import Image; import sys
im=Image.open(sys.argv[1]); r,g,b=im.getpixel((int(sys.argv[2]),int(sys.argv[3])));
print(f"{r},{g},{b}")`,
      pngPath,
      String(x),
      String(y),
    ],
    { encoding: "utf8" }
  );
  if (py.status !== 0) throw new Error(py.stderr || py.stdout || `sample failed: ${pngPath}`);
  const [r, g, b] = py.stdout.trim().split(",").map((n) => parseInt(n, 10));
  return { r, g, b };
}

function isWhite({ r, g, b }) {
  return r >= WHITE_FLOOR && g >= WHITE_FLOOR && b >= WHITE_FLOOR;
}

function contentFlatness(pngPath) {
  const py = spawnSync(
    "python3",
    [
      "-c",
      `from PIL import Image
from collections import Counter
import sys
im=Image.open(sys.argv[1])
w,h=im.size
x0,y0,x1,y1=int(w*0.08),int(h*0.08),int(w*0.94),int(h*0.92)
step=int(sys.argv[2])
c=Counter()
for y in range(y0,y1,step):
  for x in range(x0,x1,step):
    c[im.getpixel((x,y))[:3]]+=1
if not c:
  print("1.0,0")
else:
  dom=max(c.values())/sum(c.values())
  print(f"{dom:.6f},{len(c)}")`,
      pngPath,
      String(CONTENT_STEP),
    ],
    { encoding: "utf8" }
  );
  if (py.status !== 0) throw new Error(py.stderr || py.stdout || `content sample failed: ${pngPath}`);
  const [domStr, uniqStr] = py.stdout.trim().split(",");
  const dominantShare = parseFloat(domStr);
  const uniqueColors = parseInt(uniqStr, 10);
  const pass = dominantShare < FLAT_DOMINANT_SHARE && uniqueColors > 1;
  return { dominantShare, uniqueColors, pass };
}

export function runPixelBleedCheck({ artDir, distHtml, langs = ["es", "en"], outPath }) {
  const navyPhoto = loadSlideFlags(distHtml);
  const rows = [];
  let failed = false;

  for (const lang of langs) {
    for (let i = 0; i < navyPhoto.length; i++) {
      if (!navyPhoto[i]) continue;
      const slide = i + 1;
      const name = `slide-${String(slide).padStart(2, "0")}-1280-${lang}.png`;
      const pngPath = path.join(artDir, name);
      if (!fs.existsSync(pngPath)) {
        throw new Error(`missing PNG for bleed check: ${pngPath}`);
      }
      const samples = {};
      let slideFail = false;
      for (const y of SAMPLE_Y) {
        const rgb = sampleRgb(pngPath, SAMPLE_X, y);
        const pass = !isWhite(rgb);
        if (!pass) slideFail = true;
        samples[`y${y}`] = { ...rgb, pass };
      }
      if (slideFail) failed = true;
      rows.push({ slide, lang, ...samples, pass: !slideFail });
    }
  }

  const report = { sampleX: SAMPLE_X, sampleY: SAMPLE_Y, whiteFloor: WHITE_FLOOR, rows, pass: !failed };
  if (outPath) {
    fs.writeFileSync(outPath, JSON.stringify(report, null, 2));
  }
  return report;
}

export function runSlideContentCheck({ artDir, distHtml, langs = ["es", "en"], outPath }) {
  const count = slideCount(distHtml);
  const rows = [];
  let failed = false;

  for (const lang of langs) {
    for (let slide = 1; slide <= count; slide++) {
      const name = `slide-${String(slide).padStart(2, "0")}-1280-${lang}.png`;
      const pngPath = path.join(artDir, name);
      if (!fs.existsSync(pngPath)) {
        throw new Error(`missing PNG for content check: ${pngPath}`);
      }
      const { dominantShare, uniqueColors, pass } = contentFlatness(pngPath);
      if (!pass) failed = true;
      rows.push({ slide, lang, dominantShare, uniqueColors, pass });
    }
  }

  const report = {
    flatDominantShareMax: FLAT_DOMINANT_SHARE,
    contentStep: CONTENT_STEP,
    rows,
    pass: !failed,
  };
  if (outPath) {
    fs.writeFileSync(outPath, JSON.stringify(report, null, 2));
  }
  return report;
}

export function runExportSlideChecks({ artDir, distHtml, langs = ["es", "en"], outDir }) {
  const bleed = runPixelBleedCheck({
    artDir,
    distHtml,
    langs,
    outPath: outDir ? path.join(outDir, "datathon-2026-teams-pixel-bleed-report.json") : undefined,
  });
  const content = runSlideContentCheck({
    artDir,
    distHtml,
    langs,
    outPath: outDir ? path.join(outDir, "datathon-2026-teams-content-check-report.json") : undefined,
  });
  return { bleed, content, pass: bleed.pass && content.pass };
}

function printTables({ bleed, content }) {
  console.log("\n--- pixel bleed check (x=2) ---");
  console.log("slide\tlang\ty=100\t\t y=360\t\t y=620\t\tpass");
  for (const row of bleed.rows) {
    const fmt = (key) => {
      const s = row[key];
      const rgb = `(${s.r},${s.g},${s.b})`;
      return `${rgb}`.padEnd(14) + (s.pass ? "ok" : "FAIL");
    };
    console.log(
      `${row.slide}\t${row.lang}\t${fmt("y100")}\t${fmt("y360")}\t${fmt("y620")}\t${row.pass ? "PASS" : "FAIL"}`
    );
  }
  console.log(bleed.pass ? "\nPixel bleed check: PASS" : "\nPixel bleed check: FAIL");

  console.log("\n--- slide content check (flat fill) ---");
  console.log("slide\tlang\tdominantShare\tuniqueColors\tpass");
  for (const row of content.rows) {
    console.log(
      `${row.slide}\t${row.lang}\t${row.dominantShare.toFixed(4)}\t\t${row.uniqueColors}\t\t${row.pass ? "PASS" : "FAIL"}`
    );
  }
  console.log(content.pass ? "\nContent check: PASS" : "\nContent check: FAIL");
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === path.resolve(fileURLToPath(import.meta.url));
if (isMain) {
  const artDir = process.env.BLEED_ART_DIR || "/opt/cursor/artifacts";
  const distHtml = path.join(__dirname, "dist", "index.html");
  const checks = runExportSlideChecks({ artDir, distHtml, outDir: artDir });
  printTables(checks);
  if (!checks.pass) process.exit(1);
}