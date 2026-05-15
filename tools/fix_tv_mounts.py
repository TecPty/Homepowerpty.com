import os
import re

# Configuración
TARGET_DIR = "productos/soportes-tv"
MODELS = ["hp-040", "hp-041", "hp-042", "hp-043"]

def fix_extensions_and_add_slideshow(model):
    path = os.path.join(TARGET_DIR, model, "index.html")
    if not os.path.exists(path):
        print(f"Skipping {model}, file not found.")
        return

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Corregir extensiones .webp a .png en la propia galería del producto
    # (Ya convertimos a webp en el paso anterior, así que forzamos todo a .webp para la galería)
    content = content.replace('.png"', '.webp"')
    content = content.replace(".png',", ".webp',")
    
    # 2. Corregir rutas de assets globales (evitar que busquen .webp donde hay .png)
    content = content.replace('logo_white_premium.webp', 'logo_white_premium.png')
    content = content.replace('favicon-32x32.webp', 'favicon-32x32.png')

    # 3. Corregir extensiones en la sección de relacionados (pdp-related)
    content = re.sub(r'src="\.\/(hp-04[0-3])\/img\/([^"]+)\.webp"', r'src="./\1/img/\2.webp"', content)
    content = re.sub(r'src="\.\.\/(hp-04[0-3])\/img\/([^"]+)\.(png|webp)"', r'src="../\1/img/\2.webp"', content)

    # 4. Agregar lógica de Slideshow Automático (2.5s) - CORREGIDO PARA EVITAR DUPLICADOS
    if "const autoSlideshowInterval =" not in content and "let autoSlideshowInterval =" not in content:
        slideshow_script = """
    <!-- SLIDESHOW LOGIC -->
    <script>
        (function() {
            let autoSlideshowInterval = setInterval(() => {
                const thumbs = document.querySelectorAll('.pdp-thumb');
                if (thumbs.length <= 1) return;
                
                let currentIndex = Array.from(thumbs).findIndex(t => t.classList.contains('active'));
                let nextIndex = (currentIndex + 1) % thumbs.length;
                thumbs[nextIndex].click();
            }, 2500);

            const mainGallery = document.querySelector('.pdp-gallery');
            if (mainGallery) {
                mainGallery.addEventListener('mouseenter', () => clearInterval(autoSlideshowInterval));
                mainGallery.addEventListener('mouseleave', () => {
                    autoSlideshowInterval = setInterval(() => {
                        const thumbs = document.querySelectorAll('.pdp-thumb');
                        if (thumbs.length <= 1) return;
                        let currentIndex = Array.from(thumbs).findIndex(t => t.classList.contains('active'));
                        let nextIndex = (currentIndex + 1) % thumbs.length;
                        thumbs[nextIndex].click();
                    }, 2500);
                });
            }
        })();
    </script>
"""
        content = content.replace("</body>", slideshow_script + "</body>")

    # 3. Agregar lógica de Slideshow Automático (2.5s)
    # Buscamos el final de scripts o el final del body si no hay scripts específicos
    # Primero verificamos si ya tiene slideshow para no duplicar
    if "const autoSlideshowInterval =" not in content:
        slideshow_script = """
    <!-- SLIDESHOW LOGIC -->
    <script>
        let autoSlideshowInterval = setInterval(() => {
            const thumbs = document.querySelectorAll('.pdp-thumb');
            if (thumbs.length <= 1) return;
            
            let currentIndex = Array.from(thumbs).findIndex(t => t.classList.contains('active'));
            let nextIndex = (currentIndex + 1) % thumbs.length;
            thumbs[nextIndex].click();
        }, 2500);

        // Pause on hover
        const mainGallery = document.querySelector('.pdp-gallery');
        if (mainGallery) {
            mainGallery.addEventListener('mouseenter', () => clearInterval(autoSlideshowInterval));
            mainGallery.addEventListener('mouseleave', () => {
                autoSlideshowInterval = setInterval(() => {
                    const thumbs = document.querySelectorAll('.pdp-thumb');
                    if (thumbs.length <= 1) return;
                    let currentIndex = Array.from(thumbs).findIndex(t => t.classList.contains('active'));
                    let nextIndex = (currentIndex + 1) % thumbs.length;
                    thumbs[nextIndex].click();
                }, 2500);
            });
        }
    </script>
"""
        # Insertar antes del cierre de body
        content = content.replace("</body>", slideshow_script + "</body>")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Fixed {model}")

if __name__ == "__main__":
    for model in MODELS:
        fix_extensions_and_add_slideshow(model)
