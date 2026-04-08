import os, re

path = r"c:\Users\HP 15\Homepowerpty.com\index.html"
with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

original = html

# Update data-box and src attributes that reference product img folders
def replace_product_src(m):
    attr = m.group(1)  # src or data-box
    quote = m.group(2)
    src = m.group(3)
    fname = os.path.basename(src)
    fname_lower = fname.lower()

    if 'caja' in fname_lower:
        new_name = 'CAJA.webp'
    else:
        new_name = 'PRODUCTO_PRINCIPAL.webp'

    folder = '/'.join(src.split('/')[:-1])
    new_src = folder + '/' + new_name

    if new_src != src:
        return attr + '=' + quote + new_src + quote
    return m.group(0)

html = re.sub(
    r'(src|data-box)=(["\'])(productos/[^"\']+/img/[^"\']+)(["\'])',
    lambda m: (m.group(1) + '=' + m.group(2) + 
        ('/'.join(m.group(3).split('/')[:-1]) + '/CAJA.webp' if 'caja' in m.group(3).lower() else
         '/'.join(m.group(3).split('/')[:-1]) + '/PRODUCTO_PRINCIPAL.webp')
        + m.group(2)),
    html
)

if html != original:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('index.html updated successfully.')
else:
    print('No changes needed in index.html.')
