"""
fix_cafeteras_gallery.py
Wires pdp-thumbs, main img, gallery-strip-grid and pdpImages for all 6 cafeteras.
Uses the ACTUAL filenames on disk (preserving extensions and typos like KITCHET).
"""

import re
from pathlib import Path

BASE = Path(r"C:\Users\HP 15\Homepowerpty.com\productos\cafeteras")

# Actual filenames on disk, in display order.
# Tuple: (filename_on_disk, display_label)
CAFETERAS = {
    "cm02": [
        ("PRODUCTO_PRINCIPAL.webp", "Producto Principal"),
        ("CAJA.webp", "Caja"),
        ("BRAND_COMMERCIAL.png", "Brand Commercial"),
        ("DETAIL_LOGO.png", "Detail Logo"),
        ("LIFESTYLE_DARK.png", "Lifestyle Dark"),
        ("LIFESTYLE_KITCHEN.png", "Lifestyle Kitchen"),
    ],
    "wj-9001": [
        ("PRODUCTO_PRINCIPAL.webp", "Producto Principal"),
        ("CAJA.webp", "Caja"),
        ("BRAND_COMMERCIAL.png", "Brand Commercial"),
        ("DETAIL_LOGO.png", "Detail Logo"),
        ("LIFESTYLE_DARK.png", "Lifestyle Dark"),
        ("LIFESTYLE_KITCHEN.png", "Lifestyle Kitchen"),
    ],
    "wj-9002": [
        ("PRODUCTO_PRINCIPAL.webp", "Producto Principal"),
        ("CAJA.webp", "Caja"),
        ("BRAND_COMMERCIAL.png", "Brand Commercial"),
        ("DETAIL_LOGO.png", "Detail Logo"),
        ("LIFESTYLE_DARK.png", "Lifestyle Dark"),
        # Real typo on disk: KITCHET (missing N)
        ("LIFESTYLE_KITCHET.png", "Lifestyle Kitchen"),
    ],
    "wj-9008": [
        ("PRODUCTO_PRINCIPAL.webp", "Producto Principal"),
        ("CAJA.webp", "Caja"),
        ("DETAIL_LOGO.webp", "Detail Logo"),
        ("LIFESTYLE_DARK.webp", "Lifestyle Dark"),
        ("LIFESTYLE_KITCHEN.webp", "Lifestyle Kitchen"),
        # No BRAND_COMMERCIAL for wj-9008
    ],
    "wj-9009": [
        ("PRODUCTO_PRINCIPAL.webp", "Producto Principal"),
        ("CAJA.webp", "Caja"),
        ("BRAND_COMMERCIAL.webp", "Brand Commercial"),
        ("DETAIL_LOGO.webp", "Detail Logo"),
        ("LIFESTYLE_DARK.webp", "Lifestyle Dark"),
        ("LIFESTYLE_KITCHEN.webp", "Lifestyle Kitchen"),
    ],
    "wj-9011": [
        ("PRODUCTO_PRINCIPAL.webp", "Producto Principal"),
        ("CAJA.webp", "Caja"),
        ("BRAND_COMMERCIAL.png", "Brand Commercial"),
        ("DETAIL_LOGO.png", "Detail Logo"),
        ("LIFESTYLE_DARK.png", "Lifestyle Dark"),
        ("LIFESTYLE_KITCHEN.png", "Lifestyle Kitchen"),
    ],
}

SVG_ZOOM = (
    '<svg width="22" height="22" fill="none" stroke="currentColor" '
    'stroke-width="1.5" viewBox="0 0 24 24">'
    '<circle cx="11" cy="11" r="8"/>'
    '<line x1="21" y1="21" x2="16.65" y2="16.65"/>'
    '<line x1="11" y1="8" x2="11" y2="14"/>'
    '<line x1="8" y1="11" x2="14" y2="11"/></svg>'
)


def build_thumbs(images):
    """Full pdp-thumbs div with all thumb buttons."""
    lines = ['<div class="pdp-thumbs" role="list" aria-label="Im\u00e1genes del producto">']
    for i, (fname, label) in enumerate(images):
        active = " active" if i == 0 else ""
        lines.append(
            f'                        <button class="pdp-thumb{active}"\n'
            f'                                onclick="pdpSetImage(\'./img/{fname}\', this)"\n'
            f'                                aria-label="Ver {label}" role="listitem">\n'
            f'                            <img src="./img/{fname}" alt="{label}">\n'
            f"                        </button>"
        )
    lines.append("                    </div>")
    return "\n".join(lines)


def build_strip_inner(images):
    """pdp-gallery-strip-grid opening tag + strip items.
    Does NOT include the closing </div> — that stays from the original file."""
    lines = ['<div class="pdp-gallery-strip-grid">']
    for i, (fname, label) in enumerate(images):
        lines.append(
            f'                        <div class="pdp-strip-item" onclick="pdpOpenLightboxAt({i})"'
            f' role="button" tabindex="0" aria-label="Ampliar {label}">\n'
            f'                            <img src="./img/{fname}" alt="{label}" loading="lazy">\n'
            f'                            <div class="pdp-strip-overlay" aria-hidden="true">\n'
            f"                                {SVG_ZOOM}\n"
            f"                            </div>\n"
            f"                        </div>"
        )
    return "\n".join(lines)


def build_pdp_images(images):
    items = ",\n".join(f"            './img/{fname}'" for fname, _ in images)
    return f"const pdpImages = [\n{items},\n        ];"


results = []

for slug, images in CAFETERAS.items():
    path = BASE / slug / "index.html"
    if not path.exists():
        results.append(f"  MISSING  {slug}")
        continue

    content = path.read_text(encoding="utf-8")
    original = content
    issues = []

    # 1. Replace pdp-thumbs block
    # Buttons have no inner divs, so first </div> after <div class="pdp-thumbs"...> is its own closer.
    new_thumbs = build_thumbs(images)
    content, n = re.subn(
        r'<div class="pdp-thumbs"[^>]*>.*?</div>',
        new_thumbs,
        content,
        count=1,
        flags=re.DOTALL,
    )
    if n == 0:
        issues.append("pdp-thumbs not found")

    # 2. Fix main img src (only src attribute, preserve alt)
    first_img = images[0][0]
    content, n = re.subn(
        r'(<img id="pdpMainImg"\s+src=")[^"]*(")',
        rf'\g<1>./img/{first_img}\2',
        content,
        count=1,
    )
    if n == 0:
        issues.append("pdpMainImg not found")

    # 3. Replace gallery-strip-grid content
    # Strategy: find opener, find the FIRST occurrence of the grid's closing tag
    # (20-space indent </div>), replace opener+content up to (not including) closer.
    strip_opener = '<div class="pdp-gallery-strip-grid">'
    strip_closer = "\n                    </div>"  # 20 spaces = grid closing tag
    start = content.find(strip_opener)
    end = content.find(strip_closer, start + len(strip_opener)) if start != -1 else -1
    if start != -1 and end != -1:
        new_strip = build_strip_inner(images)
        content = content[:start] + new_strip + content[end:]
    else:
        issues.append("gallery-strip-grid not found")

    # 4. Replace pdpImages array
    new_arr = build_pdp_images(images)
    content, n = re.subn(
        r"const pdpImages = \[.*?\];",
        new_arr,
        content,
        count=1,
        flags=re.DOTALL,
    )
    if n == 0:
        issues.append("pdpImages not found")

    path.write_text(content, encoding="utf-8")

    if issues:
        results.append(f"  WARN  {slug}: {len(images)} imgs | issues: {', '.join(issues)}")
    elif content == original:
        results.append(f"  =     {slug}: no changes (already up to date)")
    else:
        results.append(f"  OK    {slug}: {len(images)} images wired")

print("\nCafeteras gallery fix:")
for r in results:
    print(r)
print()
