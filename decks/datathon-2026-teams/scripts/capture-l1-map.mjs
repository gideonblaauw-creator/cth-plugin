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
await page.setViewport({ width: 1200, height: 720, deviceScaleFactor: 2 });
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
  document.querySelectorAll(".envleg, .scaleleg, .databand, .left, .right, header").forEach((el) => {
    if (el) el.style.display = "none";
  });
  const wrap = document.querySelector(".mapwrap");
  if (wrap) {
    wrap.style.cssText = "position:fixed;inset:0;width:1200px;height:720px;margin:0;padding:0;";
  }
  const mapEl = document.getElementById("map");
  if (mapEl) {
    mapEl.style.width = "1200px";
    mapEl.style.height = "720px";
  }
  document.querySelectorAll(".leaflet-control-container").forEach((el) => {
    el.style.display = "none";
  });
  map.invalidateSize();
  window.__drawMap();
  const latlngs = [];
  map.eachLayer((layer) => {
    if (layer.getLatLng) latlngs.push(layer.getLatLng());
  });
  if (latlngs.length) {
    const bounds = window.L.latLngBounds(latlngs);
    map.fitBounds(bounds, { padding: [16, 16], maxZoom: 13 });
    if (map.getZoom() < 12) map.setZoom(12);
  }
});
await new Promise((r) => setTimeout(r, 3000));
const mapHandle = await page.$("#map");
if (!mapHandle) throw new Error("#map not found");
await mapHandle.screenshot({ path: outPath, type: "png" });
await browser.close();
const stat = fs.statSync(outPath);
console.log(`Wrote ${outPath} (${stat.size} bytes)`);