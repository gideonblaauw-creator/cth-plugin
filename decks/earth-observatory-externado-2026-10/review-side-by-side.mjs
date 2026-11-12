import { chromium } from 'playwright';
import { createServer } from 'http';
import { readFileSync, existsSync } from 'fs';
import { join, extname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = fileURLToPath(new URL('.', import.meta.url));
const CLP_ROOT = process.env.CLP26_ROOT || '/tmp/clp26/site';
const EO_ROOT = __dirname;
const PORT_CLP = 8765;
const PORT_EO = 8766;
const W = 640;
const H = 800;

const MIME = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml'
};

function staticServer(root, port) {
  return new Promise((resolve) => {
    const server = createServer((req, res) => {
      let p = req.url.split('?')[0];
      if (p === '/') p = '/index.html';
      const file = join(root, p);
      if (!existsSync(file)) {
        res.writeHead(404);
        res.end('404');
        return;
      }
      res.writeHead(200, { 'Content-Type': MIME[extname(file)] || 'application/octet-stream' });
      res.end(readFileSync(file));
    });
    server.listen(port, () => resolve(server));
  });
}

async function clipPage(page, url, scrollY) {
  await page.setViewportSize({ width: W, height: H });
  await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(800);
  if (scrollY) await page.evaluate((y) => window.scrollTo(0, y), scrollY);
  await page.waitForTimeout(400);
  return page.screenshot({ type: 'png' });
}

async function stitchHorizontal(leftBuf, rightBuf, outPath) {
  const { PNG } = await import('pngjs');
  const left = PNG.sync.read(leftBuf);
  const right = PNG.sync.read(rightBuf);
  const h = Math.max(left.height, right.height);
  const out = new PNG({ width: left.width + right.width, height: h });
  PNG.bitblt(left, out, 0, 0, left.width, left.height, 0, 0);
  PNG.bitblt(right, out, 0, 0, right.width, right.height, left.width, 0);
  const { writeFileSync } = await import('fs');
  writeFileSync(outPath, PNG.sync.write(out));
}

async function main() {
  const clpSrv = await staticServer(CLP_ROOT, PORT_CLP);
  const eoSrv = await staticServer(EO_ROOT, PORT_EO);
  const browser = await chromium.launch({ args: ['--no-sandbox'] });
  const ctx = await browser.newContext();
  const clp = await ctx.newPage();
  const eo = await ctx.newPage();

  const clpHero = await clipPage(clp, `http://127.0.0.1:${PORT_CLP}/`, 0);
  const eoHero = await clipPage(eo, `http://127.0.0.1:${PORT_EO}/`, 0);
  await stitchHorizontal(clpHero, eoHero, join(EO_ROOT, 'review', 'side-by-side.png'));

  const clpS2 = await clipPage(clp, `http://127.0.0.1:${PORT_CLP}/`, 900);
  const eoS2 = await clipPage(eo, `http://127.0.0.1:${PORT_EO}/`, 900);
  await stitchHorizontal(clpS2, eoS2, join(EO_ROOT, 'review', 'side-by-side-s2.png'));

  await eo.setViewportSize({ width: 1280, height: 800 });
  await eo.goto(`http://127.0.0.1:${PORT_EO}/`, { waitUntil: 'networkidle' });
  await eo.screenshot({ path: join(EO_ROOT, 'review', 'cover-clp-format.png'), fullPage: false });
  await eo.evaluate(() => window.scrollTo(0, 0));

  const sections = [
    ['review/s1-resumen.png', '#s1'],
    ['review/s6-municipios.png', '#s6'],
    ['review/s8-lentes.png', '#s8'],
    ['review/s15-cierre.png', '#s15']
  ];
  for (const [name, hash] of sections) {
    await eo.goto(`http://127.0.0.1:${PORT_EO}/`, { waitUntil: 'networkidle' });
    await eo.locator(hash).scrollIntoViewIfNeeded();
    await eo.waitForTimeout(500);
    await eo.screenshot({ path: join(EO_ROOT, name), fullPage: false });
  }

  await eo.setViewportSize({ width: 1280, height: 900 });
  await eo.goto(`http://127.0.0.1:${PORT_EO}/`, { waitUntil: 'networkidle' });
  await eo.screenshot({ path: join(EO_ROOT, 'review', 'full.png'), fullPage: true });

  await browser.close();
  clpSrv.close();
  eoSrv.close();
  console.log('Wrote review/side-by-side.png and section shots');
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
