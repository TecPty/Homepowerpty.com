"""
Auto-generates pdp-related sections for all product pages that are missing them.
Logic: picks up to 3 siblings from the same category folder (excluding self).
Inserts before </main>.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
PRODUCTOS = ROOT / "productos"

# ── 1. Build catalog: category → list of {sku, title, img_exists} ─────────────
catalog = {}  # category -> [{sku, title}]

for html in sorted(PRODUCTOS.rglob("index.html")):
    cat  = html.parts[-3]  # e.g. "percoladoras"
    sku  = html.parts[-2]  # e.g. "hp-048"
    content = html.read_text(encoding="utf-8")

    # Try to grab the page title from pdp-title h1
    m = re.search(r'class="pdp-title"[^>]*>\s*([^<]+)', content)
    if not m:
        m = re.search(r'<h1[^>]*>\s*([^<\n]+)', content)
    title = m.group(1).strip() if m else sku.upper()

    img_path = html.parent / "img" / "PRODUCTO_PRINCIPAL.webp"
    img_exists = img_path.exists()

    catalog.setdefault(cat, []).append({
        "sku": sku,
        "title": title,
        "img_exists": img_exists,
    })

# ── 2. Template helpers ────────────────────────────────────────────────────────
def make_card(sibling_sku, sibling_title):
    return f"""\
                        <li class="pdp-related-card">
                            <a href="../{sibling_sku}/" class="pdp-related-img-wrap">
                                <img src="../{sibling_sku}/img/PRODUCTO_PRINCIPAL.webp" alt="{sibling_title}" loading="lazy">
                            </a>
                            <div class="pdp-related-info">
                                <span class="pdp-related-mod">{sibling_sku.upper()}</span>
                                <h3 class="pdp-related-name"><a href="../{sibling_sku}/">{sibling_title}</a></h3>
                                <a href="../{sibling_sku}/" class="pdp-related-cta">Ver producto</a>
                            </div>
                        </li>"""

def make_related_section(siblings):
    cards = "\n".join(make_card(s["sku"], s["title"]) for s in siblings)
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

# ── 3. Insert into pages missing pdp-related ──────────────────────────────────
added = []
skipped = []

for html in sorted(PRODUCTOS.rglob("index.html")):
    cat = html.parts[-3]
    sku = html.parts[-2]
    content = html.read_text(encoding="utf-8")

    if "pdp-related" in content:
        skipped.append(f"{cat}/{sku}")
        continue

    # Pick up to 3 siblings (different SKU, prefer ones with images)
    siblings_all = [p for p in catalog.get(cat, []) if p["sku"] != sku]
    siblings_with_img = [p for p in siblings_all if p["img_exists"]]
    candidates = siblings_with_img if siblings_with_img else siblings_all
    siblings = candidates[:3]

    if not siblings:
        print(f"  SKIP (no siblings): {cat}/{sku}")
        continue

    related_html = make_related_section(siblings)

    # Insert before </main>
    if "</main>" not in content:
        print(f"  WARN (no </main>): {cat}/{sku}")
        continue

    new_content = content.replace("</main>", related_html + "        </main>", 1)
    html.write_text(new_content, encoding="utf-8")
    added.append(f"{cat}/{sku}")

print(f"\nAdded pdp-related to {len(added)} pages")
print(f"Already had it:       {len(skipped)}")
for p in added:
    print(f"  + {p}")
