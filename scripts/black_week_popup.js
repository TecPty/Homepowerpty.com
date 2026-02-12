(function () {
  'use strict';

  const popup = document.getElementById('seasonalPopup');
  // Popup habilitado para promoción actual
  const POPUP_ENABLED = false;
  if (!POPUP_ENABLED && popup) {
    popup.style.display = 'none';
    return;
  }
  if (!popup) return;

  const closeElements = popup.querySelectorAll('[data-close-popup]');
  const overlay = popup.querySelector('.promo-overlay');
  const promoCard = popup.querySelector('.promo-card');
  const promoImage = popup.querySelector('.promo-image');

  const SHOW_DELAY = 1200;
  const WHATSAPP_NUMBER = '50766133830';
  const WHATSAPP_MESSAGE = 'Me interesa obtener información de sus productos';
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

  function redirectToWhatsApp() {
    const encodedMessage = encodeURIComponent(WHATSAPP_MESSAGE);
    const whatsappURL = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodedMessage}`;
    window.open(whatsappURL, '_blank');
    closePopup();
  }

  closeElements.forEach((el) => el.addEventListener('click', closePopup));
  if (overlay) overlay.addEventListener('click', closePopup);
  
  // Click en la imagen del banner redirige a WhatsApp
  if (promoImage) {
    promoImage.style.cursor = 'pointer';
    promoImage.addEventListener('click', redirectToWhatsApp);
  }
  
  // Click en la card (excepto botón cerrar) también redirige
  if (promoCard) {
    promoCard.style.cursor = 'pointer';
    promoCard.addEventListener('click', function(e) {
      // No redirigir si se hace clic en el botón de cerrar
      if (!e.target.closest('[data-close-popup]')) {
        redirectToWhatsApp();
      }
    });
  }

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
