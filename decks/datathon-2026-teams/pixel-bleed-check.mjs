#!/usr/bin/env node
/** Fail build if navy/photo slide PNGs show white at x=2 (1280 export). */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { spawnSync } from "child_process";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SAMPLE_Y = [100, 360, 620];
const SAMPLE_X = 2;
const WHITE_FLOOR = 240;

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

function printTable(report) {
  console.log("\n--- pixel bleed check (x=2) ---");
  console.log("slide\tlang\ty=100\t\t y=360\t\t y=620\t\tpass");
  for (const row of report.rows) {
    const fmt = (key) => {
      const s = row[key];
      const rgb = `(${s.r},${s.g},${s.b})`;
      return `${rgb}`.padEnd(14) + (s.pass ? "ok" : "FAIL");
    };
    console.log(
      `${row.slide}\t${row.lang}\t${fmt("y100")}\t${fmt("y360")}\t${fmt("y620")}\t${row.pass ? "PASS" : "FAIL"}`
    );
  }
  console.log(report.pass ? "\nPixel bleed check: PASS" : "\nPixel bleed check: FAIL");
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === path.resolve(fileURLToPath(import.meta.url));
if (isMain) {
  const artDir = process.env.BLEED_ART_DIR || "/opt/cursor/artifacts";
  const distHtml = path.join(__dirname, "dist", "index.html");
  const report = runPixelBleedCheck({
    artDir,
    distHtml,
    outPath: path.join(artDir, "datathon-2026-teams-pixel-bleed-report.json"),
  });
  printTable(report);
  if (!report.pass) process.exit(1);
}