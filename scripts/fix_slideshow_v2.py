import os
import re

def update_slideshow(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Si ya tiene la clave del slideshow nuevo, no hacer nada
    if 'let pdsSlideshowInterval;' in content:
        return False

    # PATRÓN MÁS FLEXIBLE: Busca pdpImages y pdpSetImage esté como esté el array
    pattern = re.compile(r'const pdpImages = \[.*?\];?\s*let pdpLightboxIndex = 0;.*?(function pdpSetImage\(src, thumbEl\) \{.*?currentLightboxSrc = src;\s*\})', re.DOTALL)
    
    match = pattern.search(content)
    if not match:
        return False

    # Extraemos el array actual de imágenes (para preservarlas)
    array_match = re.search(r'const pdpImages = \[.*?\];', match.group(0), re.DOTALL)
    current_array = array_match.group(0) if array_match else "const pdpImages = [];"

    new_js_block = f"""{current_array}
        let pdpLightboxIndex = 0;
        let pdsSlideshowInterval;
        let pdpCurrentGalleryIndex = 0;
        const SLIDE_DURATION = 2500;

        function startSlideshow() {{
            stopSlideshow();
            if (pdpImages.length <= 1) return;
            pdsSlideshowInterval = setInterval(() => {{
                pdpCurrentGalleryIndex = (pdpCurrentGalleryIndex + 1) % pdpImages.length;
                const nextSrc = pdpImages[pdpCurrentGalleryIndex];
                const thumbs = document.querySelectorAll('.pdp-thumb');
                if (thumbs[pdpCurrentGalleryIndex]) {{
                    pdpSetImage(nextSrc, thumbs[pdpCurrentGalleryIndex], true);
                }}
            }}, SLIDE_DURATION);
        }}

        function stopSlideshow() {{
            if (pdsSlideshowInterval) clearInterval(pdsSlideshowInterval);
        }}

        function pdpSetImage(src, thumbEl, isAutomatic = false) {{
            const mainImg = document.getElementById('pdpMainImg');
            mainImg.style.opacity = '0';
            setTimeout(() => {{ 
                mainImg.src = src; 
                mainImg.style.opacity = '1'; 
            }}, 150);
            document.querySelectorAll('.pdp-thumb').forEach(t => t.classList.remove('active'));
            thumbEl.classList.add('active');
            
            // Actualizar el índice actual para el slideshow
            pdpCurrentGalleryIndex = Array.from(document.querySelectorAll('.pdp-thumb')).indexOf(thumbEl);

            // Si el usuario hace click manualmente, reiniciamos el timer
            if (!isAutomatic) {{
                startSlideshow();
            }}
        }}"""

    new_content = content.replace(match.group(0), new_js_block)

    # Inyectar el DOMContentLoaded si no está
    if 'startSlideshow();' not in new_content:
        # Buscamos pdpOpenLightbox
        old_trigger_pattern = re.compile(r'function pdpOpenLightbox\(\) \{', re.DOTALL)
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

productos_dir = 'productos'
updated_count = 0

for root, dirs, files in os.walk(productos_dir):
    if 'index.html' in files:
        file_path = os.path.join(root, 'index.html')
        # Evitamos el hp-020 que ya sabemos que está bien
        if 'hp-020' in file_path: continue
        if update_slideshow(file_path):
            print(f"Actualizado: {file_path}")
            updated_count += 1

print(f"Total dearchivos actualizados en la segunda pasada: {updated_count}")
