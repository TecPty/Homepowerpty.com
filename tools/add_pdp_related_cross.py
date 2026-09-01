"""
Adds cross-category pdp-related sections to the 6 solo products.
Paths are relative (../../other-cat/sku/) since these cross category boundaries.
"""
from pathlib import Path

ROOT = Path(__file__).parent
PRODUCTOS = ROOT / "productos"

# Cross-category mappings: target -> list of (cat, sku, title)
CROSS_RELATED = {
    "abanicos/hp-008": [
        ("estufas",      "hp-073",  "Estufa Gas 4 Quemadores + Horno"),
        ("extensiones",  "hp-050",  "Cable Extensión 1.8m"),
        ("regletas",     "hp-070",  "Regleta Polarizada 6 Tomas"),
    ],
    "asador/hp-014": [
        ("sandwicheras",      "sj-40",   "Sandwichera Premium Panini"),
        ("hornitos",          "pn-09",   "Hornito Eléctrico 9L"),
        ("freidoras-de-aire", "oc-506",  "Freidora de Aire White Pro 3.5L"),
    ],
    "basculas/hp-023": [
        ("batidoras",              "hp-021",  "Batidora de Mano 7 Velocidades"),
        ("procesador de alimento", "hp-022",  "Procesador de Alimentos 950mL"),
        ("licuadoras",             "hp-020",  "Licuadora Portátil 380mL"),
    ],
    "hornitos/pn-09": [
        ("freidoras-de-aire", "oc-506",  "Freidora de Aire White Pro 3.5L"),
        ("sandwicheras",      "sj-40",   "Sandwichera Premium Panini"),
        ("asador",            "hp-014",  "Asador Eléctrico BBQ 1400W"),
    ],
    "loncheras/jy-1001": [
        ("hornitos",      "pn-09",   "Hornito Eléctrico 9L"),
        ("sandwicheras",  "sj-22",   "Sandwichera Clásica"),
        ("teteras",       "hp-013",  "Cafetera y Tetera 2 en 1"),
    ],
    "procesador de alimento/hp-022": [
        ("batidoras",   "hp-021",  "Batidora de Mano 7 Velocidades"),
        ("licuadoras",  "hp-020",  "Licuadora Portátil 380mL"),
        ("basculas",    "hp-023",  "Báscula Digital de Cocina"),
    ],
}


def make_card_cross(cat, sku, title):
    return f"""\
                        <li class="pdp-related-card">
                            <a href="../../{cat}/{sku}/" class="pdp-related-img-wrap">
                                <img src="../../{cat}/{sku}/img/PRODUCTO_PRINCIPAL.webp" alt="{title}" loading="lazy">
                            </a>
                            <div class="pdp-related-info">
                                <span class="pdp-related-mod">{sku.upper()}</span>
                                <h3 class="pdp-related-name"><a href="../../{cat}/{sku}/">{title}</a></h3>
                                <a href="../../{cat}/{sku}/" class="pdp-related-cta">Ver producto</a>
                            </div>
                        </li>"""


def make_related_section(siblings):
    cards = "\n".join(make_card_cross(*s) for s in siblings)
    return f"""
            <section class="pdp-related">
                <div class="container">
                    <p class="section-eyebrow">TAMBIÉN TE PUEDE INTERESAR</p>
                    <h2 class="pdp-related-title">Productos similares</h2>
                    <ul class="pdp-related-grid">
{cards}
                    </ul>
                </div>
            </section>
"""


added = []
for key, siblings in CROSS_RELATED.items():
    parts = key.split("/", 1)
    html = PRODUCTOS / parts[0] / parts[1] / "index.html"
    content = html.read_text(encoding="utf-8")

    if "pdp-related" in content:
        print(f"  SKIP (already has it): {key}")
        continue

    if "</main>" not in content:
        print(f"  WARN (no </main>): {key}")
        continue

    related_html = make_related_section(siblings)
    new_content = content.replace("</main>", related_html + "        </main>", 1)
    html.write_text(new_content, encoding="utf-8")
    added.append(key)
    print(f"  + {key}")

print(f"\nDone. Added cross-category pdp-related to {len(added)} pages.")
