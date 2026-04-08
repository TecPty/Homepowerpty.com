import os
import json

base_dir = r"c:\Users\HP 15\Homepowerpty.com"
image_extensions = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".ico"}

inventory = {}

for root, dirs, files in os.walk(base_dir):
    # skip hidden/git directories
    if '.git' in root or '.gemini' in root or 'node_modules' in root:
        continue
    
    images = [f for f in files if os.path.splitext(f)[1].lower() in image_extensions]
    if images:
        rel_path = os.path.relpath(root, base_dir)
        inventory[rel_path] = images

with open("image_inventory.json", "w", encoding="utf-8") as f:
    json.dump(inventory, f, indent=2)

print(f"Encontradas {sum(len(v) for v in inventory.values())} imagenes en {len(inventory)} carpetas.")
