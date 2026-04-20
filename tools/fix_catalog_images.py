"""
fix_catalog_images.py
Corrige las referencias de imágenes en index.html para que apunten
a los archivos que realmente existen en cada carpeta img/.
"""

import re

INDEX_PATH = r"C:\Users\HP 15\Homepowerpty.com\index.html"

# Cada tupla: (old_src, new_src)
FIXES = [
    # ── LICUADORAS ─────────────────────────────────────────────────────────
    # vb-999  (tarjeta en sección superior y catálogo)
    (
        'productos/licuadoras/vb-999/img/PRODUCTO_PRINCIPAL.webp',
        'productos/licuadoras/vb-999/img/PRODUCTO_PRINCIPAL_PRINCIPAL_GRIS.png',
    ),
    # mm-111
    (
        'productos/licuadoras/mm-111/img/PRODUCTO_PRINCIPAL.webp',
        'productos/licuadoras/mm-111/img/PRODUCTO_PRINCIPAL_PRINCIPAL_GRIS.png',
    ),
    (
        'productos/licuadoras/mm-111/img/CAJA.webp',
        'productos/licuadoras/mm-111/img/CAJA_NEGRO.png',
    ),
    # mm-933
    (
        'productos/licuadoras/mm-933/img/PRODUCTO_PRINCIPAL.webp',
        'productos/licuadoras/mm-933/img/PRODUCTO_PRINCIPAL_PRINCIPAL_GRIS.webp',
    ),
    (
        'productos/licuadoras/mm-933/img/CAJA.webp',
        'productos/licuadoras/mm-933/img/CAJA_GRIS.webp',
    ),
    # mm-931
    (
        'productos/licuadoras/mm-931/img/PRODUCTO_PRINCIPAL.webp',
        'productos/licuadoras/mm-931/img/PRODUCTO_PRINCIPAL_PRINCIPAL_ROJO.png',
    ),
    (
        'productos/licuadoras/mm-931/img/CAJA.webp',
        'productos/licuadoras/mm-931/img/CAJA_NEGRO.webp',
    ),

    # ── CAFETERAS ──────────────────────────────────────────────────────────
    # Archivos reales son .png pero el index pedía .webp
    (
        'productos/cafeteras/cm02/img/PRODUCTO_PRINCIPAL.webp',
        'productos/cafeteras/cm02/img/PRODUCTO_PRINCIPAL.png',
    ),
    (
        'productos/cafeteras/wj-9001/img/PRODUCTO_PRINCIPAL.webp',
        'productos/cafeteras/wj-9001/img/PRODUCTO_PRINCIPAL.png',
    ),
    (
        'productos/cafeteras/wj-9002/img/PRODUCTO_PRINCIPAL.webp',
        'productos/cafeteras/wj-9002/img/PRODUCTO_PRINCIPAL.png',
    ),
    (
        'productos/cafeteras/wj-9011/img/PRODUCTO_PRINCIPAL.webp',
        'productos/cafeteras/wj-9011/img/PRODUCTO_PRINCIPAL.png',
    ),
    (
        'productos/cafeteras/wj-9008/img/PRODUCTO_PRINCIPAL.webp',
        'productos/cafeteras/wj-9008/img/PRODUCTO_PRINCIPAL.png',
    ),
    (
        'productos/cafeteras/wj-9009/img/PRODUCTO_PRINCIPAL.webp',
        'productos/cafeteras/wj-9009/img/PRODUCTO_PRINCIPAL.png',
    ),

    # ── ARROCERAS ──────────────────────────────────────────────────────────
    # Los archivos tienen sufijo de capacidad, el index pedía genérico .webp
    (
        'productos/arroceras/ht-03/img/PRODUCTO_PRINCIPAL.webp',
        'productos/arroceras/ht-03/img/PRODUCTO_PRINCIPAL_0.3.png',
    ),
    (
        'productos/arroceras/ht-15/img/PRODUCTO_PRINCIPAL.webp',
        'productos/arroceras/ht-15/img/PRODUCTO_PRINCIPAL_1.5.png',
    ),
    (
        'productos/arroceras/ht-18a/img/PRODUCTO_PRINCIPAL.webp',
        'productos/arroceras/ht-18a/img/PRODUCTO_PRINCIPAL_1.8A.png',
    ),
    (
        'productos/arroceras/ht-18/img/PRODUCTO_PRINCIPAL.webp',
        'productos/arroceras/ht-18/img/PRODUCTO_PRINCIPAL_1.8.png',
    ),
    (
        'productos/arroceras/ht-22/img/PRODUCTO_PRINCIPAL.webp',
        'productos/arroceras/ht-22/img/PRODUCTO_PRINCIPAL_2.2.png',
    ),
    # ht-15a  (segunda sección del catálogo)
    (
        'productos/arroceras/ht-15a/img/PRODUCTO_PRINCIPAL.webp',
        'productos/arroceras/ht-15a/img/PRODUCTO_PRINCIPAL_1.5A.png',
    ),
    (
        'productos/arroceras/ht-15a/img/CAJA.webp',
        'productos/arroceras/ht-15a/img/CAJA_1.5A.png',
    ),
    # ht-22a
    (
        'productos/arroceras/ht-22a/img/PRODUCTO_PRINCIPAL.webp',
        'productos/arroceras/ht-22a/img/PRODUCTO_PRINCIPAL_2.2A.png',
    ),
    (
        'productos/arroceras/ht-22a/img/CAJA.webp',
        'productos/arroceras/ht-22a/img/CAJA_2.2A.png',
    ),
]

with open(INDEX_PATH, encoding="utf-8") as f:
    html = f.read()

total = 0
for old, new in FIXES:
    count = html.count(old)
    if count == 0:
        print(f"[SKIP – no encontrado] {old}")
        continue
    html = html.replace(old, new)
    print(f"[OK x{count}] {old.split('/')[-1]} → {new.split('/')[-1]}")
    total += count

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\n✓ {total} referencias actualizadas en index.html")
