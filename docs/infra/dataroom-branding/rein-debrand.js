(function () {
  "use strict";

  var REIN_TITLE = "REIN Hubs Data Room";
  var LOGO_SRC = "/icons/rein-white-orange.png";
  var BRAND_ID = "rein-dataroom-brand";

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
    root.querySelectorAll('a[href*="docmost.com"]').forEach(function (el) {
      var footer = el.closest("footer");
      if (footer) {
        footer.style.display = "none";
      } else {
        el.style.display = "none";
      }
    });
    root.querySelectorAll("footer").forEach(function (footer) {
      var text = (footer.textContent || "").toLowerCase();
      if (text.indexOf("powered by") !== -1 && text.indexOf("docmost") !== -1) {
        footer.style.display = "none";
      }
    });
  }

  function patchText(root) {
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
    var node;
    while ((node = walker.nextNode())) {
      if (!node.nodeValue) continue;
      if (node.nodeValue.indexOf("Docmost") !== -1) {
        node.nodeValue = node.nodeValue.split("Docmost").join("REIN Hubs");
      }
      if (/Powered by/i.test(node.nodeValue)) {
        node.nodeValue = node.nodeValue.replace(/Powered by\s*REIN Hubs?/gi, "").trim();
      }
    }
    root.querySelectorAll('img[alt="Docmost"], img[alt*="Docmost"]').forEach(function (img) {
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

  function run() {
    ensureStyles();
    patchTitle();
    if (document.body) {
      hideDocmostBranding(document.body);
      patchText(document.body);
      injectHeaderBrand();
    }
  }

  run();

  var obs = new MutationObserver(function () {
    run();
  });
  obs.observe(document.documentElement, {
    childList: true,
    subtree: true,
    characterData: true,
  });
})();
