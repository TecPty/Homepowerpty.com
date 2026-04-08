import os, re, shutil, json

base = r"c:\Users\HP 15\Homepowerpty.com"
productos_dir = os.path.join(base, "productos")

from update_descriptions import PRODUCTS as CATALOG

# Build rename map
rename_map = {}
all_folders = sorted([d for d in os.listdir(productos_dir) if os.path.isdir(os.path.join(productos_dir, d))])

for folder in all_folders:
    if folder in CATALOG:
        sku = CATALOG[folder].get('sku', '').strip()
        if sku:
            sku_clean = re.sub(r'[\s/\.]+', '-', sku).strip('-')
            rename_map[folder] = folder + '-' + sku_clean
            continue
    match = re.search(r'-([a-zA-Z]{1,3}[\-]?[\d]+[a-zA-Z0-9\-]*)$', folder)
    if match:
        code = match.group(1).upper().replace('--', '-')
        rename_map[folder] = folder + '-' + code

done = []
errors = []

# Step 1: Rename folders
for old, new in rename_map.items():
    old_path = os.path.join(productos_dir, old)
    new_path = os.path.join(productos_dir, new)
    try:
        os.rename(old_path, new_path)
        done.append((old, new))
    except Exception as e:
        errors.append(f"ERROR {old}: {e}")

print(f"Renamed {len(done)} folders.")
if errors:
    for e in errors:
        print(e)

# Step 2: Update all href/src references in every HTML file across the site
# Build search-replace pairs
pairs = [(old + '/', new + '/') for old, new in done]

html_files = []
for root, dirs, files in os.walk(base):
    if '.git' in root or '.gemini' in root:
        continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

updated_files = []
for html_path in html_files:
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    for old_ref, new_ref in pairs:
        content = content.replace('productos/' + old_ref, 'productos/' + new_ref)
        content = content.replace('productos/' + old_ref.replace('/', ''), 'productos/' + new_ref.replace('/', ''))
    if content != original:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        updated_files.append(os.path.relpath(html_path, base))

print(f"Updated references in {len(updated_files)} HTML files.")
print("Done!")
