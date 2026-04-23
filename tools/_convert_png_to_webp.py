"""
Convierte PNGs a WebP en freidoras-de-aire y licuadoras,
actualiza referencias en los HTMLs del PDP y elimina los PNGs.
"""
from pathlib import Path
from PIL import Image

BASE = Path(r"C:\Users\HP 15\Homepowerpty.com")
CATS = ["productos/freidoras-de-aire", "productos/licuadoras"]

converted = []
failed = []

for cat in CATS:
    for png in sorted((BASE / cat).rglob("*.png")):
        webp = png.with_suffix(".webp")
        try:
            img = Image.open(png)
            if img.mode in ("RGBA", "LA", "P"):
                img = img.convert("RGBA")
            else:
                img = img.convert("RGB")
            img.save(webp, "WEBP", quality=85, method=6)
            converted.append((png, webp))
            print(f"OK   {png.relative_to(BASE)}")
        except Exception as e:
            failed.append((png, str(e)))
            print(f"ERR  {png.relative_to(BASE)} -- {e}")

print(f"\n{len(converted)} convertidos, {len(failed)} errores")

# Actualizar referencias en HTMLs de los PDPs
html_updated = []
for cat in CATS:
    for html_file in (BASE / cat).rglob("*.html"):
        content = html_file.read_text(encoding="utf-8")
        original = content
        for png, webp in converted:
            if png.name in content:
                content = content.replace(png.name, webp.name)
        if content != original:
            html_file.write_text(content, encoding="utf-8")
            html_updated.append(str(html_file.relative_to(BASE)))

# También index.html raíz (por si acaso)
root_index = BASE / "index.html"
content = root_index.read_text(encoding="utf-8")
original = content
for png, webp in converted:
    rel_png = png.relative_to(BASE).as_posix()
    rel_webp = webp.relative_to(BASE).as_posix()
    if rel_png in content:
        content = content.replace(rel_png, rel_webp)
if content != original:
    root_index.write_text(content, encoding="utf-8")
    html_updated.append("index.html")

if html_updated:
    print("HTML actualizados:")
    for h in html_updated:
        print(f"  {h}")
else:
    print("index.html raiz: sin referencias .png")

# Eliminar originales
deleted = 0
for png, webp in converted:
    if webp.exists():
        png.unlink()
        deleted += 1
        print(f"DEL  {png.relative_to(BASE)}")

print(f"\n{deleted} PNGs eliminados")
