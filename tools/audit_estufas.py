import re, os

with open('C:/Users/HP 15/Homepowerpty.com/index.html', encoding='utf-8') as f:
    html = f.read()

base = 'C:/Users/HP 15/Homepowerpty.com'
pattern_src = re.compile(r'src="(productos/estufas/[^"]+)"')
pattern_box = re.compile(r'data-box="(productos/estufas/[^"]+)"')

refs = set(pattern_src.findall(html)) | set(pattern_box.findall(html))
for ref in sorted(refs):
    full = os.path.join(base, ref.replace('/', os.sep))
    status = 'OK   ' if os.path.exists(full) else 'BROKEN'
    print(f'[{status}] {ref}')
