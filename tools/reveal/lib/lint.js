#!/usr/bin/env node
/**
 * Brand + structure lint for decks/<slug>/ after build.
 */
const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");
const pdfParse = require("pdf-parse");
const { BRAND_HEX, ALLOWED_FONTS } = require("./brand");

const TOOL_ROOT = path.resolve(__dirname, "..");
const REPO_ROOT = path.resolve(TOOL_ROOT, "../..");

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
  let html = fs.readFileSync(file, "utf8");
  const distDir = path.dirname(file);
  const cssPath = path.join(distDir, "theme", "cleantechhub.css");
  if (fs.existsSync(cssPath)) {
    html += `\n<style>\n${fs.readFileSync(cssPath, "utf8")}\n</style>`;
  }
  return html;
}

function normalizeHex(raw) {
  let hex = raw.toLowerCase();
  if (hex.length === 4) {
    hex = `#${hex[1]}${hex[1]}${hex[2]}${hex[2]}${hex[3]}${hex[3]}`;
  }
  return hex;
}

function collectColourTargets(html) {
  const chunks = [];
  for (const m of html.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/gi)) {
    chunks.push(m[1]);
  }
  for (const m of html.matchAll(/\sstyle\s*=\s*"([^"]*)"/gi)) {
    chunks.push(m[1]);
  }
  for (const m of html.matchAll(/\sstyle\s*=\s*'([^']*)'/gi)) {
    chunks.push(m[1]);
  }
  return chunks.join("\n");
}

function lintColours(html) {
  const errors = [];
  const scoped = collectColourTargets(html);
  const hexRe = /#([0-9a-fA-F]{3,8})\b/g;
  let m;
  while ((m = hexRe.exec(scoped)) !== null) {
    const hex = normalizeHex(`#${m[1]}`);
    if (!BRAND_HEX.has(hex)) {
      errors.push(`off-brand colour ${hex}`);
    }
  }
  return errors;
}

function lintFonts(html) {
  const errors = [];
  const scoped = collectColourTargets(html);
  const fontRe = /font-family\s*:\s*([^;}\n]+)/gi;
  let m;
  while ((m = fontRe.exec(scoped)) !== null) {
    const families = m[1]
      .split(",")
      .map((s) => s.trim().replace(/^['"]|['"]$/g, "").toLowerCase());
    for (const fam of families) {
      if (!fam) continue;
      if (fam.startsWith("var(--")) continue;
      if (!ALLOWED_FONTS.some((a) => fam === a || fam.includes(a))) {
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
      `data-cth-type="${t}"[\\s\\S]*?</section>`,
      "gi"
    );
    const blocks = html.match(re) || [];
    for (const block of blocks) {
      const hasSource =
        /class="cth-source"[^>]*>[^<]+/i.test(block) ||
        /class="cth-stat-tile__source"[^>]*>[^<\s]/i.test(block);
      if (!hasSource) {
        errors.push(`slide type ${t} missing source in rendered HTML`);
      }
    }
  }
  return errors;
}

/** Leaf slides only (Job A marks each with data-cth-type). */
function countSlides(html) {
  return (html.match(/<section[^>]*\sdata-cth-type\s*=/gi) || []).length;
}

function lintRemoteFontUrls(html) {
  const errors = [];
  if (/fonts\.googleapis\.com|fonts\.gstatic\.com/i.test(html)) {
    errors.push("remote Google Fonts URL in deck HTML");
  }
  const scoped = collectColourTargets(html);
  if (/fonts\.googleapis\.com|fonts\.gstatic\.com|@import\s+url\([^)]*fonts/i.test(scoped)) {
    errors.push("remote font URL in deck CSS");
  }
  return errors;
}

function lintPdfEmbeddedOpenSans(slug) {
  const { pdf } = deckPaths(slug);
  if (!fs.existsSync(pdf)) {
    return ["missing PDF for font embedding check"];
  }
  const checker = path.join(__dirname, "pdf-fonts-check.py");
  if (fs.existsSync(checker)) {
    const r = spawnSync("python3", [checker, pdf], { encoding: "utf8" });
    if (r.status === 0) return [];
    if (r.status === 2) {
      return ["pypdf required for PDF font check (pip install pypdf)"];
    }
    return [r.stderr?.trim() || "PDF does not embed Open Sans"];
  }
  return ["pdf-fonts-check.py missing"];
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

function runOverflowCheck(slug) {
  const checkJs = path.join(__dirname, "overflow-check.mjs");
  const r = spawnSync("node", [checkJs, slug], {
    encoding: "utf8",
    cwd: TOOL_ROOT,
  });
  if (r.status !== 0) {
    const msg = (r.stderr || r.stdout || "overflow check failed").trim();
    return [msg || "overflow check failed"];
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
  errors.push(...lintRemoteFontUrls(html));
  errors.push(...lintSources(html));
  if (!opts.skipOverflow) {
    errors.push(...runOverflowCheck(slug));
  }
  const slideCount = countSlides(html);
  if (!opts.skipPdf) {
    errors.push(...(await lintPdfPageCount(slug, slideCount)));
    errors.push(...lintPdfEmbeddedOpenSans(slug));
  }
  return errors;
}

if (require.main === module) {
  const args = process.argv.slice(2);
  const slugArg = args.find((a) => !a.startsWith("--"));
  const skipPdf = args.includes("--skip-pdf");
  const skipOverflow = args.includes("--skip-overflow");
  if (!slugArg) {
    console.error("Usage: lint.js [--skip-pdf] [--skip-overflow] <slug>");
    process.exit(1);
  }
  lintDeck(slugArg, { skipPdf, skipOverflow })
    .then((errors) => {
      if (errors.length) {
        for (const e of errors) console.error(`lint: ${e}`);
        process.exit(1);
      }
      console.log(`lint OK for decks/${slugArg}`);
    })
    .catch((err) => {
      console.error(`error: ${err.message}`);
      process.exit(1);
    });
}

module.exports = {
  lintDeck,
  lintColours,
  lintFonts,
  lintSources,
  countSlides,
  deckPaths,
  collectColourTargets,
  lintRemoteFontUrls,
  lintPdfEmbeddedOpenSans,
};
