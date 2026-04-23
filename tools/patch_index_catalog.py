"""
Patch index.html:
  1. Reemplaza sidebar de filtros plano por filtros agrupados (2 niveles)
  2. Agrega 55 product cards al grid
  3. Actualiza nav links "Electrodomésticos" → "Catálogo"
  4. Actualiza stat counter 59+ → 110+
"""
import re, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(BASE, "index.html")

with open(HTML, encoding="utf-8") as f:
    content = f.read()

# ─── 1. Nav links ────────────────────────────────────────────────────────────
content = content.replace(
    '<a href="#productos">Electrodomésticos</a>',
    '<a href="#catalogo">Catálogo</a>'
)
content = content.replace(
    '<a href="#productos" class="fullscreen-menu-link">Electrodomésticos</a>',
    '<a href="#catalogo" class="fullscreen-menu-link">Catálogo</a>'
)

# ─── 2. Stat counter ─────────────────────────────────────────────────────────
content = content.replace('<strong>59+</strong>', '<strong>110+</strong>')

# ─── 3. Sidebar — reemplazar bloque completo ─────────────────────────────────
OLD_SIDEBAR = """                    <!-- Sidebar Lateral de Filtros -->
                    <aside class="catalog-sidebar">
                        <h4>Filtrar por</h4>
                        <nav class="filter-group">
                            <div class="filter-item active" data-category="all">Todos los productos</div>
                            <div class="filter-item" data-category="air_fryer">Air Fryer</div>
                            <div class="filter-item" data-category="blender">Licuadoras</div>
                            <div class="filter-item" data-category="mixer">Batidoras</div>
                            <div class="filter-item" data-category="stove">Estufas</div>
                            <div class="filter-item" data-category="coffee_maker">Cafeteras</div>
                            <div class="filter-item" data-category="iron">Planchas</div>
                            <div class="filter-item" data-category="teapot">Teteras</div>
                            <div class="filter-item" data-category="toaster">Tostadoras</div>
                            <div class="filter-item" data-category="sandwich_maker">Sandwicheras</div>
                            <div class="filter-item" data-category="rice_cooker">Arroceras</div>
                            <div class="filter-item" data-category="pressure_cooker">Ollas de Presión</div>
                            <div class="filter-item" data-category="oven">Hornos</div>
                            <div class="filter-item" data-category="lonchera">Loncheras</div>
                        </nav>
                    </aside>"""

NEW_SIDEBAR = """                    <!-- Sidebar Lateral de Filtros (v2 — grupos) -->
                    <aside class="catalog-sidebar">
                        <h4>Catálogo</h4>

                        <!-- Fila 1: Grupos (tabs) -->
                        <nav class="catalog-group-tabs" aria-label="Grupos de producto">
                            <button class="catalog-group-tab active" data-group="all">Todos</button>
                            <button class="catalog-group-tab" data-group="cocina">🍳 Cocina</button>
                            <button class="catalog-group-tab" data-group="utensilios">🥘 Utensilios</button>
                            <button class="catalog-group-tab" data-group="hogar">🔌 Hogar & Eléctrico</button>
                        </nav>

                        <!-- Fila 2: Sub-filtros (pills) -->
                        <nav class="catalog-sub-filters filter-group" aria-label="Categorías">
                            <div class="filter-item active" data-category="all">Todos los productos</div>
                            <!-- Cocina -->
                            <div class="filter-item" data-category="air_fryer">Air Fryer</div>
                            <div class="filter-item" data-category="blender">Licuadoras</div>
                            <div class="filter-item" data-category="mixer">Batidoras</div>
                            <div class="filter-item" data-category="stove">Estufas</div>
                            <div class="filter-item" data-category="coffee_maker">Cafeteras</div>
                            <div class="filter-item" data-category="rice_cooker">Arroceras</div>
                            <div class="filter-item" data-category="oven">Hornos</div>
                            <div class="filter-item" data-category="lonchera">Loncheras</div>
                            <!-- Utensilios -->
                            <div class="filter-item" data-category="pressure_cooker">Ollas a Presión</div>
                            <div class="filter-item" data-category="caldero">Calderos</div>
                            <div class="filter-item" data-category="teapot">Teteras</div>
                            <div class="filter-item" data-category="iron">Planchas</div>
                            <div class="filter-item" data-category="toaster">Tostadoras</div>
                            <div class="filter-item" data-category="sandwich_maker">Sandwicheras</div>
                            <!-- Hogar & Eléctrico -->
                            <div class="filter-item" data-category="extension">Extensiones</div>
                            <div class="filter-item" data-category="power_strip">Regletas</div>
                            <div class="filter-item" data-category="tv_mount">Soportes TV</div>
                            <div class="filter-item" data-category="appliance">Electrodomésticos</div>
                        </nav>
                    </aside>"""

content = content.replace(OLD_SIDEBAR, NEW_SIDEBAR)

# ─── 4. Productos nuevos — cards ─────────────────────────────────────────────
WA = "https://wa.me/50769838322"
PLACEHOLDER = "media/icons/logo/logo.png"

def card(cat_dir, sku, data_cat, nombre, feats):
    sku_upper = sku.upper()
    feat_lines = "\n".join(f"                                        <li> {f}</li>" for f in feats)
    wa_text = nombre.replace(" ", "%20").replace('"', '%22')
    img = f"productos/{cat_dir}/{sku}/img/PRODUCTO_PRINCIPAL.webp"
    href = f"productos/{cat_dir}/{sku}/"
    return f"""                            <li class="product" data-category="{data_cat}">
                                <a href="{href}" class="product_image_wrapper">
                                    <img src="{img}"
                                        alt="{nombre}" class="product_img" loading="lazy">
                                </a>
                                <div class="product_content">
                                    <span class="product_sku">MOD: {sku_upper}</span>
                                    <h3 class="product_name"><a href="{href}">{nombre}</a></h3>
                                    <ul class="product_features">
{feat_lines}
                                    </ul>
                                    <div class="product_actions">
                                        <a href="{WA}?text=Hola, me interesa el producto {wa_text} MOD: {sku_upper}"
                                            class="product_cta" target="_blank" rel="noopener">
                                            Consultar Precio
                                        </a>
                                    </div>
                                </div>
                            </li>"""

PRODUCTS = [
    # Extensiones
    ("extensiones","hp-050","extension","Cable Extensión 1.8m",["1 Toma Polarizada","1.8 Metros","110V","Uso Interior"]),
    ("extensiones","hp-051","extension","Cable Extensión 3m",["1 Toma Polarizada","3 Metros","110V","Uso Interior"]),
    ("extensiones","hp-052","extension","Cable Extensión 4.5m",["1 Toma Polarizada","4.5 Metros","110V","Uso Interior"]),
    ("extensiones","hp-053","extension","Cable Extensión 6m",["1 Toma Polarizada","6 Metros","110V","Uso Interior"]),
    ("extensiones","hp-054","extension","Cable Extensión 7.5m",["1 Toma Polarizada","7.5 Metros","110V","Uso Interior"]),
    ("extensiones","hp-055","extension","Extensión Naranja 2.8m",["2 Conductores","2.8 Metros","Naranja","Alta Visibilidad"]),
    ("extensiones","hp-056","extension","Extensión Naranja 4.5m",["2 Conductores","4.5 Metros","Naranja","Alta Visibilidad"]),
    ("extensiones","hp-057","extension","Extensión Naranja 6m",["2 Conductores","6 Metros","Naranja","Alta Visibilidad"]),
    ("extensiones","hp-058","extension","Extensión Naranja 7.5m",["2 Conductores","7.5 Metros","Naranja","Alta Visibilidad"]),
    ("extensiones","hp-059","extension","Extensión Naranja 9m",["2 Conductores","9 Metros","Naranja","Alta Visibilidad"]),
    ("extensiones","hp-060","extension","Extensión Naranja 15m",["2 Conductores","15 Metros","Naranja","Alta Visibilidad"]),
    ("extensiones","hp-061","extension","Extensión Naranja 21m",["2 Conductores","21 Metros","Naranja","Alta Visibilidad"]),
    ("extensiones","hp-062","extension","Extensión Amarilla 3m",["3 Conductores","3 Metros","Amarilla","Uso Industrial"]),
    ("extensiones","hp-063","extension","Extensión Amarilla 5m",["3 Conductores","5 Metros","Amarilla","Uso Industrial"]),
    ("extensiones","hp-064","extension","Extensión Amarilla 8m",["3 Conductores","8 Metros","Amarilla","Uso Industrial"]),
    ("extensiones","hp-065","extension","Extensión Amarilla 10m",["3 Conductores","10 Metros","Amarilla","Uso Industrial"]),
    ("extensiones","hp-066","extension","Extensión Amarilla 15m",["3 Conductores","15 Metros","Amarilla","Uso Industrial"]),
    ("extensiones","hp-067","extension","Extensión Amarilla 20m",["3 Conductores","20 Metros","Amarilla","Uso Industrial"]),
    ("extensiones","hp-068","extension","Extensión Amarilla 25m",["3 Conductores","25 Metros","Amarilla","Uso Industrial"]),
    # Calderos
    ("calderos","hp-025","caldero","Caldero 20cm Tapa Aluminio",["20cm Diámetro","Tapa Aluminio","Uso Rudo","B2B Ideal"]),
    ("calderos","hp-026","caldero","Caldero 24cm Tapa Aluminio",["24cm Diámetro","Tapa Aluminio","Uso Rudo","B2B Ideal"]),
    ("calderos","hp-027","caldero","Caldero 26cm Tapa Aluminio",["26cm Diámetro","Tapa Aluminio","Uso Rudo","B2B Ideal"]),
    ("calderos","hp-028","caldero","Caldero 34cm Tapa Aluminio",["34cm Diámetro","Tapa Aluminio","Gran Capacidad","Catering"]),
    ("calderos","hp-029","caldero","Caldero 36cm Tapa Aluminio",["36cm Diámetro","Tapa Aluminio","Gran Capacidad","Catering"]),
    ("calderos","hp-030","caldero","Caldero 20cm Tapa Vidrio",["20cm Diámetro","Tapa Vidrio","Ver el Cocido","B2B Ideal"]),
    ("calderos","hp-031","caldero","Caldero 24cm Tapa Vidrio",["24cm Diámetro","Tapa Vidrio","Ver el Cocido","B2B Ideal"]),
    ("calderos","hp-032","caldero","Caldero 26cm Tapa Vidrio",["26cm Diámetro","Tapa Vidrio","Ver el Cocido","B2B Ideal"]),
    ("calderos","hp-033","caldero","Caldero 34cm Tapa Vidrio",["34cm Diámetro","Tapa Vidrio","Gran Capacidad","Catering"]),
    ("calderos","hp-034","caldero","Caldero 36cm Tapa Vidrio",["36cm Diámetro","Tapa Vidrio","Gran Capacidad","Catering"]),
    # Ollas a presión
    ("ollas","hp-035","pressure_cooker","Olla a Presión 4L Aluminio",["4 Litros","Aluminio","Válvula Seguridad","Uso Rudo"]),
    ("ollas","hp-036","pressure_cooker","Olla a Presión 5L Aluminio",["5 Litros","Aluminio","Válvula Seguridad","Uso Rudo"]),
    ("ollas","hp-037","pressure_cooker","Olla a Presión 7L Aluminio",["7 Litros","Aluminio","Válvula Seguridad","Gran Capacidad"]),
    ("ollas","hp-038","pressure_cooker","Olla a Presión 9L Aluminio",["9 Litros","Aluminio","Válvula Seguridad","Catering Ideal"]),
    ("ollas","hp-039","pressure_cooker","Olla a Presión 11L Aluminio",["11 Litros","Aluminio","Válvula Seguridad","Uso Industrial"]),
    # Soportes TV
    ("soportes-tv","hp-040","tv_mount","Soporte TV Fijo 66lb",["Capacidad 66lb","Montaje Fijo","VESA Universal","Fácil Inst."]),
    ("soportes-tv","hp-041","tv_mount","Soporte TV Fijo 77lb",["Capacidad 77lb","Montaje Fijo","VESA Universal","Heavy Duty"]),
    ("soportes-tv","hp-042","tv_mount","Soporte TV Inclinable 66lb",["Capacidad 66lb","Inclinable","VESA Universal","Anti-reflejo"]),
    ("soportes-tv","hp-043","tv_mount","Soporte TV Giratorio 66lb",["Capacidad 66lb","Gira 360°","VESA Universal","Pantalla Full"]),
    # Regletas
    ("regletas","hp-070","power_strip","Regleta Polarizada 6 Tomas",["6 Tomas","Polarizada","Prot. Sobrecarga","Uso Interior"]),
    ("regletas","hp-071","power_strip","Regleta Polarizada 5 Tomas",["5 Tomas","Polarizada","Prot. Sobrecarga","Compacta"]),
    ("regletas","hp-072","power_strip","Regleta 6 Tomas + USB",["6 Tomas","Puerto USB","Prot. Sobrecarga","Smart Hub"]),
    # Varios
    ('varios','hp-008','appliance','Abanico de Pedestal 18"',["3 en 1","18 Pulgadas","3 Velocidades","Oscilación Auto"]),
    ("varios","hp-013","appliance","Cafetera y Tetera 2 en 1",["4-8 Tazas","2 en 1","Dual Función","Práctico"]),
    ("varios","hp-014","appliance","Asador Eléctrico BBQ 1400W",["1400W","Parrilla BBQ","Antiadherente","Uso Interior"]),
    ("varios","hp-015","appliance","Exprimidor de Jugos 0.7L",["0.7L Cap.","Bajo Ruido","Fácil Limpieza","Cítricos"]),
    ("varios","hp-016","appliance","Exprimidor de Jugos 1L",["1L Cap.","Bajo Ruido","Fácil Limpieza","Gran Cap."]),
    ("varios","hp-019","appliance","Tetera Eléctrica Plegable",["3-4 Tazas","Plegable","Viaje","110V"]),
    ("varios","hp-020","appliance","Licuadora Portátil 380mL",["380mL","USB Recargable","Portátil","Smoothies"]),
    ("varios","hp-021","appliance","Batidora de Mano 7 Velocidades",["7 Velocidades","Mano","Accesorios incl.","Versátil"]),
    ("varios","hp-022","appliance","Procesador de Alimentos 950mL",["950mL","Manual","Sin Motor","Picado Rápido"]),
    ("varios","hp-023","appliance","Báscula Digital de Cocina",["Pantalla LCD","Tara","g/oz/lb","Precisión 1g"]),
]

new_cards = "\n".join(card(*p) for p in PRODUCTS)

# Insertar antes de cierre de </ul> del grid
INSERT_MARKER = "                        </ul>"
if INSERT_MARKER not in content:
    print("ERROR: marker no encontrado — revisar index.html")
    exit(1)

# Solo el primer cierre de </ul> (el del grid de productos)
content = content.replace(
    INSERT_MARKER,
    new_cards + "\n" + INSERT_MARKER,
    1  # solo primera ocurrencia
)

with open(HTML, "w", encoding="utf-8") as f:
    f.write(content)

print("index.html actualizado:")
print(f"  - Sidebar reemplazado (filtros 2 niveles)")
print(f"  - {len(PRODUCTS)} cards de producto agregados")
print(f"  - Nav 'Electrodomésticos' → 'Catálogo'")
print(f"  - Stat '59+' → '110+'")
