"""
Genera los 55 directorios de productos faltantes con un stub index.html cada uno.
Cada stub usa el template base del PDP (product-v2.css) con datos reales del Excel.
"""
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WA = "https://wa.me/50769838322"

# ─── Definición de los 55 productos faltantes ────────────────────────────────
# (categoria_dir, sku_dir, data_category, nombre_display, features[4])
PRODUCTS = [
    # ── Extensiones ──────────────────────────────────────────────────────────
    ("extensiones", "hp-050", "extension", "Cable Extensión 1.8m",
     ["1 Toma Polarizada", "1.8 Metros", "110V", "Uso Interior"]),
    ("extensiones", "hp-051", "extension", "Cable Extensión 3m",
     ["1 Toma Polarizada", "3 Metros", "110V", "Uso Interior"]),
    ("extensiones", "hp-052", "extension", "Cable Extensión 4.5m",
     ["1 Toma Polarizada", "4.5 Metros", "110V", "Uso Interior"]),
    ("extensiones", "hp-053", "extension", "Cable Extensión 6m",
     ["1 Toma Polarizada", "6 Metros", "110V", "Uso Interior"]),
    ("extensiones", "hp-054", "extension", "Cable Extensión 7.5m",
     ["1 Toma Polarizada", "7.5 Metros", "110V", "Uso Interior"]),
    ("extensiones", "hp-055", "extension", "Extensión Naranja 2.8m",
     ["2 Conductores", "2.8 Metros", "Naranja", "Alta Visibilidad"]),
    ("extensiones", "hp-056", "extension", "Extensión Naranja 4.5m",
     ["2 Conductores", "4.5 Metros", "Naranja", "Alta Visibilidad"]),
    ("extensiones", "hp-057", "extension", "Extensión Naranja 6m",
     ["2 Conductores", "6 Metros", "Naranja", "Alta Visibilidad"]),
    ("extensiones", "hp-058", "extension", "Extensión Naranja 7.5m",
     ["2 Conductores", "7.5 Metros", "Naranja", "Alta Visibilidad"]),
    ("extensiones", "hp-059", "extension", "Extensión Naranja 9m",
     ["2 Conductores", "9 Metros", "Naranja", "Alta Visibilidad"]),
    ("extensiones", "hp-060", "extension", "Extensión Naranja 15m",
     ["2 Conductores", "15 Metros", "Naranja", "Alta Visibilidad"]),
    ("extensiones", "hp-061", "extension", "Extensión Naranja 21m",
     ["2 Conductores", "21 Metros", "Naranja", "Alta Visibilidad"]),
    ("extensiones", "hp-062", "extension", "Extensión Amarilla 3m",
     ["3 Conductores", "3 Metros", "Amarilla", "Uso Industrial"]),
    ("extensiones", "hp-063", "extension", "Extensión Amarilla 5m",
     ["3 Conductores", "5 Metros", "Amarilla", "Uso Industrial"]),
    ("extensiones", "hp-064", "extension", "Extensión Amarilla 8m",
     ["3 Conductores", "8 Metros", "Amarilla", "Uso Industrial"]),
    ("extensiones", "hp-065", "extension", "Extensión Amarilla 10m",
     ["3 Conductores", "10 Metros", "Amarilla", "Uso Industrial"]),
    ("extensiones", "hp-066", "extension", "Extensión Amarilla 15m",
     ["3 Conductores", "15 Metros", "Amarilla", "Uso Industrial"]),
    ("extensiones", "hp-067", "extension", "Extensión Amarilla 20m",
     ["3 Conductores", "20 Metros", "Amarilla", "Uso Industrial"]),
    ("extensiones", "hp-068", "extension", "Extensión Amarilla 25m",
     ["3 Conductores", "25 Metros", "Amarilla", "Uso Industrial"]),
    # ── Calderos ─────────────────────────────────────────────────────────────
    ("calderos", "hp-025", "caldero", "Caldero 20cm Tapa Aluminio",
     ["20cm Diámetro", "Tapa Aluminio", "Uso Rudo", "B2B Ideal"]),
    ("calderos", "hp-026", "caldero", "Caldero 24cm Tapa Aluminio",
     ["24cm Diámetro", "Tapa Aluminio", "Uso Rudo", "B2B Ideal"]),
    ("calderos", "hp-027", "caldero", "Caldero 26cm Tapa Aluminio",
     ["26cm Diámetro", "Tapa Aluminio", "Uso Rudo", "B2B Ideal"]),
    ("calderos", "hp-028", "caldero", "Caldero 34cm Tapa Aluminio",
     ["34cm Diámetro", "Tapa Aluminio", "Gran Capacidad", "Catering"]),
    ("calderos", "hp-029", "caldero", "Caldero 36cm Tapa Aluminio",
     ["36cm Diámetro", "Tapa Aluminio", "Gran Capacidad", "Catering"]),
    ("calderos", "hp-030", "caldero", "Caldero 20cm Tapa Vidrio",
     ["20cm Diámetro", "Tapa Vidrio", "Ver el Cocido", "B2B Ideal"]),
    ("calderos", "hp-031", "caldero", "Caldero 24cm Tapa Vidrio",
     ["24cm Diámetro", "Tapa Vidrio", "Ver el Cocido", "B2B Ideal"]),
    ("calderos", "hp-032", "caldero", "Caldero 26cm Tapa Vidrio",
     ["26cm Diámetro", "Tapa Vidrio", "Ver el Cocido", "B2B Ideal"]),
    ("calderos", "hp-033", "caldero", "Caldero 34cm Tapa Vidrio",
     ["34cm Diámetro", "Tapa Vidrio", "Gran Capacidad", "Catering"]),
    ("calderos", "hp-034", "caldero", "Caldero 36cm Tapa Vidrio",
     ["36cm Diámetro", "Tapa Vidrio", "Gran Capacidad", "Catering"]),
    # ── Ollas a presión aluminio (van en /ollas/) ────────────────────────────
    ("ollas", "hp-035", "pressure_cooker", "Olla a Presión 4L Aluminio",
     ["4 Litros", "Aluminio", "Válvula Seguridad", "Uso Rudo"]),
    ("ollas", "hp-036", "pressure_cooker", "Olla a Presión 5L Aluminio",
     ["5 Litros", "Aluminio", "Válvula Seguridad", "Uso Rudo"]),
    ("ollas", "hp-037", "pressure_cooker", "Olla a Presión 7L Aluminio",
     ["7 Litros", "Aluminio", "Válvula Seguridad", "Gran Capacidad"]),
    ("ollas", "hp-038", "pressure_cooker", "Olla a Presión 9L Aluminio",
     ["9 Litros", "Aluminio", "Válvula Seguridad", "Catering Ideal"]),
    ("ollas", "hp-039", "pressure_cooker", "Olla a Presión 11L Aluminio",
     ["11 Litros", "Aluminio", "Válvula Seguridad", "Uso Industrial"]),
    # ── Soportes TV ─────────────────────────────────────────────────────────
    ("soportes-tv", "hp-040", "tv_mount", "Soporte TV Fijo 66lb",
     ["Capacidad 66lb", "Montaje Fijo", "VESA Universal", "Fácil Inst."]),
    ("soportes-tv", "hp-041", "tv_mount", "Soporte TV Fijo 77lb",
     ["Capacidad 77lb", "Montaje Fijo", "VESA Universal", "Heavy Duty"]),
    ("soportes-tv", "hp-042", "tv_mount", "Soporte TV Inclinable 66lb",
     ["Capacidad 66lb", "Inclinable", "VESA Universal", "Anti-reflejo"]),
    ("soportes-tv", "hp-043", "tv_mount", "Soporte TV Giratorio 66lb",
     ["Capacidad 66lb", "Gira 360°", "VESA Universal", "Pantalla Full"]),
    # ── Regletas ─────────────────────────────────────────────────────────────
    ("regletas", "hp-070", "power_strip", "Regleta Polarizada 6 Tomas",
     ["6 Tomas", "Polarizada", "Protección Sobrecarga", "Uso Interior"]),
    ("regletas", "hp-071", "power_strip", "Regleta Polarizada 5 Tomas",
     ["5 Tomas", "Polarizada", "Protección Sobrecarga", "Compacta"]),
    ("regletas", "hp-072", "power_strip", "Regleta 6 Tomas + USB",
     ["6 Tomas", "Puerto USB", "Protección Sobrecarga", "Smart Hub"]),
    # ── Varios ───────────────────────────────────────────────────────────────
    ("varios", "hp-008", "appliance", "Abanico de Pedestal 18\"",
     ["3 en 1", "18 Pulgadas", "3 Velocidades", "Oscilación Auto"]),
    ("varios", "hp-013", "appliance", "Cafetera y Tetera 2 en 1",
     ["4-8 Tazas", "2 en 1", "Dual Función", "Práctico"]),
    ("varios", "hp-014", "appliance", "Asador Eléctrico BBQ 1400W",
     ["1400W", "Parrilla BBQ", "Antiadherente", "Uso Interior"]),
    ("varios", "hp-015", "appliance", "Exprimidor de Jugos 0.7L",
     ["0.7L Cap.", "Bajo Ruido", "Fácil Limpieza", "Cítricos"]),
    ("varios", "hp-016", "appliance", "Exprimidor de Jugos 1L",
     ["1L Cap.", "Bajo Ruido", "Fácil Limpieza", "Gran Cap."]),
    ("varios", "hp-019", "appliance", "Tetera Eléctrica Plegable",
     ["3-4 Tazas", "Plegable", "Viaje", "110V"]),
    ("varios", "hp-020", "appliance", "Licuadora Portátil 380mL",
     ["380mL", "USB Recargable", "Portátil", "Smoothies"]),
    ("varios", "hp-021", "appliance", "Batidora de Mano 7 Velocidades",
     ["7 Velocidades", "Mano", "Accesorios incl.", "Versátil"]),
    ("varios", "hp-022", "appliance", "Procesador de Alimentos 950mL",
     ["950mL", "Manual", "Sin Motor", "Picado Rápido"]),
    ("varios", "hp-023", "appliance", "Báscula Digital de Cocina",
     ["Pantalla LCD", "Tara", "g/oz/lb", "Precisión 1g"]),
]

# ─── Template HTML ────────────────────────────────────────────────────────────
def make_stub(sku_upper, nombre, features, wa_url):
    feats = "".join(f"                        <li>{f}</li>\n" for f in features)
    wa_text = nombre.replace(" ", "%20")
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{nombre} MOD: {sku_upper} | Home Power PTY</title>
    <meta name="description" content="{nombre} — Consulta disponibilidad y precios mayoristas en Home Power PTY, Panamá.">
    <link rel="stylesheet" href="../../styles/luxury.css">
    <link rel="stylesheet" href="../../styles/product-v2.css">
</head>
<body>

    <header class="luxury-header product-page">
    </header>

    <main class="main">
        <section class="pdp-section">
            <div class="container pdp-container">

                <div class="pdp-breadcrumb">
                    <nav>
                        <a href="../../">Inicio</a>
                        <span>/</span>
                        <a href="../../#catalogo">Catálogo</a>
                        <span>/</span>
                        <span>{nombre}</span>
                    </nav>
                </div>

                <div class="pdp-layout">
                    <div class="pdp-gallery">
                        <div class="pdp-main-img-wrapper">
                            <img src="./img/PRODUCTO_PRINCIPAL.webp"
                                 alt="{nombre}"
                                 class="pdp-main-img" id="mainImg">
                        </div>
                        <div class="pdp-thumbs" id="thumbsContainer">
                            <button class="pdp-thumb active"
                                    onclick="pdpSetImage('./img/PRODUCTO_PRINCIPAL.webp', this)">
                                <img src="./img/PRODUCTO_PRINCIPAL.webp" alt="Vista principal">
                            </button>
                        </div>
                    </div>

                    <div class="pdp-info">
                        <span class="pdp-sku">MOD: {sku_upper}</span>
                        <h1 class="pdp-name">{nombre}</h1>

                        <ul class="pdp-spec-pills">
{feats}                        </ul>

                        <div class="pdp-cta-group">
                            <a href="{wa_url}?text=Hola,%20me%20interesa%20el%20producto%20{wa_text}%20MOD:%20{sku_upper}"
                               class="pdp-cta-whatsapp" target="_blank" rel="noopener">
                                <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.123.555 4.116 1.527 5.842L0 24l6.335-1.652A11.954 11.954 0 0 0 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.818a9.818 9.818 0 0 1-5.013-1.376l-.36-.214-3.727.977.992-3.626-.235-.373A9.818 9.818 0 1 1 12 21.818z"/></svg>
                                Consultar Precio
                            </a>
                        </div>
                    </div>
                </div>

            </div>
        </section>
    </main>

    <script src="../../scripts/gold-breeze.js"></script>
</body>
</html>
"""

# ─── Ejecución ────────────────────────────────────────────────────────────────
created = 0
skipped = 0

for cat, sku, data_cat, nombre, features in PRODUCTS:
    # Rutas relativas para categorías que no están en /productos/
    if cat in ("extensiones", "calderos", "soportes-tv", "regletas", "varios"):
        img_rel = "../../styles/"
        css_depth = "../../"
    else:
        css_depth = "../../"

    sku_upper = sku.upper()
    dir_path = os.path.join(BASE, "productos", cat, sku)
    img_dir  = os.path.join(dir_path, "img")
    html_path = os.path.join(dir_path, "index.html")

    os.makedirs(img_dir, exist_ok=True)

    if os.path.exists(html_path):
        print(f"  SKIP  {cat}/{sku}")
        skipped += 1
        continue

    content = make_stub(sku_upper, nombre, features, WA)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  OK    {cat}/{sku}  —  {nombre}")
    created += 1

print(f"\nDone: {created} creados, {skipped} ya existian.")
