/* Zidi MEG — vanilla interactions (Reveal + Chart.js). Degrades for print-pdf / decktape. */
(function () {
  "use strict";

  var isPrint = /print-pdf/.test(location.search) || document.body.classList.contains("print-pdf");
  var chartPool = {};
  var B = "#0C498A",
    C = "#B2EEFA",
    G = "#9DC384",
    F = "#669348",
    S = "#69B5FA";

  function qs(sel, root) {
    return (root || document).querySelector(sel);
  }
  function qsa(sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  }

  function initLadder() {
    qsa("[data-fp-ladder]").forEach(function (wrap) {
      var steps = qsa(".fp-ladder-step", wrap);
      var detail = qs(".fp-ladder-detail", wrap);
      function pick(i) {
        steps.forEach(function (s, j) {
          s.classList.toggle("is-active", j === i);
          s.setAttribute("aria-pressed", j === i ? "true" : "false");
        });
        if (detail) detail.textContent = steps[i].dataset.detail || "";
      }
      steps.forEach(function (step, i) {
        step.addEventListener("click", function () {
          pick(i);
        });
        step.addEventListener("keydown", function (e) {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            pick(i);
          }
        });
      });
      pick(isPrint ? 2 : 0);
    });
  }

  function initJourney() {
    qsa("[data-fp-journey]").forEach(function (wrap) {
      var nodes = qsa(".fp-journey-node", wrap);
      var panel = qs(".fp-journey-panel", wrap);
      function pick(i) {
        nodes.forEach(function (n, j) {
          n.classList.toggle("is-active", j === i);
          n.classList.toggle("is-done", j < i);
        });
        if (panel) panel.innerHTML = nodes[i].dataset.panel || "";
      }
      nodes.forEach(function (node, i) {
        node.addEventListener("click", function () {
          pick(i);
        });
      });
      pick(isPrint ? 3 : 0);
    });
  }

  function initChecklist(sel) {
    qsa(sel).forEach(function (list) {
      qsa("li", list).forEach(function (li) {
        li.setAttribute("role", "button");
        li.setAttribute("tabindex", "0");
        if (isPrint) li.classList.add("is-checked");
        function toggle() {
          li.classList.toggle("is-checked");
        }
        li.addEventListener("click", toggle);
        li.addEventListener("keydown", function (e) {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            toggle();
          }
        });
      });
    });
  }

  function initSectorGrid() {
    qsa(".fp-sector-card").forEach(function (card) {
      var detail = qs(".fp-sector-detail", card);
      function open() {
        var on = card.classList.toggle("is-open");
        card.setAttribute("aria-expanded", on ? "true" : "false");
        if (detail) detail.hidden = !on;
      }
      card.addEventListener("click", open);
      card.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          open();
        }
      });
      if (isPrint) {
        card.classList.add("is-open");
        if (detail) detail.hidden = false;
      }
    });
  }

  function initRiskTable() {
    qsa("[data-fp-risk-table]").forEach(function (table) {
      function clear() {
        qsa("th, td", table).forEach(function (c) {
          c.classList.remove("is-highlight");
        });
      }
      qsa("tbody tr", table).forEach(function (row) {
        row.addEventListener("click", function (e) {
          var cell = e.target.closest("td");
          clear();
          if (cell) {
            row.classList.add("is-highlight");
            cell.classList.add("is-highlight");
            var col = cell.cellIndex;
            qsa("thead th", table).forEach(function (th, i) {
              if (i === col) th.classList.add("is-highlight");
            });
          } else {
            row.classList.add("is-highlight");
          }
        });
      });
      qsa("thead th", table).forEach(function (th, col) {
        if (col === 0) return;
        th.addEventListener("click", function () {
          clear();
          th.classList.add("is-highlight");
          qsa("tbody tr", table).forEach(function (row) {
            var cell = row.cells[col];
            if (cell) cell.classList.add("is-highlight");
          });
        });
      });
    });
  }

  function initInvestorPath() {
    qsa("[data-fp-investor]").forEach(function (wrap) {
      var slider = qs('input[type="range"]', wrap);
      var routeEl = qs(".fp-investor-route", wrap);
      var tradeEl = qs(".fp-investor-trade", wrap);
      var routes = JSON.parse(wrap.dataset.routes || "[]");
      var trades = JSON.parse(wrap.dataset.trades || "[]");
      function sync() {
        var v = slider ? +slider.value : 0;
        qsa(".fp-investor-band", wrap).forEach(function (b, i) {
          b.classList.toggle("is-active", i === v);
        });
        if (routeEl) routeEl.textContent = routes[v] || "";
        if (tradeEl) tradeEl.textContent = trades[v] || "";
      }
      if (slider) {
        slider.addEventListener("input", sync);
        if (isPrint) slider.value = "1";
      }
      sync();
    });
  }

  function initLensToggle() {
    qsa("[data-fp-lens]").forEach(function (wrap) {
      var diaspora = qs('[data-lens="diaspora"]', wrap);
      var inst = qs('[data-lens="institutional"]', wrap);
      var body = qs(".fp-lens-body", wrap);
      var copy = JSON.parse(wrap.dataset.copy || "{}");
      function show(key) {
        diaspora && diaspora.setAttribute("aria-pressed", key === "diaspora" ? "true" : "false");
        inst && inst.setAttribute("aria-pressed", key === "institutional" ? "true" : "false");
        diaspora && diaspora.classList.toggle("is-active", key === "diaspora");
        inst && inst.classList.toggle("is-active", key === "institutional");
        if (body) body.innerHTML = copy[key] || "";
      }
      diaspora &&
        diaspora.addEventListener("click", function () {
          show("diaspora");
        });
      inst &&
        inst.addEventListener("click", function () {
          show("institutional");
        });
      show(isPrint ? "diaspora" : "diaspora");
    });
  }

  function initReadinessChecks() {
    initChecklist("[data-fp-readiness]");
  }

  function initRegChecks() {
    initChecklist("[data-fp-reg-check]");
  }

  function destroyChart(id) {
    if (chartPool[id]) {
      chartPool[id].destroy();
      delete chartPool[id];
    }
  }

  function makeChart(id, cfg) {
    var el = document.getElementById(id);
    if (!el || typeof Chart === "undefined") return;
    destroyChart(id);
    chartPool[id] = new Chart(el, cfg);
  }

  function initCharts() {
    if (typeof Chart === "undefined") return;
    Chart.defaults.font.family = "'Open Sans', sans-serif";
    Chart.defaults.color = "#0C498A";

    makeChart("chart-mubon-bars", {
      type: "bar",
      data: {
        labels: ["Charge points", "Cities", "Workshops", "kW installed"],
        datasets: [
          {
            label: "MubOn network (public case study)",
            data: [115, 9, 6, 800],
            backgroundColor: [B, S, F, G],
            borderRadius: 8,
            borderSkipped: false,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: function (c) {
                var v = c.parsed.y;
                return c.label.indexOf("kW") >= 0 ? " 800+ kW" : " " + v.toLocaleString();
              },
            },
          },
        },
        scales: {
          x: { grid: { display: false }, ticks: { font: { size: 11, weight: "600" } } },
          y: { grid: { color: "#e8f4fa" }, ticks: { font: { size: 10 } } },
        },
      },
    });

    makeChart("chart-kwh", {
      type: "bar",
      data: {
        labels: ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"],
        datasets: [
          {
            label: "kWh delivered",
            data: [28400, 56800, 82000, 96200, 99500, 48852],
            backgroundColor: [C, C, S, S, B, F],
            borderRadius: 6,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { display: false }, ticks: { font: { size: 9 } } },
          y: {
            grid: { color: "#edf2f7" },
            ticks: {
              callback: function (v) {
                return v / 1000 + "k";
              },
              font: { size: 9 },
            },
          },
        },
      },
    });

    makeChart("chart-impact-donut", {
      type: "doughnut",
      data: {
        labels: ["14k users", "20k+ sessions", "115 points", "9 cities"],
        datasets: [
          {
            data: [43, 40, 12, 5],
            backgroundColor: [B, S, F, G],
            borderWidth: 2,
            borderColor: "#fff",
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: "55%",
        plugins: { legend: { position: "bottom", labels: { font: { size: 10 }, boxWidth: 10 } } },
      },
    });

    makeChart("chart-ev-trend", {
      type: "bar",
      data: {
        labels: ["EVs matriculated 2025", "EVs registered Q1 2026"],
        datasets: [
          {
            label: "Colombia RUNT (public MubOn page)",
            data: [19724, 9349],
            backgroundColor: [S, F],
            borderRadius: 6,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { display: false } },
          y: { grid: { color: "#edf2f7" }, ticks: { font: { size: 9 } } },
        },
      },
    });

    makeChart("chart-workshops", {
      type: "doughnut",
      data: {
        labels: ["Delivered", "Grant window"],
        datasets: [
          {
            data: [6, 1],
            backgroundColor: [F, C],
            borderWidth: 2,
            borderColor: "#fff",
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: "62%",
        plugins: {
          legend: { position: "bottom", labels: { font: { size: 10 } } },
          title: { display: true, text: "Multi-stakeholder workshops", font: { size: 11 } },
        },
      },
    });
  }

  function initCounters() {
    qsa("[data-count]").forEach(function (el) {
      var target = +el.dataset.count;
      var suffix = el.dataset.suffix || "";
      if (isPrint) {
        el.textContent = target.toLocaleString() + suffix;
        return;
      }
      var start = performance.now();
      var dur = 1200;
      (function tick(now) {
        var t = Math.min((now - start) / dur, 1);
        var eased = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
        el.textContent = Math.round(target * eased).toLocaleString() + suffix;
        if (t < 1) requestAnimationFrame(tick);
        else el.textContent = target.toLocaleString() + suffix;
      })(start);
    });
  }

  function initQ3Toggle() {
    qsa("[data-fp-q3-toggle]").forEach(function (wrap) {
      var tabs = qsa("[data-q3]", wrap);
      var panel = qs(".fp-q3-panel", wrap);
      var text = JSON.parse(wrap.dataset.q3 || "{}");
      tabs.forEach(function (tab) {
        tab.addEventListener("click", function () {
          var key = tab.dataset.q3;
          tabs.forEach(function (t) {
            t.classList.toggle("is-active", t === tab);
          });
          if (panel) panel.textContent = text[key] || "";
        });
      });
      if (tabs[0]) tabs[0].click();
    });
  }

  function onSlideChanged() {
    var idx = Reveal.getIndices().h;
    if ([5, 7].indexOf(idx) >= 0) {
      initCharts();
    }
    if (idx === 5 || idx === 7) initCounters();
  }

  function boot() {
    initLadder();
    initJourney();
    initReadinessChecks();
    initRegChecks();
    initSectorGrid();
    initRiskTable();
    initInvestorPath();
    initLensToggle();
    initQ3Toggle();
    initCharts();
    if (typeof Reveal !== "undefined") {
      Reveal.on("ready", onSlideChanged);
      Reveal.on("slidechanged", onSlideChanged);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();