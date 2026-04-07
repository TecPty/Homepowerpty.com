(function() {
    console.log("🚀 HomePower Filter System Live.");
    
    // Usamos delegación de eventos para máxima fiabilidad
    document.addEventListener('click', function(e) {
        const pill = e.target.closest('.category-pill');
        if (!pill) return;
        
        e.preventDefault();
        const category = pill.dataset.category;
        console.log("🎯 Category Selected:", category);
        
        // UI: Actualizar pills active state
        document.querySelectorAll('.category-pill').forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        
        // Scroll horizontal suave (centrar pill)
        const container = document.querySelector('.category-pill-scroll');
        if (container) {
            const scrollLeft = pill.offsetLeft - (container.offsetWidth / 2) + (pill.offsetWidth / 2);
            container.scrollTo({ left: scrollLeft, behavior: 'smooth' });
        }
        
        // Lógica de filtrado
        const products = document.querySelectorAll('.product');
        products.forEach(product => {
            if (category === 'all' || product.dataset.category === category) {
                product.style.display = 'flex';
                // Trigger reflow for transition
                product.offsetHeight; 
                product.style.opacity = '1';
                product.style.transform = 'scale(1)';
            } else {
                product.style.opacity = '0';
                product.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    if (product.style.opacity === '0') {
                        product.style.display = 'none';
                    }
                }, 400);
            }
        });
    });
})();