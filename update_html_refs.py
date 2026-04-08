import os
import re

base_dir = r"c:\Users\HP 15\Homepowerpty.com\productos"
updates = []

for prod in os.listdir(base_dir):
    prod_path = os.path.join(base_dir, prod)
    if not os.path.isdir(prod_path):
        continue
    index_file = os.path.join(prod_path, 'index.html')
    if not os.path.exists(index_file):
        continue

    with open(index_file, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html

    img_dir = os.path.join(prod_path, 'img')
    if os.path.isdir(img_dir):
        existing = os.listdir(img_dir)
    else:
        existing = []

    def find_ext(key):
        for f in existing:
            name, ext = os.path.splitext(f)
            if name == key:
                return ext
        return '.webp'

    # Find all src="./img/..." or src="img/..." patterns and replace
    def replace_img(m):
        src = m.group(1)
        fname = os.path.basename(src)
        fname_lower = fname.lower()
        fname_noext = os.path.splitext(fname)[0].lower()

        # Map to standard keys
        if 'lifestyle_dark' in fname_lower:
            new = 'LIFESTYLE_DARK' + find_ext('LIFESTYLE_DARK')
        elif 'detail_logo' in fname_lower or 'detail_panel' in fname_lower:
            new = 'DETAIL_LOGO' + find_ext('DETAIL_LOGO')
        elif 'lifestyle_kitchen' in fname_lower or 'lifestyle_food' in fname_lower or 'lifestyle_morning' in fname_lower:
            new = 'LIFESTYLE_KITCHEN' + find_ext('LIFESTYLE_KITCHEN')
        elif 'brand_commercial' in fname_lower or 'lifestyle_office' in fname_lower:
            new = 'BRAND_COMMERCIAL' + find_ext('BRAND_COMMERCIAL')
        elif 'caja' in fname_lower:
            new = 'CAJA' + find_ext('CAJA')
        elif 'producto_principal' in fname_lower:
            new = 'PRODUCTO_PRINCIPAL' + find_ext('PRODUCTO_PRINCIPAL')
        else:
            # Heuristic: no keyword match, likely the main product image
            # Keep as PRODUCTO_PRINCIPAL
            new = 'PRODUCTO_PRINCIPAL' + find_ext('PRODUCTO_PRINCIPAL')

        new_src = './img/' + new
        if new_src != src:
            return m.group(0).replace(src, new_src)
        return m.group(0)

    html = re.sub(r'src=["\'](\./img/[^"\']+)["\']', replace_img, html)
    
    # Also handle the galleryImages array in <script>
    def replace_gallery(m):
        src = m.group(1)
        fname = os.path.basename(src)
        fname_lower = fname.lower()

        if 'lifestyle_dark' in fname_lower:
            new = 'LIFESTYLE_DARK' + find_ext('LIFESTYLE_DARK')
        elif 'detail_logo' in fname_lower or 'detail_panel' in fname_lower:
            new = 'DETAIL_LOGO' + find_ext('DETAIL_LOGO')
        elif 'lifestyle_kitchen' in fname_lower or 'lifestyle_food' in fname_lower or 'lifestyle_morning' in fname_lower:
            new = 'LIFESTYLE_KITCHEN' + find_ext('LIFESTYLE_KITCHEN')
        elif 'brand_commercial' in fname_lower or 'lifestyle_office' in fname_lower:
            new = 'BRAND_COMMERCIAL' + find_ext('BRAND_COMMERCIAL')
        elif 'caja' in fname_lower:
            new = 'CAJA' + find_ext('CAJA')
        elif 'producto_principal' in fname_lower:
            new = 'PRODUCTO_PRINCIPAL' + find_ext('PRODUCTO_PRINCIPAL')
        else:
            new = fname  # keep as-is if no match

        new_src = m.group(0).replace(fname, new)
        return new_src

    html = re.sub(r"['\"](\./img/[^'\"]+)['\"]", lambda m: m.group(0).replace(m.group(0)[1:-1], './img/' + (
        'LIFESTYLE_DARK' + find_ext('LIFESTYLE_DARK') if 'lifestyle_dark' in m.group(0).lower() else
        'DETAIL_LOGO' + find_ext('DETAIL_LOGO') if ('detail_logo' in m.group(0).lower() or 'detail_panel' in m.group(0).lower()) else
        'LIFESTYLE_KITCHEN' + find_ext('LIFESTYLE_KITCHEN') if any(x in m.group(0).lower() for x in ['lifestyle_kitchen','lifestyle_food','lifestyle_morning']) else
        'BRAND_COMMERCIAL' + find_ext('BRAND_COMMERCIAL') if any(x in m.group(0).lower() for x in ['brand_commercial','lifestyle_office']) else
        'CAJA' + find_ext('CAJA') if 'caja' in m.group(0).lower() else
        'PRODUCTO_PRINCIPAL' + find_ext('PRODUCTO_PRINCIPAL') if 'producto_principal' in m.group(0).lower() else
        m.group(0)[1:-1]
    )), html)

    if html != original:
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(html)
        updates.append(prod)

print('Updated product pages:', len(updates))
for u in updates:
    print(' -', u)
