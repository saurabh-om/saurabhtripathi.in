// studio.js: menu, header state, reveals, counters. No scroll listeners.
(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasIO = 'IntersectionObserver' in window;

  // --- Mobile menu ---------------------------------------------------------
  var toggle = document.querySelector('.nav-toggle');
  function setMenu(open) {
    document.body.classList.toggle('nav-open', open);
    document.body.style.overflow = open ? 'hidden' : '';
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  if (toggle) {
    toggle.addEventListener('click', function () {
      setMenu(!document.body.classList.contains('nav-open'));
    });
    document.querySelectorAll('.mobile-menu a').forEach(function (a) {
      a.addEventListener('click', function () { setMenu(false); });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && document.body.classList.contains('nav-open')) {
        setMenu(false);
        toggle.focus();
      }
    });
  }

  // --- Header goes solid once the top sentinel leaves the viewport ---------
  var header = document.querySelector('.site-header');
  var sentinel = document.querySelector('[data-header-sentinel]');
  if (header && sentinel && hasIO) {
    new IntersectionObserver(function (entries) {
      header.classList.toggle('is-solid', !entries[0].isIntersecting);
    }).observe(sentinel);
  } else if (header) {
    header.classList.add('is-solid');
  }

  // --- Reveals: hero on load, sections on enter ----------------------------
  var hero = document.querySelector('.hero');
  var groups = document.querySelectorAll('[data-reveal]');
  if (reduce || !hasIO) {
    if (hero) hero.classList.add('is-in');
    groups.forEach(function (g) { g.classList.add('is-in'); });
  } else {
    if (hero) requestAnimationFrame(function () {
      requestAnimationFrame(function () { hero.classList.add('is-in'); });
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('is-in');
        io.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.05 });
    groups.forEach(function (g) {
      g.querySelectorAll('.rise').forEach(function (el, i) {
        el.style.setProperty('--d', Math.min(i, 6) * 80 + 'ms');
      });
      io.observe(g);
    });
  }

  // --- Counters: real values ship in the HTML, animate only when allowed ---
  var counts = document.querySelectorAll('[data-count]');
  if (counts.length && !reduce && hasIO) {
    var run = function (el) {
      var target = parseFloat(el.getAttribute('data-count'));
      var start = performance.now();
      var dur = 1400;
      (function tick(now) {
        var t = Math.min(1, (now - start) / dur);
        el.textContent = Math.round(target * (1 - Math.pow(1 - t, 3)));
        if (t < 1) requestAnimationFrame(tick);
      })(start);
    };
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        run(e.target);
        cio.unobserve(e.target);
      });
    }, { threshold: 0.6 });
    counts.forEach(function (el) { el.textContent = '0'; cio.observe(el); });
  }
})();
