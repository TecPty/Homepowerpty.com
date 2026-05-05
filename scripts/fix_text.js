document.addEventListener('DOMContentLoaded', () => {
  try {
    // Fix document title
    document.title = 'Home Power - Electrodomésticos de Calidad en Panamá';

    // Fix meta description/keywords/canonical if present
    const mDesc = document.querySelector('meta[name="description"]');
    if (mDesc) mDesc.setAttribute('content', 'Stock exclusivo para negocios que buscan lo mejor en calidad y tecnología.');
    const mKeywords = document.querySelector('meta[name="keywords"]');
    if (mKeywords) mKeywords.setAttribute('content', 'electrodomésticos, planchas, licuadoras, tostadoras, sandwicheras, teteras, estufas eléctricas, air fryer, cafetera, Home Power PTY, Panamá');
    const mOgDesc = document.querySelector('meta[property="og:description"]');
    if (mOgDesc) mOgDesc.setAttribute('content', 'Stock exclusivo para negocios que buscan lo mejor en calidad y tecnología.');
    const mTwDesc = document.querySelector('meta[name="twitter:description"]');
    if (mTwDesc) mTwDesc.setAttribute('content', 'Stock exclusivo para negocios que buscan lo mejor en calidad y tecnología.');
    const linkCanonical = document.querySelector('link[rel]');
    if (linkCanonical && linkCanonical.getAttribute('href') === 'https://www.homepowerpty.com/') {
      linkCanonical.setAttribute('rel', 'canonical');
    }

    // Banner texts
    const titleEl = document.querySelector('.section_banner .title');
    if (titleEl) titleEl.textContent = 'Potencia e Innovación para tu hogar';
    const subEl = document.querySelector('.section_banner .sub_title');
    if (subEl) subEl.textContent = 'Stock exclusivo para negocios que buscan lo mejor en calidad y tecnología.';
    const bannerImg = document.querySelector('.section_banner .banner_img');
    if (bannerImg) bannerImg.setAttribute('alt', 'Electrodomésticos');

    // Products header texts
    const prodTitle = document.querySelector('.section_products .products_title');
    if (prodTitle) prodTitle.textContent = 'Catálogo de Electrodomésticos';
    const prodSub = document.querySelector('.section_products .products_subtitle');
    if (prodSub) prodSub.textContent = 'Stock exclusivo con garantía de 1 año – Precios especiales para mayoristas';

    // Fix nav label for productos
    const productosLink = document.querySelector('.nav_bar .menu a.menu_link[href="#productos"]');
    if (productosLink) productosLink.textContent = 'Electrodomésticos';

    // Ensure burger has correct id for JS bindings
    const burger = document.querySelector('.menu-burger');
    if (burger) {
      burger.id = 'menuBurger';
      burger.setAttribute('aria-label', 'Abrir menú');
    }
  } catch (e) {
    console.error('fix_text.js error:', e);
  }
});

