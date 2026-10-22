/* CleantechHUB gap teaser — loads ./data.json from the instance folder. */
(function () {
  const PUBLIC_ORIGIN = "https://proposals.cleantechhub.net";
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

  /** Gap sections: EN shows English translation only; ES shows PDF link only (no verbatim Spanish block). */
  function renderGapReportEvidence(ev) {
    const href = pdfLink(ev);
    const enQ = ev.quote_en ? `"${esc(ev.quote_en)}"` : "";
    const translationBlock =
      lang === "en" && enQ
        ? `<p class="quote-label">${t("translation")}</p><p class="verbatim">${enQ}</p>`
        : "";
    return `<div class="quote-box report-evidence">
      ${translationBlock}
      <p class="pdf-link"><a href="${href}" target="_blank" rel="noopener">${t("pdfPage")} ${ev.page}</a></p>
    </div>`;
  }

  function favicon(domain) {
    return `https://www.google.com/s2/favicons?domain=${encodeURIComponent(domain)}&sz=64`;
  }

  function normalizeMatchName(name) {
    return String(name || "")
      .trim()
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");
  }

  /** First occurrence wins; prevents duplicate cards/details per startup within a gap. */
  function dedupeMatches(matches) {
    const seen = new Set();
    const out = [];
    for (const m of matches || []) {
      const key = normalizeMatchName(m.name);
      if (!key || seen.has(key)) continue;
      seen.add(key);
      out.push(m);
    }
    return out;
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
        const title = g.title[lang];
        const ctx = g.context[lang];
        const matches = dedupeMatches(g.matches);
        const cards = matches.map((m) => startupCard(m, g.rank)).join("");
        const evidence = renderGapReportEvidence(g.report_evidence);
        return `<section id="${g.id}" class="${secClass}"><div class="wrap">
          <div class="gap-head"><h2>${esc(title)}</h2></div>
          <div class="box"><p>${esc(ctx)}</p></div>
          ${evidence}
          <h3>${t("matches")}</h3>
          <div class="card-grid">${cards}</div>
        </div></section>`;
      })
      .join("");
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
    const slug = DATA.meta?.slug || DATA.meta?.company_key;
    if (slug) {
      let canonical = document.querySelector('link[rel="canonical"]');
      if (!canonical) {
        canonical = document.createElement("link");
        canonical.rel = "canonical";
        document.head.appendChild(canonical);
      }
      const path = slug.endsWith("-teaser") ? slug : `${slug}-teaser`;
      canonical.href = `${PUBLIC_ORIGIN}/${path}/`;
    }
    const logoPath = DATA.brand?.logo || "img/logo.png";
    document.querySelectorAll(".brand-logo").forEach((img) => {
      img.src = logoPath;
    });
    renderNav();
    renderGaps();
    renderTeam();
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
