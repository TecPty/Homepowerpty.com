import re

BASE = r'C:\Users\HP 15\Homepowerpty.com\productos\sandwicheras'

STRIP_SVG = '<svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg>'

def strip_item(index, src, label, alt):
    return f'''                        <div class="pdp-strip-item" onclick="pdpOpenLightboxAt({index})" role="button" tabindex="0" aria-label="{label}">
                            <img src="{src}" alt="{alt}" loading="lazy">
                            <div class="pdp-strip-overlay" aria-hidden="true">
                                {STRIP_SVG}
                            </div>
                        </div>'''

def thumb_btn(src, label, alt, active=False):
    cls = 'pdp-thumb active' if active else 'pdp-thumb'
    return f'''                        <button class="{cls}"
                                onclick="pdpSetImage('{src}', this)"
                                aria-label="{label}" role="listitem">
                            <img src="{src}" alt="{alt}">
                        </button>'''

# ─── sj-22 ────────────────────────────────────────────────────────────────────
print('=== sj-22 ===')
path = rf'{BASE}\sj-22\index.html'
html = open(path, encoding='utf-8').read()

# Remove 4 fake PNG thumbs + fix CAJA.webp -> CAJA_PRINCIPAL.webp
old_thumbs = '''                        <button class="pdp-thumb"
                                onclick="pdpSetImage('./img/LIFESTYLE_DARK.png', this)"
                                aria-label="Ver Lifestyle Dark" role="listitem">
                            <img src="./img/LIFESTYLE_DARK.png" alt="Lifestyle Dark">
                        </button>
                        <button class="pdp-thumb"
                                onclick="pdpSetImage('./img/LIFESTYLE_KITCHEN.png', this)"
                                aria-label="Ver Lifestyle Kitchen" role="listitem">
                            <img src="./img/LIFESTYLE_KITCHEN.png" alt="Lifestyle Kitchen">
                        </button>
                        <button class="pdp-thumb"
                                onclick="pdpSetImage('./img/DETAIL_LOGO.png', this)"
                                aria-label="Ver Detail Logo" role="listitem">
                            <img src="./img/DETAIL_LOGO.png" alt="Detail Logo">
                        </button>
                        <button class="pdp-thumb"
                                onclick="pdpSetImage('./img/BRAND_COMMERCIAL.png', this)"
                                aria-label="Ver Brand Commercial" role="listitem">
                            <img src="./img/BRAND_COMMERCIAL.png" alt="Brand Commercial">
                        </button>
                        <button class="pdp-thumb"
                                onclick="pdpSetImage('./img/CAJA.webp', this)"
                                aria-label="Ver Caja" role="listitem">
                            <img src="./img/CAJA.webp" alt="Caja">
                        </button>'''
new_thumbs = thumb_btn('./img/CAJA_PRINCIPAL.webp', 'Ver Caja', 'Caja')
html = html.replace(old_thumbs, new_thumbs)

# Gallery strip: replace 4 bogus items with 1 CAJA_PRINCIPAL at index 1
old_strip = '''                    <div class="pdp-gallery-strip-grid">
                        <div class="pdp-strip-item" onclick="pdpOpenLightboxAt(0)" role="button" tabindex="0" aria-label="Ampliar Lifestyle Dark">
                            <img src="./img/LIFESTYLE_DARK.png" alt="Lifestyle Dark" loading="lazy">
                            <div class="pdp-strip-overlay" aria-hidden="true">
                                <svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg>
                            </div>
                        </div>
                        <div class="pdp-strip-item" onclick="pdpOpenLightboxAt(1)" role="button" tabindex="0" aria-label="Ampliar Lifestyle Kitchen">
                            <img src="./img/LIFESTYLE_KITCHEN.png" alt="Lifestyle Kitchen" loading="lazy">
                            <div class="pdp-strip-overlay" aria-hidden="true">
                                <svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg>
                            </div>
                        </div>
                        <div class="pdp-strip-item" onclick="pdpOpenLightboxAt(2)" role="button" tabindex="0" aria-label="Ampliar Detail Logo">
                            <img src="./img/DETAIL_LOGO.png" alt="Detail Logo" loading="lazy">
                            <div class="pdp-strip-overlay" aria-hidden="true">
                                <svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg>
                            </div>
                        </div>
                        <div class="pdp-strip-item" onclick="pdpOpenLightboxAt(3)" role="button" tabindex="0" aria-label="Ampliar Brand Commercial">
                            <img src="./img/BRAND_COMMERCIAL.png" alt="Brand Commercial" loading="lazy">
                            <div class="pdp-strip-overlay" aria-hidden="true">
                                <svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg>
                            </div>
                        </div>
                    </div>'''
new_strip = f'''                    <div class="pdp-gallery-strip-grid">
{strip_item(1, './img/CAJA_PRINCIPAL.webp', 'Ampliar Caja', 'Caja')}
                    </div>'''
html = html.replace(old_strip, new_strip)

# pdpImages
old_pdp = """        const pdpImages = [
            './img/PRODUCTO_PRINCIPAL.webp',
            './img/LIFESTYLE_DARK.png',
            './img/LIFESTYLE_KITCHEN.png',
            './img/DETAIL_LOGO.png',
            './img/BRAND_COMMERCIAL.png',
            './img/CAJA.webp',
        ];"""
new_pdp = """        const pdpImages = [
            './img/PRODUCTO_PRINCIPAL.webp',
            './img/CAJA_PRINCIPAL.webp',
        ];"""
html = html.replace(old_pdp, new_pdp)

open(path, 'w', encoding='utf-8').write(html)
print('OK: sj-22 fixed')

# ─── sj-24 ────────────────────────────────────────────────────────────────────
print('=== sj-24 ===')
path = rf'{BASE}\sj-24\index.html'
html = open(path, encoding='utf-8').read()

# Same thumb removal as sj-22
html = html.replace(old_thumbs, new_thumbs)

# Same strip replacement as sj-22
html = html.replace(old_strip, new_strip)

# pdpImages (same pattern)
html = html.replace(old_pdp, new_pdp)

# Fix WA links: COD:6975069404462 -> MOD: SJ-24
html = html.replace(
    'Hola,%20me%20interesa%20la%20Sandwichera%20Metal%20COD:%206975069404462',
    'Hola,%20me%20interesa%20la%20Sandwichera%20Metal%20MOD:%20SJ-24'
)

open(path, 'w', encoding='utf-8').write(html)
print('OK: sj-24 fixed')

# ─── sj-27 ────────────────────────────────────────────────────────────────────
print('=== sj-27 ===')
path = rf'{BASE}\sj-27\index.html'
html = open(path, encoding='utf-8').read()

# Main img .png -> .webp
html = html.replace(
    'src="./img/PRODUCTO_PRINCIPAL.png"\n                             alt="Sandwichera Grill — HomePower PTY"',
    'src="./img/PRODUCTO_PRINCIPAL.webp"\n                             alt="Sandwichera Grill — HomePower PTY"'
)

# Thumbs: replace single .png thumb with 4 .webp thumbs
old_thumbs27 = '''                    <div class="pdp-thumbs" role="list" aria-label="Imágenes del producto">
                        <button class="pdp-thumb active"
                                onclick="pdpSetImage('./img/PRODUCTO_PRINCIPAL.png', this)"
                                aria-label="Ver imagen principal" role="listitem">
                            <img src="./img/PRODUCTO_PRINCIPAL.png" alt="Vista principal">
                        </button>
                    </div>'''
new_thumbs27 = '''                    <div class="pdp-thumbs" role="list" aria-label="Imágenes del producto">
''' + thumb_btn('./img/PRODUCTO_PRINCIPAL.webp', 'Ver imagen principal', 'Vista principal', active=True) + '\n' + \
thumb_btn('./img/PRODUCTO_PRINCIPAL_ABIERTO.webp', 'Ver producto abierto', 'Producto abierto') + '\n' + \
thumb_btn('./img/PRODUCTO_PRINCIPAL_GRANDE.webp', 'Ver vista grande', 'Vista grande') + '\n' + \
thumb_btn('./img/PRODUCTO_PRINCIPAL_GRANDE_ABIERTO.webp', 'Ver vista grande abierto', 'Vista grande abierto') + '\n' + \
'                    </div>'
html = html.replace(old_thumbs27, new_thumbs27)

# Gallery strip: add 4 items
old_strip27 = '''                    <div class="pdp-gallery-strip-grid">
                    </div>'''
new_strip27 = f'''                    <div class="pdp-gallery-strip-grid">
{strip_item(0, './img/PRODUCTO_PRINCIPAL.webp', 'Ampliar vista principal', 'Vista principal')}
{strip_item(1, './img/PRODUCTO_PRINCIPAL_ABIERTO.webp', 'Ampliar producto abierto', 'Producto abierto')}
{strip_item(2, './img/PRODUCTO_PRINCIPAL_GRANDE.webp', 'Ampliar vista grande', 'Vista grande')}
{strip_item(3, './img/PRODUCTO_PRINCIPAL_GRANDE_ABIERTO.webp', 'Ampliar vista grande abierto', 'Vista grande abierto')}
                    </div>'''
html = html.replace(old_strip27, new_strip27)

# pdpImages: [,] -> full list
html = html.replace(
    '        const pdpImages = [\n            ,\n        ];',
    "        const pdpImages = [\n            './img/PRODUCTO_PRINCIPAL.webp',\n            './img/PRODUCTO_PRINCIPAL_ABIERTO.webp',\n            './img/PRODUCTO_PRINCIPAL_GRANDE.webp',\n            './img/PRODUCTO_PRINCIPAL_GRANDE_ABIERTO.webp',\n        ];"
)

open(path, 'w', encoding='utf-8').write(html)
print('OK: sj-27 fixed')

# ─── sj-40 ────────────────────────────────────────────────────────────────────
print('=== sj-40 ===')
path = rf'{BASE}\sj-40\index.html'
html = open(path, encoding='utf-8').read()

# CAJA.webp -> CAJA_PRINCIPAL.webp everywhere
html = html.replace('./img/CAJA.webp', './img/CAJA_PRINCIPAL.webp')

# Fix WA links: COD:6975069404455 -> MOD: SJ-40
html = html.replace(
    'la%20Sandwichera%20Premium%20COD:%206975069404455',
    'el%20producto%20MOD:%20SJ-40'
)

open(path, 'w', encoding='utf-8').write(html)
print('OK: sj-40 fixed')

# ─── sj-40a ───────────────────────────────────────────────────────────────────
print('=== sj-40a ===')
path = rf'{BASE}\sj-40a\index.html'
html = open(path, encoding='utf-8').read()

# Main img .png -> .webp
html = html.replace(
    'src="./img/PRODUCTO_PRINCIPAL.png"\n                             alt="Panini Maker Metal 850W — HomePower PTY"',
    'src="./img/PRODUCTO_PRINCIPAL.webp"\n                             alt="Panini Maker Metal 850W — HomePower PTY"'
)

# Thumbs: replace single .png with 2 .webp thumbs
old_thumbs40a = '''                    <div class="pdp-thumbs" role="list" aria-label="Imágenes del producto">
                        <button class="pdp-thumb active"
                                onclick="pdpSetImage('./img/PRODUCTO_PRINCIPAL.png', this)"
                                aria-label="Ver imagen principal" role="listitem">
                            <img src="./img/PRODUCTO_PRINCIPAL.png" alt="Vista principal">
                        </button>
                    </div>'''
new_thumbs40a = '''                    <div class="pdp-thumbs" role="list" aria-label="Imágenes del producto">
''' + thumb_btn('./img/PRODUCTO_PRINCIPAL.webp', 'Ver imagen principal', 'Vista principal', active=True) + '\n' + \
thumb_btn('./img/CAJA_PRINCIPAL.webp', 'Ver caja', 'Caja') + '\n' + \
'                    </div>'
html = html.replace(old_thumbs40a, new_thumbs40a)

# Gallery strip: add CAJA_PRINCIPAL at index 1
html = html.replace(old_strip27, f'''                    <div class="pdp-gallery-strip-grid">
{strip_item(1, './img/CAJA_PRINCIPAL.webp', 'Ampliar caja', 'Caja')}
                    </div>''')

# pdpImages: [,] -> full list
html = html.replace(
    '        const pdpImages = [\n            ,\n        ];',
    "        const pdpImages = [\n            './img/PRODUCTO_PRINCIPAL.webp',\n            './img/CAJA_PRINCIPAL.webp',\n        ];"
)

open(path, 'w', encoding='utf-8').write(html)
print('OK: sj-40a fixed')

# ─── sj35 ─────────────────────────────────────────────────────────────────────
print('=== sj35 ===')
path = rf'{BASE}\sj35\index.html'
html = open(path, encoding='utf-8').read()

# Main img .png -> .webp
html = html.replace(
    'src="./img/PRODUCTO_PRINCIPAL.png"\n                             alt="Sandwichera Compacta — HomePower PTY"',
    'src="./img/PRODUCTO_PRINCIPAL.webp"\n                             alt="Sandwichera Compacta — HomePower PTY"'
)

# Thumbs: replace single .png with 2 .webp thumbs
old_thumbs35 = '''                    <div class="pdp-thumbs" role="list" aria-label="Imágenes del producto">
                        <button class="pdp-thumb active"
                                onclick="pdpSetImage('./img/PRODUCTO_PRINCIPAL.png', this)"
                                aria-label="Ver imagen principal" role="listitem">
                            <img src="./img/PRODUCTO_PRINCIPAL.png" alt="Vista principal">
                        </button>
                    </div>'''
new_thumbs35 = '''                    <div class="pdp-thumbs" role="list" aria-label="Imágenes del producto">
''' + thumb_btn('./img/PRODUCTO_PRINCIPAL.webp', 'Ver imagen principal', 'Vista principal', active=True) + '\n' + \
thumb_btn('./img/PRODUCTO_PRINCIPAL_ABIERTO.webp', 'Ver producto abierto', 'Producto abierto') + '\n' + \
'                    </div>'
html = html.replace(old_thumbs35, new_thumbs35)

# Gallery strip: add 2 items
html = html.replace(old_strip27, f'''                    <div class="pdp-gallery-strip-grid">
{strip_item(0, './img/PRODUCTO_PRINCIPAL.webp', 'Ampliar vista principal', 'Vista principal')}
{strip_item(1, './img/PRODUCTO_PRINCIPAL_ABIERTO.webp', 'Ampliar producto abierto', 'Producto abierto')}
                    </div>''')

# pdpImages: [,] -> full list
html = html.replace(
    '        const pdpImages = [\n            ,\n        ];',
    "        const pdpImages = [\n            './img/PRODUCTO_PRINCIPAL.webp',\n            './img/PRODUCTO_PRINCIPAL_ABIERTO.webp',\n        ];"
)

open(path, 'w', encoding='utf-8').write(html)
print('OK: sj35 fixed')

print('\nDone. All 6 sandwichera product pages fixed.')
