(function () {
    // ── Configuración de grupos ───────────────────────────────────────────────
    const GROUPS = {
        'linea-cocina':         ['air_fryer', 'blender', 'mixer', 'stove', 'coffee_maker',
                                 'rice_cooker', 'oven', 'lonchera',
                                 'pressure_cooker', 'caldero', 'teapot',
                                 'toaster', 'sandwich_maker'],
        'planchas-ventilacion': ['iron', 'appliance'],
        electrico:              ['extension', 'power_strip', 'tv_mount'],
    };

    // Mapa inverso: category → group
    const CAT_TO_GROUP = {};
    Object.entries(GROUPS).forEach(([group, cats]) => {
        cats.forEach(cat => { CAT_TO_GROUP[cat] = group; });
    });

    // ── Elementos DOM ─────────────────────────────────────────────────────────
    const groupTabs    = document.querySelectorAll('.catalog-group-tab');
    const filterItems  = document.querySelectorAll('.filter-item[data-category]');
    const products     = document.querySelectorAll('.product[data-category]');
    const subFilterNav = document.querySelector('.catalog-sub-filters');
    const productsGrid = document.querySelector('.featured-products-grid');

    let activeGroup    = 'all';
    let activeCategory = 'all';

    // ── Helpers ───────────────────────────────────────────────────────────────
    function loadImageStatus(src) {
        return new Promise(resolve => {
            if (!src) {
                resolve(false);
                return;
            }

            const probe = new Image();
            probe.onload = () => resolve(true);
            probe.onerror = () => resolve(false);
            probe.src = src;
        });
    }

    async function prioritizeProductsWithImages() {
        if (!productsGrid || !products.length) return;

        const orderedProducts = Array.from(products).map((product, index) => ({ product, index }));

        const statuses = await Promise.all(
            orderedProducts.map(async ({ product, index }) => {
                const img = product.querySelector('.product_img');
                const hasImage = await loadImageStatus(img ? img.currentSrc || img.src : '');
                return { product, index, hasImage };
            })
        );

        statuses
            .sort((left, right) => {
                if (left.hasImage === right.hasImage) return left.index - right.index;
                return left.hasImage ? -1 : 1;
            })
            .forEach(({ product }) => {
                productsGrid.appendChild(product);
            });
    }

    function showProducts(cat) {
        products.forEach(p => {
            const match = cat === 'all' || p.dataset.category === cat;
            if (match) {
                p.style.display = 'flex';
                requestAnimationFrame(() => {
                    p.style.opacity = '1';
                    p.style.transform = 'scale(1)';
                });
            } else {
                p.style.opacity = '0';
                p.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    if (p.style.opacity === '0') p.style.display = 'none';
                }, 350);
            }
        });
    }

    function showSubFilters(group) {
        filterItems.forEach(item => {
            const cat = item.dataset.category;
            if (group === 'all') {
                item.style.display = '';          // muestra todo
            } else {
                const itemGroup = CAT_TO_GROUP[cat] || null;
                item.style.display = (cat === 'all' || itemGroup === group) ? '' : 'none';
            }
        });
    }

    function setActiveGroup(tab) {
        groupTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        activeGroup = tab.dataset.group;
    }

    function setActiveFilter(item) {
        filterItems.forEach(i => i.classList.remove('active'));
        item.classList.add('active');
        activeCategory = item.dataset.category;
    }

    // ── Scroll helper (mobile) ────────────────────────────────────────────────
    function scrollToCatalog() {
        if (window.innerWidth < 1024) {
            const el = document.getElementById('catalogo');
            if (el) el.scrollIntoView({ behavior: 'smooth' });
        }
    }

    // ── Event: click en group tab ─────────────────────────────────────────────
    groupTabs.forEach(tab => {
        tab.addEventListener('click', function () {
            setActiveGroup(this);
            showSubFilters(activeGroup);

            // Si la categoría activa no pertenece al nuevo grupo → reset a "all"
            if (activeGroup !== 'all' && activeCategory !== 'all') {
                const catGroup = CAT_TO_GROUP[activeCategory];
                if (catGroup !== activeGroup) {
                    // Activar "Todos" dentro del subfilter visible
                    const allItem = subFilterNav.querySelector('[data-category="all"]');
                    if (allItem) setActiveFilter(allItem);
                    activeCategory = 'all';
                }
            }

            // Filtrar productos: si grupo != all, mostrar solo los del grupo
            if (activeGroup === 'all') {
                showProducts('all');
            } else {
                products.forEach(p => {
                    const belongs = GROUPS[activeGroup].includes(p.dataset.category);
                    if (belongs) {
                        p.style.display = 'flex';
                        requestAnimationFrame(() => {
                            p.style.opacity = '1';
                            p.style.transform = 'scale(1)';
                        });
                    } else {
                        p.style.opacity = '0';
                        p.style.transform = 'scale(0.95)';
                        setTimeout(() => {
                            if (p.style.opacity === '0') p.style.display = 'none';
                        }, 350);
                    }
                });
            }

            scrollToCatalog();
        });
    });

    // ── Event: click en sub-filtro ────────────────────────────────────────────
    filterItems.forEach(item => {
        item.addEventListener('click', function () {
            setActiveFilter(this);
            showProducts(activeCategory);
            scrollToCatalog();
        });
    });

    // ── Init ──────────────────────────────────────────────────────────────────
    showSubFilters('all');
    prioritizeProductsWithImages();
    console.log('HomePower Catalog Filter v2 — grupos activos:', Object.keys(GROUPS));
})();