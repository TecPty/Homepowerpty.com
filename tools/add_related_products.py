"""
Agrega sección "Productos similares" a todos los PDPs que tienen pdp-trust-bar.
Para cada PDP, toma hasta 4 hermanos de la misma categoría.
Idempotente: no toca PDPs que ya tienen pdp-related.
"""
import os
import glob
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PRODUCTOS = os.path.join(ROOT, "productos")

SVG_ZOOM = (
    '<svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.5" '
    'viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/>'
    '<line x1="21" y1="21" x2="16.65" y2="16.65"/>'
    '<line x1="11" y1="8" x2="11" y2="14"/>'
    '<line x1="8" y1="11" x2="14" y2="11"/></svg>'
)

ANCHOR = '<section class="pdp-trust-bar">'


def get_principal_img(product_dir):
    """Devuelve el primer archivo PRODUCTO_PRINCIPAL*.webp del img/ del producto."""
    img_dir = os.path.join(product_dir, "img")
    if not os.path.isdir(img_dir):
        return None
    candidates = sorted([
        f for f in os.listdir(img_dir)
        if f.upper().startswith("PRODUCTO_PRINCIPAL") and f.lower().endswith(".webp")
    ])
    return candidates[0] if candidates else None


def get_pdp_name(html_path):
    """Extrae el texto del h1.pdp-name."""
    try:
        content = open(html_path, encoding="utf-8").read()
        m = re.search(r'<h1 class="pdp-name">([^<]+)</h1>', content)
        if m:
            return m.group(1).strip()
    except Exception:
        pass
    return None


def get_pdp_mod(html_path):
    """Extrae el texto del p.pdp-model (ej: MOD: 2020A)."""
    try:
        content = open(html_path, encoding="utf-8").read()
        m = re.search(r'<p class="pdp-model">([^<]+)</p>', content)
        if m:
            return m.group(1).strip()
    except Exception:
        pass
    return None


def build_related_section(siblings_info):
    """
    siblings_info: lista de dicts con keys: slug, img, name, mod
    """
    cards = ""
    for s in siblings_info:
        cards += f"""                        <li class="pdp-related-card">
                            <a href="../{s['slug']}/" class="pdp-related-img-wrap">
                                <img src="../{s['slug']}/img/{s['img']}" alt="{s['name']}" loading="lazy">
                            </a>
                            <div class="pdp-related-info">
                                <span class="pdp-related-mod">{s['mod']}</span>
                                <h3 class="pdp-related-name"><a href="../{s['slug']}/">{s['name']}</a></h3>
                                <a href="../{s['slug']}/" class="pdp-related-cta">Ver producto</a>
                            </div>
                        </li>\n"""

    return f"""            <section class="pdp-related">
                <div class="container">
                    <p class="section-eyebrow">TAMBIÉN TE PUEDE INTERESAR</p>
                    <h2 class="pdp-related-title">Productos similares</h2>
                    <ul class="pdp-related-grid">
{cards}                    </ul>
                </div>
            </section>

            """


def process_pdp(html_path):
    content = open(html_path, encoding="utf-8").read()

    # Skip si ya tiene la sección
    if "pdp-related" in content:
        return "skip"

    # Skip si no tiene el anchor
    if ANCHOR not in content:
        return "no-anchor"

    # Determinar categoría y slug actual
    parts = html_path.replace("\\", "/").split("/")
    # ...productos/CATEGORIA/SLUG/index.html
    pdp_slug = parts[-2]
    cat_dir = os.path.dirname(os.path.dirname(html_path))

    # Obtener hermanos (misma categoría, distinto slug)
    siblings = []
    for entry in sorted(os.listdir(cat_dir)):
        entry_path = os.path.join(cat_dir, entry)
        if not os.path.isdir(entry_path):
            continue
        if entry == pdp_slug:
            continue
        sibling_html = os.path.join(entry_path, "index.html")
        if not os.path.isfile(sibling_html):
            continue
        img = get_principal_img(entry_path)
        if not img:
            continue
        name = get_pdp_name(sibling_html) or entry
        mod = get_pdp_mod(sibling_html) or f"MOD: {entry.upper()}"
        siblings.append({
            "slug": entry,
            "img": img,
            "name": name,
            "mod": mod,
        })

    if not siblings:
        return "no-siblings"

    # Tomar máximo 4
    chosen = siblings[:4]
    related_html = build_related_section(chosen)

    new_content = content.replace(ANCHOR, related_html + ANCHOR, 1)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    return f"ok ({len(chosen)} productos)"


def main():
    files = glob.glob(os.path.join(PRODUCTOS, "**", "index.html"), recursive=True)
    stats = {"ok": 0, "skip": 0, "no-anchor": 0, "no-siblings": 0, "error": 0}

    for f in sorted(files):
        rel = os.path.relpath(f, ROOT)
        try:
            result = process_pdp(f)
            if result.startswith("ok"):
                stats["ok"] += 1
                print(f"  ✓  {rel}  →  {result}")
            elif result == "skip":
                stats["skip"] += 1
                print(f"  —  {rel}  (ya tiene pdp-related)")
            elif result == "no-anchor":
                stats["no-anchor"] += 1
            elif result == "no-siblings":
                stats["no-siblings"] += 1
                print(f"  !  {rel}  (sin hermanos)")
        except Exception as e:
            stats["error"] += 1
            print(f"  ✗  {rel}  ERROR: {e}")

    print()
    print(f"Procesados:    {stats['ok']}")
    print(f"Ya tenían:     {stats['skip']}")
    print(f"Sin anchor:    {stats['no-anchor']}")
    print(f"Sin hermanos:  {stats['no-siblings']}")
    print(f"Errores:       {stats['error']}")


if __name__ == "__main__":
    main()
