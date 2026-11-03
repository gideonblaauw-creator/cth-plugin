(function () {
  'use strict';

  var frame = document.querySelector('.deck-frame');
  var stage = document.querySelector('.deck-stage');
  var slides = Array.prototype.slice.call(document.querySelectorAll('.deck .slide'));
  var current = 0;
  var printMode = /\?print(?:=|$)/.test(window.location.search) || window.location.hash === '#print';

  function getQueryLang() {
    var m = window.location.search.match(/[?&]lang=(es|en)(?:&|$)/);
    return m ? m[1] : null;
  }

  function applyLang(lang) {
    lang = lang === 'en' ? 'en' : 'es';
    document.documentElement.lang = lang;
    document.body.classList.toggle('lang-en', lang === 'en');
    document.body.classList.toggle('lang-es', lang === 'es');
    document.querySelectorAll('.lang-switch [data-lang]').forEach(function (btn) {
      var on = btn.getAttribute('data-lang') === lang;
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    try { localStorage.setItem('energy-coop-deck-lang', lang); } catch (_e) { /* ignore */ }
    return lang;
  }

  function initLang() {
    var lang = getQueryLang();
    if (!lang) {
      try { lang = localStorage.getItem('energy-coop-deck-lang'); } catch (_e2) { lang = null; }
    }
    applyLang(lang || 'es');
    var sw = document.getElementById('lang-switch');
    if (sw) {
      sw.querySelectorAll('[data-lang]').forEach(function (btn) {
        btn.addEventListener('click', function (ev) {
          ev.stopPropagation();
          applyLang(btn.getAttribute('data-lang'));
        });
      });
    }
  }

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
    if (el.closest && el.closest('.deck-chrome, .deck-menu, .lang-switch')) return true;
    return false;
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

  initLang();
  initSlideNumbers();
  initDots();
  initMenu();

  if (printMode) {
    document.body.classList.add('print-all');
    slides.forEach(function (s) { s.classList.add('active'); });
  } else {
    setSlide(slideFromHash());
    window.addEventListener('resize', scaleStage);
    window.addEventListener('hashchange', function () { setSlide(slideFromHash()); });
    document.addEventListener('keydown', onKey);
    if (stage) stage.addEventListener('click', onStageClick);
    scaleStage();
  }
})();
