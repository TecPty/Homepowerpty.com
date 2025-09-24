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
            
            if (banner) {
                banner.style.paddingTop = '100px';
                banner.style.transition = 'padding-top 0.3s ease';
            }
        } else {
            header.classList.remove('active');
            socialHeader.style.transform = 'translateY(0)';
            
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
})();