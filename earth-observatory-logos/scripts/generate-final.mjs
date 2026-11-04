#!/usr/bin/env node
/**
 * Final lockups — Órbita de Datos / Data Orbit (concept 03 only).
 */
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { Resvg } from '@resvg/resvg-js';

const kitRoot = join(dirname(fileURLToPath(import.meta.url)), '..');
const finalRoot = join(kitRoot, 'final');
const fontsDir = join(dirname(fileURLToPath(import.meta.url)), 'fonts');

const PALETTES = {
  green: {
    primary: '#2D6A4F',
    dark: '#1B4332',
    accent: '#95D5B2',
    light: '#D8F3DC',
    mono: '#1B4332',
  },
  blue: {
    primary: '#0C498A',
    dark: '#0C498A',
    accent: '#69B5FA',
    light: '#B2EEFA',
    mono: '#0C498A',
  },
};

const C_COMMON = { white: '#FFFFFF', text: '#333333' };

const fontFiles = [
  join(fontsDir, 'TitilliumWeb-Bold.ttf'),
  join(fontsDir, 'OpenSans-Regular.ttf'),
  join(fontsDir, 'OpenSans-SemiBold.ttf'),
];

for (const f of fontFiles) {
  if (!existsSync(f)) {
    console.error(`Missing font: ${f}`);
    process.exit(1);
  }
}

const cthLogoB64 = readFileSync(
  join(kitRoot, 'assets', 'cleantechhub.png'),
).toString('base64');

/** Mark lives in 96×96 user units; orbits extend to ~94. */
const MARK_UNITS = 96;
/** Scale up from concept draft (0.95) to ~two-line cap height (~32 + 6 + 22 px). */
const MARK_SCALE = 1.05;

function drawOrbitMark(g, palette, mono) {
  const p = mono ? palette.mono : palette.primary;
  const a = mono ? palette.mono : palette.accent;
  return `${g}
  <circle cx="48" cy="48" r="14" fill="${p}"/>
  <ellipse cx="48" cy="48" rx="42" ry="18" fill="none" stroke="${a}" stroke-width="2.5" transform="rotate(-25 48 48)"/>
  <ellipse cx="48" cy="48" rx="38" ry="16" fill="none" stroke="${p}" stroke-width="2" transform="rotate(35 48 48)"/>
  <circle cx="86" cy="38" r="5" fill="${a}"/>
  <circle cx="14" cy="58" r="5" fill="${a}"/>
  <circle cx="58" cy="82" r="4" fill="${p}"/>`;
}

function markAt(tx, ty, palette, mono, scale = MARK_SCALE) {
  const g = `<g transform="translate(${tx},${ty}) scale(${scale})">`;
  return drawOrbitMark(g, palette, mono) + '\n</g>';
}

function styles(palette, mono) {
  const title = mono ? palette.mono : palette.dark;
  const sub = mono ? palette.mono : palette.primary;
  return `
    .title { font-family: 'Titillium Web', sans-serif; font-weight: 700; fill: ${title}; }
    .pendiente { font-family: 'Open Sans', sans-serif; font-weight: 600; fill: ${mono ? palette.mono : C_COMMON.text}; }
    .pendiente-tag { font-family: 'Open Sans', sans-serif; font-weight: 400; font-size: 10px; fill: ${mono ? palette.mono : palette.primary}; }
  `;
}

function wrapSvg(w, h, body, aria) {
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" role="img" aria-label="${aria}">
  ${body}
</svg>`;
}

function titleText(locale) {
  return locale === 'es' ? 'Observatorio de la Tierra' : 'Earth Observatory';
}

function externadoBlock(x, y, w, palette, mono) {
  const stroke = mono ? palette.mono : palette.primary;
  const fill = mono ? 'none' : palette.light;
  return `
  <rect x="${x}" y="${y}" width="${w}" height="40" rx="4" fill="${fill}" stroke="${stroke}" stroke-width="1.5" stroke-dasharray="5 4"/>
  <text class="pendiente-tag" x="${x + 8}" y="${y + 14}">PENDIENTE logo</text>
  <text class="pendiente" font-size="14" x="${x + 8}" y="${y + 32}">Universidad Externado</text>`;
}

function cthLogoBlock(x, y) {
  return `<image xlink:href="data:image/png;base64,${cthLogoB64}" x="${x}" y="${y}" width="220" height="56" preserveAspectRatio="xMinYMid meet"/>`;
}

function squareLockup(locale, palette, mono) {
  const w = 480;
  const h = 480;
  const title = titleText(locale);
  const markSize = MARK_SCALE * MARK_UNITS;
  const markX = (w - markSize) / 2 - 40;
  const markY = 72;
  const body = `<defs><style>${styles(palette, mono)}</style></defs>
  ${markAt(markX, markY, palette, mono)}
  <text class="title" font-size="32" x="${w / 2}" y="320" text-anchor="middle">${title}</text>`;
  return wrapSvg(w, h, body, `${title} square`);
}

function horizontalLockup(locale, palette, mono) {
  const w = 720;
  const h = 200;
  const title = titleText(locale);
  const markH = MARK_SCALE * MARK_UNITS;
  const markY = (h - markH) / 2;
  const textX = 120;
  const titleSize = 32;
  const body = `<defs><style>${styles(palette, mono)}</style></defs>
  ${markAt(8, markY, palette, mono)}
  <text class="title" font-size="${titleSize}" x="${textX}" y="${h / 2 - 6}">${title}</text>`;
  return wrapSvg(w, h, body, `${title} horizontal`);
}

function cobrandLockup(locale, palette, mono) {
  const w = 720;
  const h = 280;
  const title = titleText(locale);
  const markH = MARK_SCALE * MARK_UNITS;
  const markY = 24;
  const textX = 120;
  const body = `<defs><style>${styles(palette, mono)}</style></defs>
  ${markAt(8, markY, palette, mono)}
  <text class="title" font-size="30" x="${textX}" y="72">${title}</text>
  ${externadoBlock(textX, 88, 280, palette, mono)}
  ${cthLogoBlock(textX, 140)}`;
  return wrapSvg(w, h, body, `${title} co-brand`);
}

function monoLockup(locale, palette) {
  return horizontalLockup(locale, palette, true);
}

const variants = [
  ['lockup-square', squareLockup],
  ['lockup-horizontal', horizontalLockup],
  ['lockup-cobrand', cobrandLockup],
  ['lockup-mono', (loc, pal) => monoLockup(loc, pal)],
];

function renderSvg(svgString, outPath, width, bg) {
  let svg = svgString;
  if (bg) {
    const m = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/);
    const vw = m ? m[1] : '720';
    const vh = m ? m[2] : '200';
    svg = svg.replace(
      /<svg([^>]*)>/,
      `<svg$1><rect width="${vw}" height="${vh}" fill="${bg}"/>`,
    );
  }
  const resvg = new Resvg(svg, {
    fitTo: width ? { mode: 'width', value: width } : undefined,
    font: {
      loadSystemFonts: false,
      fontFiles,
      defaultFontFamily: 'Open Sans',
    },
  });
  writeFileSync(outPath, resvg.render().asPng());
}

const locales = ['es', 'en'];
const colors = ['green', 'blue'];
const manifest = [];

mkdirSync(finalRoot, { recursive: true });

for (const locale of locales) {
  for (const color of colors) {
    const dir = join(finalRoot, locale, color);
    mkdirSync(dir, { recursive: true });
    const palette = { ...PALETTES[color], ...C_COMMON };

    for (const [slug, builder] of variants) {
      const mono = slug === 'lockup-mono';
      const svg = builder(locale, palette, mono);
      const svgPath = join(dir, `${slug}.svg`);
      writeFileSync(svgPath, svg);
      manifest.push(`final/${locale}/${color}/${slug}.svg`);

      const base = join(dir, slug);
      const exportW = slug === 'lockup-square' ? 960 : slug === 'lockup-cobrand' ? 1440 : 1440;
      renderSvg(svg, `${base}-transparent.png`, exportW, null);
      renderSvg(svg, `${base}-white.png`, exportW, C_COMMON.white);
      manifest.push(`final/${locale}/${color}/${slug}-transparent.png`);
      manifest.push(`final/${locale}/${color}/${slug}-white.png`);
    }
  }
}

// Preview sheet: ES green cobrand + horizontal, EN green, blue samples
const previewItems = [
  { locale: 'es', color: 'green', slug: 'lockup-cobrand', label: 'ES · green · co-brand' },
  { locale: 'es', color: 'green', slug: 'lockup-horizontal', label: 'ES · green · horizontal' },
  { locale: 'en', color: 'green', slug: 'lockup-horizontal', label: 'EN · green · horizontal' },
  { locale: 'en', color: 'blue', slug: 'lockup-horizontal', label: 'EN · blue · horizontal' },
  { locale: 'es', color: 'blue', slug: 'lockup-cobrand', label: 'ES · blue · co-brand' },
  { locale: 'en', color: 'green', slug: 'lockup-square', label: 'EN · green · square' },
  { locale: 'es', color: 'green', slug: 'lockup-mono', label: 'ES · green · mono' },
  { locale: 'en', color: 'blue', slug: 'lockup-mono', label: 'EN · blue · mono' },
];

const thumbW = 680;
const rowH = 200;
const pad = 20;
const labelH = 28;
const cols = 1;
const sheetW = thumbW + pad * 2;
const sheetH = pad * 2 + previewItems.length * (rowH + labelH + pad) + 50;

let sheet = `<defs><style>${styles(PALETTES.green, false)}</style></defs>
  <rect width="${sheetW}" height="${sheetH}" fill="${C_COMMON.white}"/>
  <text class="title" font-size="22" x="${pad}" y="36">Órbita de Datos — final lockups (concept 03)</text>
  <text class="pendiente" font-size="12" x="${pad}" y="56">INTERNAL REVIEW · Externado first, then CleantechHUB</text>`;

previewItems.forEach((item, i) => {
  const svg = readFileSync(
    join(finalRoot, item.locale, item.color, `${item.slug}.svg`),
    'utf8',
  );
  const tmp = join(finalRoot, `_preview-${i}.png`);
  renderSvg(svg, tmp, thumbW, C_COMMON.white);
  const b64 = readFileSync(tmp).toString('base64');
  const y = 72 + i * (rowH + labelH + pad);
  sheet += `
  <text class="pendiente" font-size="13" x="${pad}" y="${y}">${item.label}</text>
  <image xlink:href="data:image/png;base64,${b64}" x="${pad}" y="${y + 8}" width="${thumbW}" height="${rowH}"/>`;
});

const previewSvg = wrapSvg(sheetW, sheetH, sheet, 'Final lockup preview');
writeFileSync(join(finalRoot, 'preview.svg'), previewSvg);
const previewPath = join(finalRoot, 'preview.png');
renderSvg(previewSvg, previewPath, sheetW, null);
manifest.push('final/preview.svg', 'final/preview.png');

writeFileSync(join(finalRoot, 'MANIFEST.json'), JSON.stringify(manifest, null, 2));
console.log(JSON.stringify({ count: manifest.length, preview: previewPath }, null, 2));
