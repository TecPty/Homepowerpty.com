#!/usr/bin/env python3
"""
Genera sitemap.xml con todas las URLs del sitio HomePower PTY.
Incluye homepage + 110 PDPs + aviso de privacidad.
"""
import os
from datetime import date

BASE_URL = "https://www.homepowerpty.com"
TODAY = date.today().isoformat()
PRODUCTOS_DIR = "productos"

urls = []

# Homepage
urls.append({
    "loc": f"{BASE_URL}/",
    "priority": "1.0",
    "changefreq": "monthly"
})

# Aviso de privacidad
urls.append({
    "loc": f"{BASE_URL}/aviso-de-privacidad/",
    "priority": "0.3",
    "changefreq": "yearly"
})

# PDPs: scan de productos/categoria/sku/
for categoria in sorted(os.listdir(PRODUCTOS_DIR)):
    cat_path = os.path.join(PRODUCTOS_DIR, categoria)
    if not os.path.isdir(cat_path):
        continue
    for sku in sorted(os.listdir(cat_path)):
        sku_path = os.path.join(cat_path, sku)
        index_path = os.path.join(sku_path, "index.html")
        if os.path.isfile(index_path):
            # URL con encoding de espacios
            cat_encoded = categoria.replace(" ", "%20")
            sku_encoded = sku.replace(" ", "%20")
            urls.append({
                "loc": f"{BASE_URL}/productos/{cat_encoded}/{sku_encoded}/",
                "priority": "0.8",
                "changefreq": "monthly"
            })

# Generar XML
lines = ['<?xml version="1.0" encoding="UTF-8"?>']
lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

for url in urls:
    lines.append("  <url>")
    lines.append(f"    <loc>{url['loc']}</loc>")
    lines.append(f"    <lastmod>{TODAY}</lastmod>")
    lines.append(f"    <changefreq>{url['changefreq']}</changefreq>")
    lines.append(f"    <priority>{url['priority']}</priority>")
    lines.append("  </url>")

lines.append("</urlset>")

sitemap_content = "\n".join(lines) + "\n"
with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_content)

print(f"[OK] sitemap.xml generado con {len(urls)} URLs")
print(f"   Homepage: 1")
print(f"   PDPs:     {len(urls) - 2}")
print(f"   Legal:    1")
