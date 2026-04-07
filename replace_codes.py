import os
import re

# Mapeo completo: Codigo de barras (COD) → Numero de modelo (SKU)
CODE_TO_SKU = {
    # Air Fryers
    "732129008888": "JD389",
    "732129008635": "AF3201",
    "732129008413": "OC-506",
    # Licuadoras
    "6902468910348": "MM-111",
    "732129008895": "VB-999",
    "732129008390": "MM-931",
    "732129008406": "MM-933",
    # Batidoras
    "732129008949": "HP-024",
    "694943899199": "HP-044",
    "694943899205": "HP-045",
    # Estufas Electricas
    "732129008901": "F-010E-1",
    "732129008918": "2020B",
    "732129008581": "1010A",
    "732129008598": "2020A",
    # Estufas Gas
    "732129008437": "2050A",
    "732129008666": "3080",
    "732129008420": "3076K",
    "732129008673": "3081K",
    "694943899489": "HP-073",
    # Cafeteras
    "732129008932": "CM02",
    "732129008567": "WJ-9008",
    "732129008574": "WJ-9009",
    "732129008680": "WJ-9001",
    "732129008697": "WJ-9002",
    "732129008703": "WJ-9011",
    "694943899212": "HP-046",
    "694943899229": "HP-047",
    "694943899236": "HP-048",
    "694943899243": "HP-049",
    # Planchas
    "6942368204482": "R.91171B",
    "732129008840": "HP-012",
    "6975069407036": "R.1808B",
    "6975069402017": "R.91261",
    "6975069407234": "R.92003",
    # Teteras
    "732129008611": "JR-A101",
    "732129008628": "JR-LD8",
    "732129008604": "H208",
    "6975069407975": "JR-A101",
    "6975069401331": "JR-LD8",
    # Sandwicheras
    "732129008369": "SJ-24",
    "732129008352": "SJ-22",
    "732129008376": "SJ-40",
    "732129008383": "SJ-40A",
    "732129008727": "SJ-27",
    "732129008710": "SJ-35",
    # Tostadoras
    "6942368206585": "HP-017",
    "694943899502": "HP-017",
    "694943899519": "HP-018",
    # Hornito
    "732129008444": "PN-09",
    # Lochera
    "732129008659": "JY-1001",
    # Arroceras
    "732129008642": "HT-03",
    "732129008451": "HT-15A",
    "732129008468": "HT-15",
    "732129008475": "HT-18A",
    "732129008482": "HT-18",
    "732129008499": "HT-22A",
    "732129008505": "HT-22",
    # Ollas de Presion
    "732129008512": "CK-02-18",
    "732129008529": "CK-02-20",
    "732129008536": "CK-02-22",
    "732129008543": "CK-02-24",
    "732129008550": "CK-02-26",
}

def replace_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = 0
    
    for barcode, sku in CODE_TO_SKU.items():
        # Replace display label: "COD: 732129008888" → "MOD: JD389"
        new = content.replace(f'COD: {barcode}', f'MOD: {sku}')
        if new != content:
            changes += 1
        content = new
        
        # Replace URL-encoded in WhatsApp links: "COD:%20732129008888" → "MOD:%20JD389"
        new = content.replace(f'COD:%20{barcode}', f'MOD:%20{sku}')
        if new != content:
            changes += 1
        content = new
        
        # Replace bare barcode in WhatsApp text strings: "COD: 732129008888"
        new = content.replace(f'COD: {barcode}', f'MOD: {sku}')
        content = new
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return changes
    return 0

def run():
    base = r'c:\Users\HP 15\Homepowerpty.com'
    html_files = []
    
    # Collect all HTML files
    for root, dirs, files in os.walk(base):
        # Skip hidden/system folders
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules']]
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    total_files = 0
    total_changes = 0
    
    for filepath in html_files:
        changes = replace_in_file(filepath)
        if changes > 0:
            total_files += 1
            total_changes += changes
            print(f"  ✓ {os.path.relpath(filepath, base)} ({changes} reemplazos)")
    
    print(f"\nListo: {total_changes} reemplazos en {total_files} archivos.")

if __name__ == '__main__':
    run()
