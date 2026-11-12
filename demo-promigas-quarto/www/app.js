(function () {
  'use strict';

  CthI18n.init();

  document.querySelectorAll('#lang-toggle button[data-lang]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      CthI18n.setLang(btn.getAttribute('data-lang'));
    });
  });

  function t(key, vars) { return CthI18n.t(key, vars); }

  var SCREENS = 7;
  var current = 0;
  var maps = { paiva: null, guajira: null };
  var guajiraLoaded = false;
  var guajiraMarkers = [];
  var paivaPopupLayer = null;
  var selectedKwp = null;
  var transformShown = false;
  var guajiraBtnDone = false;

  // Vereda Paiva, Bolívar — aprox. (Fundación Promigas; sin geocódigo en fuente)
  var PAIVA_APPROX = [10.450, -75.250];

  /** Verificado: demo-promigas-fact-check.md */
  var MAP_PROJECTS = [
    {
      mapKey: 'p1',
      lat: 11.378, lng: -72.240, approx: true, fenoge: true, dutch: false,
      kwp: 1102, kwpLabel: '1.102 kWp',
      source: 'https://fenoge.gov.co/gobierno-nacional-entrega-en-maicao-el-primer-territorio-energetico-de-la-guajira/',
      source2: 'https://www.minenergia.gov.co/es/sala-de-prensa/noticias-index/gobierno-nacional-entrega-maicao-primer-territorio-energetico-la-guajira/',
      srcLabel: 'FENOGE + MinEnergía'
    },
    {
      mapKey: 'p2',
      lat: 12.090, lng: -72.145, approx: true, fenoge: true, dutch: false,
      kwp: 1000, kwpLabel: '1 MW',
      source: 'https://www.minenergia.gov.co/es/sala-de-prensa/noticias-index/minenerg%C3%ADa-y-fenoge-instalar%C3%A1n-parque-solar-en-el-cabo-de-la-vela-y-media-luna-que-proveer%C3%A1-energ%C3%ADa-247/',
      source2: 'https://www.review-energy.com/solar/colombia-da-luz-verde-a-una-granja-solar-de-1-mw-que-beneficiara-a-comunidades-indigenas',
      srcLabel: 'MinEnergía + Review Energy'
    },
    {
      mapKey: 'p3',
      lat: 12.199722, lng: -71.263889, approx: false, fenoge: true, dutch: false,
      kwp: null, kwpLabelKey: 'map.p3.kwpLabel',
      source: 'https://fenoge.gov.co/invitacion-abietno-006-de-2024-ia-006-2024-fenoge/',
      source2: 'https://diariodelnorte.net/laguajira/gobierno-nacional-destina-25-000-millones-para-1-618-paneles-solares-y-930-baterias-en-nazareth/',
      srcLabel: 'IA-006-2024 + Diario del Norte'
    },
    {
      mapKey: 'p4',
      lat: 11.157, lng: -72.592, approx: true, fenoge: false, dutch: false,
      kwp: null, kwpLabelKey: 'map.p4.kwpLabel',
      source: 'https://gutami.com/information/news/clean-energy-in-la-guajira-colombia/',
      source2: 'https://energyincidentregister.com/facility/chivo-mono-1-solar-farm-solar-farm-co-100000832324/',
      srcLabel: 'Anuncio público (MOU)'
    }
  ];

  var VERIFIED_KWP_SUM = 2102;
  var DUTCH_MW = 750;

  var WIZARD_COMMUNITIES = [
    { i18nKey: 'commA', kwp: 45, hh: 38 },
    { i18nKey: 'commB', kwp: 62, hh: 52 },
    { i18nKey: 'commC', kwp: 28, hh: 24 }
  ];

  function flowSteps() {
    return [
      t('s3.flow0'),
      t('s3.flow1'),
      t('s3.flow2'),
      t('s3.flow3'),
      t('s3.flow4')
    ];
  }
  var flowIdx = 0;
  var flowTimer = null;

  function paivaPopupHtml() {
    return '<strong>' + t('s1.popupTitle') + '</strong><br>' +
      t('s1.popupBody') + '<br><em>' + t('s1.popupApprox') + '</em><br>' +
      t('s1.popupType') + '<br><small><a href="https://fundacionpromigas.org.co/paiva-estrena-el-primer-piloto-de-energia-solar-comunitaria-de-promigas-y-su-fundacion/" target="_blank" rel="noopener">Noticia Paiva (2025)</a></small>';
  }

  function projectKwpLabel(p) {
    if (p.kwpLabelKey) return t(p.kwpLabelKey);
    return p.kwpLabel;
  }

  function refreshActionButtons() {
    var tr = document.getElementById('btn-transform');
    if (transformShown) tr.textContent = t('s1.btnTransformDone');
    else tr.textContent = t('s1.btnTransform');
    var gj = document.getElementById('btn-guajira');
    if (guajiraBtnDone) gj.textContent = t('s2.btnGuajiraDone', { n: MAP_PROJECTS.length });
    else gj.textContent = t('s2.btnGuajira');
  }

  function refreshMapPopups() {
    if (paivaPopupLayer) paivaPopupLayer.setPopupContent(paivaPopupHtml());
    guajiraMarkers.forEach(function (entry) {
      entry.marker.setPopupContent(projectPopup(entry.project));
    });
  }

  function parseHash() {
    var h = location.hash.replace('#', '');
    var n = parseInt(h, 10);
    if (!isNaN(n) && n >= 0 && n < SCREENS) return n;
    return 0;
  }

  function goTo(idx, pushHash) {
    if (idx < 0 || idx >= SCREENS) return;
    current = idx;
    document.querySelectorAll('.screen').forEach(function (el, i) {
      el.classList.toggle('active', i === idx);
    });
    document.querySelectorAll('.dot').forEach(function (el, i) {
      el.classList.toggle('active', i === idx);
      el.classList.toggle('done', i < idx);
    });
    if (pushHash !== false) location.hash = String(idx);
    if (idx === 0) initPaivaMap();
    if (idx === 1) initGuajiraMap();
    if (idx === 4) populateCommunities();
  }

  function initPaivaMap() {
    if (maps.paiva) {
      maps.paiva.invalidateSize();
      return;
    }
    var el = document.getElementById('map-paiva');
    maps.paiva = L.map(el, { scrollWheelZoom: true }).setView(PAIVA_APPROX, 12);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap',
      maxZoom: 18
    }).addTo(maps.paiva);
    paivaPopupLayer = L.circle(PAIVA_APPROX, {
      radius: 1800,
      color: varPin(),
      fillColor: varPin(),
      fillOpacity: 0.12,
      dashArray: '6,8'
    }).addTo(maps.paiva);
    paivaPopupLayer.bindPopup(paivaPopupHtml());
    L.marker(PAIVA_APPROX, { icon: pinIcon(14) }).addTo(maps.paiva);
  }

  function varPin() { return getComputedStyle(document.documentElement).getPropertyValue('--pin-map').trim() || '#2D6A4F'; }

  function pinIcon(size, dutch) {
    var bg = dutch ? '#95D5B2' : varPin();
    var border = dutch ? '#1B4332' : '#fff';
    var s = size || 10;
    var m = -Math.round(s / 2);
    return L.divIcon({
      className: '',
      html: '<div style="background:' + bg + ';width:' + s + 'px;height:' + s + 'px;border-radius:50%;border:2px solid ' + border + ';box-shadow:0 1px 4px rgba(0,0,0,.35);margin:' + m + 'px 0 0 ' + m + 'px"></div>',
      iconSize: [s, s]
    });
  }

  function initGuajiraMap() {
    if (maps.guajira) {
      maps.guajira.invalidateSize();
      return;
    }
    maps.guajira = L.map('map-guajira').setView([4.5, -74.0], 5);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap',
      maxZoom: 18
    }).addTo(maps.guajira);
  }

  function animateValue(el, target, suffix) {
    var start = 0;
    var dur = 1200;
    var t0 = performance.now();
    function frame(t) {
      var p = Math.min(1, (t - t0) / dur);
      var v = Math.floor(start + (target - start) * (1 - Math.pow(1 - p, 3)));
      el.textContent = v + (suffix || '');
      if (p < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  function projectPopup(p) {
    var loc = p.approx
      ? '<em>' + t('s2.popupApprox') + '</em>'
      : '<em>' + t('s2.popupCoords') + '</em>';
    var tags = '';
    if (p.fenoge) tags += '<span class="tag fenoge" style="display:inline-block;margin:2px 0">' + t('tag.fenoge') + '</span>';
    return '<strong>' + t('map.' + p.mapKey + '.name') + '</strong><br>' + tags + '<br>' +
      projectKwpLabel(p) + '<br>' + t('map.' + p.mapKey + '.ben') + '<br>' + loc + '<br>' +
      '<a href="' + p.source + '" target="_blank" rel="noopener">' + p.srcLabel + '</a>' +
      (p.source2 ? ' · <a href="' + p.source2 + '" target="_blank" rel="noopener">' + t('s2.popupSource2') + '</a>' : '');
  }

  function loadGuajiraPins() {
    if (guajiraLoaded || !maps.guajira) return;
    guajiraLoaded = true;
    maps.guajira.flyTo([11.35, -72.75], 8, { duration: 1.5 });
    MAP_PROJECTS.forEach(function (p, i) {
      setTimeout(function () {
        var marker = L.marker([p.lat, p.lng], { icon: pinIcon(10, p.dutch) })
          .addTo(maps.guajira).bindPopup(projectPopup(p));
        guajiraMarkers.push({ marker: marker, project: p });
        if (p.approx) {
          L.circle([p.lat, p.lng], {
            radius: 12000, color: varPin(), fillOpacity: 0.06, dashArray: '4,6', weight: 1
          }).addTo(maps.guajira);
        }
      }, i * 120);
    });
    setTimeout(function () {
      var elCom = document.getElementById('stat-com');
      var elKwp = document.getElementById('stat-kwp');
      var elMw = document.getElementById('stat-mw');
      animateValue(elCom, MAP_PROJECTS.length, '');
      animateValue(elKwp, VERIFIED_KWP_SUM, '');
      animateValue(elMw, DUTCH_MW, '');
      document.getElementById('totals-note').hidden = false;
      setTimeout(function () {
        elCom.textContent = String(MAP_PROJECTS.length);
        elKwp.textContent = VERIFIED_KWP_SUM.toLocaleString(CthI18n.localeTag());
        elMw.textContent = String(DUTCH_MW);
      }, 1300);
    }, 400);
  }

  function populateCommunities(force) {
    var sel = document.getElementById('sel-community');
    var prev = sel.value;
    if (!force && sel.options.length > 1) return;
    while (sel.options.length > 1) sel.remove(1);
    WIZARD_COMMUNITIES.forEach(function (c) {
      var o = document.createElement('option');
      o.value = c.i18nKey;
      o.textContent = t('s3.' + c.i18nKey);
      sel.appendChild(o);
    });
    if (prev) sel.value = prev;
  }

  function updateCreateBtn() {
    var ok = document.getElementById('sel-community').value && selectedKwp;
    document.getElementById('btn-create').disabled = !ok;
  }

  function startMoneyFlow() {
    if (flowTimer) clearInterval(flowTimer);
    flowIdx = 0;
    var txt = document.getElementById('flow-text');
    var sub = document.getElementById('flow-sub');
    var steps = flowSteps();
    flowTimer = setInterval(function () {
      steps = flowSteps();
      flowIdx = (flowIdx + 1) % steps.length;
      txt.textContent = steps[flowIdx];
      sub.textContent = flowIdx === 4 ? t('s3.flowSubMultisig') : t('s3.flowSub');
    }, 1400);
  }

  document.getElementById('btn-transform').addEventListener('click', function () {
    var coop = document.getElementById('n-coop');
    var comite = document.getElementById('n-comite');
    coop.classList.remove('dim');
    coop.classList.add('highlight');
    comite.classList.add('dim');
    document.getElementById('gov-list').hidden = false;
    this.disabled = true;
    transformShown = true;
    this.textContent = t('s1.btnTransformDone');
  });

  document.getElementById('btn-guajira').addEventListener('click', function () {
    initGuajiraMap();
    loadGuajiraPins();
    this.disabled = true;
    guajiraBtnDone = true;
    this.textContent = t('s2.btnGuajiraDone', { n: MAP_PROJECTS.length });
  });

  document.getElementById('size-options').addEventListener('click', function (e) {
    var btn = e.target.closest('button[data-kwp]');
    if (!btn) return;
    selectedKwp = parseInt(btn.dataset.kwp, 10);
    document.querySelectorAll('#size-options button').forEach(function (b) {
      b.classList.toggle('selected', b === btn);
    });
    updateCreateBtn();
  });

  document.getElementById('sel-community').addEventListener('change', updateCreateBtn);

  document.getElementById('btn-create').addEventListener('click', function () {
    document.getElementById('ceof-wrap').classList.add('visible');
    startMoneyFlow();
  });

  document.getElementById('nav-prev').addEventListener('click', function () { goTo(current - 1); });
  document.getElementById('nav-next').addEventListener('click', function () { goTo(current + 1); });
  document.querySelectorAll('.dot').forEach(function (d) {
    d.addEventListener('click', function () { goTo(parseInt(d.dataset.goto, 10)); });
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'Enter') {
      if (e.key === ' ' || e.key === 'Enter') e.preventDefault();
      if (current === 1 && !guajiraLoaded && e.key !== 'ArrowLeft') {
        var btn = document.getElementById('btn-guajira');
        if (!btn.disabled) { btn.click(); return; }
      }
      goTo(current + 1);
    } else if (e.key === 'ArrowLeft') {
      goTo(current - 1);
    }
  });

  window.addEventListener('hashchange', function () { goTo(parseHash(), false); });

  goTo(parseHash(), false);

  CthI18n.onChange(function () {
    refreshActionButtons();
    populateCommunities(true);
    refreshMapPopups();
    if (flowTimer) {
      var txt = document.getElementById('flow-text');
      var sub = document.getElementById('flow-sub');
      var steps = flowSteps();
      txt.textContent = steps[flowIdx];
      sub.textContent = flowIdx === 4 ? t('s3.flowSubMultisig') : t('s3.flowSub');
    }
  });

  var params = new URLSearchParams(location.search);
  if (params.get('capture') === '1') {
    setTimeout(function () {
      if (current === 0) document.getElementById('btn-transform').click();
      if (current === 1) {
        initGuajiraMap();
        document.getElementById('btn-guajira').click();
      }
      if (current === 4) {
        populateCommunities();
        document.getElementById('sel-community').selectedIndex = 1;
        selectedKwp = 25;
        document.querySelector('#size-options button[data-kwp="25"]').classList.add('selected');
        updateCreateBtn();
        document.getElementById('btn-create').click();
      }
    }, 800);
  }
})();
