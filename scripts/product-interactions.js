document.addEventListener('DOMContentLoaded', function() {
    // Seleccionar todos los contenedores de imágenes de productos
    const productImages = document.querySelectorAll('.product_image_wrapper');
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    const modalCaption = document.getElementById('modalCaption');

    productImages.forEach(wrapper => {
        const picture = wrapper.querySelector('picture');
        const img = wrapper.querySelector('.product_img');
        if (!picture || !img) return;

        let isMainImage = true;
        const mainSrc = img.src;
        const boxSrc = img.dataset.box;

        // Función para cambiar entre fuentes de imagen
        const toggleImageSources = (showHover) => {
            const mainSources = Array.from(picture.querySelectorAll('source:not([data-hover])'));
            const hoverSources = Array.from(picture.querySelectorAll('source[data-hover]'));
            
            if (showHover) {
                // Ocultar fuentes principales
                mainSources.forEach(source => {
                    source.dataset.originalSrcset = source.srcset;
                    source.srcset = '';
                });
                
                // Mostrar fuentes hover
                hoverSources.forEach(source => {
                    source.srcset = source.dataset.originalSrcset || source.srcset;
                });
                
                // Actualizar imagen por defecto
                img.src = boxSrc;
                isMainImage = false;
            } else {
                // Restaurar fuentes principales
                mainSources.forEach(source => {
                    source.srcset = source.dataset.originalSrcset || source.srcset;
                });
                
                // Ocultar fuentes hover
                hoverSources.forEach(source => {
                    source.srcset = '';
                });
                
                // Restaurar imagen por defecto
                img.src = mainSrc;
                isMainImage = true;
            }
        };

        // Cambiar imagen al hover
        wrapper.addEventListener('mouseenter', () => {
            toggleImageSources(true);
        });

        wrapper.addEventListener('mouseleave', () => {
            toggleImageSources(false);
        });

        // Abrir modal al hacer click
        img.addEventListener('click', () => {
            if (modal) {
                modal.style.display = 'block';
                if (modalImg) modalImg.src = isMainImage ? mainSrc : boxSrc;
                if (modalCaption) modalCaption.innerHTML = img.alt;
            }
        });
    });

    // Cerrar modal
    const closeModal = document.querySelector('.close-modal');
    closeModal.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    // Cerrar modal al hacer click fuera de la imagen
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Cerrar modal con ESC
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            modal.style.display = 'none';
        }
    });
});