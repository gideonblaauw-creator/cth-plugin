#!/usr/bin/env node
/** Render logo SVGs in assets/logos to light/dark PNG (1024px width). */
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { Resvg } from '@resvg/resvg-js';

const bookRoot = join(dirname(fileURLToPath(import.meta.url)), '..');
const logosDir = join(bookRoot, 'assets', 'logos');
const fontsDir = join(bookRoot, 'assets', 'fonts');

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

function toDark(svg) {
  return svg
    .replace(/#0C498A/gi, '%%PRIMARY%%')
    .replace(/#B2EEFA/gi, '#69B5FA')
    .replace(/#669348/gi, '#9DC384')
    .replace(/%%PRIMARY%%/g, '#B2EEFA');
}

function renderSvg(svgString, outPath, width) {
  const resvg = new Resvg(svgString, {
    fitTo: { mode: 'width', value: width },
    font: {
      loadSystemFonts: false,
      fontFiles,
      defaultFontFamily: 'Open Sans',
    },
  });
  writeFileSync(outPath, resvg.render().asPng());
}

const basenames = [
  'datalab-logo',
  'datalab-logo-endorsed',
  'data-flow',
  'data-flow-endorsed',
  'data-set',
  'data-set-endorsed',
  'data-dashboard',
  'data-dashboard-endorsed',
];

for (const name of basenames) {
  const svgPath = join(logosDir, `${name}.svg`);
  if (!existsSync(svgPath)) {
    console.warn(`skip ${name}: no svg`);
    continue;
  }
  const svg = readFileSync(svgPath, 'utf8');
  renderSvg(svg, join(logosDir, `${name}-light.png`), 1024);
  renderSvg(toDark(svg), join(logosDir, `${name}-dark.png`), 1024);
  console.log(`ok ${name}`);
}
