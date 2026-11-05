(function() {
  'use strict';
  if (!/\/diagnostico/.test(window.location.pathname)) return;

  var LEAD_ENDPOINT = 'https://agents.cleantechhub.net/diagnostico/lead';
  var firedStart = false;

  function collectAnswers() {
    var answers = {};
    var radios = document.querySelectorAll('input[type="radio"]:checked');
    radios.forEach(function(r) {
      var label = r.closest('.option-card, .quiz-option, label, div');
      var text = label ? label.textContent.trim().substring(0, 100) : r.value;
      var section = r.closest('[id^="sec-"], .quiz-section, .elementor-widget');
      var key = section ? section.id || 'q' : 'q';
      answers[key] = text;
    });
    return answers;
  }

  function sendLead(partial) {
    var payload = {
      email: window.userEmail || '',
      name: window.userName || '',
      source: 'diagnostico',
      green_score: partial ? null : (window.finalScore || window.greenScore || null),
      answers: collectAnswers(),
      contact_consent: false,
      submitted_at: new Date().toISOString(),
      partial: !!partial
    };
    if (!payload.email) return;
    try {
      var consent = document.getElementById('newsletter-consent');
      if (consent) payload.contact_consent = consent.checked;
    } catch(e) {}
    fetch(LEAD_ENDPOINT, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload)
    }).catch(function(){});
  }

  function patchFunctions() {
    if (typeof window.goNext !== 'function') return false;

    var _origGoNext = window.goNext;
    window.goNext = function() {
      if (!firedStart) {
        firedStart = true;
        gtag('event', 'diagnostic_start', {
          event_category: 'diagnostico',
          event_label: 'wizard_start'
        });
      }
      return _origGoNext.apply(this, arguments);
    };

    var _origContinueAfterGate = window.continueAfterGate;
    window.continueAfterGate = function() {
      var result = _origContinueAfterGate.apply(this, arguments);
      if (window.userEmail) {
        gtag('event', 'diagnostic_email_captured', {
          event_category: 'diagnostico',
          event_label: 'email_gate'
        });
        sendLead(true);
      }
      return result;
    };

    var _origCalcScore = window.calcScore;
    window.calcScore = function() {
      var result = _origCalcScore.apply(this, arguments);
      gtag('event', 'diagnostic_score_calculated', {
        event_category: 'diagnostico',
        event_label: 'score_calc',
        value: window.finalScore || window.greenScore || 0
      });
      return result;
    };

    var _origShowResults = window.showResults;
    window.showResults = function() {
      var result = _origShowResults.apply(this, arguments);
      gtag('event', 'diagnostic_complete', {
        event_category: 'diagnostico',
        event_label: 'results_shown',
        value: window.finalScore || window.greenScore || 0
      });
      sendLead(false);
      return result;
    };

    return true;
  }

  function injectConsent() {
    var gateEmail = document.getElementById('gate-email');
    if (!gateEmail) return;
    var gateSection = gateEmail.closest('div');
    if (!gateSection || document.getElementById('newsletter-consent')) return;
    var btn = gateSection.querySelector('button');
    var container = btn ? btn.parentElement : gateSection;
    var lbl = document.createElement('label');
    lbl.style.cssText = 'font-size:11px;display:flex;align-items:flex-start;gap:6px;margin-top:8px;color:#666;';
    lbl.innerHTML = '<input type="checkbox" id="newsletter-consent" style="margin-top:2px;">' +
      'Quiero recibir tips de financiamiento verde (max 1/semana)';
    container.appendChild(lbl);
  }

  function init() {
    if (!patchFunctions()) {
      setTimeout(init, 500);
      return;
    }
    injectConsent();
  }

  if (document.readyState === 'complete') {
    init();
  } else {
    window.addEventListener('load', init);
  }
})();
