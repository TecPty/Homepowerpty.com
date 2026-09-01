import os, re, shutil, json
from update_descriptions import PRODUCTS

base = r"c:\Users\HP 15\Homepowerpty.com\productos"

# Build rename map: old_folder -> new_folder
rename_map = {}

for folder, data in PRODUCTS.items():
    sku = data.get('sku', '').strip()
    if not sku or sku == 'N/A':
        continue
    # Sanitize SKU for folder name: replace spaces, slashes, dots with hyphens
    sku_clean = re.sub(r'[\s/\.]+', '-', sku).strip('-')
    new_folder = folder + '-' + sku_clean
    rename_map[folder] = new_folder

# Preview first
print("Preview (first 20):")
for old, new in list(rename_map.items())[:20]:
    print(f"  {old} -> {new}")
    
print(f"\nTotal to rename: {len(rename_map)}")
