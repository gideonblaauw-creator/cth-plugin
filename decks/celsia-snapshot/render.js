(function () {
  const PUBLIC_ORIGIN = "https://proposals.cleantechhub.net";
  const DASH = "—";
  const NOT_STATED = /not stated|no indicado|not stated on/i;

  let DATA = null;
  let lang = localStorage.getItem("cth-snapshot-lang") || "en";
  let activeGap = 0;

  function t(key) {
    return DATA?.ui?.[lang]?.[key] || DATA?.ui?.en?.[key] || "";
  }

  function esc(s) {
    return String(s ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function cell(v) {
    if (!v || NOT_STATED.test(String(v))) return DASH;
    return esc(v);
  }

  function favicon(domain) {
    return `https://www.google.com/s2/favicons?domain=${encodeURIComponent(domain)}&sz=64`;
  }

  function themeLabel(key) {
    const map = {
      en: { CE: "Circular economy", BIO: "Bioeconomy", EN: "Energy" },
      es: { CE: "Economía circular", BIO: "Bioeconomía", EN: "Energía" },
    };
    return map[lang][key] || "";
  }

  function renderBarChart(gap) {
    const ch = gap.chart || {};
    const bars = ch.bars || [];
    if (!bars.length) {
      const note = ch.note?.[lang] || ch.note?.en || "";
      return note ? `<p class="one-line">${esc(note)}</p>` : "";
    }
    const max = Math.max(...bars.map((b) => b.max || b.value || 1), 1);
    const rows = bars
      .map((b) => {
        const pct = Math.min(100, Math.round(((b.value || 0) / max) * 100));
        const lab = b.label?.[lang] || b.label?.en || "";
        const disp =
          b.display ||
          `${b.value}${b.unit || ""}`;
        return `<div class="bar-row"><span>${esc(lab)}</span><div class="bar-track"><div class="bar-fill" style="width:${pct}%"></div></div><span class="bar-val">${esc(disp)}</span></div>`;
      })
      .join("");
    const src = ch.source?.[lang] || ch.source?.en || "";
    return `<div class="bar-chart">${rows}<p class="pdf-link">${esc(src)}</p></div>`;
  }

  function renderMetricsTable(gap) {
    const rows = (gap.datalab?.[lang]?.startup_metrics || [])
      .map(
        (r) =>
          `<tr><td>${esc(r.startup)}</td><td>${esc(r.metric)}</td><td>${cell(r.unit)}</td><td>${cell(r.frequency)}</td><td>${cell(r.method)}</td><td><a href="${esc(r.source)}" target="_blank" rel="noopener">${esc(r.source)}</a></td></tr>`
      )
      .join("");
    const head =
      lang === "es"
        ? "<tr><th>Startup</th><th>Métrica</th><th>Unidad</th><th>Frecuencia</th><th>Método</th><th>Fuente</th></tr>"
        : "<tr><th>Startup</th><th>Metric</th><th>Unit</th><th>Frequency</th><th>Method</th><th>Source</th></tr>";
    return `<table class="data-table"><thead>${head}</thead><tbody>${rows}</tbody></table>`;
  }

  function renderFlow(gap) {
    const flow = gap.datalab?.[lang]?.flow || {};
    const keys = ["l1", "l2", "l3"];
    const nodes = keys
      .map((k, i) => {
        const label = k.toUpperCase();
        return `<button type="button" class="flow-node${i === 0 ? " on" : ""}" data-flow="${i}">${esc(label)}</button>`;
      })
      .join("");
    const detail = keys.map((k) => flow[k] || "").filter(Boolean);
    return `<div class="flow-diagram" data-gap="${gap.rank}">${nodes}</div><div class="flow-detail" id="flow-detail-${gap.rank}">${esc(detail[0] || "")}</div>`;
  }

  function renderNxCards(matches, gapRank) {
    return matches
      .map((m) => {
        const nx = DATA.nexus?.[m.name] || {};
        const desc = lang === "es" ? nx.ds || "" : nx.d || "";
        const host = (m.website || "").replace(/^https?:\/\//, "").split("/")[0];
        const theme = nx.t ? themeLabel(nx.t) : "";
        return `<article class="nx-card"><div class="top"><img class="th" src="${favicon(host)}" alt="" width="40" height="40"><strong>${esc(m.name)}</strong></div><p class="one-line">${esc(desc)}</p><div>${theme ? `<span class="chip">${esc(theme)}</span>` : ""}<span class="chip">${t("nav.g1").replace(/\d+/, gapRank)}</span>${nx.p ? `<span class="chip">${esc(nx.p)}</span>` : ""}<a class="chip" href="${esc(m.website)}" target="_blank" rel="noopener">${lang === "es" ? "Visitar" : "Visit"}</a></div></article>`;
      })
      .join("");
  }

  function renderGapPanel(g, i) {
    const title = g.title[lang];
    const head = g.headline?.[lang] || "";
    const dl = g.datalab?.[lang] || {};
    return `<div class="gap-panel${i === activeGap ? " on" : ""}" id="gap-panel-${i}" role="tabpanel">
      <div class="gap-card">
        <h3>${esc(title)}</h3>
        <p class="one-line">${esc(head)}</p>
        ${renderBarChart(g)}
        <h4>${t("datalab.bLabel")}</h4>
        ${renderMetricsTable(g)}
        <h4>${t("datalab.cLabel")}</h4>
        ${renderFlow(g)}
        <p class="one-line"><strong>${t("datalab.dLabel")}:</strong> ${esc(dl.deliverable || "")}</p>
        <h4>${lang === "es" ? "Coincidencias" : "Matches"}</h4>
        <div class="nx-grid">${renderNxCards(g.matches || [], g.rank)}</div>
        <p class="pdf-link"><a href="${esc(g.report_evidence.pdf_url)}#page=${g.report_evidence.page}" target="_blank" rel="noopener">${lang === "es" ? "PDF página" : "PDF page"} ${g.report_evidence.page}</a></p>
      </div>
    </div>`;
  }

  function bindFlowClicks() {
    document.querySelectorAll(".flow-diagram").forEach((wrap) => {
      const rank = +wrap.dataset.gap;
      const gap = DATA.gaps.find((g) => g.rank === rank);
      const detail = document.getElementById(`flow-detail-${rank}`);
      if (!gap || !detail) return;
      const texts = ["l1", "l2", "l3"].map((k) => gap.datalab?.[lang]?.flow?.[k] || "");
      wrap.querySelectorAll(".flow-node").forEach((btn) => {
        btn.addEventListener("click", () => {
          wrap.querySelectorAll(".flow-node").forEach((b) => b.classList.remove("on"));
          btn.classList.add("on");
          const idx = +btn.dataset.flow;
          detail.textContent = texts[idx] || "";
        });
      });
    });
  }

  function allStartupsRows() {
    const rows = [];
    const seen = new Set();
    for (const g of DATA.gaps || []) {
      for (const m of g.matches || []) {
        const k = m.name.toLowerCase();
        if (seen.has(k)) continue;
        seen.add(k);
        const nx = DATA.nexus?.[m.name] || {};
        rows.push({
          name: m.name,
          gap: g.rank,
          theme: nx.t || "",
          stage: m.stage || "",
          website: m.website || "",
        });
      }
    }
    return rows;
  }

  function renderCompare() {
    const thead = document.querySelector("#compare-table thead");
    const tbody = document.querySelector("#compare-table tbody");
    const filters = document.getElementById("compare-filters");
    if (!thead || !tbody || !filters) return;
    const rows = allStartupsRows();
    const themes = [...new Set(rows.map((r) => r.theme).filter(Boolean))];
    filters.innerHTML =
      `<label>${lang === "es" ? "Brecha" : "Gap"} <select id="f-gap"><option value="">All</option>${DATA.gaps.map((g) => `<option value="${g.rank}">${g.rank}</option>`).join("")}</select></label>` +
      `<label>${lang === "es" ? "Tema" : "Theme"} <select id="f-theme"><option value="">All</option>${themes.map((t) => `<option value="${t}">${esc(themeLabel(t))}</option>`).join("")}</select></label>` +
      `<label>${lang === "es" ? "Buscar" : "Search"} <input type="search" id="f-q" placeholder="${lang === "es" ? "Nombre" : "Name"}"></label>`;
    function draw() {
      const fg = document.getElementById("f-gap")?.value || "";
      const ft = document.getElementById("f-theme")?.value || "";
      const q = (document.getElementById("f-q")?.value || "").toLowerCase();
      const filtered = rows.filter((r) => {
        if (fg && String(r.gap) !== fg) return false;
        if (ft && r.theme !== ft) return false;
        if (q && !r.name.toLowerCase().includes(q)) return false;
        return true;
      });
      thead.innerHTML =
        lang === "es"
          ? "<tr><th>Startup</th><th>Brecha</th><th>Tema</th><th>Etapa</th><th>Web</th></tr>"
          : "<tr><th>Startup</th><th>Gap</th><th>Theme</th><th>Stage</th><th>Web</th></tr>";
      tbody.innerHTML = filtered
        .map(
          (r) =>
            `<tr><td>${esc(r.name)}</td><td>${r.gap}</td><td>${r.theme ? esc(themeLabel(r.theme)) : DASH}</td><td>${r.stage ? esc(r.stage) : DASH}</td><td>${r.website ? `<a href="${esc(r.website)}" target="_blank" rel="noopener">${esc(r.website)}</a>` : DASH}</td></tr>`
        )
        .join("");
    }
    filters.querySelectorAll("select,input").forEach((el) => el.addEventListener("input", draw));
    draw();
  }

  function renderCoverage() {
    const sites = DATA.interactive?.coverage_sites || [];
    const slider = document.getElementById("coverage-slider");
    const out = document.getElementById("coverage-output");
    const label = document.getElementById("coverage-label");
    if (!slider || !out || !sites.length) return;
    slider.max = String(sites.length - 1);
    const hint = document.getElementById("coverage-hint");
    if (hint) {
      hint.textContent =
        lang === "es"
          ? "Desliza para simular sitios a instrumentar; muestra brechas e indicadores GRI cubiertos (sin cifras inventadas)."
          : "Drag to simulate sites you would instrument; shows covered gaps and GRI indicators (no invented figures).";
    }
    function update() {
      const idx = +slider.value;
      const site = sites[idx];
      const siteLabel = site.label[lang] || site.label.en;
      if (label) label.textContent = siteLabel;
      const covered = site.gaps.map((n) => `Gap ${n}`).join(", ");
      const gri = (site.gri || []).join(", ");
      out.innerHTML = `<p class="one-line"><strong>${esc(siteLabel)}</strong></p><p class="one-line">${lang === "es" ? "Brechas" : "Gaps"}: ${esc(covered)}</p><p class="one-line">GRI: ${esc(gri)}</p>`;
    }
    slider.addEventListener("input", update);
    update();
  }

  function renderHistory() {
    const hist = DATA.cth_history || {};
    const metricsEl = document.getElementById("history-metrics");
    const tlEl = document.getElementById("history-timeline");
    if (metricsEl) {
      metricsEl.innerHTML = (hist.metrics || [])
        .map(
          (m) =>
            `<div class="metric-tile"><div class="num">${esc(m.value)}</div><div>${esc(m.label[lang] || m.label.en)}</div><div class="src"><a href="${esc(m.source_url)}" target="_blank" rel="noopener">${esc(m.source_label)}</a></div></div>`
        )
        .join("");
    }
    if (tlEl) {
      tlEl.innerHTML = (hist.timeline || [])
        .map(
          (item) =>
            `<div class="tl-item">${item.year ? `<strong>${esc(item.year)}</strong> — ` : ""}${esc(item.text[lang] || item.text.en)} <a href="${esc(item.source_url)}" target="_blank" rel="noopener">(${esc(item.source_label)})</a></div>`
        )
        .join("");
    }
  }

  function renderTeam() {
    const root = document.getElementById("team-grid");
    if (!root) return;
    root.innerHTML = (DATA.team || [])
      .map((person) => {
        const bio = person.bio[lang] || person.bio.en;
        return `<article class="nx-card"><img src="${esc(person.photo)}" alt="${esc(person.name)}" style="width:100%;border-radius:10px;object-fit:cover;max-height:320px"><p class="eyebrow">${esc(person.role[lang] || person.role.en)}</p><h3>${esc(person.name)}</h3><p class="one-line">${esc(bio)}</p></article>`;
      })
      .join("");
  }

  function setGapTab(i) {
    activeGap = i;
    document.querySelectorAll(".gap-panel").forEach((p, j) => p.classList.toggle("on", j === i));
    document.querySelectorAll(".tab-btn").forEach((b, j) => b.classList.toggle("on", j === i));
  }

  function apply() {
    document.documentElement.lang = lang;
    if (DATA.meta?.title) document.title = DATA.meta.title[lang] || DATA.meta.title.en;
    const slug = DATA.meta?.slug || "celsia-snapshot";
    let canonical = document.querySelector('link[rel="canonical"]');
    if (!canonical) {
      canonical = document.createElement("link");
      canonical.rel = "canonical";
      document.head.appendChild(canonical);
    }
    canonical.href = `${PUBLIC_ORIGIN}/${slug}/`;

    document.getElementById("brand-logo").src = DATA.brand?.logo || "img/cth-logo.png";
    document.getElementById("hero-eyebrow").textContent = t("hero.eyebrow");
    document.getElementById("hero-title").textContent = t("hero.title");
    document.getElementById("hero-meta").innerHTML = [
      ["hero.companyLbl", "hero.company", false],
      ["hero.scopeLbl", "hero.scope", false],
      ["hero.reportLbl", "hero.report", true],
    ]
      .map(([l, v, html]) => {
        const val = t(v);
        const inner = html ? val : esc(val);
        return `<div><span class="lbl">${esc(t(l))}</span><span>${inner}</span></div>`;
      })
      .join("");

    document.getElementById("history-eyebrow").textContent = "CleantechHUB";
    document.getElementById("history-title").textContent = t("history.title");
    document.getElementById("history-lead").textContent = t("history.lead");
    document.getElementById("datalab-eyebrow").textContent = t("datalab.eyebrow");
    document.getElementById("datalab-title").textContent = t("datalab.title");
    document.getElementById("datalab-intro").textContent = t("datalab.intro");
    document.getElementById("gaps-title").textContent = t("nav.gaps");
    document.getElementById("compare-title").textContent = t("compare.title");
    document.getElementById("coverage-title").textContent = t("coverage.title");
    document.getElementById("team-eyebrow").textContent = t("team.eyebrow");
    document.getElementById("team-title").textContent = t("team.title");
    document.getElementById("team-intro").textContent = t("team.intro");
    document.getElementById("cta-sandbox").textContent = t("datalab.ctaSandbox");
    const cta = document.getElementById("cta-btn");
    if (cta) {
      cta.textContent = t("cta.btn");
      cta.href = DATA.cta?.url || "#";
    }

    const nav = document.getElementById("main-nav");
    if (nav) {
      nav.innerHTML = [
        ["#history", "nav.history"],
        ["#datalab", "nav.datalab"],
        ["#gaps", "nav.gaps"],
        ["#compare", "nav.compare"],
        ["#coverage", "nav.coverage"],
        ["#team", "nav.team"],
        ["#cta", "nav.cta"],
      ]
        .map(([href, key]) => `<a href="${href}">${esc(t(key))}</a>`)
        .join("");
    }

    const tabs = document.getElementById("gap-tabs");
    const panels = document.getElementById("gap-panels");
    if (tabs && panels) {
      tabs.innerHTML = DATA.gaps
        .map((g, i) => `<button type="button" class="tab-btn${i === activeGap ? " on" : ""}" data-gap="${i}">${esc(DATA.ui[lang][`nav.g${g.rank}`] || `Gap ${g.rank}`)}</button>`)
        .join("");
      panels.innerHTML = DATA.gaps.map((g, i) => renderGapPanel(g, i)).join("");
      tabs.querySelectorAll(".tab-btn").forEach((btn) => {
        btn.addEventListener("click", () => setGapTab(+btn.dataset.gap));
      });
    }

    document.querySelectorAll(".lang button").forEach((b) => b.classList.toggle("on", b.dataset.lang === lang));
    renderHistory();
    renderCompare();
    renderCoverage();
    renderTeam();
    bindFlowClicks();
  }

  document.querySelectorAll(".lang button").forEach((btn) => {
    btn.addEventListener("click", () => {
      lang = btn.dataset.lang;
      localStorage.setItem("cth-snapshot-lang", lang);
      apply();
    });
  });

  fetch("./data.json")
    .then((r) => r.json())
    .then((json) => {
      DATA = json;
      apply();
    })
    .catch(() => {
      document.body.insertAdjacentHTML("beforeend", "<p style='padding:2rem'>Could not load data.json.</p>");
    });
})();
