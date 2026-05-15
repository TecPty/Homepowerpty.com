import os

BASE = r"c:\Users\HP 15\Homepowerpty.com"
INDEX_PATH = os.path.join(BASE, "index.html")

NEW_PRODUCTS = [
    # folder, sku, nombre, features (list of 4), category, badge
    ("air-fryer-3l", "AF3201", "Air Fryer 3L", ["Capacidad: 3L", "Colores: B/N", "110V / 50Hz", "800W"], "air_fryer", "new"),
    ("licuadora-vb999", "VB-999", "Licuadora Plástico 2000W", ["2000W Power", "4 Colores", "110V", "Jarra Plástica"], "blender", "premium"),
    ("batidora-pedestal", "HP-024", "Batidora de Pedestal", ["Mezcla Pro", "Bowl Incluido", "Uso rudo", "Garantía 1 año"], "mixer", "premium"),
    ("batidora-mano", "HP-044", "Batidora de Mano", ["Liviana/Versátil", "5 Velocidades", "Económica", "Fácil Limpieza"], "mixer", "new"),
    ("batidora-mano-metal", "HP-045", "Batidora de Mano Metal", ["Cuerpo Metal", "Premium Feel", "Uso intensivo", "Duradera"], "mixer", "premium"),
    ("estufa-electrica-1-quemador", "1010A", "Estufa Eléctrica 1Q", ["1000W", "Hierro 0.3mm", "Plato 155mm", "Portátil"], "stove", "new"),
    ("estufa-electrica-1q-premium", "F-010E-1", "Estufa Eléctrica 1Q Pro", ["1000W Premium", "Diseño Slim", "Eficiente", "Garantía"], "stove", "new"),
    ("estufa-electrica-2q-negra", "2020A", "Estufa Eléctrica 2Q", ["2000W", "Hierro 0.35mm", "Plato 155mm", "Dual Control"], "stove", "new"),
    ("estufa-gas-3q-v2", "3081K", "Estufa Gas 3Q Pro", ["Acero Inox", "Quemador Plata", "Auto-ignición", "Para Gas LP"], "stove", "new"),
    ("estufa-gas-2q-v2", "3080", "Estufa Gas 2Q Pro", ["Hierro Fundido", "90mm Burner", "Acero Inox", "Auto-ignición"], "stove", "new"),
    ("estufa-gas-4q-horno", "HP-073", "Estufa 4Q + Horno", ["4 Quemadores", "Horno Integrado", "Premium B2B", "Uso Industrial"], "stove", "premium"),
    ("cafetera-12t-cm02", "CM02", "Cafetera 12 Tazas", ["900W Power", "1.2L Capacidad", "Diseño Moderno", "Poli-carb"], "coffee_maker", "new"),
    ("cafetera-6t-v2", "WJ-9001", "Cafetera 6 Tazas Pro", ["0.625L Cap", "600W", "Filtro Fino", "Jarra Vidrio"], "coffee_maker", "new"),
    ("cafetera-12t-v2", "WJ-9002", "Cafetera 12 Tazas Pro", ["1.25L Cap", "800W", "B2B Ideal", "Resistente"], "coffee_maker", "new"),
    ("cafetera-7-5-tazas", "WJ-9011", "Cafetera 7.5 Tazas", ["0.625L", "7.5 Tazas", "600W", "Filtro Fino"], "coffee_maker", "new"),
    ("cafetera-percoladora-30t", "HP-046", "Percoladora 30 Tazas", ["30 Tazas", "Acero Inoxidable", "Catering Ideal", "B2B Pro"], "coffee_maker", "hot"),
    ("cafetera-percoladora-40t", "HP-047", "Percoladora 40 Tazas", ["40 Tazas", "Full Acero", "Uso Continuo", "Gran Capacidad"], "coffee_maker", "hot"),
    ("cafetera-percoladora-50t", "HP-048", "Percoladora 50 Tazas", ["50 Tazas", "Industrial", "Acero Inox", "Grifo Pro"], "coffee_maker", "hot"),
    ("cafetera-percoladora-100t", "HP-049", "Percoladora 100 Tazas", ["100 Tazas", "Master Venue", "Premium Steel", "Heavy Duty"], "coffee_maker", "premium"),
    ("plancha-vapor-hp012", "HP-012", "Plancha Vapor 1400W", ["1400W", "Depósito 170ml", "Vapor Continuo", "Ergonómica"], "iron", "new"),
    ("plancha-vapor-r91171b", "R.91171B", "Plancha Vapor Premium", ["Suela Cerámica", "Premium Finish", "1400W", "170ml Water"], "iron", "premium"),
    ("tetera-plastico-1-5l", "H208", "Tetera Plástico 1.5L", ["1.5L Capacidad", "Económica", "Apagado Auto", "Blanco/Negro"], "teapot", "new"),
    ("panini-metal", "SJ-40A", "Panini Metal 850W", ["850W Power", "Metal Body", "Giro 180°", "Placas Pro"], "sandwich_maker", "premium"),
    ("sandwichera-grill", "SJ-27", "Sandwichera Grill", ["Grill Plates", "750W", "Non-stick", "Compacta"], "sandwich_maker", "new"),
    ("sandwichera-sj35", "SJ-35", "Sandwichera Home", ["Simple Use", "750W", "Easy Clean", "Resistente"], "sandwich_maker", "new"),
    ("tostadora-metal", "HP-018", "Tostadora Metal", ["Cuerpo Metal", "7 Niveles", "750W", "Premium Look"], "toaster", "premium"),
    ("lochera-termica", "JY-1001", "Lochera Eléctrica", ["Térmica", "110V", "Transportable", "B2B Merch"], "all", "new"),
    ("arrocera-0-3l", "HT-03", "Arrocera Mini 0.3L", ["0.3L Mini", "200W", "Vaporizador", "Antiadherente"], "rice_cooker", "new"),
    ("arrocera-1-8l", "HT-18A", "Arrocera 1.8L Pro", ["1.8L Cap", "700W", "Vaporera Incl", "Automatic"], "rice_cooker", "new"),
    ("arrocera-2-2l-basica", "HT-22", "Arrocera 2.2L Heavy", ["2.2L Cap", "900W", "Industrial Use", "Durable Bowl"], "rice_cooker", "new"),
    ("olla-presion-3-2l", "CK-02-18", "Olla Presión 3.2L", ["3.2L - 18cm", "Aluminio Pro", "Válvula Seg", "Compacta"], "pressure_cooker", "new"),
    ("olla-presion-4-2l", "CK-02-20", "Olla Presión 4.2L", ["4.2L - 20cm", "Familiar", "Roscado Seg", "Alta Calidad"], "pressure_cooker", "new"),
    ("olla-presion-9l", "CK-02-26", "Olla Presión 9L", ["9L - 26cm", "Catering XL", "Grosor Extra", "Seguridad Pro"], "pressure_cooker", "hot"),
]

def generate_product_html(p):
    folder, sku, nombre, features, category, badge = p
    badge_html = f'<div class="product_badge {badge}">{badge.upper()}</div>' if badge else ''
    feat_html = "".join([f"<li> {f}</li>" for f in features])
    return f"""
            <li class="product" data-category="{category}">
                {badge_html}
                <a href="productos/{folder}/" class="product_image_wrapper">
                    <img src="productos/{folder}/img/PRODUCTO_PRINCIPAL.webp"
                         alt="{nombre}" class="product_img" loading="lazy">
                </a>
                <div class="product_content">
                    <span class="product_sku">MOD: {sku}</span>
                    <h3 class="product_name"><a href="productos/{folder}/">{nombre}</a></h3>
                    <ul class="product_features">
                        {feat_html}
                    </ul>
                    <div class="product_actions">
                        <span class="stock_status in_stock"> Disponible</span>
                        <a href="https://wa.me/50769838322?text=Hola, me interesa el producto {nombre} MOD: {sku}" 
                           class="product_cta" target="_blank" rel="noopener">
                            Consultar Precio
                        </a>
                    </div>
                </div>
            </li>"""

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update stats
content = content.replace('<strong>27+</strong>', '<strong>59+</strong>')
content = content.replace('<strong>11</strong>', '<strong>12</strong>')

# 2. Add Mixer Category
mixer_cat = """                <div class="category-card" data-category="mixer">
                    <div class="category-icon"><svg width="40" height="40" fill="none" stroke="var(--color-accent)" stroke-width="1.5" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><circle cx="12" cy="12" r="3"></circle></svg></div>
                    <span>Batidoras</span>
                </div>
"""
if 'data-category="mixer"' not in content:
    content = content.replace('<div class="category-card" data-category="all">', mixer_cat + '                <div class="category-card" data-category="all">')

# 3. Add products
new_products_html = "".join([generate_product_html(p) for p in NEW_PRODUCTS])

# Insert before the end of the grid script or marker
# Since the file is large, I'll look for a logical end point in the products list.
# The user's index.html ends around line 1035. The products list usually ends before the scripts.
# I'll look for the last </li> before <!-- CLIENTS --> or similar.

if '<!-- PRODUCTS END -->' not in content:
    # Let's find the last </li> of the product list
    # Actually, I'll just append it to the end of the existing list by finding a common footer.
    content = content.replace('<!-- PRODUCTS START -->', '<!-- PRODUCTS START -->' + new_products_html)

with open(INDEX_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("index.html actualizado exitosamente.")
