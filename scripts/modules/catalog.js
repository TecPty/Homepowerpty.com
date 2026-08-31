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
                               'toaster', 'sandwich_maker', 'juicer', 'food_processor'],
      'planchas-ventilacion': ['iron', 'appliance', 'scale'],
      electrico:              ['extension', 'power_strip', 'tv_mount'],
    };

    const CAT_TO_GROUP = {};
    Object.entries(GROUPS).forEach(([group, cats]) => {
      cats.forEach(cat => { CAT_TO_GROUP[cat] = group; });
    });

    const groupTabs    = document.querySelectorAll('.catalog-group-tab');
    const filterItems  = document.querySelectorAll('.filter-item[data-category]');
    const subFilterNav = document.querySelector('.catalog-sub-filters');
    const productsGrid = document.querySelector('.featured-products-grid');

    function getProducts() {
      return Array.from(document.querySelectorAll('.product[data-category]'));
    }

    function parseModel(text) {
      return (text || '').replace(/^\s*MOD:\s*/i, '').trim();
    }

    function parseVariantLabel(name) {
      const match = (name || '').match(/(\d+(?:[\.,]\d+)?\s*(?:m|cm|l))/i);
      return match ? match[1].replace(/\s+/g, '') : name;
    }

    function buildGroupedCard(items, options) {
      if (!items.length) return null;

      const templateBase = options.templateBase;
      const groupTitle = options.groupTitle;
      const category = options.category;
      const modelOrder = Array.isArray(options.models) ? options.models : [];

      const variants = items.map(item => {
        const nameEl = item.querySelector('.product_name a');
        const skuEl = item.querySelector('.product_sku');
        const imgEl = item.querySelector('.product_img');
        const model = parseModel(skuEl?.textContent || '');
        const name = (nameEl?.textContent || '').trim();
        return {
          model,
          name,
          href: `${templateBase}?mod=${encodeURIComponent(model)}`,
          image: imgEl?.getAttribute('src') || '',
          alt: imgEl?.getAttribute('alt') || name,
          label: parseVariantLabel(name),
        };
      });

      if (modelOrder.length) {
        const orderMap = new Map(modelOrder.map((model, idx) => [model, idx]));
        variants.sort((a, b) => {
          const aIdx = orderMap.has(a.model) ? orderMap.get(a.model) : Number.MAX_SAFE_INTEGER;
          const bIdx = orderMap.has(b.model) ? orderMap.get(b.model) : Number.MAX_SAFE_INTEGER;
          return aIdx - bIdx;
        });
      }

      const primary = variants[0];
      const codes = variants.map(v => v.model).filter(Boolean);
      const labels = variants.map(v => v.label).filter(Boolean);
      const variantList = variants.map(v => (
        `<a href="${v.href}" class="product_variant_chip">${v.model}</a>`
      )).join('');
      const thumbs = variants.slice(0, 5).map(v => (
        `<a href="${v.href}" class="product_variant_thumb" aria-label="Ver variante ${v.model}">
            <img src="${v.image}" alt="${v.alt}" loading="lazy">
        </a>`
      )).join('');
      const skuHtml = codes.map(c => `<span class="sku-code">${c}</span>`).join(' · ');

      const card = document.createElement('li');
      card.className = 'product product--grouped';
      card.dataset.category = category;
      card.dataset.variants = codes.join(' ');

      const isSimple = options.simple || false;

      card.innerHTML = `
        <a href="${primary.href}" class="product_image_wrapper">
          <img src="${primary.image}" alt="${primary.alt}" class="product_img" loading="lazy">
        </a>
        <div class="product_content">
          <h3 class="product_name"><a href="${primary.href}">${groupTitle}</a></h3>
          <span class="product_sku">${skuHtml}</span>
          <ul class="product_features">
            ${isSimple
              ? `<li>${variants.length} Medidas disponibles</li>`
              : `<li>${variants.length} códigos disponibles</li>
            <li>Medidas: ${labels.join(', ')}</li>`
            }
          </ul>
          ${isSimple ? '' : `
          <div class="product_variants" aria-label="Variantes disponibles">
            ${variantList}
          </div>
          <div class="product_variant_gallery" aria-label="Imágenes de variantes">
            ${thumbs}
          </div>`}
        </div>`;

      return card;
    }

    function groupCatalogVariants() {
      if (!productsGrid) return;

      function productLinkHref(product) {
        const linkEl = product.querySelector('.product_image_wrapper');
        if (!linkEl) return '';
        const href = linkEl.getAttribute('href') || '';
        return href.replace(/\\/g, '/');
      }

      const groups = [
        {
          category: 'extension',
          models: ['HP-050', 'HP-051', 'HP-052', 'HP-053', 'HP-054'],
          templateBase: 'productos/extensiones/cable-extension/',
          groupTitle: 'Extension Blanca',
          simple: true,
        },
        {
          category: 'extension',
          models: ['HP-055', 'HP-056', 'HP-057', 'HP-058', 'HP-059', 'HP-060', 'HP-061'],
          templateBase: 'productos/extensiones/extension-naranja/',
          groupTitle: 'Extensión Naranja',
          simple: true,
        },
        {
          category: 'extension',
          models: ['HP-062', 'HP-063', 'HP-064', 'HP-065', 'HP-066', 'HP-067', 'HP-068'],
          templateBase: 'productos/extensiones/extension-amarilla/',
          groupTitle: 'Extensión Amarilla',
          simple: true,
        },
        {
          category: 'caldero',
          models: ['HP-030', 'HP-031', 'HP-032', 'HP-033', 'HP-034'],
          templateBase: 'productos/calderos/caldero-vidrio/',
          groupTitle: 'Caldero Tapa Vidrio',
          simple: true,
        },
        {
          category: 'caldero',
          models: ['HP-025', 'HP-026', 'HP-027', 'HP-028', 'HP-029'],
          templateBase: 'productos/calderos/caldero-aluminio/',
          groupTitle: 'Caldero Tapa Aluminio',
          simple: true,
        },
        {
          category: 'pressure_cooker',
          models: ['HP-035', 'HP-036', 'HP-037', 'HP-038', 'HP-039'],
          templateBase: 'productos/ollas/olla-presion-aluminio/',
          groupTitle: 'Ollas a Presion Aluminio Pulido',
          simple: true,
        },
        {
          category: 'pressure_cooker',
          models: ['CK-02-18', 'CK-02-20', 'CK-02-22', 'CK-02-24', 'CK-02-26'],
          templateBase: 'productos/ollas/olla-presion-ck02/',
          groupTitle: 'Ollas a Presion Aluminio',
          simple: true,
        },
        {
          category: 'rice_cooker',
          models: ['HT-03', 'HT-15', 'HT-18', 'HT-22'],
          modelPathMap: {
            'HT-03': 'productos/arroceras/ht-03/',
            'HT-15': 'productos/arroceras/ht-15/',
            'HT-18': 'productos/arroceras/ht-18/',
            'HT-22': 'productos/arroceras/ht-22/',
          },
          templateBase: 'productos/arroceras/arrocera-ht/',
          groupTitle: 'Arrocera sin Vaporera',
          simple: true,
        },
        {
          category: 'rice_cooker',
          models: ['HT-15A', 'HT-18A', 'HT-22A'],
          modelPathMap: {
            'HT-15A': 'productos/arroceras/ht-15a/',
            'HT-18A': 'productos/arroceras/ht-18a/',
            'HT-22A': 'productos/arroceras/ht-22a/',
          },
          templateBase: 'productos/arroceras/arrocera-vaporera-hta/',
          groupTitle: 'Arrocera con Vaporera',
          simple: true,
        },
      ];

      groups.forEach(group => {
        const groupedItems = getProducts().filter(product => {
          if (product.dataset.category !== group.category) return false;
          const skuEl = product.querySelector('.product_sku');
          const model = parseModel(skuEl?.textContent || '');
          if (!group.models.includes(model)) return false;

          if (group.modelPathMap && group.modelPathMap[model]) {
            const href = productLinkHref(product);
            return href.includes(group.modelPathMap[model]);
          }

          return true;
        });

        if (groupedItems.length < 2) return;

        const groupedCard = buildGroupedCard(groupedItems, {
          category: group.category,
          models: group.models,
          templateBase: group.templateBase,
          groupTitle: group.groupTitle,
          simple: group.simple || false,
        });
        if (!groupedCard) return;

        const insertBefore = groupedItems[0];
        productsGrid.insertBefore(groupedCard, insertBefore);
        groupedItems.forEach(card => card.remove());
      });
    }

    if (!groupTabs.length && !filterItems.length) return; // guard

    groupCatalogVariants();

    // Strip "MOD: " prefix and move SKU below title for all static product cards
    document.querySelectorAll('.product:not(.product--grouped) .product_content').forEach(content => {
      const sku = content.querySelector('.product_sku');
      const name = content.querySelector('.product_name');
      if (sku) sku.textContent = sku.textContent.replace(/^\s*MOD:\s*/i, '').trim();
      if (sku && name && content.firstElementChild === sku) {
        // Move SKU to after the name
        name.insertAdjacentElement('afterend', sku);
      }
    });

    let products = getProducts();
    let activeGroup    = 'all';
    let activeCategory = 'all';
    let searchQuery    = '';

    // Elemento de búsqueda
    const searchInput = document.getElementById('catalog-search');

    // Mensaje de sin resultados (lo insertamos una vez)
    let noResultsEl = productsGrid ? productsGrid.querySelector('.catalog-no-results') : null;
    if (productsGrid && !noResultsEl) {
      noResultsEl = document.createElement('li');
      noResultsEl.className = 'catalog-no-results';
      noResultsEl.textContent = 'No se encontraron productos.';
      productsGrid.appendChild(noResultsEl);
    }

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
      const orderedProducts = products.map((product, index) => ({ product, index }));
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
      const q = searchQuery.trim().toLowerCase();
      let visible = 0;
      products.forEach(p => {
        const catMatch  = cat === 'all' || p.dataset.category === cat;
        let   textMatch = true;
        if (q) {
          const name = (p.querySelector('.product_name')?.textContent || '').toLowerCase();
          const sku  = (p.querySelector('.product_sku')?.textContent || '').toLowerCase();
          const variants = (p.dataset.variants || '').toLowerCase();
          textMatch  = name.includes(q) || sku.includes(q) || variants.includes(q);
        }
        const show = catMatch && textMatch;
        if (show) {
          visible++;
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
      if (noResultsEl) noResultsEl.style.display = visible === 0 ? 'block' : 'none';
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

    function scrollToCatalog(immediate = false) {
      const el = document.getElementById('catalogo');
      if (el) {
        // En desktop bajamos un poco más para que la búsqueda/filtros no queden pegados arriba
        const offset = window.innerWidth >= 1024 ? 60 : 0;
        const rect = el.getBoundingClientRect();
        const top = rect.top + window.pageYOffset - offset;
        window.scrollTo({ 
          top, 
          behavior: immediate ? 'auto' : 'smooth' 
        });
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

    if (searchInput) {
      searchInput.addEventListener('input', function () {
        searchQuery = this.value;
        showProducts(activeCategory);
      });
    }

    // --- LÓGICA DE FILTRO POR URL ---
    const params = new URLSearchParams(window.location.search);
    const catParam = params.get('cat');
    if (catParam) {
      const targetItem = Array.from(filterItems).find(i => i.dataset.category === catParam);
      if (targetItem) {
        // Determinamos el grupo para activar el tab correspondiente
        const groupKey = CAT_TO_GROUP[catParam];
        if (groupKey) {
          const targetTab = Array.from(groupTabs).find(t => t.dataset.group === groupKey);
          if (targetTab) {
            setActiveGroup(targetTab);
            showSubFilters(groupKey);
          }
        }
        
        setActiveFilter(targetItem);
        showProducts(catParam);
        
        // Scroll inmediato si venimos de una categoría (evita el "rebote" por el anclaje #productos)
        scrollToCatalog(true);
      }
    }

    products = getProducts();
    showSubFilters('all');
    prioritizeProductsWithImages();
  },
};

export default Catalog;
