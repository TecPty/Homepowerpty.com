(function () {
  'use strict';

  const popup = document.getElementById('seasonalPopup');
  if (!popup) return;

  const closeElements = popup.querySelectorAll('[data-close-popup]');
  const overlay = popup.querySelector('.promo-overlay');

  const SHOW_DELAY = 1200;
  let lastFocused = null;

  const getFocusable = () =>
    popup.querySelectorAll(
      'a[href], button, textarea, input, select, [tabindex]:not([tabindex="-1"])'
    );

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

  function openPopup() {
    popup.classList.add('active');
    document.body.style.overflow = 'hidden';
    lastFocused = document.activeElement;
    const focusable = getFocusable();
    if (focusable.length) focusable[0].focus();
  }

  function closePopup() {
    popup.classList.remove('active');
    document.body.style.overflow = '';
    if (lastFocused && typeof lastFocused.focus === 'function') {
      lastFocused.focus();
    }
  }

  closeElements.forEach((el) => el.addEventListener('click', closePopup));
  if (overlay) overlay.addEventListener('click', closePopup);

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && popup.classList.contains('active')) {
      closePopup();
    }
    trapFocus(e);
  });

  window.addEventListener('load', () => {
    setTimeout(openPopup, SHOW_DELAY);
  });

  window.BlackWeekPopup = {
    show: openPopup,
    hide: closePopup,
  };
})();
