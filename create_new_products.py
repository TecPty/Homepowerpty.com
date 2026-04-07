import os, re

BASE = r"c:\Users\HP 15\Homepowerpty.com"
TEMPLATE = r"c:\Users\HP 15\Homepowerpty.com\productos\air-fryer-4-5l\index.html"

NEW_PRODUCTS = [
    # folder, sku, nombre, desc, potencia, voltaje, capacidad, colores, cod_wa, badge
    ("air-fryer-3l", "AF3201", "Air Fryer 3L", "Freidora de aire compacta de 3 litros con tecnología de circulación de calor 360°. Sin aceite, resultados crujientes en menos tiempo.", "800W", "110V / 50Hz", "3 Litros", "Blanco / Negro", "732129008635", "NUEVO"),
    ("licuadora-vb999", "VB-999", "Licuadora Plástico 2000W", "Licuadora de alta potencia con 2000W y jarra plástica de gran capacidad. Disponible en 4 colores: rojo, gris, negro y verde.", "2000W", "110V", "Gran capacidad", "Rojo / Gris / Negro / Verde", "732129008895", "MÁS POTENCIA"),
    ("batidora-pedestal", "HP-024", "Batidora Eléctrica de Pedestal", "Batidora de pedestal para mezclas profesionales. Ideal para repostería, panadería y preparaciones de alto volumen en negocios gastronómicos.", "N/A", "110V", "Bowl incluido", "Blanco", "732129008949", "PREMIUM"),
    ("batidora-mano", "HP-044", "Batidora Eléctrica de Mano", "Batidora de mano liviana y versátil para mezclar, batir y montar cremas. Perfecta para uso doméstico y profesional ligero.", "N/A", "110V", "Portátil", "Blanco", "694943899199", "NUEVO"),
    ("batidora-mano-metal", "HP-045", "Batidora de Mano de Metal", "Batidora de mano con cuerpo metálico de alta durabilidad. Diseño premium para uso intensivo en cocinas profesionales.", "N/A", "110V", "Portátil", "Acero / Negro", "694943899205", "PREMIUM"),
    ("estufa-electrica-1-quemador", "1010A", "Estufita Eléctrica 1 Quemador", "Estufita eléctrica compacta de 1 quemador. Material: hierro 0.3mm, plato de 155mm. Ideal como equipo de apoyo o cocina individual.", "1000W", "110V", "1 Quemador (155mm)", "Blanco / Negro", "732129008581", "COMPACTA"),
    ("estufa-electrica-1q-premium", "F-010E-1", "Estufita Eléctrica 1 Quemador Premium", "Estufita eléctrica de 1 quemador con materiales premium. Compacta, portátil y eficiente para espacios reducidos.", "1000W", "110V", "1 Quemador", "Blanco / Negro", "732129008901", "NUEVO"),
    ("estufa-electrica-2q-negra", "2020A", "Estufita Eléctrica 2 Quemadores", "Estufita eléctrica de 2 quemadores. Material: 0.35mm hierro, platos de 155mm. Potencia dividida para máxima versatilidad.", "2000W", "110V", "2 Quemadores (155mm)", "Blanco / Negro", "732129008598", "NUEVO"),
    ("estufa-gas-3q-v2", "3081K", "Estufa Gas Acero 3 Quemadores", "Segunda variante de la estufa a gas de 3 quemadores con acero inoxidable y quemadores de hierro color plata con encendido automático.", "Gas LP", "N/A", "3 Quemadores", "Acero Inoxidable", "732129008673", "NUEVO"),
    ("estufa-gas-2q-v2", "3080", "Estufa Gas Acero 2 Quemadores", "Estufa a gas de 2 quemadores con quemadores de hierro fundido 90MM y encendido automático. Cuerpo de acero inoxidable.", "Gas LP", "N/A", "2 Quemadores", "Acero Inoxidable", "732129008666", "NUEVO"),
    ("estufa-gas-4q-horno", "HP-073", "Estufa Gas 4 Quemadores + Horno", "Estufa a gas de 4 quemadores con horno integrado. La solución completa para cocinas profesionales y negocios gastronómicos.", "Gas LP", "N/A", "4 Quemadores + Horno", "Acero Inoxidable", "694943899489", "PREMIUM"),
    ("cafetera-12t-cm02", "CM02", "Cafetera 12 Tazas", "Cafetera eléctrica de 12 tazas con capacidad de 1.2 litros. 900W de potencia para un café listo en minutos.", "900W", "110V", "1.2 Litros (12 Tazas)", "Negro", "732129008932", "NUEVO"),
    ("cafetera-6t-v2", "WJ-9001", "Cafetera con Filtro 6 Tazas", "Cafetera de filtro fino con capacidad de 0.625 litros. Extracción lenta para un café aromático y de sabor completo.", "600W", "110V / 50-60Hz", "0.625 Litros (6 Tazas)", "Negro", "732129008680", "NUEVO"),
    ("cafetera-12t-v2", "WJ-9002", "Cafetera con Filtro 12 Tazas", "Cafetera de filtro fino de 12 tazas con capacidad de 1.25 litros. Ideal para oficinas y espacios de trabajo.", "800W", "110V / 50-60Hz", "1.25 Litros (12 Tazas)", "Negro", "732129008697", "NUEVO"),
    ("cafetera-7-5-tazas", "WJ-9011", "Cafetera con Filtro 7.5 Tazas", "Cafetera de filtro fino de 7.5 tazas. Capacidad intermedia perfecta para reuniones pequeñas y desayunos de equipo.", "600W", "110V / 50-60Hz", "0.625 Litros (7.5 Tazas)", "Negro", "732129008703", "NUEVO"),
    ("cafetera-percoladora-30t", "HP-046", "Cafetera Percoladora 30 Tazas", "Cafetera percoladora de gran capacidad para 30 tazas. Ideal para eventos, oficinas y servicios de catering.", "N/A", "110V", "30 Tazas", "Acero Inoxidable", "694943899212", "B2B"),
    ("cafetera-percoladora-40t", "HP-047", "Cafetera Percoladora 40 Tazas", "Cafetera percoladora para 40 tazas. Capacidad profesional para eventos medianos y servicios de café corporativo.", "N/A", "110V", "40 Tazas", "Acero Inoxidable", "694943899229", "B2B"),
    ("cafetera-percoladora-50t", "HP-048", "Cafetera Percoladora 50 Tazas", "Cafetera percoladora industrial de 50 tazas para eventos, hoteles y servicios de alimentación masiva.", "N/A", "110V", "50 Tazas", "Acero Inoxidable", "694943899236", "B2B"),
    ("cafetera-percoladora-100t", "HP-049", "Cafetera Percoladora 100 Tazas", "La cafetera percoladora de mayor capacidad: 100 tazas. Para grandes eventos, hoteles, auditorios y servicios masivos.", "N/A", "110V", "100 Tazas", "Acero Inoxidable", "694943899243", "B2B PREMIUM"),
    ("plancha-vapor-hp012", "HP-012", "Plancha de Vapor 1400W", "Plancha de vapor de 1400W con depósito de 170ml. Vapor continuo para eliminar arrugas en cualquier tipo de tela.", "1400W", "110V", "Depósito 170ml", "Blanco / Azul", "732129008840", "NUEVO"),
    ("plancha-vapor-r91171b", "R.91171B", "Plancha de Vapor Premium 1400W", "Plancha de vapor de alta gama con 1400W y depósito de 170ml. Suela cerámica de alta deslizabilidad para planchado profesional.", "1400W", "110V", "Depósito 170ml", "Blanco / Violeta", "6942368204482", "PREMIUM"),
    ("tetera-plastico-1-5l", "H208", "Tetera Eléctrica Plástico 1.5L", "Tetera eléctrica de plástico resistente con capacidad de 1.5 litros. Económica y eficiente para el uso diario.", "N/A", "110V", "1.5 Litros", "Blanco / Negro", "732129008604", "NUEVO"),
    ("panini-metal", "SJ-40A", "Panini Maker Metal 850W", "Sandwichera y parrilla de cuerpo metálico con apertura 180°. 850W de potencia y placas antiadherentes para resultados profesionales.", "850W", "110V / 60Hz", "2 Sandwiches / Parrilla", "Acero / Negro", "732129008383", "PREMIUM"),
    ("sandwichera-grill", "SJ-27", "Sandwichera Grill", "Sandwichera con función grill para sandwiches perfectos con marcas de parrilla. Diseño compacto y placas antiadherentes.", "750W", "110V", "2 Sandwiches", "Negro / Gris", "732129008727", "NUEVO"),
    ("sandwichera-sj35", "SJ-35", "Sandwichera Compacta", "Sandwichera compacta ideal para uso doméstico y pequeños establecimientos. Fácil de usar y limpiar.", "750W", "110V", "2 Sandwiches", "Blanco / Gris", "732129008710", "NUEVO"),
    ("tostadora-metal", "HP-018", "Tostadora Eléctrica 2 Reb. Metal", "Tostadora eléctrica de 2 rebanadas con cuerpo metálico de alta durabilidad. 7 niveles de tostado y funciones de descongelado y recalentado.", "750W", "110V", "2 Rebanadas", "Acero / Negro", "694943899519", "PREMIUM"),
    ("lochera-termica", "JY-1001", "Lochera Térmica Eléctrica", "Lochera eléctrica para mantener la temperatura de los alimentos. Ideal para oficinas, escuelas y personas en movimiento.", "N/A", "110V", "Térmica", "Blanco / Gris", "732129008659", "NUEVO"),
    ("arrocera-0-3l", "HT-03", "Arrocera Mini 0.3L", "Arrocera eléctrica compacta de 0.3 litros con interior antiadherente y vaporizador. Ideal para porciones individuales.", "200W", "110V / 60Hz", "0.3 Litros", "Blanco", "732129008642", "MINI"),
    ("arrocera-1-8l", "HT-18A", "Arrocera 1.8L con Vaporera", "Arrocera eléctrica de 1.8 litros con interior antiadherente y vaporizador incluido. Perfecta para familias medianas.", "700W", "110V / 60Hz", "1.8 Litros", "Blanco", "732129008475", "NUEVO"),
    ("arrocera-2-2l-basica", "HT-22", "Arrocera 2.2L sin Recubrimiento", "Arrocera de 2.2 litros sin recubrimiento en spray. Mayor durabilidad en uso intensivo para negocios y comedores.", "900W", "110V / 60Hz", "2.2 Litros", "Blanco", "732129008505", "NUEVO"),
    ("olla-presion-3-2l", "CK-02-18", "Olla de Presión 3.2L — 18cm", "Olla de presión de aluminio tamaño 3.2 litros (18cm). Compacta e ideal para porciones individuales o parejas.", "N/A (Estufa)", "N/A", "3.2 Litros — 18cm", "Aluminio / Negro", "732129008512", "NUEVO"),
    ("olla-presion-4-2l", "CK-02-20", "Olla de Presión 4.2L — 20cm", "Olla de presión de aluminio 4.2 litros (20cm). Tamaño familiar ideal para preparar guisos, frijoles y sopas.", "N/A (Estufa)", "N/A", "4.2 Litros — 20cm", "Aluminio / Negro", "732129008529", "NUEVO"),
    ("olla-presion-9l", "CK-02-26", "Olla de Presión 9L — 26cm", "Olla de presión de aluminio de 9 litros (26cm). Capacidad máxima para cocinas de alto volumen, comedores y catering.", "N/A (Estufa)", "N/A", "9 Litros — 26cm", "Aluminio / Negro", "732129008550", "GRAN CAPACIDAD"),
]

WA = "50769838322"

def make_html(sku, nombre, desc, potencia, voltaje, capacidad, colores, cod_wa, badge):
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="icon" href="../../media/icons/favicon/favicon-32x32.png" type="image/png">
    <title>{nombre} — HomePower PTY</title>
    <meta name="description" content="{desc} Distribuidor B2B exclusivo en Panamá.">
    <meta name="robots" content="index, follow">
    <link rel="stylesheet" href="../../styles/luxury.css">
    <link rel="stylesheet" href="../../styles/product.css">
    <link rel="stylesheet" href="../../styles/gold-effects.css">
</head>
<body class="product-page">

    <!-- NAVBAR -->
    <div class="announcement-bar">
        <div class="container text-center">
            <span>Distribución B2B · Al por mayor · WhatsApp: (507) 6983-8322</span>
        </div>
    </div>

    <header class="luxury-header">
        <div class="container header-container">
            <div class="logo-container">
                <a href="../../index.html">
                    <img src="../../media/icons/logo/logo.png" alt="Home Power PTY" class="luxury-logo">
                </a>
            </div>
            <nav class="luxury-nav">
                <ul class="nav-links">
                    <li><a href="../../index.html">Inicio</a></li>
                    <li><a href="../../index.html#productos">Electrodomésticos</a></li>
                    <li><a href="../../index.html#nosotros">Nosotros</a></li>
                    <li><a href="../../index.html#contacto">Contacto</a></li>
                </ul>
            </nav>
            <div class="header-actions">
                <a href="https://wa.me/{WA}" class="btn-outline-gold" target="_blank" rel="noopener">Consultar</a>
            </div>
        </div>
    </header>

    <main>

        <!-- HERO -->
        <section class="product-hero">
            <div class="shimmer-sweep" aria-hidden="true"></div>
            <div class="container product-hero-container">
                <div class="product-hero-content">
                    <span class="product-badge-label">{badge}</span>
                    <h1 class="product-hero-title">{nombre}</h1>
                    <p class="product-hero-subtitle">{desc}</p>
                    <div class="product-hero-actions">
                        <a href="https://wa.me/{WA}?text=Hola,%20me%20interesa%20el%20producto%20MOD:%20{sku}"
                           class="btn-solid-gold" target="_blank" rel="noopener">
                            Solicitar Cotización
                            <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24" style="display:inline;vertical-align:middle;margin-left:8px;"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.123.555 4.116 1.527 5.842L0 24l6.335-1.652A11.954 11.954 0 0 0 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.818a9.818 9.818 0 0 1-5.013-1.376l-.36-.214-3.727.977.992-3.626-.235-.373A9.818 9.818 0 1 1 12 21.818z"/></svg>
                        </a>
                        <a href="../../index.html#productos" class="btn-ghost-light">Ver todos los productos</a>
                    </div>
                </div>
                <div class="product-hero-image">
                    <div class="product-hero-img-frame">
                        <img src="./img/PRODUCTO_PRINCIPAL.webp" alt="{nombre} HomePower" class="hero-product-img">
                        <div class="hero-glow"></div>
                    </div>
                </div>
            </div>
        </section>

        <!-- GALLERY -->
        <section class="gallery-section">
            <div class="container">
                <p class="section-eyebrow">GALERÍA DEL PRODUCTO</p>
                <h2 class="section-title-left" style="color:#fff;">Cada ángulo, una historia.</h2>
                <div class="gallery-grid">
                    <div class="gallery-item gallery-item--main" onclick="openLightbox(0)">
                        <img src="./img/LIFESTYLE_DARK.png" alt="{nombre} - Lifestyle" loading="lazy">
                        <div class="gallery-overlay"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg></div>
                    </div>
                    <div class="gallery-item" onclick="openLightbox(1)">
                        <img src="./img/DETAIL_LOGO.png" alt="{nombre} - Detalle" loading="lazy">
                        <div class="gallery-overlay"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg></div>
                    </div>
                    <div class="gallery-item" onclick="openLightbox(2)">
                        <img src="./img/LIFESTYLE_KITCHEN.png" alt="{nombre} - Cocina" loading="lazy">
                        <div class="gallery-overlay"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg></div>
                    </div>
                    <div class="gallery-item" onclick="openLightbox(3)">
                        <img src="./img/BRAND_COMMERCIAL.png" alt="{nombre} - Comercial" loading="lazy">
                        <div class="gallery-overlay"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg></div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Lightbox -->
        <div class="lightbox" id="lightbox" onclick="closeLightbox()">
            <button class="lightbox-close" onclick="closeLightbox()">✕</button>
            <button class="lightbox-prev" onclick="event.stopPropagation(); changeLightbox(-1)">&#8592;</button>
            <img id="lightbox-img" src="" alt="">
            <button class="lightbox-next" onclick="event.stopPropagation(); changeLightbox(1)">&#8594;</button>
        </div>

        <!-- SPECS -->
        <section class="specs-section">
            <div class="container">
                <p class="section-eyebrow">FICHA TÉCNICA</p>
                <h2 class="section-title-left">Especificaciones Completas</h2>
                <div class="specs-layout">
                    <div class="specs-table-wrapper">
                        <table class="specs-table">
                            <tbody>
                                <tr><td>Modelo</td><td>MOD: {sku}</td></tr>
                                <tr><td>Colores</td><td>{colores}</td></tr>
                                <tr><td>Potencia</td><td>{potencia}</td></tr>
                                <tr><td>Voltaje</td><td>{voltaje}</td></tr>
                                <tr><td>Capacidad</td><td>{capacidad}</td></tr>
                                <tr><td>Garantía</td><td>1 Año</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="specs-product-img">
                        <img src="./img/CAJA.webp" alt="{nombre} Empaque" class="caja-img">
                        <div class="specs-note">
                            <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>
                            Producto importado. Distribución exclusiva en Panamá.
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- CTA -->
        <section class="cta-band">
            <div class="container text-center">
                <h2>¿Listo para elevar tu estándar?</h2>
                <p>Solicita una cotización B2B personalizada. Te contactamos en menos de 10 minutos.</p>
                <a href="https://wa.me/{WA}?text=Hola,%20me%20interesa%20el%20producto%20MOD:%20{sku}"
                   class="btn-cta-band" target="_blank" rel="noopener">
                    <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24" style="display:inline;vertical-align:middle;margin-right:8px;"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.123.555 4.116 1.527 5.842L0 24l6.335-1.652A11.954 11.954 0 0 0 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.818a9.818 9.818 0 0 1-5.013-1.376l-.36-.214-3.727.977.992-3.626-.235-.373A9.818 9.818 0 1 1 12 21.818z"/></svg>
                    CONSULTAR PRECIO B2B
                </a>
                <p class="cta-sub-note">Sin compromiso · Respuesta en minutos · Toda Panamá</p>
            </div>
        </section>

    </main>

    <footer class="luxury-footer">
        <div class="container footer-container">
            <div class="footer-col" style="align-items:flex-start;">
                <img src="../../media/icons/logo/logo.png" alt="Home Power" style="max-height:40px; margin-bottom:20px;">
                <p>📞 (507) 6983-8322</p>
                <p>✉️ ventas@homepowerpty.com</p>
            </div>
            <div class="footer-col" style="flex-direction:column; align-items:flex-start; gap:10px;">
                <a href="../../index.html">Inicio</a>
                <a href="../../index.html#productos">Electrodomésticos</a>
                <a href="../../index.html#contacto">Contacto</a>
            </div>
            <div class="footer-col" style="align-items:flex-end;">
                <p style="font-size:0.8rem; color:gray;">© 2024 HomePower PTY.<br>Todos los derechos reservados.</p>
            </div>
        </div>
    </footer>

    <script src="../../scripts/gold-effects.js"></script>
    <script>
        const galleryImages = [
            './img/LIFESTYLE_DARK.png',
            './img/DETAIL_LOGO.png',
            './img/LIFESTYLE_KITCHEN.png',
            './img/BRAND_COMMERCIAL.png',
        ];
        let currentIndex = 0;
        function openLightbox(index) {{
            currentIndex = index;
            document.getElementById('lightbox-img').src = galleryImages[index];
            document.getElementById('lightbox').classList.add('active');
            document.body.style.overflow = 'hidden';
        }}
        function closeLightbox() {{
            document.getElementById('lightbox').classList.remove('active');
            document.body.style.overflow = '';
        }}
        function changeLightbox(dir) {{
            currentIndex = (currentIndex + dir + galleryImages.length) % galleryImages.length;
            document.getElementById('lightbox-img').src = galleryImages[currentIndex];
        }}
        document.addEventListener('keydown', e => {{
            if (e.key === 'Escape') closeLightbox();
            if (e.key === 'ArrowLeft') changeLightbox(-1);
            if (e.key === 'ArrowRight') changeLightbox(1);
        }});
    </script>
</body>
</html>"""


def run():
    productos_dir = os.path.join(BASE, "productos")
    created = 0

    for item in NEW_PRODUCTS:
        folder, sku, nombre, desc, potencia, voltaje, capacidad, colores, cod_wa, badge = item
        folder_path = os.path.join(productos_dir, folder)
        img_path = os.path.join(folder_path, "img")
        html_path = os.path.join(folder_path, "index.html")

        os.makedirs(img_path, exist_ok=True)

        if not os.path.exists(html_path):
            html = make_html(sku, nombre, desc, potencia, voltaje, capacidad, colores, cod_wa, badge)
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html)
            created += 1
            print(f"  ✓ Creado: {folder}")
        else:
            print(f"  ~ Existe: {folder}")

    print(f"\nListo: {created} nuevas páginas creadas.")


if __name__ == "__main__":
    run()
