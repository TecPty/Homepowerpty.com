// Filtros de productos mejorados
document.addEventListener('DOMContentLoaded', function() {
    const filterButtons = document.querySelectorAll('.product_category');
    const products = document.querySelectorAll('.product');

    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const category = this.getAttribute('data-category');
            
            // Remover clase active de todos los botones
            filterButtons.forEach(btn => btn.classList.remove('active'));
            
            // Agregar clase active al botón actual
            this.classList.add('active');
            
            // Filtrar productos
            products.forEach(product => {
                const productCategory = product.getAttribute('data-category');
                
                if (category === 'all' || productCategory === category) {
                    product.style.display = 'block';
                    product.style.animation = 'fadeIn 0.5s ease';
                } else {
                    product.style.display = 'none';
                }
            });
        });
    });
});

// Animación CSS para fadeIn
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
`;
document.head.appendChild(style);