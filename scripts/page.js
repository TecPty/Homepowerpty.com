import Header     from './modules/header.js';
import GoldBreeze from './effects/gold-breeze.js';

// ─── Menú compacto: reemplaza el fullscreen-menu en páginas de producto ──────
// header.js busca getElementById('mobileMenu') || getElementById('fullscreenMenu').
// Inyectando #mobileMenu primero, el compact-menu del home queda activo.
// El fullscreenMenu del HTML queda en el DOM pero nunca se activa.
function injectMobileMenu() {
  if (document.getElementById('mobileMenu')) return;
  const header = document.querySelector('.luxury-header');
  if (!header) return;

  const el = document.createElement('div');
  el.className = 'mobile-menu';
  el.id        = 'mobileMenu';
  el.setAttribute('aria-label', 'Menú de navegación');
  el.setAttribute('aria-hidden', 'true');
  el.innerHTML = `
    <nav>
      <ul class="mobile-menu__links">
        <li><a href="/index.html"                  class="mobile-menu-link">Inicio</a></li>
        <li><a href="/index.html#catalogo"          class="mobile-menu-link">Catálogo</a></li>
        <li><a href="/index.html#nosotros"          class="mobile-menu-link">Nosotros</a></li>
        <li><a href="/index.html#clientes"          class="mobile-menu-link">Clientes</a></li>
        <li><a href="/index.html#contacto"          class="mobile-menu-link">Consulta</a></li>
        <li><a href="/index.html#oportunidades"     class="mobile-menu-link">Oportunidades</a></li>
      </ul>
    </nav>
    <a href="https://wa.me/50769838322" class="mobile-menu__cta" target="_blank" rel="noopener">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor"
           stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07
                 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11
                 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45
                 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45
                 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
      </svg>
      Contactar
    </a>`;

  header.insertAdjacentElement('afterend', el);
}

// ─── Flecha de regreso ────────────────────────────────────────────────────────
function isSafeInternalUrl(url) {
  return typeof url === 'string' && url.startsWith('/') && !url.startsWith('//');
}

function goBack() {
  const returnUrl = sessionStorage.getItem('hpReturnUrl');
  const scrollY   = sessionStorage.getItem('hpReturnScrollY');

  sessionStorage.removeItem('hpReturnUrl');
  sessionStorage.removeItem('hpReturnScrollY');

  if (isSafeInternalUrl(returnUrl)) {
    if (scrollY !== null) sessionStorage.setItem('hpRestoreScrollY', scrollY);
    window.location.href = returnUrl;
  } else {
    window.location.href = '/index.html#catalogo';
  }
}

function injectBackButton() {
  if (document.getElementById('pdpBackBtn')) return;
  const header = document.querySelector('.luxury-header');
  if (!header) return;

  const btn = document.createElement('button');
  btn.className = 'pdp-back-btn';
  btn.id        = 'pdpBackBtn';
  btn.type      = 'button';
  btn.setAttribute('aria-label', 'Volver al catálogo');
  btn.innerHTML = `
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"
         stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <line x1="19" y1="12" x2="5" y2="12"/>
      <polyline points="12 19 5 12 12 5"/>
    </svg>`;
  btn.addEventListener('click', goBack);

  // prepend (no append): mantiene el tab order alineado con el orden visual
  // (la flecha se ve a la izquierda del logo en mobile y desktop).
  header.prepend(btn);
}

// ─── Init ─────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  injectMobileMenu();
  injectBackButton();
  Header.init();
  GoldBreeze.init();
});
