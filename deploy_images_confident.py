"""
deploy_images_confident.py
--------------------------
Copia y convierte imágenes desde PRODUCTOS-IMAGENES/PRODUCTOS/ a las carpetas
correctas de productos. Solo trabaja con mappings 100% seguros y carpetas vacías.

Uso:
    python deploy_images_confident.py           # ejecución real
    python deploy_images_confident.py --dry-run # solo muestra qué haría
"""

import sys
import shutil
from pathlib import Path
from PIL import Image

DRY_RUN = "--dry-run" in sys.argv

SRC_DIR = Path("PRODUCTOS-IMAGENES/PRODUCTOS")
PRODUCTOS_DIR = Path("productos")

# ---------------------------------------------------------------------------
# Mappings 100% seguros
# Formato: (nombre_imagen_fuente, categoria/sku, nombre_destino_sin_ext)
#
# Criterio de "seguro":
#   - El nombre del producto destino es único en el catálogo (un solo SKU posible)
#   - La carpeta img/ está vacía o solo contiene archivos que sabemos a qué
#     producto pertenecen
# ---------------------------------------------------------------------------
CONFIDENT_MAPPINGS = [
    # AIR FRYER 3L (AF3201) — único air fryer con ese nombre exacto
    ("AIR FRYER.png",               "freidoras-de-aire/af3201", "PRODUCTO_PRINCIPAL"),
    ("AIR FRYER CAJA.png",          "freidoras-de-aire/af3201", "CAJA"),

    # OLLA A PRESIÓN — imagen compartida por las 5 ollas (misma olla, distintos tamaños)
    ("OLLA PRESION.png",            "ollas/ck-02-18",           "PRODUCTO_PRINCIPAL"),
    ("OLLA PRESION CAJA.png",       "ollas/ck-02-18",           "CAJA"),
    ("OLLA PRESION.png",            "ollas/ck-02-20",           "PRODUCTO_PRINCIPAL"),
    ("OLLA PRESION CAJA.png",       "ollas/ck-02-20",           "CAJA"),
    ("OLLA PRESION.png",            "ollas/ck-02-26",           "PRODUCTO_PRINCIPAL"),
    ("OLLA PRESION CAJA.png",       "ollas/ck-02-26",           "CAJA"),

    # TOSTADORA METAL (HP-018) — única tostadora vacía; hp-017 ya tiene imágenes
    ("TOSTADORA.png",               "tostadoras/hp-018",        "PRODUCTO_PRINCIPAL"),
    ("TOSTADORA CAJA.png",          "tostadoras/hp-018",        "CAJA"),

    # ARROCERA VAPOR → ht-18a (1.8L con vapor, vacía; ht-22a=2.2L vapor ya tiene imágenes)
    ("ARROCERA VAPOR.png",          "arroceras/ht-18a",         "PRODUCTO_PRINCIPAL"),
    ("ARROCERA VAPOR CAJA.png",     "arroceras/ht-18a",         "CAJA"),

    # ARROCERA básica → ht-22 (2.2L sin recubrimiento, sin vapor, vacía)
    ("ARROCERA.png",                "arroceras/ht-22",          "PRODUCTO_PRINCIPAL"),
    ("ARROCERA CAJA.png",           "arroceras/ht-22",          "CAJA"),

    # LONCHERA ELÉCTRICA (JY-1001) — nombre del archivo lo indica directamente
    ("lonchera foto.png",           "otros/jy-1001",            "PRODUCTO_PRINCIPAL"),
    ("caja lonchera.png",           "otros/jy-1001",            "CAJA"),

    # ESTUFA ELÉCTRICA DOBLE (F-010E-1) — usuario confirmó: DOBLE → f-010e-1
    # f-010e-1-doble era carpeta duplicada, se elimina
    ("ESTUFA ELECTRICA DOBLE BLANCA.png",      "estufas/f-010e-1", "PRODUCTO_PRINCIPAL"),
    ("ESTUFA ELECTRICA DOBLE BLANCA CAJA.png", "estufas/f-010e-1", "CAJA"),
    ("ESTUFA ELECTRICA DOBLE NEGRA.png",       "estufas/f-010e-1", "PRODUCTO_PRINCIPAL_NEGRA"),
    ("ESTUFA ELECTRICA DOBLE NEGRA CAJA.png",  "estufas/f-010e-1", "CAJA_NEGRA"),

    # TETERA PLÁSTICO 1.5L (H208) — usuario confirmó: compacta y plegable → h208
    ("Tetera eléctrica compacta y plegable.png", "teteras/h208", "PRODUCTO_PRINCIPAL"),
]

# NO desplegados por falta de imagen fuente:
#   arroceras/ht-03 (Mini 0.3L) — sin imagen específica en PRODUCTOS-IMAGENES
#   percoladoras/hp-046/047/048/049 — sin imágenes en PRODUCTOS-IMAGENES

# Ollas ck-02-22 y ck-02-24 ya tienen imágenes — no se tocan.

# ---------------------------------------------------------------------------
# Productos que ya tienen imágenes — se dejan intactos aunque tengamos
# imágenes candidatas (esperamos clarificación del usuario antes de reemplazar)
# ---------------------------------------------------------------------------
ALREADY_HAS_IMAGES = [
    # arroceras
    "arroceras/ht-15a",   # 6 archivos
    "arroceras/ht-22a",   # 6 archivos
    # cafeteras
    "cafeteras/wj-9008",  # 5 archivos
    "cafeteras/wj-9009",  # 6 archivos
    # estufas
    "estufas/2020b",      # 6 archivos
    "estufas/2050a",      # 2 archivos
    "estufas/3076k",      # 2 archivos
    # estufas/f-010e-1-doble eliminada (carpeta duplicada — skus merge a f-010e-1)
    # freidoras
    "freidoras-de-aire/jd389",   # 6 archivos
    "freidoras-de-aire/oc-506",  # 6 archivos
    # hornitos
    "hornitos/pn-09",     # 6 archivos
    # licuadoras
    "licuadoras/mm-111",  # 5 archivos
    "licuadoras/mm-931",  # 2 archivos
    "licuadoras/mm-933",  # 2 archivos
    "licuadoras/vb-999",  # 2 archivos
    # ollas
    "ollas/ck-02-22",     # 2 archivos
    "ollas/ck-02-24",     # 2 archivos
    # planchas
    "planchas/r-1808b",   # 6 archivos
    "planchas/r-91261",   # 6 archivos
    "planchas/r-92003",   # 6 archivos
    # sandwicheras
    "sandwicheras/sj-22", # 6 archivos
    "sandwicheras/sj-24", # 6 archivos
    "sandwicheras/sj-40", # 2 archivos
    # teteras
    "teteras/jr-a101",    # 6 archivos
    "teteras/jr-ld8",     # 6 archivos
    # tostadoras
    "tostadoras/hp-017",  # 2 archivos
]


def convert_and_copy(src_path: Path, dest_path: Path):
    """Convierte PNG a WebP y guarda en dest_path (.webp)."""
    with Image.open(src_path) as img:
        img.save(dest_path, "WEBP", quality=90, method=6)


def main():
    mode_label = "[DRY RUN]" if DRY_RUN else "[DEPLOY]"
    print(f"\n{mode_label} deploy_images_confident.py")
    print("=" * 60)

    results = {"ok": [], "skipped_exists": [], "skipped_no_src": [], "error": []}

    for src_name, sku_path, dest_name in CONFIDENT_MAPPINGS:
        src_file = SRC_DIR / src_name
        dest_dir = PRODUCTOS_DIR / sku_path / "img"
        dest_file = dest_dir / f"{dest_name}.webp"

        # Verificar fuente
        if not src_file.exists():
            print(f"  ✗ FUENTE NO ENCONTRADA: {src_name}")
            results["skipped_no_src"].append(src_name)
            continue

        # Verificar destino
        if dest_file.exists():
            print(f"  ~ Ya existe, se omite: {sku_path}/img/{dest_name}.webp")
            results["skipped_exists"].append(str(dest_file))
            continue

        # Crear carpeta si no existe
        if not DRY_RUN:
            dest_dir.mkdir(parents=True, exist_ok=True)

        print(f"  ✓ {src_name}  →  {sku_path}/img/{dest_name}.webp")

        if not DRY_RUN:
            try:
                convert_and_copy(src_file, dest_file)
                results["ok"].append(str(dest_file))
            except Exception as e:
                print(f"    ERROR: {e}")
                results["error"].append(str(dest_file))
        else:
            results["ok"].append(str(dest_file))

    print()
    print("─" * 60)
    print(f"  Desplegadas : {len(results['ok'])}")
    print(f"  Ya existían : {len(results['skipped_exists'])}")
    print(f"  Sin fuente  : {len(results['skipped_no_src'])}")
    print(f"  Errores     : {len(results['error'])}")
    print()

    if results["skipped_no_src"]:
        print("FUENTES NO ENCONTRADAS:")
        for f in results["skipped_no_src"]:
            print(f"  - {f}")
        print()

    print("─" * 60)
    print("OMITIDOS (requieren clarificación del usuario):")
    ambiguous = [
        "Estufas eléctricas: INDIVIDUAL / UNA / DOS / 2  →  1010a / 2020a  (DOBLE→f-010e-1 ya deployado)",
        "Estufas de gas: DOS / TRES  →  2050a+3080 / 3076k+3081k / hp-073",
        "Cafeteras: 6 TAZAS / 12 TAZAS (3 imgs)  →  wj-9001 / wj-9002 / cm02 / wj-9011",
        "Freidoras de aire: #1 / #2  →  jd389 vs oc-506 (ambas YA tienen imágenes)",
        "Arrocera: ht-03 (Mini 0.3L) — sin imagen fuente específica",
        "Licuadoras: VERDE 2 / NEGRA 3 / ROJA 3 / BLANCA 4 / CREMA  →  ¿qué SKU?",
        "Batidoras: mano (hp-044/hp-045) / pedestal (hp-024)  →  3 imgs para 3 SKUs",
        "Planchas: VAPOR / VAPOR 2  →  hp012 vs r91171b (ambas vapor 1400W)",
        "Planchas: SECO 2 (SECO ya fue a r-91261 que tiene imgs)  →  ¿a cuál?",
        "Teteras: ELECTRICA / ELECTRICA 2  →  jr-a101 / jr-ld8 (ambas ya tienen imgs; h208 compacta ya deployada)",
        "Sandwicheras: #1 / #2 / grande / mediana  →  sj-27 / sj35 / sj-40a",
        "Percoladoras: hp-046/047/048/049  →  SIN imágenes en PRODUCTOS-IMAGENES",
        "Productos nuevos: extensiones, cables, regletas, cortador  →  sin carpetas aún",
    ]
    for item in ambiguous:
        print(f"  ⚠  {item}")

    if DRY_RUN:
        print()
        print("Ejecutá sin --dry-run para aplicar los cambios.")


if __name__ == "__main__":
    main()
