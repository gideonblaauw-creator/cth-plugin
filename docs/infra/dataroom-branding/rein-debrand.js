(function () {
  "use strict";

  var REIN_TITLE = "REIN Hubs Data Room";
  var LOGO_SRC = "/icons/rein-white-orange.png";
  var BRAND_ID = "rein-dataroom-brand";
  var DEBOUNCE_MS = 200;

  var observer = null;
  var debounceTimer = null;
  var rafId = 0;

  function isEditorSubtree(el) {
    if (!el || el.nodeType !== 1) return false;
    if (el.isContentEditable) return true;
    if (el.closest) {
      return !!el.closest(
        '[contenteditable="true"], .ProseMirror, [class*="ProseMirror"]'
      );
    }
    return false;
  }

  function shouldSkipNode(node) {
    if (!node) return true;
    if (node.nodeType === 1) return isEditorSubtree(node);
    if (node.nodeType === 3) {
      var parent = node.parentElement;
      return parent ? isEditorSubtree(parent) : false;
    }
    return false;
  }

  function ensureStyles() {
    if (document.getElementById("rein-brand-css")) return;
    var link = document.createElement("link");
    link.id = "rein-brand-css";
    link.rel = "stylesheet";
    link.href = "/rein-brand.css";
    document.head.appendChild(link);
  }

  function patchTitle() {
    if (document.title !== REIN_TITLE) {
      document.title = REIN_TITLE;
    }
    var meta = document.querySelector('meta[name="apple-mobile-web-app-title"]');
    if (meta && meta.getAttribute("content") !== REIN_TITLE) {
      meta.setAttribute("content", REIN_TITLE);
    }
    var theme = document.querySelector('meta[name="theme-color"]');
    if (theme) {
      theme.setAttribute("content", "#335d4f");
    }
  }

  function hideDocmostBranding(root) {
    if (!root || !root.querySelectorAll) return;
    root.querySelectorAll('a[href*="docmost.com"]').forEach(function (el) {
      if (isEditorSubtree(el)) return;
      var footer = el.closest("footer");
      if (footer) {
        footer.style.display = "none";
      } else {
        el.style.display = "none";
      }
    });
    root.querySelectorAll("footer").forEach(function (footer) {
      if (isEditorSubtree(footer)) return;
      var text = (footer.textContent || "").toLowerCase();
      if (text.indexOf("powered by") !== -1 && text.indexOf("docmost") !== -1) {
        footer.style.display = "none";
      }
    });
  }

  function patchText(root) {
    if (!root || shouldSkipNode(root)) return;

    var filter = {
      acceptNode: function (node) {
        if (shouldSkipNode(node)) return NodeFilter.FILTER_REJECT;
        var parent = node.parentElement;
        while (parent) {
          if (isEditorSubtree(parent)) return NodeFilter.FILTER_REJECT;
          parent = parent.parentElement;
        }
        return NodeFilter.FILTER_ACCEPT;
      },
    };

    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, filter);
    var node;
    while ((node = walker.nextNode())) {
      if (!node.nodeValue) continue;
      if (node.nodeValue.indexOf("Docmost") !== -1) {
        node.nodeValue = node.nodeValue.split("Docmost").join("REIN Hubs");
      }
      if (/Powered by/i.test(node.nodeValue)) {
        node.nodeValue = node.nodeValue
          .replace(/Powered by\s*REIN Hubs?/gi, "")
          .trim();
      }
    }

    if (!root.querySelectorAll) return;
    root.querySelectorAll('img[alt="Docmost"], img[alt*="Docmost"]').forEach(function (img) {
      if (isEditorSubtree(img)) return;
      img.alt = REIN_TITLE;
      if (/docmost/i.test(img.src || "")) {
        img.style.display = "none";
      }
    });
  }

  function injectHeaderBrand() {
    var header =
      document.querySelector('header[class*="_header_"]') ||
      document.querySelector('[class*="_header_"]');
    if (!header || document.getElementById(BRAND_ID)) return;

    var left =
      header.querySelector('[class*="_headerLeft_"]') ||
      header.querySelector('[class*="_headerInner_"]') ||
      header;

    var brand = document.createElement("a");
    brand.id = BRAND_ID;
    brand.href = "/";
    brand.setAttribute("aria-label", REIN_TITLE);
    brand.innerHTML =
      '<img src="' +
      LOGO_SRC +
      '" alt="" width="120" height="32" decoding="async" />' +
      "<span>REIN Hubs</span>";

    left.insertBefore(brand, left.firstChild);
  }

  function disconnectObserver() {
    if (observer) observer.disconnect();
  }

  function connectObserver() {
    if (!observer || !document.documentElement) return;
    observer.observe(document.documentElement, {
      childList: true,
      subtree: true,
    });
  }

  function patchRoots(roots) {
    disconnectObserver();
    try {
      ensureStyles();
      patchTitle();
      roots.forEach(function (root) {
        if (root.nodeType === 1) {
          hideDocmostBranding(root);
          patchText(root);
        } else if (root.nodeType === 3 && root.parentElement) {
          hideDocmostBranding(root.parentElement);
          patchText(root.parentElement);
        }
      });
      injectHeaderBrand();
    } finally {
      connectObserver();
    }
  }

  function runInitial() {
    disconnectObserver();
    try {
      ensureStyles();
      patchTitle();
      if (document.body) {
        hideDocmostBranding(document.body);
        patchText(document.body);
        injectHeaderBrand();
      }
    } finally {
      connectObserver();
    }
  }

  function uniqueRoots(nodes) {
    var seen = new Set();
    var out = [];
    nodes.forEach(function (node) {
      if (!node || shouldSkipNode(node)) return;
      var root = node.nodeType === 1 ? node : node.parentElement;
      if (!root || shouldSkipNode(root) || seen.has(root)) return;
      seen.add(root);
      out.push(root);
    });
    return out;
  }

  function rootsFromMutations(records) {
    var added = [];
    records.forEach(function (record) {
      if (record.type !== "childList") return;
      record.addedNodes.forEach(function (node) {
        added.push(node);
      });
    });
    return uniqueRoots(added);
  }

  function schedulePatch(records) {
    if (debounceTimer) clearTimeout(debounceTimer);
    debounceTimer = setTimeout(function () {
      debounceTimer = null;
      if (rafId) cancelAnimationFrame(rafId);
      rafId = requestAnimationFrame(function () {
        rafId = 0;
        var roots = records ? rootsFromMutations(records) : [];
        if (roots.length) {
          patchRoots(roots);
        } else {
          disconnectObserver();
          try {
            patchTitle();
            injectHeaderBrand();
          } finally {
            connectObserver();
          }
        }
      });
    }, DEBOUNCE_MS);
  }

  observer = new MutationObserver(function (records) {
    schedulePatch(records);
  });

  runInitial();

})();
