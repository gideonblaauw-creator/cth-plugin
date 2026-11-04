/**
 * Optional: call before print or PDF export in custom pipelines.
 * export-deck-pdf.py runs the same logic in the page context.
 */
(function cthDeckPdfPrep() {
  document.querySelectorAll(".reveal").forEach(function (el) {
    el.classList.add("visible");
  });
  document.querySelectorAll("[data-count]").forEach(function (el) {
    var target = el.getAttribute("data-count");
    if (target !== null && target !== "") {
      el.textContent = target;
    }
  });
  document.body.classList.add("print-all");
})();
