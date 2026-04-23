"""
patch_pdp_mobile_nav.py
Adds hamburger button + fullscreen menu + header.js to all PDP index.html files
under productos/**/index.html.
"""
import os
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
PRODUCTOS = ROOT / "productos"

# ── What to inject after .header-actions block ─────────────────────────────
HAMBURGER_BTN = """\

            <!-- Hamburger (visible only on mobile) -->
            <button class="hamburger-btn" id="menuBurger" aria-label="Abrir menú" aria-expanded="false">
                <span></span>
                <span></span>
                <span></span>
            </button>"""

# Fullscreen menu — uses relative path back to root depending on depth
def fullscreen_menu(depth: int) -> str:
    prefix = "../" * depth  # e.g. ../../../  for depth=3
    return f"""\

    <!-- Fullscreen mobile menu -->
    <div class="fullscreen-menu" id="fullscreenMenu" role="dialog" aria-modal="true" aria-label="Menú de navegación">
        <button class="fullscreen-menu__close" id="menuClose" aria-label="Cerrar menú">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
        <nav>
            <ul class="fullscreen-menu__links">
                <li><a href="{prefix}index.html" class="fullscreen-menu-link">Inicio</a></li>
                <li><a href="{prefix}index.html#productos" class="fullscreen-menu-link">Electrodomésticos</a></li>
                <li><a href="{prefix}index.html#nosotros" class="fullscreen-menu-link">Nosotros</a></li>
                <li><a href="{prefix}index.html#clientes" class="fullscreen-menu-link">Clientes</a></li>
                <li><a href="{prefix}index.html#contacto" class="fullscreen-menu-link">Contacto</a></li>
            </ul>
        </nav>
        <a href="https://wa.me/50769838322" class="fullscreen-menu__cta" target="_blank" rel="noopener">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            Consultar
        </a>
    </div>"""

def header_js_tag(depth: int) -> str:
    prefix = "../" * depth
    return f'    <script defer src="{prefix}scripts/header.js"></script>'


def patch_file(path: Path):
    # Determine depth relative to ROOT
    # productos/licuadoras/mm-111/index.html → depth 3 from root
    try:
        rel = path.parent.relative_to(ROOT)
        depth = len(rel.parts)
    except ValueError:
        depth = 3  # fallback

    text = path.read_text(encoding="utf-8")
    changed = False

    # ── 1. Add hamburger btn before </header> ────────────────────────────
    if 'id="menuBurger"' not in text:
        # Find the closing </header> tag (first occurrence)
        header_close = text.find("</header>")
        if header_close != -1:
            # Find the </div> that closes .header-container just before </header>
            # Strategy: insert before </header>
            text = text[:header_close] + HAMBURGER_BTN + "\n        </div>\n    </header>" + text[header_close + len("</header>"):]
            # But we need to remove any extra </div></header> that was already there
            # Actually let's be more careful — find end of header-actions block
            pass
        changed = True

    # ── 1 (safer approach). Replace </div>\n    </header> end pattern ────
    # Reset and redo more carefully
    text = path.read_text(encoding="utf-8")

    if 'id="menuBurger"' not in text:
        # Match: closing of header-actions div, then closing header-container div, then </header>
        # Pattern: </div>\n        </div>\n    </header>  (last occurrence in header)
        # We'll find the header block and inject before its closing tags
        header_match = re.search(
            r'([ \t]*</div>\s*\n\s*</div>\s*\n\s*</header>)',
            text
        )
        if header_match:
            insert_at = header_match.start(1)
            # Find last occurrence before any <main> or <!-- BREADCRUMB -->
            # More robust: find all matches and use the one inside the header
            header_start = text.find('<header class="luxury-header">')
            if header_start == -1:
                header_start = text.find('<header')
            header_end = text.find('</header>', header_start) + len('</header>')
            header_block = text[header_start:header_end]

            # Find position of last </div>\n        </div>\n    </header> in header
            inner_match = list(re.finditer(
                r'([ \t]*</div>\s*\n[ \t]*</div>\s*\n[ \t]*</header>)',
                header_block
            ))
            if inner_match:
                m = inner_match[-1]
                abs_pos = header_start + m.start(1)
                text = text[:abs_pos] + HAMBURGER_BTN + "\n" + text[abs_pos:]
                changed = True
                print(f"  [hamburger] Injected in {path.relative_to(ROOT)}")
            else:
                print(f"  [WARN] Could not find header closing pattern in {path.relative_to(ROOT)}")
        else:
            print(f"  [WARN] Could not match header close in {path.relative_to(ROOT)}")
    else:
        print(f"  [skip hamburger] Already present: {path.relative_to(ROOT)}")

    # ── 2. Add fullscreen menu after </header> ───────────────────────────
    if 'id="fullscreenMenu"' not in text:
        header_close = text.find("</header>")
        if header_close != -1:
            insert_pos = header_close + len("</header>")
            text = text[:insert_pos] + fullscreen_menu(depth) + text[insert_pos:]
            changed = True
            print(f"  [fullscreen-menu] Injected in {path.relative_to(ROOT)}")
    else:
        print(f"  [skip fullscreen] Already present: {path.relative_to(ROOT)}")

    # ── 3. Add header.js before </body> ──────────────────────────────────
    js_tag = f'scripts/header.js'
    if js_tag not in text:
        body_close = text.rfind("</body>")
        if body_close != -1:
            tag = header_js_tag(depth) + "\n"
            text = text[:body_close] + tag + text[body_close:]
            changed = True
            print(f"  [header.js] Injected in {path.relative_to(ROOT)}")
    else:
        print(f"  [skip header.js] Already present: {path.relative_to(ROOT)}")

    if changed:
        path.write_text(text, encoding="utf-8")


def main():
    pdp_files = sorted(PRODUCTOS.glob("**/index.html"))
    print(f"Found {len(pdp_files)} PDP files\n")
    for f in pdp_files:
        print(f"Processing: {f.relative_to(ROOT)}")
        patch_file(f)
        print()
    print("Done.")


if __name__ == "__main__":
    main()
