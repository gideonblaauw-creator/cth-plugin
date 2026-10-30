(function () {
  'use strict';
  const C = { blue: '#0C498A', cyan: '#B2EEFA', lgreen: '#9DC384', green: '#669348', sky: '#69B5FA' };
  let EO = null;

  function esc(s) {
    return String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  }

  document.getElementById('burger').onclick = () => document.getElementById('nav').classList.toggle('open');
  document.querySelectorAll('#nav a').forEach((a) => {
    a.onclick = () => document.getElementById('nav').classList.remove('open');
  });

  const sections = [...document.querySelectorAll('section[id]')];
  const navLinks = [...document.querySelectorAll('#nav a[href^="#"]')];
  if ('IntersectionObserver' in window && navLinks.length) {
    const ioNav = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (!e.isIntersecting) return;
          const id = e.target.id;
          navLinks.forEach((l) => l.classList.toggle('act', l.getAttribute('href') === '#' + id));
        });
      },
      { rootMargin: '-40% 0px -45% 0px', threshold: 0 }
    );
    sections.forEach((s) => ioNav.observe(s));
  }

  const ioCount = new IntersectionObserver(
    (es) =>
      es.forEach((e) => {
        if (!e.isIntersecting) return;
        const el = e.target;
        const n = +el.dataset.count;
        const suffix = el.dataset.suffix || '';
        const st = performance.now();
        (function f(ts) {
          const p = Math.min(1, (ts - st) / 900);
          el.textContent = Math.round(n * p) + suffix;
          if (p < 1) requestAnimationFrame(f);
          else ioCount.unobserve(el);
        })(st);
      }),
    { threshold: 0.4 }
  );
  document.querySelectorAll('[data-count]').forEach((el) => ioCount.observe(el));

  function bindTabs() {
    const tabs = document.querySelectorAll('#lensTabs button');
    const panel = document.getElementById('lensPanel');
    if (!tabs.length || !panel || !EO) return;
    const urbanaExtra =
      ' No monta red de estaciones; adoptante <span class="pendiente">sin evidencia</span> en fuente fechada.';
    tabs.forEach((btn) => {
      btn.onclick = () => {
        tabs.forEach((b) => b.classList.remove('on'));
        btn.classList.add('on');
        const lens = EO.lenses.find((x) => x.id === btn.dataset.lens);
        if (!lens) return;
        let body = esc(lens.body);
        if (lens.id === 'urbana') body += urbanaExtra;
        panel.innerHTML = '<h3>' + esc(lens.title) + '</h3><p>' + body + '</p>';
      };
    });
  }

  function bindLevelSlider() {
    const sl = document.getElementById('levelSlider');
    const pan = document.getElementById('levelPanel');
    if (!sl || !pan || !EO) return;
    const sync = () => {
      pan.innerHTML = EO.levels[sl.value];
      sl.setAttribute('aria-valuetext', 'L' + sl.value);
    };
    sl.oninput = sync;
    sync();
  }

  function bindPhaseSlider() {
    const sl = document.getElementById('phaseSlider');
    const pan = document.getElementById('phasePanel');
    if (!sl || !pan || !EO) return;
    const sync = () => {
      const d = EO.phases[sl.value];
      pan.innerHTML = '<strong>' + esc(d.title) + '</strong><br>' + esc(d.body);
      document.querySelectorAll('[data-phase]').forEach((c) => c.classList.toggle('on', c.dataset.phase === sl.value));
    };
    sl.oninput = sync;
    sync();
  }

  function bindEnvTable() {
    const tbody = document.querySelector('#envTable tbody');
    if (!tbody) return;
    document.querySelectorAll('#envTable th.sortable').forEach((th) => {
      th.onclick = () => {
        const key = th.dataset.sort;
        const asc = th.dataset.asc !== 'true';
        th.dataset.asc = asc;
        const rows = [...tbody.querySelectorAll('tr')];
        rows.sort((a, b) => {
          if (key === 'days') return (asc ? 1 : -1) * (Number(a.dataset.days) - Number(b.dataset.days));
          const ta = a.children[1].textContent.trim();
          const tb = b.children[1].textContent.trim();
          return (asc ? 1 : -1) * ta.localeCompare(tb, 'es');
        });
        rows.forEach((r) => tbody.appendChild(r));
      };
    });
  }

  function initCharts() {
    if (!window.Chart || !EO) return;
    const cols = [C.blue, C.green, C.lgreen, C.cyan, C.sky];
    const s = EO.charts.structure;
    new Chart(document.getElementById('chartStructure'), {
      type: 'bar',
      data: {
        labels: s.labels,
        datasets: [{ label: 'Conteo (WP)', data: s.data, backgroundColor: cols }]
      },
      options: {
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }
      }
    });
    const p = EO.charts.procolombia;
    new Chart(document.getElementById('chartProcolombia'), {
      type: 'bar',
      data: {
        labels: [p.label],
        datasets: [{ label: 'ProColombia + GGGI (7 ene 2026)', data: [p.value], backgroundColor: C.green }]
      },
      options: { plugins: { legend: { display: true } }, scales: { y: { beginAtZero: true } } }
    });
  }

  bindEnvTable();

  fetch('data/eo-deck.json')
    .then((r) => r.json())
    .then((d) => {
      EO = d;
      bindTabs();
      bindLevelSlider();
      bindPhaseSlider();
      initCharts();
    })
    .catch(() => {});
})();
