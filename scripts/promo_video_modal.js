(function () {
  'use strict';

  const popup = document.getElementById('seasonalPopup');
  if (!popup) return;
  const heroSection = document.getElementById('inicio');

  const POPUP_ENABLED = true;
  const SHOW_DELAY_MS = 500;
  const HERO_THRESHOLD = 0.45;

  if (!POPUP_ENABLED) {
    popup.style.display = 'none';
    return;
  }

  const closeElements = popup.querySelectorAll('[data-close-popup]');
  const promoVideo = popup.querySelector('.promo-video');
  let lastFocused = null;
  let isInHero = false;
  let pendingOpenTimeout = null;

  const getFocusable = () =>
    popup.querySelectorAll(
      'a[href], button, textarea, input, select, [tabindex]:not([tabindex="-1"])'
    );

  function openPopup() {
    popup.classList.add('active');
    document.body.style.overflow = 'hidden';
    lastFocused = document.activeElement;
    const focusable = getFocusable();
    if (focusable.length) focusable[0].focus();
    if (promoVideo) {
      promoVideo.muted = true;
      promoVideo.currentTime = 0;
      promoVideo.play().catch(function () {});
    }
  }

  function closePopup() {
    popup.classList.remove('active');
    document.body.style.overflow = '';
    if (promoVideo) promoVideo.pause();
    if (lastFocused && typeof lastFocused.focus === 'function') {
      lastFocused.focus();
    }
  }

  function scheduleOpen() {
    if (pendingOpenTimeout) clearTimeout(pendingOpenTimeout);
    pendingOpenTimeout = setTimeout(function () {
      if (isInHero && !popup.classList.contains('active')) {
        openPopup();
      }
    }, SHOW_DELAY_MS);
  }

  function trapFocus(event) {
    if (!popup.classList.contains('active')) return;
    if (event.key !== 'Tab') return;
    const nodes = Array.from(getFocusable()).filter(
      (el) => !el.hasAttribute('disabled') && el.offsetParent !== null
    );
    if (!nodes.length) return;
    const first = nodes[0];
    const last = nodes[nodes.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  }

  closeElements.forEach((el) => el.addEventListener('click', closePopup));
  if (promoVideo) promoVideo.addEventListener('ended', closePopup);

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && popup.classList.contains('active')) {
      closePopup();
    }
    trapFocus(e);
  });

  if (heroSection && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          const currentlyInHero =
            entry.isIntersecting && entry.intersectionRatio >= HERO_THRESHOLD;
          if (currentlyInHero && !isInHero) {
            isInHero = true;
            scheduleOpen();
          }
          if (!currentlyInHero && isInHero) {
            isInHero = false;
            if (pendingOpenTimeout) {
              clearTimeout(pendingOpenTimeout);
              pendingOpenTimeout = null;
            }
          }
        });
      },
      { threshold: [0, HERO_THRESHOLD, 0.75] }
    );
    observer.observe(heroSection);
  } else {
    window.addEventListener('load', function () {
      setTimeout(openPopup, SHOW_DELAY_MS);
    });
  }

  window.PromoVideoModal = {
    show: openPopup,
    hide: closePopup,
  };
})();
