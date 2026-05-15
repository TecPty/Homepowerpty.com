"""
Adds <script type="module" src="../../../scripts/page.js"></script>
before </body> in all product pages that don't already have it.
"""
import os
import re
from pathlib import Path

ROOT = Path(__file__).parent
PRODUCTOS = ROOT / "productos"
SCRIPT_TAG = '    <script type="module" src="../../../scripts/page.js"></script>\n'

added = []
skipped = []

for html in sorted(PRODUCTOS.rglob("index.html")):
    content = html.read_text(encoding="utf-8")
    if "page.js" in content:
        skipped.append(html.relative_to(ROOT))
        continue
    if "</body>" not in content:
        print(f"  WARN: no </body> found in {html.relative_to(ROOT)}")
        continue
    new_content = content.replace("</body>", SCRIPT_TAG + "</body>", 1)
    html.write_text(new_content, encoding="utf-8")
    added.append(html.relative_to(ROOT))

print(f"\n✓ Added page.js to {len(added)} files")
print(f"  Already had it: {len(skipped)}")
for f in added:
    print(f"  + {f}")
