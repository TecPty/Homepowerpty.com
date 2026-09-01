#!/usr/bin/env python3
"""
sync_galleries.py
=================
Convierte PNGs a WebP y sincroniza la galería de cada producto con
las imágenes reales que hay en su carpeta img/.

Uso:
  python sync_galleries.py                      # todos los productos
  python sync_galleries.py extensiones          # solo esa categoría
  python sync_galleries.py extensiones/hp-061   # solo ese producto

Qué hace por cada producto:
  1. Convierte cualquier PNG en img/ a WebP (quality=88) y borra el PNG
  2. Escanea los WebPs existentes y los ordena
  3. Actualiza el index.html:
       - Imagen principal (pdpMainImg)
       - Thumbnails (pdp-thumbs)
       - Galería inferior (pdp-gallery-strip-grid)
       - Array del lightbox (pdpImages)
       - Imagen inicial del lightbox
"""

import re
import sys
from pathlib import Path

try:
    from PIL import Image
    PIL_OK = True
except ImportError:
    PIL_OK = False
    print("WARNING: Pillow no instalado. Los PNGs no se convertirán.")
    print("         Instalá con:  pip install Pillow\n")

ROOT = Path(__file__).parent

STRIP_SVG = (
    '<svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.5" '
    'viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/>'
    '<line x1="21" y1="21" x2="16.65" y2="16.65"/>'
    '<line x1="11" y1="8" x2="11" y2="14"/>'
    '<line x1="8" y1="11" x2="14" y2="11"/></svg>'
)

# ─── Ordenamiento ─────────────────────────────────────────────────────────────

def sort_key(stem: str) -> tuple:
    s = stem.upper()
    if s == 'PRODUCTO_PRINCIPAL':
        return (0, 0, s)
    if s.startswith('PRODUCTO_PRINCIPAL'):
        return (1, 0, s)
    if s.startswith('DETAIL_'):
        num_str = s[7:].split('_')[0]
        try:
            return (2, int(num_str), s)
        except ValueError:
            return (2, 999, s)
    return (3, 0, s)


# ─── Alt text ─────────────────────────────────────────────────────────────────

ALT_MAP = {
    'PRODUCTO_PRINCIPAL':       'Vista principal',
    'PRODUCTO_PRINCIPAL_BLANCO':'Variante blanca',
    'PRODUCTO_PRINCIPAL_NEGRO': 'Variante negra',
    'PRODUCTO_PRINCIPAL_WHITE': 'Variante blanca',
    'PRODUCTO_PRINCIPAL_BLACK': 'Variante negra',
}

def alt_text(stem: str) -> str:
    s = stem.upper()
    if s in ALT_MAP:
        return ALT_MAP[s]
    if s.startswith('DETAIL_'):
        num = s[7:].split('_')[0]
        return f'Detalle {num}'
    return stem.replace('_', ' ').title()


# ─── Conversión PNG → WebP ────────────────────────────────────────────────────

def convert_pngs(img_dir: Path) -> list:
    if not PIL_OK:
        return []
    done = []
    for png in sorted(img_dir.glob('*.png')):
        webp = png.with_suffix('.webp')
        try:
            with Image.open(png) as im:
                mode = 'RGBA' if im.mode in ('RGBA', 'LA', 'P') else 'RGB'
                im.convert(mode).save(webp, 'WEBP', quality=88, method=6)
            png.unlink()
            done.append(png.name)
        except Exception as e:
            print(f'    ERR convirtiendo {png.name}: {e}')
    return done


def get_images(img_dir: Path) -> list:
    imgs = list(img_dir.glob('*.webp'))
    return sorted(imgs, key=lambda p: sort_key(p.stem))


# ─── Construcción de HTML ─────────────────────────────────────────────────────

def make_thumbs(images: list) -> str:
    PAD  = '                    '   # 20 sp — nivel del div
    PAD2 = PAD + '    '             # 24 sp — nivel del button
    PAD3 = PAD2 + '    '           # 28 sp — nivel del img

    lines = [f'{PAD}<div class="pdp-thumbs" role="list" aria-label="Imágenes del producto">']
    for i, img in enumerate(images):
        src   = f'./img/{img.name}'
        alt   = alt_text(img.stem)
        active = ' active' if i == 0 else ''
        lines += [
            f'{PAD2}<button class="pdp-thumb{active}"',
            f'{PAD2}        onclick="pdpSetImage(\'{src}\', this)"',
            f'{PAD2}        aria-label="Ver {alt.lower()}" role="listitem">',
            f'{PAD3}<img src="{src}" alt="{alt}">',
            f'{PAD2}</button>',
        ]
    lines.append(f'{PAD}</div>')
    return '\n'.join(lines)


def make_strip(images: list) -> str:
    PAD  = '                    '   # 20 sp
    PAD2 = PAD + '    '             # 24 sp
    PAD3 = PAD2 + '    '           # 28 sp

    lines = [f'{PAD}<div class="pdp-gallery-strip-grid">']
    for i, img in enumerate(images):
        src = f'./img/{img.name}'
        alt = alt_text(img.stem)
        lines += [
            f'{PAD2}<div class="pdp-strip-item" onclick="pdpOpenLightboxAt({i})" '
            f'role="button" tabindex="0" aria-label="Ampliar {alt.lower()}">',
            f'{PAD3}<img src="{src}" alt="{alt}" loading="lazy">',
            f'{PAD3}<div class="pdp-strip-overlay" aria-hidden="true">{STRIP_SVG}</div>',
            f'{PAD2}</div>',
        ]
    lines.append(f'{PAD}</div>')
    return '\n'.join(lines)


def make_array(images: list) -> str:
    entries = '\n'.join(f"            './img/{img.name}'," for img in images)
    return f'        const pdpImages = [\n{entries}\n        ];'


# ─── Reemplazo de bloques div ─────────────────────────────────────────────────

def find_div_end(content: str, start: int) -> int:
    """Devuelve el índice justo después del </div> que cierra el div en `start`."""
    depth = 0
    i = start
    n = len(content)
    while i < n:
        c4  = content[i:i+4].lower()
        c6  = content[i:i+6].lower()
        if c4 == '<div':
            next_ch = content[i+4:i+5]
            if next_ch in ('>', ' ', '\t', '\n', '\r', '/'):
                depth += 1
        elif c6 == '</div>':
            depth -= 1
            if depth == 0:
                return i + 6
        i += 1
    return -1


def replace_div_by_class(content: str, css_class: str, replacement: str) -> str:
    pattern = re.compile(
        r'<div\s[^>]*class="' + re.escape(css_class) + r'"[^>]*>',
        re.DOTALL
    )
    m = pattern.search(content)
    if not m:
        return content
    start = m.start()
    end = find_div_end(content, start)
    if end == -1:
        return content
    # Expand start to the beginning of the line so leading whitespace is replaced
    # by the indentation already embedded in `replacement`, keeping indentation clean.
    line_start = content.rfind('\n', 0, start) + 1
    return content[:line_start] + replacement + content[end:]


# ─── Actualización del HTML ───────────────────────────────────────────────────

def update_html(html_path: Path, images: list) -> bool:
    content = html_path.read_text(encoding='utf-8')
    original = content

    first_src = f'./img/{images[0].name}'

    # 1. Imagen principal
    content = re.sub(
        r'(<img\s+id="pdpMainImg"\s+src=")[^"]*(")',
        rf'\g<1>{first_src}\2',
        content
    )

    # 2. Lightbox — imagen inicial
    content = re.sub(
        r'(<img\s+class="pdp-lightbox-img"\s+id="pdpLightboxImg"\s+src=")[^"]*(")',
        rf'\g<1>{first_src}\2',
        content
    )

    # 3. Thumbnails
    content = replace_div_by_class(content, 'pdp-thumbs', make_thumbs(images))

    # 3b. Structural fix: pdp-main-img-wrap must close BEFORE pdp-thumbs.
    #     Detects broken pattern: zoom-hint </div> (24sp) followed directly by
    #     pdp-thumbs without an intermediate </div> for the wrap div.
    content = re.sub(
        r'( {24}</div>)([ \t]*\n(?:[ \t]*\n)*)([ \t]*<div\b[^>]+class="pdp-thumbs")',
        lambda m: (
            m.group(1) + '\n' + ' ' * 20 + '</div>\n\n' + m.group(3)
            if '</div>' not in m.group(2)
            else m.group(0)
        ),
        content
    )

    # 4. Gallery strip
    content = replace_div_by_class(content, 'pdp-gallery-strip-grid', make_strip(images))

    # 5. Array pdpImages
    content = re.sub(
        r'const pdpImages = \[.*?\];',
        make_array(images),
        content,
        flags=re.DOTALL
    )

    if content != original:
        html_path.write_text(content, encoding='utf-8')
        return True
    return False


# ─── Procesamiento por producto ───────────────────────────────────────────────

def process_product(product_dir: Path) -> dict | None:
    img_dir   = product_dir / 'img'
    html_path = product_dir / 'index.html'

    if not img_dir.exists() or not html_path.exists():
        return None

    converted = convert_pngs(img_dir)
    images    = get_images(img_dir)

    if not images:
        return {'label': f'{product_dir.parent.name}/{product_dir.name}',
                'images': 0, 'converted': converted, 'updated': False}

    updated = update_html(html_path, images)

    return {
        'label':     f'{product_dir.parent.name}/{product_dir.name}',
        'images':    len(images),
        'converted': converted,
        'updated':   updated,
    }


# ─── Main ─────────────────────────────────────────────────────────────────────

def collect_targets(scope: str | None) -> list:
    base = ROOT / 'productos'
    if not scope:
        return [
            prod
            for cat in sorted(base.iterdir()) if cat.is_dir()
            for prod in sorted(cat.iterdir()) if prod.is_dir()
        ]

    scope_path = base / Path(scope.replace('\\', '/'))
    if not scope_path.exists():
        print(f"ERROR: no existe {scope_path}")
        sys.exit(1)

    # ¿Es un producto concreto (tiene index.html)?
    if (scope_path / 'index.html').exists():
        return [scope_path]

    # Es una categoría
    return [p for p in sorted(scope_path.iterdir()) if p.is_dir()]


def main():
    scope   = sys.argv[1] if len(sys.argv) > 1 else None
    targets = collect_targets(scope)

    total = updated = converted_n = empty = 0

    for prod_dir in targets:
        result = process_product(prod_dir)
        if result is None:
            continue

        total += 1

        if result['converted']:
            print(f"  PNG→WebP  {result['label']}: {', '.join(result['converted'])}")
            converted_n += len(result['converted'])

        if result['images'] == 0:
            empty += 1
            print(f"  VACÍO     {result['label']}")
        elif result['updated']:
            updated += 1
            print(f"  HTML ✓    {result['label']} — {result['images']} imagen(es)")

    print()
    print(f"{'─'*50}")
    print(f"  Productos procesados : {total}")
    print(f"  HTMLs actualizados   : {updated}")
    print(f"  PNGs convertidos     : {converted_n}")
    print(f"  Sin imágenes         : {empty}")
    print(f"{'─'*50}")


if __name__ == '__main__':
    main()
