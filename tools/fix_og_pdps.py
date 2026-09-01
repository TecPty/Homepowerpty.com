#!/usr/bin/env python3
"""
Fix OG image en todos los PDPs: reemplaza rutas relativas por URLs absolutas.
Tambien corrige og:site_name, og:locale y twitter:image si existen.
"""
import os
import re

BASE_URL = "https://www.homepowerpty.com"
PRODUCTOS_DIR = "productos"

fixed = 0
skipped = 0
errors = 0

for categoria in sorted(os.listdir(PRODUCTOS_DIR)):
    cat_path = os.path.join(PRODUCTOS_DIR, categoria)
    if not os.path.isdir(cat_path):
        continue
    for sku in sorted(os.listdir(cat_path)):
        index_path = os.path.join(cat_path, sku, "index.html")
        if not os.path.isfile(index_path):
            continue
        try:
            with open(index_path, "r", encoding="utf-8") as f:
                content = f.read()

            original = content

            # URL absoluta para og:image y twitter:image del producto
            cat_encoded = categoria.replace(" ", "%20")
            sku_encoded  = sku.replace(" ", "%20")
            abs_img = f"{BASE_URL}/productos/{cat_encoded}/{sku_encoded}/img/PRODUCTO_PRINCIPAL.webp"

            # Reemplazar og:image relativa
            content = re.sub(
                r'(<meta\s+property="og:image"\s+content=")(?!https?://)([^"]+)(")',
                rf'\g<1>{abs_img}\g<3>',
                content
            )

            # Reemplazar twitter:image relativa
            content = re.sub(
                r'(<meta\s+name="twitter:image"\s+content=")(?!https?://)([^"]+)(")',
                rf'\g<1>{abs_img}\g<3>',
                content
            )

            # Corregir og:site_name si es incorrecto
            content = re.sub(
                r'(<meta\s+property="og:site_name"\s+content=")[^"]*(")',
                r'\g<1>Home Power PTY\g<2>',
                content
            )

            # Corregir og:locale a es_PA
            content = re.sub(
                r'(<meta\s+property="og:locale"\s+content=")es_ES(")',
                r'\g<1>es_PA\g<2>',
                content
            )

            if content != original:
                with open(index_path, "w", encoding="utf-8") as f:
                    f.write(content)
                fixed += 1
            else:
                skipped += 1

        except Exception as e:
            errors += 1
            print(f"ERROR {index_path}: {e}")

print(f"[OK] OG fix completado")
print(f"   Corregidos : {fixed}")
print(f"   Sin cambios: {skipped}")
print(f"   Errores    : {errors}")
