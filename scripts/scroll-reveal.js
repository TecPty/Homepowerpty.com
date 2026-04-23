(function () {
    'use strict';

    var MOBILE_BP = 768;

    function isMobile() {
        return window.innerWidth <= MOBILE_BP;
    }

    var cards  = document.querySelectorAll('.featured-products-grid .product');
    var strips = document.querySelectorAll('.showcase-strips .showcase-strip');

    function showAll() {
        cards.forEach(function (c) { c.classList.add('product--visible'); });
        strips.forEach(function (s) {
            s.classList.remove('strip--init');
            s.classList.add('strip--visible');
        });
    }

    // On desktop or if IntersectionObserver not supported: show everything
    if (!isMobile() || !window.IntersectionObserver) {
        showAll();
        window.addEventListener('resize', function () {
            if (!isMobile()) showAll();
        });
        return;
    }

    // Progressive enhancement: JS hides strips via class.
    // If JS never runs or IO fails, CSS default = visible.
    strips.forEach(function (s) { s.classList.add('strip--init'); });

    // ── PRODUCT CARDS observer ───────────────────────────
    var cardObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('product--visible');
            } else if (entry.boundingClientRect.top > 0) {
                entry.target.classList.remove('product--visible');
            }
        });
    }, { threshold: 0.08, rootMargin: '0px 0px -30px 0px' });

    cards.forEach(function (c) { cardObserver.observe(c); });

    // ── SHOWCASE STRIPS observer ─────────────────────────
    var stripObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.remove('strip--init');
                entry.target.classList.add('strip--visible');
            } else if (entry.boundingClientRect.top > 0) {
                entry.target.classList.remove('strip--visible');
                entry.target.classList.add('strip--init');
            }
        });
    }, { threshold: 0.05 });

    strips.forEach(function (s) { stripObserver.observe(s); });

    // Resize into desktop
    window.addEventListener('resize', function () {
        if (!isMobile()) {
            cardObserver.disconnect();
            stripObserver.disconnect();
            showAll();
        }
    });
})();
