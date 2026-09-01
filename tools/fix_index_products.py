import re

# ─── 1. Fix index.html: cerrar todos los <li class='product'> ────────────────
content = open('index.html', encoding='utf-8').read()

CLOSING = (
    '\n                                    </ul>'
    '\n                                </div>'
    '\n                            </li>'
)

# Antes de cada <li class="product"> que siga a los features
def insert_closing_before_product(m):
    return m.group(1) + CLOSING + '\n' + m.group(2)

content2 = re.sub(
    r'(\n[ \t]+<li>[^<]*</li>)\n([ \t]+<li class="product")',
    insert_closing_before_product,
    content
)

# Cerrar el ÚLTIMO producto antes del cierre del grid </ul>
def insert_closing_before_grid_end(m):
    return m.group(1) + CLOSING + '\n' + m.group(2)

content2 = re.sub(
    r'(\n[ \t]+<li>[^<]*</li>)\n([ \t]+</ul>[ \t]*\n[ \t]+</section>)',
    insert_closing_before_grid_end,
    content2
)

# Fix SKU incorrecto de ht-22a
old_sku = (
    'href="productos/arroceras/ht-22a/" class="product_image_wrapper">\n'
    '                                    <img src="productos/arroceras/ht-22a/img/PRODUCTO_PRINCIPAL_2.2A.webp"\n'
    '                                        data-box="productos/arroceras/ht-22a/img/CAJA_2.2A.webp"\n'
    '                                        alt="Arrocera con Vaporera" class="product_img" loading="lazy">\n'
    '                                </a>\n'
    '                                <div class="product_content">\n'
    '                                    <span class="product_sku">MOD: HT-18A</span>'
)
new_sku = old_sku.replace('MOD: HT-18A</span>', 'MOD: HT-22A</span>')

content2 = content2.replace(old_sku, new_sku)

if content2 != content:
    open('index.html', 'w', encoding='utf-8').write(content2)
    count = content2.count(CLOSING)
    print(f'index.html: {count} cierres insertados')
    if 'MOD: HT-22A' in content2:
        print('SKU ht-22a corregido: HT-18A -> HT-22A')
else:
    print('index.html: sin cambios detectados')
