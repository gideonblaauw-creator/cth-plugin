#!/usr/bin/env node
/**
 * Render logo and social PNGs from SVG via @resvg/resvg-js with bundled OFL fonts.
 */
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { Resvg } from '@resvg/resvg-js';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const fontsDir = join(dirname(fileURLToPath(import.meta.url)), 'fonts');

const fontFiles = [
  join(fontsDir, 'TitilliumWeb-Bold.ttf'),
  join(fontsDir, 'OpenSans-Regular.ttf'),
  join(fontsDir, 'OpenSans-SemiBold.ttf'),
];

for (const f of fontFiles) {
  if (!existsSync(f)) {
    console.error(`Missing font: ${f}. Run from repo with scripts/fonts/*.ttf present.`);
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
    fitTo: width ? { mode: 'width', value: width } : undefined,
    font: {
      loadSystemFonts: false,
      fontFiles,
      defaultFontFamily: 'Open Sans',
    },
  });
  const png = resvg.render().asPng();
  writeFileSync(outPath, png);
  return png.length;
}

const logos = ['option-a', 'option-b', 'option-c'];
for (const name of logos) {
  const svgPath = join(root, 'logo', `${name}.svg`);
  const svg = readFileSync(svgPath, 'utf8');
  const lightOut = join(root, 'logo', `${name}-light.png`);
  const darkOut = join(root, 'logo', `${name}-dark.png`);
  const lightBytes = renderSvg(svg, lightOut, 1024);
  const darkBytes = renderSvg(toDark(svg), darkOut, 1024);
  console.log(`${name}: light ${lightBytes} B, dark ${darkBytes} B`);
}

const social = [
  { file: 'post-1080x1080.svg', width: 1080 },
  { file: 'post-1200x627.svg', width: 1200 },
];
for (const { file, width } of social) {
  const svg = readFileSync(join(root, 'social', file), 'utf8');
  const pngName = file.replace('.svg', '.png');
  const bytes = renderSvg(svg, join(root, 'social', pngName), width);
  console.log(`${pngName}: ${bytes} B`);
}
