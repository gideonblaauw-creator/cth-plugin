import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import path from 'path';
import fs from 'fs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const baseUrl = process.env.EO_DECK_URL || 'http://127.0.0.1:8765/index.html';
const reviewDir = path.join(__dirname, 'review');
fs.mkdirSync(reviewDir, { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
await page.goto(baseUrl, { waitUntil: 'networkidle' });
await page.waitForTimeout(1200);

await page.screenshot({ path: path.join(reviewDir, 'v7-hero.png'), fullPage: false });

await page.click('.hub-nav button[data-view="actors"]');
await page.waitForTimeout(800);
await page.waitForFunction(() => window.EOHub && document.querySelectorAll('#coMap circle.pin').length > 0);
await page.evaluate(() => window.EOHub.selectStartup('mubon'));
await page.waitForTimeout(400);
await page.locator('#view-actors').screenshot({ path: path.join(reviewDir, 'v7-map.png') });

await page.click('.hub-nav button[data-view="lenses"]');
await page.waitForTimeout(300);
await page.click('#hubLensTabs button[data-lens="ciudadana"]');
await page.waitForTimeout(300);
await page.locator('#view-lenses').screenshot({ path: path.join(reviewDir, 'v7-interactive-lenses.png') });

await page.click('.hub-nav button[data-view="datalab"]');
await page.waitForTimeout(300);
await page.locator('#hubLevelSlider').fill('3');
await page.waitForTimeout(300);
await page.locator('#view-datalab').screenshot({ path: path.join(reviewDir, 'v7-interactive-datalab.png') });

await page.screenshot({ path: path.join(reviewDir, 'v7-full.png'), fullPage: true });

await browser.close();
console.log('v7 review shots OK');
