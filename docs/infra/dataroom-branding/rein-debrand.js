(function () {
  var REIN_TITLE = "REIN Hubs Data Room";
  function patchTitle() {
    if (document.title !== REIN_TITLE) {
      document.title = REIN_TITLE;
    }
    var meta = document.querySelector('meta[name="apple-mobile-web-app-title"]');
    if (meta && meta.getAttribute("content") !== REIN_TITLE) {
      meta.setAttribute("content", REIN_TITLE);
    }
  }
  function patchText(root) {
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
    var node;
    while ((node = walker.nextNode())) {
      if (node.nodeValue && node.nodeValue.indexOf("Docmost") !== -1) {
        node.nodeValue = node.nodeValue.split("Docmost").join(REIN_TITLE);
      }
    }
    root.querySelectorAll('img[alt="Docmost"]').forEach(function (img) {
      img.alt = REIN_TITLE;
    });
  }
  function run() {
    patchTitle();
    if (document.body) {
      patchText(document.body);
    }
  }
  run();
  var obs = new MutationObserver(function () {
    patchTitle();
    if (document.body) {
      patchText(document.body);
    }
  });
  obs.observe(document.documentElement, {
    childList: true,
    subtree: true,
    characterData: true,
  });
})();
