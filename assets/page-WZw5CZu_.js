import{n as e,t}from"./header-CV_-Pxcz.js";function n(){if(document.getElementById(`mobileMenu`))return;let e=document.querySelector(`.luxury-header`);if(!e)return;let t=document.createElement(`div`);t.className=`mobile-menu`,t.id=`mobileMenu`,t.setAttribute(`aria-label`,`Menú de navegación`),t.setAttribute(`aria-hidden`,`true`),t.innerHTML=`
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
    </a>`,e.insertAdjacentElement(`afterend`,t)}function r(e){return typeof e==`string`&&e.startsWith(`/`)&&!e.startsWith(`//`)}function i(){let e=sessionStorage.getItem(`hpReturnUrl`),t=sessionStorage.getItem(`hpReturnScrollY`);sessionStorage.removeItem(`hpReturnUrl`),sessionStorage.removeItem(`hpReturnScrollY`),r(e)?(t!==null&&sessionStorage.setItem(`hpRestoreScrollY`,t),window.location.href=e):window.location.href=`/index.html#catalogo`}function a(){if(document.getElementById(`pdpBackBtn`))return;let e=document.querySelector(`.luxury-header`);if(!e)return;let t=document.createElement(`button`);t.className=`pdp-back-btn`,t.id=`pdpBackBtn`,t.type=`button`,t.setAttribute(`aria-label`,`Volver al catálogo`),t.innerHTML=`
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"
         stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <line x1="19" y1="12" x2="5" y2="12"/>
      <polyline points="12 19 5 12 12 5"/>
    </svg>`,t.addEventListener(`click`,i),e.prepend(t)}document.addEventListener(`DOMContentLoaded`,()=>{n(),a(),t.init(),e.init()});