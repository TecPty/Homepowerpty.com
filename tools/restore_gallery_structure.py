import os
import re

files = [
    'productos/percoladoras/hp-047/index.html',
    'productos/percoladoras/hp-048/index.html',
    'productos/percoladoras/hp-049/index.html'
]

def final_fix(f_path):
    full_path = os.path.join(os.getcwd(), f_path)
    if not os.path.exists(full_path):
        print(f"File not found: {f_path}")
        return
    
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Extraer los thumbs
    thumbs_pat = re.compile(r'(<div\s+class="pdp-thumbs"[\s\S]*?</div>)', re.DOTALL)
    thumbs_match = thumbs_pat.search(content)
    if not thumbs_match:
        print(f"Thumbs not found in {f_path}")
        return
    thumbs_html = thumbs_match.group(1)
    
    # 2. Extraer la imagen principal
    main_img_pat = re.compile(r'(<img\s+id="pdpMainImg"[\s\S]*?>)', re.DOTALL)
    main_img_match = main_img_pat.search(content)
    if not main_img_match:
        print(f"Main image not found in {f_path}")
        return
    main_img_tag = main_img_match.group(1)

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
    content = target_pat.sub(new_gallery + '\n\n                <!-- RIGHT: INFO PANEL -->', content)
    
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully fixed gallery structure in {f_path}")

if __name__ == "__main__":
    for f in files:
        final_fix(f)
