import openpyxl

wb = openpyxl.load_workbook('EXCEL DE PRODUCTOS PARA MKT.xlsx', data_only=True)
ws = wb.active

all_products = []

for i, row in enumerate(ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=5, values_only=True)):
    codigo, numero, imagen, descripcion, piezas = row
    if codigo and str(codigo).strip() not in ('', 'Codigo', 'None'):
        prod = {
            'codigo': str(codigo).strip(),
            'numero': str(numero).strip() if numero else '',
            'piezas': str(piezas).strip() if piezas else '',
            'descripcion': str(descripcion).strip().replace('\n', ' | ') if descripcion else ''
        }
        all_products.append(prod)

# Write clean output to a text file
with open('catalog_output.txt', 'w', encoding='utf-8') as f:
    f.write(f"Total productos: {len(all_products)}\n\n")
    f.write("="*80 + "\n")
    for p in all_products:
        f.write(f"COD: {p['codigo']}\n")
        f.write(f"  SKU:    {p['numero']}\n")
        f.write(f"  Piezas: {p['piezas']}\n")
        f.write(f"  Desc:   {p['descripcion'][:300]}\n")
        f.write("\n")

print(f"Listo. {len(all_products)} productos guardados en catalog_output.txt")
