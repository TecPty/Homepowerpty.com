"""
fix_related_names.py
Fixes pdp-related-name cards where the anchor text is just the folder slug
(e.g. "2020b") instead of the real product name (e.g. "Estufa Eléctrica").

Also fixes the matching img alt="" on the related card image.

Steps:
  1. Build folder -> real_name map from each PDP's pdp-name h1
  2. Walk every HTML file
  3. Replace slug-as-text in related cards with the real name
"""

import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
PRODUCTOS = os.path.join(BASE, "productos")

# ── 1. Build the name map ────────────────────────────────────────────────────
name_map = {}   # folder_slug (lowercase) -> real product name

for root, dirs, files in os.walk(PRODUCTOS):
    for f in files:
        if f != "index.html":
            continue
        path = os.path.join(root, f)
        html = open(path, encoding="utf-8", errors="ignore").read()
        m = re.search(r'class="pdp-name"[^>]*>(.*?)<', html)
        if m:
            name = m.group(1).strip()
            folder = os.path.basename(root).lower()
            name_map[folder] = name

print("=== Name map built ===")
for k, v in sorted(name_map.items()):
    print(f"  {k:20s} -> {v}")

# ── 2. Fix related cards ─────────────────────────────────────────────────────
# Pattern: anchor text equals the folder slug (case-insensitive)
# <a href="../SLUG/">SLUG_TEXT</a>
RE_ANCHOR = re.compile(
    r'(<h3 class="pdp-related-name"><a href="[^"]+/([^/"]+)/")>([^<]+)(</a></h3>)',
    re.IGNORECASE
)
# Pattern: img alt equals the folder slug on a related-img-wrap
# <img src="../SLUG/img/..." alt="SLUG_TEXT" loading="lazy">
RE_IMG_ALT = re.compile(
    r'(<img\s[^>]*src="[^"]*\/([^/"]+)\/img\/[^"]*"[^>]*alt=")([^"]+)(")',
    re.IGNORECASE
)

files_changed = []
total_replacements = 0

for root, dirs, files in os.walk(PRODUCTOS):
    for f in files:
        if f != "index.html":
            continue
        path = os.path.join(root, f)
        original = open(path, encoding="utf-8", errors="ignore").read()
        updated = original

        # Fix <h3 class="pdp-related-name"> anchor text
        def fix_anchor(m):
            prefix, slug, text, suffix = m.group(1), m.group(2), m.group(3), m.group(4)
            key = slug.lower()
            if key in name_map and text.strip().lower() == key:
                return f'{prefix}>{name_map[key]}{suffix}'
            return m.group(0)

        updated = RE_ANCHOR.sub(fix_anchor, updated)

        # Fix img alt on related card images (only when alt == slug)
        def fix_img_alt(m):
            prefix, slug, alt_text, suffix = m.group(1), m.group(2), m.group(3), m.group(4)
            key = slug.lower()
            if key in name_map and alt_text.strip().lower() == key:
                return f'{prefix}{name_map[key]}{suffix}'
            return m.group(0)

        updated = RE_IMG_ALT.sub(fix_img_alt, updated)

        if updated != original:
            open(path, "w", encoding="utf-8").write(updated)
            rel = os.path.relpath(path, BASE)
            files_changed.append(rel)
            # Count replacements (rough)
            total_replacements += original.count('\n') - updated.count('\n') + abs(len(updated) - len(original))
            print(f"  FIXED: {rel}")

print(f"\n=== Done: {len(files_changed)} files updated ===")
