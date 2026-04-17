"""
Análisis completo: Excel vs carpetas de productos vs imágenes fuente
"""
import pandas as pd
import os
import re
from pathlib import Path

# --- Leer Excel ---
df = pd.read_excel('EXCEL DE PRODUCTOS PARA MKT.xlsx', header=1)
df = df.dropna(axis=1, how='all')
df = df.dropna(subset=['Numero'])
df = df.rename(columns={
    'Codigo': 'CODIGO_BARRA',
    'Numero': 'SKU',
    'Descripcion': 'DESC',
    'Piezas x bulto': 'BULTO',
    'Unnamed: 5': 'NOTA'
})
df = df[['CODIGO_BARRA', 'SKU', 'DESC', 'BULTO', 'NOTA']].copy()
df['SKU'] = df['SKU'].astype(str).str.strip()
df['CODIGO_BARRA'] = df['CODIGO_BARRA'].astype(str).str.strip().str.replace('.0', '', regex=False)

# Extraer nombre limpio del producto (primera línea de DESC)
def extract_name(desc):
    if pd.isna(desc):
        return ''
    lines = str(desc).split('\n')
    # Primera parte antes de los dos puntos o la primera línea
    first = lines[0].strip()
    # Limpiar espacios múltiples
    first = re.sub(r'\s+', ' ', first)
    return first

df['NOMBRE'] = df['DESC'].apply(extract_name)

excel_skus = {r['SKU'].upper().replace('.', '').replace(' ', ''): r for _, r in df.iterrows()}

# --- Carpetas existentes ---
productos_dir = Path('productos')
folders = []
for cat_dir in productos_dir.iterdir():
    if cat_dir.is_dir() and not cat_dir.name.startswith('_'):
        for sku_dir in cat_dir.iterdir():
            if sku_dir.is_dir():
                folders.append({
                    'categoria': cat_dir.name,
                    'folder': sku_dir.name,
                    'folder_upper': sku_dir.name.upper().replace('-', '').replace('_', ''),
                    'path': sku_dir
                })

folder_skus = {f['folder_upper']: f for f in folders}

# --- Imágenes fuente ---
source_dir = Path('PRODUCTOS-IMAGENES/PRODUCTOS')
source_images = {}
if source_dir.exists():
    for img in source_dir.glob('*.png'):
        source_images[img.name.upper()] = img

# --- Imágenes ya desplegadas ---
def count_deployed_images(folder_path):
    img_dir = folder_path / 'img'
    if img_dir.exists():
        return len(list(img_dir.glob('*.webp')))
    return 0

print("=" * 80)
print("ANÁLISIS: EXCEL vs CARPETAS vs IMÁGENES")
print("=" * 80)

print(f"\nTotal en Excel:    {len(df)} productos")
print(f"Total carpetas:    {len(folders)} SKUs")
print(f"Imágenes fuente:   {len(source_images)} archivos PNG")

# --- 1. SKUs en Excel sin carpeta ---
print("\n" + "=" * 80)
print("❌ EN EXCEL PERO SIN CARPETA DE PRODUCTO:")
print("=" * 80)
missing_folders = []
for sku, row in df.iterrows():
    sku_val = row['SKU']
    sku_clean = sku_val.upper().replace('.', '').replace(' ', '').replace('-', '')
    found = False
    for fkey, fval in folder_skus.items():
        if fkey == sku_clean or fkey.replace('-','') == sku_clean:
            found = True
            break
    if not found:
        missing_folders.append(sku_val)
        print(f"  {sku_val:20s} | {row['NOMBRE'][:60]}")

# --- 2. Carpetas sin registro en Excel ---
print("\n" + "=" * 80)
print("⚠️  CARPETAS SIN REGISTRO EN EXCEL:")
print("=" * 80)
extra_folders = []
for fkey, fval in folder_skus.items():
    sku_clean = fkey.replace('-', '')
    found = False
    for ekey in excel_skus:
        if ekey == sku_clean or ekey.replace('-','') == sku_clean:
            found = True
            break
    if not found:
        extra_folders.append(fval)
        imgs = count_deployed_images(fval['path'])
        print(f"  {fval['folder']:35s} | cat: {fval['categoria']:20s} | imgs desplegadas: {imgs}")

# --- 3. Matching con discrepancias de nombre de carpeta ---
print("\n" + "=" * 80)
print("🔍 DISCREPANCIAS DE NOMBRE: Excel SKU vs Nombre de Carpeta")
print("=" * 80)
for _, row in df.iterrows():
    sku_excel = row['SKU']
    sku_clean_excel = sku_excel.upper().replace('.', '').replace(' ', '').replace('-', '').replace('(', '').split('(')[0].strip()
    # Buscar carpeta que coincida
    match = None
    for fkey, fval in folder_skus.items():
        fkey_clean = fkey.replace('-', '')
        if fkey_clean == sku_clean_excel or fkey == sku_clean_excel:
            match = fval
            break
    if match:
        # Ver si hay diferencia entre el SKU del Excel y el nombre de carpeta
        folder_name = match['folder']
        expected_folder = sku_excel.lower().replace('.', '-').replace(' ', '-')
        if folder_name.lower() != expected_folder.lower():
            print(f"  Excel: {sku_excel:20s} → Carpeta actual: {folder_name:30s}")

# --- 4. Estado de imágenes por producto ---
print("\n" + "=" * 80)
print("📸 ESTADO DE IMÁGENES POR PRODUCTO (Excel)")
print("=" * 80)
print(f"{'SKU':<15} {'BARCODE':<16} {'CARPETA':<35} {'IMGS DESP':>10} {'NOMBRE'}")
print("-" * 100)

matched = 0
unmatched = 0
for _, row in df.iterrows():
    sku_excel = row['SKU']
    sku_clean = sku_excel.upper().replace('.', '').replace(' ', '').replace('-', '').split('(')[0].strip()
    match = None
    for fkey, fval in folder_skus.items():
        if fkey.replace('-','') == sku_clean or fkey == sku_clean:
            match = fval
            break
    if match:
        imgs = count_deployed_images(match['path'])
        status = "✅" if imgs > 0 else "📭"
        print(f"{sku_excel:<15} {row['CODIGO_BARRA']:<16} {match['folder']:<35} {status} {imgs:>3}     {row['NOMBRE'][:40]}")
        matched += 1
    else:
        print(f"{sku_excel:<15} {row['CODIGO_BARRA']:<16} {'--- SIN CARPETA ---':<35} ❓       {row['NOMBRE'][:40]}")
        unmatched += 1

print(f"\nTotal: {matched} con carpeta, {unmatched} sin carpeta")

# --- 5. Guardar JSON de datos para uso en el sitio ---
import json
products_data = []
for _, row in df.iterrows():
    products_data.append({
        'sku': row['SKU'],
        'barcode': row['CODIGO_BARRA'],
        'nombre': row['NOMBRE'],
        'es_nuevo': pd.notna(row['NOTA']) and 'NUEVO' in str(row['NOTA']).upper()
    })

with open('tools/products_from_excel.json', 'w', encoding='utf-8') as f:
    json.dump(products_data, f, ensure_ascii=False, indent=2)

print(f"\n✅ Datos guardados en tools/products_from_excel.json")
