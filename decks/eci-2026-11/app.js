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

  function animateCount(el, target, ms) {
    var start = 0;
    var t0 = performance.now();
    function frame(now) {
      var p = Math.min(1, (now - t0) / ms);
      var v = Math.floor(start + (target - start) * p);
      el.textContent = String(v);
      if (p < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  document.querySelectorAll(".stat .num[data-count]").forEach(function (el) {
    var t = parseInt(el.getAttribute("data-count"), 10);
    if (!isNaN(t)) animateCount(el, t, 1100);
  });

  if (typeof Chart === "undefined") return;

  var common = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "bottom",
        labels: { font: { size: 11 }, color: "#1a2b3a" },
      },
    },
  };

  var c1 = document.getElementById("cCountry");
  if (c1) {
    new Chart(c1, {
      type: "bar",
      data: {
        labels: ["Colombia", "Perú", "Guatemala", "El Salvador", "Costa Rica"],
        datasets: [
          {
            label: "Participación (ilustrativo · alinear al deck CLP26 en producción)",
            data: [312, 198, 145, 112, 80],
            backgroundColor: ["#0C498A", "#69B5FA", "#9DC384", "#669348", "#B2EEFA"],
          },
        ],
      },
      options: Object.assign({}, common, { indexAxis: "y" }),
    });
  }

  var c2 = document.getElementById("cFunnel");
  if (c2) {
    new Chart(c2, {
      type: "bar",
      data: {
        labels: ["Ideas", "Bootcamp", "Nacionales", "Regional", "Global"],
        datasets: [
          {
            label: "Embudo (ilustrativo · alinear al deck CLP26 en producción)",
            data: [847, 412, 84, 18, 5],
            backgroundColor: "#0C498A",
          },
        ],
      },
      options: common,
    });
  }

  var c3 = document.getElementById("cTheme");
  if (c3) {
    new Chart(c3, {
      type: "doughnut",
      data: {
        labels: ["Energía", "Economía circular", "Agua", "Alimentación", "Otros"],
        datasets: [
          {
            data: [28, 22, 18, 14, 18],
            backgroundColor: ["#0C498A", "#69B5FA", "#9DC384", "#669348", "#B2EEFA"],
          },
        ],
      },
      options: common,
    });
  }
})();
