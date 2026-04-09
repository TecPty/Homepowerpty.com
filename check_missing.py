import os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base = r"c:\Users\HP 15\Homepowerpty.com\productos"
REQUIRED = ['PRODUCTO_PRINCIPAL', 'CAJA', 'LIFESTYLE_DARK', 'DETAIL_LOGO', 'LIFESTYLE_KITCHEN', 'BRAND_COMMERCIAL']

results = {}
for prod in sorted(os.listdir(base)):
    prod_path = os.path.join(base, prod)
    if not os.path.isdir(prod_path): continue
    img_dir = os.path.join(prod_path, 'img')
    if not os.path.isdir(img_dir):
        results[prod] = REQUIRED[:]
        continue
    existing_names = [os.path.splitext(f)[0] for f in os.listdir(img_dir)]
    missing = [r for r in REQUIRED if r not in existing_names]
    if missing:
        results[prod] = missing

print(f"Productos con imagenes faltantes: {len(results)}")
print(f"Productos completos: {len(os.listdir(base)) - len(results)}\n")
for prod, missing in results.items():
    print(prod)
    for m in missing:
        print(f"  - {m}")
