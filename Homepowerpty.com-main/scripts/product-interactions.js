document.addEventListener('DOMContentLoaded', function() {
    // Seleccionar todos los contenedores de imágenes de productos
    const productImages = document.querySelectorAll('.product_image_wrapper');
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    const modalCaption = document.getElementById('modalCaption');

    productImages.forEach(wrapper => {
        const img = wrapper.querySelector('.product_img');
        const mainSrc = img.src;
        const boxSrc = img.dataset.box;
        let isMainImage = true;

        // Cambiar imagen al hover
        wrapper.addEventListener('mouseenter', () => {
            if (boxSrc) {
                img.src = boxSrc;
                isMainImage = false;
            }
        });

        wrapper.addEventListener('mouseleave', () => {
            img.src = mainSrc;
            isMainImage = true;
        });

        // Abrir modal al hacer click
        img.addEventListener('click', () => {
            modal.style.display = 'block';
            modalImg.src = isMainImage ? mainSrc : boxSrc;
            modalCaption.innerHTML = img.alt;
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