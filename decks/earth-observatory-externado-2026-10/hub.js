(function () {
  'use strict';

  const body = document.body;
  const hubMain = document.getElementById('hub-main');
  if (!hubMain) return;

  let EO = null;
  let startups = [];
  let geoFeatures = [];
  let mapState = { selectedSlug: null, deptFilter: '' };

  function esc(s) {
    return String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  }

  function switchView(viewId) {
    document.querySelectorAll('.hub-view').forEach((v) => v.classList.toggle('active', v.id === 'view-' + viewId));
    document.querySelectorAll('.hub-nav button[data-view]').forEach((b) => b.classList.toggle('on', b.dataset.view === viewId));
    if (viewId === 'actors' && !mapState.built) buildMap();
  }

  function openDocSection(sectionId) {
    body.dataset.mode = 'doc';
    if (docToggle) docToggle.textContent = 'Volver al Hub';
    if (docNav) docNav.style.display = 'flex';
    const el = document.getElementById(sectionId);
    if (el) setTimeout(() => el.scrollIntoView({ behavior: 'smooth' }), 50);
  }

  document.querySelectorAll('.hub-nav button[data-view]').forEach((btn) => {
    btn.addEventListener('click', () => switchView(btn.dataset.view));
  });

  const docToggle = document.getElementById('hubDocToggle');
  const docNav = document.getElementById('nav');
  if (docToggle) {
    docToggle.addEventListener('click', () => {
      const toDoc = body.dataset.mode !== 'doc';
      body.dataset.mode = toDoc ? 'doc' : 'hub';
      docToggle.textContent = toDoc ? 'Volver al Hub' : 'Documento WP (16 §)';
      if (docNav) docNav.style.display = toDoc ? 'flex' : 'none';
      if (toDoc) window.scrollTo(0, 0);
      else switchView('overview');
    });
  }

  document.querySelectorAll('[data-goto-doc]').forEach((el) => {
    el.addEventListener('click', (e) => {
      e.preventDefault();
      openDocSection(el.getAttribute('data-goto-doc').replace('#', ''));
    });
  });

  document.querySelectorAll('[data-goto-view]').forEach((el) => {
    el.addEventListener('click', (e) => {
      e.preventDefault();
      body.dataset.mode = 'hub';
      if (docToggle) docToggle.textContent = 'Documento WP (16 §)';
      if (docNav) docNav.style.display = 'none';
      switchView(el.getAttribute('data-goto-view'));
    });
  });

  document.querySelectorAll('.hub-card.clickable[data-goto-view]').forEach((el) => {
    el.addEventListener('click', () => {
      body.dataset.mode = 'hub';
      switchView(el.getAttribute('data-goto-view'));
    });
  });

  /* MLP */
  const mlpData = {
    paisaje: {
      title: 'Paisaje',
      desc: 'Presión exterior: clima, mercados, marcos internacionales (EUDR). El lente Ambiental lee este nivel.',
      role: 'No pronostica la vía de un lente; una celda vacía no es un cero (WP §2).',
      inter: 'Cooperación internacional transporta presión de paisaje; no es el paisaje por sí sola.'
    },
    regimen: {
      title: 'Régimen sociotécnico',
      desc: 'Sistema existente: reglas, mercados, instituciones. Se cita IDEAM, CREG, MinAmbiente; no se sustituye.',
      role: 'El observatorio no publica tasas nacionales propias ni un atlas alternativo.',
      inter: 'Sector privado como adoptante posible; sin lista de empresas en esta nota.'
    },
    nicho: {
      title: 'Nicho de innovación',
      desc: 'Donde se forma lo nuevo bajo protección (sandbox, living lab, cohorte vía REIN).',
      role: 'Aquí se sienta el hilo tecnológico. Externado y CTH conectan niveles como intermediarios.',
      inter: 'CTH es intermediario de confianza; no es dueño de un data warehouse (WP §2, §9).'
    }
  };

  function selectMlpTier(key) {
    const d = mlpData[key];
    if (!d) return;
    document.getElementById('mlp-detail-title').textContent = d.title;
    document.getElementById('mlp-detail-desc').textContent = d.desc;
    document.getElementById('mlp-detail-role').textContent = d.role;
    document.getElementById('mlp-detail-inter').textContent = d.inter;
    ['paisaje', 'regimen', 'nicho'].forEach((k) => {
      document.getElementById('tier-' + k)?.classList.toggle('sel', k === key);
    });
  }

  document.querySelectorAll('[data-mlp-tier]').forEach((el) => {
    el.addEventListener('click', () => selectMlpTier(el.dataset.mlpTier));
  });
  selectMlpTier('nicho');

  /* Lenses hub */
  function bindHubLenses() {
    const tabs = document.querySelectorAll('#hubLensTabs button');
    const panel = document.getElementById('hubLensPanel');
    if (!tabs.length || !panel || !EO) return;
    const urbExtra = ' No monta red de estaciones; adoptante <span class="pendiente">sin evidencia</span> en fuente fechada.';
    tabs.forEach((btn) => {
      btn.onclick = () => {
        tabs.forEach((b) => b.classList.remove('on'));
        btn.classList.add('on');
        const lens = EO.lenses.find((x) => x.id === btn.dataset.lens);
        if (!lens) return;
        let bodyHtml = esc(lens.body);
        if (lens.id === 'urbana') bodyHtml += urbExtra;
        panel.innerHTML =
          '<h3>' +
          esc(lens.title) +
          '</h3><p>' +
          bodyHtml +
          '</p><p class="source-foot">Fuente: WP §8. <a href="#" data-goto-doc="s8">Ver sección completa →</a></p>';
        panel.querySelector('[data-goto-doc]')?.addEventListener('click', (e) => {
          e.preventDefault();
          openDocSection('s8');
        });
      };
    });
    tabs[0]?.click();
  }

  /* Datalab pipe */
  const pipeSteps = [
    { id: 'l1', title: 'L1 Bruto', body: 'Copia cruda con fecha y fuente. Carril A1/A2/A3 ≠ L1/L2/L3.' },
    { id: 'l2', title: 'L2 Limpio', body: 'Validado, unidades unificadas, un hecho por fila.' },
    { id: 'l3', title: 'L3 Listo', body: 'Respuesta trazable a una pregunta; dashboards leen solo L3.' }
  ];

  function selectPipeStep(idx) {
    document.querySelectorAll('.hub-pipe-step').forEach((s, i) => s.classList.toggle('on', i === idx));
    const sl = document.getElementById('hubLevelSlider');
    if (sl) sl.value = String(idx + 1);
    syncHubLevelPanel();
  }

  document.querySelectorAll('.hub-pipe-step').forEach((el, i) => {
    el.addEventListener('click', () => selectPipeStep(i));
  });

  function syncHubLevelPanel() {
    const sl = document.getElementById('hubLevelSlider');
    const pan = document.getElementById('hubLevelPanel');
    if (!sl || !pan || !EO) return;
    pan.innerHTML = EO.levels[sl.value];
    selectPipeStep(Number(sl.value) - 1);
  }

  const hubLevelSlider = document.getElementById('hubLevelSlider');
  if (hubLevelSlider) hubLevelSlider.addEventListener('input', syncHubLevelPanel);

  /* Phases hub */
  function bindHubPhases() {
    const cards = document.querySelectorAll('.hub-phase-card');
    const sl = document.getElementById('hubPhaseSlider');
    const pan = document.getElementById('hubPhasePanel');
    if (!EO || !sl || !pan) return;
    const sync = (val) => {
      sl.value = val;
      const d = EO.phases[val];
      pan.innerHTML = '<strong>' + esc(d.title) + '</strong><p>' + esc(d.body) + '</p><p class="source-foot">Plazos y planta: <span class="pendiente">PENDIENTE</span> (v2). <a href="#" data-goto-doc="s13">WP §13 →</a></p>';
      pan.querySelector('[data-goto-doc]')?.addEventListener('click', (e) => {
        e.preventDefault();
        openDocSection('s13');
      });
      cards.forEach((c) => c.classList.toggle('sel', c.dataset.phase === val));
    };
    cards.forEach((c) => c.addEventListener('click', () => sync(c.dataset.phase)));
    sl.addEventListener('input', () => sync(sl.value));
    sync('1');
  }

  /* Actors */
  const actorData = {
    gobierno: {
      title: 'Gobierno (hélice)',
      role: 'Porta regla e información oficial: IDEAM, UPME, normas de comunidades energéticas.',
      limit: 'Ningún ministerio es miembro del observatorio. El dato sostiene la conversación.'
    },
    startups: {
      title: 'Startups / innovación (hélice)',
      role: 'Nicho si la oferta necesita protección. Cohorte solo vía REIN.',
      limit: 'Esta nota no nombra empresas en el texto WP; el mapa muestra solo filas con fuente en nexus-co-cities.csv (25).'
    },
    privado: {
      title: 'Sector privado (hélice)',
      role: 'Régimen; adoptante posible con informe público citado.',
      limit: 'Sin lista de empresas ni clientes en la nota.'
    },
    cooperacion: {
      title: 'Cooperación internacional (hélice)',
      role: 'Presión de paisaje; puede proteger el nicho con proyecto con dueño.',
      limit: 'No es el paisaje (el lente Ambiental sí lee paisaje).'
    },
    locales: {
      title: 'Gobiernos locales (círculo)',
      role: 'Invitación vía Carapulica; ejemplo pedido agrovoltaica sin anunciar membresía.',
      limit: '<span class="pendiente">PENDIENTE</span>: ninguna alcaldía colombiana invitada en esta nota (WP §6 paso 5).'
    },
    cooperativas: {
      title: 'Cooperativas / sociedad civil (círculo)',
      role: 'Contexto normativo Dec. 2236/2023; sociedad civil fuera de la hélice.',
      limit: 'Una comunidad energética no es, por esa sola norma, una cooperativa.'
    }
  };

  function selectActor(key) {
    const d = actorData[key];
    if (!d) return;
    document.getElementById('actor-title').innerHTML = d.title;
    document.getElementById('actor-role').innerHTML = d.role;
    document.getElementById('actor-limit').innerHTML = d.limit;
    document.querySelectorAll('.hub-actor-svg .node').forEach((n) => n.classList.toggle('sel', n.dataset.actor === key));
  }

  document.querySelectorAll('.hub-actor-svg .node').forEach((n) => {
    n.addEventListener('click', () => selectActor(n.dataset.actor));
  });
  selectActor('startups');

  /* Colombia map */
  function parseCsv(text) {
    const lines = text.trim().split(/\r?\n/);
    const out = [];
    for (let i = 1; i < lines.length; i++) {
      const parts = lines[i].split(',');
      if (parts.length < 7) continue;
      const source = parts.slice(6).join(',');
      out.push({
        name: parts[0],
        slug: parts[1],
        city: parts[2],
        department: parts[3],
        lat: parseFloat(parts[4]),
        lng: parseFloat(parts[5]),
        source_url: source
      });
    }
    return out;
  }

  function normDept(s) {
    return String(s)
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase()
      .replace(/[^a-z0-9\s]/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  }

  const deptGroups = [
    ['bogota capital district', 'bogota d c', 'distrito capital', 'bogota'],
    ['valle del cauca', 'valle'],
    ['norte de santander', 'norte santander']
  ];

  function deptMatch(a, b) {
    const na = normDept(a);
    const nb = normDept(b);
    if (na === nb || na.includes(nb) || nb.includes(na)) return true;
    for (const g of deptGroups) {
      const ng = g.map(normDept);
      const inA = ng.some((x) => na === x || na.includes(x) || x.includes(na));
      const inB = ng.some((x) => nb === x || nb.includes(x) || x.includes(nb));
      if (inA && inB) return true;
    }
    return false;
  }

  mapState.built = false;

  function renderMapPanel(s) {
    const panel = document.getElementById('mapStartupPanel');
    if (!panel) return;
    if (!s) {
      panel.className = 'map-panel empty';
      panel.innerHTML = '<p>Selecciona un pin o una fila de la lista. Solo startups con fila en <code>nexus-co-cities.csv</code>.</p>';
      return;
    }
    panel.className = 'map-panel';
    panel.innerHTML =
      '<h3>' +
      esc(s.name) +
      '</h3><p class="meta"><strong>Ciudad:</strong> ' +
      esc(s.city) +
      '<br><strong>Departamento:</strong> ' +
      esc(s.department) +
      '</p><a class="src" href="' +
      esc(s.source_url) +
      '" target="_blank" rel="noopener noreferrer">Fuente verificada →</a><p class="source-foot">Coordenadas de ciudad (CSV). No implica sede operativa.</p>';
  }

  function applyMapFilter() {
    const sel = document.getElementById('mapDeptFilter');
    mapState.deptFilter = sel ? sel.value : '';
    document.querySelectorAll('#coMap path.dept').forEach((p) => {
      const name = p.dataset.dept;
      const show = !mapState.deptFilter || deptMatch(name, mapState.deptFilter);
      p.classList.toggle('dim', !show);
      p.classList.toggle('hl', !!mapState.deptFilter && show);
    });
    document.querySelectorAll('#coMap circle.pin').forEach((c) => {
      const show = !mapState.deptFilter || deptMatch(c.dataset.dept, mapState.deptFilter);
      c.classList.toggle('dim', !show);
    });
    renderStartupList();
  }

  function renderStartupList() {
    const list = document.getElementById('mapStartupList');
    if (!list) return;
    const filtered = startups.filter((s) => !mapState.deptFilter || deptMatch(s.department, mapState.deptFilter));
    list.innerHTML = filtered
      .map(
        (s) =>
          '<button type="button" class="linkish" data-slug="' +
          esc(s.slug) +
          '" style="margin:4px 6px 4px 0">' +
          esc(s.name) +
          '</button>'
      )
      .join('');
    list.querySelectorAll('button').forEach((b) => {
      b.addEventListener('click', () => selectStartup(b.dataset.slug));
    });
  }

  function selectStartup(slug) {
    mapState.selectedSlug = slug;
    const s = startups.find((x) => x.slug === slug);
    document.querySelectorAll('#coMap circle.pin').forEach((c) => c.classList.toggle('sel', c.dataset.slug === slug));
    renderMapPanel(s);
  }

  function buildMap() {
    if (mapState.built || !geoFeatures.length || !startups.length) return;
    const container = document.getElementById('coMap');
    if (!container || !window.d3) return;

    const width = container.clientWidth || 640;
    const height = container.clientHeight || 420;
    container.innerHTML = '';
    const svg = d3.select(container).append('svg').attr('viewBox', '0 0 ' + width + ' ' + height);

    const projection = d3.geoMercator().fitExtent(
      [
        [16, 12],
        [width - 16, height - 12]
      ],
      { type: 'FeatureCollection', features: geoFeatures }
    );
    const path = d3.geoPath().projection(projection);

    svg
      .selectAll('path.dept')
      .data(geoFeatures)
      .join('path')
      .attr('class', 'dept')
      .attr('d', path)
      .attr('data-dept', (d) => d.properties.name)
      .each(function (d) {
        this.dataset.dept = d.properties.name;
      })
      .on('click', (_, d) => {
        const sel = document.getElementById('mapDeptFilter');
        if (sel) {
          sel.value = d.properties.name;
          applyMapFilter();
        }
      });

    const cityGroups = {};
    startups.forEach((s, i) => {
      const key = s.lat + ',' + s.lng;
      if (!cityGroups[key]) cityGroups[key] = [];
      cityGroups[key].push({ s, i });
    });

    Object.values(cityGroups).forEach((group) => {
      group.forEach((item, j) => {
        const s = item.s;
        const spread = 0.14 * (1 + j * 0.08);
        const lng = s.lng + Math.cos(j * 1.85) * spread;
        const lat = s.lat + Math.sin(j * 1.85) * spread;
        const pt = projection([lng, lat]);
        if (!pt) return;
        svg
          .append('circle')
          .attr('class', 'pin')
          .attr('cx', pt[0])
          .attr('cy', pt[1])
          .attr('r', 5)
          .attr('data-slug', s.slug)
          .attr('data-dept', s.department)
          .on('click', (ev) => {
            ev.stopPropagation();
            selectStartup(s.slug);
          });
      });
    });

    mapState.built = true;
    applyMapFilter();
    const countEl = document.getElementById('mapStartupCount');
    if (countEl) countEl.textContent = String(startups.length);
  }

  function populateDeptFilter() {
    const sel = document.getElementById('mapDeptFilter');
    if (!sel) return;
    const depts = [...new Set(geoFeatures.map((f) => f.properties.name))].sort((a, b) => a.localeCompare(b, 'es'));
    depts.forEach((d) => {
      const o = document.createElement('option');
      o.value = d;
      o.textContent = d;
      sel.appendChild(o);
    });
    sel.addEventListener('change', applyMapFilter);
  }

  Promise.all([
    fetch('data/eo-deck.json').then((r) => r.json()),
    fetch('data/nexus-co-cities.csv').then((r) => r.text()),
    fetch('data/col-min.geojson').then((r) => r.json())
  ])
    .then(([deck, csvText, geo]) => {
      EO = deck;
      startups = parseCsv(csvText);
      geoFeatures = geo.features || [];
      populateDeptFilter();
      bindHubLenses();
      bindHubPhases();
      syncHubLevelPanel();
      document.getElementById('mapStartupCount') && (document.getElementById('mapStartupCount').textContent = String(startups.length));
      if (body.dataset.mode === 'hub' && document.querySelector('#view-actors.active')) buildMap();
    })
    .catch(() => {});

  switchView('overview');

  window.EOHub = { switchView, selectStartup, openDocSection, buildMap };
})();
