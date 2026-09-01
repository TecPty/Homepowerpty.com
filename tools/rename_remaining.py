import os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base = r"c:\Users\HP 15\Homepowerpty.com"
productos_dir = os.path.join(base, "productos")

# Map: current_folder_name -> (base_name, correct_sku)
# For folders that were OK, leave blank. For those needing fix, provide base+sku.
FIXES = {
    # New folders (23 that had no SKU)
    "air-fryer-3l":              ("air-fryer-3l",             "AF3201"),
    "arrocera-0-3l":             ("arrocera-0-3l",            "HT-03"),
    "arrocera-1-8l":             ("arrocera-1-8l",            "HT-18A"),
    "arrocera-2-2l-basica":      ("arrocera-2-2l-basica",     "HT-22"),
    "batidora-mano":             ("batidora-mano",            "HP-044"),
    "batidora-mano-metal":       ("batidora-mano-metal",      "HP-045"),
    "batidora-pedestal":         ("batidora-pedestal",        "HP-024"),
    "cafetera-7-5-tazas":        ("cafetera-7-5-tazas",       "WJ-9011"),
    "cafetera-percoladora-100t": ("cafetera-percoladora-100t","HP-049"),
    "cafetera-percoladora-30t":  ("cafetera-percoladora-30t", "HP-046"),
    "cafetera-percoladora-40t":  ("cafetera-percoladora-40t", "HP-047"),
    "cafetera-percoladora-50t":  ("cafetera-percoladora-50t", "HP-048"),
    "estufa-electrica-1-quemador":   ("estufa-electrica-1-quemador",  "1010A"),
    "estufa-electrica-1q-premium":   ("estufa-electrica-1q-premium",  "F-010E-1"),
    "estufa-electrica-2q-negra":     ("estufa-electrica-2q-negra",    "2020A"),
    "lochera-termica":           ("lochera-termica",          "JY-1001"),
    "olla-presion-3-2l":         ("olla-presion-3-2l",        "CK-02-18"),
    "olla-presion-4-2l":         ("olla-presion-4-2l",        "CK-02-20"),
    "olla-presion-9l":           ("olla-presion-9l",          "CK-02-26"),
    "panini-metal":              ("panini-metal",             "SJ-40A"),
    "sandwichera-grill":         ("sandwichera-grill",        "SJ-27"),
    "tetera-plastico-1-5l":      ("tetera-plastico-1-5l",     "H208"),
    "tostadora-metal":           ("tostadora-metal",          "HP-018"),
    # Fix bad auto-suffixed names (replace the suffix, not append)
    "cafetera-12t-v2-V2":           ("cafetera-12t-v2",         "WJ-9002"),
    "cafetera-6t-v2-V2":            ("cafetera-6t-v2",          "WJ-9001"),
    "estufa-gas-2q-v2-GAS-2Q-V2":  ("estufa-gas-2q-v2",        "3080"),
    "estufa-gas-3q-v2-GAS-3Q-V2":  ("estufa-gas-3q-v2",        "3081K"),
    "estufa-gas-4q-horno-GAS-4Q-HORNO": ("estufa-gas-4q-horno","HP-073"),
    "licuadora-vb999-VB999":        ("licuadora-vb999",         "VB-999"),
}

rename_ops = {}
all_folders = [d for d in os.listdir(productos_dir) if os.path.isdir(os.path.join(productos_dir, d))]

for folder in all_folders:
    if folder in FIXES:
        base_name, sku = FIXES[folder]
        sku_clean = sku.replace('.', '-').strip('-')
        new_folder = base_name + '-' + sku_clean
        if new_folder != folder:
            rename_ops[folder] = new_folder

# Execute renames
done = []
errors = []
for old, new in rename_ops.items():
    old_path = os.path.join(productos_dir, old)
    new_path = os.path.join(productos_dir, new)
    try:
        os.rename(old_path, new_path)
        done.append((old, new))
    except Exception as e:
        errors.append(f"ERROR {old}: {e}")

print(f"Renamed: {len(done)}")
for old, new in done:
    print(f"  {old} -> {new}")
if errors:
    print("ERRORS:")
    for e in errors: print(e)

# Update HTML references
pairs = [(old + '/', new + '/') for old, new in done]
html_files = []
for root, dirs, files in os.walk(base):
    if '.git' in root or '.gemini' in root:
        continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

updated = []
for html_path in html_files:
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    for old_ref, new_ref in pairs:
        content = content.replace('productos/' + old_ref, 'productos/' + new_ref)
    if content != original:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        updated.append(os.path.relpath(html_path, base))

print(f"\nUpdated {len(updated)} HTML files.")
