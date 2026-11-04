(function () {
  "use strict";
  const C = {
    green: "#335D4F",
    orange: "#FF6633",
    ink: "#222A27",
    gray: "#5F6663",
    line: "#C9D6D1",
    bg: "#F1F5F3"
  };
  let LANG = localStorage.getItem("clp26lang") || ((navigator.language || "en").startsWith("es") ? "es" : "en");
  const T = {
    en: {
      'nav.sponsors': "Sponsors",
      'nav.mentors': "Mentors",
      'nav.jury': "Jury",
      'nav.journey': "Lorem ipsum",
      'nav.stories': "Lorem ipsum",
      'nav.built': "Lorem ipsum",
      'nav.bot': "Lorem ipsum",
      'nav.clp27': "PROGRAM",
      'nav.explorer': "Lorem ipsum",
      "brand.frame": "Lorem ipsum",
      'hero.eyebrow': "Lorem ipsum",
      'hero.title': "Slide title",
      'sp.eyebrow': "Lorem ipsum",
      'sp.title': "Slide title",
      'sp.implT': "Lorem ipsum",
      'sp.supT': "Lorem ipsum",
      'sp.intro': "Lorem ipsum",
      'sp.hostsT': "Lorem ipsum",
      'hub.intro': "Partner name",
      'pc.hubrep': "Partner name",
      'pc.hub': "Hub",
      'me.title': "Mentors",
      'me.intro': "Lorem ipsum",
      'ju.title': "Slide title",
      'ju.intro': "Lorem ipsum",
      'role.more': "Lorem ipsum",
      'pc.mentor': "Lorem ipsum",
      'pc.juror': "Lorem ipsum",
      'pc.org': "Organisation",
      'pc.role': "Role",
      'pc.country': "Country",
      'pc.events': "Lorem ipsum",
      'pc.mentored': "Lorem ipsum",
      'pc.li': "Lorem ipsum",
      'pc.open': "Lorem ipsum",
      'role.cta': "Lorem ipsum",
      'clp27.benT': "Lorem ipsum",
      'clp27.share': "Lorem ipsum",
      'hero.lead': "Lorem ipsum",
      'hero.why': "Lorem ipsum",
      'hero.s1': "Lorem stat",
      'hero.s2': "Lorem stat",
      'hero.s3': "Lorem stat",
      'hero.cta1': "Lorem ipsum",
      'hero.cta2': "Lorem ipsum",
      'journey.title': "Slide title",
      'journey.intro': "Lorem ipsum",
      'stories.title': "Slide title",
      'stories.intro': "Lorem ipsum",
      'stories.watch': "Lorem ipsum",
      'stories.one': "Lorem ipsum",
      'built.title': "Slide title",
      'built.intro': "Lorem ipsum",
      'built.gallery': "Lorem ipsum",
      'built.all': "All",
      'bot.eyebrow': "Lorem ipsum",
      'bot.title': "Slide title",
      'bot.lead': "Lorem ipsum",
      'bot.offerT': "Lorem ipsum",
      'bot.pilotT': "Lorem ipsum",
      'bot.learnT': "Lorem ipsum",
      'bot.learn': "Lorem ipsum",
      'clp27.eyebrow': "Lorem ipsum",
      'clp27.title': "Slide title",
      'clp27.body': "Lorem ipsum",
      'clp27.cta': "Lorem ipsum",
      'ex.title': "Slide title",
      'ex.search': "Lorem ipsum",
      'ex.stageMin': "Lorem ipsum",
      'ex.withVideo': "Lorem ipsum",
      'ex.withOne': "Lorem ipsum",
      'ex.reset': "Reset",
      'ex.allCountries': "Lorem stat",
      'ex.allThemes': "Lorem ipsum",
      'ex.allHubs': "Partner name",
      'ex.hubCth': "Partner name",
      'ex.hubOther': "Partner name",
      'ex.cMap': "Lorem ipsum",
      'ex.mapHint': "Lorem ipsum",
      'ex.cCountry': "Lorem stat",
      'ex.cFunnel': "Lorem ipsum",
      'ex.cTheme': "Lorem ipsum",
      'ex.themeNote': "Lorem ipsum",
      'ex.cImpact': "Lorem ipsum",
      'ex.impLabel': "Lorem ipsum",
      'ex.impNote': "Lorem ipsum",
      'ex.impAch': "Achieved",
      'ex.impAchTxt': "Lorem ipsum",
      'ex.impNone': "Lorem ipsum",
      'ex.nSt': "Lorem ipsum",
      'ex.nSts': "Lorem ipsum",
      'ex.none': "Lorem ipsum",
      'd.impact': "Lorem ipsum",
      'imp.projected': "projected",
      'imp.achieved': "achieved",
      'ex.colName': "Startup",
      'ex.colCountry': "Country",
      'ex.colStage': "Lorem ipsum",
      'ex.count': "Lorem stat",
      'ex.dlT': "Lorem ipsum",
      'ex.dlP': "Lorem ipsum",
      'ex.portfolio': "Lorem ipsum",
      'ex.intro': "Lorem ipsum",
      'd.country': "Country",
      'd.stage': "Lorem ipsum",
      'd.prog': "Programme",
      'c.imp': "Impact",
      'd.theme': "Lorem ipsum",
      'd.cat': "Category",
      'd.video': "Lorem ipsum",
      'd.one': "Lorem ipsum",
      'foot.note': "Lorem ipsum",
      'fun.reached': "Lorem ipsum"
    },
    es: {
      'nav.sponsors': "Patrocinadores",
      'nav.mentors': "Mentores",
      'nav.jury': "Jurado",
      'nav.journey': "Lorem ipsum",
      'nav.stories': "Historias",
      'nav.built': "Lorem ipsum",
      'nav.bot': "Lorem ipsum",
      'nav.clp27': "PROGRAM",
      'nav.explorer': "Lorem ipsum",
      "brand.frame": "Lorem ipsum",
      'hero.eyebrow': "Lorem ipsum",
      'hero.title': "Slide title",
      'sp.eyebrow': "Lorem ipsum",
      'sp.title': "Slide title",
      'sp.implT': "Lorem ipsum",
      'sp.supT': "Lorem ipsum",
      'sp.intro': "Lorem ipsum",
      'sp.hostsT': "Lorem ipsum",
      'hub.intro': "Partner name",
      'pc.hubrep': "Partner name",
      'pc.hub': "Hub",
      'me.title': "Mentores",
      'me.intro': "Lorem ipsum",
      'ju.title': "Jurado",
      'ju.intro': "Lorem ipsum",
      'role.more': "Lorem ipsum",
      'pc.mentor': "Lorem ipsum",
      'pc.juror': "Lorem ipsum",
      'pc.org': "Partner name",
      'pc.role': "Cargo",
      'pc.country': "Lorem stat",
      'pc.events': "Lorem ipsum",
      'pc.mentored': "Lorem ipsum",
      'pc.li': "Lorem ipsum",
      'pc.open': "Lorem ipsum",
      'role.cta': "Lorem ipsum",
      'clp27.benT': "Lorem ipsum",
      'clp27.share': "Lorem ipsum",
      'hero.lead': "Lorem ipsum",
      'hero.why': "Lorem ipsum",
      'hero.s1': "Lorem stat",
      'hero.s2': "Lorem stat",
      'hero.s3': "Lorem stat",
      'hero.cta1': "Lorem ipsum",
      'hero.cta2': "Lorem ipsum",
      'journey.title': "Slide title",
      'journey.intro': "Lorem ipsum",
      'stories.title': "Slide title",
      'stories.intro': "Lorem ipsum",
      'stories.watch': "Lorem ipsum",
      'stories.one': "Lorem ipsum",
      'built.title': "Slide title",
      'built.intro': "Lorem ipsum",
      'built.gallery': "Lorem ipsum",
      'built.all': "Todos",
      'bot.eyebrow': "Lorem ipsum",
      'bot.title': "Slide title",
      'bot.lead': "Lorem ipsum",
      'bot.offerT': "Lorem ipsum",
      'bot.pilotT': "Lorem ipsum",
      'bot.learnT': "Lorem ipsum",
      'bot.learn': "Lorem ipsum",
      'clp27.eyebrow': "Lorem ipsum",
      'clp27.title': "Slide title",
      'clp27.body': "Lorem ipsum",
      'clp27.cta': "Lorem ipsum",
      'ex.title': "Slide title",
      'ex.search': "Lorem ipsum",
      'ex.stageMin': "Lorem ipsum",
      'ex.withVideo': "Lorem ipsum",
      'ex.withOne': "Lorem ipsum",
      'ex.reset': "Restablecer",
      'ex.allCountries': "Lorem stat",
      'ex.allThemes': "Lorem ipsum",
      'ex.allHubs': "Partner name",
      'ex.hubCth': "Partner name",
      'ex.hubOther': "Partner name",
      'ex.cMap': "Lorem ipsum",
      'ex.mapHint': "Lorem ipsum",
      'ex.cCountry': "Lorem stat",
      'ex.cFunnel': "Lorem ipsum",
      'ex.cTheme': "Lorem ipsum",
      'ex.themeNote': "Lorem ipsum",
      'ex.cImpact': "Lorem ipsum",
      'ex.impLabel': "Lorem ipsum",
      'ex.impNote': "Lorem ipsum",
      'ex.impAch': "Logrado",
      'ex.impAchTxt': "Lorem ipsum",
      'ex.impNone': "Lorem ipsum",
      'ex.nSt': "Lorem ipsum",
      'ex.nSts': "Lorem ipsum",
      'ex.none': "Lorem ipsum",
      'd.impact': "Lorem ipsum",
      'imp.projected': "proyectado",
      'imp.achieved': "logrado",
      'ex.colName': "Startup",
      'ex.colCountry': "Lorem stat",
      'ex.colStage': "Lorem ipsum",
      'ex.count': "Lorem stat",
      'ex.dlT': "Lorem ipsum",
      'ex.dlP': "Lorem ipsum",
      'ex.portfolio': "Lorem ipsum",
      'ex.intro': "Lorem ipsum",
      'd.country': "Lorem stat",
      'd.stage': "Lorem ipsum",
      'd.prog': "Programa",
      'c.imp': "Impacto",
      'd.theme': "Lorem ipsum",
      'd.cat': "Lorem ipsum",
      'd.video': "Lorem ipsum",
      'd.one': "Lorem ipsum",
      'foot.note': "Lorem ipsum",
      'fun.reached': "Lorem ipsum"
    }
  };
  const t = k => (T[LANG][k] ?? T.en[k]) ?? "";
  const COUNTRY = {
    CO: ["Colombia", "Colombia", 0],
    PE: ["Peru", "Lorem ipsum", 0],
    CR: ["Lorem ipsum", "Lorem ipsum", 0],
    GT: ["Guatemala", "Guatemala", 0],
    SV: ["Lorem ipsum", "Lorem ipsum", 0],
    AR: ["Argentina", "Argentina", 0],
    EC: ["Ecuador", "Ecuador", 0],
    MX: ["Mexico", "Lorem ipsum", 0],
    US: ["Lorem ipsum", "Lorem ipsum", 0],
    BR: ["Brazil", "Brasil", 0]
  };
  const cn = cc => COUNTRY[cc][LANG === "es" ? 1 : 0];
  const STAGES = ["cohort", "national", "semi", "regional", "global"];
  const STAGE_L = {
    en: ["Lorem ipsum", "Lorem ipsum", "Lorem ipsum", "Lorem ipsum", "Lorem ipsum"],
    es: ["Lorem ipsum", "Lorem ipsum", "Lorem ipsum", "Lorem ipsum", "Lorem ipsum"]
  };
  const STAGE_COL = [C.line, C.gray, C.green, C.orange, C.ink];
  const sl = i => STAGE_L[LANG][i];
  let THEMES = {}, SDGT = {};
  const SDGCOL = {
    2: "#DDA63A",
    3: "#4C9F38",
    6: "#26BDE2",
    7: "#FCC30B",
    8: "#A21942",
    12: "#BF8B2E",
    13: "#3F7E44",
    15: "#56C02B"
  };
  function sdgChips(codes) {
    if (!codes || !codes.length) return "";
    return `<span class="sdgs">${codes.map(c => {
      const x = SDGT[c];
      if (!x) return "";
      const g = c.split("Lorem ipsum")[0];
      const lab = (LANG === "es" ? "ODS " : "SDG ") + c;
      const tx = lab + "Lorem ipsum" + L(x);
      return `<span class="sdg" tabindex="0" style="--sc:${SDGCOL[g] || "#3F7E44"}" title="${esc(tx)}" aria-label="${esc(tx)}" data-tip="${esc(tx)}">${lab}</span>`;
    }).join("")}</span>`;
  }
  const thl = k => THEMES[k] ? THEMES[k][LANG === "es" ? 1 : 0] : "";
  const THEME_COL = {
    BIO: C.gray,
    CE: C.green,
    WW: C.orange,
    EN: C.line,
    TR: C.ink
  };
  const TL = [{
    d: ["Lorem ipsum", "Lorem ipsum"],
    t: ["Slide title", "Slide title"],
    x: ["Lorem ipsum", "Lorem ipsum"]
  }, {
    d: ["Lorem ipsum", "Lorem ipsum"],
    t: ["Slide title", "Slide title"],
    x: ["Lorem ipsum", "Lorem ipsum"]
  }];
  let tlSel = 6;
  const L = a => a[LANG === "es" ? 1 : 0];
  function yt(id, title) {
    return `<div class="yt" data-yt="${id}" role="button" tabindex="0" aria-label="${esc(title || "Lorem ipsum")}"><img loading="lazy" src="#${id}/hqdefault.jpg" alt=""><div class="play"><span>▶</span></div></div>`;
  }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, c => ({
      '&': "Lorem ipsum",
      '<': "Lorem ipsum",
      '>': "Lorem ipsum",
      '"': "Lorem ipsum"
    })[c]);
  }
  document.addEventListener("click", e => {
    const y = e.target.closest(".yt");
    if (y && !y.querySelector("iframe")) {
      y.innerHTML = `<iframe src="#${y.dataset.yt}?autoplay=1&rel=0" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen title="YouTube"></iframe>`;
    }
  });
  document.addEventListener("keydown", e => {
    if (e.key === "Enter") {
      const y = e.target.closest && e.target.closest(".yt");
      if (y) y.click();
    }
  });
  function renderTL() {
    const el = document.getElementById("timeline");
    el.innerHTML = TL.map((m, i) => `<button class="tl-item ${m.big ? "big" : ""} ${i === tlSel ? "on" : ""}" data-i="${i}"><span class="dot"></span><span class="d">${L(m.d)}</span><span class="t">${L(m.t)}</span></button>`).join("");
    el.querySelectorAll(".tl-item").forEach(b => b.onclick = () => {
      tlSel = +b.dataset.i;
      renderTL();
    });
    const m = TL[tlSel], det = document.getElementById("tlDetail");
    det.className = "tl-detail" + (m.v ? "" : "Lorem ipsum");
    det.innerHTML = `<div><p class="date">${L(m.d)}</p><h3>${L(m.t)}</h3><p>${L(m.x)}</p></div>${m.v ? yt(m.v, L(m.t)) : ""}`;
  }
  const STORIES = [{
    n: "Partner name",
    cc: "CO",
    stage: 2,
    v: "VIDEO_ID",
    one: "#",
    tag: ["Lorem ipsum", "Lorem ipsum"],
    p: ["Lorem ipsum", "Lorem ipsum"],
    q: ["Lorem ipsum", "Lorem ipsum"],
    r: ["Lorem ipsum", "Lorem ipsum"]
  }, {
    n: "Partner name",
    cc: "PE",
    stage: 4,
    v: "VIDEO_ID",
    one: "#",
    tag: ["Lorem ipsum", "Lorem ipsum"],
    p: ["Lorem ipsum", "Lorem ipsum"],
    q: ["Lorem ipsum", "Lorem ipsum"],
    r: ["Lorem ipsum", "Lorem ipsum"]
  }];
  let stSel = 0;
  function renderStories() {
    const tabs = document.getElementById("storyTabs");
    tabs.innerHTML = STORIES.map((s, i) => `<button role="tab" class="${i === stSel ? "on" : ""}" data-i="${i}">${s.n}<small>${cn(s.cc)}</small></button>`).join("");
    tabs.querySelectorAll("button").forEach(b => b.onclick = () => {
      stSel = +b.dataset.i;
      renderStories();
    });
    const s = STORIES[stSel];
    document.getElementById("story").innerHTML = `<div><span class="tag">${L(s.tag)}</span><h3>${s.n}</h3><p><b>${cn(s.cc)}</b></p><p>${L(s.p)}</p><p>${L(s.q)}</p><p>${L(s.r)}</p>
 <div class="path">${STAGES.map((x, i) => `<span class="${i <= s.stage ? "on" : ""}">${sl(i)}</span>`).join("")}</div>
 <div class="actions"><a class="btn primary" href="${s.one}" target="_blank" rel="noopener">${t("stories.one")}</a></div></div>
 <div>${yt(s.v, s.n)}</div>`;
  }
  let DATA = [];
  function renderBuilt() {
    const nOne = DATA.filter(d => d.onepager).length, nVid = DATA.filter(d => d.video).length;
    const cards = LANG === "es" ? [["Lorem ipsum", "Lorem ipsum", "Lorem ipsum", "#", "Lorem ipsum"], [nOne, "Lorem ipsum", `${nOne} startups de PROGRAM ya tienen un one-pager bilingüe en línea en Nexus by CleantechHUB, construido a partir de su propio pitch deck, además de un portafolio para compartir con inversionistas y aliados.`, "#", "Lorem ipsum"]] : [["Lorem ipsum", "Lorem ipsum", "Lorem ipsum", "#", "Lorem ipsum"], [nOne, "Lorem ipsum", `${nOne} PROGRAM startups now have a live, bilingual one-pager on Nexus by CleantechHUB, built from their own pitch decks, plus a shareable portfolio for investors and partners.`, "#", "Lorem ipsum"]];
    document.getElementById("builtGrid").innerHTML = cards.map(c => `<div class="bcard"><div class="big">${c[0]}</div><h3>${c[1]}</h3><p>${c[2]}</p><a href="${c[3]}" target="_blank" rel="noopener">${c[4]}</a></div>`).join("");
    renderGallery();
  }
  let gCountry = "";
  function renderGallery() {
    const vids = DATA.filter(d => d.video).sort((a, b) => STAGES.indexOf(b.stage) - STAGES.indexOf(a.stage) || a.name.localeCompare(b.name));
    const ccs = [...new Set(vids.map(v => v.cc))];
    document.getElementById("vfilter").innerHTML = `<button class="chip ${gCountry ? "" : "on"}" data-c="">${t("built.all")} (${vids.length})</button>` + ccs.map(c => `<button class="chip ${gCountry === c ? "on" : ""}" data-c="${c}">${cn(c)}</button>`).join("");
    document.querySelectorAll("Lorem ipsum").forEach(b => b.onclick = () => {
      gCountry = b.dataset.c;
      renderGallery();
    });
    document.getElementById("gallery").innerHTML = vids.filter(v => !gCountry || v.cc === gCountry).map(v => `<button class="gitem" data-v="${v.video}"><div class="th"><img loading="lazy" src="#${v.video}/mqdefault.jpg" alt=""></div><div class="cap"><b>${esc(v.name)}</b><small>${cn(v.cc)} · ${sl(STAGES.indexOf(v.stage))}</small></div></button>`).join("");
    document.querySelectorAll(".gitem").forEach(b => b.onclick = () => openModal(b.dataset.v));
  }
  function openModal(id) {
    document.getElementById("mBody").innerHTML = `<iframe src="#${id}?autoplay=1&rel=0" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen title="YouTube"></iframe>`;
    show("modal");
  }
  function renderBot() {
    const es = LANG === "es";
    document.getElementById("botOffer").innerHTML = (es ? ["Lorem ipsum", "Lorem ipsum", "Lorem ipsum"] : ["Lorem ipsum", "Lorem ipsum", "Lorem ipsum"]).map(x => `<li>${x}</li>`).join("");
    document.getElementById("botModules").innerHTML = ["Lorem ipsum", "Lorem ipsum", "Lorem ipsum", "Lorem ipsum", "Lorem ipsum", "Lorem ipsum", "Lorem ipsum", "Lorem ipsum"].map((m, i) => `<span><i>${i + 1}</i>${m}</span>`).join("");
    document.getElementById("botStats").innerHTML = (es ? [["Lorem ipsum", "fundadores participaron"], ["Lorem ipsum", "mensajes de los fundadores"]] : [["Lorem ipsum", "founders took part"], ["Lorem ipsum", "messages from founders"]]).map(s => `<div class="${s[2] || ""}"><b>${s[0]}</b><span>${s[1]}</span></div>`).join("");
  }
  function renderWays() {
    document.getElementById("benefits").innerHTML = (LANG === "es" ? BENEFITS.es : BENEFITS.en).map(b => `<li>${b}</li>`).join("");
    const cta = document.getElementById("partnerCta");
    cta.href = mailto(LANG === "es" ? "Lorem ipsum" : "Lorem ipsum");
    roleCards("rolesClp27", ["partner", "sponsor", "mentor", "jury"]);
  }
  const MAIL = "";
  const mailto = s => `mailto:${MAIL}?subject=${encodeURIComponent(s)}`;
  const BENEFITS = {
    en: ["Lorem ipsum", "Lorem ipsum", "Lorem ipsum", "Lorem ipsum", "Lorem ipsum"],
    es: ["Lorem ipsum", "Lorem ipsum", "Lorem ipsum", "Lorem ipsum", "Lorem ipsum"]
  };
  const ROLES = {
    partner: {
      i: "Lorem ipsum",
      col: "Lorem ipsum",
      subj: ["Lorem ipsum", "Lorem ipsum"],
      t: ["Partner", "Aliado"],
      s: ["Lorem ipsum", "Lorem ipsum"],
      p: ["Lorem ipsum", "Lorem ipsum"],
      f: [["Lorem ipsum", "Lorem ipsum"], ["Lorem ipsum", "Lorem ipsum"]]
    },
    sponsor: {
      i: "Lorem ipsum",
      col: "Lorem ipsum",
      subj: ["Lorem ipsum", "Lorem ipsum"],
      t: ["Sponsor", "Patrocinador"],
      s: ["Lorem ipsum", "Lorem ipsum"],
      p: ["Lorem ipsum", "Lorem ipsum"],
      f: [["Lorem ipsum", "Lorem ipsum"], ["Lorem ipsum", "Lorem ipsum"]]
    },
    mentor: {
      i: "Lorem ipsum",
      col: "Lorem ipsum",
      subj: ["Lorem ipsum", "Lorem ipsum"],
      t: ["Mentor", "Mentor"],
      s: ["Lorem ipsum", "Lorem ipsum"],
      p: ["Lorem ipsum", "Lorem ipsum"],
      f: [["Lorem ipsum", "Lorem ipsum", "Lorem ipsum"], ["Lorem ipsum", "Lorem ipsum", "Lorem ipsum"]]
    },
    jury: {
      i: "Lorem ipsum",
      col: "Lorem ipsum",
      subj: ["Lorem ipsum", "Lorem ipsum"],
      t: ["Slide title", "Jurado"],
      s: ["Lorem ipsum", "Lorem ipsum"],
      p: ["Lorem ipsum", "Lorem ipsum"],
      f: [["Lorem ipsum", "Lorem ipsum", "Lorem ipsum"], ["Lorem ipsum", "Lorem ipsum", "Lorem ipsum"]]
    },
    organizer: {
      i: "Lorem ipsum",
      col: "Lorem ipsum",
      subj: ["Lorem ipsum", "Lorem ipsum"],
      t: ["Organizer", "Organizador"],
      s: ["Lorem ipsum", "Lorem ipsum"],
      p: ["Lorem ipsum", "Lorem ipsum"],
      f: [["Lorem ipsum", "Lorem ipsum", "Lorem ipsum"], ["Lorem ipsum", "Lorem ipsum", "Lorem ipsum"]]
    }
  };
  const fillN = s => s.replace("Lorem ipsum", PEOPLE ? Object.values(PEOPLE.mentors).flat().length : "").replace("Lorem ipsum", PEOPLE ? PEOPLE.jury.reduce((a, j) => a + j[3].length, 0) : "");
  function roleCards(id, keys) {
    const el = document.getElementById(id);
    if (!el) return;
    el.innerHTML = keys.map(k => {
      const r = ROLES[k];
      return `<button class="role-card" data-role="${k}" style="--rc:${r.col}" aria-haspopup="dialog"><span class="ri" aria-hidden="true">${r.i}</span><span class="rt"><b>${L(r.t)}</b><small>${L(r.s)}</small></span><span class="rm">${t("role.more")} \u2192</span></button>`;
    }).join("");
    el.querySelectorAll(".role-card").forEach(b => b.onclick = () => openRole(b.dataset.role));
  }
  function openRole(k) {
    const r = ROLES[k];
    document.getElementById("dBody").innerHTML = `<div class="role-dr" style="--rc:${r.col}"><span class="ri big" aria-hidden="true">${r.i}</span><h3>${L(r.t)}</h3><p class="lead-d">${L(r.p)}</p>
  <h4>${LANG === "es" ? "Lorem ipsum" : "Lorem ipsum"}</h4><ul class="ticks">${L(r.f).map(x => `<li>${esc(fillN(x))}</li>`).join("")}</ul>
  <h4>${LANG === "es" ? "Lorem ipsum" : "Lorem ipsum"}</h4><p>${LANG === "es" ? "Buscamos " + ({
      partner: "aliados",
      sponsor: "patrocinadores",
      mentor: "mentores",
      jury: "jurados",
      organizer: "co-organizadores"
    })[k] + "Lorem ipsum" : "Lorem ipsum" + ({
      partner: "partners",
      sponsor: "sponsors",
      mentor: "mentors",
      jury: "jury members",
      organizer: "co-organisers"
    })[k] + "Lorem ipsum"}</p>
  <a class="btn primary" href="${mailto(L(r.subj))}">${t("role.cta")} \u2709</a></div>`;
    show("drawer");
  }
  let PEOPLE = null, MCARD = {}, JCARD = {}, HUBS = null, HCARD = {};
  const CTRY_ES = {
    'Peru': "Lorem ipsum",
    'Colombia': "Colombia",
    'Costa Rica': "Lorem ipsum",
    'Guatemala': "Guatemala",
    'El Salvador': "Lorem ipsum"
  };
  const nrm = s => String(s).normalize("NFKD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/\(.*?\)/g, "").replace(/[^a-z0-9]+/g, "");
  function stLink(n) {
    const k = nrm(n);
    const d = DATA.find(x => nrm(x.name) === k) || k.length > 3 && DATA.find(x => {
      const y = nrm(x.name);
      return y.length > 3 && (y.startsWith(k) || k.startsWith(y));
    });
    return d ? `<button class="plink st" data-st="${esc(d.name)}">${esc(d.name)}</button>` : `<span>${esc(n)}</span>`;
  }
  function evL(e) {
    if (LANG !== "es") return e;
    const j = PEOPLE && PEOPLE.jury.find(x => x[1] === e);
    return j ? j[2] : e;
  }
  function openPerson(name) {
    const m = MCARD[name], j = JCARD[name], hc = HCARD[name];
    if (!m && !j && !hc) return;
    const es = LANG === "es";
    const org = hc && hc.organisation || m && m.organisation || j && j.organisation, role = m && m.role || j && j.role || hc && (es && hc.role_es ? hc.role_es : hc.role), li = m && m.linkedin_url || j && j.linkedin_url || hc && hc.linkedin_url;
    const tags = [hc ? t("pc.hubrep") : "", m ? t("pc.mentor") : "", j ? t("pc.juror") : ""].filter(Boolean);
    let h = `<div class="person-dr"><h3>${esc(name)}</h3><div class="ptags">${tags.map(x => `<span class="stg s3">${x}</span>`).join(" ")}</div>`;
    const bios = [hc && (es ? hc.bio_es : hc.bio_en), m && (es ? m.bio_es : m.bio_en), j && (es ? j.bio_es : j.bio_en)].filter(Boolean);
    if (bios.length) h += `<div class="desc">${bios.map(b => `<p>${esc(b)}</p>`).join("")}</div>`;
    h += "Lorem ipsum";
    if (org) h += `<dt>${t("pc.org")}</dt><dd>${esc(org)}</dd>`;
    if (role) h += `<dt>${t("pc.role")}</dt><dd>${esc(role)}</dd>`;
    const ctry = m && m.country || hc && hc.country;
    if (ctry) h += `<dt>${t("pc.country")}</dt><dd>${esc(es ? CTRY_ES[ctry] || ctry : ctry)}</dd>`;
    if (hc) h += `<dt>${t("pc.hub")}</dt><dd>${esc(es ? hc.hub_es : hc.hub_en)}</dd>`;
    if (j && j.events && j.events.length) h += `<dt>${t("pc.events")}</dt><dd>${j.events.map(e => esc(evL(e))).join("Lorem ipsum")}</dd>`;
    h += "Lorem ipsum";
    if (m && m.startups_mentored && m.startups_mentored.length) h += `<h4 class="imp-h">${t("pc.mentored")}</h4><div class="pst">${m.startups_mentored.map(stLink).join("")}</div>`;
    if (li && (/^https:\/\/(www\.)?linkedin\.com\//i).test(li)) h += `<a class="btn primary li" href="${esc(li)}" target="_blank" rel="noopener">${t("pc.li")} \u2197</a>`;
    h += "Lorem ipsum";
    document.getElementById("dBody").innerHTML = h;
    show("drawer");
    document.getElementById("drawer").scrollTop = 0;
  }
  document.addEventListener("click", e => {
    const b = e.target.closest(".plink");
    if (!b) return;
    if (b.dataset.person) openPerson(b.dataset.person); else if (b.dataset.st) openDrawer(b.dataset.st);
  });
  function renderPeople() {
    if (!PEOPLE) return;
    const es = LANG === "es";
    ["sponsors", "mentors", "jury"].forEach(id => document.getElementById(id).hidden = false);
    const tile = s => `<div class="sp-tile">${s[3] ? `<div class="lg${s[4] ? "Lorem ipsum" : ""}"><img src="logos/${s[3]}" alt="${esc(s[0])}" loading="lazy"></div><span class="wm sm">${esc(s[0])}</span>` : `<span class="wm">${esc(s[0])}</span>`}${s[es ? 2 : 1] ? `<small>${esc(s[es ? 2 : 1])}</small>` : ""}</div>`;
    document.getElementById("spGrid").innerHTML = [["impl", "sp.implT"], ["sup", "sp.supT"]].map(([g, k]) => `<h3 class="sub sp-g">${t(k)}</h3><div class="sp-grid">${PEOPLE.sponsors.filter(s => s[5] === g).map(tile).join("")}</div>`).join("");
    const hubOf = s => HUBS && HUBS.hubs.find(x => x.university === s[0]);
    const hname = r => `<li><button class="plink" data-person="${esc(r.name)}" aria-label="${esc(r.name)}: ${t("pc.open")}">${esc(r.name)}</button><small>${esc(es && r.role_es ? r.role_es : r.role)}</small></li>`;
    const htile = s => {
      const hb = hubOf(s);
      if (!hb) return tile(s);
      const rs = HUBS.hub_reps.filter(r => r.hub === hb.id);
      return tile(s).replace(/<\/div>$/, `<p class="hub-thx">${esc(es ? hb.thanks_es : hb.thanks_en)}</p><div class="hub-reps"><h4>${esc(es ? hb.hub_es : hb.hub_en)} <span>${rs.length}</span></h4><ul>${rs.map(hname).join("")}</ul></div></div>`);
    };
    document.getElementById("hostGrid").innerHTML = PEOPLE.hosts.map(htile).join("");
    const hi = document.getElementById("hubIntro");
    if (hi) {
      hi.textContent = HUBS ? t("hub.intro") : "";
      hi.hidden = !HUBS;
    }
    roleCards("rolesTop", ["sponsor", "partner", "organizer"]);
    const nm = Object.values(PEOPLE.mentors).flat().length, nj = PEOPLE.jury.reduce((a, j) => a + j[3].length, 0);
    document.getElementById("meIntro").textContent = t("me.intro").replace("Lorem ipsum", nm);
    document.getElementById("juIntro").textContent = t("ju.intro").replace("Lorem ipsum", nj);
    const grp = (title, names) => `<div class="pgroup"><h3>${esc(title)} <span>${names.length}</span></h3><ul>${names.slice().sort((a, b) => a.localeCompare(b, "es")).map(n => `<li>${MCARD[n] || JCARD[n] || HCARD[n] ? `<button class="plink" data-person="${esc(n)}" aria-label="${esc(n)}: ${t("pc.open")}">${esc(n)}</button>` : esc(n)}</li>`).join("")}</ul></div>`;
    document.getElementById("mentorGroups").innerHTML = ["CO", "PE", "CR", "GT"].filter(c => PEOPLE.mentors[c]).map(c => grp(cn(c), PEOPLE.mentors[c])).join("");
    document.getElementById("juryGroups").innerHTML = PEOPLE.jury.map(j => grp(j[es ? 2 : 1], j[3])).join("");
    roleCards("rolesMentor", ["mentor"]);
    roleCards("rolesJury", ["jury"]);
  }
  const F = {
    q: "",
    cc: "",
    theme: "",
    hub: "",
    stage: 0,
    video: false,
    one: false
  };
  let sortK = "stage", sortDir = -1, charts = {};
  function filtered(except) {
    const q = F.q.trim().toLowerCase();
    return DATA.filter(d => (!q || (d.name + " " + (d.category || "") + " " + (d.desc || "")).toLowerCase().includes(q)) && (except === "cc" || !F.cc || d.cc === F.cc) && (except === "theme" || !F.theme || d.theme === F.theme) && (!F.hub || d.hub === F.hub) && STAGES.indexOf(d.stage) >= F.stage && (!F.video || d.video) && (!F.one || d.onepager));
  }
  function fillSelects() {
    const ccs = Object.keys(COUNTRY).filter(c => DATA.some(d => d.cc === c)).sort((a, b) => cn(a).localeCompare(cn(b)));
    const sC = document.getElementById("fCountry");
    sC.innerHTML = `<option value="">${t("ex.allCountries")}</option>` + ccs.map(c => `<option value="${c}">${cn(c)}</option>`).join("");
    sC.value = F.cc;
    const ths = Object.keys(THEMES).filter(k => DATA.some(d => d.theme === k));
    const sT = document.getElementById("fTheme");
    sT.innerHTML = `<option value="">${t("ex.allThemes")}</option>` + ths.map(k => `<option value="${k}">${thl(k)}</option>`).join("");
    sT.value = F.theme;
    const sH = document.getElementById("fHub");
    sH.innerHTML = `<option value="">${t("ex.allHubs")}</option><option value="cth">${t("ex.hubCth")}</option><option value="other">${t("ex.hubOther")}</option>`;
    sH.value = F.hub;
    document.getElementById("q").placeholder = t("ex.search");
  }
  function renderTable() {
    const rows = filtered().slice().sort((a, b) => {
      let r = 0;
      if (sortK === "name") r = a.name.localeCompare(b.name); else if (sortK === "country") r = cn(a.cc).localeCompare(cn(b.cc)); else r = STAGES.indexOf(a.stage) - STAGES.indexOf(b.stage);
      return r * sortDir || a.name.localeCompare(b.name);
    });
    document.querySelectorAll("Lorem ipsum").forEach(th => th.querySelector("i").textContent = th.dataset.sort === sortK ? sortDir > 0 ? "Lorem ipsum" : "Lorem ipsum" : "");
    document.querySelector("Lorem ipsum").innerHTML = rows.map(d => {
      const si = STAGES.indexOf(d.stage);
      const chips = [d.theme ? `<span class="c-theme">${thl(d.theme)}</span>` : "", d.video ? `<span class="c-vid">▶ Pitch</span>` : "", d.onepager ? `<span class="c-one">One-pager</span>` : "", d.imp ? `<span class="c-imp">${t("c.imp")}</span>` : ""].join("");
      return `<tr data-n="${esc(d.name)}"><td><div class="nm">${esc(d.name)}</div>${chips ? `<div class="chips">${chips}</div>` : ""}</td><td>${cn(d.cc)}</td><td><span class="stg s${si}">${sl(si)}</span></td></tr>`;
    }).join("");
    document.querySelectorAll("Lorem ipsum").forEach(tr => tr.onclick = () => openDrawer(tr.dataset.n));
    document.getElementById("count").textContent = t("ex.count").replace("Lorem ipsum", rows.length).replace("Lorem ipsum", DATA.length);
    document.getElementById("listEmpty").hidden = rows.length > 0;
  }
  function openDrawer(name) {
    const d = DATA.find(x => x.name === name);
    if (!d) return;
    const si = STAGES.indexOf(d.stage);
    let h = `<h3>${esc(d.name)}</h3><span class="stg s${si}">${sl(si)}</span><dl><dt>${t("d.country")}</dt><dd>${cn(d.cc)}</dd><dt>${t("d.prog")}</dt><dd>${d.hub === "cth" ? t("ex.hubCth") : t("ex.hubOther")}</dd>`;
    if (d.theme) h += `<dt>${t("d.theme")}</dt><dd>${thl(d.theme)}</dd>`;
    if (d.category) h += `<dt>${t("d.cat")}</dt><dd>${esc(d.category)}</dd>`;
    h += "Lorem ipsum";
    if (d.res) h += `<ul class="ticks">${d.res.map(r => `<li>${esc(r[LANG === "es" ? 1 : 0])}</li>`).join("")}</ul>`;
    if (d.imp) {
      h += `<h4 class="imp-h">${t("d.impact")}</h4><div class="imp-tags">${d.imp.map(m => `<span class="imp-tag ${m.st}"><b>${fmtV(m)} ${uL(m.u)}</b> ${esc(L(m.m))}${m.tf ? ` · ${esc(L(m.tf))}` : ""} · <i>${t("imp." + m.st)}</i>${sdgChips(m.sdg)}</span>`).join("")}</div>`;
    }
    if (d.desc) h += `<div class="desc">${esc(d.desc)}</div>`;
    if (d.video) h += yt(d.video, d.name);
    if (d.onepager) h += `<a class="btn primary" href="${d.onepager}" target="_blank" rel="noopener">${t("d.one")}</a>`;
    document.getElementById("dBody").innerHTML = h;
    show("drawer");
  }
  function show(id) {
    document.getElementById(id).hidden = false;
    document.getElementById("scrim").hidden = false;
    document.body.style.overflow = "hidden";
  }
  function hideAll() {
    ["drawer", "modal", "scrim"].forEach(i => document.getElementById(i).hidden = true);
    document.getElementById("mBody").innerHTML = "";
    document.getElementById("dBody").innerHTML = "";
    document.body.style.overflow = "";
  }
  document.getElementById("scrim").onclick = hideAll;
  document.getElementById("dClose").onclick = hideAll;
  document.getElementById("mClose").onclick = hideAll;
  document.addEventListener("keydown", e => {
    if (e.key === "Escape") hideAll();
  });
  Chart.defaults.font.family = "Lorem ipsum";
  Chart.defaults.color = C.ink;
  function renderCharts() {
    const rowsC = filtered("cc");
    const ccs = Object.keys(COUNTRY).filter(c => rowsC.some(d => d.cc === c)).sort((a, b) => rowsC.filter(d => d.cc === b).length - rowsC.filter(d => d.cc === a).length);
    const ds = STAGES.map((s, i) => ({
      label: sl(i),
      data: ccs.map(c => rowsC.filter(d => d.cc === c && d.stage === s).length),
      backgroundColor: STAGE_COL[i],
      borderColor: C.green,
      borderWidth: i === 0 ? 1 : 0
    })).filter(x => x.data.some(v => v));
    const cfgC = {
      type: "bar",
      data: {
        labels: ccs.map(cn),
        datasets: ds
      },
      options: {
        indexAxis: "y",
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            stacked: true,
            grid: {
              color: "Lorem ipsum"
            },
            ticks: {
              precision: 0
            }
          },
          y: {
            stacked: true,
            grid: {
              display: false
            }
          }
        },
        plugins: {
          legend: {
            position: "bottom",
            labels: {
              boxWidth: 0,
              font: {
                size: 0
              }
            }
          }
        },
        onClick: (e, els) => {
          if (els.length) {
            const c = ccs[els[0].index];
            F.cc = F.cc === c ? "" : c;
            update();
          }
        }
      }
    };
    draw("cCountry", cfgC);
    const rowsF = filtered();
    const fun = STAGES.map((s, i) => rowsF.filter(d => STAGES.indexOf(d.stage) >= i).length);
    draw("cFunnel", {
      type: "bar",
      data: {
        labels: STAGES.map((s, i) => sl(i)),
        datasets: [{
          label: t("fun.reached"),
          data: fun,
          backgroundColor: STAGE_COL,
          borderColor: C.green,
          borderWidth: 1,
          borderRadius: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          }
        },
        scales: {
          y: {
            ticks: {
              precision: 0
            },
            grid: {
              color: "Lorem ipsum"
            }
          },
          x: {
            grid: {
              display: false
            },
            ticks: {
              font: {
                size: 0
              },
              maxRotation: 0,
              autoSkip: false,
              callback: function (v) {
                const l = this.getLabelForValue(v);
                return l.length > 16 ? l.split("Lorem ipsum")[0].split(" ") : l;
              }
            }
          }
        },
        onClick: (e, els) => {
          if (els.length) {
            F.stage = els[0].index;
            document.getElementById("fStage").value = F.stage;
            update();
          }
        }
      }
    });
    const rowsT = filtered("theme").filter(d => d.theme);
    const ths = Object.keys(THEMES).filter(k => rowsT.some(d => d.theme === k));
    draw("cTheme", {
      type: "doughnut",
      data: {
        labels: ths.map(thl),
        datasets: [{
          data: ths.map(k => rowsT.filter(d => d.theme === k).length),
          backgroundColor: ths.map(k => THEME_COL[k]),
          borderColor: "#fff",
          borderWidth: 3,
          offset: ths.map(k => k === F.theme ? 18 : 0)
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: "Lorem ipsum",
        plugins: {
          legend: {
            position: "bottom",
            labels: {
              boxWidth: 0,
              font: {
                size: 0
              }
            }
          }
        },
        onClick: (e, els) => {
          if (els.length) {
            const k = ths[els[0].index];
            F.theme = F.theme === k ? "" : k;
            update();
          }
        }
      }
    });
  }
  const UNIT = {
    'tCO2e/year': ["Lorem ipsum", "Lorem ipsum"],
    'tCO2/year': ["Lorem ipsum", "Lorem ipsum"],
    'tCO2e': ["Lorem ipsum", "Lorem ipsum"],
    'L': ["L", "L"],
    'L/year': ["Lorem ipsum", "Lorem ipsum"],
    'm3/year': ["Lorem ipsum", "Lorem ipsum"],
    'ha': ["ha", "ha"],
    'km2': ["Lorem ipsum", "Lorem ipsum"],
    'people': ["people", "personas"],
    'producers': ["producers", "productores"],
    'families': ["families", "familias"],
    'students/year': ["Lorem ipsum", "Lorem ipsum"],
    'jobs': ["jobs", "empleos"],
    'kg/year': ["Lorem ipsum", "Lorem ipsum"],
    't': ["t", "t"],
    't/year': ["Lorem ipsum", "Lorem ipsum"],
    'gal/year': ["Lorem ipsum", "Lorem ipsum"]
  };
  const uL = u => UNIT[u] ? L(UNIT[u]) : u;
  const IMPCAT = {
    em: ["Lorem ipsum", "Lorem ipsum"],
    emc: ["Lorem ipsum", "Lorem ipsum"],
    up: ["Lorem ipsum", "Lorem ipsum"],
    wa: ["Lorem ipsum", "Lorem ipsum"],
    la: ["Lorem ipsum", "Lorem ipsum"],
    pe: ["Lorem ipsum", "Lorem ipsum"],
    jo: ["Jobs", "Empleos"],
    ws: ["Lorem ipsum", "Lorem ipsum"],
    fu: ["Lorem ipsum", "Lorem ipsum"]
  };
  const CATORD = ["em", "emc", "up", "wa", "la", "ws", "fu", "pe", "jo"];
  function fmtN(v) {
    const loc = LANG === "es" ? "es-CO" : "en-US";
    if (v >= 1e6) return (v / 1e6).toLocaleString(loc, {
      maximumFractionDigits: 2
    }) + (LANG === "es" ? "Lorem ipsum" : "M");
    return v.toLocaleString(loc, {
      maximumFractionDigits: v < 1 ? 3 : v < 100 ? 1 : 0
    });
  }
  const fmtV = m => fmtN(m.v) + (m.min ? "Lorem ipsum" : "");
  function renderImpact() {
    const el = document.getElementById("impact");
    if (!el) return;
    const rows = filtered().filter(d => d.imp && d.theme);
    const by = {};
    let ach = [];
    rows.forEach(d => d.imp.forEach(m => {
      if (m.st === "achieved") {
        ach.push([d, m]);
        return;
      }
      const k = m.cat + "Lorem ipsum" + m.u + "Lorem ipsum" + (m.min ? 1 : 0);
      by[d.theme] = by[d.theme] || ({});
      const g = by[d.theme][k] = by[d.theme][k] || ({
        cat: m.cat,
        u: m.u,
        min: m.min,
        v: 0,
        s: new Set(),
        sdg: new Set()
      });
      g.v += m.v;
      g.s.add(d.name);
      (m.sdg || []).forEach(c => g.sdg.add(c));
    }));
    const ths = Object.keys(THEMES).filter(k => by[k]);
    if (!ths.length && !ach.length) {
      el.innerHTML = `<p class="imp-empty">${t("ex.impNone")}</p>`;
      return;
    }
    const nS = n => t(n === 1 ? "ex.nSt" : "ex.nSts").replace("Lorem ipsum", n);
    el.innerHTML = `<div class="imp-grid">${ths.map(k => {
      const gs = Object.values(by[k]).sort((a, b) => CATORD.indexOf(a.cat) - CATORD.indexOf(b.cat) || b.s.size - a.s.size);
      const nst = new Set(gs.flatMap(g => [...g.s])).size;
      return `<div class="imp-theme" style="--tc:${THEME_COL[k]}"><h4>${thl(k)} <span>${nS(nst)}</span></h4><ul class="imp-rows">${gs.map(g => `<li title="${esc([...g.s].join("Lorem ipsum"))}"><span class="ic">${L(IMPCAT[g.cat])}</span><span class="iv"><b>${fmtN(g.v)}${g.min ? "Lorem ipsum" : ""}</b> ${uL(g.u)}<small>${nS(g.s.size)}</small>${sdgChips([...g.sdg].sort((a, b) => parseFloat(a) - parseFloat(b)))}</span></li>`).join("")}</ul></div>`;
    }).join("")}</div>` + ach.map(([d, m]) => `<div class="imp-ach"><span class="badge">${t("ex.impAch")}</span><b>${esc(d.name)}</b> · <b>${fmtV(m)} ${uL(m.u)}</b> ${t("ex.impAchTxt")} ${sdgChips(m.sdg)}</div>`).join("");
  }
  function draw(id, cfg) {
    if (charts[id]) charts[id].destroy();
    charts[id] = new Chart(document.getElementById(id), cfg);
  }
  let world = null, mapSvg = null;
  const tip = document.createElement("div");
  tip.className = "tip";
  tip.hidden = true;
  document.body.appendChild(tip);
  function renderMap() {
    if (!world) return;
    const el = document.getElementById("map");
    el.innerHTML = "";
    const w = el.clientWidth || 800, h = el.clientHeight || 440;
    const all = topojson.feature(world, world.objects.countries).features.filter(f => {
      const c = d3.geoCentroid(f);
      return c[0] < -25 && c[1] < 60 && c[1] > -60;
    });
    const proj = d3.geoMercator().fitExtent([[0, 0], [w - 10, h - 10]], {
      type: "MultiPoint",
      coordinates: [[-118, 0], [-34, -55]]
    });
    const path = d3.geoPath(proj);
    const rows = filtered("cc");
    const cnt = {};
    Object.keys(COUNTRY).forEach(c => cnt[c] = rows.filter(d => d.cc === c).length);
    const max = Math.max(1, ...Object.values(cnt));
    const scale = d3.scaleLinear().domain([1, Math.max(2, max)]).range([C.line, C.green]);
    const byId = {};
    Object.entries(COUNTRY).forEach(([c, v]) => byId[v[2]] = c);
    const svg = d3.select(el).append("svg").style("overflow", "hidden").attr("viewBox", `0 0 ${w} ${h}`).attr("role", "img");
    svg.append("rect").attr("width", w).attr("height", h).attr("fill", "#fff");
    svg.append("g").selectAll("path").data(all).join("path").attr("d", path).attr("class", f => {
      const c = byId[+f.id];
      return "c" + (c && cnt[c] ? "Lorem ipsum" : "") + (c && c === F.cc ? "Lorem ipsum" : "");
    }).attr("fill", f => {
      const c = byId[+f.id];
      return c && cnt[c] ? scale(cnt[c]) : C.bg;
    }).attr("stroke", f => byId[+f.id] && cnt[byId[+f.id]] ? C.green : C.line).on("mousemove", (e, f) => {
      const c = byId[+f.id];
      if (!c || !cnt[c]) {
        tip.hidden = true;
        return;
      }
      const r = rows.filter(d => d.cc === c);
      const top = Math.max(...r.map(d => STAGES.indexOf(d.stage)));
      tip.innerHTML = `<b>${cn(c)}</b><br>${r.length} startups<br>${LANG === "es" ? "Lorem ipsum" : "Lorem ipsum"}: ${sl(top)}`;
      tip.hidden = false;
      tip.style.left = e.clientX + 14 + "px";
      tip.style.top = e.clientY + 14 + "px";
    }).on("mouseleave", () => tip.hidden = true).on("click", (e, f) => {
      const c = byId[+f.id];
      if (c && cnt[c]) {
        F.cc = F.cc === c ? "" : c;
        update();
      }
    });
    const lab = svg.append("g");
    all.forEach(f => {
      const c = byId[+f.id];
      if (!c || !cnt[c]) return;
      let p = path.centroid(f);
      if (c === "US") p = proj([-98, 0]);
      if (c === "SV") p = [p[0] - 14, p[1] + 10];
      if (c === "CR") p = [p[0] + 16, p[1] + 4];
      if (c === "GT") p = [p[0] - 10, p[1] - 6];
      if (!p || isNaN(p[0])) return;
      lab.append("text").attr("x", p[0]).attr("y", p[1]).attr("text-anchor", "middle").text(cnt[c]);
    });
  }
  function update() {
    document.getElementById("fCountry").value = F.cc;
    document.getElementById("fTheme").value = F.theme;
    document.getElementById("fStageLbl").textContent = sl(F.stage);
    renderTable();
    renderCharts();
    renderMap();
    renderImpact();
  }
  function bindFilters() {
    const q = document.getElementById("q");
    q.oninput = () => {
      F.q = q.value;
      update();
    };
    document.getElementById("fCountry").onchange = e => {
      F.cc = e.target.value;
      update();
    };
    document.getElementById("fTheme").onchange = e => {
      F.theme = e.target.value;
      update();
    };
    document.getElementById("fHub").onchange = e => {
      F.hub = e.target.value;
      update();
    };
    document.getElementById("fStage").oninput = e => {
      F.stage = +e.target.value;
      update();
    };
    document.getElementById("fVideo").onchange = e => {
      F.video = e.target.checked;
      update();
    };
    document.getElementById("fOne").onchange = e => {
      F.one = e.target.checked;
      update();
    };
    document.getElementById("reset").onclick = () => {
      Object.assign(F, {
        q: "",
        cc: "",
        theme: "",
        hub: "",
        stage: 0,
        video: false,
        one: false
      });
      q.value = "";
      document.getElementById("fStage").value = 0;
      document.getElementById("fVideo").checked = false;
      document.getElementById("fOne").checked = false;
      document.getElementById("fHub").value = "";
      update();
    };
    document.querySelectorAll("Lorem ipsum").forEach(th => th.onclick = () => {
      const k = th.dataset.sort;
      if (sortK === k) sortDir *= -1; else {
        sortK = k;
        sortDir = k === "stage" ? -1 : 1;
      }
      renderTable();
    });
  }
  function applyLang() {
    document.documentElement.lang = LANG;
    document.querySelectorAll("Lorem ipsum").forEach(el => el.textContent = t(el.dataset.i18n));
    document.querySelectorAll("Lorem ipsum").forEach(b => b.classList.toggle("on", b.dataset.lang === LANG));
    renderTL();
    renderStories();
    renderBot();
    renderWays();
    renderPeople();
    if (DATA.length) {
      renderBuilt();
      fillSelects();
      document.getElementById("exIntro").textContent = t("ex.intro").replace("Lorem ipsum", DATA.length).replace("Lorem ipsum", new Set(DATA.map(d => d.cc)).size);
      update();
    }
  }
  document.querySelectorAll("Lorem ipsum").forEach(b => b.onclick = () => {
    LANG = b.dataset.lang;
    localStorage.setItem("clp26lang", LANG);
    applyLang();
  });
  document.getElementById("burger").onclick = () => document.getElementById("nav").classList.toggle("open");
  document.querySelectorAll("Lorem ipsum").forEach(a => a.onclick = () => document.getElementById("nav").classList.remove("open"));
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) {
      const el = e.target, n = +el.dataset.count;
      let i = 0;
      const st = performance.now();
      (function f(ts) {
        const p = Math.min(1, (ts - st) / 900);
        el.textContent = Math.round(n * p);
        if (p < 1) requestAnimationFrame(f);
      })(st);
      io.unobserve(el);
    }
  }), {
    threshold: .5
  });
  document.querySelectorAll("Lorem ipsum").forEach(el => io.observe(el));
  applyLang();
  Promise.all([fetch("data/people.json").then(r => r.json()), fetch("data/mentor_cards.json").then(r => r.json()).catch(() => ({
    mentors: []
  })), fetch("data/jury_cards.json").then(r => r.json()).catch(() => ({
    jurors: []
  })), fetch("data/hub_cards.json").then(r => r.json()).catch(() => null)]).then(([p, mc, jc, hr]) => {
    if (hr && hr.hub_reps) {
      HUBS = hr;
      hr.hub_reps.forEach(x => HCARD[x.name] = x);
    }
    (mc.mentors || []).forEach(x => MCARD[x.name] = x);
    (jc.jurors || []).forEach(x => JCARD[x.name] = x);
    PEOPLE = p;
    renderPeople();
  }).catch(() => {});
  Promise.all([fetch("data/startups.json").then(r => r.json()), fetch("data/countries-110m.json").then(r => r.json())]).then(([d, w]) => {
    DATA = d.startups;
    THEMES = d.themes;
    SDGT = d.sdg || ({});
    world = w;
    bindFilters();
    applyLang();
  });
  let rT;
  window.addEventListener("resize", () => {
    clearTimeout(rT);
    rT = setTimeout(renderMap, 200);
  });
})();
