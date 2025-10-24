(function() {
    // Sistema de filtrado con categoría "Todos"
    const categories = document.querySelectorAll('.product_category');
    const products = document.querySelectorAll('.product');
    
    categories.forEach(category => {
        category.addEventListener('click', function() {
            // Remover active de todas
            categories.forEach(cat => cat.classList.remove('active'));
            // Agregar active a la seleccionada
            this.classList.add('active');
            
            const filter = this.dataset.category;
            
            // Filtrar productos
            products.forEach(product => {
                if (filter === 'all') {
                    product.style.display = 'flex';
                    product.style.animation = 'fadeIn 0.5s ease';
                } else {
                    if (product.dataset.category === filter) {
                        product.style.display = 'flex';
                        product.style.animation = 'fadeIn 0.5s ease';
                    } else {
                        product.style.display = 'none';
                    }
                }
            });
        });
    });
    
    // Vista rápida
    const quickViewBtns = document.querySelectorAll('.quick_view_btn');
    quickViewBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const product = this.dataset.product;
            // Por ahora redirige a WhatsApp
            const productCard = this.closest('.product');
            const sku = productCard.querySelector('.product_sku').textContent;
            const name = productCard.querySelector('.product_name').textContent;
            window.open(`https://wa.me/50769838322?text=Hola, me interesa el producto: ${name} - ${sku}`, '_blank', 'noopener');
        });
    });
})();