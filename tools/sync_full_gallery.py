import os
import re

# Configuración
TARGET_DIR = "productos/soportes-tv"
MODELS = ["hp-040", "hp-041", "hp-042", "hp-043"]

def get_images_from_thumbs(content):
    # Busca todas las imágenes dentro de los thumbnails (pdp-thumb)
    thumbs_section = re.search(r'<div class="pdp-thumbs"[^>]*>(.*?)</div>', content, re.DOTALL)
    if not thumbs_section:
        return []
    
    # Extrae las rutas de las imágenes de los thumbs
    img_paths = re.findall(r'src="([^"]+)"', thumbs_section.group(1))
    return img_paths

def generate_gallery_strip_html(img_paths):
    html = '<div class="pdp-gallery-strip-grid">\n'
    for i, path in enumerate(img_paths):
        # Aseguramos que use .webp para el strip
        webp_path = path.replace('.png', '.webp')
        alt_text = f"Vista {i+1}"
        html += f'                        <div class="pdp-strip-item" onclick="pdpOpenLightboxAt({i})" role="button" tabindex="0" aria-label="Ampliar {alt_text}">\n'
        html += f'                            <img src="{webp_path}" alt="{alt_text}" loading="lazy">\n'
        html += f'                            <div class="pdp-strip-overlay" aria-hidden="true"><svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg></div>\n'
        html += f'                        </div>\n'
    html += '                    </div>'
    return html

def fix_full_gallery(model):
    path = os.path.join(TARGET_DIR, model, "index.html")
    if not os.path.exists(path):
        print(f"Skipping {model}, file not found.")
        return

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Obtener las imágenes actuales de los thumbs
    img_paths = get_images_from_thumbs(content)
    if not img_paths:
        print(f"No thumbnails found for {model}")
        return

    # 2. Generar el nuevo HTML para el strip
    new_strip_html = generate_gallery_strip_html(img_paths)

    # 3. Reemplazar la sección pdp-gallery-strip-grid
    pattern = r'<div class="pdp-gallery-strip-grid">.*?</div>'
    content = re.sub(pattern, new_strip_html, content, flags=re.DOTALL)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated Full Gallery for {model} ({len(img_paths)} images)")

if __name__ == "__main__":
    for model in MODELS:
        fix_full_gallery(model)
