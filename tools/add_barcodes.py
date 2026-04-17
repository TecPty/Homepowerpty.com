"""
Agrega el código de barras (pdp-barcode) a todas las páginas de producto.
Lee el SKU actual del HTML (pdp-model), lo busca en el Excel, e inserta la línea debajo.
"""
import json
import re
from pathlib import Path

# Cargar datos del Excel
with open('tools/products_from_excel.json', encoding='utf-8') as f:
    products = json.load(f)

# Construir mapa SKU → barcode (normalizado a mayúsculas sin puntos)
def normalize_sku(s):
    return s.upper().replace('.', '').replace(' ', '').replace('-', '').split('(')[0].strip()

sku_to_barcode = {}
sku_to_raw = {}
for p in products:
    key = normalize_sku(p['sku'])
    sku_to_barcode[key] = p['barcode']
    sku_to_raw[key] = p['sku']

# Patrón para encontrar pdp-model
MODEL_RE = re.compile(r'(<p class="pdp-model">)(MOD:\s*)([^<]+)(</p>)')
BARCODE_RE = re.compile(r'pdp-barcode')

productos_dir = Path('productos')
updated = 0
skipped = 0
no_match = 0
already_has = 0

for html_file in sorted(productos_dir.rglob('index.html')):
    content = html_file.read_text(encoding='utf-8')

    # Verificar si ya tiene barcode
    if BARCODE_RE.search(content):
        already_has += 1
        print(f"  YA TIENE  {html_file}")
        continue

    # Buscar pdp-model
    m = MODEL_RE.search(content)
    if not m:
        skipped += 1
        print(f"  SIN MODEL {html_file}")
        continue

    sku_in_html = m.group(3).strip()
    sku_key = normalize_sku(sku_in_html)

    if sku_key not in sku_to_barcode:
        no_match += 1
        print(f"  NO EXCEL  {html_file}  SKU: {sku_in_html}")
        continue

    barcode = sku_to_barcode[sku_key]

    # Construir línea de barcode con la misma indentación que pdp-model
    # Detectar indentación
    line_start = content.rfind('\n', 0, m.start()) + 1
    indent = ''
    for ch in content[line_start:m.start()]:
        if ch in (' ', '\t'):
            indent += ch
        else:
            break

    barcode_line = f'\n{indent}<p class="pdp-barcode">CÓD. BARRAS: {barcode}</p>'

    new_content = content[:m.end()] + barcode_line + content[m.end():]
    html_file.write_text(new_content, encoding='utf-8')
    updated += 1
    print(f"  ✅ {sku_in_html:15s} → {barcode:15s}  {html_file.parent.name}")

print()
print(f"Actualizados:  {updated}")
print(f"Ya tenían:     {already_has}")
print(f"Sin pdp-model: {skipped}")
print(f"Sin match Excel: {no_match}")
