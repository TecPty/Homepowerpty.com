"""
Corrige referencias de imágenes en las páginas de licuadoras.
Reemplaza nombres genéricos (PRODUCTO_PRINCIPAL.webp, CAJA.webp)
por los archivos reales que existen en cada carpeta img/.
"""
from pathlib import Path

BASE = Path('productos/licuadoras')

FIXES = {
    'mm-111': {
        './img/PRODUCTO_PRINCIPAL.webp': './img/PRODUCTO_PRINCIPAL_NEGRO.png',
        './img/CAJA.webp':              './img/CAJA_NEGRO.png',
        # Estos no existen — remover los thumbnails del gallery strip
        './img/LIFESTYLE_DARK.png':     None,
        './img/LIFESTYLE_KITCHEN.png':  None,
        './img/DETAIL_LOGO.png':        None,
    },
    'mm-931': {
        './img/PRODUCTO_PRINCIPAL.webp': './img/PRODUCTO_PRINCIPAL_NEGRO.webp',
        './img/CAJA.webp':              './img/CAJA_NEGRO.webp',
    },
    'mm-933': {
        './img/PRODUCTO_PRINCIPAL.webp': './img/PRODUCTO_PRINCIPAL_AZUL.webp',
        './img/CAJA.webp':              './img/CAJA_AZUL.webp',
    },
    'vb-999': {
        './img/PRODUCTO_PRINCIPAL.webp': './img/PRODUCTO_PRINCIPAL_ROJO.png',
        './img/CAJA.webp':              './img/CAJA_ROJO.png',
    },
}

import re

for sku, replacements in FIXES.items():
    path = BASE / sku / 'index.html'
    if not path.exists():
        print(f'  ⚠️  No encontrado: {path}')
        continue

    html = path.read_text(encoding='utf-8')
    original = html

    for old, new in replacements.items():
        if new is None:
            # Eliminar el bloque <div class="pdp-strip-item"> o <button class="pdp-thumb"> que contenga esta imagen
            # Patrón para pdp-thumb button
            html = re.sub(
                r'<button class="pdp-thumb[^"]*"[^>]*>[\s\S]*?' + re.escape(old) + r'[\s\S]*?</button>\s*',
                '', html
            )
            # Patrón para pdp-strip-item div
            html = re.sub(
                r'<div class="pdp-strip-item"[^>]*>[\s\S]*?' + re.escape(old) + r'[\s\S]*?</div>\s*',
                '', html
            )
        else:
            count = html.count(old)
            html = html.replace(old, new)
            print(f'  [{sku}] {old} → {new} ({count}x)')

    if html != original:
        path.write_text(html, encoding='utf-8')
        print(f'  ✅ {sku} actualizado')
    else:
        print(f'  — {sku} sin cambios')

print('\nDone.')
