document.addEventListener('DOMContentLoaded', function() {
    const menuBurger = document.getElementById('menuBurger');
    const menuClose = document.getElementById('menuClose');
    const fullscreenMenu = document.getElementById('fullscreenMenu');
    const menuLinks = document.querySelectorAll('.fullscreen-menu-link');
    const body = document.body;
    
    // Abrir menú
    if (menuBurger) {
        menuBurger.addEventListener('click', function(e) {
            e.preventDefault();
            fullscreenMenu.classList.add('active');
            body.classList.add('menu-open');
        });
    }
    
    // Cerrar menú con botón X
    if (menuClose) {
        menuClose.addEventListener('click', function(e) {
            e.preventDefault();
            closeMenu();
        });
    }
    
    // Cerrar menú al hacer click en un enlace
    menuLinks.forEach(link => {
        link.addEventListener('click', function() {
            closeMenu();
        });
    });
    
    // Cerrar menú con ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && fullscreenMenu.classList.contains('active')) {
            closeMenu();
        }
    });
    
    // Función para cerrar el menú
    function closeMenu() {
        fullscreenMenu.classList.remove('active');
        body.classList.remove('menu-open');
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
    
    btnMenu.addEventListener('click', () => {
        header.classList.add('translate');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    });
    
    btnMenuClose.addEventListener('click', closeMenu);
    overlay.addEventListener('click', closeMenu);
    
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
        return socialHeight + headerHeight;
    };
    
    if (banner) {
        banner.style.paddingTop = `${getHeadersHeight() + 30}px`;
    }
    
    btnMenu.addEventListener('click', () => {
        header.classList.add('translate');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    });
    
    function closeMenu() {
        header.classList.remove('translate');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    }
    
    btnMenuClose.addEventListener('click', closeMenu);
    overlay.addEventListener('click', closeMenu);
    
    menuItems.forEach(item => {
        item.addEventListener('click', closeMenu);
    });
    let lastScrollTop = 0;
    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > 100) {
            header.classList.add('active');
            socialHeader.style.transform = 'translateY(-100%)';
            socialHeader.style.transition = 'transform 0.3s ease';
            
            // Efecto adicional: hacer el header más transparente y elegante
            header.style.background = 'rgba(255, 255, 255, 0.92)';
            header.style.backdropFilter = 'blur(20px)';
            
            if (banner) {
                banner.style.paddingTop = '90px';
                banner.style.transition = 'padding-top 0.3s ease';
            }
        } else {
            header.classList.remove('active');
            socialHeader.style.transform = 'translateY(0)';
            
            // Restaurar apariencia original
            header.style.background = 'rgba(255, 255, 255, 0.98)';
            header.style.backdropFilter = 'blur(10px)';
            
            if (banner) {
                banner.style.paddingTop = `${getHeadersHeight() + 30}px`;
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
            banner.style.paddingTop = `${getHeadersHeight() + 30}px`;
        }
    });
    
    // Logo clickeable para ir al inicio
    const logoContainer = document.querySelector('.logo_container');
    if (logoContainer) {
        logoContainer.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
        
        // Efecto visual en hover
        logoContainer.addEventListener('mouseenter', () => {
            if (header.classList.contains('active')) {
                logoContainer.style.transform = 'scale(1.05)';
            }
        });
        
        logoContainer.addEventListener('mouseleave', () => {
            logoContainer.style.transform = 'scale(1)';
        });
    }
})();