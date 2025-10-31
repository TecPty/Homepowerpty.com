document.addEventListener('DOMContentLoaded', () => {
    const menuBurger = document.getElementById('menuBurger');
    const fullscreenMenu = document.getElementById('fullscreenMenu');
    const menuClose = document.getElementById('menuClose');
    const menuLinks = document.querySelectorAll('.fullscreen-menu-link');

    // Usa el menú fullscreen si existe; si no, abre el menú lateral existente
    if (menuBurger && fullscreenMenu && menuClose) {
        const closeMenu = () => {
            fullscreenMenu.classList.remove('active');
            document.body.classList.remove('menu-open');
        };

        menuBurger.addEventListener('click', () => {
            fullscreenMenu.classList.add('active');
            document.body.classList.add('menu-open');
        });

        menuClose.addEventListener('click', closeMenu);
        menuLinks.forEach(link => link.addEventListener('click', closeMenu));
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && fullscreenMenu.classList.contains('active')) {
                closeMenu();
            }
        });
    } else if (menuBurger) {
        const headerEl = document.getElementById('header');
        const overlayEl = document.getElementById('overlay');
        const open = () => {
            if (!headerEl || !overlayEl) return;
            headerEl.classList.add('translate');
            overlayEl.classList.add('active');
            document.body.classList.add('menu-open');
            document.body.style.overflow = 'hidden';
        };
        const close = () => {
            if (!headerEl || !overlayEl) return;
            headerEl.classList.remove('translate');
            overlayEl.classList.remove('active');
            document.body.classList.remove('menu-open');
            document.body.style.overflow = '';
        };
        menuBurger.addEventListener('click', open);
        if (overlayEl) overlayEl.addEventListener('click', close);
        document.addEventListener('keydown', (e) => { if (e.key === 'Escape') close(); });
    }
});

(function(){
    const header = document.getElementById('header');
    const socialHeader = document.querySelector('.social_header_bar');
    const banner = document.querySelector('.section_banner');
    const btnMenu = document.getElementById('btn_menu');
    const btnMenuClose = document.getElementById('btn_menu_close');
    const menuItems = document.querySelectorAll('.menu_item');
    const overlay = document.getElementById('overlay');
    
    if (btnMenu) {
        btnMenu.addEventListener('click', () => {
            header.classList.add('translate');
            overlay.classList.add('active');
            document.body.classList.add('menu-open');
            document.body.style.overflow = 'hidden';
        });
    }
    
    if (btnMenuClose) btnMenuClose.addEventListener('click', closeMenu);
    if (overlay) overlay.addEventListener('click', closeMenu);
    
    function closeMenu() {
        header.classList.remove('translate');
        overlay.classList.remove('active');
        document.body.classList.remove('menu-open');
        document.body.style.overflow = '';
    }
    
    menuItems.forEach(item => {
        item.addEventListener('click', closeMenu);
    });

    const getHeadersHeight = () => {
        const socialHeight = socialHeader ? socialHeader.offsetHeight : 0;
        const headerHeight = header.offsetHeight;
        return socialHeight + headerHeight;
    };
    
    if (banner) {
        banner.style.paddingTop = `${getHeadersHeight() + 30}px`;
    }
    
    if (btnMenu) {
        btnMenu.addEventListener('click', () => {
            header.classList.add('translate');
            overlay.classList.add('active');
            document.body.classList.add('menu-open');
            document.body.style.overflow = 'hidden';
        });
    }
    
    function closeMenu() {
        header.classList.remove('translate');
        overlay.classList.remove('active');
        document.body.classList.remove('menu-open');
        document.body.style.overflow = '';
    }
    
    if (btnMenuClose) btnMenuClose.addEventListener('click', closeMenu);
    if (overlay) overlay.addEventListener('click', closeMenu);
    
    menuItems.forEach(item => {
        item.addEventListener('click', closeMenu);
    });
    
    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > 100) {
            header.classList.add('active');
            if (socialHeader) {
                socialHeader.style.transform = 'translateY(-100%)';
                socialHeader.style.transition = 'transform 0.3s ease';
            }
            header.style.background = 'rgba(255, 255, 255, 0.92)';
            header.style.backdropFilter = 'blur(20px)';
            if (banner) {
                banner.style.paddingTop = '90px';
                banner.style.transition = 'padding-top 0.3s ease';
            }
        } else {
            header.classList.remove('active');
            if (socialHeader) socialHeader.style.transform = 'translateY(0)';
            header.style.background = 'rgba(255, 255, 255, 0.98)';
            header.style.backdropFilter = 'blur(10px)';
            if (banner) banner.style.paddingTop = `${getHeadersHeight() + 30}px`;
        }
    });
    
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const target = document.getElementById(targetId);
            if (target) {
                const headerHeight = getHeadersHeight();
                const targetPosition = target.offsetTop - headerHeight + 20;
                window.scrollTo({ top: targetPosition, behavior: 'smooth' });
            }
        });
    });
    
    window.addEventListener('resize', () => {
        if (banner && window.scrollY < 100) {
            banner.style.paddingTop = `${getHeadersHeight() + 30}px`;
        }
    });
})();

