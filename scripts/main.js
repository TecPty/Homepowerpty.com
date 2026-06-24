import GoldBreeze  from './effects/gold-breeze.js';
import Header      from './modules/header.js';
import Catalog     from './modules/catalog.js';
import ContactForm from './modules/contact-form.js';
import CareersForm from './modules/careers-form.js';
import ScrollReveal from './modules/scroll-reveal.js';

// ─── Restaurar scroll al volver desde una página de producto ─────────────────
// Se ejecuta antes del DOMContentLoaded para ser lo más temprano posible.
(function maybeRestoreScroll() {
  const y = sessionStorage.getItem('hpRestoreScrollY');
  if (!y) return;
  sessionStorage.removeItem('hpRestoreScrollY');
  const target = Number(y);
  // 150ms: permite que el DOM y las imágenes above-the-fold terminen de pintar.
  setTimeout(() => window.scrollTo({ top: target, behavior: 'auto' }), 150);
})();

document.addEventListener('DOMContentLoaded', () => {
  GoldBreeze.init();
  Header.init();
  Catalog.init();
  ContactForm.init();
  CareersForm.init();
  ScrollReveal.init();

  // ─── Guardar punto de retorno antes de navegar a cualquier producto ─────
  document.addEventListener('click', (e) => {
    const link = e.target.closest('a[href]');
    if (!link) return;

    const href = link.getAttribute('href');
    if (!href || !href.includes('/productos/')) return;

    sessionStorage.setItem('hpReturnUrl',
      window.location.pathname + window.location.search + window.location.hash);
    sessionStorage.setItem('hpReturnScrollY', String(window.scrollY));
  });
});
