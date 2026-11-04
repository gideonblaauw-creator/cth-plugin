(function () {
  'use strict';

  var ROWS = [];
  var COVERAGE = {};
  var chart = null;
  var sortKey = 'value_tco2e';
  var sortDir = -1;
  var LOG_MIN = 0;
  var LOG_MAX = 1;
  var LOG_MAX_SLIDER = 1;
  var searchQ = '';

  function uniq(arr) {
    return arr.filter(function (v, i, a) { return a.indexOf(v) === i; }).sort();
  }

  function fmtNum(n) {
    if (n >= 1e6) return (n / 1e6).toLocaleString('en-US', { maximumFractionDigits: 2 }) + 'M';
    if (n >= 1000) return n.toLocaleString('en-US', { maximumFractionDigits: 0 });
    if (n >= 10) return n.toLocaleString('en-US', { maximumFractionDigits: 1 });
    return n.toLocaleString('en-US', { maximumFractionDigits: 2 });
  }

  function esc(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function nexusUrl(slug) {
    return 'https://nexus.cleantechhub.net/s/' + slug;
  }

  function citation(row) {
    if (row.source_kind === 'website' && row.source_url) {
      return { href: row.source_url, label: 'Own website' };
    }
    return { href: '#deck-cards', label: row.source_title || 'Investor deck' };
  }

  function getFilters() {
    return {
      country: document.getElementById('f-country').value,
      sector: document.getElementById('f-sector').value,
      theme: document.getElementById('f-theme').value,
      metric: document.getElementById('f-metric').value,
      source: document.getElementById('f-source').value,
      status: document.getElementById('f-status').value,
      logMin: parseFloat(document.getElementById('f-range-min').value, 10),
      logMax: parseFloat(document.getElementById('f-range-max').value, 10)
    };
  }

  function rowMatches(row, f) {
    if (f.country !== 'all' && row.country !== f.country) return false;
    if (f.sector !== 'all' && row.sector !== f.sector) return false;
    if (f.theme !== 'all' && row.theme !== f.theme) return false;
    if (f.metric !== 'all' && row.metric_type !== f.metric) return false;
    if (f.source !== 'all' && row.source_kind !== f.source) return false;
    if (f.status !== 'all' && row.claim_status !== f.status) return false;
    var minV = Math.pow(10, f.logMin);
    var maxV = Math.pow(10, f.logMax);
    if (row.value_tco2e < minV * 0.999 || row.value_tco2e > maxV * 1.001) return false;
    if (searchQ) {
      var hay = (row.name + ' ' + row.quote + ' ' + row.source_title).toLowerCase();
      if (hay.indexOf(searchQ.toLowerCase()) === -1) return false;
    }
    return true;
  }

  function filteredRows() {
    var f = getFilters();
    return ROWS.filter(function (r) { return rowMatches(r, f); });
  }

  function sumBuckets(rows) {
    var metrics = ['mitigated', 'avoided', 'managed', 'sequestered'];
    var out = { achieved: {}, target: {} };
    metrics.forEach(function (m) {
      out.achieved[m] = 0;
      out.target[m] = 0;
    });
    rows.forEach(function (r) {
      var bucket = r.claim_status === 'target' ? out.target : out.achieved;
      if (bucket[r.metric_type] !== undefined) bucket[r.metric_type] += r.value_tco2e;
    });
    return out;
  }

  function renderCounters(rows) {
    var el = document.getElementById('counter-grid');
    var sums = sumBuckets(rows);
    var metrics = ['mitigated', 'avoided', 'managed', 'sequestered'];
    var html = '';
    ['achieved', 'target'].forEach(function (st) {
      metrics.forEach(function (m) {
        var v = sums[st][m];
        if (!v) return;
        html += '<div class="box ' + (st === 'target' ? 'target' : '') + '">' +
          '<span class="badge-pill ' + st + '">' + st + '</span> ' +
          '<span class="badge-pill">' + m + '</span>' +
          '<b>' + fmtNum(v) + ' t</b>Σ ' + m + ' (' + st + ', filtered)</div>';
      });
    });
    el.innerHTML = html || '<p class="intro">No rows match filters.</p>';
  }

  function groupBySlug(rows) {
    var map = {};
    rows.forEach(function (row) {
      if (!map[row.slug]) {
        map[row.slug] = { slug: row.slug, name: row.name, country: row.country, sector: row.sector, theme: row.theme, claims: [] };
      }
      map[row.slug].claims.push(row);
    });
    return Object.keys(map).map(function (k) { return map[k]; });
  }

  function renderExploreCards(rows) {
    var grid = document.getElementById('startup-grid');
    if (!rows.length) {
      grid.innerHTML = '<p class="imp-empty">No startups match filters.</p>';
      return;
    }
    grid.innerHTML = groupBySlug(rows).map(function (g) {
      var claimHtml = g.claims.map(function (c) {
        var cite = citation(c);
        return '<li><span class="ic">' + esc(c.metric_type) + '</span><span class="iv"><b>' + fmtNum(c.value_tco2e) +
          '</b> tCO₂e<small><span class="badge-pill ' + esc(c.claim_status) + '">' + esc(c.claim_status) +
          '</span> <span class="badge-pill ' + esc(c.source_kind) + '">' + esc(c.source_kind) + '</span></small></span></li>' +
          '<p style="font-size:.82rem;margin:4px 0 0">"' + esc(c.quote) + '"</p>' +
          '<a href="' + esc(cite.href) + '" style="font-size:.78rem"' + (cite.href.indexOf('http') === 0 ? ' target="_blank" rel="noopener"' : '') + '>' + esc(cite.label) + '</a>';
      }).join('');
      return '<div class="imp-theme" style="--tc:#335D4F"><h4><a href="' + nexusUrl(g.slug) + '" target="_blank" rel="noopener">' +
        esc(g.name) + '</a> <span>' + esc(g.country) + '</span></h4><ul class="imp-rows">' + claimHtml + '</ul></div>';
    }).join('');
  }

  function renderChart(rows) {
    var sorted = rows.slice().sort(function (a, b) { return b.value_tco2e - a.value_tco2e; }).slice(0, 24);
    var labels = sorted.map(function (r) { return r.name.length > 18 ? r.name.slice(0, 16) + '…' : r.name; });
    var data = sorted.map(function (r) { return r.value_tco2e; });
    var colors = sorted.map(function (r) {
      var base = r.metric_type === 'managed' ? '#B2EEFA' : r.metric_type === 'mitigated' ? '#9DC384' : r.metric_type === 'sequestered' ? '#669348' : '#69B5FA';
      return r.claim_status === 'target' ? base + '99' : base;
    });
    if (chart) chart.destroy();
    chart = new Chart(document.getElementById('cBars'), {
      type: 'bar',
      data: { labels: labels, datasets: [{ label: 'tCO₂e', data: data, backgroundColor: colors }] },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: { x: { type: 'logarithmic', title: { display: true, text: 'tCO₂e (log scale)' } } }
      }
    });
  }

  function renderTable(rows) {
    var tbody = document.querySelector('#tbl tbody');
    tbody.innerHTML = '';
    var sorted = rows.slice().sort(function (a, b) {
      var av = a[sortKey];
      var bv = b[sortKey];
      if (typeof av === 'number' && typeof bv === 'number') return (av - bv) * sortDir;
      av = String(av).toLowerCase();
      bv = String(bv).toLowerCase();
      if (av < bv) return -sortDir;
      if (av > bv) return sortDir;
      return 0;
    });
    sorted.forEach(function (row) {
      var cite = citation(row);
      var tr = document.createElement('tr');
      tr.innerHTML =
        '<td><a href="' + nexusUrl(row.slug) + '" target="_blank" rel="noopener">' + esc(row.name) + '</a></td>' +
        '<td>' + esc(row.metric_type) + '</td>' +
        '<td><span class="badge-pill ' + esc(row.claim_status) + '">' + esc(row.claim_status) + '</span></td>' +
        '<td><b>' + fmtNum(row.value_tco2e) + '</b></td>' +
        '<td><span class="badge-pill ' + esc(row.source_kind) + '">' + esc(row.source_kind) + '</span></td>' +
        '<td>' + (row.period ? esc(row.period) : '—') + '</td>' +
        '<td>' + esc(row.quote) + '</td>' +
        '<td><a href="' + esc(cite.href) + '" target="_blank" rel="noopener">' + esc(cite.label) + '</a></td>';
      tbody.appendChild(tr);
    });
    document.getElementById('count').textContent = sorted.length + ' row(s)';
  }

  function renderDeckCards() {
    var deckRows = ROWS.filter(function (r) { return r.source_kind === 'investor_deck'; });
    var bySlug = {};
    deckRows.forEach(function (r) {
      if (!bySlug[r.slug] || r.value_tco2e > bySlug[r.slug].value_tco2e) bySlug[r.slug] = r;
    });
    var grid = document.getElementById('deck-card-grid');
    grid.innerHTML = '';
    Object.keys(bySlug).sort().forEach(function (slug) {
      var r = bySlug[slug];
      var card = document.createElement('article');
      card.className = 'deck-card';
      card.id = 'deck-card-' + slug;
      card.innerHTML =
        '<h3><a href="' + nexusUrl(slug) + '" target="_blank" rel="noopener">' + esc(r.name) + '</a></h3>' +
        '<p class="meta">' + esc(r.country) + ' · ' + esc(r.sector) + ' · ' + esc(r.theme) + '</p>' +
        '<p class="amt">' + fmtNum(r.value_tco2e) + ' tCO₂e <span class="badge-pill ' + esc(r.claim_status) + '">' + esc(r.claim_status) + '</span> <span class="badge-pill">' + esc(r.metric_type) + '</span></p>' +
        (r.period ? '<p class="meta">Period: ' + esc(r.period) + '</p>' : '') +
        '<blockquote>' + esc(r.quote) + '</blockquote>' +
        '<p class="src">Source: ' + esc(r.source_title) + '</p>';
      grid.appendChild(card);
    });
  }

  function renderHero() {
    document.getElementById('hs-figures').textContent = String(ROWS.length);
    document.getElementById('hs-startups').textContent = String(uniq(ROWS.map(function (r) { return r.slug; })).length);
    var deckSlugs = uniq(ROWS.filter(function (r) { return r.source_kind === 'investor_deck'; }).map(function (r) { return r.slug; }));
    document.getElementById('hs-decks').textContent = String(deckSlugs.length);
  }

  function renderCoverage() {
    var el = document.getElementById('cov-stats');
    var reporting = uniq(ROWS.map(function (r) { return r.slug; })).length;
    el.innerHTML =
      '<div class="stat"><b>' + COVERAGE.portfolio + '</b><span>Portfolio startups</span></div>' +
      '<div class="stat"><b>' + COVERAGE.websitesChecked + '</b><span>Websites checked</span></div>' +
      '<div class="stat"><b>' + COVERAGE.noWebsite + '</b><span>No website URL</span></div>' +
      '<div class="stat"><b>' + COVERAGE.unreachable + '</b><span>Sites unreachable (~)</span></div>' +
      '<div class="stat"><b>' + (COVERAGE.decksInManifest || 47) + '</b><span>Decks in manifest</span></div>' +
      '<div class="stat"><b>' + reporting + '</b><span>Startups in this deck</span></div>' +
      '<div class="stat"><b>' + ROWS.length + '</b><span>Total claim rows</span></div>';
  }

  function syncRangeLabels() {
    var f = getFilters();
    document.getElementById('range-lbl').textContent = fmtNum(Math.pow(10, f.logMin)) + ' – ' + fmtNum(Math.pow(10, f.logMax)) + ' t';
  }

  function refresh() {
    var rows = filteredRows();
    renderCounters(rows);
    renderExploreCards(rows);
    renderChart(rows);
    renderTable(rows);
    syncRangeLabels();
  }

  function initFilters() {
    ['country', 'sector', 'theme', 'metric_type'].forEach(function (field) {
      var id = field === 'metric_type' ? 'f-metric' : 'f-' + field.replace('_type', '');
      var sel = document.getElementById(id);
      uniq(ROWS.map(function (r) { return r[field === 'metric_type' ? 'metric_type' : field]; })).forEach(function (v) {
        var opt = document.createElement('option');
        opt.value = v;
        opt.textContent = v;
        sel.appendChild(opt);
      });
    });
    var rMin = document.getElementById('f-range-min');
    var rMax = document.getElementById('f-range-max');
    rMin.min = rMax.min = String(LOG_MIN);
    rMin.max = rMax.max = String(LOG_MAX_SLIDER);
    rMin.step = rMax.step = '0.001';
    rMin.value = String(LOG_MIN);
    rMax.value = String(LOG_MAX_SLIDER);
    ['f-country', 'f-sector', 'f-theme', 'f-metric', 'f-source', 'f-status', 'f-range-min', 'f-range-max'].forEach(function (id) {
      document.getElementById(id).addEventListener('input', function () {
        var f = getFilters();
        if (f.logMin > f.logMax) {
          if (id === 'f-range-min') document.getElementById('f-range-max').value = rMin.value;
          else document.getElementById('f-range-min').value = rMax.value;
        }
        refresh();
      });
    });
    document.getElementById('btn-reset').addEventListener('click', function () {
      document.getElementById('f-country').value = 'all';
      document.getElementById('f-sector').value = 'all';
      document.getElementById('f-theme').value = 'all';
      document.getElementById('f-metric').value = 'all';
      document.getElementById('f-source').value = 'all';
      document.getElementById('f-status').value = 'all';
      rMin.value = String(LOG_MIN);
      rMax.value = String(LOG_MAX_SLIDER);
      searchQ = '';
      document.getElementById('q').value = '';
      refresh();
    });
    document.getElementById('q').addEventListener('input', function (e) {
      searchQ = e.target.value;
      refresh();
    });
    document.querySelectorAll('#tbl th[data-sort]').forEach(function (th) {
      th.addEventListener('click', function () {
        var key = th.getAttribute('data-sort');
        if (sortKey === key) sortDir *= -1;
        else { sortKey = key; sortDir = key === 'value_tco2e' ? -1 : 1; }
        renderTable(filteredRows());
      });
    });
  }

  function initNav() {
    var burger = document.getElementById('burger');
    var nav = document.getElementById('nav');
    if (burger && nav) {
      burger.addEventListener('click', function () { nav.classList.toggle('open'); });
    }
  }

  function boot(data) {
    ROWS = data.rows;
    COVERAGE = data.coverage || {};
    var vals = ROWS.map(function (r) { return r.value_tco2e; });
    LOG_MIN = Math.log10(Math.min.apply(null, vals));
    LOG_MAX = Math.log10(Math.max.apply(null, vals));
    LOG_MAX_SLIDER = Math.ceil(LOG_MAX * 100) / 100;
    renderHero();
    renderCoverage();
    renderDeckCards();
    initFilters();
    initNav();
    refresh();
  }

  fetch('data/co2.json')
    .then(function (r) { return r.json(); })
    .then(boot)
    .catch(function (err) {
      console.error(err);
      document.body.insertAdjacentHTML('afterbegin', '<p style="padding:20px;color:red">Load data/co2.json via http server (run ./build.sh then python3 -m http.server).</p>');
    });
})();
