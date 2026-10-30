import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import path from 'path';
import fs from 'fs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const html = path.join(__dirname, 'index.html');
const outDir = path.join(__dirname, 'screenshots');
fs.mkdirSync(outDir, { recursive: true });

const sections = [
  { id: 'cover', slug: '00-portada' },
  { id: 's1', slug: '01-resumen' },
  { id: 's2', slug: '02-capitulo1' },
  { id: 's3', slug: '03-notas-origen' },
  { id: 's4', slug: '04-proposito' },
  { id: 's5', slug: '05-banda' },
  { id: 's6', slug: '06-mapa-municipios' },
  { id: 's7', slug: '07-tipos' },
  { id: 's8', slug: '08-lentes' },
  { id: 's9', slug: '09-datalab' },
  { id: 's10', slug: '10-papel' },
  { id: 's11', slug: '11-edw' },
  { id: 's12', slug: '12-rein' },
  { id: 's13', slug: '13-ruta' },
  { id: 's14', slug: '14-perfiles' },
  { id: 's15', slug: '15-cierre' },
];

const viewports = [
  { suffix: '', width: 1440, height: 900 },
  { suffix: '-mobile', width: 390, height: 844 },
];

const browser = await chromium.launch();
for (const vp of viewports) {
  const context = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
  const page = await context.newPage();
  await page.goto('file://' + html, { waitUntil: 'networkidle' });
  await page.waitForTimeout(800);

  if (vp.width >= 1000) {
    await page.click('.tab-btn[data-tab="ciudadana"]');
    await page.waitForTimeout(200);
    await page.locator('#level-slider').fill('3');
    await page.locator('#phase-slider').fill('2');
    await page.click('#env-table th.sortable[data-sort="days"]');
    await page.waitForTimeout(300);
  }

  for (const sec of sections) {
    const el = page.locator('#' + sec.id);
    await el.scrollIntoViewIfNeeded();
    await page.waitForTimeout(350);
    const box = await el.boundingBox();
    if (!box || box.height < 40) {
      throw new Error(`Section ${sec.id} appears blank (height ${box?.height})`);
    }
    const file = path.join(outDir, `${sec.slug}${vp.suffix}.png`);
    await el.screenshot({ path: file });
  }
  await context.close();
}
await browser.close();
console.log('OK', sections.length * viewports.length, 'screenshots');
