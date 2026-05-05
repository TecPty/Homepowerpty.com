"""Convierte PNGs a WebP, borra los PNGs y actualiza referencias en HTML."""
from pathlib import Path
from PIL import Image
import re

BASE = Path(r'c:\Users\HP 15\Homepowerpty.com\productos')
converted = []
skipped = []
errors = []

for png in sorted(BASE.glob('*/*/img/*.png')):
    webp = png.with_suffix('.webp')

    if not webp.exists():
        try:
            img = Image.open(png)
            mode = 'RGBA' if img.mode in ('RGBA', 'LA', 'P') else 'RGB'
            img.convert(mode).save(webp, 'WEBP', quality=88, method=6)
            converted.append(str(png.relative_to(BASE)))
        except Exception as e:
            errors.append(f'{png.relative_to(BASE)}: {e}')
            continue
    else:
        skipped.append(png.name)

    try:
        png.unlink()
    except Exception as e:
        errors.append(f'del {png.name}: {e}')

# Actualizar referencias PNG -> WebP en index.html
updated_html = []
pattern = re.compile(r'(\./img/[^"\'<>\s]+)\.png')
for html_file in BASE.glob('*/*/index.html'):
    content = html_file.read_text(encoding='utf-8')
    new_content = pattern.sub(r'\1.webp', content)
    if new_content != content:
        html_file.write_text(new_content, encoding='utf-8')
        updated_html.append(str(html_file.relative_to(BASE)))

print(f'Convertidos nuevos: {len(converted)}')
for c in converted:
    print(f'  + {c}')
print(f'Ya tenian WebP (solo borrado PNG): {len(skipped)}')
print(f'HTML actualizados: {len(updated_html)}')
for h in updated_html:
    print(f'  ~ {h}')
if errors:
    print(f'\nERRORES ({len(errors)}):')
    for e in errors:
        print(f'  ! {e}')
else:
    print('\nSin errores.')
