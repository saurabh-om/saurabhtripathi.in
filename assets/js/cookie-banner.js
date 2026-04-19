// cookie-banner.js — minimal consent + conditional GA4 loader
(function () {
  'use strict';

  var GA_ID = 'G-XXXXXXXXXX'; // replace with real GA4 Measurement ID before launch
  var KEY = 'st_consent_v1';

  function loadGA() {
    if (window.__gaLoaded) return;
    window.__gaLoaded = true;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', GA_ID, { anonymize_ip: true });
  }

  var stored;
  try { stored = localStorage.getItem(KEY); } catch (e) { stored = null; }

  if (stored === 'accept') {
    loadGA();
    return;
  }
  if (stored === 'decline') return;

  // No decision yet — show banner
  function renderBanner() {
    var b = document.createElement('div');
    b.className = 'cookie-banner';
    b.setAttribute('role', 'region');
    b.setAttribute('aria-label', 'Cookie consent');
    b.innerHTML =
      '<p>This site uses cookies for basic analytics. Read the <a href="/privacy.html">privacy notice</a>.</p>' +
      '<div class="cookie-actions">' +
        '<button class="decline" type="button">Decline</button>' +
        '<button class="accept" type="button">Accept</button>' +
      '</div>';
    document.body.appendChild(b);
    requestAnimationFrame(function () { b.classList.add('is-visible'); });

    b.querySelector('.accept').addEventListener('click', function () {
      try { localStorage.setItem(KEY, 'accept'); } catch (e) {}
      b.remove();
      loadGA();
    });
    b.querySelector('.decline').addEventListener('click', function () {
      try { localStorage.setItem(KEY, 'decline'); } catch (e) {}
      b.remove();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderBanner);
  } else {
    renderBanner();
  }

})();
