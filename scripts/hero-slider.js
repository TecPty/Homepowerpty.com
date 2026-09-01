
(function () {
  'use strict';

  var BASE = (function () {
    var scripts = document.querySelectorAll('script[src]');
    for (var i = 0; i < scripts.length; i++) {
      var src = scripts[i].getAttribute('src');
      if (src && src.indexOf('hero-slider') !== -1) {
        return src.replace(/scripts\/hero-slider\.js.*$/, '');
      }
    }
    var loc = window.location.href;
    return loc.substring(0, loc.lastIndexOf('/') + 1);
  })();

  var SLIDES = [
    {
      category: 'Cafeteras',
      title: 'Disfruta tu café,<br>todos los días',
      desc: 'Prácticas, elegantes y perfectas para tu rutina.',
      img: BASE + 'productos/cafeteras/cm02/img/BRAND_COMMERCIAL.webp',
      href: BASE + 'productos/cafeteras/cm02/'
    },
    {
      category: 'Air Fryer',
      title: 'Cocina sin aceite,<br>vive mejor',
      desc: 'Digital 4.5L con 8 programas automáticos.',
      img: BASE + 'productos/freidoras-de-aire/af3201/img/LIFESTYLE_DARK_HERO.png',
      href: BASE + 'productos/freidoras-de-aire/af3201/'
    },
    {
      category: 'Sandwicheras',
      title: 'El desayuno perfecto<br>cada día',
      desc: 'Placas antiadherentes, diseño compacto.',
      img: BASE + 'productos/sandwicheras/sj35/img/LIFESTYLE_DARK.webp',
      href: BASE + 'productos/sandwicheras/sj35/'
    },
    {
      category: 'Planchas',
      title: 'Potencia y precisión<br>para tu ropa',
      desc: 'Base cerámica, control de temperatura.',
      img: BASE + 'productos/planchas/r91171b/img/LIFESTYLE_MAN.webp',
      href: BASE + 'productos/planchas/r91171b/'
    },
    {
      category: 'Licuadoras',
      title: 'Potencia en cada<br>preparación',
      desc: 'Motor 500W, jarra de vidrio 1.5L.',
      img: BASE + 'productos/licuadoras/mm-931/img/LIFESTYLE_DARK_HERO.png',
      href: BASE + 'productos/licuadoras/mm-931/'
    }
  ];

  /* ── Guard ───────────────────────────────────────────────── */
  var track = document.querySelector('.hero-slider__track');
  if (!track) return;

  /* ── Referencias DOM ─────────────────────────────────────── */
  var img      = document.querySelector('.hero-slider__img');
  var category = document.querySelector('.hero-slider__category');
  var title    = document.querySelector('.hero-slider__title');
  var desc     = document.querySelector('.hero-slider__desc');
  var cta      = document.querySelector('.hero-slider__cta');
  var overlay  = document.querySelector('.hero-slider__overlay');
  var dots     = document.querySelectorAll('.hero-slider__dot');
  var btnPrev  = document.getElementById('hero-prev');
  var btnNext  = document.getElementById('hero-next');
  var wrapper  = document.querySelector('.hero-slider__wrapper');
  var leftCol  = document.querySelector('.hero-left__col');
  var trustBar = document.querySelector('.hero-left__trust');

  if (!img || !overlay || !btnPrev || !btnNext) return;

  var originalParent = wrapper ? wrapper.parentNode : null;
  var originalNextSibling = wrapper ? wrapper.nextSibling : null;

  function placeSliderForViewport(isMobile) {
    if (!wrapper || !leftCol || !trustBar || !originalParent) return;

    if (isMobile) {
      if (!leftCol.contains(wrapper)) {
        leftCol.insertBefore(wrapper, trustBar);
      }
      return;
    }

    if (wrapper.parentNode === originalParent) return;

    if (originalNextSibling && originalNextSibling.parentNode === originalParent) {
      originalParent.insertBefore(wrapper, originalNextSibling);
    } else {
      originalParent.appendChild(wrapper);
    }
  }

  var mobileQuery = window.matchMedia('(max-width: 768px)');
  placeSliderForViewport(mobileQuery.matches);

  if (mobileQuery.addEventListener) {
    mobileQuery.addEventListener('change', function (event) {
      placeSliderForViewport(event.matches);
    });
  } else if (mobileQuery.addListener) {
    mobileQuery.addListener(function (event) {
      placeSliderForViewport(event.matches);
    });
  }

  /* ── Estado ──────────────────────────────────────────────── */
  var current   = 0;
  var total     = SLIDES.length;
  var timer     = null;
  var busy      = false;
  var DURATION  = 400;  /* ms de transición CSS */
  var INTERVAL  = 5000; /* ms entre slides */

  /* ── Precargar imágenes ──────────────────────────────────── */
  SLIDES.forEach(function (s) {
    var pre = new Image();
    pre.src = s.img;
  });

  /* ── Actualizar dots ─────────────────────────────────────── */
  function updateDots(idx) {
    dots.forEach(function (d, i) {
      d.classList.toggle('active', i === idx);
      d.setAttribute('aria-selected', i === idx ? 'true' : 'false');
    });
  }

  function normalizeIndex(idx) {
    return ((idx % total) + total) % total;
  }

  function applySlide(idx) {
    idx = normalizeIndex(idx);
    var slide = SLIDES[idx];

    img.src = slide.img;
    img.alt = slide.category + ' — ' + slide.title.replace(/<br>/g, ' ');
    category.textContent = slide.category;
    title.innerHTML = slide.title;
    desc.textContent = slide.desc;
    cta.href = slide.href;

    var eyebrow = document.querySelector('.hero-left__eyebrow');
    if (eyebrow) eyebrow.textContent = slide.category;

    updateDots(idx);
    current = idx;
  }

  function goTo(idx) {
    if (busy) return;
    busy = true;

    /* Normalizar índice */
    idx = normalizeIndex(idx);

    /* Fade out */
    img.classList.add('transitioning');
    overlay.classList.add('transitioning');

    setTimeout(function () {
      applySlide(idx);

      /* Fade in */
      img.classList.remove('transitioning');
      overlay.classList.remove('transitioning');

      setTimeout(function () { busy = false; }, DURATION);
    }, DURATION);
  }

  /* ── Autoavance ──────────────────────────────────────────── */
  function startTimer() {
    stopTimer();
    timer = setInterval(function () {
      goTo(current + 1);
    }, INTERVAL);
  }

  function stopTimer() {
    if (timer) { clearInterval(timer); timer = null; }
  }

  /* ── Eventos botones ─────────────────────────────────────── */
  btnPrev.addEventListener('click', function () {
    goTo(current - 1);
    startTimer(); /* resetear intervalo al navegar manualmente */
  });

  btnNext.addEventListener('click', function () {
    goTo(current + 1);
    startTimer();
  });

  /* ── Eventos dots ────────────────────────────────────────── */
  dots.forEach(function (dot, i) {
    dot.addEventListener('click', function () {
      goTo(i);
      startTimer();
    });
  });

  /* ── Pausa en hover ──────────────────────────────────────── */
  if (wrapper) {
    wrapper.addEventListener('mouseenter', stopTimer);
    wrapper.addEventListener('mouseleave', startTimer);
    wrapper.addEventListener('focusin',    stopTimer);
    wrapper.addEventListener('focusout',   startTimer);
  }

  /* ── Swipe táctil ────────────────────────────────────────── */
  var touchStartX = 0;

  track.addEventListener('touchstart', function (e) {
    touchStartX = e.changedTouches[0].clientX;
  }, { passive: true });

  track.addEventListener('touchend', function (e) {
    var diff = touchStartX - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 40) {
      goTo(diff > 0 ? current + 1 : current - 1);
      startTimer();
    }
  }, { passive: true });

  /* ── Teclado (accesibilidad) ─────────────────────────────── */
  document.addEventListener('keydown', function (e) {
    var focused = document.activeElement;
    if (focused === btnPrev || focused === btnNext ||
        focused.classList.contains('hero-slider__dot')) {
      if (e.key === 'ArrowLeft')  { goTo(current - 1); startTimer(); }
      if (e.key === 'ArrowRight') { goTo(current + 1); startTimer(); }
    }
  });

  /* ── Arrancar ────────────────────────────────────────────── */
  applySlide(0);
  startTimer();

})();