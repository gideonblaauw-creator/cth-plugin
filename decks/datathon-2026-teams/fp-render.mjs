#!/usr/bin/env node
/**
 * Render deck.yaml (+ deck-en.yaml) → bilingual index.html with FODESEP fp-* layout.
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const toolNode = path.resolve(__dirname, "../../tools/reveal/node_modules");
const yamlPath = path.join(__dirname, "deck.yaml");
const yamlEnPath = path.join(__dirname, "deck-en.yaml");
const yamlFpPath = path.join(__dirname, "deck-fp.yaml");

function foot(dark) {
  const cls = dark ? "fp-foot fp-foot--dark" : "fp-foot";
  return `<footer class="${cls}">
    <span class="l-es"><span class="fp-conf">Confidencial — piloto Datatón</span> · Datalab + Datatón · piloto Air4U · 24 nov 2026</span>
    <span class="l-en"><span class="fp-conf">Confidential — Datathon pilot</span> · Datalab + Datathon · Air4U pilot · 24 Nov 2026</span>
  </footer>`;
}

function esc(s) {
  return String(s ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function T(es, en) {
  if (!en || es === en) return esc(es);
  return `<span class="l-es">${esc(es)}</span><span class="l-en">${esc(en)}</span>`;
}

function pick(es, en) {
  return { es, en: en ?? es };
}

function photoLayers(bg, pos, scrim, scrimVariant) {
  if (!bg || bg === "navy") return "";
  const position = pos ? `background-position:${esc(pos)};` : "";
  const scrimCls = scrim === "light" ? " fp-photo-scrim--light" : "";
  const variantCls = scrimVariant ? ` fp-photo-scrim--${esc(scrimVariant)}` : "";
  return `<div class="fp-photo-bg" style="background-image:url('${esc(bg)}');${position}" role="presentation"></div>
  <div class="fp-photo-scrim${scrimCls}${variantCls}" aria-hidden="true"></div>`;
}

function sectionOpen(cls, type, bg, extra = "", pos, scrim, boost, bleed, scrimVariant) {
  const photo = bg && bg !== "navy" ? " fp-has-photo" : "";
  const navy = bg === "navy" ? " fp--navy-only" : "";
  const boostCls = boost ? ` fp-photo-boost--${esc(boost)}` : "";
  const bleedCls = bleed === "full" ? " fp-photo-bleed--full" : "";
  const bgColor = navy || photo ? "#0C498A" : "#FFFFFF";
  return `<section class="fp ${cls}${photo}${navy}${boostCls}${bleedCls}${extra}" data-cth-type="${esc(type)}" data-background-color="${bgColor}">
  ${photoLayers(bg, pos, scrim, scrimVariant)}`;
}

function renderCpStats(stats, statsEn) {
  if (!stats?.length) return "";
  const tiles = stats
    .map((st, i) => {
      const stEn = statsEn?.[i] || {};
      const lab = st.label ?? st.label_es;
      const labEn = stEn.label ?? st.label_en ?? st.label_es;
      return `<div class="fp-cp__stat"><span class="fp-cp__v">${esc(st.value)}</span><span class="fp-cp__l">${T(lab, labEn)}</span></div>`;
    })
    .join("");
  return `<div class="fp-cp__stats">${tiles}</div>`;
}

function renderTrioRow(cards, cardsEn) {
  if (!cards?.length) return "";
  const n = Math.min(cards.length, 4);
  const items = cards
    .map((c, i) => {
      const cEn = cardsEn?.[i] || {};
      const title = c.title ?? c.title_es ?? c.name;
      const titleEn = cEn.title ?? c.title_en ?? cEn.name;
      return `<div class="fp-card fp-trio__card fp-card--fill"><p class="fp-card__title">${T(title, titleEn)}</p><p class="fp-card__text">${T(c.text ?? c.text_es, cEn.text ?? c.text_en)}</p></div>`;
    })
    .join("");
  return `<div class="fp-trio fp-trio--${n}">${items}</div>`;
}

function renderCalloutBand(s, sEn) {
  const text = s.callout ?? s.callout_es;
  if (!text) return "";
  const textEn = sEn?.callout ?? s.callout_en;
  return `<p class="fp-note fp-note--box fp-fill-callout">${T(text, textEn ?? text)}</p>`;
}

function renderCtas(ctas, ctasEn) {
  if (!ctas?.length) return "";
  const btns = ctas
    .map((c, i) => {
      const cEn = ctasEn?.[i] || {};
      return `<a class="fp-btn" href="${esc(c.url)}">${T(c.label ?? c.label_es, cEn.label ?? c.label_en)}</a>`;
    })
    .join("");
  return `<div class="fp-cp__cta fp-contact__cta">${btns}</div>`;
}

function fillExtras(s, sEn) {
  const parts = [
    renderCpStats(s.stat_strip, sEn?.stat_strip),
    renderTrioRow(s.trio_row, sEn?.trio_row),
    renderCalloutBand(s, sEn),
    renderCtas(s.ctas, sEn?.ctas),
  ].filter(Boolean);
  if (!parts.length) return "";
  return `<div class="fp-fill-extras">${parts.join("\n    ")}</div>`;
}

function timelineDate(it) {
  if (it.date === "16:00") return esc(it.date);
  if (it.date === "confirm" || it.date === "[confirmar]" || it.date === "[confirm]") {
    return `<span class="fp-tl__confirm"><span class="l-es">por confirmar</span><span class="l-en">to confirm</span></span>`;
  }
  return esc(it.date);
}

function head(title, kicker, titleEn, kickerEn) {
  const ey = kicker
    ? `<p class="fp-eyebrow">${T(kicker, kickerEn)}</p>`
    : "";
  return `<header class="fp-head"><div class="fp-head__text">${ey}<h2 class="fp-title">${T(title, titleEn)}</h2></div><img class="fp-head__logo" src="assets/cth-logo.png" alt="CleantechHUB" /></header>`;
}

function notes(slide) {
  return slide.notes
    ? `\n  <aside class="notes">${esc(slide.notes)}</aside>`
    : "";
}

function sourceLine(s, sEn) {
  const line = s.source || s.link;
  const lineEn = sEn?.source || sEn?.link || line;
  if (!line) return "";
  return `<p class="cth-source fp-source">${T(line, lineEn)}</p>`;
}

function takeaway(s, sEn) {
  if (!s.takeaway) return "";
  return `<p class="fp-takeaway">${T(s.takeaway, sEn?.takeaway)}</p>`;
}

function renderCover(s, sEn) {
  const bg = s.bg;
  const chips = (s.method_chips || [])
    .map((c, i) => {
      const cEn = (sEn?.method_chips || [])[i] ?? c;
      return `<span class="fp-method-chip">${T(c, cEn)}</span>`;
    })
    .join("");
  const chipRow = chips
    ? `<div class="fp-method-chips" role="list">${chips}</div>`
    : "";
  return `${sectionOpen("fp-cover", "cover", bg, bg ? " fp-cover--photo" : "", s.bg_position, s.photo_scrim, s.photo_boost, s.photo_bleed, s.photo_scrim_variant)}
  <div class="fp-deco-wrap"><img class="fp-deco fp-cover__blob" src="assets/blob-cyan.png" alt="" /></div>
  <div class="fp-deco-wrap"><img class="fp-deco fp-cover__blob2" src="assets/blob-green.png" alt="" /></div>
  <div class="fp-cover__top">
    <img class="fp-cover__logo" src="${bg ? "assets/cth-logo-white.png" : "assets/cth-logo.png"}" alt="CleantechHUB" />
    <span class="fp-pill">${T("Confidencial — equipos Datatón", "Confidential — Datathon teams")}</span>
  </div>
  <div class="fp-cover__main fp-cover__main--chips">
    <div class="fp-cover__text">
      <p class="fp-eyebrow fp-eyebrow--lg">${T("CleantechHUB · Datalab", "CleantechHUB · Datalab")}</p>
      <h1 class="fp-cover__title">${T(s.title, sEn.title)}</h1>
      <p class="fp-cover__sub">${T(s.subtitle, sEn.subtitle)}</p>
      <p class="fp-cover__meta">${T(`${s.client ?? ""} · ${s.date}`, `${sEn.client ?? s.client} · ${sEn.date ?? s.date}`)}</p>
      ${chipRow}
    </div>
  </div>${notes(s)}
</section>`;
}

function renderStatement(s, sEn, stmtIndex = 1) {
  const kicker =
    stmtIndex === 1
      ? pick("Principio del método", "Method principle")
      : pick("Siguiente bloque", "Next block");
  const bg = s.bg;
  return `${sectionOpen("fp-statement fp--dark", "statement", bg, "", s.bg_position, s.photo_scrim, s.photo_boost, s.photo_bleed, s.photo_scrim_variant)}
  <div class="fp-deco-wrap"><img class="fp-deco fp-statement__plant" src="assets/plant-white.png" alt="" /></div>
  <img class="fp-statement__logo" src="assets/cth-logo-white.png" alt="CleantechHUB" />
  <div class="fp-statement__body">
    <p class="fp-eyebrow fp-eyebrow--light">${T(kicker.es, kicker.en)}</p>
    <p class="fp-statement__text">${T(s.text, sEn.text)}</p>
    ${s.attribution ? `<p class="fp-statement__attr">${T(s.attribution, sEn.attribution)}</p>` : ""}
  </div>
  ${foot(true)}${notes(s)}
</section>`;
}

function renderEcosystem(s, sEn) {
  const nodes = s.nodes || [];
  const nodesEn = sEn.nodes || [];
  const row1 = nodes.slice(0, 3);
  const row2 = nodes.slice(3);
  const card = (n, nEn, core) =>
    `<div class="fp-card fp-eco__node fp-eco__node--${core ? "core" : "outer"} fp-card--fill"><p class="fp-card__title">${T(n.label, nEn?.label)}</p><p class="fp-card__text">${T(n.text, nEn?.text)}</p></div>`;
  const rows = [];
  if (row1.length)
    rows.push(
      `<div class="fp-eco__row">${row1.map((n, i) => card(n, nodesEn[i], true)).join("")}</div>`
    );
  if (s.centre)
    rows.push(
      `<p class="fp-credit" style="text-align:center;font-weight:700;font-size:32px;color:#669348;margin:12px 0;">${esc(s.centre)}</p>`
    );
  if (row2.length)
    rows.push(
      `<div class="fp-eco__row">${row2.map((n, i) => card(n, nodesEn[i + 3], false)).join("")}</div>`
    );
  const fill = s.layout === "fill" ? " fp-ecosystem--fill" : "";
  return `${sectionOpen(`fp-ecosystem${fill}`, "ecosystem", s.bg, "", s.bg_position)}
  ${head(s.title, s.kicker ?? "Metodología", sEn.title, sEn.kicker ?? "Methodology")}
  <div class="fp-body fp-eco">${rows.join("\n    ")}</div>
  ${fillExtras(s, sEn)}
  ${sourceLine(s, sEn)}
  ${foot(false)}${notes(s)}
</section>`;
}

function renderProcess(s, sEn) {
  const steps = s.steps || [];
  const stepsEn = sEn.steps || [];
  const body = steps
    .map(
      (st, i) => `<div class="fp-step fp-step--fill">
      <div class="fp-step__head"><span class="fp-step__n">${i + 1}</span><span class="fp-step__label">${T(st.label, stepsEn[i]?.label)}</span></div>
      <div class="fp-step__body"><p class="fp-step__line">${T(st.text, stepsEn[i]?.text)}</p></div>
    </div>`
    )
    .join("\n    ");
  const n = Math.min(Math.max(steps.length, 1), 6);
  const fill = s.layout === "fill" ? " fp-process--fill" : "";
  return `${sectionOpen(`fp-process${fill}`, "process", s.bg)}
  <div class="fp-deco-wrap"><img class="fp-deco fp-blob-br" src="assets/blob-cyan.png" alt="" /></div>
  ${head(s.title, s.kicker ?? "Metodología", sEn.title, sEn.kicker ?? "Methodology")}
  <div class="fp-body fp-steps fp-steps--${n}">${body}</div>
  ${sourceLine(s, sEn)}
  ${foot(false)}${notes(s)}
</section>`;
}

function renderTimeline(s, sEn) {
  const items = s.items || [];
  const itemsEn = sEn.items || [];
  const body = items
    .map(
      (it, i) => `<div class="fp-tl__item${it.date === "16:00" ? " fp-tl__item--key" : ""}">
      <div class="fp-tl__dot"></div>
      <div class="fp-tl__date">${timelineDate(it)}</div>
      <p class="fp-tl__label">${T(it.label, itemsEn[i]?.label)}</p>
      ${it.text ? `<p class="fp-tl__text">${T(it.text, itemsEn[i]?.text)}</p>` : ""}
    </div>`
    )
    .join("\n    ");
  return `${sectionOpen("fp-timeline", "timeline", s.bg)}
  ${head(s.title, s.kicker ?? "Metodología", sEn.title, sEn.kicker ?? "Methodology")}
  <div class="fp-body fp-tl">${body}</div>
  ${sourceLine(s, sEn)}
  ${foot(false)}${notes(s)}
</section>`;
}

function renderShowcase(s, sEn) {
  const img = (s.images || [])[0];
  const zoom = s.shot_zoom ? ` transform:scale(${s.shot_zoom}); transform-origin:top center;` : "";
  const shot = img
    ? `<div class="fp-cp__shot fp-cp__shot--zoom"><img src="${esc(img)}" alt="" style="${zoom}" /></div>`
    : "";
  const dark = s.bg ? " fp-chart-proof--photo" : "";
  return `${sectionOpen(`fp-chart-proof fp-cp--mix${dark}`, "showcase", s.bg, "", s.bg_position, s.photo_scrim, s.photo_boost, s.photo_bleed, s.photo_scrim_variant)}
  <div class="fp-deco-wrap"><img class="fp-deco fp-blob-br" src="assets/blob-green.png" alt="" /></div>
  ${head(s.title, s.kicker ?? "Ejemplo · piloto Air4U", sEn.title, sEn.kicker)}
  <div class="fp-body fp-cp">
    ${shot}
    <div class="fp-cp__proof">
      <p class="fp-cp__cap">${T(s.text, sEn.text)}</p>
      ${takeaway(s, sEn)}
      ${sourceLine(s, sEn)}
    </div>
  </div>
  ${foot(false)}${notes(s)}
</section>`;
}

function renderCaseCards(s, sEn) {
  const heat = (s.cards || []).find((c) => c.image)?.image;
  const tall = s.shot_tall ? " fp-cp__shot--tall" : "";
  const shot = heat
    ? `<div class="fp-cp__shot${tall}"><img src="${esc(heat)}" alt="" style="object-fit:contain;max-height:${s.shot_tall ? "840" : "760"}px;width:100%;" /></div>`
    : "";
  const cards = s.cards || [];
  const cardsEn = sEn.cards || [];
  const cardHtml = cards
    .map(
      (c, i) => `<div class="fp-card fp-card--fill" style="margin-bottom:18px;"><p class="fp-card__title">${T(c.name, cardsEn[i]?.name)}</p><p class="fp-card__text">${T(c.text, cardsEn[i]?.text)}</p></div>`
    )
    .join("\n      ");
  const dark = s.bg ? " fp-chart-proof--photo" : "";
  return `${sectionOpen(`fp-chart-proof${dark}`, "case-cards", s.bg)}
  ${head(s.title, s.kicker, sEn.title, sEn.kicker)}
  <div class="fp-body fp-cp">
    ${shot}
    <div class="fp-cp__proof">${cardHtml}${takeaway(s, sEn)}${sourceLine(s, sEn)}</div>
  </div>
  ${foot(false)}${notes(s)}
</section>`;
}

function renderHoja4Native() {
  const nd = pick("[sin dato]", "[no data]");
  const field = (labEs, labEn, placeholder = nd) =>
    `<div class="fp-h4__row"><span class="fp-h4__lab">${T(labEs, labEn)}</span><span class="fp-h4__val">${T(placeholder.es, placeholder.en)}</span></div>`;
  const panels = [
    {
      title: pick("Línea base del cliente", "Client baseline"),
      role: pick("(entrada)", "(input)"),
    },
    {
      title: pick("Delta del innovador", "Innovator delta"),
      role: pick("(salida)", "(output)"),
    },
    {
      title: pick("Panorama de datos abiertos", "Open-data landscape"),
      role: pick("(entrada)", "(input)"),
    },
  ];
  const panelHtml = panels
    .map(
      (p) => `<div class="fp-h4__panel fp-card fp-card--fill">
      <p class="fp-h4__panel-title">${T(p.title.es, p.title.en)} <span class="fp-h4__panel-role">${T(p.role.es, p.role.en)}</span></p>
      ${field("Valor", "Value")}
      ${field("Rango", "Range")}
      ${field("Confianza", "Confidence", pick("firme / estimado", "firm / estimated"))}
      ${field("Por qué", "Why")}
      ${field("Grada", "Ladder step")}
    </div>`
    )
    .join("\n      ");
  const bridge = pick(
    "Delta: donde el dato se vuelve valor",
    "Delta: where data becomes value"
  );
  const flow = pick("entradas → salida → línea de valor", "inputs → output → value line");
  const foot = pick(
    "sin tablero público mientras los derechos de datos estén abiertos",
    "no public dashboard while data rights remain open"
  );
  return `<div class="fp-h4 fp-dash__solo" role="img" aria-label="Hoja 4 plantilla">
    <div class="fp-h4__head">
      <div class="fp-h4__hdr">${T("Usuario", "User")}<span class="fp-h4__blank"></span></div>
      <div class="fp-h4__hdr">${T("Decisión", "Decision")}<span class="fp-h4__blank"></span></div>
    </div>
    <p class="fp-h4__delta"><span class="fp-h4__delta-label">${T(bridge.es, bridge.en)}</span><span class="fp-h4__delta-flow">${T(flow.es, flow.en)}</span></p>
    <div class="fp-h4__panels">${panelHtml}</div>
    <p class="fp-h4__foot">${T(foot.es, foot.en)}</p>
  </div>`;
}

function renderDashboardTemplate(s, sEn) {
  const img = s.native_template ? null : (s.images || [])[0];
  const shot = img ? `<div class="fp-dash__solo"><img src="${esc(img)}" alt="" /></div>` : renderHoja4Native();
  const capEs =
    s.template_caption_es ??
    "Ejemplo diligenciado (Hoja 4b): en el paquete de equipo v0.3-es — no en esta lámina.";
  const capEn =
    sEn?.template_caption_en ??
    s.template_caption_en ??
    "Filled example (Sheet 4b): in team pack v0.3-es — not on this slide.";
  return `${sectionOpen("fp-chart-proof fp-dash-solo", "dashboard-template", s.bg)}
  ${head(s.title, s.kicker, sEn.title, sEn.kicker)}
  <div class="fp-body fp-dash-solo__body">
    ${shot}
    <p class="fp-dash__pack-ref">${T(capEs, capEn)}</p>
    <p class="fp-cp__cap">${T(s.text, sEn.text)}</p>
    ${takeaway(s, sEn)}
    ${sourceLine(s, sEn)}
  </div>
  ${foot(false)}${notes(s)}
</section>`;
}

function renderDashboardDuo(s, sEn) {
  const imgs = s.images || [];
  const labels = pick("Plantilla en blanco", "Blank template");
  const labels2 = pick("Ejemplo Air4U (relleno)", "Filled Air4U example");
  const capEn = s.caption_en || sEn.caption_en;
  const shots = imgs
    .map((src, i) => {
      const lab = i === 0 ? labels : labels2;
      return `<figure class="fp-dash__fig"><img src="${esc(src)}" alt="" /><figcaption>${T(lab.es, lab.en)}</figcaption></figure>`;
    })
    .join("\n      ");
  const bridge = pick(
    "Delta: donde el dato se vuelve valor",
    "Delta: where data becomes value"
  );
  return `${sectionOpen("fp-chart-proof fp-dash-duo", "dashboard-duo", s.bg)}
  ${head(s.title, s.kicker, sEn.title, sEn.kicker)}
  <div class="fp-body fp-dash">
    <p class="fp-dash__bridge">${T(bridge.es, bridge.en)}</p>
    <div class="fp-dash__grid">${shots}</div>
    <p class="fp-cp__cap">${T(s.text, sEn.text)}</p>
    ${takeaway(s, sEn)}
    ${capEn ? `<p class="fp-dash__caption">${T(capEn, sEn.caption_en ?? capEn)}</p>` : ""}
    ${sourceLine(s, sEn)}
  </div>
  ${foot(false)}${notes(s)}
</section>`;
}

function renderKeyFacts(s, sEn) {
  const items = s.items || [];
  const itemsEn = sEn.items || [];
  const fill = s.layout === "fill" ? " fp-key-facts--fill" : "";
  const facts = items
    .map(
      (it, i) => `<div class="fp-fact fp-fact--fill"><div class="fp-fact__icon">${esc(it.icon)}</div><div><p class="fp-fact__label">${T(it.label, itemsEn[i]?.label)}</p><p class="fp-fact__text">${T(it.text, itemsEn[i]?.text)}</p></div></div>`
    )
    .join("\n    ");
  return `${sectionOpen(`fp-key-facts${fill}`, "key-facts", s.bg)}
  <div class="fp-deco-wrap"><img class="fp-deco fp-blob-br" src="assets/blob-cyan.png" alt="" /></div>
  ${head(s.title, s.kicker, sEn.title, sEn.kicker)}
  <div class="fp-body fp-facts">${facts}</div>
  ${fillExtras(s, sEn)}
  ${sourceLine(s, sEn)}
  ${foot(false)}${notes(s)}
</section>`;
}

function renderTitleBullets(s, sEn) {
  const bullets = s.bullets || [];
  const bulletsEn = sEn.bullets || [];
  const lis = bullets.map((b, i) => `<li>${T(b, bulletsEn[i] ?? b)}</li>`).join("");
  const fill = s.layout === "fill" ? " fp-title-bullets--fill" : "";
  return `${sectionOpen(`fp-title-bullets${fill}`, "title-bullets", s.bg)}
  <div class="fp-deco-wrap"><img class="fp-deco fp-blob-br" src="assets/blob-green.png" alt="" /></div>
  ${head(s.title, s.kicker, sEn.title, sEn.kicker)}
  <div class="fp-body">
    <div class="fp-card fp-col fp-card--fill" style="max-width:100%;">
      <ul class="fp-bullets">${lis}</ul>
    </div>
  </div>
  ${fillExtras(s, sEn)}
  ${sourceLine(s, sEn)}
  ${foot(false)}${notes(s)}
</section>`;
}

function renderOffer(s, sEn) {
  const inc = s.includes || [];
  const incEn = sEn.includes || [];
  const items = inc.map((x, i) => `<li>${T(x, incEn[i] ?? x)}</li>`).join("");
  const fill = s.layout === "fill" ? " fp-offer--fill" : "";
  return `${sectionOpen(`fp-offer${fill}`, "offer", s.bg)}
  ${head(s.title, s.kicker ?? "Metodología", sEn.title, sEn.kicker)}
  <div class="fp-body fp-offer__grid" style="grid-template-columns:1fr;">
    <div class="fp-card fp-col fp-card--fill">
      <p class="fp-col__head"><span style="text-transform:uppercase;font-size:22px;color:#669348;">${esc(s.currency)}</span> · ${T(s.price, sEn.price)}</p>
      <ul class="fp-checks">${items}</ul>
      ${s.note ? `<p class="fp-cp__honest" style="margin-top:20px;">${T(s.note, sEn.note)}</p>` : ""}
    </div>
  </div>
  ${fillExtras(s, sEn)}
  ${sourceLine(s, sEn)}
  ${foot(false)}${notes(s)}
</section>`;
}

function renderContact(s, sEn) {
  const people = s.people || [];
  const peopleEn = sEn.people || [];
  const links = s.links || [];
  const body = people
    .map((p, i) => {
      const pe = peopleEn[i] || p;
      const linkLines = links
        .map((l) => `<p class="fp-person__link"><a href="${esc(l.url)}">${esc(l.kind)}</a></p>`)
        .join("");
      return `<div class="fp-card fp-person fp-card--fill"><p class="fp-person__name">${T(p.name, pe.name)}</p><p class="fp-person__role">${T(p.role, pe.role)}</p>${p.email ? `<p class="fp-person__mail">${esc(p.email)}</p>` : ""}${linkLines}</div>`;
    })
    .join("\n    ");
  return `${sectionOpen("fp-contact", "contact", s.bg)}
  <div class="fp-deco-wrap"><img class="fp-deco fp-blob-br" src="assets/blob-green.png" alt="" /></div>
  ${head(s.title, s.kicker ?? "Contacto", sEn.title, sEn.kicker ?? "Contact")}
  <div class="fp-body fp-contact__grid" style="grid-template-columns:1fr;">${body}</div>
  ${fillExtras(s, sEn)}
  ${foot(false)}${notes(s)}
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
  "dashboard-duo": renderDashboardDuo,
  "dashboard-template": renderDashboardTemplate,
  "key-facts": renderKeyFacts,
  "title-bullets": renderTitleBullets,
  offer: renderOffer,
  contact: renderContact,
};

const LANG_SCRIPT = `
(function () {
  function applyLang(lang) {
    document.body.setAttribute('data-lang', lang);
    document.documentElement.setAttribute('lang', lang);
    document.querySelectorAll('.lang-toggle button').forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-set-lang') === lang ? 'true' : 'false');
    });
  }
  var q = new URLSearchParams(location.search);
  var start = q.get('lang') === 'en' ? 'en' : 'es';
  applyLang(start);
  document.querySelectorAll('.lang-toggle button').forEach(function (btn) {
    btn.addEventListener('click', function () { applyLang(btn.getAttribute('data-set-lang')); });
  });
})();
`;

async function main() {
  const yamlMod = await import(path.join(toolNode, "js-yaml", "index.js"));
  const load = yamlMod.default?.load ?? yamlMod.load;
  const outline = load(fs.readFileSync(yamlPath, "utf8"));
  const outlineEn = load(fs.readFileSync(yamlEnPath, "utf8"));
  const fpOverlay = load(fs.readFileSync(yamlFpPath, "utf8"));
  const fpSlides = fpOverlay.slides || [];
  const slidesEn = outlineEn.slides || [];
  const sections = [];
  let stmtIdx = 0;
  outline.slides.forEach((base, idx) => {
    const slide = { ...base, ...(fpSlides[idx] || {}) };
    const slideEn = slidesEn[idx] || {};
    const type = slide.render_as || slide.type;
    const fn = RENDERERS[type];
    if (!fn) throw new Error(`No fp renderer for type ${type} (slide ${idx + 1})`);
    if (type === "statement") {
      stmtIdx += 1;
      sections.push(fn(slide, slideEn, stmtIdx));
    } else {
      sections.push(fn(slide, slideEn));
    }
  });
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
<body data-lang="es">
  <div class="lang-toggle" role="group" aria-label="Idioma / Language">
    <button type="button" data-set-lang="es" aria-pressed="true">ES</button>
    <button type="button" data-set-lang="en" aria-pressed="false">EN</button>
  </div>
  <div class="reveal">
    <div class="slides">
      ${sections.join("\n      ")}
    </div>
  </div>
  <script src="reveal.js/dist/reveal.js"></script>
  <script>
    Reveal.initialize({ hash: true, slideNumber: true, width: 1920, height: 1080, margin: 0.04 });
    ${LANG_SCRIPT}
  </script>
</body>
</html>
`;
  fs.writeFileSync(path.join(__dirname, "index.html"), html, "utf8");
  console.log(`Wrote index.html (${sections.length} fp slides, ES+EN)`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});