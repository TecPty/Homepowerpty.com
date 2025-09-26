document.addEventListener('DOMContentLoaded', function() {
    // Hover para cambiar imagen del producto a la caja
    const productImages = document.querySelectorAll('.product_img');
    
    productImages.forEach(img => {
        const originalSrc = img.src;
        const boxSrc = img.getAttribute('data-box');
        
        if (boxSrc) {
            // Hover para cambiar imagen
            img.addEventListener('mouseenter', function() {
                this.src = boxSrc;
            });
            
            img.addEventListener('mouseleave', function() {
                this.src = originalSrc;
            });
            
            // Touch para dispositivos móviles
            let touchTimeout;
            img.addEventListener('touchstart', function(e) {
                e.preventDefault();
                this.src = boxSrc;
                
                touchTimeout = setTimeout(() => {
                    this.src = originalSrc;
                }, 2000); // Vuelve a la imagen original después de 2 segundos
            });
        }
    });
    
    // Modal para ampliar imagen
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    const modalCaption = document.getElementById('modalCaption');
    const closeModal = document.getElementsByClassName('close-modal')[0];
    
    productImages.forEach(img => {
        img.addEventListener('click', function() {
            modal.style.display = 'block';
            modalImg.src = this.src;
            
            // Obtener el nombre del producto
            const productCard = this.closest('.product');
            const productName = productCard.querySelector('.product_name').textContent;
            modalCaption.textContent = productName;
        });
    });
    
    // Cerrar modal
    if (closeModal) {
        closeModal.addEventListener('click', function() {
            modal.style.display = 'none';
        });
    }
    
    // Cerrar modal al hacer click fuera
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
    
    // Cerrar modal con ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.style.display === 'block') {
            modal.style.display = 'none';
        }
    });
    
    // Precargar imágenes de caja para mejor rendimiento
    productImages.forEach(img => {
        const boxSrc = img.getAttribute('data-box');
        if (boxSrc) {
            const preloadImg = new Image();
            preloadImg.src = boxSrc;
        }
    });
});