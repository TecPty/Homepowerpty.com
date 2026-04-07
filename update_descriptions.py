import os
import re

# ─────────────────────────────────────────────────────────────────────────────
# CATALOG DATA — exact specs from "EXCEL DE PRODUCTOS PARA MKT"
# Each entry: folder → { specs for table, subtitle, colors, usage_tip }
# ─────────────────────────────────────────────────────────────────────────────
PRODUCTS = {
    "air-fryer-4-5l": {
        "sku": "JD389",
        "nombre": "Air Fryer Digital 4.5L",
        "colores": "Negro",
        "potencia": "1580W",
        "voltaje": "110V / 60Hz",
        "capacidad": "4.5 Litros",
        "specs_extra": [
            ("Temperatura", "80°C – 200°C"),
            ("Tiempo máximo", "60 minutos"),
            ("Pantalla", "LED Digital Táctil"),
            ("Programas", "8 presets"),
            ("Revestimiento", "Antiadherente"),
            ("Garantía", "1 Año"),
        ],
        "subtitle": "Tecnología de circulación de aire caliente a 360° para cocinar sin aceite. Ideal para restaurantes, cafeterías y distribuidores que buscan el máximo rendimiento con el mínimo consumo energético.",
        "usos": "Ideal para freír, hornear, asar y gratinar. Sin aceite, resultados crujientes y saludables.",
    },
    "freidora-aire-blanca": {
        "sku": "OC-506",
        "nombre": "Air Fryer Blanco 3L",
        "colores": "Blanco / Negro",
        "potencia": "800W",
        "voltaje": "110V / 50Hz",
        "capacidad": "3 Litros",
        "specs_extra": [
            ("Temperatura", "Ajustable"),
            ("Temporizador", "30 minutos"),
            ("Revestimiento", "Antiadherente"),
            ("Garantía", "1 Año"),
        ],
        "subtitle": "Freidora de aire compacta en edición blanca. Diseño minimalista para cocinas modernas con la misma potencia de cocción saludable sin aceite.",
        "usos": "Papas fritas, pollo a la plancha, vegetales asados. Sin aceite, sin humo.",
    },
    "licuadora-3v-glass": {
        "sku": "MM-111",
        "nombre": "Licuadora de Vidrio 1.5L",
        "colores": "Negro / Gris",
        "potencia": "450W",
        "voltaje": "110V",
        "capacidad": "1.5 Litros",
        "specs_extra": [
            ("Jarra", "Vidrio templado"),
            ("Velocidades", "3 + Pulso"),
            ("Garantía", "1 Año"),
        ],
        "subtitle": "Licuadora de jarra de vidrio templado con motor de alto rendimiento. Apta para hielo, frutas duras y preparaciones profesionales.",
        "usos": "Smoothies, batidos, salsas, sopas frías. Jarra desmontable apta para lavavajillas.",
    },
    "licuadora-azul": {
        "sku": "MM-931",
        "nombre": "Licuadora Plástico 1.6L",
        "colores": "Negro / Rojo",
        "potencia": "300–400W",
        "voltaje": "110V / 60Hz",
        "capacidad": "1.6 Litros",
        "specs_extra": [
            ("Motor", "7020"),
            ("Garantía", "1 Año"),
        ],
        "subtitle": "Licuadora de diseño moderno con cuerpo en negro y rojo. Motor eficiente para uso doméstico y comercial intensivo.",
        "usos": "Batidos, jugos, salsas y trituración de hielo. Fácil limpieza y mantenimiento.",
    },
    "licuadora-chocolate": {
        "sku": "MM-933",
        "nombre": "Licuadora Plástico 1.6L",
        "colores": "Azul / Blanco",
        "potencia": "300–400W",
        "voltaje": "110V / 60Hz",
        "capacidad": "1.6 Litros",
        "specs_extra": [
            ("Motor", "7025"),
            ("Garantía", "1 Año"),
        ],
        "subtitle": "Licuadora de diseño moderno con cuerpo en azul y blanco. Motor eficiente para uso doméstico y comercial intensivo.",
        "usos": "Batidos, jugos, salsas y trituración de hielo. Fácil limpieza y mantenimiento.",
    },
    "estufa-2-quemadores-blanca": {
        "sku": "2020B",
        "nombre": "Estufita Eléctrica 2 Quemadores",
        "colores": "Blanco / Negro",
        "potencia": "2000W",
        "voltaje": "110V",
        "capacidad": "2 Quemadores",
        "specs_extra": [
            ("Tipo", "Placa eléctrica"),
            ("Controles", "2 perillas independientes"),
            ("Garantía", "1 Año"),
        ],
        "subtitle": "Estufita eléctrica de 2 quemadores para cocinas compactas, dormitorios con cocina y espacios de oficina. Potencia total de 2000W distribuida en 2 placas independientes.",
        "usos": "Hervir, saltear, cocinar a fuego lento. Ideal para espacios pequeños y cocinas secundarias.",
    },
    "estufa-2-quemadores-negra": {
        "sku": "2020B",
        "nombre": "Estufita Eléctrica 2 Quemadores",
        "colores": "Negro / Blanco",
        "potencia": "2000W",
        "voltaje": "110V",
        "capacidad": "2 Quemadores",
        "specs_extra": [
            ("Tipo", "Placa eléctrica"),
            ("Controles", "2 perillas independientes"),
            ("Garantía", "1 Año"),
        ],
        "subtitle": "Estufita eléctrica de 2 quemadores en color negro. Misma potencia de 2000W con diseño sofisticado para cocinas modernas.",
        "usos": "Hervir, saltear, cocinar a fuego lento. Ideal para espacios compactos.",
    },
    "estufa-electrica-doble": {
        "sku": "F-010E-1",
        "nombre": "Estufita Eléctrica 1 Quemador",
        "colores": "Blanco / Negro",
        "potencia": "1000W",
        "voltaje": "110V",
        "capacidad": "1 Quemador (Espiral)",
        "specs_extra": [
            ("Tipo", "Resistencia espiral de acero"),
            ("Material plato", "0.3mm Hierro"),
            ("Diámetro plato", "155mm"),
            ("Garantía", "1 Año"),
        ],
        "subtitle": "Estufita eléctrica de un quemador con resistencia espiral de acero inoxidable. Compacta y eficiente para uso individual o como equipo de apoyo en cocinas.",
        "usos": "Hervir agua, calentar alimentos, preparaciones simples. Portátil y de fácil almacenamiento.",
    },
    "estufa-gas-3-quemadores": {
        "sku": "3076K",
        "nombre": "Estufa a Gas Acero 3 Quemadores",
        "colores": "Acero Inoxidable / Negro",
        "potencia": "N/A (Gas LP)",
        "voltaje": "N/A",
        "capacidad": "3 Quemadores",
        "specs_extra": [
            ("Material", "Acero Inoxidable"),
            ("Quemador Central", "Hierro color plata"),
            ("Encendido", "Automático piezoeléctrico"),
            ("Tipo de Gas", "Gas LP"),
            ("Garantía", "1 Año"),
        ],
        "subtitle": "Estufa a gas de 3 quemadores en acero inoxidable. Quemadores de hierro de alta eficiencia con encendido automático para un máximo control de la llama.",
        "usos": "Cocción rápida, hervido, fritura y cocina profesional de alto volumen.",
    },
    "estufa-gas-2-quemadores": {
        "sku": "2050A",
        "nombre": "Estufa a Gas Acero 2 Quemadores",
        "colores": "Acero Inoxidable / Negro",
        "potencia": "N/A (Gas LP)",
        "voltaje": "N/A",
        "capacidad": "2 Quemadores",
        "specs_extra": [
            ("Material", "Acero Inoxidable S201"),
            ("Quemador", "Hierro fundido 90MM"),
            ("Encendido", "Automático piezoeléctrico"),
            ("Tipo de Gas", "Gas LP"),
            ("Garantía", "1 Año"),
        ],
        "subtitle": "Estufa a gas compacta de 2 quemadores con cuerpo de acero inoxidable y encendido automático. Diseño eficiente para cocinas pequeñas y espacios de trabajo.",
        "usos": "Cocción cotidiana, hervido y salteado. Encendido automático sin necesidad de fósforos.",
    },
    "cafetera-6-tazas": {
        "sku": "WJ-9008",
        "nombre": "Cafetera con Filtro 6 Tazas",
        "colores": "Negro",
        "potencia": "600W",
        "voltaje": "110V / 50-60Hz",
        "capacidad": "0.6 Litros (6 Tazas)",
        "specs_extra": [
            ("Filtro", "Fino permanente"),
            ("Jarra", "Vidrio"),
            ("Garantía", "1 Año"),
        ],
        "subtitle": "Cafetera de filtro fino de 6 tazas con jarra de vidrio. Extracción lenta que preserva el aroma y el sabor completo de cada grano.",
        "usos": "Café americano, cold brew caliente, infusiones. Placa calentadora para mantener el café a temperatura.",
    },
    "cafetera-12-tazas": {
        "sku": "WJ-9009",
        "nombre": "Cafetera con Filtro 12 Tazas",
        "colores": "Negro",
        "potencia": "800W",
        "voltaje": "110V / 50-60Hz",
        "capacidad": "1.2 Litros (12 Tazas)",
        "specs_extra": [
            ("Filtro", "Fino permanente"),
            ("Jarra", "Vidrio"),
            ("Garantía", "1 Año"),
        ],
        "subtitle": "Cafetera de filtro fino de 12 tazas. Capacidad ideal para oficinas, restaurantes y hogares con alta demanda de café.",
        "usos": "Café americano, café de oficina, servicios de catering. Jarra de vidrio con placa calentadora.",
    },
    "plancha-seco": {
        "sku": "R.91261",
        "nombre": "Plancha en Seco",
        "colores": "Blanco / Gris",
        "potencia": "1200W",
        "voltaje": "110V / 60Hz",
        "capacidad": "N/A",
        "specs_extra": [
            ("Suela", "Cerámica antiadherente"),
            ("Función", "Plancha en seco"),
            ("Garantía", "1 Año"),
        ],
        "subtitle": "Plancha en seco de suela cerámica de alta deslizabilidad. Distribución uniforme del calor para un planchado profesional sin esfuerzo.",
        "usos": "Ropa de algodón, lino, sintéticos. Control de temperatura ajustable para cada tipo de tela.",
    },
    "plancha-seco-premium": {
        "sku": "R.1808B",
        "nombre": "Plancha de Vapor Premium",
        "colores": "Blanco / Azul",
        "potencia": "1200W",
        "voltaje": "110V / 50-60Hz",
        "capacidad": "N/A",
        "specs_extra": [
            ("Función", "Vapor y seco"),
            ("Depósito", "Agua para vapor"),
            ("Garantía", "1 Año"),
        ],
        "subtitle": "Plancha premium con función vapor y seco. 1200W de potencia para un planchado profesional con golpe de vapor para las arrugas más difíciles.",
        "usos": "Planchado de camisas, vestidos, ropa delicada. Función vapor para tejidos gruesos.",
    },
    "plancha-vapor-premium": {
        "sku": "R.92003",
        "nombre": "Plancha en Seco 1000W",
        "colores": "Blanco / Morado",
        "potencia": "1000W",
        "voltaje": "110V / 60Hz",
        "capacidad": "N/A",
        "specs_extra": [
            ("Suela", "Cerámica antiadherente"),
            ("Función", "Plancha en seco"),
            ("Garantía", "1 Año"),
        ],
        "subtitle": "Plancha en seco compacta de 1000W con cerámica de alta performance. Ideal para uso diario y planchado rápido.",
        "usos": "Ropa cotidiana, uniformes, telas delicadas. Ligera y ergonómica.",
    },
    "tetera-1-8l": {
        "sku": "JR-A101",
        "nombre": "Tetera Eléctrica 1.8L",
        "colores": "Blanco / Negro",
        "potencia": "1500W",
        "voltaje": "110V",
        "capacidad": "1.8 Litros",
        "specs_extra": [
            ("Base", "Giratoria 360°"),
            ("Apagado", "Automático al hervir"),
            ("Garantía", "1 Año"),
        ],
        "subtitle": "Tetera eléctrica de 1.8L con apagado automático al hervir. Hervido ultrarrápido ideal para té, café instantáneo, sopas y preparaciones calientes.",
        "usos": "Hervir agua para té, café, sopas instantáneas, bebidas calientes. Base 360° desmontable.",
    },
    "tetera-premium": {
        "sku": "JR-LD8",
        "nombre": "Tetera Eléctrica 1.8L Premium",
        "colores": "Negro / Acero",
        "potencia": "1500W",
        "voltaje": "110V",
        "capacidad": "1.8 Litros",
        "specs_extra": [
            ("Base", "Giratoria 360°"),
            ("Apagado", "Automático al hervir"),
            ("Acabado", "Acero inoxidable"),
            ("Garantía", "1 Año"),
        ],
        "subtitle": "Tetera eléctrica premium con cuerpo de acero inoxidable y base giratoria. Diseño elegante para cocinas de alta gama.",
        "usos": "Hervir agua, preparar té, café y bebidas calientes. Indicador de nivel de agua visible.",
    },
    "sandwichera-clasica": {
        "sku": "SJ-22",
        "nombre": "Sandwichera Plástico",
        "colores": "Blanco / Gris",
        "potencia": "750W",
        "voltaje": "110V / 60Hz",
        "capacidad": "2 Sandwiches",
        "specs_extra": [
            ("Placas", "Antiadherentes"),
            ("Cierre", "Manual con seguro"),
            ("Garantía", "1 Año"),
        ],
        "subtitle": "Sandwichera clásica de plástico con placas antiadherentes para 2 sandwiches. Rápida, compacta y fácil de limpiar. Ideal para desayunos y meriendas.",
        "usos": "Sándwiches tostados, emparedados, paninis simples. Listo en menos de 3 minutos.",
    },
    "sandwichera-metal": {
        "sku": "SJ-24",
        "nombre": "Sandwichera Metal",
        "colores": "Acero / Negro",
        "potencia": "750W",
        "voltaje": "110V / 60Hz",
        "capacidad": "2 Sandwiches",
        "specs_extra": [
            ("Cuerpo", "Metal de alta resistencia"),
            ("Placas", "Antiadherentes"),
            ("Cierre", "Manual con seguro"),
            ("Garantía", "1 Año"),
        ],
        "subtitle": "Sandwichera de cuerpo metálico de última generación. Mayor durabilidad y retención del calor para un tostado perfecto y uniforme.",
        "usos": "Sandwiches, emparedados, tostadas. Placas antiadherentes de fácil limpieza.",
    },
    "sandwichera-premium": {
        "sku": "SJ-40",
        "nombre": "Panini Maker / Grill Plástico",
        "colores": "Blanco / Gris",
        "potencia": "750W",
        "voltaje": "110V / 60Hz",
        "capacidad": "2 Sandwiches / Parrilla",
        "specs_extra": [
            ("Modo", "Sandwichera + Parrilla abierta"),
            ("Placas", "Antiadherentes"),
            ("Apertura", "180° para usar como grill"),
            ("Garantía", "1 Año"),
        ],
        "subtitle": "2 en 1: Sandwichera y parrilla abierta con apertura de 180°. Versátil para paninis, hamburguesas, filetes y vegetales a la plancha.",
        "usos": "Paninis, hamburguesas, pechugas, vegetales. Apertura total para usar como parrilla.",
    },
    "hornito-23l": {
        "sku": "PN-09",
        "nombre": "Hornito Eléctrico 9L",
        "colores": "Negro",
        "potencia": "800W",
        "voltaje": "110V / 60Hz",
        "capacidad": "9 Litros",
        "specs_extra": [
            ("Temperatura", "7 niveles de control"),
            ("Temporizador", "0–60 minutos"),
            ("Elemento calefactor", "Acero inoxidable"),
            ("Incluye", "Bandeja y parrilla"),
            ("Garantía", "1 Año"),
        ],
        "subtitle": "Hornito eléctrico de 9 litros con 7 niveles de temperatura y temporizador de 60 minutos. Compacto pero potente para pizzas, panes, carnes y recetas de horno.",
        "usos": "Pizza, pan, pollo al horno, pasteles. Temporizador con alarma sonora al finalizar.",
    },
    "arrocera-1-5l": {
        "sku": "HT-15A",
        "nombre": "Arrocera 1.5L con Vaporera",
        "colores": "Blanco",
        "potencia": "500W",
        "voltaje": "110V / 60Hz",
        "capacidad": "1.5 Litros",
        "specs_extra": [
            ("Interior", "Antiadherente"),
            ("Vaporizador", "Incluido"),
            ("Función", "Cocción + Mantener caliente"),
            ("Garantía", "1 Año"),
        ],
        "subtitle": "Arrocera eléctrica de 1.5L con interior antiadherente y vaporizador incluido. Cocción automática perfecta y función de mantener caliente para servir en cualquier momento.",
        "usos": "Arroz blanco, arroz integral, quinoa, frijoles, vegetales al vapor.",
    },
    "arrocera-vaporera-2-2l": {
        "sku": "HT-22A",
        "nombre": "Arrocera 2.2L con Vaporera",
        "colores": "Blanco",
        "potencia": "900W",
        "voltaje": "110V / 60Hz",
        "capacidad": "2.2 Litros",
        "specs_extra": [
            ("Interior", "Antiadherente"),
            ("Vaporizador", "Incluido"),
            ("Función", "Cocción + Mantener caliente"),
            ("Garantía", "1 Año"),
        ],
        "subtitle": "Arrocera de mayor capacidad (2.2L) con vaporizador incluido. Ideal para familias, restaurantes pequeños y catering con alta demanda de porciones.",
        "usos": "Arroz para grupos, vegetales al vapor, pollo al vapor. Interior antiadherente fácil de lavar.",
    },
    "olla-presion-5l": {
        "sku": "CK-02-22",
        "nombre": "Olla de Presión Aluminio 5.5L",
        "colores": "Aluminio plateado / Negro",
        "potencia": "N/A (Estufa)",
        "voltaje": "N/A",
        "capacidad": "5.5 Litros — 22cm",
        "specs_extra": [
            ("Material", "Aluminio de alta resistencia"),
            ("Válvulas de seguridad", "Sistema múltiple"),
            ("Asas", "Bakelita resistente al calor"),
            ("Compatible con", "Gas y eléctrica"),
            ("Garantía", "1 Año"),
        ],
        "subtitle": "Olla de presión de aluminio de 5.5 litros con sistema de válvulas de seguridad múltiple. Cocción 3x más rápida que los métodos tradicionales.",
        "usos": "Guisos, frijoles, sopas, carnes duras, arroz. Compatible con estufas de gas y eléctricas.",
    },
    "olla-presion-7l": {
        "sku": "CK-02-24",
        "nombre": "Olla de Presión Aluminio 7L",
        "colores": "Aluminio plateado / Negro",
        "potencia": "N/A (Estufa)",
        "voltaje": "N/A",
        "capacidad": "7 Litros — 24cm",
        "specs_extra": [
            ("Material", "Aluminio de alta resistencia"),
            ("Válvulas de seguridad", "Sistema múltiple"),
            ("Asas", "Bakelita resistente al calor"),
            ("Compatible con", "Gas y eléctrica"),
            ("Garantía", "1 Año"),
        ],
        "subtitle": "Olla de presión de aluminio de 7 litros para preparaciones de mayor volumen. Ideal para negocios de comida, comedores y cocinas de alto flujo.",
        "usos": "Guisos en cantidad, sopas, frijoles, tamales, carnes. Capacidad profesional para grandes porciones.",
    },
    "tostadora-2-rebanadas": {
        "sku": "HP-017",
        "nombre": "Tostadora Eléctrica 2 Rebanadas",
        "colores": "Blanco",
        "potencia": "750W",
        "voltaje": "110V",
        "capacidad": "2 Rebanadas",
        "specs_extra": [
            ("Niveles de tostado", "7"),
            ("Funciones", "Tostar / Descongelar / Recalentar"),
            ("Bandeja", "Recoge migas desmontable"),
            ("Garantía", "1 Año"),
        ],
        "subtitle": "Tostadora eléctrica de 2 ranuras anchas con 7 niveles de tostado y funciones de descongelado y recalentado. Perfecta para desayunos rápidos y servicios de cafetería.",
        "usos": "Pan de molde, bagels, waffles, pan artesanal. Bandeja de migas removible para fácil limpieza.",
    },
}


def build_specs_table(data):
    """Build a complete <tbody> for the specs table from product data."""
    rows = ""
    rows += f"<tr><td>Modelo</td><td>MOD: {data['sku']}</td></tr>\n"
    if data.get("colores") and data["colores"] != "N/A":
        rows += f"<tr><td>Colores</td><td>{data['colores']}</td></tr>\n"
    if data.get("potencia") and data["potencia"] != "N/A (Estufa)" and data["potencia"] != "N/A (Gas LP)":
        rows += f"<tr><td>Potencia</td><td>{data['potencia']}</td></tr>\n"
    else:
        rows += f"<tr><td>Potencia</td><td>{data.get('potencia', 'N/A')}</td></tr>\n"
    if data.get("voltaje") and data["voltaje"] not in ("N/A", ""):
        rows += f"<tr><td>Voltaje</td><td>{data['voltaje']}</td></tr>\n"
    if data.get("capacidad"):
        rows += f"<tr><td>Capacidad</td><td>{data['capacidad']}</td></tr>\n"
    for label, value in data.get("specs_extra", []):
        rows += f"<tr><td>{label}</td><td>{value}</td></tr>\n"
    return rows


def update_product_page(folder_name, data):
    base = r"c:\Users\HP 15\Homepowerpty.com\productos"
    filepath = os.path.join(base, folder_name, "index.html")

    if not os.path.exists(filepath):
        print(f"  SKIP (no existe): {folder_name}")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # 1) Replace the full <tbody> of the specs table
    new_tbody = build_specs_table(data)
    content = re.sub(
        r"<tbody>.*?</tbody>",
        f"<tbody>\n{new_tbody}</tbody>",
        content,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # 2) Update the hero subtitle if it exists
    if data.get("subtitle"):
        content = re.sub(
            r'<p class="product-hero-subtitle">.*?</p>',
            f'<p class="product-hero-subtitle">{data["subtitle"]}</p>',
            content,
            flags=re.DOTALL,
        )

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✓ {folder_name}")
    else:
        print(f"  ~ sin cambios: {folder_name}")


def run():
    print("Actualizando fichas de producto con datos exactos del catálogo...\n")
    for folder, data in PRODUCTS.items():
        update_product_page(folder, data)
    print("\nListo.")


if __name__ == "__main__":
    run()
