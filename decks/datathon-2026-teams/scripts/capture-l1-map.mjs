#!/usr/bin/env node
/** L1-only map PNG (19 RMCAB + Mochuelo, no L2/L3/pins/legend). */
import fs from "fs";
import path from "path";
import { fileURLToPath, pathToFileURL } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const deckRoot = path.join(__dirname, "..");
const toolNode = path.resolve(deckRoot, "../../tools/reveal/node_modules");
const puppeteer = (await import(pathToFileURL(path.join(toolNode, "puppeteer-core/lib/esm/puppeteer/puppeteer-core.js")))).default;

const htmlPath = path.join(deckRoot, "assets/cth-living-lab-skeleton-v2.html");
const outPath = path.join(deckRoot, "assets/datalab-living-lab-l1-map-cropped.png");
const chrome = process.env.CHROME_PATH || "/usr/bin/google-chrome-stable";

const browser = await puppeteer.launch({
  executablePath: chrome,
  headless: true,
  args: ["--no-sandbox", "--disable-gpu"],
});
const page = await browser.newPage();
await page.setViewport({ width: 1600, height: 1000, deviceScaleFactor: 2 });
await page.goto(`file://${htmlPath}`, { waitUntil: "networkidle0", timeout: 120000 });
await page.waitForFunction(() => window.CTH && window.CTH.map, { timeout: 60000 });
await page.evaluate(() => {
  const { state, map } = window.CTH;
  state.layers = { L1: true, L2: false, L3: false };
  state.sites.forEach((s) => {
    s.placed = false;
  });
  state.dropMode = null;
  document.body.classList.remove("crosshair");
  document.querySelectorAll(".envleg, .scaleleg, .databand").forEach((el) => {
    el.style.display = "none";
  });
  document.querySelector(".left")?.style.setProperty("display", "none");
  document.querySelector(".right")?.style.setProperty("display", "none");
  document.querySelector("header")?.style.setProperty("display", "none");
  const wrap = document.querySelector(".mapwrap");
  if (wrap) {
    wrap.style.position = "fixed";
    wrap.style.inset = "0";
    wrap.style.width = "1600px";
    wrap.style.height = "1000px";
  }
  const mapEl = document.getElementById("map");
  if (mapEl) {
    mapEl.style.width = "1600px";
    mapEl.style.height = "1000px";
  }
  map.invalidateSize();
  window.__drawMap();
  const bounds = [];
  map.eachLayer((layer) => {
    if (layer.getLatLng) bounds.push(layer.getLatLng());
  });
  if (bounds.length) map.fitBounds(bounds, { padding: [40, 40] });
});
await new Promise((r) => setTimeout(r, 2500));
const mapHandle = await page.$("#map");
if (!mapHandle) throw new Error("#map not found");
await mapHandle.screenshot({ path: outPath, type: "png" });
await browser.close();
const stat = fs.statSync(outPath);
console.log(`Wrote ${outPath} (${stat.size} bytes)`);