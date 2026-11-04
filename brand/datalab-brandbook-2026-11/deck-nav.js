(function () {
  "use strict";

  function applyExportSlide(index) {
    document.body.classList.add("export-one");
    document.querySelectorAll(".topbar, .site-footer, .pdf-dl-fixed").forEach(function (el) {
      el.style.display = "none";
    });
    var reset =
      "position:static!important;display:block!important;width:1920px!important;height:1080px!important;overflow:visible!important;transform:none!important;margin:0!important;padding:0!important;";
    ["deck-viewport", "deck-frame", "deck-stage", "deck"].forEach(function (cls) {
      var el = document.querySelector("." + cls);
      if (el) el.style.cssText = reset;
    });
    slides.forEach(function (s, i) {
      s.style.cssText =
        i === index
          ? "display:flex!important;position:relative!important;width:1920px!important;height:1080px!important;inset:auto!important;"
          : "display:none!important;";
    });
  }

  var params = new URLSearchParams(window.location.search);
  var exportSlide = params.get("exportSlide");

  var frame = document.querySelector(".deck-frame");
  var stage = document.querySelector(".deck-stage");
  var slides = Array.prototype.slice.call(document.querySelectorAll(".deck .slide"));
  var current = 0;
  var printMode =
    /\?print(?:=|$)/.test(window.location.search) || window.location.hash === "#print";

  function scaleStage() {
    if (!frame || !stage || printMode) return;
    var vw = window.innerWidth;
    var vh = window.innerHeight - 120;
    var scale = Math.min(vw / 1920, vh / 1080) * 0.96;
    frame.style.width = Math.round(1920 * scale) + "px";
    frame.style.height = Math.round(1080 * scale) + "px";
    stage.style.transform = "scale(" + scale + ")";
  }

  function setSlide(index) {
    if (!slides.length) return;
    index = Math.max(0, Math.min(slides.length - 1, index));
    current = index;
    slides.forEach(function (s, i) {
      s.classList.toggle("active", i === index);
    });
    var id = slides[index].id;
    if (id) {
      history.replaceState(null, "", "#" + id);
    }
  }

  function slideFromHash() {
    var hash = window.location.hash.replace("#", "");
    if (!hash) return;
    slides.forEach(function (s, i) {
      if (s.id === hash) setSlide(i);
    });
  }

  document.querySelectorAll(".nav a[data-slide]").forEach(function (a) {
    a.addEventListener("click", function (e) {
      e.preventDefault();
      var id = a.getAttribute("href").replace("#", "");
      slides.forEach(function (s, i) {
        if (s.id === id) setSlide(i);
      });
    });
  });

  window.addEventListener("keydown", function (e) {
    if (printMode) return;
    if (e.key === "ArrowRight" || e.key === "PageDown") setSlide(current + 1);
    if (e.key === "ArrowLeft" || e.key === "PageUp") setSlide(current - 1);
  });

  window.addEventListener("resize", scaleStage);
  window.addEventListener("hashchange", slideFromHash);

  if (exportSlide !== null && exportSlide !== "") {
    var idx = parseInt(exportSlide, 10);
    if (!Number.isNaN(idx)) applyExportSlide(idx);
  } else if (printMode) {
    document.body.classList.add("print-all");
  } else {
    setSlide(0);
    slideFromHash();
    scaleStage();
  }
})();
