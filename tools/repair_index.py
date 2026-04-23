"""
Repair index.html:
1. Remove the accidentally inserted products in the showcase section.
2. Ensure the catalog sidebar is correct.
3. Insert the 51 products correctly into the featured-products-grid.
"""
import os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(BASE, "index.html")

with open(HTML, encoding="utf-8") as f:
    content = f.read()

# 1. Eliminar la inserción errónea (empieza con HP-050)
# Buscamos el bloque que empieza con la primera card corrupta
corrupt_start = '<li class="product" data-category="extension">\n                                <a href="productos/extensiones/hp-050/"'
if corrupt_start in content:
    print("Encontrada inserción corrupta. Limpiando...")
    # Buscamos desde el inicio de la corrupción hasta el final de la última card agregada (HP-023)
    # El script anterior agregó 51 productos. El último es HP-023.
    last_sku = "HP-023"
    # Buscamos el final de la card de HP-023
    end_pattern = r'<li class="product" data-category="appliance">.*?MOD: HP-023.*?</a>\s+</div>\s+</div>\s+</li>'
    match = re.search(end_pattern, content, re.DOTALL)
    if match:
        full_corrupt_block = content[content.find(corrupt_start) : match.end()]
        content = content.replace(full_corrupt_block, "")
        print("Bloque corrupto eliminado.")
    else:
        print("No se pudo encontrar el final del bloque corrupto con MOD: HP-023")

# 2. Re-insertar productos en el lugar correcto
# El lugar correcto es dentro de <ul class="featured-products-grid">
# Buscaremos el cierre de esta lista específicamente en la sección de catálogo.
# La sección de catálogo ahora tiene el id="catalogo" y la clase "featured-products-section".

# Definimos las cards (re-uso la lógica del script anterior)
WA = "https://wa.me/50769838322"
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
    ("ollas","hp-035","pressure_cooker","Olla a Presión 4L Aluminio",["4 Litros","Aluminio","Válvula Seguridad","Uso Rudo"]),
    ("ollas","hp-036","pressure_cooker","Olla a Presión 5L Aluminio",["5 Litros","Aluminio","Válvula Seguridad","Uso Rudo"]),
    ("ollas","hp-037","pressure_cooker","Olla a Presión 7L Aluminio",["7 Litros","Aluminio","Válvula Seguridad","Gran Capacidad"]),
    ("ollas","hp-038","pressure_cooker","Olla a Presión 9L Aluminio",["9 Litros","Aluminio","Válvula Seguridad","Catering Ideal"]),
    ("ollas","hp-039","pressure_cooker","Olla a Presión 11L Aluminio",["11 Litros","Aluminio","Válvula Seguridad","Uso Industrial"]),
    ("soportes-tv","hp-040","tv_mount","Soporte TV Fijo 66lb",["Capacidad 66lb","Montaje Fijo","VESA Universal","Fácil Inst."]),
    ("soportes-tv","hp-041","tv_mount","Soporte TV Fijo 77lb",["Capacidad 77lb","Montaje Fijo","VESA Universal","Heavy Duty"]),
    ("soportes-tv","hp-042","tv_mount","Soporte TV Inclinable 66lb",["Capacidad 66lb","Inclinable","VESA Universal","Anti-reflejo"]),
    ("soportes-tv","hp-043","tv_mount","Soporte TV Giratorio 66lb",["Capacidad 66lb","Gira 360°","VESA Universal","Pantalla Full"]),
    ("regletas","hp-070","power_strip","Regleta Polarizada 6 Tomas",["6 Tomas","Polarizada","Prot. Sobrecarga","Uso Interior"]),
    ("regletas","hp-071","power_strip","Regleta Polarizada 5 Tomas",["5 Tomas","Polarizada","Prot. Sobrecarga","Compacta"]),
    ("regletas","hp-072","power_strip","Regleta 6 Tomas + USB",["6 Tomas","Puerto USB","Prot. Sobrecarga","Smart Hub"]),
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

# Buscamos la etiqueta de apertura de la grid después de la sección catalogo
# <section class="featured-products-section" id="catalogo">
# ...
# <ul class="featured-products-grid">
grid_marker = '<ul class="featured-products-grid">'
catalog_section_marker = 'id="catalogo"'

catalog_start = content.find(catalog_section_marker)
if catalog_start != -1:
    grid_start = content.find(grid_marker, catalog_start)
    if grid_start != -1:
        insertion_point = grid_start + len(grid_marker)
        content = content[:insertion_point] + "\n" + new_cards + content[insertion_point:]
        print("Productos insertados correctamente en la grid del catálogo.")
    else:
        print("Error: No se encontró la grid dentro de la sección de catálogo.")
else:
    print("Error: No se encontró la sección de catálogo.")

with open(HTML, "w", encoding="utf-8") as f:
    f.write(content)

print("index.html REPARADO.")
