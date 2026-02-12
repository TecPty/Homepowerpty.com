(function () {
  'use strict';

  const popup = document.getElementById('seasonalPopup');
  // Popup habilitado para promoción actual - CARNAVAL
  const POPUP_ENABLED = true;
  if (!POPUP_ENABLED && popup) {
    popup.style.display = 'none';
    return;
  }
  if (!popup) return;

  const closeElements = popup.querySelectorAll('[data-close-popup]');
  const overlay = popup.querySelector('.promo-overlay');
  const promoCard = popup.querySelector('.promo-card');
  const canvas = popup.querySelector('#carnivalCanvas');
  const ctx = canvas ? canvas.getContext('2d') : null;

  const SHOW_DELAY = 1200;
  const WHATSAPP_NUMBER = '50766133830';
  const WHATSAPP_MESSAGE = 'Me interesa obtener información de sus productos';
  let lastFocused = null;

  // Configuración de carnaval
  const PRODUCT_IMAGES = [
    'media/images/products/AIR_FRYER.webp',
    'media/images/products/CAFETERA_12_TAZAS.webp',
    'media/images/products/ESTUFA_ELECTRICA_DOBLE_NEGRA.webp',
    'media/images/products/FRIEDORA_DE_AIRE_BLANCA_1.webp',
    'media/images/products/LICUADORA_ROJA.webp',
    'media/images/products/OLLA_PRESION.webp',
    'media/images/products/PANINI_1.webp',
    'media/images/products/PLANCHA_VAPOR.webp',
    'media/images/products/SANDWCHERA_METAL.webp',
    'media/images/products/TETERA_ELECTRICA.webp'
  ];

  let products = [];
  let animationId = null;

  // Clase para productos rebotantes
  class BouncingProduct {
    constructor(x, y, imagePath) {
      this.x = x;
      this.y = y;
      this.vx = (Math.random() - 0.5) * 4;
      this.vy = Math.random() * -2 - 1;
      this.radius = 70; // Duplicado de 35 a 70
      this.gravity = 0.15;
      this.restitution = 0.88;
      this.imagePath = imagePath;
      this.image = null;
      this.loadImage();
    }

    loadImage() {
      const img = new Image();
      img.src = this.imagePath;
      img.onload = () => {
        this.image = img;
      };
    }

    update(width, height) {
      this.vy += this.gravity;
      this.x += this.vx;
      this.y += this.vy;

      // Colisión con paredes
      if (this.x - this.radius < 0) {
        this.x = this.radius;
        this.vx *= -this.restitution;
      }
      if (this.x + this.radius > width) {
        this.x = width - this.radius;
        this.vx *= -this.restitution;
      }

      // Colisión con piso - ajustado para evitar que desaparezcan
      const floorLimit = height - 20; // Margen de 20px desde el borde inferior
      if (this.y + this.radius > floorLimit) {
        this.y = floorLimit - this.radius;
        this.vy *= -this.restitution;
      }

      // Colisión con techo
      if (this.y - this.radius < 0) {
        this.y = this.radius;
        this.vy *= -this.restitution;
      }
    }

    draw(ctx) {
      if (!this.image || !this.image.complete) return;

      ctx.save();
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.clip();

      ctx.drawImage(
        this.image,
        this.x - this.radius,
        this.y - this.radius,
        this.radius * 2,
        this.radius * 2
      );

      ctx.restore();
    }
  }

  function initCarnival() {
    if (!canvas || !ctx) return;

    // Configurar canvas
    const container = popup.querySelector('.carnival-container') || promoCard;
    canvas.width = container.offsetWidth;
    canvas.height = container.offsetHeight;

    // Crear productos
    products = [];
    for (let i = 0; i < PRODUCT_IMAGES.length; i++) {
      const x = Math.random() * (canvas.width - 80) + 40;
      const y = Math.random() * (canvas.height - 80) + 40;
      products.push(new BouncingProduct(x, y, PRODUCT_IMAGES[i]));
    }

    // Hacer fondo transparente
    canvas.style.position = 'absolute';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.pointerEvents = 'none';

    animate();
  }

  function animate() {
    if (!ctx || !canvas) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    products.forEach((product) => {
      product.update(canvas.width, canvas.height);
      product.draw(ctx);
    });

    animationId = requestAnimationFrame(animate);
  }

  function stopCarnival() {
    if (animationId) {
      cancelAnimationFrame(animationId);
      animationId = null;
    }
    if (ctx && canvas) {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
  }

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
    initCarnival();
    const focusable = getFocusable();
    if (focusable.length) focusable[0].focus();
  }

  function closePopup() {
    popup.classList.remove('active');
    document.body.style.overflow = '';
    stopCarnival();
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

  // Click en la card redirige a WhatsApp
  if (promoCard) {
    promoCard.style.cursor = 'pointer';
    promoCard.addEventListener('click', function (e) {
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
