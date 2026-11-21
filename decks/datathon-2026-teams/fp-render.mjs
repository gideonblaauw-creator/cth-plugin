#!/usr/bin/env node
/**
 * Render deck.yaml → index.html using FODESEP fp-* layout (local deck.css).
 * Work stays in decks/datathon-2026-teams/; outline.sh --validate-only checks yaml.
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolNode = path.resolve(__dirname, "../../tools/reveal/node_modules");
const yamlPath = path.join(__dirname, "deck.yaml");

const FOOT =
  '<footer class="fp-foot"><span class="fp-conf">Confidencial — piloto Datatón</span><span>Datalab + Datatón · piloto Air4U · 24 nov 2026</span></footer>';
const FOOT_DARK = FOOT.replace("fp-foot", "fp-foot fp-foot--dark");

function esc(s) {
  return String(s ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function head(title, eyebrow) {
  const ey = eyebrow
    ? `<p class="fp-eyebrow">${esc(eyebrow)}</p>`
    : `<p class="fp-eyebrow">Ejemplo · piloto Air4U</p>`;
  return `<header class="fp-head"><div class="fp-head__text">${ey}<h2 class="fp-title">${esc(title)}</h2></div><img class="fp-head__logo" src="assets/cth-logo.png" alt="CleantechHUB" /></header>`;
}

function notes(slide) {
  return slide.notes
    ? `\n  <aside class="notes">${esc(slide.notes)}</aside>`
    : "";
}

function renderCover(s) {
  const art = s.image
    ? `<img class="fp-cover__art" src="${esc(s.image)}" alt="" />`
    : "";
  return `<section class="fp fp-cover" data-cth-type="cover" data-background-color="#FFFFFF">
  <div class="fp-deco-wrap"><img class="fp-deco fp-cover__blob" src="assets/blob-cyan.png" alt="" /></div>
  <div class="fp-deco-wrap"><img class="fp-deco fp-cover__blob2" src="assets/blob-green.png" alt="" /></div>
  <div class="fp-cover__top">
    <img class="fp-cover__logo" src="assets/cth-logo.png" alt="CleantechHUB" />
    <span class="fp-pill">Confidencial — equipos Datatón</span>
  </div>
  <div class="fp-cover__main">
    <div class="fp-cover__text">
      <p class="fp-eyebrow fp-eyebrow--lg">CleantechHUB · Datalab</p>
      <h1 class="fp-cover__title">${esc(s.title)}</h1>
      <p class="fp-cover__sub">${esc(s.subtitle)}</p>
      <p class="fp-cover__meta">${esc(s.client ?? "")} · ${esc(s.date)}</p>
    </div>
    ${art}
  </div>${notes(s)}
</section>`;
}

function renderStatement(s, stmtIndex = 1) {
  const foot = FOOT_DARK;
  const eyebrow = stmtIndex === 1 ? "Principio del método" : "Siguiente bloque";
  return `<section class="fp fp-statement fp--dark" data-cth-type="statement" data-background-color="#0C498A">
  <div class="fp-deco-wrap"><img class="fp-deco fp-statement__plant" src="assets/plant-white.png" alt="" /></div>
  <img class="fp-statement__logo" src="assets/cth-logo-white.png" alt="CleantechHUB" />
  <div class="fp-statement__body">
    <p class="fp-eyebrow fp-eyebrow--light">${eyebrow}</p>
    <p class="fp-statement__text">${esc(s.text)}</p>
    ${s.attribution ? `<p class="fp-statement__attr">${esc(s.attribution)}</p>` : ""}
  </div>
  ${foot}${notes(s)}
</section>`;
}

function renderEcosystem(s) {
  const nodes = s.nodes || [];
  const row1 = nodes.slice(0, 3);
  const row2 = nodes.slice(3);
  const card = (n, core) => `<div class="fp-card fp-eco__node fp-eco__node--${core ? "core" : "outer"}"><p class="fp-card__title">${esc(n.label)}</p><p class="fp-card__text">${esc(n.text)}</p></div>`;
  const rows = [];
  if (row1.length) rows.push(`<div class="fp-eco__row">${row1.map((n) => card(n, true)).join("")}</div>`);
  if (s.centre)
    rows.push(`<p class="fp-credit" style="text-align:center;font-weight:700;font-size:32px;color:#669348;margin:12px 0;">${esc(s.centre)}</p>`);
  if (row2.length) rows.push(`<div class="fp-eco__row">${row2.map((n) => card(n, false)).join("")}</div>`);
  return `<section class="fp fp-ecosystem" data-cth-type="ecosystem" data-background-color="#FFFFFF">
  ${head(s.title)}
  <div class="fp-body fp-eco">${rows.join("\n    ")}</div>
  ${FOOT}${notes(s)}
</section>`;
}

function renderProcess(s) {
  const steps = (s.steps || [])
    .map(
      (st, i) => `<div class="fp-step">
      <div class="fp-step__head"><span class="fp-step__n">${i + 1}</span><span class="fp-step__label">${esc(st.label)}</span></div>
      <div class="fp-step__body"><p class="fp-step__line">${esc(st.text)}</p></div>
    </div>`
    )
    .join("\n    ");
  const n = Math.min(Math.max((s.steps || []).length, 1), 6);
  return `<section class="fp fp-process" data-cth-type="process" data-background-color="#FFFFFF">
  <div class="fp-deco-wrap"><img class="fp-deco fp-blob-br" src="assets/blob-cyan.png" alt="" /></div>
  ${head(s.title)}
  <div class="fp-body fp-steps fp-steps--${n}">${steps}</div>
  ${FOOT}${notes(s)}
</section>`;
}

function renderTimeline(s) {
  const items = (s.items || [])
    .map(
      (it) => `<div class="fp-tl__item${it.date === "16:00" ? " fp-tl__item--key" : ""}">
      <div class="fp-tl__dot"></div>
      <div class="fp-tl__date">${esc(it.date)}</div>
      <p class="fp-tl__label">${esc(it.label)}</p>
      ${it.text ? `<p class="fp-tl__text">${esc(it.text)}</p>` : ""}
    </div>`
    )
    .join("\n    ");
  return `<section class="fp fp-timeline" data-cth-type="timeline" data-background-color="#FFFFFF">
  ${head(s.title)}
  <div class="fp-body fp-tl">${items}</div>
  ${FOOT}${notes(s)}
</section>`;
}

function renderShowcase(s) {
  const img = (s.images || [])[0];
  const shot = img
    ? `<div class="fp-cp__shot"><img src="${esc(img)}" alt="" /></div>`
    : "";
  return `<section class="fp fp-chart-proof fp-cp--mix" data-cth-type="showcase" data-background-color="#FFFFFF">
  <div class="fp-deco-wrap"><img class="fp-deco fp-blob-br" src="assets/blob-green.png" alt="" /></div>
  ${head(s.title)}
  <div class="fp-body fp-cp">
    ${shot}
    <div class="fp-cp__proof">
      <p class="fp-cp__cap">${esc(s.text)}</p>
      ${s.link ? `<p class="cth-source" style="font-size:17px;color:#69B5FA;margin-top:14px;">${esc(s.link)}</p>` : ""}
    </div>
  </div>
  ${FOOT}${notes(s)}
</section>`;
}

function renderCaseCards(s) {
  const heat = (s.cards || []).find((c) => c.image)?.image;
  const shot = heat
    ? `<div class="fp-cp__shot"><img src="${esc(heat)}" alt="" style="object-fit:contain;max-height:760px;" /></div>`
    : "";
  const cards = (s.cards || [])
    .map(
      (c) => `<div class="fp-card" style="margin-bottom:18px;"><p class="fp-card__title">${esc(c.name)}</p><p class="fp-card__text">${esc(c.text)}</p></div>`
    )
    .join("\n      ");
  return `<section class="fp fp-chart-proof" data-cth-type="case-cards" data-background-color="#FFFFFF">
  ${head(s.title)}
  <div class="fp-body fp-cp">
    ${shot}
    <div class="fp-cp__proof">${cards}</div>
  </div>
  ${FOOT}${notes(s)}
</section>`;
}

function renderKeyFacts(s) {
  const facts = (s.items || [])
    .map(
      (it) => `<div class="fp-fact"><div class="fp-fact__icon">${esc(it.icon)}</div><div><p class="fp-fact__label">${esc(it.label)}</p><p class="fp-fact__text">${esc(it.text)}</p></div></div>`
    )
    .join("\n    ");
  return `<section class="fp fp-key-facts" data-cth-type="key-facts" data-background-color="#FFFFFF">
  <div class="fp-deco-wrap"><img class="fp-deco fp-blob-br" src="assets/blob-cyan.png" alt="" /></div>
  ${head(s.title)}
  <div class="fp-body fp-facts">${facts}</div>
  ${FOOT}${notes(s)}
</section>`;
}

function renderTitleBullets(s) {
  const bullets = (s.bullets || []).map((b) => `<li>${esc(b)}</li>`).join("");
  return `<section class="fp fp-title-bullets" data-cth-type="title-bullets" data-background-color="#FFFFFF">
  <div class="fp-deco-wrap"><img class="fp-deco fp-blob-br" src="assets/blob-green.png" alt="" /></div>
  ${head(s.title, s.eyebrow)}
  <div class="fp-body">
    <div class="fp-card fp-col" style="max-width:100%;">
      <ul class="fp-bullets">${bullets}</ul>
    </div>
  </div>
  ${FOOT}${notes(s)}
</section>`;
}

function renderOffer(s) {
  const items = (s.includes || []).map((x) => `<li>${esc(x)}</li>`).join("");
  return `<section class="fp fp-offer" data-cth-type="offer" data-background-color="#FFFFFF">
  ${head(s.title)}
  <div class="fp-body fp-offer__grid" style="grid-template-columns:1fr;">
    <div class="fp-card fp-col">
      <p class="fp-col__head"><span style="text-transform:uppercase;font-size:22px;color:#669348;">${esc(s.currency)}</span> · ${esc(s.price)}</p>
      <ul class="fp-checks">${items}</ul>
      ${s.note ? `<p class="fp-cp__honest" style="margin-top:20px;">${esc(s.note)}</p>` : ""}
    </div>
  </div>
  ${FOOT}${notes(s)}
</section>`;
}

function renderContact(s) {
  const people = (s.people || [])
    .map(
      (p) => `<div class="fp-card fp-person"><p class="fp-person__name">${esc(p.name)}</p><p class="fp-person__role">${esc(p.role)}</p>${p.email ? `<p class="fp-person__mail">${esc(p.email)}</p>` : ""}</div>`
    )
    .join("\n    ");
  const chips = (s.links || [])
    .map((l) => `<span class="fp-chip">${esc(l.kind)}</span>`)
    .join("");
  return `<section class="fp fp-contact" data-cth-type="contact" data-background-color="#FFFFFF">
  <div class="fp-deco-wrap"><img class="fp-deco fp-blob-br" src="assets/blob-green.png" alt="" /></div>
  ${head(s.title)}
  <div class="fp-body fp-contact__grid" style="grid-template-columns:1fr;">${people}</div>
  ${chips ? `<div class="fp-chips">${chips}</div>` : ""}
  ${FOOT}${notes(s)}
</section>`;
}

const RENDERERS = {
  cover: renderCover,
  statement: renderStatement,
  ecosystem: renderEcosystem,
  process: renderProcess,
  timeline: renderTimeline,
  showcase: renderShowcase,
  "case-cards": renderCaseCards,
  "key-facts": renderKeyFacts,
  "title-bullets": renderTitleBullets,
  offer: renderOffer,
  contact: renderContact,
};

async function main() {
  const yamlMod = await import(path.join(toolNode, "js-yaml", "index.js"));
  const load = yamlMod.default?.load ?? yamlMod.load;
  const raw = fs.readFileSync(yamlPath, "utf8");
  const outline = load(raw);
  const sections = [];
  let stmtIdx = 0;
  for (const slide of outline.slides) {
    const fn = RENDERERS[slide.type];
    if (!fn) throw new Error(`No fp renderer for type ${slide.type}`);
    if (slide.type === "statement") {
      stmtIdx += 1;
      sections.push(fn(slide, stmtIdx));
    } else {
      sections.push(fn(slide));
    }
  }
  const title = esc(outline.meta.title);
  const html = `<!DOCTYPE html>
<html lang="${outline.meta.lang}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>${title}</title>
  <meta name="cth-deck-gated" content="true" />
  <link rel="stylesheet" href="reveal.js/dist/reveal.css" />
  <link rel="stylesheet" href="theme/cleantechhub.css" id="theme" />
  <link rel="stylesheet" href="assets/deck.css" />
</head>
<body>
  <div class="reveal">
    <div class="slides">
      ${sections.join("\n      ")}
    </div>
  </div>
  <script src="reveal.js/dist/reveal.js"></script>
  <script>
    Reveal.initialize({ hash: true, slideNumber: true, width: 1920, height: 1080, margin: 0.04 });
  </script>
</body>
</html>
`;
  fs.writeFileSync(path.join(__dirname, "index.html"), html, "utf8");
  console.log(`Wrote index.html (${sections.length} fp slides)`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});