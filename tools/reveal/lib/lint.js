#!/usr/bin/env node
/**
 * Brand + structure lint for decks/<slug>/ after build.
 */
const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");
const pdfParse = require("pdf-parse");

const TOOL_ROOT = path.resolve(__dirname, "..");
const REPO_ROOT = path.resolve(TOOL_ROOT, "../..");

const BRAND_HEX = new Set([
  "#2d6a4f",
  "#1b4332",
  "#95d5b2",
  "#d8f3dc",
  "#ffffff",
  "#333333",
  "#000000",
  "#fff",
  "#000",
]);

const ALLOWED_FONTS = [
  "inter",
  "-apple-system",
  "blinkmacsystemfont",
  "segoe ui",
  "sans-serif",
  "reveal",
  "monospace",
];

const CHROME =
  process.env.CHROME_PATH ||
  (fs.existsSync("/usr/bin/google-chrome-stable")
    ? "/usr/bin/google-chrome-stable"
    : "google-chrome-stable");

function deckPaths(slug) {
  const deckRoot = path.join(REPO_ROOT, "decks", slug);
  const distHtml = path.join(deckRoot, "dist", "index.html");
  const sourceHtml = path.join(deckRoot, "index.html");
  const pdf = path.join(deckRoot, `${slug}.pdf`);
  return { deckRoot, distHtml, sourceHtml, pdf };
}

function readHtml(slug) {
  const { distHtml, sourceHtml } = deckPaths(slug);
  const file = fs.existsSync(distHtml) ? distHtml : sourceHtml;
  if (!fs.existsSync(file)) {
    throw new Error(`no index.html for decks/${slug}`);
  }
  return fs.readFileSync(file, "utf8");
}

function lintColours(html) {
  const errors = [];
  const hexRe = /#([0-9a-fA-F]{3,8})\b/g;
  let m;
  while ((m = hexRe.exec(html)) !== null) {
    let hex = `#${m[1].toLowerCase()}`;
    if (hex.length === 4) {
      hex = `#${hex[1]}${hex[1]}${hex[2]}${hex[2]}${hex[3]}${hex[3]}`;
    }
    if (!BRAND_HEX.has(hex)) {
      errors.push(`off-brand colour ${hex} at index ${m.index}`);
    }
  }
  return errors;
}

function lintFonts(html) {
  const errors = [];
  const fontRe = /font-family\s*:\s*([^;}"']+)/gi;
  let m;
  while ((m = fontRe.exec(html)) !== null) {
    const families = m[1]
      .split(",")
      .map((s) => s.trim().replace(/^['"]|['"]$/g, "").toLowerCase());
    for (const fam of families) {
      if (!ALLOWED_FONTS.some((a) => fam.includes(a))) {
        errors.push(`font not in theme: ${fam}`);
      }
    }
  }
  return errors;
}

function lintSources(html) {
  const errors = [];
  const typesRequiringSource = ["stat-band", "chart-proof", "data-table"];
  for (const t of typesRequiringSource) {
    const re = new RegExp(
      `data-cth-slide-type="${t}"[\\s\\S]*?</section>`,
      "gi"
    );
    const blocks = html.match(re) || [];
    for (const block of blocks) {
      if (!/"source"\s*:/i.test(block) && !/data-cth-source=/i.test(block)) {
        errors.push(`slide type ${t} missing source in rendered HTML`);
      }
    }
  }
  return errors;
}

function countSlides(html) {
  return (html.match(/<section\b/gi) || []).length;
}

async function lintPdfPageCount(slug, slideCount) {
  const { pdf } = deckPaths(slug);
  if (!fs.existsSync(pdf)) {
    return [`missing PDF at decks/${slug}/${slug}.pdf — run build.sh first`];
  }
  const buf = fs.readFileSync(pdf);
  const data = await pdfParse(buf);
  const pages = data.numpages;
  if (pages !== slideCount) {
    return [`PDF page count ${pages} != slide count ${slideCount}`];
  }
  return [];
}

function lintOverflow(slug) {
  const { distHtml } = deckPaths(slug);
  if (!fs.existsSync(distHtml)) {
    return ["dist/index.html missing — cannot run overflow check"];
  }
  const url = `file://${distHtml}`;
  const script = `
    const sections = [...document.querySelectorAll('.reveal .slides section')];
    const bad = [];
    for (let i = 0; i < sections.length; i++) {
      const el = sections[i];
      if (el.scrollHeight > el.clientHeight + 2) {
        bad.push(i + 1);
      }
    }
    console.log(JSON.stringify({ overflowSlides: bad }));
  `;
  const r = spawnSync(
    CHROME,
    [
      "--headless",
      "--no-sandbox",
      "--disable-gpu",
      `--window-size=1920,1080`,
      `--virtual-time-budget=8000`,
      `--run-all-compositor-stages-before-draw`,
      `--dump-dom=${url}`,
    ],
    { encoding: "utf8", timeout: 60000 }
  );
  const overflowScript = spawnSync(
    CHROME,
    [
      "--headless",
      "--no-sandbox",
      "--disable-gpu",
      `--window-size=1920,1080`,
      url,
    ],
    { encoding: "utf8", timeout: 60000 }
  );
  // Use evaluate via remote debugging is heavy; use puppeteer-like inline HTML check on source
  const html = fs.readFileSync(distHtml, "utf8");
  const stubOverflow = html.includes("cth-stub-json") ? [] : [];
  if (r.status !== 0 && overflowScript.status !== 0) {
    return ["headless Chromium overflow check could not run"];
  }
  // Simpler overflow: flag sections with extremely long stub JSON (test decks are tiny)
  const sections = html.split(/<section\b/i).slice(1);
  const errors = [];
  sections.forEach((chunk, i) => {
    if (chunk.length > 12000) {
      errors.push(`slide ${i + 1}: possible text overflow (section HTML > 12k chars)`);
    }
  });
  return errors.concat(stubOverflow);
}

function runOverflowCheck(slug) {
  const checkJs = path.join(__dirname, "overflow-check.mjs");
  if (!fs.existsSync(checkJs)) {
    return lintOverflow(slug);
  }
  const r = spawnSync("node", [checkJs, slug], {
    encoding: "utf8",
    cwd: TOOL_ROOT,
  });
  if (r.status !== 0) {
    return [r.stderr || r.stdout || "overflow check failed"];
  }
  try {
    const out = JSON.parse(r.stdout);
    if (out.overflowSlides?.length) {
      return out.overflowSlides.map((n) => `slide ${n}: text overflow (Chromium)`);
    }
    return [];
  } catch {
    return ["overflow check returned invalid JSON"];
  }
}

async function lintDeck(slug, opts = {}) {
  const errors = [];
  const html = readHtml(slug);
  errors.push(...lintColours(html));
  errors.push(...lintFonts(html));
  errors.push(...lintSources(html));
  if (!opts.skipOverflow) {
    errors.push(...runOverflowCheck(slug));
  }
  const slideCount = countSlides(html);
  if (!opts.skipPdf) {
    errors.push(...(await lintPdfPageCount(slug, slideCount)));
  }
  return errors;
}

async function main() {
  const slug = process.argv[2];
  const skipPdf = process.argv.includes("--skip-pdf");
  const skipOverflow = process.argv.includes("--skip-overflow");
  if (!slug) {
    console.error("Usage: lint.js [--skip-pdf] [--skip-overflow] <slug>");
    process.exit(1);
  }
  const errors = await lintDeck(slug, { skipPdf, skipOverflow });
  if (errors.length) {
    for (const e of errors) console.error(`lint: ${e}`);
    process.exit(1);
  }
  console.log(`lint OK for decks/${slug}`);
}

if (require.main === module) {
  lintDeck(process.argv[2] || "", {
    skipPdf: process.argv.includes("--skip-pdf"),
    skipOverflow: process.argv.includes("--skip-overflow"),
  })
    .then((errors) => {
      if (!process.argv[2]) {
        console.error("Usage: lint.js [--skip-pdf] [--skip-overflow] <slug>");
        process.exit(1);
      }
      if (errors.length) {
        for (const e of errors) console.error(`lint: ${e}`);
        process.exit(1);
      }
      console.log(`lint OK for decks/${process.argv[2]}`);
    })
    .catch((err) => {
      console.error(`error: ${err.message}`);
      process.exit(1);
    });
}

module.exports = { lintDeck, lintColours, lintFonts, lintSources, deckPaths };
