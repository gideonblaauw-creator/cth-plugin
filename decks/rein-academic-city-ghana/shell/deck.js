(function () {
  'use strict';

  var frame = document.querySelector('.deck-frame');
  var stage = document.querySelector('.deck-stage');
  var slides = Array.prototype.slice.call(document.querySelectorAll('.deck .slide'));
  var current = 0;
  var printMode = /\?print(?:=|$)/.test(window.location.search) || window.location.hash === '#print';

  function scaleStage() {
    if (!frame || !stage || printMode) return;
    var vw = window.innerWidth;
    var vh = window.innerHeight;
    var scale = Math.min(vw / 1920, vh / 1080) * 0.96;
    frame.style.width = Math.round(1920 * scale) + 'px';
    frame.style.height = Math.round(1080 * scale) + 'px';
    stage.style.transform = 'scale(' + scale + ')';
  }

  function initSlideNumbers() {
    var total = slides.length;
    slides.forEach(function (s, i) {
      var el = s.querySelector('.slide-num');
      if (el) el.textContent = (i + 1) + ' / ' + total;
    });
  }

  function updateDots() {
    var dots = document.querySelectorAll('.slide-dots button');
    dots.forEach(function (btn, i) {
      var on = i === current;
      btn.classList.toggle('active', on);
      btn.setAttribute('aria-current', on ? 'true' : 'false');
    });
  }

  function setSlide(index) {
    if (!slides.length) return;
    index = Math.max(0, Math.min(slides.length - 1, index));
    slides.forEach(function (s, i) {
      s.classList.toggle('active', i === index);
    });
    current = index;
    updateDots();
    if (!printMode) {
      var hash = '#' + (index + 1);
      if (window.location.hash !== hash && window.location.hash !== '#print') {
        history.replaceState(null, '', hash);
      }
    }
  }

  function next() { setSlide(current + 1); }
  function prev() { setSlide(current - 1); }

  function slideFromHash() {
    var h = window.location.hash.replace(/^#/, '');
    if (!h || h === 'print') return 0;
    var n = parseInt(h, 10);
    if (!isNaN(n) && n >= 1) return n - 1;
    return 0;
  }

  function isInteractiveTarget(el) {
    if (!el || el === stage) return false;
    var tag = el.tagName;
    if (tag === 'A' || tag === 'BUTTON' || tag === 'INPUT') return true;
    if (el.closest && el.closest('.deck-chrome, .deck-menu, .lightbox, .expand-card, .lightbox-open, .tab-set, .chart, [role="tablist"], [data-stage-map]')) return true;
    return false;
  }

  function selectTab(tab) {
    var set = tab.closest('.tab-set');
    if (!set) return;
    var tabs = set.querySelectorAll('[role="tab"]');
    tabs.forEach(function (t) {
      var on = t === tab;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
      var panel = document.getElementById(t.getAttribute('aria-controls'));
      if (panel) panel.hidden = !on;
    });
    var year = tab.getAttribute('data-year');
    document.querySelectorAll('.chart [data-year]').forEach(function (node) {
      node.classList.toggle('is-on', node.getAttribute('data-year') === year);
    });
  }

  function moveTab(list, dir) {
    var tabs = Array.prototype.slice.call(list.querySelectorAll('[role="tab"]'));
    if (!tabs.length) return;
    var idx = tabs.findIndex(function (t) { return t.getAttribute('aria-selected') === 'true'; });
    if (idx < 0) idx = 0;
    var nextIdx = (idx + dir + tabs.length) % tabs.length;
    selectTab(tabs[nextIdx]);
    tabs[nextIdx].focus();
  }

  function selectStage(map, id) {
    map.classList.add('has-selection');
    map.querySelectorAll('[data-stage-btn]').forEach(function (btn) {
      var on = btn.getAttribute('data-stage-btn') === id;
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    map.querySelectorAll('[data-stage-group]').forEach(function (group) {
      group.classList.toggle('is-on', group.getAttribute('data-stage-group') === id);
    });
  }

  function initStageMap() {
    document.querySelectorAll('[data-stage-map]').forEach(function (map) {
      var buttons = Array.prototype.slice.call(map.querySelectorAll('[data-stage-btn]'));
      buttons.forEach(function (btn, i) {
        btn.tabIndex = i === 0 ? 0 : -1;
        btn.addEventListener('click', function (ev) {
          ev.stopPropagation();
          selectStage(map, btn.getAttribute('data-stage-btn'));
          buttons.forEach(function (b) { b.tabIndex = b === btn ? 0 : -1; });
        });
        btn.addEventListener('keydown', function (ev) {
          if (ev.key !== 'ArrowRight' && ev.key !== 'ArrowLeft') return;
          ev.preventDefault();
          ev.stopPropagation();
          var idx = buttons.indexOf(btn);
          var dir = ev.key === 'ArrowRight' ? 1 : -1;
          var nextBtn = buttons[(idx + dir + buttons.length) % buttons.length];
          selectStage(map, nextBtn.getAttribute('data-stage-btn'));
          buttons.forEach(function (b) { b.tabIndex = b === nextBtn ? 0 : -1; });
          nextBtn.focus();
        });
      });
      var current = map.querySelector('[data-stage-btn][aria-pressed="true"]') || buttons[0];
      if (current) selectStage(map, current.getAttribute('data-stage-btn'));
    });
  }

  function initTabs() {
    document.querySelectorAll('.tab-set').forEach(function (set) {
      var tabs = set.querySelectorAll('[role="tab"]');
      tabs.forEach(function (tab, i) {
        tab.tabIndex = i === 0 ? 0 : -1;
        tab.addEventListener('click', function (ev) {
          ev.stopPropagation();
          selectTab(tab);
        });
      });
      set.querySelectorAll('.step-btn').forEach(function (btn) {
        btn.addEventListener('click', function (ev) {
          ev.stopPropagation();
          var list = set.querySelector('[role="tablist"]');
          moveTab(list, btn.getAttribute('data-step') === 'prev' ? -1 : 1);
        });
      });
      var first = set.querySelector('[role="tab"][aria-selected="true"]') || tabs[0];
      if (first) selectTab(first);
    });
    document.querySelectorAll('.chart [data-year]').forEach(function (node) {
      node.addEventListener('click', function (ev) {
        ev.stopPropagation();
        var year = node.getAttribute('data-year');
        var tab = document.querySelector('[role="tab"][data-year="' + year + '"]');
        if (tab) selectTab(tab);
      });
    });
  }

  function onKey(e) {
    if (printMode) return;
    var menu = document.getElementById('deck-menu');
    var menuBtn = document.getElementById('btn-menu');
    if (menu && !menu.hidden && e.key === 'Escape') {
      menu.hidden = true;
      if (menuBtn) menuBtn.setAttribute('aria-expanded', 'false');
      return;
    }
    var lb = document.getElementById('lightbox');
    if (lb && !lb.hidden && e.key === 'Escape') {
      lb.hidden = true;
      return;
    }
    var list = e.target && e.target.closest && e.target.closest('[role="tablist"]');
    if (list && (e.key === 'ArrowRight' || e.key === 'ArrowLeft' || e.key === 'ArrowUp' || e.key === 'ArrowDown')) {
      e.preventDefault();
      e.stopPropagation();
      var dir = (e.key === 'ArrowRight' || e.key === 'ArrowDown') ? 1 : -1;
      moveTab(list, dir);
      return;
    }
    var k = e.key;
    if (k === 'ArrowRight' || k === ' ' || k === 'PageDown') {
      e.preventDefault();
      next();
    } else if (k === 'ArrowLeft' || k === 'PageUp') {
      e.preventDefault();
      prev();
    }
  }

  function onStageClick(e) {
    if (printMode || isInteractiveTarget(e.target)) return;
    var rect = (frame || stage).getBoundingClientRect();
    var x = e.clientX - rect.left;
    if (x > rect.width / 2) next();
    else prev();
  }

  function initExpandCards() {
    document.querySelectorAll('.expand-card .expand-trigger').forEach(function (btn) {
      btn.addEventListener('click', function (ev) {
        ev.stopPropagation();
        var body = btn.parentElement.querySelector('.expand-body');
        if (!body) return;
        var open = body.classList.toggle('open');
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    });
  }

  function initDots() {
    var wrap = document.getElementById('slide-dots');
    if (!wrap) return;
    wrap.innerHTML = '';
    slides.forEach(function (_s, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('aria-label', 'Go to slide ' + (i + 1));
      b.addEventListener('click', function (ev) {
        ev.stopPropagation();
        setSlide(i);
      });
      wrap.appendChild(b);
    });
  }

  function initMenu() {
    var menu = document.getElementById('deck-menu');
    var list = document.getElementById('deck-menu-list');
    var btnMenu = document.getElementById('btn-menu');
    if (!menu || !list || !btnMenu) return;
    list.innerHTML = '';
    slides.forEach(function (slide, i) {
      var li = document.createElement('li');
      var b = document.createElement('button');
      b.type = 'button';
      var title = slide.getAttribute('data-menu-title') || ('Slide ' + (i + 1));
      b.textContent = (i + 1) + '. ' + title;
      b.addEventListener('click', function () {
        menu.hidden = true;
        btnMenu.setAttribute('aria-expanded', 'false');
        setSlide(i);
      });
      li.appendChild(b);
      list.appendChild(li);
    });
    btnMenu.addEventListener('click', function (ev) {
      ev.stopPropagation();
      menu.hidden = !menu.hidden;
      btnMenu.setAttribute('aria-expanded', menu.hidden ? 'false' : 'true');
    });
    menu.addEventListener('click', function (ev) {
      if (ev.target === menu) {
        menu.hidden = true;
        btnMenu.setAttribute('aria-expanded', 'false');
      }
    });
  }

  function initQuestionsToggle() {
    var btn = document.getElementById('btn-questions');
    if (!btn) return;
    btn.addEventListener('click', function (ev) {
      ev.stopPropagation();
      var on = document.body.classList.toggle('show-questions');
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      btn.textContent = on ? 'Hide questions' : 'Show questions';
    });
  }

  function initLightbox() {
    var lb = document.getElementById('lightbox');
    var img = document.getElementById('lightbox-img');
    var cap = document.getElementById('lightbox-cap');
    var close = document.getElementById('lightbox-close');
    if (!lb || !img) return;
    document.querySelectorAll('.lightbox-open').forEach(function (btn) {
      btn.addEventListener('click', function (ev) {
        ev.stopPropagation();
        img.src = btn.getAttribute('data-src') || '';
        img.alt = btn.getAttribute('data-caption') || '';
        if (cap) cap.textContent = btn.getAttribute('data-caption') || '';
        lb.hidden = false;
      });
    });
    function closeLb() {
      lb.hidden = true;
      img.src = '';
    }
    if (close) close.addEventListener('click', closeLb);
    lb.addEventListener('click', function (ev) {
      if (ev.target === lb) closeLb();
    });
  }

  initSlideNumbers();
  initDots();
  initMenu();
  initQuestionsToggle();
  initExpandCards();
  initLightbox();
  initTabs();
  initStageMap();

  if (printMode) {
    document.body.classList.add('print-all');
    document.body.classList.add('show-questions');
    slides.forEach(function (s) { s.classList.add('active'); });
    document.querySelectorAll('.expand-body').forEach(function (el) { el.classList.add('open'); });
  } else {
    setSlide(slideFromHash());
    window.addEventListener('resize', scaleStage);
    window.addEventListener('hashchange', function () { setSlide(slideFromHash()); });
    document.addEventListener('keydown', onKey);
    if (stage) stage.addEventListener('click', onStageClick);
    scaleStage();
  }
})();
