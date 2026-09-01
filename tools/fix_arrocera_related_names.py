"""
Fix related card names for arrocera PDPs.
Uses the (model span + h3 href) pattern to make targeted replacements.
"""
import os
import re

# Name map based on Excel inventory
NAME_MAP = {
    'ht-03':  'Arrocera Eléctrica 0.3L',
    'ht-15':  'Arrocera Eléctrica 1.5L',
    'ht-15a': 'Arrocera con Vaporera 1.5L',
    'ht-18':  'Arrocera Eléctrica 1.8L',
    'ht-18a': 'Arrocera con Vaporera 1.8L',
    'ht-22':  'Arrocera Eléctrica 2.2L',
    'ht-22a': 'Arrocera con Vaporera 2.2L',
}

ARROCERAS_DIR = os.path.join('productos', 'arroceras')
updated_count = 0

for folder in os.listdir(ARROCERAS_DIR):
    filepath = os.path.join(ARROCERAS_DIR, folder, 'index.html')
    if not os.path.exists(filepath):
        continue

    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    original = content

    # Replace each related card h3 for the known SKUs
    for slug, name in NAME_MAP.items():
        # Pattern: <h3 class="pdp-related-name"><a href="../{slug}/">ANY TEXT</a></h3>
        pattern = r'(<h3 class="pdp-related-name"><a href="\.\./{}/">)[^<]*(</a></h3>)'.format(re.escape(slug))
        replacement = r'\g<1>' + name + r'\g<2>'
        content = re.sub(pattern, replacement, content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated: {filepath}')
        updated_count += 1
    else:
        print(f'No changes: {filepath}')

print(f'\nTotal files updated: {updated_count}')
