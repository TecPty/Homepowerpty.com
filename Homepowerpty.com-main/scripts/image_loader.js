/**
 * Image Loader - Optimización de carga de imágenes
 * Maneja lazy loading y animaciones de carga
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // Seleccionar todas las imágenes de productos
    const productImages = document.querySelectorAll('.product_img');
    const bannerImage = document.querySelector('.banner_img');
    
    /**
     * Función para manejar la carga de una imagen
     */
    function handleImageLoad(img) {
        if (img.complete) {
            img.classList.add('loaded');
        } else {
            img.addEventListener('load', function() {
                img.classList.add('loaded');
            });
            
            img.addEventListener('error', function() {
                console.warn('Error al cargar imagen:', img.src);
                img.classList.add('loaded'); // Mostrar aunque haya error
            });
        }
    }
    
    // Procesar imagen del banner inmediatamente
    if (bannerImage) {
        handleImageLoad(bannerImage);
    }
    
    // Procesar imágenes de productos con Intersection Observer
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    handleImageLoad(img);
                    observer.unobserve(img);
                }
            });
        }, {
            rootMargin: '50px 0px',
            threshold: 0.01
        });
        
        productImages.forEach(img => {
            imageObserver.observe(img);
        });
    } else {
        // Fallback para navegadores antiguos
        productImages.forEach(img => {
            handleImageLoad(img);
        });
    }
    
    // Precargar imágenes críticas
    const criticalImages = [
        'media/icons/logo/logo.png',
        'media/images/banner/banner_img.png'
    ];
    
    criticalImages.forEach(src => {
        const link = document.createElement('link');
        link.rel = 'preload';
        link.as = 'image';
        link.href = src;
        document.head.appendChild(link);
    });
    
    // Mejorar performance con requestIdleCallback
    if ('requestIdleCallback' in window) {
        requestIdleCallback(() => {
            // Precarga de imágenes de productos visibles
            const visibleProducts = document.querySelectorAll('.product:nth-child(-n+6) .product_img');
            visibleProducts.forEach(img => {
                if (img.loading === 'lazy') {
                    const tempImg = new Image();
                    tempImg.src = img.src;
                }
            });
        });
    }
});

// Optimización adicional: comprimir imágenes dinámicamente si el navegador lo soporta
if ('connection' in navigator) {
    const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    
    if (connection && connection.effectiveType) {
        // Si la conexión es lenta, podemos ajustar la calidad
        if (connection.effectiveType === 'slow-2g' || connection.effectiveType === '2g') {
            document.body.classList.add('low-bandwidth');
            console.log('Modo de ancho de banda bajo activado');
        }
    }
}
