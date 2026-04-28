/* Header — módulo ES
 * Lógica original sin cambios. Solo envuelto en init() + export.
 * Incluye: menú fullscreen, scroll behavior, smooth anchors, resize.
 */
const Header = {
  init() {
    // ── Menú fullscreen (implementación activa) ─────────────────
    const menuBurger = document.getElementById('menuBurger');
    const fullscreenMenu = document.getElementById('fullscreenMenu');
    const menuClose = document.getElementById('menuClose');
    const menuLinks = document.querySelectorAll('.fullscreen-menu-link');

    if (menuBurger && fullscreenMenu) {
      const openMenu = () => {
        fullscreenMenu.classList.add('active');
        menuBurger.classList.add('active');
        menuBurger.setAttribute('aria-expanded', 'true');
        document.body.classList.add('menu-open');
      };
      const closeMenu = () => {
        fullscreenMenu.classList.remove('active');
        menuBurger.classList.remove('active');
        menuBurger.setAttribute('aria-expanded', 'false');
        document.body.classList.remove('menu-open');
      };
      menuBurger.addEventListener('click', openMenu);
      if (menuClose) menuClose.addEventListener('click', closeMenu);
      if (menuLinks && menuLinks.length) {
        menuLinks.forEach(link => link.addEventListener('click', closeMenu));
      }
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && fullscreenMenu.classList.contains('active')) closeMenu();
      });
    }

    // ── Menú legacy + scroll behavior + anchors ─────────────────
    const header = document.getElementById('header');
    const socialHeader = document.querySelector('.social_header_bar');
    const banner = document.querySelector('.section_banner');
    const bannerLogo = document.querySelector('.banner_logo');
    const btnMenu = document.getElementById('btn_menu');
    const btnMenuClose = document.getElementById('btn_menu_close');
    const menuItems = document.querySelectorAll('.menu_item');
    const overlay = document.getElementById('overlay');

    function closeLegacyMenu() {
      if (header) header.classList.remove('translate');
      if (overlay) overlay.classList.remove('active');
      document.body.style.overflow = '';
    }

    if (btnMenu && overlay) {
      btnMenu.addEventListener('click', () => {
        header.classList.add('translate');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
      });
    }
    if (btnMenuClose) btnMenuClose.addEventListener('click', closeLegacyMenu);
    if (overlay) overlay.addEventListener('click', closeLegacyMenu);
    menuItems.forEach(item => item.addEventListener('click', closeLegacyMenu));

    const getHeadersHeight = () => {
      const socialHeight = socialHeader ? socialHeader.offsetHeight : 0;
      const headerHeight = header ? header.offsetHeight : 0;
      return (window.innerWidth <= 768) ? socialHeight : (socialHeight + headerHeight);
    };

    if (banner) banner.style.paddingTop = `${getHeadersHeight()}px`;
    if (header) {
      header.style.top = `${socialHeader ? socialHeader.offsetHeight : 0}px`;
    }
    if (bannerLogo) {
      bannerLogo.style.top = `${(socialHeader ? socialHeader.offsetHeight : 0) + 80}px`;
    }

    // ── Scroll behavior ──────────────────────────────────────────
    let lastScrollTop = 0;
    window.addEventListener('scroll', () => {
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      const scrollingDown = scrollTop > lastScrollTop;

      if (scrollTop > 100) {
        if (header) {
          header.classList.add('active');
          header.style.background = 'rgba(255, 255, 255, 0.92)';
          header.style.backdropFilter = 'blur(20px)';
          scrollingDown ? header.classList.add('hide') : header.classList.remove('hide');
        }
        if (socialHeader) {
          socialHeader.style.transform = 'translateY(-100%)';
          socialHeader.style.transition = 'transform 0.3s ease';
        }
        if (banner) {
          const h = (window.innerWidth <= 768) ? (header ? header.offsetHeight : 0) : 90;
          banner.style.paddingTop = `${h}px`;
          banner.style.transition = 'padding-top 0.3s ease';
        }
      } else {
        if (header) {
          header.classList.remove('active');
          header.style.background = 'rgba(255, 255, 255, 0.98)';
          header.style.backdropFilter = 'blur(10px)';
          header.style.top = `${socialHeader ? socialHeader.offsetHeight : 0}px`;
        }
        if (socialHeader) socialHeader.style.transform = 'translateY(0)';
        if (bannerLogo) {
          bannerLogo.style.top = `${(socialHeader ? socialHeader.offsetHeight : 0) + 80}px`;
        }
        if (banner) banner.style.paddingTop = `${getHeadersHeight()}px`;
      }

      lastScrollTop = scrollTop;
    });

    // ── Smooth scroll anchors ────────────────────────────────────
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href').substring(1);
        const target = document.getElementById(targetId);
        if (target) {
          const targetPosition = target.offsetTop - getHeadersHeight() + 20;
          window.scrollTo({ top: targetPosition, behavior: 'smooth' });
        }
      });
    });

    // ── Resize ───────────────────────────────────────────────────
    window.addEventListener('resize', () => {
      if (banner && window.scrollY < 100) {
        banner.style.paddingTop = `${getHeadersHeight()}px`;
      }
      if (window.scrollY < 100 && header) {
        header.style.top = `${socialHeader ? socialHeader.offsetHeight : 0}px`;
      }
      if (bannerLogo && window.scrollY < 100) {
        bannerLogo.style.top = `${(socialHeader ? socialHeader.offsetHeight : 0) + 80}px`;
      }
    });
  },
};

export default Header;
