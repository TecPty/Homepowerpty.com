(function(){
    const products_categories = document.querySelectorAll('.product_category');
    let products_categories_actives = [];

    for (let i = 0; i < products_categories.length; i++) {
        products_categories[i].addEventListener('click', () => {
            products_categories[i].classList.toggle('active');

            if (products_categories[i].classList.contains('active')) {
                products_categories_actives.push(products_categories[i].dataset.category);
            } else {
                let filter_index = products_categories_actives.indexOf(products_categories[i].dataset.category);
                if(filter_index !== -1) {
                    products_categories_actives.splice(filter_index, 1);
                }
            }

            const products = document.querySelectorAll('.product');
            products.forEach(product => {
                if (products_categories_actives.length === 0) {
                    product.style.display = 'flex';
                } else {
                    if (products_categories_actives.some(category => product.dataset.category === category)) {
                        product.style.display = 'flex';
                    } else {
                        product.style.display = 'none';
                    }
                }
            });
        });
    }
})();