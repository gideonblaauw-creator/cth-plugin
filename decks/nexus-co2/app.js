(function () {
  'use strict';

  /** @type {Array<Record<string, string|number>>} */
  var ROWS = [
    { slug: 'bio-natural-solutions', name: 'BIO NATURAL SOLUTIONS', country: 'CO', sector: 'CT-AF-010', theme: 'Bioeconomy', metric_type: 'mitigated', value_tco2e: 7500, period: '', quote: '+7500 TM CO2 mitigadas', source_url: 'https://bionatsolutions.com/' },
    { slug: 'bio-natural-solutions', name: 'BIO NATURAL SOLUTIONS', country: 'CO', sector: 'CT-AF-010', theme: 'Bioeconomy', metric_type: 'mitigated', value_tco2e: 4500, period: '', quote: 'Evitamos emisiones asociadas al uso de agroquímicos sintéticos y al desperdicio de alimentos, mitigando +4500 TM de CO2.', source_url: 'https://bionatsolutions.com/' },
    { slug: 'batx', name: 'BATX SAS', country: 'CO', sector: 'CT-EN-004', theme: 'Energy', metric_type: 'avoided', value_tco2e: 520, period: '', quote: 'Evitado 520 toneladas de CO₂ equivalentes a la fabricación de baterías de primera vida.', source_url: 'https://www.batx.co/impacto-1' },
    { slug: 'ciclorganicos', name: 'CICLORGÁNICOS (BIO ABONOS GAIA)', country: 'CO', sector: 'CT-WA-002', theme: 'Bioeconomy', metric_type: 'avoided', value_tco2e: 25000, period: '2019-2026', quote: '+25.000 t de CO₂ eq evitadas', source_url: 'https://ciclorganicos.com/' },
    { slug: 'kimsa', name: 'CARBON BOX', country: 'CO', sector: 'CT-IC-002', theme: 'Energy', metric_type: 'managed', value_tco2e: 13000, period: '', quote: '13000+ Toneladas de gases efecto invernadero gestionadas', source_url: 'https://www.kimsa.co/tecnologia-para-la-naturaleza' },
    { slug: 'carbonbox', name: 'CARBONBOX', country: 'CO', sector: 'CT-XS-001', theme: 'Energy', metric_type: 'managed', value_tco2e: 112000, period: '', quote: '112K+ tCO₂e gestionadas', source_url: 'https://carbonbox.app/' },
    { slug: 'o3-smart-cities', name: 'O3 SMART CITIES', country: 'CO', sector: 'CT-EN-001', theme: 'Energy', metric_type: 'avoided', value_tco2e: 1500, period: '', quote: '1.500+ t CO₂ evitadas', source_url: 'https://o3smartcities.com.co' },
    { slug: 'seos-energy', name: 'SEOS ENERGY SAS BIC', country: 'CO', sector: 'CT-XS-003', theme: 'Energy', metric_type: 'avoided', value_tco2e: 645, period: '', quote: '645 toneladas de CO₂ evitadas', source_url: 'https://seosenergy.co/' },
    { slug: 'zhana-solutions', name: 'ZHANA SOLUTIONS', country: 'CO', sector: 'CT-WW-002', theme: 'Circular', metric_type: 'avoided', value_tco2e: 2.73, period: '', quote: 'Toneladas de reducción CO2', source_url: 'https://zhanasolutions.com/' }
  ];

  var COVERAGE = {
    portfolio: 174,
    websitesChecked: 126,
    noWebsite: 48,
    unreachable: 22
  };

  var VALUE_MIN = Math.min.apply(null, ROWS.map(function (r) { return r.value_tco2e; }));
  var VALUE_MAX = Math.max.apply(null, ROWS.map(function (r) { return r.value_tco2e; }));
  var LOG_MIN = Math.log10(VALUE_MIN);
  var LOG_MAX = Math.log10(VALUE_MAX);
  /** Inclusive upper log bound so range input step does not drop the largest claim. */
  var LOG_MAX_SLIDER = Math.ceil(LOG_MAX * 100) / 100;

  function uniq(arr) {
    return arr.filter(function (v, i, a) { return a.indexOf(v) === i; }).sort();
  }

  function fmtNum(n) {
    if (n >= 1000) return n.toLocaleString('en-US', { maximumFractionDigits: 0 });
    if (n >= 10) return n.toLocaleString('en-US', { maximumFractionDigits: 1 });
    return n.toLocaleString('en-US', { maximumFractionDigits: 2 });
  }

  function nexusUrl(slug) {
    return 'https://nexus.cleantechhub.net/s/' + slug;
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

  function getFilters() {
    return {
      country: document.getElementById('f-country').value,
      sector: document.getElementById('f-sector').value,
      theme: document.getElementById('f-theme').value,
      metric: document.getElementById('f-metric').value,
      logMin: parseFloat(document.getElementById('f-range').value, 10),
      logMax: parseFloat(document.getElementById('f-range-max').value, 10)
    };
  }

  function rowMatches(row, f) {
    if (f.country !== 'all' && row.country !== f.country) return false;
    if (f.sector !== 'all' && row.sector !== f.sector) return false;
    if (f.theme !== 'all' && row.theme !== f.theme) return false;
    if (f.metric !== 'all' && row.metric_type !== f.metric) return false;
    var minV = Math.pow(10, f.logMin);
    var maxV = Math.pow(10, f.logMax);
    if (row.value_tco2e < minV * 0.999 || row.value_tco2e > maxV * 1.001) return false;
    return true;
  }

  function filteredRows() {
    var f = getFilters();
    return ROWS.filter(function (r) { return rowMatches(r, f); });
  }

  function sumByMetric(rows) {
    var out = { mitigated: 0, avoided: 0, managed: 0 };
    rows.forEach(function (r) {
      if (out[r.metric_type] !== undefined) out[r.metric_type] += r.value_tco2e;
    });
    return out;
  }

  function updateCounters(rows) {
    var startups = uniq(rows.map(function (r) { return r.slug; })).length;
    var sums = sumByMetric(rows);
    document.getElementById('c-startups').textContent = String(startups);
    document.getElementById('c-claims').textContent = String(rows.length);
    document.getElementById('c-mitigated').textContent = fmtNum(sums.mitigated) + ' t';
    document.getElementById('c-avoided').textContent = fmtNum(sums.avoided) + ' t';
    document.getElementById('c-managed').textContent = fmtNum(sums.managed) + ' t';
  }

  function renderCards(rows) {
    var grid = document.getElementById('startup-grid');
    if (!grid) return;
    grid.innerHTML = '';
    var groups = groupBySlug(rows);
    groups.forEach(function (g) {
      var card = document.createElement('article');
      card.className = 'startup-card';
      var h = document.createElement('h3');
      var link = document.createElement('a');
      link.href = nexusUrl(g.slug);
      link.target = '_blank';
      link.rel = 'noopener';
      link.textContent = g.name;
      h.appendChild(link);
      card.appendChild(h);
      var meta = document.createElement('p');
      meta.className = 'meta';
      meta.textContent = g.country + ' · ' + g.sector + ' · ' + g.theme;
      card.appendChild(meta);
      g.claims.forEach(function (c) {
        var line = document.createElement('div');
        line.className = 'claim-line';
        var badge = document.createElement('span');
        badge.className = 'badge ' + c.metric_type;
        badge.textContent = c.metric_type;
        line.appendChild(badge);
        var val = document.createElement('strong');
        val.textContent = ' ' + fmtNum(c.value_tco2e) + ' tCO₂e';
        val.style.marginLeft = '6px';
        line.appendChild(val);
        if (c.period) {
          var per = document.createElement('span');
          per.className = 'meta';
          per.textContent = ' · ' + c.period;
          line.appendChild(per);
        }
        var q = document.createElement('blockquote');
        q.textContent = '"' + c.quote + '"';
        line.appendChild(q);
        var src = document.createElement('a');
        src.className = 'cite';
        src.href = c.source_url;
        src.target = '_blank';
        src.rel = 'noopener';
        src.textContent = 'Source (own site)';
        line.appendChild(src);
        card.appendChild(line);
      });
      grid.appendChild(card);
    });
    if (!groups.length) {
      grid.innerHTML = '<p class="note">No startups match the current filters.</p>';
    }
  }

  function renderChart(rows) {
    var svg = document.getElementById('bar-chart');
    if (!svg) return;
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    var sorted = rows.slice().sort(function (a, b) { return b.value_tco2e - a.value_tco2e; });
    var w = 1700;
    var h = 720;
    var padL = 120;
    var padB = 48;
    var padT = 24;
    var barH = Math.max(18, Math.min(36, (h - padT - padB) / Math.max(1, sorted.length) - 4));
    var maxV = sorted.length ? sorted[0].value_tco2e : 1;
    svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);

    sorted.forEach(function (row, i) {
      var y = padT + i * (barH + 6);
      var barW = maxV ? ((w - padL - 40) * (row.value_tco2e / maxV)) : 0;
      var label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      label.setAttribute('x', padL - 8);
      label.setAttribute('y', y + barH * 0.72);
      label.setAttribute('text-anchor', 'end');
      label.textContent = row.name.length > 22 ? row.name.slice(0, 20) + '…' : row.name;
      svg.appendChild(label);

      var rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      rect.setAttribute('x', padL);
      rect.setAttribute('y', y);
      rect.setAttribute('width', Math.max(2, barW));
      rect.setAttribute('height', barH);
      rect.setAttribute('rx', '4');
      var fill = row.metric_type === 'managed' ? '#5F6663' : row.metric_type === 'mitigated' ? '#2D6A4F' : '#40916C';
      rect.setAttribute('fill', fill);
      svg.appendChild(rect);

      var val = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      val.setAttribute('x', padL + barW + 8);
      val.setAttribute('y', y + barH * 0.72);
      val.textContent = fmtNum(row.value_tco2e) + ' (' + row.metric_type + ')';
      svg.appendChild(val);
    });
    if (!sorted.length) {
      var empty = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      empty.setAttribute('x', w / 2);
      empty.setAttribute('y', h / 2);
      empty.setAttribute('text-anchor', 'middle');
      empty.textContent = 'No rows to chart';
      svg.appendChild(empty);
    }
  }

  var sortKey = 'value_tco2e';
  var sortDir = -1;

  function renderTable(rows) {
    var tbody = document.getElementById('data-tbody');
    if (!tbody) return;
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
      var tr = document.createElement('tr');
      tr.innerHTML =
        '<td><a href="' + nexusUrl(row.slug) + '" target="_blank" rel="noopener">' + escapeHtml(row.name) + '</a></td>' +
        '<td>' + escapeHtml(row.country) + '</td>' +
        '<td>' + escapeHtml(row.sector) + '</td>' +
        '<td>' + escapeHtml(row.theme) + '</td>' +
        '<td><span class="badge ' + row.metric_type + '">' + row.metric_type + '</span></td>' +
        '<td class="num">' + fmtNum(row.value_tco2e) + '</td>' +
        '<td>' + (row.period ? escapeHtml(row.period) : '—') + '</td>' +
        '<td>' + escapeHtml(row.quote) + '</td>' +
        '<td><a class="cite" href="' + escapeHtml(row.source_url) + '" target="_blank" rel="noopener">Link</a></td>';
      tbody.appendChild(tr);
    });
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function syncRangeLabels() {
    var f = getFilters();
    var minV = Math.pow(10, f.logMin);
    var maxV = Math.pow(10, f.logMax);
    document.getElementById('range-min-label').textContent = fmtNum(minV) + ' t';
    document.getElementById('range-max-label').textContent = fmtNum(maxV) + ' t';
  }

  function refresh() {
    var rows = filteredRows();
    updateCounters(rows);
    renderCards(rows);
    renderChart(rows);
    renderTable(rows);
    syncRangeLabels();
  }

  function initFilters() {
    var fields = ['country', 'sector', 'theme', 'metric_type'];
    fields.forEach(function (field) {
      var id = field === 'metric_type' ? 'f-metric' : 'f-' + field;
      var sel = document.getElementById(id);
      var key = field;
      var values = uniq(ROWS.map(function (r) { return r[key]; }));
      values.forEach(function (v) {
        var opt = document.createElement('option');
        opt.value = v;
        opt.textContent = v;
        sel.appendChild(opt);
      });
    });

    var range = document.getElementById('f-range');
    var rangeMax = document.getElementById('f-range-max');
    range.min = String(LOG_MIN);
    range.max = String(LOG_MAX_SLIDER);
    range.step = '0.001';
    range.value = String(LOG_MIN);
    rangeMax.min = String(LOG_MIN);
    rangeMax.max = String(LOG_MAX_SLIDER);
    rangeMax.step = '0.001';
    rangeMax.value = String(LOG_MAX_SLIDER);

    ['f-country', 'f-sector', 'f-theme', 'f-metric', 'f-range', 'f-range-max'].forEach(function (id) {
      document.getElementById(id).addEventListener('input', function () {
        var f = getFilters();
        if (f.logMin > f.logMax) {
          if (id === 'f-range') document.getElementById('f-range-max').value = range.value;
          else document.getElementById('f-range').value = rangeMax.value;
        }
        refresh();
      });
      document.getElementById(id).addEventListener('change', refresh);
    });

    document.getElementById('btn-reset-filters').addEventListener('click', function (ev) {
      ev.stopPropagation();
      document.getElementById('f-country').value = 'all';
      document.getElementById('f-sector').value = 'all';
      document.getElementById('f-theme').value = 'all';
      document.getElementById('f-metric').value = 'all';
      range.value = String(LOG_MIN);
      rangeMax.value = String(LOG_MAX_SLIDER);
      refresh();
    });
  }

  function initTableSort() {
    document.querySelectorAll('#data-table th[data-sort]').forEach(function (th) {
      th.addEventListener('click', function (ev) {
        ev.stopPropagation();
        var key = th.getAttribute('data-sort');
        if (sortKey === key) sortDir *= -1;
        else { sortKey = key; sortDir = key === 'value_tco2e' ? -1 : 1; }
        renderTable(filteredRows());
      });
    });
  }

  function initCoverage() {
    document.getElementById('cov-portfolio').textContent = String(COVERAGE.portfolio);
    document.getElementById('cov-checked').textContent = String(COVERAGE.websitesChecked);
    document.getElementById('cov-no-site').textContent = String(COVERAGE.noWebsite);
    document.getElementById('cov-unreach').textContent = String(COVERAGE.unreachable);
    document.getElementById('cov-reporting').textContent = String(uniq(ROWS.map(function (r) { return r.slug; })).length);
    document.getElementById('cov-claims').textContent = String(ROWS.length);
  }

  initFilters();
  initTableSort();
  initCoverage();
  refresh();
})();
