import os
import re

# Carpetas a auditar y corregir
target_folders = [
    'productos/batidoras',
    'productos/estufas'
]

def structural_fix(f_path):
    if not os.path.exists(f_path):
        return False
    
    with open(f_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Extraer los thumbs
    thumbs_pat = re.compile(r'(<div\s+class="pdp-thumbs"[\s\S]*?</div>)', re.DOTALL)
    thumbs_match = thumbs_pat.search(content)
    if not thumbs_match:
        return False
    thumbs_html = thumbs_match.group(1)
    
    # 2. Extraer la imagen principal
    main_img_pat = re.compile(r'(<img\s+id="pdpMainImg"[\s\S]*?>)', re.DOTALL)
    main_img_match = main_img_pat.search(content)
    if not main_img_match:
        return False
    main_img_tag = main_img_match.group(1)

    # 3. Extraer el modelo del nombre del archivo o del contenido
    model_match = re.search(r'<p class="pdp-model">(.*?)</p>', content)
    model_name = model_match.group(1) if model_match else "PRODUCTO"

    # Reconstrucción TOTAL garantizada
    new_gallery = f'''                <!-- LEFT: GALLERY -->
                <div class="pdp-gallery">

                    <div class="pdp-main-img-wrap" id="pdpMainImgWrap"
                         onclick="pdpOpenLightbox()"
                         role="button"
                         tabindex="0"
                         aria-label="Ampliar imagen">
                        {main_img_tag}
                        <div class="pdp-zoom-hint" aria-hidden="true">
                            <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg>
                            Ampliar
                        </div>
                    </div>

                    {thumbs_html}

                </div>'''

    target_pat = re.compile(r'<!-- LEFT: GALLERY -->[\s\S]*?<!-- RIGHT: INFO PANEL -->', re.DOTALL)
    
    # Solo aplicamos si el patrón existe
    if target_pat.search(content):
        new_content = target_pat.sub(new_gallery + '\n\n                <!-- RIGHT: INFO PANEL -->', content)
        
        # Limpieza extra: quitar prefijo MOD: si existe
        new_content = new_content.replace('MOD: ', '')
        
        with open(f_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

if __name__ == "__main__":
    count = 0
    for folder in target_folders:
        for root, dirs, files in os.walk(folder):
            if 'index.html' in files:
                file_path = os.path.join(root, 'index.html')
                if structural_fix(file_path):
                    print(f"Fixed: {file_path}")
                    count += 1
    print(f"Total files fixed: {count}")
