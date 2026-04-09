import os, shutil

artifacts = r"C:\Users\HP 15\.gemini\antigravity\brain\ab7c71c9-4cac-44e6-800e-ae397af80097"
base = r"C:\Users\HP 15\Homepowerpty.com\productos"

# Map: artifact filename -> (product_folder, standard_name)
copies = [
    # Sandwichera Clasica SJ-22
    ("sandwichera_clasica_lifestyle_dark_1775750421679.png",  "sandwichera-clasica-SJ-22", "LIFESTYLE_DARK.png"),
    ("sandwichera_clasica_detail_logo_1775750441419.png",     "sandwichera-clasica-SJ-22", "DETAIL_LOGO.png"),
    ("sandwichera_clasica_lifestyle_kitchen_1775750461679.png","sandwichera-clasica-SJ-22", "LIFESTYLE_KITCHEN.png"),
    ("sandwichera_clasica_brand_commercial_1775750484064.png", "sandwichera-clasica-SJ-22", "BRAND_COMMERCIAL.png"),
    # Sandwichera Metal SJ-24
    ("sandwichera_metal_lifestyle_dark_1775750503736.png",    "sandwichera-metal-SJ-24",   "LIFESTYLE_DARK.png"),
    ("sandwichera_metal_detail_logo_1775750522681.png",       "sandwichera-metal-SJ-24",   "DETAIL_LOGO.png"),
    ("sandwichera_metal_lifestyle_kitchen_1775750542982.png", "sandwichera-metal-SJ-24",   "LIFESTYLE_KITCHEN.png"),
    ("sandwichera_metal_brand_commercial_1775750561075.png",  "sandwichera-metal-SJ-24",   "BRAND_COMMERCIAL.png"),
    # Teteras (both share same images)
    ("tetera_lifestyle_dark_1775750579486.png",               "tetera-1-8l-JR-A101",       "LIFESTYLE_DARK.png"),
    ("tetera_detail_logo_1775750598764.png",                  "tetera-1-8l-JR-A101",       "DETAIL_LOGO.png"),
    ("tetera_lifestyle_kitchen_1775750617053.png",            "tetera-1-8l-JR-A101",       "LIFESTYLE_KITCHEN.png"),
    ("tetera_brand_commercial_1775750635042.png",             "tetera-1-8l-JR-A101",       "BRAND_COMMERCIAL.png"),
    ("tetera_lifestyle_dark_1775750579486.png",               "tetera-premium-JR-LD8",     "LIFESTYLE_DARK.png"),
    ("tetera_detail_logo_1775750598764.png",                  "tetera-premium-JR-LD8",     "DETAIL_LOGO.png"),
    ("tetera_lifestyle_kitchen_1775750617053.png",            "tetera-premium-JR-LD8",     "LIFESTYLE_KITCHEN.png"),
    ("tetera_brand_commercial_1775750635042.png",             "tetera-premium-JR-LD8",     "BRAND_COMMERCIAL.png"),
    # Planchas secas (shared)
    ("plancha_seco_lifestyle_dark_1775750661332.png",         "plancha-seco-R-91261",      "LIFESTYLE_DARK.png"),
    ("plancha_seco_detail_logo_1775750680046.png",            "plancha-seco-R-91261",      "DETAIL_LOGO.png"),
    ("plancha_lifestyle_kitchen_1775750700746.png",           "plancha-seco-R-91261",      "LIFESTYLE_KITCHEN.png"),
    ("plancha_brand_commercial_1775750720388.png",            "plancha-seco-R-91261",      "BRAND_COMMERCIAL.png"),
    ("plancha_seco_lifestyle_dark_1775750661332.png",         "plancha-seco-premium-R-1808B", "LIFESTYLE_DARK.png"),
    ("plancha_seco_detail_logo_1775750680046.png",            "plancha-seco-premium-R-1808B", "DETAIL_LOGO.png"),
    ("plancha_lifestyle_kitchen_1775750700746.png",           "plancha-seco-premium-R-1808B", "LIFESTYLE_KITCHEN.png"),
    ("plancha_brand_commercial_1775750720388.png",            "plancha-seco-premium-R-1808B", "BRAND_COMMERCIAL.png"),
    ("plancha_seco_lifestyle_dark_1775750661332.png",         "plancha-vapor-premium-R-92003", "LIFESTYLE_DARK.png"),
    ("plancha_seco_detail_logo_1775750680046.png",            "plancha-vapor-premium-R-92003", "DETAIL_LOGO.png"),
    ("plancha_lifestyle_kitchen_1775750700746.png",           "plancha-vapor-premium-R-92003", "LIFESTYLE_KITCHEN.png"),
    ("plancha_brand_commercial_1775750720388.png",            "plancha-vapor-premium-R-92003", "BRAND_COMMERCIAL.png"),
]

done = 0
errors = []
for fname, prod_folder, std_name in copies:
    src = os.path.join(artifacts, fname)
    dst_dir = os.path.join(base, prod_folder, "img")
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, std_name)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        done += 1
    else:
        errors.append(f"NOT FOUND: {fname}")

print(f"Copied: {done} files")
if errors:
    for e in errors: print(e)
