(function () {
  'use strict';

  var stage = document.querySelector('.deck-stage');
  var slides = Array.prototype.slice.call(document.querySelectorAll('.deck .slide'));
  var current = 0;
  var printMode = /\?print(?:=|$)/.test(window.location.search) || window.location.hash === '#print';

  function scaleStage() {
    if (!stage || printMode) return;
    var vw = window.innerWidth;
    var vh = window.innerHeight;
    var sw = 1920;
    var sh = 1080;
    var scale = Math.min(vw / sw, vh / sh);
    stage.style.transform = 'scale(' + scale + ')';
  }

  function setSlide(index) {
    if (!slides.length) return;
    index = Math.max(0, Math.min(slides.length - 1, index));
    slides.forEach(function (s, i) {
      s.classList.toggle('active', i === index);
    });
    current = index;
    var numEls = document.querySelectorAll('.footer .slide-num');
    numEls.forEach(function (el) {
      el.textContent = (index + 1) + ' / ' + slides.length;
    });
    if (!printMode) {
      var hash = index === 0 ? '#1' : '#' + (index + 1);
      if (window.location.hash !== hash) {
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

  function onKey(e) {
    if (printMode) return;
    var k = e.key;
    if (k === 'ArrowRight' || k === ' ' || k === 'PageDown') {
      e.preventDefault();
      next();
    } else if (k === 'ArrowLeft' || k === 'PageUp') {
      e.preventDefault();
      prev();
    }
  }

  function onClick(e) {
    if (printMode) return;
    var rect = stage.getBoundingClientRect();
    var x = e.clientX - rect.left;
    if (x > rect.width / 2) next();
    else prev();
  }

  if (printMode) {
    document.body.classList.add('print-all');
    slides.forEach(function (s) {
      s.classList.add('active');
    });
  } else {
    setSlide(slideFromHash());
    window.addEventListener('resize', scaleStage);
    window.addEventListener('hashchange', function () {
      setSlide(slideFromHash());
    });
    document.addEventListener('keydown', onKey);
    if (stage) stage.addEventListener('click', onClick);
    scaleStage();
  }
})();
