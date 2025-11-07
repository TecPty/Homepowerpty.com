document.addEventListener('DOMContentLoaded', () => {
  const menuBurger = document.getElementById('menuBurger');
  const fullscreenMenu = document.getElementById('fullscreenMenu');
  const menuClose = document.getElementById('menuClose');
  const menuLinks = document.querySelectorAll('.fullscreen-menu-link');

  if (menuBurger && fullscreenMenu) {
    const openMenu = () => {
      fullscreenMenu.classList.add('active');
      document.body.classList.add('menu-open');
    };
    const closeMenu = () => {
      fullscreenMenu.classList.remove('active');
      document.body.classList.remove('menu-open');
    };
    menuBurger.addEventListener('click', openMenu);
    if (menuClose) menuClose.addEventListener('click', closeMenu);
    if (menuLinks && menuLinks.length) menuLinks.forEach(link => link.addEventListener('click', closeMenu));
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && fullscreenMenu.classList.contains('active')) closeMenu();
    });
  }
});

(function(){
    const header = document.getElementById('header');
    const socialHeader = document.querySelector('.social_header_bar');
    const banner = document.querySelector('.section_banner');
    const bannerLogo = document.querySelector('.banner_logo');
    const btnMenu = document.getElementById('btn_menu');
    const btnMenuClose = document.getElementById('btn_menu_close');
    const menuItems = document.querySelectorAll('.menu_item');
    const overlay = document.getElementById('overlay');
    
    if (btnMenu && overlay) { btnMenu.addEventListener('click', () => { header.classList.add('translate'); overlay.classList.add('active'); document.body.style.overflow = 'hidden'; }); }
    
    if (btnMenuClose) btnMenuClose.addEventListener('click', closeMenu);
    if (overlay) overlay.addEventListener('click', closeMenu);
    
    function closeMenu() {
        header.classList.remove('translate');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    }
    
    menuItems.forEach(item => {
        item.addEventListener('click', closeMenu);
    });

    const getHeadersHeight = () => {
        const socialHeight = socialHeader ? socialHeader.offsetHeight : 0;
        const headerHeight = header.offsetHeight;
        // En mÃ³vil no empujamos el banner por la altura del header para evitar franja blanca
        return (window.innerWidth <= 768) ? socialHeight : (socialHeight + headerHeight);
    };
    
    if (banner) {
        banner.style.paddingTop = `${getHeadersHeight()}px`;
    }
    // Ensure header sits below social bar height on load
    header.style.top = `${socialHeader ? socialHeader.offsetHeight : 0}px`; if (bannerLogo) { const offset = (socialHeader ? socialHeader.offsetHeight : 0) + 80; bannerLogo.style.top = `${offset}px`; }
    
    if (btnMenu && overlay) { btnMenu.addEventListener('click', () => { header.classList.add('translate'); overlay.classList.add('active'); document.body.style.overflow = 'hidden'; }); }
    
    function closeMenu() {
        header.classList.remove('translate');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    }
    
    if (btnMenuClose) btnMenuClose.addEventListener('click', closeMenu);
    if (overlay) overlay.addEventListener('click', closeMenu);
    
    menuItems.forEach(item => {
        item.addEventListener('click', closeMenu);
    });
    let lastScrollTop = 0;
    window.addEventListener('scroll', () => {    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const scrollingDown = scrollTop > lastScrollTop;
if (scrollTop > 100) {
            header.classList.add('active');
            socialHeader.style.transform = 'translateY(-100%)';
            socialHeader.style.transition = 'transform 0.3s ease';
            
            // Efecto adicional: hacer el header mÃ¡s transparente y elegante
            header.style.background = 'rgba(255, 255, 255, 0.92)';
            header.style.backdropFilter = 'blur(20px)';
            
            if (banner) {
                // con barra social oculta, solo compensamos el header
                const h = (window.innerWidth <= 768) ? header.offsetHeight : 90;
                banner.style.paddingTop = `${h}px`;
                banner.style.transition = 'padding-top 0.3s ease';
            // Ocultar header al desplazarse hacia abajo; mostrar al subir
            if (scrollingDown) {
                header.classList.add('hide');
            } else {
                header.classList.remove('hide');
            }
            }
        } else {
            header.classList.remove('active');
            socialHeader.style.transform = 'translateY(0)';
            
            // Restaurar apariencia original
            header.style.background = 'rgba(255, 255, 255, 0.98)';
            header.style.backdropFilter = 'blur(10px)';
            // Reposition header right under social bar when visible
            header.style.top = `${socialHeader ? socialHeader.offsetHeight : 0}px`; if (bannerLogo) { const offset = (socialHeader ? socialHeader.offsetHeight : 0) + 80; bannerLogo.style.top = `${offset}px`; }
            
            if (banner) {
                banner.style.paddingTop = `${getHeadersHeight()}px`;
            }
        }
        
        lastScrollTop = scrollTop;
    });
    
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const target = document.getElementById(targetId);
            
            if (target) {
                const headerHeight = getHeadersHeight();
                const targetPosition = target.offsetTop - headerHeight + 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    window.addEventListener('resize', () => {
        if (banner && window.scrollY < 100) {
            banner.style.paddingTop = `${getHeadersHeight()}px`;
        }
        if (window.scrollY < 100) {
            header.style.top = `${socialHeader ? socialHeader.offsetHeight : 0}px`; if (bannerLogo) { const offset = (socialHeader ? socialHeader.offsetHeight : 0) + 80; bannerLogo.style.top = `${offset}px`; }
        }
    });
})();














