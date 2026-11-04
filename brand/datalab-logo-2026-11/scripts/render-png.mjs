#!/usr/bin/env node
/**
 * Render logo and social PNGs from SVG via @resvg/resvg-js.
 * Logo dark variants: remap fills for dark backgrounds.
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { Resvg } from '@resvg/resvg-js';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');

function toDark(svg) {
  return svg
    .replace(/#0C498A/gi, '#B2EEFA')
    .replace(/#669348/gi, '#9DC384')
    .replace(/opacity="0\.35"/g, 'opacity="0.55"');
}

function renderSvg(svgString, outPath, width) {
  const resvg = new Resvg(svgString, {
    fitTo: width ? { mode: 'width', value: width } : undefined,
    font: {
      loadSystemFonts: true,
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
