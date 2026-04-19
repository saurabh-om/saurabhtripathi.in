// motion.js — kinetic type, counters, parallax, rails, magnetic buttons
(function () {
  'use strict';

  var prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---------------------------------------------------------------
  // Word-by-word reveal (hero headlines with .reveal-word spans)
  // ---------------------------------------------------------------
  (function () {
    var words = document.querySelectorAll('.reveal-word');
    if (!words.length) return;
    if (prefersReduced) { words.forEach(function (w) { w.classList.add('is-in'); }); return; }
    if (!('IntersectionObserver' in window)) { words.forEach(function (w) { w.classList.add('is-in'); }); return; }

    words.forEach(function (w, i) { w.style.transitionDelay = (i * 80) + 'ms'; });

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('is-in');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.2 });
    words.forEach(function (w) { io.observe(w); });
  })();

  // ---------------------------------------------------------------
  // Morphing word rotator  <span class="morph"><span data-words="a,b,c"></span></span>
  // ---------------------------------------------------------------
  (function () {
    var rotators = document.querySelectorAll('[data-rotate]');
    rotators.forEach(function (root) {
      var words = (root.getAttribute('data-rotate') || '').split('|').map(function (s) { return s.trim(); }).filter(Boolean);
      if (words.length < 2) return;
      var slot = root.querySelector('.morph-slot');
      if (!slot) return;
      // Pre-create children
      var nodes = words.map(function (w, i) {
        var span = document.createElement('span');
        span.className = 'morph-word' + (i === 0 ? ' is-in' : '');
        span.textContent = w;
        slot.appendChild(span);
        return span;
      });
      // Size slot to widest word
      var sizer = document.createElement('span');
      sizer.style.visibility = 'hidden';
      sizer.style.position = 'absolute';
      sizer.style.whiteSpace = 'nowrap';
      sizer.style.fontFamily = window.getComputedStyle(nodes[0]).fontFamily;
      sizer.style.fontWeight = window.getComputedStyle(nodes[0]).fontWeight;
      sizer.style.fontSize = window.getComputedStyle(nodes[0]).fontSize;
      sizer.style.letterSpacing = window.getComputedStyle(nodes[0]).letterSpacing;
      document.body.appendChild(sizer);
      var maxW = 0;
      words.forEach(function (w) {
        sizer.textContent = w;
        if (sizer.offsetWidth > maxW) maxW = sizer.offsetWidth;
      });
      document.body.removeChild(sizer);
      slot.style.width = (maxW + 8) + 'px';

      if (prefersReduced) return;

      var idx = 0;
      setInterval(function () {
        nodes[idx].classList.remove('is-in');
        nodes[idx].classList.add('is-out');
        idx = (idx + 1) % nodes.length;
        nodes[idx].classList.remove('is-out');
        setTimeout(function () { nodes[idx].classList.add('is-in'); }, 40);
      }, 2400);
    });
  })();

  // ---------------------------------------------------------------
  // Counter — .count with data-target="20", data-prefix, data-suffix
  // ---------------------------------------------------------------
  (function () {
    var counts = document.querySelectorAll('.count[data-target]');
    if (!counts.length) return;
    function fmt(n, decimals) { return decimals ? n.toFixed(decimals) : Math.round(n).toString(); }
    function run(el) {
      var target = parseFloat(el.getAttribute('data-target'));
      var decimals = (el.getAttribute('data-decimals') | 0);
      var prefix = el.getAttribute('data-prefix') || '';
      var suffix = el.getAttribute('data-suffix') || '';
      var dur = parseInt(el.getAttribute('data-dur') || '1400', 10);
      if (prefersReduced) { el.textContent = prefix + fmt(target, decimals) + suffix; return; }
      var start = performance.now();
      function tick(now) {
        var t = Math.min(1, (now - start) / dur);
        var eased = 1 - Math.pow(1 - t, 3);
        el.textContent = prefix + fmt(target * eased, decimals) + suffix;
        if (t < 1) requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
    }
    if (!('IntersectionObserver' in window)) { counts.forEach(run); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { run(e.target); io.unobserve(e.target); } });
    }, { threshold: 0.5 });
    counts.forEach(function (el) { io.observe(el); });
  })();

  // ---------------------------------------------------------------
  // Hero image parallax — .parallax-img gets subtle translate+scale
  // ---------------------------------------------------------------
  (function () {
    if (prefersReduced) return;
    var imgs = document.querySelectorAll('[data-parallax]');
    if (!imgs.length) return;
    var ticking = false;
    function onScroll() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        var vh = window.innerHeight;
        imgs.forEach(function (img) {
          var rect = img.getBoundingClientRect();
          if (rect.bottom < -100 || rect.top > vh + 100) return;
          var speed = parseFloat(img.getAttribute('data-parallax')) || 0.08;
          var center = rect.top + rect.height / 2;
          var offset = (center - vh / 2) * speed;
          img.style.transform = 'translate3d(0,' + offset.toFixed(2) + 'px,0) scale(1.06)';
        });
        ticking = false;
      });
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  })();

  // ---------------------------------------------------------------
  // Rail scroll — prev/next buttons, keyboard arrows
  // ---------------------------------------------------------------
  (function () {
    document.querySelectorAll('[data-rail]').forEach(function (rail) {
      var controls = document.querySelectorAll('[data-rail-ctl="' + rail.dataset.rail + '"]');
      function step(dir) {
        var card = rail.querySelector(':scope > *');
        if (!card) return;
        var delta = card.getBoundingClientRect().width + 20;
        rail.scrollBy({ left: delta * dir, behavior: prefersReduced ? 'auto' : 'smooth' });
      }
      controls.forEach(function (btn) {
        btn.addEventListener('click', function () { step(btn.dataset.dir === 'prev' ? -1 : 1); });
      });
      rail.setAttribute('tabindex', '0');
      rail.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight') { step(1); e.preventDefault(); }
        if (e.key === 'ArrowLeft')  { step(-1); e.preventDefault(); }
      });
    });
  })();

  // ---------------------------------------------------------------
  // Scroll-reveal for .reveal blocks (existing, kept)
  // ---------------------------------------------------------------
  (function () {
    var els = document.querySelectorAll('.reveal');
    if (!els.length) return;
    if (prefersReduced || !('IntersectionObserver' in window)) {
      els.forEach(function (e) { e.classList.add('is-in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.15 });
    els.forEach(function (el) { io.observe(el); });
  })();

})();
