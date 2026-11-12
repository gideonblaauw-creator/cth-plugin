#!/usr/bin/env node
/**
 * Render deck.yaml -> decks/<slug>/index.html (+ meta), then optional build.
 * Validates against library/schema.json; renders Job A Nunjucks types/*.njk.
 */
const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");
const yaml = require("js-yaml");
const Ajv2020 = require("ajv/dist/2020");
const addFormats = require("ajv-formats");
const nunjucks = require("nunjucks");

const TOOL_ROOT = path.resolve(__dirname, "..");
const REPO_ROOT = path.resolve(TOOL_ROOT, "../..");
const SCHEMA_PATH = path.join(TOOL_ROOT, "library", "schema.json");
const TYPES_DIR = path.join(TOOL_ROOT, "library", "types");

const KNOWN_TYPES = fs
  .readdirSync(TYPES_DIR)
  .filter((f) => f.endsWith(".njk"))
  .map((f) => f.replace(/\.njk$/, ""));

function loadSchema() {
  return JSON.parse(fs.readFileSync(SCHEMA_PATH, "utf8"));
}

function validateOutline(outline) {
  const ajv = new Ajv2020({ allErrors: true, strict: false });
  addFormats(ajv);
  const validate = ajv.compile(loadSchema());
  const ok = validate(outline);
  if (!ok) {
    const msg = (validate.errors || [])
      .map((e) => `${e.instancePath || "/"} ${e.message}`)
      .join("; ");
    throw new Error(`deck.yaml schema validation failed: ${msg}`);
  }
  for (const [i, slide] of outline.slides.entries()) {
    if (!KNOWN_TYPES.includes(slide.type)) {
      throw new Error(
        `slide ${i + 1}: unknown type "${slide.type}" (not in library)`
      );
    }
  }
}

function renderSlide(slide, env) {
  const tplPath = path.join(TYPES_DIR, `${slide.type}.njk`);
  if (!fs.existsSync(tplPath)) {
    throw new Error(`missing template for type "${slide.type}"`);
  }
  return env.renderString(fs.readFileSync(tplPath, "utf8"), slide);
}

function deckHtml(meta, slideSections, lang) {
  const title = meta.title.replace(/</g, "&lt;");
  const sections = slideSections.join("\n      ");
  return `<!DOCTYPE html>
<html lang="${lang}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>${title}</title>
  <meta name="cth-deck-gated" content="true" />
  <link rel="stylesheet" href="reveal.js/dist/reveal.css" />
  <link rel="stylesheet" href="theme/cleantechhub.css" id="theme" />
</head>
<body>
  <div class="reveal">
    <div class="slides">
      ${sections}
    </div>
  </div>
  <script src="reveal.js/dist/reveal.js"></script>
  <script>
    Reveal.initialize({ hash: true, slideNumber: true, width: 1920, height: 1080, margin: 0.04 });
  </script>
</body>
</html>
`;
}

function writeDeck(meta, html, { allowOverwrite }) {
  const slug = meta.slug;
  const deckRoot = path.join(REPO_ROOT, "decks", slug);
  if (fs.existsSync(deckRoot) && !allowOverwrite) {
    throw new Error(
      `decks/${slug}/ already exists — pass --force to overwrite from outline`
    );
  }
  fs.mkdirSync(deckRoot, { recursive: true });
  fs.writeFileSync(path.join(deckRoot, "index.html"), html, "utf8");
  const deckMeta = {
    gated: true,
    language: meta.lang,
    slug: meta.slug,
    title: meta.title,
    client: meta.client,
    date: meta.date,
    toolkit: "tools/reveal",
    source: "deck.yaml",
    publish_note:
      "gated is a label only; real gate is Caddy/oauth2-proxy.",
  };
  fs.writeFileSync(
    path.join(deckRoot, "deck-meta.json"),
    `${JSON.stringify(deckMeta, null, 2)}\n`,
    "utf8"
  );
  const sources = path.join(TOOL_ROOT, "template", "SOURCES.md");
  const readme = path.join(TOOL_ROOT, "template", "README.md");
  if (!fs.existsSync(path.join(deckRoot, "SOURCES.md"))) {
    fs.copyFileSync(sources, path.join(deckRoot, "SOURCES.md"));
  }
  if (!fs.existsSync(path.join(deckRoot, "README.md"))) {
    fs.copyFileSync(readme, path.join(deckRoot, "README.md"));
  }
  return deckRoot;
}

function runBuild(slug) {
  const build = path.join(TOOL_ROOT, "build.sh");
  const r = spawnSync(build, [slug], { stdio: "inherit", cwd: TOOL_ROOT });
  if (r.status !== 0) {
    throw new Error(`build.sh failed for slug "${slug}"`);
  }
}

function parseArgs(argv) {
  const flags = new Set();
  const positional = [];
  for (const a of argv) {
    if (a.startsWith("--")) flags.add(a);
    else positional.push(a);
  }
  return {
    yamlPath: positional[0],
    skipBuild: flags.has("--skip-build"),
    force: flags.has("--force"),
    validateOnly: flags.has("--validate-only"),
  };
}

function main() {
  const { yamlPath, skipBuild, force, validateOnly } = parseArgs(
    process.argv.slice(2)
  );
  if (!yamlPath) {
    console.error(
      "Usage: render-outline.js [--force] [--skip-build] [--validate-only] <deck.yaml>"
    );
    process.exit(1);
  }
  const absYaml = path.resolve(yamlPath);
  const raw = fs.readFileSync(absYaml, "utf8");
  const outline = yaml.load(raw);
  validateOutline(outline);

  if (validateOnly) {
    console.log("deck.yaml OK");
    return;
  }

  const env = nunjucks.configure({ autoescape: true, throwOnUndefined: false });
  const sections = outline.slides.map((s) => renderSlide(s, env));
  const html = deckHtml(outline.meta, sections, outline.meta.lang);
  const deckRoot = writeDeck(outline.meta, html, { allowOverwrite: force });
  console.log(`Wrote ${deckRoot}/index.html (${outline.slides.length} slides)`);

  if (!skipBuild) {
    runBuild(outline.meta.slug);
  }
}

if (require.main === module) {
  try {
    main();
  } catch (err) {
    console.error(`error: ${err.message}`);
    process.exit(1);
  }
}

module.exports = {
  validateOutline,
  renderSlide,
  deckHtml,
  KNOWN_TYPES,
  TOOL_ROOT,
  REPO_ROOT,
};
