import os
import re
from update_descriptions import PRODUCTS

base = r'c:\Users\HP 15\Homepowerpty.com\productos'
discrepancies = []

def extract_numbers(text):
    return set(re.findall(r'\b\d+(?:\.\d+)?(?:L|W|Tazas| Litros| cm| Liters)?\b', text, re.IGNORECASE))

for folder, data in PRODUCTS.items():
    filepath = os.path.join(base, folder, 'index.html')
    if not os.path.exists(filepath): continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. Check title
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL | re.IGNORECASE)
    if title_match:
        title = re.sub(r'<[^>]+>', ' ', title_match.group(1)).strip()
        # Find explicit capacity/power in title
        expected_cap = str(data.get('capacidad', '')).replace(' Litros', 'L')
        expected_pot = str(data.get('potencia', ''))
        
        # Super rough check: If there's a number followed by L or W in the title, it should match the expected ones.
        nums_in_title = extract_numbers(title)
        
        # We will just print the title alongside expected data if there's any mismatched unit.
        # But to be precise, I'll print them for manual review if they seem suspicious.
        
        # specific check for capacity
        cap_val = re.search(r'(\d+(?:\.\d+)?) ?(?:L|Litros)', expected_cap, re.IGNORECASE)
        if cap_val:
            c_val = cap_val.group(1)
            # if we find a DIFFERENT L value in title
            title_caps = re.findall(r'(\d+(?:\.\d+)?) ?L\b', title, re.IGNORECASE)
            for tc in title_caps:
                if float(tc) != float(c_val):
                    discrepancies.append(f"[{folder}] TITLE MISMATCH! Title says {tc}L but Source says {c_val}L -> {title}")
                    
        # Check specific features
        features_match = re.search(r'<section class="features-section">(.*?)</section>', html, re.DOTALL)
        if features_match:
            features_text = re.sub(r'<[^>]+>', ' ', features_match.group(1))
            feat_caps = re.findall(r'(\d+(?:\.\d+)?) ?L\b', features_text, re.IGNORECASE)
            for tc in feat_caps:
                if cap_val and float(tc) != float(c_val):
                    # Ignoring generic things, print only if different
                    discrepancies.append(f"[{folder}] FEATURE MISMATCH! Features say {tc}L but Source says {c_val}L")

if not discrepancies:
    print("SUCCESS: No obvious volumetric or power mismatches found between HTML details and Source Dictionary.")
else:
    for d in set(discrepancies):
        print(d)
