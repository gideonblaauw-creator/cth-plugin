/* Zidi MEG — vanilla interactions (Reveal + Chart.js). Degrades for print-pdf / decktape. */
(function () {
  "use strict";

  var reduceMotion =
    typeof window !== "undefined" &&
    window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var isPrint =
    /print-pdf/.test(location.search) ||
    /decktape=1/.test(location.search) ||
    document.body.classList.contains("print-pdf") ||
    document.body.classList.contains("deck-static") ||
    reduceMotion;
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

  function initProgrammeGrid() {
    qsa("[data-fp-programme]").forEach(function (wrap) {
      var cards = qsa(".fp-programme-card", wrap);
      var detail = qs(".fp-programme-detail", wrap);
      function pick(i) {
        if (isPrint) return;
        cards.forEach(function (c, j) {
          c.classList.toggle("is-active", j === i);
          c.setAttribute("aria-pressed", j === i ? "true" : "false");
        });
        if (detail) detail.textContent = cards[i].dataset.detail || "";
      }
      if (isPrint) {
        cards.forEach(function (card) {
          card.classList.add("is-active");
        });
        if (detail) detail.textContent = cards.map(function (c) { return c.dataset.detail || ""; }).join(" ");
        return;
      }
      cards.forEach(function (card, i) {
        card.setAttribute("role", "button");
        card.setAttribute("tabindex", "0");
        card.addEventListener("click", function () {
          pick(i);
        });
        card.addEventListener("keydown", function (e) {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            pick(i);
          }
        });
      });
      pick(0);
    });
  }

  function initFlipCards() {
    qsa("[data-fp-flip]").forEach(function (flip) {
      var titleEl = qs(".fp-flip__title", flip);
      var backEl = qs(".fp-flip__face--back", flip);
      var titleText = titleEl ? titleEl.textContent : flip.dataset.flipTitle || "";
      var back = backEl ? backEl.innerHTML : flip.dataset.flipBack || "";

      if (isPrint) {
        if (!qs(".fp-flip__print-pair", flip)) {
          var pair = document.createElement("div");
          pair.className = "fp-flip__print-pair";
          pair.innerHTML =
            '<article><h4>Front</h4><p>' +
            titleText +
            '</p></article><article><h4>Back</h4><p>' +
            back +
            "</p></article>";
          flip.appendChild(pair);
        }
        return;
      }

      function toggle() {
        flip.classList.toggle("is-flipped");
        flip.setAttribute("aria-pressed", flip.classList.contains("is-flipped") ? "true" : "false");
      }
      flip.setAttribute("role", "button");
      flip.setAttribute("tabindex", "0");
      flip.addEventListener("click", toggle);
      flip.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          toggle();
        }
      });
    });
  }

  function initLadder() {
    qsa("[data-fp-ladder]").forEach(function (wrap) {
      var steps = qsa(".fp-ladder-step", wrap);
      var detail = qs(".fp-ladder-detail", wrap);
      function pick(i) {
        if (isPrint) return;
        steps.forEach(function (s, j) {
          s.classList.toggle("is-active", j === i);
          s.setAttribute("aria-pressed", j === i ? "true" : "false");
        });
        if (detail) detail.textContent = steps[i].dataset.detail || "";
      }
      if (isPrint) {
        steps.forEach(function (step) {
          step.classList.add("is-active");
          if (!qs(".fp-ladder-step__print", step)) {
            var p = document.createElement("p");
            p.className = "fp-ladder-step__print";
            p.textContent = step.dataset.detail || "";
            step.appendChild(p);
          }
        });
        if (detail) detail.textContent = "";
        return;
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
      pick(0);
    });
  }

  function initJourney() {
    qsa("[data-fp-journey]").forEach(function (wrap) {
      var nodes = qsa(".fp-journey-node", wrap);
      var panel = qs(".fp-journey-panel", wrap);
      if (isPrint) {
        var stack = qs(".fp-journey-print-stack", wrap);
        if (!stack) {
          stack = document.createElement("div");
          stack.className = "fp-journey-print-stack";
          nodes.forEach(function (n) {
            var block = document.createElement("div");
            block.className = "fp-journey-print-block";
            block.innerHTML = "<strong>" + n.textContent.trim() + "</strong> — " + (n.dataset.panel || "");
            stack.appendChild(block);
          });
          wrap.appendChild(stack);
        }
        nodes.forEach(function (n) {
          n.classList.add("is-active", "is-done");
        });
        if (panel) panel.innerHTML = "";
        return;
      }
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
      pick(0);
    });
  }

  function initChecklist(sel) {
    qsa(sel).forEach(function (list) {
      qsa("li", list).forEach(function (li) {
        li.setAttribute("role", "button");
        li.setAttribute("tabindex", "0");
        if (isPrint) li.classList.add("is-checked");
        function toggle() {
          if (isPrint) return;
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
      var tap = qs(".fp-card__text:not(.fp-sector-detail)", card);
      function open() {
        if (isPrint) return;
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
        if (tap) tap.classList.add("fp-tap-hint");
      }
    });
  }

  function initRiskTable() {
    qsa("[data-fp-risk-table]").forEach(function (table) {
      var noteBar = qs(".fp-risk-note", table.parentElement);
      if (!noteBar) {
        noteBar = document.createElement("p");
        noteBar.className = "fp-risk-note";
        noteBar.setAttribute("aria-live", "polite");
        table.parentElement.appendChild(noteBar);
      }
      qsa("td[data-risk-detail]", table).forEach(function (cell) {
        var detail = cell.dataset.riskDetail || "";
        var note = qs(".fp-risk-cell-note", cell);
        if (note) note.textContent = detail;
        cell.setAttribute("title", detail);
        cell.addEventListener("click", function (e) {
          e.stopPropagation();
          qsa("td[data-risk-detail]", table).forEach(function (c) {
            c.classList.remove("is-detail-open");
          });
          cell.classList.add("is-detail-open");
          if (noteBar) noteBar.textContent = detail;
        });
      });
      if (isPrint) {
        qsa("td[data-risk-detail]", table).forEach(function (cell) {
          cell.classList.add("is-detail-open");
        });
      }
      function clear() {
        qsa("th, td", table).forEach(function (c) {
          c.classList.remove("is-highlight");
        });
      }
      qsa("tbody tr", table).forEach(function (row) {
        row.addEventListener("click", function (e) {
          if (isPrint) return;
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
          if (isPrint) return;
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
      var bands = ["Small angel ticket", "Platform syndicate", "Direct equity"];

      if (isPrint) {
        var grid = qs(".fp-investor-print-grid", wrap);
        if (!grid) {
          grid = document.createElement("div");
          grid.className = "fp-investor-print-grid";
          routes.forEach(function (route, i) {
            var card = document.createElement("article");
            card.className = "fp-investor-print-card";
            card.innerHTML =
              "<h4>" +
              bands[i] +
              "</h4><p>" +
              route +
              "</p><p class=\"fp-investor-trade\">" +
              (trades[i] || "") +
              "</p>";
            grid.appendChild(card);
          });
          wrap.appendChild(grid);
        }
        if (slider) slider.closest(".fp-investor-controls").classList.add("fp-screen-only");
        qs(".fp-investor-panel", wrap).classList.add("fp-screen-only");
        return;
      }

      function sync() {
        var v = slider ? +slider.value : 0;
        qsa(".fp-investor-band", wrap).forEach(function (b, i) {
          b.classList.toggle("is-active", i === v);
        });
        if (routeEl) routeEl.textContent = routes[v] || "";
        if (tradeEl) tradeEl.textContent = trades[v] || "";
      }
      if (slider) slider.addEventListener("input", sync);
      sync();
    });
  }

  function initLensToggle() {
    qsa("[data-fp-lens]").forEach(function (wrap) {
      var diaspora = qs('[data-lens="diaspora"]', wrap);
      var inst = qs('[data-lens="institutional"]', wrap);
      var body = qs(".fp-lens-body", wrap);
      var copy = JSON.parse(wrap.dataset.copy || "{}");

      if (isPrint) {
        var both = qs(".fp-lens-print-both", wrap);
        if (!both) {
          both = document.createElement("div");
          both.className = "fp-lens-print-both";
          both.innerHTML = (copy.diaspora || "") + "<br/><br/>" + (copy.institutional || "");
          wrap.appendChild(both);
        }
        qs(".fp-lens-toggle", wrap).classList.add("fp-screen-only");
        if (body) body.classList.add("fp-screen-only");
        return;
      }

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
      show("diaspora");
    });
  }

  function initRegFlips() {
    /* regulatory flip cards use initFlipCards via data-fp-flip */
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
    if (isPrint) {
      cfg.options = cfg.options || {};
      cfg.options.animation = false;
    }
    chartPool[id] = new Chart(el, cfg);
  }

  var kwhLabels = ["Q1 Oct'24", "Q2", "Q3", "Q4", "Q5", "Q6 Jan'26"];

  function initCharts() {
    if (typeof Chart === "undefined") return;
    Chart.defaults.font.family = "'Open Sans', sans-serif";
    Chart.defaults.color = "#0C498A";

    makeChart("chart-kwh", {
      type: "bar",
      data: {
        labels: kwhLabels,
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
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              afterLabel: function (ctx) {
                if (ctx.dataIndex === 5) return "Partial quarter — grant ended Mar 2026";
                return "";
              },
            },
          },
        },
        scales: {
          x: { grid: { display: false }, ticks: { font: { size: 10, weight: "600" } } },
          y: {
            grid: { color: "#edf2f7" },
            ticks: {
              callback: function (v) {
                return v / 1000 + "k";
              },
              font: { size: 10 },
            },
          },
        },
      },
    });

    makeChart("chart-ev-brands", {
      type: "bar",
      data: {
        labels: ["Tesla", "BYD", "Chery", "MG", "Chevrolet", "Others"],
        datasets: [
          {
            label: "% share (RUNT)",
            data: [48.4, 17.8, 5.2, 4.7, 3.8, 20.1],
            backgroundColor: [B, S, F, G, C, "#c8d9e8"],
            borderRadius: 6,
          },
        ],
      },
      options: {
        indexAxis: "y",
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: {
            grid: { color: "#edf2f7" },
            max: 55,
            ticks: { callback: function (v) { return v + "%"; }, font: { size: 10 } },
          },
          y: { grid: { display: false }, ticks: { font: { size: 11, weight: "600" } } },
        },
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
  }

  function initCounters() {
    qsa("[data-count]").forEach(function (el) {
      var target = +el.dataset.count;
      var suffix = el.dataset.suffix || "";
      if (isPrint || reduceMotion) {
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

      if (isPrint) {
        var dual = qs(".fp-q3-dual", wrap);
        if (!dual) {
          dual = document.createElement("div");
          dual.className = "fp-q3-dual";
          dual.innerHTML =
            '<article class="fp-q3-dual__col"><h4>Scalable (MubOn)</h4><p>' +
            (text.scalable || "") +
            '</p></article><article class="fp-q3-dual__col"><h4>Subsidy-dependent</h4><p>' +
            (text.subsidy || "") +
            "</p></article>";
          wrap.insertBefore(dual, panel);
        }
        qs(".fp-q3-toggle", wrap).classList.add("fp-screen-only");
        if (panel) panel.classList.add("fp-screen-only");
        return;
      }

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
    if (isPrint) document.body.classList.add("deck-static");
    initProgrammeGrid();
    initFlipCards();
    initLadder();
    initJourney();
    initRegFlips();
    initSectorGrid();
    initRiskTable();
    initInvestorPath();
    initLensToggle();
    initQ3Toggle();
    initCharts();
    if (isPrint) {
      initCounters();
    }
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