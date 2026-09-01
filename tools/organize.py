import os
import shutil
import json

base_dir = r"c:\Users\HP 15\Homepowerpty.com\productos"
os.chdir(base_dir)

products = [d for d in os.listdir() if os.path.isdir(d)]

report = {
    'renamed': [],
    'deleted': [],
    'missing': {}
}

for prod in products:
    img_dir = os.path.join(prod, 'img')
    if not os.path.isdir(img_dir):
        report['missing'][prod] = ['PRODUCTO_PRINCIPAL', 'CAJA', 'LIFESTYLE_DARK', 'DETAIL_LOGO', 'LIFESTYLE_KITCHEN', 'BRAND_COMMERCIAL']
        continue
    
    files = [f for f in os.listdir(img_dir) if f.lower().endswith(('.png', '.webp', '.jpg', '.jpeg'))]
    
    mapped_this_folder = {}
    unmapped = []

    def assign(file, key):
        if key not in mapped_this_folder:
            mapped_this_folder[key] = file
            return True
        return False

    # 1. Map by clear keywords
    for file in files:
        f_lower = file.lower()
        if 'caja' in f_lower:
            assign(file, 'CAJA')
        elif 'lifestyle_dark' in f_lower:
            assign(file, 'LIFESTYLE_DARK')
        elif 'detail_logo' in f_lower or 'detail_panel' in f_lower:
            assign(file, 'DETAIL_LOGO')
        elif 'lifestyle_kitchen' in f_lower or 'lifestyle_food' in f_lower or 'lifestyle_morning' in f_lower:
            assign(file, 'LIFESTYLE_KITCHEN')
        elif 'brand_commercial' in f_lower or 'lifestyle_office' in f_lower or 'lifestyle_ambient' in f_lower:
            assign(file, 'BRAND_COMMERCIAL')
        elif 'producto_principal' in f_lower:
            assign(file, 'PRODUCTO_PRINCIPAL')

    # 2. Heuristic for PRODUCTO_PRINCIPAL
    for file in files:
        if file not in mapped_this_folder.values():
            if not assign(file, 'PRODUCTO_PRINCIPAL'):
                unmapped.append(file)

    # 3. Apply Re-naming and Deletions
    populated = []
    
    for key, old_filename in mapped_this_folder.items():
        ext = os.path.splitext(old_filename)[1]
        new_filename = key + ext
        old_path = os.path.join(img_dir, old_filename)
        new_path = os.path.join(img_dir, new_filename)
        
        if old_filename == new_filename:
            populated.append(key)
        else:
            if os.path.exists(new_path) and old_filename != new_filename:
                if new_filename in unmapped:
                    unmapped.remove(new_filename)
                try:
                    os.remove(new_path)
                except Exception:
                    pass
            try:
                os.rename(old_path, new_path)
                report['renamed'].append(prod + ": " + old_filename + " -> " + new_filename)
                populated.append(key)
            except Exception:
                pass
            
    for file in unmapped:
        if file in mapped_this_folder.values(): continue
        path = os.path.join(img_dir, file)
        if os.path.exists(path):
            try:
                os.remove(path)
                report['deleted'].append(prod + ": " + file)
            except Exception:
                pass
            
    # 4. Check Missing
    missing = []
    for req in ['PRODUCTO_PRINCIPAL', 'CAJA', 'LIFESTYLE_DARK', 'DETAIL_LOGO', 'LIFESTYLE_KITCHEN', 'BRAND_COMMERCIAL']:
        if req not in populated:
            missing.append(req)
            
    if missing:
        report['missing'][prod] = missing

with open(r"c:\Users\HP 15\Homepowerpty.com\migration_report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)

r_len = len(report['renamed'])
d_len = len(report['deleted'])
m_len = len(report['missing'])
print("Renamed:", r_len)
print("Deleted:", d_len)
print("Missing Products:", m_len)
