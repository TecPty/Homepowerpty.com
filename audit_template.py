#!/usr/bin/env python3
"""
audit_template.py
=================
Audita todas las páginas de producto contra la plantilla de referencia (hp-048).

Verifica:
  1.  pdp-main-img-wrap cierra ANTES de pdp-thumbs            [CRÍTICO]
  2.  pdp-thumbs existe                                        [CRÍTICO]
  3.  pdp-gallery-strip-grid existe                            [CRÍTICO]
  4.  pdp-lightbox existe                                      [CRÍTICO]
  5.  pdpImages array en <script>                              [CRÍTICO]
  6.  pdpOpenLightboxAt function                               [CRÍTICO]
  7.  pdp-accordion (especificaciones + envío)                 [IMPORTANTE]
  8.  pdp-trust-bar                                            [IMPORTANTE]
  9.  pdp-cta-band                                            [IMPORTANTE]
  10. pdp-related                                              [IMPORTANTE]
  11. fullscreen-menu (menú hamburguesa)                       [IMPORTANTE]
  12. pdp-breadcrumb                                           [IMPORTANTE]
  13. scripts/page.js                                          [IMPORTANTE]
  14. pdp-cta-group (botones CTA del panel derecho)            [MENOR]
  15. pdp-spec-pills                                           [MENOR]
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent

CHECKS = [
    # (id, descripción, nivel, regex/string a buscar)
    ('wrap_closes', 'pdp-main-img-wrap cierra antes de pdp-thumbs', 'CRÍTICO',  None),   # lógica especial
    ('pdp_thumbs',  'div.pdp-thumbs presente',                       'CRÍTICO',  'class="pdp-thumbs"'),
    ('gallery_strip','pdp-gallery-strip-grid presente',              'CRÍTICO',  'class="pdp-gallery-strip-grid"'),
    ('lightbox',    'pdp-lightbox presente',                         'CRÍTICO',  'id="pdpLightbox"'),
    ('pdp_images',  'array pdpImages en script',                     'CRÍTICO',  'const pdpImages'),
    ('lb_at',       'función pdpOpenLightboxAt',                     'CRÍTICO',  'pdpOpenLightboxAt'),
    ('accordion',   'pdp-accordion (specs/envío)',                   'IMPORTANTE','class="pdp-accordion"'),
    ('trust_bar',   'pdp-trust-bar',                                 'IMPORTANTE','class="pdp-trust-bar"'),
    ('cta_band',    'pdp-cta-band',                                  'IMPORTANTE','class="pdp-cta-band"'),
    ('related',     'sección pdp-related',                           'IMPORTANTE','class="pdp-related"'),
    ('hamburger',   'fullscreen-menu (hamburguesa)',                  'IMPORTANTE','id="fullscreenMenu"'),
    ('breadcrumb',  'pdp-breadcrumb',                                'IMPORTANTE','class="pdp-breadcrumb"'),
    ('page_js',     'scripts/page.js',                               'IMPORTANTE','scripts/page.js'),
    ('cta_group',   'pdp-cta-group (botones CTA)',                   'MENOR',    'class="pdp-cta-group"'),
    ('spec_pills',  'pdp-spec-pills',                                'MENOR',    'class="pdp-spec-pills"'),
]

NIVEL_ORDER = {'CRÍTICO': 0, 'IMPORTANTE': 1, 'MENOR': 2}


def check_wrap_closes_before_thumbs(content: str) -> bool:
    """
    Retorna True si pdp-main-img-wrap cierra antes de pdp-thumbs
    (estructura correcta: el div wrap tiene su </div> antes del div thumbs).
    """
    wrap_open  = content.find('id="pdpMainImgWrap"')
    if wrap_open == -1:
        wrap_open = content.find('class="pdp-main-img-wrap"')
    thumbs_open = content.find('class="pdp-thumbs"')
    if wrap_open == -1 or thumbs_open == -1:
        return True  # no podemos verificar → skip

    # Buscar el </div> entre pdp-main-img-wrap y pdp-thumbs
    segment = content[wrap_open:thumbs_open]
    # El wrap abre, tiene pdp-zoom-hint (otro div), y debería cerrar dos veces
    # Contamos aperturas y cierres de div en ese segmento
    opens  = len(re.findall(r'<div[\s>]', segment, re.IGNORECASE))
    closes = len(re.findall(r'</div>', segment, re.IGNORECASE))
    # Si opens == closes → el wrap está correctamente cerrado antes de thumbs
    return opens == closes


def audit_file(html_path: Path) -> list:
    """Retorna lista de (check_id, descripción, nivel) para cada falla."""
    content = html_path.read_text(encoding='utf-8')
    fails = []
    for check_id, desc, nivel, pattern in CHECKS:
        if check_id == 'wrap_closes':
            ok = check_wrap_closes_before_thumbs(content)
        else:
            ok = pattern in content
        if not ok:
            fails.append((check_id, desc, nivel))
    return fails


def main():
    base = ROOT / 'productos'
    results = {}  # path → lista de fallos

    for html_path in sorted(base.rglob('index.html')):
        fails = audit_file(html_path)
        if fails:
            rel = html_path.relative_to(ROOT)
            results[rel] = fails

    if not results:
        print("\n✅  Todas las plantillas están correctas.\n")
        return

    # Agrupar por nivel de severidad
    criticos   = {p: [f for f in fs if f[2] == 'CRÍTICO']   for p, fs in results.items()}
    importantes= {p: [f for f in fs if f[2] == 'IMPORTANTE'] for p, fs in results.items()}
    menores    = {p: [f for f in fs if f[2] == 'MENOR']     for p, fs in results.items()}

    total_criticos   = sum(len(v) for v in criticos.values())
    total_importantes= sum(len(v) for v in importantes.values())
    total_menores    = sum(len(v) for v in menores.values())

    print()
    print('=' * 70)
    print('  AUDITORÍA DE PLANTILLAS — HomePower PTY')
    print('=' * 70)

    if total_criticos:
        print(f'\n🔴  PROBLEMAS CRÍTICOS ({total_criticos} en {len([p for p,v in criticos.items() if v])} páginas)')
        print('─' * 70)
        for path, fails in sorted(criticos.items()):
            if fails:
                print(f'\n  📄  {path}')
                for _, desc, _ in fails:
                    print(f'       ✗  {desc}')

    if total_importantes:
        print(f'\n🟡  PROBLEMAS IMPORTANTES ({total_importantes} en {len([p for p,v in importantes.items() if v])} páginas)')
        print('─' * 70)
        for path, fails in sorted(importantes.items()):
            if fails:
                print(f'\n  📄  {path}')
                for _, desc, _ in fails:
                    print(f'       ✗  {desc}')

    if total_menores:
        print(f'\n🔵  MENORES ({total_menores} en {len([p for p,v in menores.items() if v])} páginas)')
        print('─' * 70)
        for path, fails in sorted(menores.items()):
            if fails:
                print(f'\n  📄  {path}')
                for _, desc, _ in fails:
                    print(f'       ✗  {desc}')

    print()
    print('─' * 70)
    total_pages = len([p for p,v in results.items() if v])
    print(f'  Total páginas con problemas : {total_pages}')
    print(f'  Críticos   : {total_criticos}')
    print(f'  Importantes: {total_importantes}')
    print(f'  Menores    : {total_menores}')
    print('─' * 70)
    print()


if __name__ == '__main__':
    main()
