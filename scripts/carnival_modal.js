/**
 * CARNIVAL MODAL - Animación de Rebote de Productos
 * Muestra 10 productos rebotando dentro del modal carnavales
 */

(function () {
    'use strict';

    // Configuración
    const MODAL_ENABLED = true;
    const SESSION_KEY = 'carnivalModalShown';
    const SHOW_DELAY = 1500;
    
    // Debug logging
    console.log('[CARNIVAL] Modal initializing...', { MODAL_ENABLED, SESSION_KEY });
    
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

    const modal = document.getElementById('carnivalModal');
    if (!MODAL_ENABLED || !modal) {
        console.log('[CARNIVAL] Modal disabled or not found', { MODAL_ENABLED, modalFound: !!modal });
        return;
    }

    console.log('[CARNIVAL] Modal element found ✅');

    // Elementos DOM
    const overlay = modal.querySelector('.carnival-overlay');
    const closeBtn = modal.querySelector('.carnival-close');
    const canvas = document.getElementById('carnivalCanvas');
    const container = modal.querySelector('.carnival-container');
    const ctx = canvas?.getContext('2d');

    if (!canvas || !ctx) {
        console.error('Canvas no disponible para carnival modal');
        return;
    }

    // Variables de animación
    let products = [];
    let animationId = null;
    let isAnimating = false;

    /**
     * Clase para cada producto rebotante
     */
    class BouncingProduct {
        constructor(x, y, size, imageUrl) {
            this.x = x;
            this.y = y;
            this.size = size;
            this.vx = (Math.random() - 0.5) * 6; // velocidad X
            this.vy = (Math.random() - 0.5) * 6; // velocidad Y
            this.imageUrl = imageUrl;
            this.image = new Image();
            this.image.src = imageUrl;
            this.loaded = false;
            this.image.onload = () => {
                this.loaded = true;
            };
            this.damage = 0; // para efecto visual al rebotar
        }

        update(width, height) {
            // Mover
            this.x += this.vx;
            this.y += this.vy;

            // Gravedad simple
            this.vy += 0.15; // aceleración hacia abajo

            // Rebote en bordes
            if (this.x - this.size < 0 || this.x + this.size > width) {
                this.vx *= -1;
                this.x = this.x - this.size < 0 ? this.size : width - this.size;
                this.damage = 8;
            }

            if (this.y - this.size < 0) {
                this.vy *= -0.85; // Pérdida de energía en rebote arriba
                this.y = this.size;
                this.damage = 8;
            }

            // Piso (rebote principal)
            if (this.y + this.size > height) {
                this.vy *= -0.88; // Coeficiente de restitución (pérdida de energía)
                this.y = height - this.size;
                this.damage = 10;

                // Dejar de rebotar si la velocidad es muy pequeña
                if (Math.abs(this.vy) < 0.5) {
                    this.vy = 0;
                }
            }

            // Reducir efecto de damage
            if (this.damage > 0) {
                this.damage -= 0.3;
            }
        }

        draw(ctx) {
            if (!this.loaded) return;

            ctx.save();

            // Efecto visual de impacto
            if (this.damage > 0) {
                ctx.shadowBlur = this.damage * 2;
                ctx.shadowColor = 'rgba(255, 159, 28, 0.4)';
            }

            // Dibujar imagen con borde
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(255, 255, 255, 0.1)';
            ctx.fill();

            // Clip circular para imagen
            ctx.clip();
            ctx.drawImage(
                this.image,
                this.x - this.size,
                this.y - this.size,
                this.size * 2,
                this.size * 2
            );

            ctx.restore();

            // Borde del círculo
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.strokeStyle = 'rgba(255, 159, 28, 0.6)';
            ctx.lineWidth = 2;
            ctx.stroke();
        }
    }

    /**
     * Inicializar productos
     */
    function initializeProducts() {
        products = [];
        const width = canvas.width;
        const height = canvas.height;
        const productSize = Math.min(width, height) / 12; // Tamaño proporcional

        PRODUCT_IMAGES.forEach((imageUrl, index) => {
            const x = Math.random() * (width - productSize * 2) + productSize;
            const y = Math.random() * (height * 0.4) + productSize;
            products.push(new BouncingProduct(x, y, productSize, imageUrl));
        });
    }

    /**
     * Animar rebotes
     */
    function animate() {
        const width = canvas.width;
        const height = canvas.height;

        // Limpiar canvas
        ctx.clearRect(0, 0, width, height);

        // Actualizar y dibujar productos
        products.forEach((product) => {
            product.update(width, height);
            product.draw(ctx);
        });

        animationId = requestAnimationFrame(animate);
    }

    /**
     * Ajustar canvas al tamaño del contenedor
     */
    function resizeCanvas() {
        const rect = container.getBoundingClientRect();
        canvas.width = container.offsetWidth;
        canvas.height = container.offsetHeight;
        initializeProducts();
    }

    /**
     * Abrir modal
     */
    function openModal() {
        console.log('[CARNIVAL] Opening modal...');
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
        
        if (!isAnimating) {
            resizeCanvas();
            animate();
            isAnimating = true;
            console.log('[CARNIVAL] Animation started ✅');
        }
    }

    /**
     * Cerrar modal
     */
    function closeModal() {
        modal.classList.remove('active');
        document.body.style.overflow = '';

        if (animationId) {
            cancelAnimationFrame(animationId);
            animationId = null;
        }
        isAnimating = false;

        // Marcar como mostrado en esta sesión
        sessionStorage.setItem(SESSION_KEY, 'true');
    }

    /**
     * Event Listeners
     */
    closeBtn?.addEventListener('click', closeModal);
    overlay?.addEventListener('click', closeModal);

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });

    /**
     * Mostrar modal al cargar (solo una vez por sesión)
     */
    window.addEventListener('load', () => {
        const alreadyShown = sessionStorage.getItem(SESSION_KEY);
        console.log('[CARNIVAL] Page loaded. Already shown in session?', alreadyShown);
        
        if (!alreadyShown) {
            console.log(`[CARNIVAL] Scheduling modal to open in ${SHOW_DELAY}ms...`);
            setTimeout(() => {
                console.log('[CARNIVAL] Timeout trigger - opening modal now');
                openModal();
            }, SHOW_DELAY);
        } else {
            console.log('[CARNIVAL] Modal already shown this session - skipping');
        }
    });

    /**
     * Ajustar canvas al redimensionar ventana
     */
    window.addEventListener('resize', () => {
        if (isAnimating) {
            resizeCanvas();
        }
    });

    // Exponer función para abrir modal manualmente si es necesario
    window.openCarnivalModal = openModal;
    window.closeCarnivalModal = closeModal;

})();
