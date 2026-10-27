// Render per-slide PNGs (presentation + review), overflow QA, and a high-gloss PDF.
// Usage: NODE_PATH=<dir with playwright-core> node tools/render.js
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright-core');
const ROOT = path.resolve(__dirname, '..');
const OUT = process.env.OUT || path.join(ROOT, 'png');
const PDF = process.env.PDF || path.join(ROOT, 'CEE-CTH-2026-10-14.pdf');
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ executablePath: process.env.CHROME || '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const url = 'file://' + path.join(ROOT, 'index.html');
  const problems = [];
  for (const mode of ['', 'review']) {
    await page.goto(url + '?print' + (mode ? '&' + mode : ''), { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    const n = await page.locator('.deck .slide').count();
    for (let i = 0; i < n; i++) {
      const s = page.locator('.deck .slide').nth(i);
      const f = path.join(OUT, `${String(i + 1).padStart(2, '0')}${mode ? '-review' : ''}.png`);
      await s.screenshot({ path: f });
      if (!mode || mode === 'review') {
        const issues = await s.evaluate((el) => {
          const r = el.getBoundingClientRect(); const out = [];
          const foot = el.querySelector('.footer'); const fr = foot ? foot.getBoundingClientRect() : null;
          el.querySelectorAll('*').forEach((c) => {
            if (c.closest('.footer') || c.tagName === 'STYLE') return;
            const cs = getComputedStyle(c); if (cs.display === 'none' || cs.visibility === 'hidden') return;
            const b = c.getBoundingClientRect(); if (!b.width || !b.height) return;
            if (b.right > r.right + 1 || b.bottom > r.bottom + 1 || b.left < r.left - 1 || b.top < r.top - 1) out.push('outside:' + c.tagName + '.' + c.className + ' ' + (c.textContent||'').trim().slice(0, 40));
            else if (fr && b.bottom > fr.top + 2 && c.children.length === 0 && (c.textContent||'').trim()) out.push('hits-footer:' + c.tagName + '.' + c.className + ' ' + c.textContent.trim().slice(0, 40));
            if (c.scrollHeight > c.clientHeight + 2 && ['hidden','clip'].includes(cs.overflowY) && c.clientHeight > 0 && !c.classList.contains('slide')) out.push('clipped:' + c.tagName + '.' + c.className);
          });
          return out;
        });
        if (issues.length) problems.push(`slide ${i + 1}${mode ? ' (review)' : ''}: ` + issues.slice(0, 8).join(' | '));
      }
    }
    console.log(`${mode || 'presentation'}: ${n} slides`);
  }
  await page.goto(url + '?print', { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.emulateMedia({ media: 'screen' });
  await page.pdf({ path: PDF, width: '1920px', height: '1080px', printBackground: true, margin: { top: '0', right: '0', bottom: '0', left: '0' } });
  console.log('PDF', PDF);
  console.log(problems.length ? 'QA ISSUES:\n' + problems.join('\n') : 'QA: no overflow / footer collisions');
  await browser.close();
})();
