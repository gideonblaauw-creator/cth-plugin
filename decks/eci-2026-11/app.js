(function () {
  "use strict";

  var sections = [].slice.call(document.querySelectorAll("section[id].deck-section"));
  var nav = document.getElementById("nav");
  var navLinks = document.querySelectorAll("#nav a[href^='#']");
  var burger = document.getElementById("burger");

  if (sections.length && navLinks.length && "IntersectionObserver" in window) {
    var obs = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          var id = en.target.id;
          navLinks.forEach(function (a) {
            a.classList.toggle("act", a.getAttribute("href") === "#" + id);
          });
        });
      },
      { rootMargin: "-42% 0px -42% 0px", threshold: 0 }
    );
    sections.forEach(function (s) {
      obs.observe(s);
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

  function animateCount(el, target, ms, suffix) {
    suffix = suffix || "";
    var start = 0;
    var t0 = performance.now();
    function frame(now) {
      var p = Math.min(1, (now - t0) / ms);
      var v = Math.floor(start + (target - start) * p);
      el.textContent = String(v) + suffix;
      if (p < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  document.querySelectorAll(".stat .num[data-count]").forEach(function (el) {
    var t = parseInt(el.getAttribute("data-count"), 10);
    if (!isNaN(t)) {
      var suf = el.getAttribute("data-suffix");
      suf = suf === null ? "" : suf;
      animateCount(el, t, 1100, suf);
    }
  });

  if (typeof Chart === "undefined") return;

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

  var ST_ORDER = ["cohort", "national", "semi", "regional", "global"];
  var ST_ES = {
    cohort: "Cohort / bootcamp",
    national: "Final nacional",
    semi: "Semifinal regional",
    regional: "Final regional Américas",
    global: "Final global (Singapur)",
  };

  function fetchJson(url) {
    return fetch(url).then(function (r) {
      if (!r.ok) throw new Error("fetch " + url + " " + r.status);
      return r.json();
    });
  }

  fetchJson("data/startups.json")
    .then(function (d) {
      var startups = d.startups || [];
      var themeLabels = d.themes || {};

      /* ---- Por país (solo data/startups.json) ---- */
      var byCc = {};
      startups.forEach(function (s) {
        var cc = s.cc || "?";
        byCc[cc] = (byCc[cc] || 0) + 1;
      });
      var priority = ["CO", "PE", "SV", "CR", "GT"];
      var ccs = Object.keys(byCc);
      ccs.sort(function (a, b) {
        var ia = priority.indexOf(a);
        var ib = priority.indexOf(b);
        if (ia === -1 && ib === -1) return (CC_ES[a] || a).localeCompare(CC_ES[b] || b, "es");
        if (ia === -1) return 1;
        if (ib === -1) return -1;
        return ia - ib;
      });
      var labelsCountry = ccs.map(function (cc) {
        return CC_ES[cc] || cc;
      });
      var dataCountry = ccs.map(function (cc) {
        return byCc[cc];
      });
      var bgCountry = ccs.map(function (_, i) {
        return COL[i % COL.length];
      });

      var c1 = document.getElementById("cCountry");
      if (c1) {
        new Chart(c1, {
          type: "bar",
          data: {
            labels: labelsCountry,
            datasets: [
              {
                label: "Startups en cartera (data/startups.json)",
                data: dataCountry,
                backgroundColor: bgCountry,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: "y",
            plugins: {
              legend: { display: false },
            },
            scales: {
              x: { beginAtZero: true, ticks: { precision: 0 } },
            },
          },
        });
      }

      /* ---- Embudo por etapa ---- */
      var bySt = {};
      ST_ORDER.forEach(function (k) {
        bySt[k] = 0;
      });
      startups.forEach(function (s) {
        var st = s.stage;
        if (st && bySt.hasOwnProperty(st)) bySt[st] += 1;
      });
      var labelsF = ST_ORDER.map(function (k) {
        return ST_ES[k] || k;
      });
      var dataF = ST_ORDER.map(function (k) {
        return bySt[k];
      });

      var c2 = document.getElementById("cFunnel");
      if (c2) {
        new Chart(c2, {
          type: "bar",
          data: {
            labels: labelsF,
            datasets: [
              {
                label: "Startups",
                data: dataF,
                backgroundColor: "#0C498A",
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { display: false },
            },
            scales: {
              y: { ticks: { autoSkip: false, maxRotation: 65, minRotation: 0, font: { size: 10 } } },
              x: { beginAtZero: true, ticks: { precision: 0 } },
            },
          },
        });
      }

      /* ---- Temáticas (solo filas con theme en JSON) ---- */
      var byTh = {};
      startups.forEach(function (s) {
        if (!s.theme) return;
        byTh[s.theme] = (byTh[s.theme] || 0) + 1;
      });
      var thKeys = Object.keys(byTh).sort(function (a, b) {
        return byTh[b] - byTh[a];
      });
      var labelsTh = thKeys.map(function (k) {
        var pair = themeLabels[k];
        return Array.isArray(pair) ? pair[1] || pair[0] : k;
      });
      var dataTh = thKeys.map(function (k) {
        return byTh[k];
      });
      var bgTh = thKeys.map(function (_, i) {
        return COL[i % COL.length];
      });

      var c3 = document.getElementById("cTheme");
      if (c3 && dataTh.length) {
        new Chart(c3, {
          type: "doughnut",
          data: {
            labels: labelsTh,
            datasets: [
              {
                data: dataTh,
                backgroundColor: bgTh,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: "bottom",
                labels: { font: { size: 10 }, color: "#1a2b3a" },
              },
            },
          },
        });
      } else if (c3) {
        var ctx = c3.getContext("2d");
        ctx.font = "14px sans-serif";
        ctx.fillStyle = "#5f6b75";
        ctx.fillText("Sin campo theme en los registros", 10, 80);
      }
    })
    .catch(function () {
      console.warn("eci deck: no se pudo cargar data/startups.json");
    });
})();
