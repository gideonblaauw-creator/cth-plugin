(function () {
  "use strict";

  /* ---------- preferences ---------- */
  var mqReduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  var reducedMotion = mqReduce.matches;

  function isMobileWidth() {
    return window.matchMedia("(max-width: 768px)").matches;
  }

  /* Ancho + reduced-motion only: (pointer: coarse) is true in many headless profiles and would hide WebGL en capturas. */
  var allow3d = typeof THREE !== "undefined" && !reducedMotion && !isMobileWidth();

  /* ---------- layout: progress + nav spy + burger ---------- */
  var sections = [].slice.call(document.querySelectorAll("section[id].deck-section"));
  var nav = document.getElementById("nav");
  var navLinks = document.querySelectorAll("#nav a[href^='#']");
  var burger = document.getElementById("burger");
  var readProgress = document.getElementById("readProgress");
  var readProgressBar = document.getElementById("readProgressBar");

  function setReadProgress() {
    if (!readProgressBar) return;
    var doc = document.documentElement;
    var scrollTop = window.scrollY || doc.scrollTop;
    var max = Math.max(1, doc.scrollHeight - window.innerHeight);
    var p = Math.min(100, Math.max(0, (scrollTop / max) * 100));
    readProgressBar.style.width = p.toFixed(2) + "%";
  }

  window.addEventListener("scroll", setReadProgress, { passive: true });
  window.addEventListener("resize", setReadProgress);
  setReadProgress();

  if (sections.length && navLinks.length && "IntersectionObserver" in window) {
    var obsNav = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          var id = en.target.id;
          navLinks.forEach(function (a) {
            a.classList.toggle("act", a.getAttribute("href") === "#" + id);
          });
        });
      },
      { rootMargin: "-38% 0px -38% 0px", threshold: 0 }
    );
    sections.forEach(function (s) {
      obsNav.observe(s);
    });
  }

  if (burger && nav) {
    burger.addEventListener("click", function () {
      nav.classList.toggle("open");
    });
    navLinks.forEach(function (a) {
      a.addEventListener("click", function () {
        nav.classList.remove("open");
      });
    });
  }

  /* ---------- reveal on scroll ---------- */
  if ("IntersectionObserver" in window) {
    var revObs = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) en.target.classList.add("is-visible");
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
    );
    document.querySelectorAll(".reveal-on-scroll").forEach(function (el) {
      revObs.observe(el);
    });
  } else {
    document.querySelectorAll(".reveal-on-scroll").forEach(function (el) {
      el.classList.add("is-visible");
    });
  }

  /* ---------- count-up (once, when stats visible) ---------- */
  function animateCount(el, target, ms, suffix) {
    suffix = suffix || "";
    var t0 = performance.now();
    function frame(now) {
      var p = Math.min(1, (now - t0) / ms);
      var e = 1 - Math.pow(1 - p, 3);
      var v = Math.round(target * e);
      el.textContent = String(v) + suffix;
      if (p < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  var statEls = document.querySelectorAll(".stat .num[data-count]");
  if (statEls.length && "IntersectionObserver" in window && !reducedMotion) {
    var didCount = false;
    var countObs = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting || didCount) return;
          didCount = true;
          statEls.forEach(function (el) {
            var t = parseInt(el.getAttribute("data-count"), 10);
            if (isNaN(t)) return;
            var suf = el.getAttribute("data-suffix");
            suf = suf === null ? "" : suf;
            animateCount(el, t, 1000, suf);
          });
          countObs.disconnect();
        });
      },
      { threshold: 0.25 }
    );
    var clpSec = document.getElementById("clp");
    if (clpSec) countObs.observe(clpSec);
  } else {
    statEls.forEach(function (el) {
      var t = parseInt(el.getAttribute("data-count"), 10);
      if (isNaN(t)) return;
      var suf = el.getAttribute("data-suffix");
      suf = suf === null ? "" : suf;
      el.textContent = String(t) + suf;
    });
  }

  /* ---------- HELIX núcleo accordion ---------- */
  document.querySelectorAll(".nucleo-card").forEach(function (btn) {
    var id = btn.getAttribute("aria-controls");
    var body = id ? document.getElementById(id) : null;
    if (!body) return;
    btn.addEventListener("click", function () {
      var open = btn.getAttribute("aria-expanded") === "true";
      open = !open;
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      body.hidden = !open;
      btn.classList.toggle("is-open", open);
    });
  });

  /* ---------- Datalab env tabs ---------- */
  var envTabs = document.querySelectorAll(".env-tab");
  envTabs.forEach(function (tab) {
    tab.addEventListener("click", function () {
      var panelId = tab.getAttribute("aria-controls");
      var panel = panelId ? document.getElementById(panelId) : null;
      if (!panel) return;
      envTabs.forEach(function (t) {
        var on = t === tab;
        t.classList.toggle("on", on);
        t.setAttribute("aria-selected", on ? "true" : "false");
        var pid = t.getAttribute("aria-controls");
        var p = pid ? document.getElementById(pid) : null;
        if (p) {
          p.classList.toggle("on", on);
          p.hidden = !on;
        }
      });
    });
  });

  /* ---------- work stepper ---------- */
  var stepper = document.getElementById("workStepper");
  if (stepper) {
    stepper.querySelectorAll(".stepper-btn").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var item = btn.closest(".stepper-item");
        if (!item) return;
        var open = btn.getAttribute("aria-expanded") === "true";
        stepper.querySelectorAll(".stepper-item").forEach(function (it) {
          var b = it.querySelector(".stepper-btn");
          var p = it.querySelector(".stepper-panel");
          var isHere = it === item;
          if (b) b.setAttribute("aria-expanded", isHere ? "true" : "false");
          it.classList.toggle("is-open", isHere);
          if (p) p.hidden = !isHere;
        });
      });
    });
  }

  /* ---------- subtle card tilt ---------- */
  if (!reducedMotion && window.matchMedia("(hover: hover)").matches) {
    document
      .querySelectorAll(".card, .invite-card, .chart-card, .bcard, .nucleo-card, .explorer")
      .forEach(function (card) {
      var max = 5;
      function reset() {
        card.style.transform = "";
      }
      card.addEventListener("pointermove", function (e) {
        var r = card.getBoundingClientRect();
        var px = (e.clientX - r.left) / r.width - 0.5;
        var py = (e.clientY - r.top) / r.height - 0.5;
        var rx = (-py * max).toFixed(2);
        var ry = (px * max).toFixed(2);
        card.style.transform = "perspective(900px) rotateX(" + rx + "deg) rotateY(" + ry + "deg)";
      });
      card.addEventListener("pointerleave", reset);
      card.addEventListener("blur", reset);
    });
  }

  /* ---------- Chart.js data layer ---------- */
  var COL = ["#0C498A", "#69B5FA", "#9DC384", "#669348", "#B2EEFA"];

  var CC_ES = {
    CO: "Colombia",
    PE: "Perú",
    SV: "El Salvador",
    CR: "Costa Rica",
    GT: "Guatemala",
    AR: "Argentina",
    EC: "Ecuador",
    MX: "México",
    US: "Estados Unidos",
    BR: "Brasil",
  };

  /* approximate lat/lon for startup country codes (cartera CLP26) */
  var CC_LATLON = {
    CO: [4.65, -74.05],
    PE: [-12.05, -77.04],
    CR: [9.93, -84.09],
    GT: [14.63, -90.51],
    SV: [13.7, -89.2],
    AR: [-34.6, -58.38],
    EC: [-0.18, -78.47],
    MX: [19.43, -99.13],
    US: [38.9, -77.04],
    BR: [-15.78, -47.93],
  };

  var ST_ORDER = ["cohort", "national", "semi", "regional", "global"];
  var ST_ES = {
    cohort: "Cohort / bootcamp",
    national: "Final nacional",
    semi: "Semifinal regional",
    regional: "Final regional Américas",
    global: "Final global (Singapur)",
  };

  var CTH5 = ["CO", "PE", "SV", "CR", "GT"];

  var chartInstances = {};
  var chartChip = { country: "all", funnel: "all", theme: "coded" };
  var globalFilters = { cc: "", theme: "", stage: "" };
  var startupsAll = [];
  var themeLabels = {};
  var chartTooltip = {
    callbacks: {
      label: function (ctx) {
        var v = ctx.parsed;
        if (ctx.chart && ctx.chart.config.type === "doughnut") {
          var t = ctx.label || "";
          return t + ": " + (ctx.parsed || 0);
        }
        if (typeof v === "object" && v !== null) {
          if (v.x !== undefined) return (ctx.dataset.label || "") + ": " + v.x;
          if (v.y !== undefined) return (ctx.dataset.label || "") + ": " + v.y;
        }
        return (ctx.dataset.label || "") + ": " + (v != null ? v : "");
      },
    },
  };

  function fetchJson(url) {
    return fetch(url).then(function (r) {
      if (!r.ok) throw new Error("fetch " + url + " " + r.status);
      return r.json();
    });
  }

  function startupMatchesGlobal(s) {
    if (globalFilters.cc && s.cc !== globalFilters.cc) return false;
    if (globalFilters.stage && s.stage !== globalFilters.stage) return false;
    if (globalFilters.theme) {
      if (!s.theme || s.theme !== globalFilters.theme) return false;
    }
    return true;
  }

  function applyExplorerFilters(list) {
    var c = document.getElementById("exCountry");
    var th = document.getElementById("exTheme");
    var st = document.getElementById("exStage");
    var q = document.getElementById("exQ");
    var country = c && c.value;
    var theme = th && th.value;
    var stage = st && st.value;
    var needle = (q && q.value ? q.value : "").trim().toLowerCase();
    return list.filter(function (s) {
      if (country && s.cc !== country) return false;
      if (theme && s.theme !== theme) return false;
      if (stage && s.stage !== stage) return false;
      if (needle) {
        var cat = (s.category || "").toLowerCase();
        var name = (s.name || "").toLowerCase();
        if (name.indexOf(needle) === -1 && cat.indexOf(needle) === -1) return false;
      }
      return true;
    });
  }

  function aggregateForCharts(startups) {
    var byCc = {};
    startups.forEach(function (s) {
      var cc = s.cc || "?";
      byCc[cc] = (byCc[cc] || 0) + 1;
    });

    var bySt = {};
    ST_ORDER.forEach(function (k) {
      bySt[k] = 0;
    });
    startups.forEach(function (s) {
      var st = s.stage;
      if (st && Object.prototype.hasOwnProperty.call(bySt, st)) bySt[st] += 1;
    });

    var byTh = {};
    startups.forEach(function (s) {
      if (!s.theme) return;
      byTh[s.theme] = (byTh[s.theme] || 0) + 1;
    });

    return { byCc: byCc, bySt: bySt, byTh: byTh };
  }

  function countryChartData(byCc) {
    var ccs = Object.keys(byCc);
    var mode = chartChip.country;
    if (mode === "cth5") {
      ccs = ccs.filter(function (c) {
        return CTH5.indexOf(c) >= 0;
      });
      ccs.sort(function (a, b) {
        return CTH5.indexOf(a) - CTH5.indexOf(b);
      });
    } else if (mode === "top5") {
      ccs.sort(function (a, b) {
        var d = byCc[b] - byCc[a];
        if (d !== 0) return d;
        return (CC_ES[a] || a).localeCompare(CC_ES[b] || b, "es");
      });
      ccs = ccs.slice(0, 5);
    } else {
      var priority = CTH5.slice();
      ccs.sort(function (a, b) {
        var ia = priority.indexOf(a);
        var ib = priority.indexOf(b);
        if (ia === -1 && ib === -1) return (CC_ES[a] || a).localeCompare(CC_ES[b] || b, "es");
        if (ia === -1) return 1;
        if (ib === -1) return -1;
        return ia - ib;
      });
    }
    return {
      labels: ccs.map(function (cc) {
        return CC_ES[cc] || cc;
      }),
      data: ccs.map(function (cc) {
        return byCc[cc];
      }),
      codes: ccs,
    };
  }

  function funnelChartData(bySt) {
    var order = ST_ORDER.slice();
    if (chartChip.funnel === "trim") {
      order = order.filter(function (k) {
        return k !== "cohort";
      });
    }
    return {
      labels: order.map(function (k) {
        return ST_ES[k] || k;
      }),
      data: order.map(function (k) {
        return bySt[k] || 0;
      }),
    };
  }

  function themeChartData(byTh) {
    var thKeys = Object.keys(byTh).sort(function (a, b) {
      return byTh[b] - byTh[a];
    });
    if (chartChip.theme === "all") {
      var n = startupsAll.filter(function (s) {
        return startupMatchesGlobal(s) && !s.theme;
      }).length;
      if (n > 0) {
        thKeys.push("__none__");
        byTh.__none__ = n;
      }
    }
    return {
      keys: thKeys,
      labels: thKeys.map(function (k) {
        if (k === "__none__") return "Sin tema codificado";
        var pair = themeLabels[k];
        return Array.isArray(pair) ? pair[1] || pair[0] : k;
      }),
      data: thKeys.map(function (k) {
        return byTh[k] || 0;
      }),
    };
  }

  function updateCharts(startups) {
    if (typeof Chart === "undefined") return;
    var agg = aggregateForCharts(startups);
    var cd = countryChartData(agg.byCc);
    var fd = funnelChartData(agg.bySt);
    var td = themeChartData(agg.byTh);

    var common = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { enabled: true, callbacks: chartTooltip.callbacks },
      },
    };

    var c1 = document.getElementById("cCountry");
    if (c1 && chartInstances.country) {
      chartInstances.country.data.labels = cd.labels;
      chartInstances.country.data.datasets[0].data = cd.data;
      chartInstances.country.data.datasets[0].backgroundColor = cd.data.map(function (_, i) {
        return COL[i % COL.length];
      });
      chartInstances.country.update();
    } else if (c1) {
      chartInstances.country = new Chart(c1, {
        type: "bar",
        data: {
          labels: cd.labels,
          datasets: [
            {
              label: "Startups",
              data: cd.data,
              backgroundColor: cd.data.map(function (_, i) {
                return COL[i % COL.length];
              }),
            },
          ],
        },
        options: Object.assign({}, common, {
          indexAxis: "y",
          scales: {
            x: { beginAtZero: true, ticks: { precision: 0 } },
          },
        }),
      });
    }

    var c2 = document.getElementById("cFunnel");
    if (c2 && chartInstances.funnel) {
      chartInstances.funnel.data.labels = fd.labels;
      chartInstances.funnel.data.datasets[0].data = fd.data;
      chartInstances.funnel.update();
    } else if (c2) {
      chartInstances.funnel = new Chart(c2, {
        type: "bar",
        data: {
          labels: fd.labels,
          datasets: [{ label: "Startups", data: fd.data, backgroundColor: "#0C498A" }],
        },
        options: Object.assign({}, common, {
          scales: {
            y: {
              ticks: { autoSkip: false, maxRotation: 65, minRotation: 0, font: { size: 10 } },
            },
            x: { beginAtZero: true, ticks: { precision: 0 } },
          },
        }),
      });
    }

    var c3 = document.getElementById("cTheme");
    if (c3 && chartInstances.theme) {
      chartInstances.theme.destroy();
      chartInstances.theme = null;
    }
    if (c3 && td.data.length) {
      chartInstances.theme = new Chart(c3, {
        type: "doughnut",
        data: {
          labels: td.labels,
          datasets: [{ data: td.data, backgroundColor: td.data.map(function (_, i) {
            return COL[i % COL.length];
          }) }],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: "bottom",
              labels: { font: { size: 10 }, color: "#1a2b3a" },
            },
            tooltip: { enabled: true, callbacks: chartTooltip.callbacks },
          },
        },
      });
    } else if (c3) {
      var ctx = c3.getContext("2d");
      ctx.clearRect(0, 0, c3.width, c3.height);
      ctx.font = "14px sans-serif";
      ctx.fillStyle = "#5f6b75";
      ctx.fillText("Sin datos con los filtros actuales", 10, 80);
    }
  }

  function fillSelect(sel, values, labelFn, keepFirst) {
    if (!sel) return;
    var firstOpt = sel.options[0];
    var firstClone = keepFirst && firstOpt ? firstOpt.cloneNode(true) : null;
    sel.innerHTML = "";
    if (firstClone) sel.appendChild(firstClone);
    else {
      var o0 = document.createElement("option");
      o0.value = "";
      o0.textContent = "Todos";
      sel.appendChild(o0);
    }
    values.forEach(function (v) {
      var o = document.createElement("option");
      o.value = v;
      o.textContent = labelFn(v);
      sel.appendChild(o);
    });
  }

  function uniqueSorted(arr) {
    var u = {};
    arr.forEach(function (x) {
      u[x] = true;
    });
    return Object.keys(u).sort(function (a, b) {
      return (CC_ES[a] || a).localeCompare(CC_ES[b] || b, "es");
    });
  }

  function renderExplorer(rows) {
    var tb = document.querySelector("#exTable tbody");
    var cnt = document.getElementById("exCount");
    if (!tb) return;
    tb.innerHTML = "";
    rows.forEach(function (s) {
      var tr = document.createElement("tr");
      var thKey = s.theme || "";
      var pair = themeLabels[thKey];
      var thLabel = Array.isArray(pair) ? pair[1] || pair[0] : thKey || "—";
      tr.innerHTML =
        "<td>" +
        (s.name || "") +
        "</td><td>" +
        (CC_ES[s.cc] || s.cc || "—") +
        "</td><td>" +
        thLabel +
        "</td><td>" +
        (ST_ES[s.stage] || s.stage || "—") +
        "</td>";
      tb.appendChild(tr);
    });
    if (cnt) cnt.textContent = rows.length === 1 ? "1 startup" : rows.length + " startups";
  }

  function getFilteredForCharts() {
    return startupsAll.filter(startupMatchesGlobal);
  }

  function wireFiltersAndExplorer() {
    var gfCountry = document.getElementById("gfCountry");
    var gfTheme = document.getElementById("gfTheme");
    var gfStage = document.getElementById("gfStage");
    var gfReset = document.getElementById("gfReset");

    function syncGlobalFromUI() {
      globalFilters.cc = gfCountry && gfCountry.value ? gfCountry.value : "";
      globalFilters.theme = gfTheme && gfTheme.value ? gfTheme.value : "";
      globalFilters.stage = gfStage && gfStage.value ? gfStage.value : "";
    }

    function refresh() {
      syncGlobalFromUI();
      var forCharts = getFilteredForCharts();
      updateCharts(forCharts);
      renderExplorer(applyExplorerFilters(forCharts));
    }

    if (gfReset) {
      gfReset.addEventListener("click", function () {
        if (gfCountry) gfCountry.value = "";
        if (gfTheme) gfTheme.value = "";
        if (gfStage) gfStage.value = "";
        refresh();
      });
    }
    [gfCountry, gfTheme, gfStage].forEach(function (el) {
      if (el) el.addEventListener("change", refresh);
    });

    document.querySelectorAll(".chart-filter-row").forEach(function (row) {
      var scope = row.getAttribute("data-chart-scope");
      row.querySelectorAll(".chip-filter").forEach(function (chip) {
        chip.addEventListener("click", function () {
          row.querySelectorAll(".chip-filter").forEach(function (c) {
            c.classList.remove("on");
            c.setAttribute("aria-pressed", "false");
          });
          chip.classList.add("on");
          chip.setAttribute("aria-pressed", "true");
          var mode = chip.getAttribute("data-mode") || "all";
          if (scope === "country") chartChip.country = mode;
          else if (scope === "funnel") chartChip.funnel = mode;
          else if (scope === "theme") chartChip.theme = mode;
          refresh();
        });
      });
    });

    ["exCountry", "exTheme", "exStage", "exQ"].forEach(function (id) {
      var el = document.getElementById(id);
      if (!el) return;
      el.addEventListener(id === "exQ" ? "input" : "change", function () {
        syncGlobalFromUI();
        renderExplorer(applyExplorerFilters(getFilteredForCharts()));
      });
    });
  }

  /* ---------- Three.js hero (globe + arcs Bogotá hub CTH → países en cartera) ---------- */
  function latLonToVec3(lat, lon, r) {
    var phi = ((90 - lat) * Math.PI) / 180;
    var theta = ((lon + 180) * Math.PI) / 180;
    return new THREE.Vector3(
      -r * Math.sin(phi) * Math.cos(theta),
      r * Math.cos(phi),
      r * Math.sin(phi) * Math.sin(theta)
    );
  }

  function initHeroGlobe(byCc) {
    var wrap = document.getElementById("heroGlobeWrap");
    var canvas = document.getElementById("heroGlobe");
    if (!wrap || !canvas) return;
    var heroRoot = wrap.closest(".hero");

    if (!allow3d) {
      wrap.style.display = "none";
      return;
    }
    if (heroRoot) heroRoot.classList.add("hero-3d-on");

    var renderer = new THREE.WebGLRenderer({
      canvas: canvas,
      alpha: true,
      antialias: true,
      powerPreference: "low-power",
    });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(42, 1, 0.1, 100);
    camera.position.z = 2.55;

    var group = new THREE.Group();
    scene.add(group);

    var amb = new THREE.AmbientLight(0xffffff, 0.55);
    scene.add(amb);
    var dir = new THREE.DirectionalLight(0xb2eefa, 0.45);
    dir.position.set(2, 3, 4);
    scene.add(dir);

    var sphereGeom = new THREE.SphereGeometry(1, 48, 48);
    var sphereMat = new THREE.MeshPhongMaterial({
      color: 0x0c498a,
      emissive: 0x072a4d,
      shininess: 18,
      transparent: true,
      opacity: 0.92,
    });
    var globe = new THREE.Mesh(sphereGeom, sphereMat);
    group.add(globe);

    var wire = new THREE.Mesh(
      sphereGeom.clone(),
      new THREE.MeshBasicMaterial({ color: 0x69b5fa, wireframe: true, transparent: true, opacity: 0.11 })
    );
    wire.scale.setScalar(1.002);
    group.add(wire);

    /* markers — point size encodes volume lightly via color */
    var positions = [];
    var cols = [];
    /* Origen único: Bogotá (hub CleantechHUB; misma ventana geográfica que la sesión con la Escuela). */
    var hubBogota = latLonToVec3(4.65, -74.05, 1.02);

    Object.keys(byCc).forEach(function (cc) {
      var ll = CC_LATLON[cc];
      if (!ll) return;
      var n = byCc[cc];
      var p = latLonToVec3(ll[0], ll[1], 1.03);
      positions.push(p.x, p.y, p.z);
      var c = new THREE.Color(n >= 10 ? 0x9dc384 : 0x69b5fa);
      cols.push(c.r, c.g, c.b);
    });

    if (positions.length) {
      var g = new THREE.BufferGeometry();
      g.setAttribute("position", new THREE.Float32BufferAttribute(positions, 3));
      g.setAttribute("color", new THREE.Float32BufferAttribute(cols, 3));
      var m = new THREE.PointsMaterial({
        size: 0.055,
        vertexColors: true,
        transparent: true,
        opacity: 0.95,
        depthWrite: false,
        sizeAttenuation: true,
      });
      var pts = new THREE.Points(g, m);
      group.add(pts);
    }

    Object.keys(byCc).forEach(function (cc) {
      var ll = CC_LATLON[cc];
      if (!ll) return;
      var end = latLonToVec3(ll[0], ll[1], 1.03);
      var mid = hubBogota.clone().lerp(end, 0.5).normalize().multiplyScalar(1.28);
      var curve = new THREE.QuadraticBezierCurve3(hubBogota, mid, end);
      var segs = Math.min(24, 8 + (byCc[cc] || 0));
      var pts2 = curve.getPoints(segs);
      var geo = new THREE.BufferGeometry().setFromPoints(pts2);
      group.add(
        new THREE.Line(
          geo,
          new THREE.LineBasicMaterial({
            color: cc === "CO" ? 0x9dc384 : 0x69b5fa,
            transparent: true,
            opacity: 0.28,
          })
        )
      );
    });

    var running = true;
    var t0 = performance.now();

    function resize() {
      var w = wrap.clientWidth || 1;
      var h = wrap.clientHeight || 1;
      renderer.setSize(w, h, false);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
    }

    var ro = new ResizeObserver(resize);
    ro.observe(wrap);
    resize();

    function tick(now) {
      if (!running) return;
      var t = (now - t0) / 1000;
      group.rotation.y = t * 0.22;
      group.rotation.x = Math.sin(t * 0.15) * 0.08;
      renderer.render(scene, camera);
      requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);

    document.addEventListener("visibilitychange", function () {
      running = document.visibilityState === "visible";
      if (running) requestAnimationFrame(tick);
    });

    function onReduceChange() {
      if (mqReduce.matches) {
        running = false;
        wrap.style.display = "none";
        if (heroRoot) heroRoot.classList.remove("hero-3d-on");
      }
    }
    if (mqReduce.addEventListener) mqReduce.addEventListener("change", onReduceChange);
    else if (mqReduce.addListener) mqReduce.addListener(onReduceChange);
  }

  /* ---------- load startups.json ---------- */
  fetchJson("data/startups.json")
    .then(function (d) {
      startupsAll = d.startups || [];
      themeLabels = d.themes || {};

      /* globe aggregates (full cartera) */
      var byCcFull = {};
      startupsAll.forEach(function (s) {
        var cc = s.cc || "?";
        byCcFull[cc] = (byCcFull[cc] || 0) + 1;
      });
      initHeroGlobe(byCcFull);

      /* global filter options */
      var themesInData = {};
      startupsAll.forEach(function (s) {
        if (s.theme) themesInData[s.theme] = true;
      });
      var themeKeys = Object.keys(themesInData).sort();
      fillSelect(
        document.getElementById("gfTheme"),
        themeKeys,
        function (k) {
          var pair = themeLabels[k];
          return Array.isArray(pair) ? pair[1] || pair[0] : k;
        },
        true
      );
      fillSelect(
        document.getElementById("gfCountry"),
        uniqueSorted(
          startupsAll.map(function (s) {
            return s.cc;
          })
        ),
        function (cc) {
          return CC_ES[cc] || cc;
        },
        true
      );
      fillSelect(
        document.getElementById("gfStage"),
        ST_ORDER.slice(),
        function (k) {
          return ST_ES[k] || k;
        },
        true
      );

      fillSelect(
        document.getElementById("exCountry"),
        uniqueSorted(
          startupsAll.map(function (s) {
            return s.cc;
          })
        ),
        function (cc) {
          return CC_ES[cc] || cc;
        },
        true
      );
      fillSelect(
        document.getElementById("exTheme"),
        themeKeys,
        function (k) {
          var pair = themeLabels[k];
          return Array.isArray(pair) ? pair[1] || pair[0] : k;
        },
        true
      );
      fillSelect(
        document.getElementById("exStage"),
        ST_ORDER,
        function (k) {
          return ST_ES[k] || k;
        },
        true
      );

      wireFiltersAndExplorer();
      updateCharts(getFilteredForCharts());
      renderExplorer(applyExplorerFilters(getFilteredForCharts()));
    })
    .catch(function () {
      console.warn("eci deck: no se pudo cargar data/startups.json");
      initHeroGlobe({});
    });
})();
