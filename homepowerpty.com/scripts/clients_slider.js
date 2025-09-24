class ClientsSlider {
    constructor(options = {}) {
        // Configuración por defecto
        this.config = {
            sliderId: 'clients_slider',
            leftArrowId: 'slider_clients_arrow_left',
            rightArrowId: 'slider_clients_arrow_right',
            transitionDuration: 300,
            breakpoint: 864,
            virtualItems: 5, // Número de items a renderizar
            ...options
        };

        // Referencias DOM
        this.slider = document.getElementById(this.config.sliderId);
        this.leftArrow = document.getElementById(this.config.leftArrowId);
        this.rightArrow = document.getElementById(this.config.rightArrowId);

        // Estado
        this.isAnimating = false;

        this.init();
    }

    init() {
        if (!this.validateElements()) {
            console.error('No se pudieron encontrar los elementos necesarios del slider');
            return;
        }

        this.setupAccessibility();
        this.bindEvents();
        this.setupTouchSupport();
    }

    validateElements() {
        return this.slider && this.leftArrow && this.rightArrow;
    }

    setupAccessibility() {
        // Mejoras de accesibilidad
        this.slider.setAttribute('role', 'region');
        this.slider.setAttribute('aria-label', 'Carrusel de clientes');
        
        this.leftArrow.setAttribute('aria-label', 'Anterior slide');
        this.rightArrow.setAttribute('aria-label', 'Siguiente slide');
        
        // Añadir soporte para teclado
        this.slider.setAttribute('tabindex', '0');
    }

    getSliderValues() {
        const window_width = window.innerWidth;
        return window_width > this.config.breakpoint 
            ? { moveDistance: 50, resetMargin: -25 }
            : { moveDistance: 100, resetMargin: -50 };
    }

    async moveSlide(direction) {
        if (this.isAnimating) return;
        this.isAnimating = true;

        const { moveDistance, resetMargin } = this.getSliderValues();
        const margin = direction === 'right' ? `-${moveDistance}` : '0';

        try {
            await this.animateSlide(margin);
            this.updateSlideOrder(direction);
            this.resetSlidePosition(resetMargin);
        } catch (error) {
            console.error('Error en la animación:', error);
        } finally {
            this.isAnimating = false;
        }
    }

    animateSlide(margin) {
        return new Promise(resolve => {
            this.slider.style.transition = `transform ${this.config.transitionDuration}ms ease`;
            this.slider.style.transform = `translateX(${margin}%)`;
            setTimeout(resolve, this.config.transitionDuration);
        });
    }

    updateSlideOrder(direction) {
        if (direction === 'right') {
            const first = this.slider.firstElementChild;
            this.slider.appendChild(first);
        } else {
            const last = this.slider.lastElementChild;
            this.slider.prepend(last);
        }
    }

    resetSlidePosition(resetMargin) {
        this.slider.style.transition = 'none';
        this.slider.style.transform = `translateX(${resetMargin}%)`;
    }

    setupTouchSupport() {
        let touchStartX = 0;
        let touchEndX = 0;

        this.slider.addEventListener('touchstart', e => {
            touchStartX = e.touches[0].clientX;
        }, { passive: true });

        this.slider.addEventListener('touchend', e => {
            touchEndX = e.changedTouches[0].clientX;
            this.handleSwipe(touchStartX, touchEndX);
        }, { passive: true });
    }

    handleSwipe(startX, endX) {
        const swipeThreshold = 50;
        const diff = startX - endX;

        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                this.moveSlide('right');
            } else {
                this.moveSlide('left');
            }
        }
    }

    bindEvents() {
        // Click events
        this.rightArrow.addEventListener('click', () => this.moveSlide('right'));
        this.leftArrow.addEventListener('click', () => this.moveSlide('left'));

        // Keyboard support
        this.slider.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') this.moveSlide('left');
            if (e.key === 'ArrowRight') this.moveSlide('right');
        });

        // Resize observer para actualizar valores
        const resizeObserver = new ResizeObserver(() => {
            const { resetMargin } = this.getSliderValues();
            this.resetSlidePosition(resetMargin);
        });

        resizeObserver.observe(this.slider);
    }

    virtualizeItems() {
        const items = Array.from(this.slider.children);
        this.totalItems = items.length;
        
        // Mantener solo los items visibles
        this.slider.innerHTML = '';
        items.slice(0, this.config.virtualItems).forEach(item => {
            this.slider.appendChild(item);
        });
    }
}

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    const slider = new ClientsSlider();
});
