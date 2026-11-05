#!/usr/bin/env node
/**
 * Earth Observatory / Observatorio de la Tierra — logo concept kit (internal review).
 */
import {
  readFileSync,
  writeFileSync,
  mkdirSync,
  existsSync,
  readdirSync,
} from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { Resvg } from '@resvg/resvg-js';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const fontsDir = join(dirname(fileURLToPath(import.meta.url)), 'fonts');
const conceptsDir = join(root, 'concepts');
const previewsDir = join(root, 'previews');

const C = {
  primary: '#2D6A4F',
  dark: '#1B4332',
  accent: '#95D5B2',
  light: '#D8F3DC',
  white: '#FFFFFF',
  text: '#333333',
};

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

const cthLogoB64 = readFileSync(join(root, 'assets', 'cleantechhub.png')).toString(
  'base64',
);

const concepts = [
  {
    id: '01-lente-global',
    nameEs: 'Lente Global',
    nameEn: 'Global Lens',
    rationale:
      'An eye-lens over the globe: collaboration is the lens that brings territories and partners into shared focus.',
    drawMark: (g, mono) => {
      const p = mono ? C.dark : C.primary;
      const a = mono ? C.dark : C.accent;
      return `${g}
  <circle cx="48" cy="48" r="36" fill="none" stroke="${p}" stroke-width="3"/>
  <ellipse cx="48" cy="48" rx="36" ry="14" fill="none" stroke="${a}" stroke-width="2" opacity="${mono ? 1 : 0.85}"/>
  <ellipse cx="48" cy="48" rx="14" ry="36" fill="none" stroke="${a}" stroke-width="2" opacity="${mono ? 1 : 0.85}"/>
  <path d="M 24 48 Q 48 28 72 48 Q 48 68 24 48 Z" fill="${a}" opacity="${mono ? 0.35 : 0.45}"/>
  <circle cx="48" cy="48" r="10" fill="${p}"/>
  <circle cx="45" cy="45" r="3" fill="${mono ? C.white : C.light}"/>`;
    },
  },
  {
    id: '02-grilla-territorio',
    nameEs: 'Grilla Territorio',
    nameEn: 'Terrain Grid',
    rationale:
      'A data grid reads as rising terrain: data is the infrastructure that lifts local decisions.',
    drawMark: (g, mono) => {
      const cells = [
        [0, 2, 1, 2],
        [1, 3, 2, 1],
        [2, 1, 3, 2],
        [1, 2, 2, 3],
      ];
      const base = mono ? C.dark : C.primary;
      const hi = mono ? C.dark : C.accent;
      const mid = mono ? C.dark : C.light;
      let out = g;
      const sz = 18;
      const ox = 12;
      const oy = 12;
      for (let r = 0; r < 4; r++) {
        for (let c = 0; c < 4; c++) {
          const h = cells[r][c];
          const x = ox + c * (sz + 4);
          const y = oy + (3 - r) * (sz + 4) - h * 3;
          const fill = h >= 3 ? base : h === 2 ? hi : mid;
          out += `\n  <rect x="${x}" y="${y}" width="${sz}" height="${sz + h * 3}" rx="3" fill="${fill}"/>`;
        }
      }
      return out;
    },
  },
  {
    id: '03-orbita-datos',
    nameEs: 'Órbita de Datos',
    nameEn: 'Data Orbit',
    rationale:
      'Orbits and nodes around Earth: international cooperation linking startups, data, and territories.',
    drawMark: (g, mono) => {
      const p = mono ? C.dark : C.primary;
      const a = mono ? C.dark : C.accent;
      return `${g}
  <circle cx="48" cy="48" r="14" fill="${p}"/>
  <ellipse cx="48" cy="48" rx="42" ry="18" fill="none" stroke="${a}" stroke-width="2.5" transform="rotate(-25 48 48)"/>
  <ellipse cx="48" cy="48" rx="38" ry="16" fill="none" stroke="${p}" stroke-width="2" transform="rotate(35 48 48)"/>
  <circle cx="86" cy="38" r="5" fill="${a}"/>
  <circle cx="14" cy="58" r="5" fill="${a}"/>
  <circle cx="58" cy="82" r="4" fill="${p}"/>`;
    },
  },
  {
    id: '04-brujula-norte',
    nameEs: 'Brújula Norte',
    nameEn: 'North Compass',
    rationale:
      'A compass rose: knowledge orients decisions across cooperation, startups, and landscapes.',
    drawMark: (g, mono) => {
      const p = mono ? C.dark : C.primary;
      const a = mono ? C.dark : C.accent;
      return `${g}
  <circle cx="48" cy="48" r="38" fill="none" stroke="${p}" stroke-width="2"/>
  <polygon points="48,12 54,42 48,48 42,42" fill="${p}"/>
  <polygon points="48,84 54,54 48,48 42,54" fill="${a}"/>
  <polygon points="12,48 42,42 48,48 42,54" fill="${a}" opacity="0.85"/>
  <polygon points="84,48 54,54 48,48 54,42" fill="${a}" opacity="0.85"/>
  <circle cx="48" cy="48" r="6" fill="${p}"/>`;
    },
  },
  {
    id: '05-mapas-capas',
    nameEs: 'Mapas en Capas',
    nameEn: 'Layered Maps',
    rationale:
      'Stacked map sheets: layered data infrastructure underpinning collaboration and territory.',
    drawMark: (g, mono) => {
      const p = mono ? C.dark : C.primary;
      const a = mono ? C.dark : C.accent;
      const l = mono ? C.dark : C.light;
      return `${g}
  <path d="M 18 70 L 18 30 L 58 22 L 58 62 Z" fill="${l}" stroke="${p}" stroke-width="2"/>
  <path d="M 28 76 L 28 36 L 68 28 L 68 68 Z" fill="${a}" stroke="${p}" stroke-width="2" opacity="0.9"/>
  <path d="M 38 82 L 38 42 L 78 34 L 78 74 Z" fill="${p}" stroke="${p}" stroke-width="2"/>
  <path d="M 44 50 L 52 46 L 60 54 L 48 58 Z" fill="${mono ? C.white : C.light}"/>`;
    },
  },
];

function styles(mono) {
  const title = mono ? C.dark : C.dark;
  const sub = mono ? C.dark : C.primary;
  return `
    .title { font-family: 'Titillium Web', sans-serif; font-weight: 700; fill: ${title}; }
    .subtitle { font-family: 'Open Sans', sans-serif; font-weight: 600; fill: ${sub}; }
    .caption { font-family: 'Open Sans', sans-serif; font-weight: 400; fill: ${mono ? C.dark : C.text}; }
    .muted { font-family: 'Open Sans', sans-serif; font-weight: 400; fill: ${mono ? C.dark : C.primary}; }
    .partner { font-family: 'Open Sans', sans-serif; font-weight: 600; fill: ${mono ? C.dark : C.text}; }
  `;
}

function wrapSvg(w, h, body, aria) {
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" role="img" aria-label="${aria}">
  <defs><style>${body.includes('<style>') ? '' : ''}</style></defs>
  ${body}
</svg>`;
}

function markGroup(concept, mono, scale = 1, tx = 0, ty = 0) {
  const g = `<g transform="translate(${tx},${ty}) scale(${scale})">`;
  return concept.drawMark(g, mono) + '\n</g>';
}

function squareLockup(concept, mono) {
  const w = 480;
  const h = 480;
  const body = `<defs><style>${styles(mono)}</style></defs>
  ${markGroup(concept, mono, 1.35, 48, 40)}
  <text class="title" font-size="28" x="240" y="300" text-anchor="middle">Observatorio de la Tierra</text>
  <text class="subtitle" font-size="20" x="240" y="332" text-anchor="middle">Earth Observatory</text>`;
  return wrapSvg(w, h, body, `${concept.nameEn} square lockup`);
}

function horizontalLockup(concept, mono) {
  const w = 720;
  const h = 200;
  const body = `<defs><style>${styles(mono)}</style></defs>
  ${markGroup(concept, mono, 0.95, 8, 28)}
  <text class="title" font-size="32" x="200" y="88">Observatorio de la Tierra</text>
  <text class="subtitle" font-size="22" x="200" y="122">Earth Observatory</text>
  <text class="caption" font-size="14" x="200" y="158">CleantechHUB × Universidad Externado</text>`;
  return wrapSvg(w, h, body, `${concept.nameEn} horizontal lockup`);
}

function endorsedLockup(concept, mono) {
  const w = 720;
  const h = 240;
  const body = `<defs><style>${styles(mono)}</style></defs>
  ${markGroup(concept, mono, 0.85, 8, 20)}
  <text class="title" font-size="30" x="188" y="78">Observatorio de la Tierra</text>
  <text class="subtitle" font-size="20" x="188" y="108">Earth Observatory</text>
  <text class="muted" font-size="13" x="188" y="138">powered by CleantechHUB</text>
  <image xlink:href="data:image/png;base64,${cthLogoB64}" x="188" y="148" width="200" height="52" preserveAspectRatio="xMinYMid meet"/>`;
  return wrapSvg(w, h, body, `${concept.nameEn} endorsed lockup`);
}

function cobrandLockup(concept, mono) {
  const w = 720;
  const h = 260;
  const body = `<defs><style>${styles(mono)}</style></defs>
  ${markGroup(concept, mono, 0.85, 8, 24)}
  <text class="title" font-size="28" x="188" y="72">Observatorio de la Tierra</text>
  <text class="subtitle" font-size="19" x="188" y="102">Earth Observatory</text>
  <rect x="188" y="118" width="220" height="36" rx="4" fill="${mono ? 'none' : C.light}" stroke="${C.primary}" stroke-width="1.5" stroke-dasharray="4 3"/>
  <text class="partner" font-size="14" x="298" y="142" text-anchor="middle">Universidad Externado</text>
  <text class="caption" font-size="12" x="188" y="178">CleantechHUB × Universidad Externado</text>
  <text class="muted" font-size="12" x="188" y="200">powered by CleantechHUB</text>
  <image xlink:href="data:image/png;base64,${cthLogoB64}" x="188" y="208" width="180" height="46" preserveAspectRatio="xMinYMid meet"/>`;
  return wrapSvg(w, h, body, `${concept.nameEn} co-brand lockup`);
}

function monoLockup(concept) {
  return horizontalLockup(concept, true);
}

const variants = [
  ['lockup-square', squareLockup],
  ['lockup-horizontal', horizontalLockup],
  ['lockup-endorsed', endorsedLockup],
  ['lockup-cobrand', cobrandLockup],
  ['lockup-mono', monoLockup],
];

function renderSvg(svgString, outPath, width, bg) {
  let svg = svgString;
  if (bg) {
    const m = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/);
    const w = m ? m[1] : '720';
    const h = m ? m[2] : '200';
    svg = svg.replace(
      /<svg([^>]*)>/,
      `<svg$1><rect width="${w}" height="${h}" fill="${bg}"/>`,
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
  const png = resvg.render().asPng();
  writeFileSync(outPath, png);
  return png.length;
}

mkdirSync(conceptsDir, { recursive: true });
mkdirSync(previewsDir, { recursive: true });

const manifest = [];

for (const concept of concepts) {
  const dir = join(conceptsDir, concept.id);
  mkdirSync(dir, { recursive: true });
  writeFileSync(
    join(dir, 'RATIONALE.md'),
    `# ${concept.nameEs} / ${concept.nameEn}\n\n${concept.rationale}\n`,
  );

  for (const [slug, builder] of variants) {
    const mono = slug === 'lockup-mono';
    const svg = builder(concept, mono);
    const svgPath = join(dir, `${slug}.svg`);
    writeFileSync(svgPath, svg);
    manifest.push(`${concept.id}/${slug}.svg`);

    const base = join(dir, slug);
    const tOut = `${base}-transparent.png`;
    const wOut = `${base}-white.png`;
    const w = slug === 'lockup-square' ? 960 : 1440;
    renderSvg(svg, tOut, w, null);
    renderSvg(svg, wOut, w, C.white);
    manifest.push(`${concept.id}/${slug}-transparent.png`);
    manifest.push(`${concept.id}/${slug}-white.png`);
  }
}

// Contact sheet
const thumbW = 340;
const cols = 2;
const pad = 24;
const labelH = 36;
let rowHeights = [];
const items = [];
for (const concept of concepts) {
  const slug = 'lockup-horizontal';
  const svg = readFileSync(join(conceptsDir, concept.id, `${slug}.svg`), 'utf8');
  items.push({ concept, svg, slug });
}

const rows = Math.ceil(items.length / cols);
const sheetW = cols * thumbW + (cols + 1) * pad;
const sheetH =
  rows * (120 + labelH + pad) + pad + 80;

let sheetBody = `<defs><style>${styles(false)}</style></defs>
  <rect width="${sheetW}" height="${sheetH}" fill="${C.white}"/>
  <text class="title" font-size="26" x="${pad}" y="44">Observatorio de la Tierra — Earth Observatory</text>
  <text class="caption" font-size="14" x="${pad}" y="68">Concept contact sheet · INTERNAL REVIEW · CleantechHUB × Universidad Externado</text>`;

items.forEach((item, i) => {
  const col = i % cols;
  const row = Math.floor(i / cols);
  const x = pad + col * (thumbW + pad);
  const y = 88 + row * (120 + labelH + pad);
  const tmpPng = join(previewsDir, `_tmp-${item.concept.id}.png`);
  renderSvg(item.svg, tmpPng, thumbW, C.light);
  const b64 = readFileSync(tmpPng).toString('base64');
  sheetBody += `
  <image xlink:href="data:image/png;base64,${b64}" x="${x}" y="${y}" width="${thumbW}" height="120"/>
  <text class="subtitle" font-size="13" x="${x}" y="${y + 120 + 22}">${item.concept.id} · ${item.concept.nameEs}</text>`;
});

const sheetSvg = wrapSvg(sheetW, sheetH, sheetBody, 'Earth Observatory concept contact sheet');
const sheetSvgPath = join(root, 'contact-sheet.svg');
writeFileSync(sheetSvgPath, sheetSvg);
const contactPath = join(root, 'contact-sheet.png');
renderSvg(sheetSvg, contactPath, sheetW, null);
manifest.push('contact-sheet.svg', 'contact-sheet.png');

writeFileSync(join(root, 'MANIFEST.json'), JSON.stringify(manifest, null, 2));
console.log(`Generated ${manifest.length} deliverable paths`);
console.log(`Contact sheet: ${contactPath}`);
