/* Catalog — módulo ES
 * Lógica original de filter_products.js sin cambios. Solo envuelto en init() + export.
 * Selectores reales del HTML: .catalog-group-tab, .filter-item[data-category], .product[data-category]
 */
const Catalog = {
  init() {
    const GROUPS = {
      'linea-cocina':         ['air_fryer', 'blender', 'mixer', 'stove', 'coffee_maker',
                               'rice_cooker', 'oven', 'lonchera',
                               'pressure_cooker', 'caldero', 'teapot',
                               'toaster', 'sandwich_maker'],
      'planchas-ventilacion': ['iron', 'appliance'],
      electrico:              ['extension', 'power_strip', 'tv_mount'],
    };

    const CAT_TO_GROUP = {};
    Object.entries(GROUPS).forEach(([group, cats]) => {
      cats.forEach(cat => { CAT_TO_GROUP[cat] = group; });
    });

    const groupTabs    = document.querySelectorAll('.catalog-group-tab');
    const filterItems  = document.querySelectorAll('.filter-item[data-category]');
    const products     = document.querySelectorAll('.product[data-category]');
    const subFilterNav = document.querySelector('.catalog-sub-filters');
    const productsGrid = document.querySelector('.featured-products-grid');

    if (!groupTabs.length && !filterItems.length) return; // guard

    let activeGroup    = 'all';
    let activeCategory = 'all';

    function loadImageStatus(src) {
      return new Promise(resolve => {
        if (!src) { resolve(false); return; }
        const probe = new Image();
        probe.onload  = () => resolve(true);
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
        .sort((l, r) => {
          if (l.hasImage === r.hasImage) return l.index - r.index;
          return l.hasImage ? -1 : 1;
        })
        .forEach(({ product }) => productsGrid.appendChild(product));
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
          setTimeout(() => { if (p.style.opacity === '0') p.style.display = 'none'; }, 350);
        }
      });
    }

    function showSubFilters(group) {
      filterItems.forEach(item => {
        const cat = item.dataset.category;
        if (group === 'all') {
          item.style.display = '';
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

    function scrollToCatalog() {
      if (window.innerWidth < 1024) {
        const el = document.getElementById('catalogo');
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      }
    }

    groupTabs.forEach(tab => {
      tab.addEventListener('click', function () {
        setActiveGroup(this);
        showSubFilters(activeGroup);

        if (activeGroup !== 'all' && activeCategory !== 'all') {
          const catGroup = CAT_TO_GROUP[activeCategory];
          if (catGroup !== activeGroup) {
            const allItem = subFilterNav ? subFilterNav.querySelector('[data-category="all"]') : null;
            if (allItem) setActiveFilter(allItem);
            activeCategory = 'all';
          }
        }

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
              setTimeout(() => { if (p.style.opacity === '0') p.style.display = 'none'; }, 350);
            }
          });
        }

        scrollToCatalog();
      });
    });

    filterItems.forEach(item => {
      item.addEventListener('click', function () {
        setActiveFilter(this);
        showProducts(activeCategory);
        scrollToCatalog();
      });
    });

    showSubFilters('all');
    prioritizeProductsWithImages();
  },
};

export default Catalog;
