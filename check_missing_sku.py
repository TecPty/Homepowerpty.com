import os
from update_descriptions import PRODUCTS

base = r"c:\Users\HP 15\Homepowerpty.com\productos"
all_folders = set(d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d)))
catalog_folders = set(PRODUCTS.keys())

# Folders with no catalog entry
no_catalog = all_folders - catalog_folders
print("Folders with NO catalog entry (need manual SKU or skip):")
for f in sorted(no_catalog):
    print(" -", f)
    
# Catalog entries with no SKU
print("\nCatalog entries with missing/empty SKU:")
for k, v in PRODUCTS.items():
    sku = v.get('sku','').strip()
    if not sku:
        print(f"  {k} -> SKU is EMPTY")
