/* CleantechHUB gap teaser — loads ./data.json from the instance folder. */
(function () {
  const UI_STATIC = {
    en: {
      reportVerbatim: "Sustainability report (verbatim, Spanish)",
      translation: "Translation (English)",
      pdfPage: "Open report PDF — page",
      publicQuote: "Public quote (verbatim, Spanish)",
      journey: "Journey step",
      matches: "Matches",
      how: "How this match relates to the gap",
      theme: "Theme",
      visit: "Visit",
      shortfallTrue: "shortfall: true",
      shortfallFalse: "shortfall: false",
      funder: "Funder",
      gapLabel: "Gap",
    },
    es: {
      reportVerbatim: "Reporte de sostenibilidad (literal, español)",
      translation: "Traducción (inglés)",
      pdfPage: "Abrir PDF del reporte — página",
      publicQuote: "Cita pública (literal, español)",
      journey: "Paso del journey",
      matches: "Coincidencias",
      how: "Cómo se relaciona con la brecha",
      theme: "Tema",
      visit: "Visitar",
      shortfallTrue: "shortfall: true",
      shortfallFalse: "shortfall: false",
      funder: "Financiador",
      gapLabel: "Brecha",
    },
  };

  const THEME = {
    EN: { CE: "Circular economy", BIO: "Bioeconomy", EN: "Energy" },
    ES: { CE: "Economía circular", BIO: "Bioeconomía", EN: "Energía" },
  };

  let DATA = null;
  let lang = localStorage.getItem("cth-teaser-lang") || "en";

  function t(key) {
    const ui = DATA?.ui?.[lang]?.[key];
    if (ui) return ui;
    return UI_STATIC[lang][key] || UI_STATIC.en[key] || key;
  }

  function esc(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function pdfLink(ev) {
    const base = ev.pdf_url || DATA.report.pdf_url;
    const page = ev.page;
    return `${base}#page=${page}`;
  }

  function renderReportQuote(ev) {
    const href = pdfLink(ev);
    const esQ = `"${esc(ev.quote_es)}"`;
    const enQ = ev.quote_en ? `"${esc(ev.quote_en)}"` : "";
    return `<div class="quote-box report-evidence">
      <p class="quote-label">${t("reportVerbatim")}</p>
      <p lang="es" class="verbatim">${esQ}</p>
      ${enQ ? `<p class="quote-label l-en">${t("translation")}</p><p class="l-en verbatim">${enQ}</p>` : ""}
      <p class="pdf-link"><a href="${href}" target="_blank" rel="noopener">${t("pdfPage")} ${ev.page}</a></p>
    </div>`;
  }

  function favicon(domain) {
    return `https://www.google.com/s2/favicons?domain=${encodeURIComponent(domain)}&sz=64`;
  }

  function startupCard(m, gapRank) {
    const nx = (DATA.nexus && DATA.nexus[m.name]) || {};
    const desc = lang === "es" ? nx.ds || m.description || "" : nx.d || m.description || "";
    const themeKey = nx.t;
    const theme = themeKey ? THEME[lang.toUpperCase()][themeKey] : "";
    const host = (m.website || "").replace(/^https?:\/\//, "").replace(/\/.*$/, "");
    return `<article class="card"><div class="cb"></div><div class="ct">
      <img class="thumb" src="${favicon(host)}" alt="" width="40" height="40" loading="lazy">
      <div class="cn">${esc(m.name)}</div></div>
      <div class="cd">${esc(desc)}</div>
      <div class="cbot">
      ${theme ? `<span class="chip">${t("theme")}: ${theme}</span>` : ""}
      ${m.funder ? `<span class="chip funder">${t("funder")}</span>` : `<span class="chip stage">${esc(m.stage || "")}</span>`}
      <span class="chip gap">${t("gapLabel")} ${gapRank}</span>
      ${nx.p ? `<span class="chip">${esc(nx.p)}</span>` : ""}
      <a class="chip" href="${esc(m.website)}" target="_blank" rel="noopener">${t("visit")}</a>
      </div></article>`;
  }

  function matchDetail(m) {
    const why = lang === "es" ? m.why_es || m.why : m.why;
    const pubQ = `"${esc(m.public_quote)}"`;
    return `<div class="match-detail"><h4>${esc(m.name)}</h4>
      <p class="why">${t("how")}: ${esc(why)}</p>
      <p class="quote-label">${t("publicQuote")}</p>
      <div class="quote-box"><p lang="es" class="verbatim">${pubQ}</p></div>
      <p class="src"><a href="${esc(m.public_source_url || m.website)}" target="_blank" rel="noopener">${esc(m.public_source_url || m.website)}</a></p>
    </div>`;
  }

  function renderNav() {
    const nav = document.getElementById("nav-gaps");
    if (!nav || !DATA.gaps) return;
    nav.innerHTML = DATA.gaps
      .map((g, i) => {
        const label = DATA.ui[lang][`nav.g${i + 1}`] || `Gap ${i + 1}`;
        return `<a href="#${g.id}">${esc(label)}</a>`;
      })
      .join("");
  }

  function renderGaps() {
    const root = document.getElementById("gaps-root");
    if (!root) return;
    root.innerHTML = DATA.gaps
      .map((g, i) => {
        const secClass = i % 2 ? "sec page" : "sec light";
        const sf = g.shortfall ? t("shortfallTrue") : t("shortfallFalse");
        const badgeClass = g.shortfall ? "badge warn" : "badge ok";
        const title = g.title[lang];
        const ctx = g.context[lang];
        const cards = g.matches.map((m) => startupCard(m, g.rank)).join("");
        const details = g.matches.map(matchDetail).join("");
        const journeyLine = `${t("journey")}: ${g.journey_step}. ${
          g.note ? g.note[lang] : `${t("matches")}: ${g.match_count}.`
        }`;
        const evidence = renderReportQuote(g.report_evidence);
        return `<section id="${g.id}" class="${secClass}"><div class="wrap">
          <div class="gap-head"><h2>${esc(title)}</h2><span class="${badgeClass}">${sf}</span></div>
          <div class="box"><p>${esc(ctx)}</p></div>
          ${evidence}
          <h3>${t("matches")}</h3>
          <div class="card-grid">${cards}</div>
          ${details}
          <p class="intro journey-line">${esc(journeyLine)}</p>
        </div></section>`;
      })
      .join("");
    const foot = DATA.footer_note;
    if (foot) {
      root.innerHTML += `<section class="sec"><div class="wrap"><div class="box blue">
        <p class="l-en">${foot.en}</p><p class="l-es">${foot.es}</p>
      </div></div></section>`;
    }
  }

  function renderTeam() {
    const root = document.getElementById("team-grid");
    if (!root || !DATA.team) return;
    root.innerHTML = DATA.team
      .map((person) => {
        const bio = person.bio[lang] || person.bio.en;
        const nick =
          person.nickname && person.nickname[lang]
            ? ` <span>(${esc(person.nickname[lang])})</span>`
            : "";
        return `<article class="team-card">
          <img src="${esc(person.photo)}" alt="${esc(person.name)}" width="400" height="420">
          <p class="kicker">${esc(person.role[lang] || person.role.en)}</p>
          <h3>${esc(person.name)}${nick}</h3>
          <p>${esc(bio)}</p>
        </article>`;
      })
      .join("");
  }

  function applyI18n() {
    document.documentElement.lang = lang;
    document.querySelectorAll("[data-i18n]").forEach((el) => {
      const k = el.getAttribute("data-i18n");
      const v = t(k);
      if (v) el.innerHTML = v;
    });
    document.querySelectorAll(".lang button").forEach((b) =>
      b.classList.toggle("on", b.dataset.lang === lang)
    );
    if (DATA.meta?.title) document.title = DATA.meta.title[lang] || DATA.meta.title.en;
    const logoPath = DATA.brand?.logo || "img/logo.png";
    document.querySelectorAll(".brand-logo").forEach((img) => {
      img.src = logoPath;
    });
    renderNav();
    renderGaps();
    renderTeam();
    const snapQuote = document.getElementById("snapshot-report-quote");
    if (snapQuote && DATA.snapshot?.report_evidence) {
      snapQuote.innerHTML = renderReportQuote(DATA.snapshot.report_evidence);
    }
    const ctaBtn = document.getElementById("cta-btn");
    if (ctaBtn && DATA.cta?.url) ctaBtn.href = DATA.cta.url;
  }

  function bindLang() {
    document.querySelectorAll(".lang button").forEach((btn) => {
      btn.addEventListener("click", () => {
        lang = btn.dataset.lang;
        localStorage.setItem("cth-teaser-lang", lang);
        applyI18n();
      });
    });
  }

  function showError(msg) {
    document.body.insertAdjacentHTML(
      "beforeend",
      `<p style="padding:2rem;color:#0C498A">${esc(msg)}</p>`
    );
  }

  fetch("./data.json")
    .then((r) => {
      if (!r.ok) throw new Error("data.json not found");
      return r.json();
    })
    .then((json) => {
      DATA = json;
      bindLang();
      applyI18n();
    })
    .catch((e) => showError("Could not load data.json. Serve this folder over HTTP (see README). " + e.message));
})();
