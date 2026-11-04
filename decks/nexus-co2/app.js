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

  var IMPACT_LABELS = ['Self-reported', 'Target', 'Evaluated'];
  var METRICS = ['mitigated', 'avoided', 'managed', 'sequestered'];

  var FLAGS = { CO: '🇨🇴', ES: '🇪🇸', BO: '🇧🇴', CL: '🇨🇱', US: '🇺🇸' };

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

  function themeCode(theme) {
    if (theme === 'Bioeconomy') return { cls: 'bt-BIO', short: 'BIO' };
    if (theme === 'Energy') return { cls: 'bt-EN', short: 'EN' };
    return { cls: 'bt-CE', short: 'CE' };
  }

  function sectorBadgeClass(sector) {
    var m = /^CT-([A-Z]{2})-/i.exec(sector || '');
    if (!m) return 'bt-ct-xs';
    return 'bt-ct-' + m[1].toLowerCase();
  }

  function metricColor(metric) {
    if (metric === 'managed') return '#B2EEFA';
    if (metric === 'mitigated') return '#9DC384';
    if (metric === 'sequestered') return '#669348';
    return '#69B5FA';
  }

  function labelSlug(label) {
    return label.toLowerCase().replace(/[^a-z]+/g, '-');
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
      label: document.getElementById('f-label').value,
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
    if (f.label !== 'all' && row.impact_label !== f.label) return false;
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
    return ROWS.filter(function (r) { return rowMatches(r, getFilters()); });
  }

  function sumByLabelAndMetric(rows) {
    var out = {};
    IMPACT_LABELS.forEach(function (lb) {
      out[lb] = {};
      METRICS.forEach(function (m) { out[lb][m] = 0; });
    });
    rows.forEach(function (r) {
      if (out[r.impact_label] && out[r.impact_label][r.metric_type] !== undefined) {
        out[r.impact_label][r.metric_type] += r.value_tco2e;
      }
    });
    return out;
  }

  function renderCounters(rows) {
    var el = document.getElementById('counter-grid');
    var sums = sumByLabelAndMetric(rows);
    var html = '';
    IMPACT_LABELS.forEach(function (lb) {
      METRICS.forEach(function (m) {
        var v = sums[lb][m];
        if (!v) return;
        html += '<div class="box lbl-' + labelSlug(lb) + '">' +
          '<span class="lbl-badge lb-' + labelSlug(lb) + '">' + esc(lb) + '</span> ' +
          '<span class="lbl-badge lb-metric">' + esc(m) + '</span>' +
          '<b>' + fmtNum(v) + ' t</b>Σ ' + esc(m) + ' · ' + esc(lb) + ' (filtered)</div>';
      });
    });
    el.innerHTML = html || '<p class="intro">No rows match filters.</p>';
  }

  function claimBlock(c) {
    var cite = citation(c);
    var period = c.period ? '<span class="co2-period">' + esc(c.period) + '</span>' : '';
    return '<div class="co2-claim">' +
      '<div class="co2-head">' +
      '<span class="lbl-badge lb-' + labelSlug(c.impact_label) + '">' + esc(c.impact_label) + '</span>' +
      '<span class="co2-amt">' + fmtNum(c.value_tco2e) + ' tCO₂e</span>' +
      '<span class="lbl-badge lb-metric">' + esc(c.metric_type) + '</span>' + period +
      '</div>' +
      '<p class="co2-quote">“' + esc(c.quote) + '”</p>' +
      '<p class="co2-src">' + esc(c.source_kind === 'website' ? 'Website' : 'Deck') + ' · ' +
      '<a href="' + esc(cite.href) + '"' + (cite.href.indexOf('http') === 0 ? ' target="_blank" rel="noopener"' : '') + '>' + esc(cite.label) + '</a></p>' +
      '</div>';
  }

  function nexusStartupCard(g, claims, descOverride) {
    var th = themeCode(g.theme);
    var flag = FLAGS[g.country] || '🌐';
    var desc = descOverride || (claims[0] ? claims[0].quote : '');
    if (desc.length > 140) desc = desc.slice(0, 137) + '…';
    return '<article class="nx-card">' +
      '<div class="nx-cb" style="background:var(--deep-blue)"></div>' +
      '<div class="nx-logo" aria-hidden="true">' + flag + '</div>' +
      '<div class="nx-ct"><div class="nx-cn"><a href="' + nexusUrl(g.slug) + '" target="_blank" rel="noopener">' + esc(g.name) + '</a></div></div>' +
      '<p class="nx-cd">' + esc(desc) + '</p>' +
      '<div class="nx-cbot">' +
      '<span class="nx-badge ' + th.cls + '">' + th.short + '</span>' +
      '<span class="nx-badge ' + sectorBadgeClass(g.sector) + '">' + esc(g.sector) + '</span>' +
      '<span class="nx-badge bs-PS">' + esc(g.country) + '</span>' +
      '<a class="nexus-btn" href="' + nexusUrl(g.slug) + '" target="_blank" rel="noopener">Nexus ↗</a>' +
      '</div>' +
      claims.map(claimBlock).join('') +
      '</article>';
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
      return nexusStartupCard(g, g.claims);
    }).join('');
  }

  function renderChartLegend(rows) {
    var el = document.getElementById('chart-legend');
    if (!el) return;
    var counts = {};
    IMPACT_LABELS.forEach(function (lb) { counts[lb] = 0; });
    rows.forEach(function (r) { counts[r.impact_label] = (counts[r.impact_label] || 0) + 1; });
    el.innerHTML = IMPACT_LABELS.map(function (lb) {
      return '<span class="leg-item"><span class="leg-swatch lb-' + labelSlug(lb) + '"></span>' + esc(lb) + ' (' + counts[lb] + ')</span>';
    }).join('') + '<span class="leg-note">Bar fill = metric type · border = impact label</span>';
  }

  function renderChart(rows) {
    var sorted = rows.slice().sort(function (a, b) { return b.value_tco2e - a.value_tco2e; }).slice(0, 24);
    var labels = sorted.map(function (r) { return r.name.length > 18 ? r.name.slice(0, 16) + '…' : r.name; });
    var data = sorted.map(function (r) { return r.value_tco2e; });
    var colors = sorted.map(function (r) { return metricColor(r.metric_type); });
    var borders = sorted.map(function (r) {
      if (r.impact_label === 'Target') return '#FF6633';
      if (r.impact_label === 'Evaluated') return '#6A1B9A';
      return '#0C498A';
    });
    var borderWidths = sorted.map(function (r) { return r.impact_label === 'Self-reported' ? 1 : 3; });
    if (chart) chart.destroy();
    chart = new Chart(document.getElementById('cBars'), {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'tCO₂e',
          data: data,
          backgroundColor: colors,
          borderColor: borders,
          borderWidth: borderWidths
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            labels: {
              generateLabels: function () {
                return [
                  { text: 'Self-reported (solid border)', fillStyle: '#69B5FA', strokeStyle: '#0C498A', lineWidth: 1 },
                  { text: 'Target (orange border)', fillStyle: '#69B5FA', strokeStyle: '#FF6633', lineWidth: 3 },
                  { text: 'Evaluated (purple border)', fillStyle: '#69B5FA', strokeStyle: '#6A1B9A', lineWidth: 3 }
                ];
              }
            }
          }
        },
        scales: { x: { type: 'logarithmic', title: { display: true, text: 'tCO₂e (log scale)' } } }
      }
    });
    renderChartLegend(rows);
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
        '<td><span class="lbl-badge lb-' + labelSlug(row.impact_label) + '">' + esc(row.impact_label) + '</span></td>' +
        '<td><b>' + fmtNum(row.value_tco2e) + '</b></td>' +
        '<td><span class="lbl-badge lb-source">' + esc(row.source_kind) + '</span></td>' +
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
      if (!bySlug[r.slug]) bySlug[r.slug] = { slug: r.slug, name: r.name, country: r.country, sector: r.sector, theme: r.theme, claims: [] };
      bySlug[r.slug].claims.push(r);
    });
    var grid = document.getElementById('deck-card-grid');
    grid.innerHTML = Object.keys(bySlug).sort().map(function (slug) {
      var g = bySlug[slug];
      var top = g.claims.slice().sort(function (a, b) { return b.value_tco2e - a.value_tco2e; })[0];
      return nexusStartupCard(g, [top], 'Investor deck · ' + (top.source_title || ''));
    }).join('');
  }

  function renderHero() {
    document.getElementById('hs-figures').textContent = String(ROWS.length);
    document.getElementById('hs-startups').textContent = String(uniq(ROWS.map(function (r) { return r.slug; })).length);
    var deckSlugs = uniq(ROWS.filter(function (r) { return r.source_kind === 'investor_deck'; }).map(function (r) { return r.slug; }));
    document.getElementById('hs-decks').textContent = String(deckSlugs.length);
    var lc = document.getElementById('hs-labels');
    if (lc) {
      var c = {};
      ROWS.forEach(function (r) { c[r.impact_label] = (c[r.impact_label] || 0) + 1; });
      lc.textContent = IMPACT_LABELS.map(function (lb) { return lb + ' ' + (c[lb] || 0); }).join(' · ');
    }
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
    ['f-country', 'f-sector', 'f-theme', 'f-metric', 'f-source', 'f-label', 'f-range-min', 'f-range-max'].forEach(function (id) {
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
      document.getElementById('f-label').value = 'all';
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
    if (burger && nav) burger.addEventListener('click', function () { nav.classList.toggle('open'); });
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
