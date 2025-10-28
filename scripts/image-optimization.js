/**
 * Optimización de imágenes
 * Maneja lazy loading, capacidades del navegador y optimizaciones
 */

document.addEventListener('DOMContentLoaded', function() {
    // Detectar soporte para WebP
    function checkWebP(callback) {
        const webP = new Image();
        webP.onload = webP.onerror = function () {
            callback(webP.height === 2);
        };
        webP.src = 'data:image/webp;base64,UklGRjoAAABXRUJQVlA4IC4AAACyAgCdASoCAAIALmk0mk0iIiIiIgBoSygABc6WWgAA/veff/0PP8bA//LwYAAA';
    }

    // Verificar conexión lenta
    const isSlowConnection = () => {
        return navigator.connection && 
               (navigator.connection.saveData || 
                navigator.connection.effectiveType.includes('2g') ||
                navigator.connection.effectiveType.includes('3g'));
    }

    // Inicializar optimizaciones
    function initImageOptimizations() {
        const hasSlowConnection = isSlowConnection();
        
        // Configurar el observador de intersección para lazy loading
        const imageObserver = new IntersectionObserver(
            (entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        const parent = img.closest('.product_image_wrapper');
                        
                        // En conexiones lentas, cargar imágenes de menor resolución
                        if (hasSlowConnection && parent) {
                            const sources = parent.querySelectorAll('source[srcset]');
                            sources.forEach(source => {
                                const srcset = source.srcset.split(',')
                                    .filter(src => src.includes('400w'))
                                    .join(',');
                                if (srcset) source.srcset = srcset;
                            });
                        }

                        // Marcar como cargada
                        img.classList.add('loaded');
                        observer.unobserve(img);
                    }
                });
            },
            {
                rootMargin: '50px 0px',
                threshold: 0.01
            }
        );

        // Observar todas las imágenes de productos
        document.querySelectorAll('.product_img').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Verificar soporte WebP y configurar el documento
    checkWebP(hasWebP => {
        if (!hasWebP) {
            document.documentElement.classList.add('no-webp');
        }
        initImageOptimizations();
    });

    // Evento para actualizar las imágenes cuando cambie la conexión
    if (navigator.connection) {
        navigator.connection.addEventListener('change', initImageOptimizations);
    }
});