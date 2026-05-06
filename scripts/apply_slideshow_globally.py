import os
import re

def update_slideshow(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Patrón para detectar el JS del producto que no tiene el slideshow nuevo
    # Buscamos el array pdpImages y las funciones básicas
    if 'let pdsSlideshowInterval;' in content:
        return False # Ya está actualizado

    # Regex para capturar el bloque de script antiguo
    # Buscamos desde las miniaturas hasta el lightbox
    pattern = re.compile(r'(const pdpImages = \[\s*\'\./img/PRODUCTO_PRINCIPAL\.webp\',\s*\];?\s*let pdpLightboxIndex = 0;\s*let currentLightboxSrc = pdpImages\[0\] \|\| \'\';\s*function pdpSetImage\(src, thumbEl\) \{)', re.DOTALL)
    
    # El nuevo bloque JS que queremos inyectar
    new_js_block = """const pdpImages = [
            './img/PRODUCTO_PRINCIPAL.webp',
        ];
        let pdpLightboxIndex = 0;
        let pdsSlideshowInterval;
        let pdpCurrentGalleryIndex = 0;
        const SLIDE_DURATION = 2500;

        function startSlideshow() {
            stopSlideshow();
            if (pdpImages.length <= 1) return;
            pdsSlideshowInterval = setInterval(() => {
                pdpCurrentGalleryIndex = (pdpCurrentGalleryIndex + 1) % pdpImages.length;
                const nextSrc = pdpImages[pdpCurrentGalleryIndex];
                const thumbs = document.querySelectorAll('.pdp-thumb');
                if (thumbs[pdpCurrentGalleryIndex]) {
                    pdpSetImage(nextSrc, thumbs[pdpCurrentGalleryIndex], true);
                }
            }, SLIDE_DURATION);
        }

        function stopSlideshow() {
            if (pdsSlideshowInterval) clearInterval(pdsSlideshowInterval);
        }

        function pdpSetImage(src, thumbEl, isAutomatic = false) {"""

    new_content = pattern.sub(new_js_block, content)
    
    # También necesitamos inyectar el DOMContentLoaded y los event listeners
    if 'startSlideshow();' not in new_content:
        # Buscamos donde termina el bloque de scripts o antes de pdpOpenLightbox
        old_trigger_pattern = re.compile(r'(function pdpOpenLightbox\(\) \{)', re.DOTALL)
        
        event_listeners = """// Iniciar slideshow al cargar
        document.addEventListener('DOMContentLoaded', () => {
            startSlideshow();
            const galleryArea = document.querySelector('.pdp-gallery');
            if (galleryArea) {
                galleryArea.addEventListener('mouseenter', stopSlideshow);
                galleryArea.addEventListener('mouseleave', startSlideshow);
            }
        });

        function pdpOpenLightbox() {"""
        
        new_content = old_trigger_pattern.sub(event_listeners, new_content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

# Buscar todos los index.html en productos
productos_dir = 'productos'
updated_count = 0

for root, dirs, files in os.walk(productos_dir):
    if 'index.html' in files:
        file_path = os.path.join(root, 'index.html')
        if update_slideshow(file_path):
            print(f"Actualizado: {file_path}")
            updated_count += 1

print(f"Total dearchivos actualizados: {updated_count}")
