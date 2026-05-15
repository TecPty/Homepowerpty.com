import os
import re

target_folders = ['productos/planchas', 'productos/teteras']

def structural_fix(f_path):
    if not os.path.exists(f_path): return False
    with open(f_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extraer imagen principal
    main_img_pat = re.compile(r'(<img\s+id="pdpMainImg"[\s\S]*?>)', re.DOTALL)
    main_img_match = main_img_pat.search(content)
    if not main_img_match: return False
    main_img_tag = main_img_match.group(1)

    # Extraer thumbs
    thumbs_pat = re.compile(r'(<div\s+class="pdp-thumbs"[\s\S]*?</div>)', re.DOTALL)
    thumbs_match = thumbs_pat.search(content)
    if not thumbs_match: return False
    thumbs_html = thumbs_match.group(1)

    # Reconstrucción del bloque de galería
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

    boundary_pat = re.compile(r'<!-- LEFT: GALLERY -->[\s\S]*?<!-- RIGHT: INFO PANEL -->', re.DOTALL)
    if boundary_pat.search(content):
        new_content = boundary_pat.sub(new_gallery + '\n\n                <!-- RIGHT: INFO PANEL -->', content)
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
                p = os.path.join(root, 'index.html')
                if structural_fix(p):
                    count += 1
                    print(f"Fixed: {p}")
    print(f"Total fixed: {count}")
