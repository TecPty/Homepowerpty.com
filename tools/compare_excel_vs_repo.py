"""
Compara los SKUs del Excel de marketing vs los directorios de producto en el repo.
Genera un reporte de: en Excel pero sin PDP, en repo pero no en Excel.
"""
import openpyxl
import os
import re

PRODUCTOS_DIR = "productos"

# ─── 1. Leer SKUs del Excel ───────────────────────────────────────────────────
wb = openpyxl.load_workbook("PRODUCTOS HOME POWER MKT 23ABR.xlsx", read_only=True, data_only=True)
ws = wb["ZL"]

excel_rows = []
for i, row in enumerate(ws.iter_rows(values_only=True), 1):
    if i < 3:
        continue  # skip title + header
    non_none = [c for c in row if c is not None]
    if not non_none:
        continue
    if len(row) >= 2 and row[1]:
        sku_raw = str(row[1]).strip()
        desc = str(row[2]).strip() if len(row) > 2 and row[2] else ""
        # Algunos SKUs tienen alias en segunda línea ej: "2020B\n(F-011A-1)"
        sku_clean = sku_raw.split("\n")[0].strip().upper()
        alias = sku_raw.split("\n")[1].strip().strip("()") if "\n" in sku_raw else None
        if sku_clean and sku_clean not in ("NUMERO", "CÓDIGO", "CODIGO"):
            excel_rows.append({
                "sku": sku_clean,
                "alias": alias.upper() if alias else None,
                "desc": desc[:80].replace("\n", " "),
            })

print(f"SKUs en Excel: {len(excel_rows)}")

# ─── 2. Leer SKUs del repo (directorios de producto) ─────────────────────────
repo_skus = {}  # sku_upper -> (categoria, path)
for categoria in os.listdir(PRODUCTOS_DIR):
    cat_path = os.path.join(PRODUCTOS_DIR, categoria)
    if not os.path.isdir(cat_path):
        continue
    for sku_dir in os.listdir(cat_path):
        sku_path = os.path.join(cat_path, sku_dir)
        if os.path.isdir(sku_path):
            repo_skus[sku_dir.upper()] = (categoria, sku_path)

print(f"SKUs en repo: {len(repo_skus)}")

# ─── 3. Comparar ─────────────────────────────────────────────────────────────
in_excel_not_repo = []
in_repo_not_excel = []

excel_sku_set = set()
for row in excel_rows:
    excel_sku_set.add(row["sku"])
    if row["alias"]:
        excel_sku_set.add(row["alias"])

for row in excel_rows:
    found = (
        row["sku"] in repo_skus
        or (row["alias"] and row["alias"] in repo_skus)
    )
    # También buscar con guion vs sin guion y variantes
    if not found:
        # intento normalizar quitando guiones
        sku_norm = row["sku"].replace("-", "")
        for repo_sku in repo_skus:
            if repo_sku.replace("-", "") == sku_norm:
                found = True
                break
    if not found:
        in_excel_not_repo.append(row)

for repo_sku, (cat, path) in sorted(repo_skus.items()):
    if repo_sku not in excel_sku_set:
        # verificar normalizado
        repo_norm = repo_sku.replace("-", "")
        found = any(r["sku"].replace("-", "") == repo_norm or
                    (r["alias"] and r["alias"].replace("-", "") == repo_norm)
                    for r in excel_rows)
        if not found:
            in_repo_not_excel.append((cat, repo_sku))

# ─── 4. Reporte ──────────────────────────────────────────────────────────────
print("\n" + "="*70)
print(f"EN EL EXCEL PERO SIN PÁGINA EN EL REPO ({len(in_excel_not_repo)}):")
print("="*70)
for row in in_excel_not_repo:
    alias_str = f"  (alias: {row['alias']})" if row["alias"] else ""
    print(f"  {row['sku']:20s}{alias_str}")
    print(f"    → {row['desc'][:70]}")

print("\n" + "="*70)
print(f"EN EL REPO PERO NO EN EL EXCEL ({len(in_repo_not_excel)}):")
print("="*70)
for cat, sku in sorted(in_repo_not_excel):
    print(f"  [{cat}] {sku}")

print("\n" + "="*70)
print("RESUMEN:")
print(f"  Excel total:           {len(excel_rows)}")
print(f"  Repo total:            {len(repo_skus)}")
print(f"  Faltan en repo:        {len(in_excel_not_repo)}")
print(f"  En repo, no en Excel:  {len(in_repo_not_excel)}")
