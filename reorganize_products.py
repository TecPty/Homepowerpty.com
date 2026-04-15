#!/usr/bin/env python3
"""
reorganize_products.py — Migra productos/ plano → productos/categoria/sku/

Cambios que aplica:
  1. Mueve cada carpeta de producto a su nueva ubicación categórica
  2. Actualiza las rutas ../../ → ../../../ en cada index.html de producto
  3. Actualiza todos los hrefs/srcs en el index.html principal
  4. Productos con mismo SKU (2020B): el primero en el mapa gana, el duplicado
     se mueve a productos/_para-revisar/ para revisión manual

Uso:
  python reorganize_products.py --dry-run   # preview sin tocar nada
  python reorganize_products.py             # migración real
"""

import os
import shutil
import sys

BASE      = os.path.dirname(os.path.abspath(__file__))
PRODUCTOS = os.path.join(BASE, "productos")
INDEX     = os.path.join(BASE, "index.html")

# ── Mapa completo: carpeta_actual → (categoría, slug_nuevo) ────────────────
# Para duplicados: el PRIMERO en el mapa es el que queda; el segundo se archiva.
MAPPING = {
    # Freidoras de aire
    "air-fryer-3l-AF3201":                   ("freidoras-de-aire", "af3201"),
    "air-fryer-4-5l-JD389":                  ("freidoras-de-aire", "jd389"),
    "freidora-aire-blanca-OC-506":           ("freidoras-de-aire", "oc-506"),
    # Licuadoras
    "licuadora-3v-glass-MM-111":             ("licuadoras",        "mm-111"),
    "licuadora-azul-MM-931":                 ("licuadoras",        "mm-931"),
    "licuadora-chocolate-MM-933":            ("licuadoras",        "mm-933"),
    "licuadora-vb999-VB-999":               ("licuadoras",        "vb-999"),
    # Batidoras
    "batidora-pedestal-HP-024":              ("batidoras",         "hp-024"),
    "batidora-mano-HP-044":                  ("batidoras",         "hp-044"),
    "batidora-mano-metal-HP-045":            ("batidoras",         "hp-045"),
    # Cafeteras
    "cafetera-6-tazas-WJ-9008":             ("cafeteras",         "wj-9008"),
    "cafetera-6t-v2-WJ-9001":              ("cafeteras",         "wj-9001"),
    "cafetera-7-5-tazas-WJ-9011":          ("cafeteras",         "wj-9011"),
    "cafetera-12-tazas-WJ-9009":           ("cafeteras",         "wj-9009"),
    "cafetera-12t-cm02-CM02":              ("cafeteras",         "cm02"),
    "cafetera-12t-v2-WJ-9002":             ("cafeteras",         "wj-9002"),
    # Percoladoras
    "cafetera-percoladora-30t-HP-046":     ("percoladoras",      "hp-046"),
    "cafetera-percoladora-40t-HP-047":     ("percoladoras",      "hp-047"),
    "cafetera-percoladora-50t-HP-048":     ("percoladoras",      "hp-048"),
    "cafetera-percoladora-100t-HP-049":    ("percoladoras",      "hp-049"),
    # Estufas eléctricas
    "estufa-electrica-1-quemador-1010A":   ("estufas",           "1010a"),
    "estufa-electrica-2q-negra-2020A":     ("estufas",           "2020a"),
    "estufa-electrica-1q-premium-F-010E-1":("estufas",           "f-010e-1"),
    "estufa-electrica-doble-F-010E-1":     ("estufas",           "f-010e-1-doble"),
    # Estufas 2020B — NEGRA es la página principal, BLANCA se archiva
    "estufa-2-quemadores-negra-2020B":     ("estufas",           "2020b"),  # ← queda
    "estufa-2-quemadores-blanca-2020B":    ("estufas",           "2020b"),  # ← archivado
    # Estufas de gas
    "estufa-gas-2-quemadores-2050A":       ("estufas",           "2050a"),
    "estufa-gas-2q-v2-3080":              ("estufas",           "3080"),
    "estufa-gas-3-quemadores-3076K":       ("estufas",           "3076k"),
    "estufa-gas-3q-v2-3081K":             ("estufas",           "3081k"),
    "estufa-gas-4q-horno-HP-073":          ("estufas",           "hp-073"),
    # Arroceras
    "arrocera-0-3l-HT-03":               ("arroceras",          "ht-03"),
    "arrocera-1-5l-HT-15A":              ("arroceras",          "ht-15a"),
    "arrocera-1-8l-HT-18A":              ("arroceras",          "ht-18a"),
    "arrocera-2-2l-basica-HT-22":        ("arroceras",          "ht-22"),
    "arrocera-vaporera-2-2l-HT-22A":     ("arroceras",          "ht-22a"),
    # Ollas a presión
    "olla-presion-3-2l-CK-02-18":        ("ollas",              "ck-02-18"),
    "olla-presion-4-2l-CK-02-20":        ("ollas",              "ck-02-20"),
    "olla-presion-5l-CK-02-22":          ("ollas",              "ck-02-22"),
    "olla-presion-7l-CK-02-24":          ("ollas",              "ck-02-24"),
    "olla-presion-9l-CK-02-26":          ("ollas",              "ck-02-26"),
    # Sandwicheras / Panini
    "sandwichera-clasica-SJ-22":         ("sandwicheras",       "sj-22"),
    "sandwichera-metal-SJ-24":           ("sandwicheras",       "sj-24"),
    "sandwichera-grill-SJ-27":           ("sandwicheras",       "sj-27"),
    "sandwichera-sj35-SJ35":             ("sandwicheras",       "sj35"),
    "sandwichera-premium-SJ-40":         ("sandwicheras",       "sj-40"),
    "panini-metal-SJ-40A":               ("sandwicheras",       "sj-40a"),
    # Planchas
    "plancha-seco-R-91261":              ("planchas",           "r-91261"),
    "plancha-seco-premium-R-1808B":      ("planchas",           "r-1808b"),
    "plancha-vapor-hp012-HP012":         ("planchas",           "hp012"),
    "plancha-vapor-r91171b-R91171B":     ("planchas",           "r91171b"),
    "plancha-vapor-premium-R-92003":     ("planchas",           "r-92003"),
    # Teteras
    "tetera-plastico-1-5l-H208":         ("teteras",            "h208"),
    "tetera-1-8l-JR-A101":              ("teteras",            "jr-a101"),
    "tetera-premium-JR-LD8":             ("teteras",            "jr-ld8"),
    # Tostadoras
    "tostadora-2-rebanadas-HP-017":      ("tostadoras",         "hp-017"),
    "tostadora-metal-HP-018":            ("tostadoras",         "hp-018"),
    # Hornitos
    "hornito-23l-PN-09":                 ("hornitos",           "pn-09"),
    # Otros
    "lochera-termica-JY-1001":           ("otros",              "jy-1001"),
}


def update_product_html(html_path: str) -> None:
    """Actualiza rutas relativas en el index.html del producto.
    
    Los productos pasan de estar a 2 niveles de profundidad (productos/slug/)
    a 3 niveles (productos/categoria/sku/), así que ../../ → ../../../
    """
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    updated = content.replace("../../", "../../../")
    with open(html_path, "w", encoding="utf-8", newline="") as f:
        f.write(updated)


def run(dry_run: bool = False) -> None:
    archive_dir = os.path.join(PRODUCTOS, "_para-revisar")
    moved_targets: set[str] = set()   # evita doble-move del mismo destino
    
    link_map: dict[str, str] = {}
    archived_folders: list[str] = []

    # ── Fase 1: mover carpetas ──────────────────────────────────────────────
    print("=" * 60)
    print("FASE 1 — Moviendo carpetas de producto")
    print("=" * 60)

    for old_folder, (category, slug) in MAPPING.items():
        old_path = os.path.join(PRODUCTOS, old_folder)
        new_path = os.path.join(PRODUCTOS, category, slug)
        old_link = f"productos/{old_folder}/"
        new_link = f"productos/{category}/{slug}/"

        if not os.path.exists(old_path):
            print(f"  SKIP  (no existe): {old_folder}")
            link_map[old_link] = new_link  # igual actualizamos el link
            continue

        # Destino ya existe → es un duplicado (ej. 2020B blanca vs negra)
        if new_path in moved_targets or os.path.exists(new_path):
            archive_path = os.path.join(archive_dir, old_folder)
            archived_folders.append(old_folder)
            print(f"  ARCHIVO (duplicado): {old_folder} -> _para-revisar/{old_folder}")
            if not dry_run:
                os.makedirs(archive_dir, exist_ok=True)
                shutil.move(old_path, archive_path)
            # En el index.html este link apunta a la página principal del merge
            link_map[old_link] = new_link
            continue

        print(f"  MOVE: {old_folder}")
        print(f"        -> productos/{category}/{slug}/")
        if not dry_run:
            os.makedirs(os.path.join(PRODUCTOS, category), exist_ok=True)
            shutil.move(old_path, new_path)
            prod_html = os.path.join(new_path, "index.html")
            if os.path.exists(prod_html):
                update_product_html(prod_html)

        moved_targets.add(new_path)
        link_map[old_link] = new_link

    # ── Fase 2: actualizar index.html principal ─────────────────────────────
    print()
    print("=" * 60)
    print("FASE 2 — Actualizando links en index.html")
    print("=" * 60)

    with open(INDEX, "r", encoding="utf-8") as f:
        content = f.read()

    changes = 0
    for old_link, new_link in link_map.items():
        count = content.count(old_link)
        if count:
            content = content.replace(old_link, new_link)
            print(f"  {old_link}")
            print(f"    -> {new_link}  ({count}x)")
            changes += count

    if not dry_run:
        with open(INDEX, "w", encoding="utf-8", newline="") as f:
            f.write(content)

    # ── Resumen ─────────────────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("RESUMEN")
    print("=" * 60)
    print(f"  Carpetas movidas:       {len(moved_targets)}")
    print(f"  Archivados (duplicado): {len(archived_folders)}")
    print(f"  Links actualizados:     {changes}")
    if archived_folders:
        print()
        print("  Carpetas en _para-revisar/ (revisar manualmente):")
        for f in archived_folders:
            print(f"    - {f}")
    if dry_run:
        print()
        print("  *** DRY RUN — no se tocó nada ***")
    print()
    print("Listo.")


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    if dry:
        print("=== DRY RUN — preview sin cambios ===\n")
    run(dry_run=dry)
