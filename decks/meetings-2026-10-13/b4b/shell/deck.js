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
    var sw = 1920;
    var sh = 1080;
    var scale = Math.min(vw / sw, vh / sh) * 0.96;
    frame.style.width = Math.round(sw * scale) + 'px';
    frame.style.height = Math.round(sh * scale) + 'px';
    stage.style.transform = 'scale(' + scale + ')';
  }

  function initSlideNumbers() {
    var total = slides.length;
    slides.forEach(function (s, i) {
      var el = s.querySelector('.slide-num');
      if (el) {
        el.textContent = i + 1 + ' / ' + total;
      }
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
      var hash = index === 0 ? '#1' : '#' + (index + 1);
      if (window.location.hash !== hash && window.location.hash !== '#print') {
        history.replaceState(null, '', hash);
      }
    }
  }

  function next() {
    setSlide(current + 1);
  }

  function prev() {
    setSlide(current - 1);
  }

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
    if (el.closest && el.closest('.deck-chrome, .deck-menu, .lightbox, .expand-card, .lightbox-open')) return true;
    return false;
  }

  function onKey(e) {
    if (printMode) return;
    var menu = document.getElementById('deck-menu');
    if (menu && !menu.hidden && e.key === 'Escape') {
      menu.hidden = true;
      return;
    }
    var lb = document.getElementById('lightbox');
    if (lb && !lb.hidden && e.key === 'Escape') {
      lb.hidden = true;
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
      b.title = 'Diapositiva ' + (i + 1);
      b.setAttribute('aria-label', 'Ir a diapositiva ' + (i + 1));
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
      var title = slide.getAttribute('data-menu-title') || 'Diapositiva ' + (i + 1);
      b.textContent = i + 1 + '. ' + title;
      b.addEventListener('click', function () {
        menu.hidden = true;
        setSlide(i);
      });
      li.appendChild(b);
      list.appendChild(li);
    });

    btnMenu.addEventListener('click', function (ev) {
      ev.stopPropagation();
      menu.hidden = !menu.hidden;
    });

    menu.addEventListener('click', function (ev) {
      if (ev.target === menu) menu.hidden = true;
    });
  }

  function initQuestionsToggle() {
    var btn = document.getElementById('btn-questions');
    if (!btn) return;
    btn.addEventListener('click', function (ev) {
      ev.stopPropagation();
      var on = document.body.classList.toggle('show-questions');
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      btn.textContent = on ? 'Ocultar preguntas' : 'Mostrar preguntas';
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

  if (printMode) {
    document.body.classList.add('print-all');
    document.body.classList.add('show-questions');
    slides.forEach(function (s) {
      s.classList.add('active');
    });
    document.querySelectorAll('.expand-body').forEach(function (el) {
      el.classList.add('open');
    });
  } else {
    setSlide(slideFromHash());
    window.addEventListener('resize', scaleStage);
    window.addEventListener('hashchange', function () {
      setSlide(slideFromHash());
    });
    document.addEventListener('keydown', onKey);
    if (stage) stage.addEventListener('click', onStageClick);
    scaleStage();
  }
})();
