class ClientsSlider {
    constructor(options = {}) {
        // Configuración por defecto
        this.config = {
            sliderId: 'clients_slider',
            leftArrowId: 'slider_clients_arrow_left',
            rightArrowId: 'slider_clients_arrow_right',
            transitionDuration: 300,
            breakpoint: 864,
            virtualItems: 5,
            ...options
        };

        // Referencias DOM
        this.slider = document.getElementById(this.config.sliderId);
        this.leftArrow = document.getElementById(this.config.leftArrowId);
        this.rightArrow = document.getElementById(this.config.rightArrowId);

        // Estado
        this.isAnimating = false;
        this.isPaused = false;

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
        this.setupIntersectionObserver(); // NUEVO: Pausa cuando no está visible
    }

    validateElements() {
        return this.slider && this.leftArrow && this.rightArrow;
    }

    setupAccessibility() {
        this.slider.setAttribute('role', 'region');
        this.slider.setAttribute('aria-label', 'Carrusel de clientes');
        
        this.leftArrow.setAttribute('aria-label', 'Anterior slide');
        this.rightArrow.setAttribute('aria-label', 'Siguiente slide');
        
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

    // NUEVO: Pausa la animación CSS cuando no está visible
    setupIntersectionObserver() {
        const options = {
            root: null,
            rootMargin: '0px',
            threshold: 0.1
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    // Slider visible - reanudar animación
                    this.slider.style.animationPlayState = 'running';
                    this.isPaused = false;
                } else {
                    // Slider fuera de vista - pausar animación
                    this.slider.style.animationPlayState = 'paused';
                    this.isPaused = true;
                }
            });
        }, options);

        observer.observe(this.slider);
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

        // Pause on hover
        this.slider.addEventListener('mouseenter', () => {
            this.slider.style.animationPlayState = 'paused';
        });

        this.slider.addEventListener('mouseleave', () => {
            if (!this.isPaused) {
                this.slider.style.animationPlayState = 'running';
            }
        });

        // Resize observer
        const resizeObserver = new ResizeObserver(() => {
            const { resetMargin } = this.getSliderValues();
            this.resetSlidePosition(resetMargin);
        });

        resizeObserver.observe(this.slider);
    }
}

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    const slider = new ClientsSlider();
});