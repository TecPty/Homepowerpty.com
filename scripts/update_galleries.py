import re
import os

def update_gallery(file_path, images):
    if not os.path.exists(file_path):
        return
    data = open(file_path, 'r', encoding='utf-8').read()
    
    # Update pdp-thumbs
    thumbs_html = '<div class="pdp-thumbs" role="list" aria-label="Imágenes del producto">\n'
    for i, img in enumerate(images):
        active = ' active' if i == 0 else ''
        thumbs_html += f'                        <button class="pdp-thumb{active}"\n                                onclick="pdpSetImage(\'./img/{img}\', this)"\n                                aria-label="Ver vista {i+1}" role="listitem">\n                            <img src="./img/{img}" alt="Vista {i+1}">\n                        </button>\n'
    thumbs_html += '                    </div>'
    data = re.sub(r'<div class="pdp-thumbs".*?</div>\s*</div>', thumbs_html + '\n                </div>', data, flags=re.DOTALL)
    
    # Update pdp-gallery-strip-grid
    strip_html = '<div class="pdp-gallery-strip-grid">\n'
    for i, img in enumerate(images):
        strip_html += f'                        <div class="pdp-strip-item" onclick="pdpOpenLightboxAt({i})" role="button" tabindex="0" aria-label="Ampliar Vista {i+1}">\n                            <img src="./img/{img}" alt="Vista {i+1}" loading="lazy">\n                            <div class="pdp-strip-overlay" aria-hidden="true"><svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg></div>\n                        </div>\n'
    strip_html += '                    </div>'
    data = re.sub(r'<div class="pdp-gallery-strip-grid">.*?</div>\s*</div>\s*</div>\s*</div>', strip_html + '\n                    </div>\n                </div>\n            </div>', data, flags=re.DOTALL)
    
    # Update pdpImages
    pdp_array = 'const pdpImages = [\n'
    for img in images:
        pdp_array += f'            \'./img/{img}\',\n'
    pdp_array += '        ];'
    data = re.sub(r'const pdpImages = \[.*?\];', pdp_array, data, flags=re.DOTALL)
    
    # Update main image to use the first image in the list
    data = re.sub(r'<img id="pdpMainImg"\s*src="\./img/[^"]+"', f'<img id="pdpMainImg"\n                             src="./img/{images[0]}"', data)
    data = re.sub(r'<img class="pdp-lightbox-img" id="pdpLightboxImg" src="\./img/[^"]+"', f'<img class="pdp-lightbox-img" id="pdpLightboxImg" src="./img/{images[0]}"', data)

    open(file_path, 'w', encoding='utf-8').write(data)

update_gallery('productos/soportes-tv/hp-040/index.html', ['PRODUCTO_PRINCIPAL.webp', 'BRAND_COMMERCIAL.webp', 'DETAIL.webp', 'FLAT_LAY.webp', 'LIFESTYLE_DAY.webp'])
update_gallery('productos/soportes-tv/hp-041/index.html', ['PRODUCTO_PRINCIPAL.webp', 'BRAND_COMMERCIAL.webp', 'DETAIL_.webp', 'FLAT_LAY.webp', 'LIFESTYLE_DARK.webp'])
