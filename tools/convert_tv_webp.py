from pathlib import Path
from PIL import Image
import os

BASE = Path(r"C:\Users\HP 15\Homepowerpty.com")
TARGETS = ["productos/soportes-tv"]

converted = 0

for target in TARGETS:
    target_path = BASE / target
    print(f"Buscando en: {target_path}")
    for png in target_path.rglob("*.png"):
        webp = png.with_suffix(".webp")
        try:
            img = Image.open(png)
            if img.mode in ("RGBA", "LA", "P"):
                img = img.convert("RGBA")
            else:
                img = img.convert("RGB")
            img.save(webp, "WEBP", quality=90)
            converted += 1
            print(f"Convertido: {png.name} -> {webp.name}")
        except Exception as e:
            print(f"Error convirtiendo {png.name}: {e}")

print(f"\nTotal: {converted} imágenes convertidas a WebP.")
