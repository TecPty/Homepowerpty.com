/* ScrollReveal — módulo ES
 * Lógica original de scroll-reveal.js sin cambios. Solo envuelto en init() + export.
 * Selectores: .featured-products-grid .product, .showcase-strips .showcase-strip
 */
const ScrollReveal = {
  init() {
    const MOBILE_BP = 768;

    function isMobile() {
      return window.innerWidth <= MOBILE_BP;
    }

    const cards  = document.querySelectorAll('.featured-products-grid .product');
    const strips = document.querySelectorAll('.showcase-strips .showcase-strip');

    function showAll() {
      cards.forEach(c => c.classList.add('product--visible'));
      strips.forEach(s => {
        s.classList.remove('strip--init');
        s.classList.add('strip--visible');
      });
    }

    if (!isMobile() || !window.IntersectionObserver) {
      showAll();
      window.addEventListener('resize', () => { if (!isMobile()) showAll(); });
      return;
    }

    strips.forEach(s => s.classList.add('strip--init'));

    const cardObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('product--visible');
        } else if (entry.boundingClientRect.top > 0) {
          entry.target.classList.remove('product--visible');
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -30px 0px' });

    cards.forEach(c => cardObserver.observe(c));

    const stripObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.remove('strip--init');
          entry.target.classList.add('strip--visible');
        } else if (entry.boundingClientRect.top > 0) {
          entry.target.classList.remove('strip--visible');
          entry.target.classList.add('strip--init');
        }
      });
    }, { threshold: 0.05 });

    strips.forEach(s => stripObserver.observe(s));

    window.addEventListener('resize', () => {
      if (!isMobile()) {
        cardObserver.disconnect();
        stripObserver.disconnect();
        showAll();
      }
    });
  },
};

export default ScrollReveal;
