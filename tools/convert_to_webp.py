"""
convert_to_webp.py
Convierte todos los PNG de licuadoras, cafeteras y arroceras a WebP,
luego actualiza las referencias en index.html.
"""

from pathlib import Path
from PIL import Image

BASE = Path(r"C:\Users\HP 15\Homepowerpty.com")
INDEX = BASE / "index.html"

CATEGORIAS = [
    "productos/licuadoras",
    "productos/cafeteras",
    "productos/arroceras",
    "productos/ollas",
]

converted = []
failed = []

for cat in CATEGORIAS:
    for png in (BASE / cat).rglob("*.png"):
        webp = png.with_suffix(".webp")
        try:
            img = Image.open(png).convert("RGBA")
            img.save(webp, "WEBP", quality=85, method=6)
            converted.append((png, webp))
            print(f"OK  {png.relative_to(BASE)}")
        except Exception as e:
            failed.append((png, str(e)))
            print(f"ERR {png.relative_to(BASE)} — {e}")

print(f"\n{len(converted)} convertidos, {len(failed)} errores")

# ── Actualizar index.html ──────────────────────────────────────────────────
html = INDEX.read_text(encoding="utf-8")
updates = 0
for png, webp in converted:
    rel_png = png.relative_to(BASE).as_posix()
    rel_webp = webp.relative_to(BASE).as_posix()
    if rel_png in html:
        html = html.replace(rel_png, rel_webp)
        updates += 1

INDEX.write_text(html, encoding="utf-8")
print(f"{updates} referencias actualizadas en index.html")
