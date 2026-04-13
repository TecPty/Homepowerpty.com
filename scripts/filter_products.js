(function() {
    console.log("🚀 HomePower Sidebar Filter Live.");

    const items = document.querySelectorAll('.filter-item');
    const products = document.querySelectorAll('.product');

    // 1. Selection Logic (Click on sidebar item)
    items.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const category = this.dataset.category;

            console.log("🎯 Category Selection:", category);

            // UI Updates: Mark active item
            items.forEach(i => i.classList.remove('active'));
            this.classList.add('active');

            // Filtering Logic
            products.forEach(product => {
                if (category === 'all' || product.dataset.category === category) {
                    product.style.display = 'flex';
                    product.offsetHeight; // Reflow for transition
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

            // Opcional: Auto-scroll al inicio del catálogo en móvil
            if (window.innerWidth < 1024) {
                document.getElementById('catalogo').scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
})();