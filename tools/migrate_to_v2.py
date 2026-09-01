#!/usr/bin/env python3
"""
migrate_to_v2.py
Converts all product pages from the old scroll-linear layout to the
new BG-style split-column layout (product-v2.css).

Usage:
    python migrate_to_v2.py           # migrates all products
    python migrate_to_v2.py --dry-run # shows what would be done, no writes
    python migrate_to_v2.py --product air-fryer-3l-AF3201  # single product
"""

import os
import re
import sys
import shutil
import argparse
from pathlib import Path
from bs4 import BeautifulSoup

# ─── CONFIG ───────────────────────────────────────────────────────────────────

ROOT = Path(__file__).parent
PRODUCTOS_DIR = ROOT / "productos"

# Category breadcrumb label derived from folder name prefix
CATEGORY_MAP = {
    "air-fryer":    "Freidoras de Aire",
    "arrocera":     "Arroceras",
    "batidora":     "Batidoras",
    "cafetera":     "Cafeteras",
    "estufa":       "Estufas",
    "freidora":     "Freidoras de Aire",
    "hornito":      "Hornitos",
    "licuadora":    "Licuadoras",
    "lochera":      "Locheras",
    "olla":         "Ollas de Presión",
    "panini":       "Sandwicheras",
    "plancha":      "Planchas",
    "sandwichera":  "Sandwicheras",
    "tetera":       "Teteras",
    "tostadora":    "Tostadoras",
}

# Known image filenames in priority order (thumbnail rail + gallery)
KNOWN_IMAGES = [
    "PRODUCTO_PRINCIPAL.png",
    "PRODUCTO_PRINCIPAL.webp",
    "LIFESTYLE_DARK.png",
    "LIFESTYLE_DARK.webp",
    "LIFESTYLE_KITCHEN.png",
    "LIFESTYLE_KITCHEN.webp",
    "DETAIL_LOGO.png",
    "DETAIL_LOGO.webp",
    "BRAND_COMMERCIAL.png",
    "BRAND_COMMERCIAL.webp",
    "CAJA.webp",
    "CAJA.png",
]

# SVG icons for spec pills (keyed by lowercase spec label)
PILL_ICONS = {
    "potencia":    '<svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M13 2L7 14h6l-1 8 7-12h-6L13 2z"/></svg>',
    "capacidad":   '<svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 8h1a4 4 0 0 1 0 8h-1"/><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"/></svg>',
    "voltaje":     '<svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/></svg>',
    "garantía":    '<svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "garantia":    '<svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "quemadores":  '<svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/></svg>',
    "temperatura": '<svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/></svg>',
    "material":    '<svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>',
    "velocidades": '<svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    "colores":     '<svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 2a10 10 0 0 1 0 20"/></svg>',
    "default":     '<svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
}

# Which specs to pick as highlighted pills, in priority order
PILL_PRIORITY = [
    "potencia", "capacidad", "voltaje", "garantía", "garantia",
    "quemadores", "temperatura", "velocidades", "material", "colores",
    "modelo",
]

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def get_category(folder_name: str) -> str:
    for prefix, label in CATEGORY_MAP.items():
        if folder_name.startswith(prefix):
            return label
    return "Electrodomésticos"


def get_available_images(img_dir: Path) -> list[str]:
    """Return list of ./img/FILENAME for each known image that exists."""
    found = []
    if not img_dir.exists():
        return found
    existing = {f.name for f in img_dir.iterdir()}
    for name in KNOWN_IMAGES:
        if name in existing:
            found.append(f"./img/{name}")
    return found


def extract_product_data(soup: BeautifulSoup) -> dict:
    """Extract all relevant data from the existing product page."""
    data = {}

    # Name — keep <br> for multi-line titles
    h1 = soup.find("h1", class_="product-hero-title")
    if h1:
        data["name_html"] = h1.decode_contents().strip()
        data["name_text"] = h1.get_text(" ").strip()
    else:
        # Fallback to <title>
        title = soup.find("title")
        raw = title.get_text() if title else "Producto"
        data["name_text"] = raw.split("—")[0].strip()
        data["name_html"] = data["name_text"]

    # Short description
    subtitle = soup.find("p", class_="product-hero-subtitle")
    if subtitle:
        data["description"] = subtitle.get_text().strip()
    else:
        meta_desc = soup.find("meta", attrs={"name": "description"})
        data["description"] = meta_desc["content"].strip() if meta_desc else ""

    # Badge
    badge = soup.find("span", class_="product-badge-label")
    data["badge"] = badge.get_text().strip() if badge else "HomePower"

    # WhatsApp URL — look in btn-solid-gold first, then btn-cta-band
    wa_link = soup.find("a", class_="btn-solid-gold")
    if not wa_link:
        wa_link = soup.find("a", class_="btn-cta-band")
    if wa_link and wa_link.get("href", "").startswith("https://wa.me"):
        data["wa_url"] = wa_link["href"]
    else:
        data["wa_url"] = "https://wa.me/50769838322"

    # All specs from table
    specs = []
    table = soup.find("table", class_="specs-table")
    if table:
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) == 2:
                key = cells[0].get_text().strip()
                val = cells[1].get_text().strip()
                specs.append((key, val))
    data["specs"] = specs

    # Model — from specs table first, then extract from folder/URL
    model = next((v for k, v in specs if k.lower() == "modelo"), None)
    if model:
        # Strip "MOD: " prefix if present
        data["model"] = re.sub(r"^MOD:\s*", "", model).strip()
    else:
        data["model"] = ""

    # Meta description fallback
    meta_desc = soup.find("meta", attrs={"name": "description"})
    data["meta_description"] = meta_desc["content"].strip() if meta_desc else data["description"]

    return data


def pick_pills(specs: list[tuple]) -> list[tuple]:
    """Pick up to 4 specs for the highlighted pill row."""
    spec_dict = {k.lower(): (k, v) for k, v in specs}
    pills = []
    for key in PILL_PRIORITY:
        if key in spec_dict and len(pills) < 4:
            pills.append(spec_dict[key])
    # If we still have < 4, fill with remaining specs
    used_keys = {k.lower() for k, v in pills}
    for k, v in specs:
        if k.lower() not in used_keys and len(pills) < 4:
            pills.append((k, v))
            used_keys.add(k.lower())
    return pills


def pill_icon(key: str) -> str:
    return PILL_ICONS.get(key.lower(), PILL_ICONS.get(key.lower().rstrip("s"), PILL_ICONS["default"]))


# ─── HTML GENERATOR ───────────────────────────────────────────────────────────

def render_thumbnails(images: list[str]) -> str:
    if not images:
        return """
                        <button class="pdp-thumb active"
                                onclick="pdpSetImage('./img/PRODUCTO_PRINCIPAL.png', this)"
                                aria-label="Ver imagen principal" role="listitem">
                            <img src="./img/PRODUCTO_PRINCIPAL.png" alt="Vista principal">
                        </button>"""
    lines = []
    for i, src in enumerate(images[:6]):  # max 6 thumbs
        active = " active" if i == 0 else ""
        alt = src.split("/")[-1].replace("_", " ").rsplit(".", 1)[0].title()
        lines.append(f"""
                        <button class="pdp-thumb{active}"
                                onclick="pdpSetImage('{src}', this)"
                                aria-label="Ver {alt}" role="listitem">
                            <img src="{src}" alt="{alt}">
                        </button>""")
    return "".join(lines)


def render_spec_pills(pills: list[tuple]) -> str:
    lines = []
    for key, val in pills:
        icon = pill_icon(key)
        lines.append(f"""
                        <div class="pdp-spec-pill">
                            <span class="pill-icon">{icon}</span>
                            <span class="pill-key">{key}</span>
                            <span class="pill-val">{val}</span>
                        </div>""")
    return "".join(lines)


def render_specs_table_rows(specs: list[tuple]) -> str:
    lines = []
    for key, val in specs:
        lines.append(f"                                            <tr><td>{key}</td><td>{val}</td></tr>")
    return "\n".join(lines)


def render_gallery_strip(images: list[str]) -> str:
    """Render up to 4 strip items (skip PRODUCTO_PRINCIPAL — already in main)."""
    strip_images = [img for img in images if "PRODUCTO_PRINCIPAL" not in img][:4]
    # If fewer than 4, pad with whatever we have
    if not strip_images:
        strip_images = images[:4]
    items = []
    for i, src in enumerate(strip_images):
        alt = src.split("/")[-1].replace("_", " ").rsplit(".", 1)[0].title()
        items.append(f"""
                        <div class="pdp-strip-item" onclick="pdpOpenLightboxAt({i})" role="button" tabindex="0" aria-label="Ampliar {alt}">
                            <img src="{src}" alt="{alt}" loading="lazy">
                            <div class="pdp-strip-overlay" aria-hidden="true">
                                <svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg>
                            </div>
                        </div>""")
    return "".join(items)


def render_js_images(images: list[str]) -> str:
    items = ",\n            ".join(f"'{img}'" for img in images)
    return f"[\n            {items},\n        ]"


def generate_html(folder_name: str, data: dict, images: list[str]) -> str:
    category = get_category(folder_name)
    name_text = data["name_text"]
    name_html = data["name_html"]
    description = data["description"]
    meta_desc = data["meta_description"]
    badge = data["badge"]
    wa_url = data["wa_url"]
    model = data["model"]
    specs = data["specs"]

    pills = pick_pills(specs)
    main_img = images[0] if images else "./img/PRODUCTO_PRINCIPAL.png"
    model_display = f"MOD: {model}" if model else ""

    # Build WhatsApp text from name
    wa_text_product = name_text.replace(" ", "%20")
    wa_cta = wa_url  # Use original URL which already has correct product text

    thumbnails_html = render_thumbnails(images)
    pills_html = render_spec_pills(pills)
    specs_rows_html = render_specs_table_rows(specs)
    gallery_strip_html = render_gallery_strip(images)
    js_images = render_js_images(images)

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="icon" href="../../media/icons/favicon/favicon-32x32.png" type="image/png">
    <title>{name_text} — HomePower PTY</title>
    <meta name="description" content="{meta_desc}">
    <meta name="robots" content="index, follow">
    <link rel="stylesheet" href="../../styles/luxury.css">
    <link rel="stylesheet" href="../../styles/product-v2.css">
</head>
<body class="product-page">

    <!-- ANNOUNCEMENT BAR -->
    <div class="announcement-bar">
        <div class="container text-center">
            <span>Stock exclusivo · Garantía 1 año · WhatsApp: (507) 6983-8322</span>
        </div>
    </div>

    <!-- NAVBAR -->
    <header class="luxury-header">
        <div class="container header-container">
            <div class="logo-container">
                <a href="../../index.html">
                    <img src="../../media/icons/logo/logo.png" alt="Home Power PTY" class="luxury-logo">
                </a>
            </div>
            <nav class="luxury-nav">
                <ul class="nav-links">
                    <li><a href="../../index.html">Inicio</a></li>
                    <li><a href="../../index.html#productos">Electrodomésticos</a></li>
                    <li><a href="../../index.html#nosotros">Nosotros</a></li>
                    <li><a href="../../index.html#clientes">Clientes</a></li>
                    <li><a href="../../index.html#contacto">Contacto</a></li>
                </ul>
            </nav>
            <div class="header-actions">
                <a href="https://wa.me/50769838322" class="btn-outline-gold" target="_blank" rel="noopener">Consultar</a>
            </div>
        </div>
    </header>

    <!-- BREADCRUMB -->
    <div class="pdp-breadcrumb">
        <div class="container">
            <nav aria-label="Breadcrumb">
                <a href="../../index.html">Inicio</a>
                <span class="crumb-sep" aria-hidden="true">›</span>
                <a href="../../index.html#productos">Electrodomésticos</a>
                <span class="crumb-sep" aria-hidden="true">›</span>
                <a href="../../index.html#productos">{category}</a>
                <span class="crumb-sep" aria-hidden="true">›</span>
                <span class="crumb-current">{name_text}</span>
            </nav>
        </div>
    </div>

    <!-- MAIN PRODUCT — SPLIT COLUMN -->
    <main>
        <section class="pdp-main">
            <div class="pdp-grid">

                <!-- LEFT: GALLERY -->
                <div class="pdp-gallery">

                    <div class="pdp-thumbs" role="list" aria-label="Imágenes del producto">{thumbnails_html}
                    </div>

                    <div class="pdp-main-img-wrap"
                         id="pdpMainImgWrap"
                         onclick="pdpOpenLightbox()"
                         role="button"
                         tabindex="0"
                         aria-label="Ampliar imagen">
                        <img id="pdpMainImg"
                             src="{main_img}"
                             alt="{name_text} — HomePower PTY">
                        <div class="pdp-zoom-hint" aria-hidden="true">
                            <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg>
                            Ampliar
                        </div>
                    </div>

                </div>

                <!-- RIGHT: INFO PANEL -->
                <div class="pdp-info">

                    <span class="pdp-badge">{badge}</span>
                    <p class="pdp-brand">HomePower PTY</p>
                    <h1 class="pdp-name">{name_html}</h1>
                    {f'<p class="pdp-model">{model_display}</p>' if model_display else ''}

                    <div class="pdp-divider" aria-hidden="true"></div>

                    <p class="pdp-short-desc">{description}</p>

                    <div class="pdp-spec-pills">{pills_html}
                    </div>

                    <div class="pdp-cta-group">
                        <a href="{wa_cta}"
                           class="pdp-btn-primary"
                           target="_blank"
                           rel="noopener">
                            <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.123.555 4.116 1.527 5.842L0 24l6.335-1.652A11.954 11.954 0 0 0 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.818a9.818 9.818 0 0 1-5.013-1.376l-.36-.214-3.727.977.992-3.626-.235-.373A9.818 9.818 0 1 1 12 21.818z"/></svg>
                            Solicitar cotización B2B
                        </a>
                        <a href="../../index.html#productos" class="pdp-btn-secondary">
                            <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
                            Ver más productos
                        </a>
                    </div>

                    <!-- ACCORDION -->
                    <div class="pdp-accordion">

                        <div class="pdp-accordion-item">
                            <button class="pdp-accordion-trigger open"
                                    onclick="pdpToggle(this)"
                                    aria-expanded="true"
                                    aria-controls="acc-specs">
                                Especificaciones técnicas
                                <svg class="pdp-accordion-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" aria-hidden="true"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                            </button>
                            <div class="pdp-accordion-body open" id="acc-specs" role="region">
                                <div class="pdp-accordion-content">
                                    <table class="pdp-specs-table">
                                        <tbody>
{specs_rows_html}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>

                        <div class="pdp-accordion-item">
                            <button class="pdp-accordion-trigger"
                                    onclick="pdpToggle(this)"
                                    aria-expanded="false"
                                    aria-controls="acc-shipping">
                                Distribución y envío
                                <svg class="pdp-accordion-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" aria-hidden="true"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                            </button>
                            <div class="pdp-accordion-body" id="acc-shipping" role="region">
                                <div class="pdp-accordion-content">
                                    <div class="pdp-shipping-list">
                                        <div class="pdp-shipping-item">
                                            <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>
                                            <div>
                                                <strong>Entrega en 2 días hábiles</strong>
                                                Logística directa para distribuidores en toda la República de Panamá.
                                            </div>
                                        </div>
                                        <div class="pdp-shipping-item">
                                            <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1"/></svg>
                                            <div>
                                                <strong>Factura disponible</strong>
                                                Documentación formal para empresas, cadenas y distribuidores.
                                            </div>
                                        </div>
                                        <div class="pdp-shipping-item">
                                            <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg>
                                            <div>
                                                <strong>Stock exclusivo</strong>
                                                Importado directo. No disponible en retail masivo.
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>

                </div>

            </div>
        </section>

        <!-- GALLERY STRIP + TRUST + CTA -->
        <div class="pdp-below">

            <section class="pdp-gallery-strip">
                <div class="container">
                    <p class="section-eyebrow pdp-gallery-eyebrow">GALERÍA COMPLETA</p>
                    <div class="pdp-gallery-strip-grid">{gallery_strip_html}
                    </div>
                </div>
            </section>

            <section class="pdp-trust-bar">
                <div class="container">
                    <div class="pdp-trust-row">
                        <div class="pdp-trust-cell">
                            <div class="pdp-trust-cell-icon">
                                <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>
                            </div>
                            <div>
                                <h4>2 días de entrega</h4>
                                <p>Logística directa a distribuidores en Panamá</p>
                            </div>
                        </div>
                        <div class="pdp-trust-cell">
                            <div class="pdp-trust-cell-icon">
                                <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1"/></svg>
                            </div>
                            <div>
                                <h4>Factura disponible</h4>
                                <p>Documentación para empresas y cadenas</p>
                            </div>
                        </div>
                        <div class="pdp-trust-cell">
                            <div class="pdp-trust-cell-icon">
                                <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg>
                            </div>
                            <div>
                                <h4>Importado directo</h4>
                                <p>Stock exclusivo — no disponible en retail masivo</p>
                            </div>
                        </div>
                        <div class="pdp-trust-cell">
                            <div class="pdp-trust-cell-icon">
                                <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                            </div>
                            <div>
                                <h4>Soporte 24/7</h4>
                                <p>WhatsApp — respuesta en menos de 30 min</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section class="pdp-cta-band">
                <div class="container">
                    <h2>¿Listo para incluir este producto<br>en su catálogo?</h2>
                    <p>Cotización B2B personalizada para distribuidores. Respuesta en menos de 10 minutos.</p>
                    <a href="{wa_cta}"
                       class="pdp-btn-primary pdp-btn-cta-centered"
                       target="_blank"
                       rel="noopener">
                        <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.123.555 4.116 1.527 5.842L0 24l6.335-1.652A11.954 11.954 0 0 0 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.818a9.818 9.818 0 0 1-5.013-1.376l-.36-.214-3.727.977.992-3.626-.235-.373A9.818 9.818 0 1 1 12 21.818z"/></svg>
                        Consultar precio B2B
                    </a>
                    <p class="pdp-cta-note">Sin compromiso · Toda Panamá · Stock disponible</p>
                </div>
            </section>

        </div>
    </main>

    <!-- FOOTER -->
    <footer class="luxury-footer">
        <div class="container footer-container">
            <div class="footer-col" style="align-items:flex-start;">
                <img src="../../media/icons/logo/logo.png" alt="Home Power PTY" style="max-height:40px; margin-bottom:20px;">
                <p>(507) 6983-8322</p>
                <p>ventas@homepowerpty.com</p>
            </div>
            <div class="footer-col" style="flex-direction:column; align-items:flex-start; gap:10px;">
                <a href="../../index.html">Inicio</a>
                <a href="../../index.html#productos">Electrodomésticos</a>
                <a href="../../index.html#clientes">Clientes</a>
                <a href="../../index.html#contacto">Contacto</a>
            </div>
            <div class="footer-col" style="align-items:flex-end;">
                <p style="font-size:0.8rem; color:gray;">© 2025 HomePower PTY.<br>Todos los derechos reservados.</p>
            </div>
        </div>
    </footer>

    <!-- LIGHTBOX -->
    <div class="pdp-lightbox" id="pdpLightbox" role="dialog" aria-modal="true" aria-label="Visor de imágenes">
        <button class="pdp-lightbox-close" onclick="pdpCloseLightbox()" aria-label="Cerrar visor">✕</button>
        <button class="pdp-lightbox-prev" onclick="pdpLightboxMove(-1)" aria-label="Imagen anterior">&#8592;</button>
        <img class="pdp-lightbox-img" id="pdpLightboxImg" src="" alt="Imagen ampliada del producto">
        <button class="pdp-lightbox-next" onclick="pdpLightboxMove(1)" aria-label="Imagen siguiente">&#8594;</button>
    </div>

    <script>
        const pdpImages = {js_images};
        let pdpLightboxIndex = 0;
        let currentLightboxSrc = pdpImages[0] || '';

        function pdpSetImage(src, thumbEl) {{
            const mainImg = document.getElementById('pdpMainImg');
            mainImg.style.opacity = '0';
            setTimeout(() => {{ mainImg.src = src; mainImg.style.opacity = '1'; }}, 150);
            document.querySelectorAll('.pdp-thumb').forEach(t => t.classList.remove('active'));
            thumbEl.classList.add('active');
            currentLightboxSrc = src;
        }}

        function pdpOpenLightbox() {{
            const idx = pdpImages.indexOf(currentLightboxSrc);
            pdpLightboxIndex = idx >= 0 ? idx : 0;
            document.getElementById('pdpLightboxImg').src = pdpImages[pdpLightboxIndex];
            document.getElementById('pdpLightbox').classList.add('active');
            document.body.style.overflow = 'hidden';
        }}

        function pdpOpenLightboxAt(index) {{
            pdpLightboxIndex = index;
            document.getElementById('pdpLightboxImg').src = pdpImages[index];
            document.getElementById('pdpLightbox').classList.add('active');
            document.body.style.overflow = 'hidden';
        }}

        function pdpCloseLightbox() {{
            document.getElementById('pdpLightbox').classList.remove('active');
            document.body.style.overflow = '';
        }}

        function pdpLightboxMove(dir) {{
            pdpLightboxIndex = (pdpLightboxIndex + dir + pdpImages.length) % pdpImages.length;
            document.getElementById('pdpLightboxImg').src = pdpImages[pdpLightboxIndex];
        }}

        document.getElementById('pdpLightbox').addEventListener('click', function(e) {{
            if (e.target === this) pdpCloseLightbox();
        }});

        document.addEventListener('keydown', e => {{
            if (!document.getElementById('pdpLightbox').classList.contains('active')) return;
            if (e.key === 'Escape') pdpCloseLightbox();
            if (e.key === 'ArrowLeft') pdpLightboxMove(-1);
            if (e.key === 'ArrowRight') pdpLightboxMove(1);
        }});

        document.getElementById('pdpMainImgWrap').addEventListener('keydown', e => {{
            if (e.key === 'Enter') pdpOpenLightbox();
        }});

        function pdpToggle(trigger) {{
            const item = trigger.closest('.pdp-accordion-item');
            const body = item.querySelector('.pdp-accordion-body');
            const isOpen = body.classList.contains('open');
            document.querySelectorAll('.pdp-accordion-body.open').forEach(b => {{
                b.classList.remove('open');
                b.previousElementSibling.classList.remove('open');
                b.previousElementSibling.setAttribute('aria-expanded', 'false');
            }});
            if (!isOpen) {{
                body.classList.add('open');
                trigger.classList.add('open');
                trigger.setAttribute('aria-expanded', 'true');
            }}
        }}
    </script>

</body>
</html>
"""


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def migrate_product(folder: Path, dry_run: bool = False) -> str:
    """Migrate a single product folder. Returns status string."""
    index_path = folder / "index.html"
    backup_path = folder / "index-backup.html"
    img_dir = folder / "img"

    if not index_path.exists():
        return f"  SKIP  {folder.name}  — no index.html"

    # Read and parse existing HTML
    html = index_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    # Skip if already migrated (check for product-v2.css link)
    already_v2 = any(
        "product-v2.css" in (tag.get("href", ""))
        for tag in soup.find_all("link", rel="stylesheet")
    )
    if already_v2:
        return f"  SKIP  {folder.name}  — already v2"

    data = extract_product_data(soup)
    images = get_available_images(img_dir)

    new_html = generate_html(folder.name, data, images)

    if dry_run:
        pills = pick_pills(data["specs"])
        pill_labels = ", ".join(k for k, v in pills)
        return (
            f"  DRY   {folder.name}\n"
            f"         name={data['name_text']!r}\n"
            f"         model={data['model']!r}\n"
            f"         images={len(images)}\n"
            f"         pills={pill_labels!r}"
        )

    # Backup original
    if not backup_path.exists():
        shutil.copy2(index_path, backup_path)

    # Write new
    index_path.write_text(new_html, encoding="utf-8")
    return f"  OK    {folder.name}  ({len(images)} img, {len(data['specs'])} specs)"


def main():
    parser = argparse.ArgumentParser(description="Migrate product pages to v2 layout")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--product", metavar="FOLDER", help="Migrate a single product folder")
    args = parser.parse_args()

    if args.product:
        folders = [PRODUCTOS_DIR / args.product]
    else:
        folders = sorted(
            p for p in PRODUCTOS_DIR.iterdir()
            if p.is_dir() and (p / "index.html").exists()
        )

    ok = skip = error = 0
    for folder in folders:
        try:
            result = migrate_product(folder, dry_run=args.dry_run)
            print(result)
            if "OK" in result:
                ok += 1
            else:
                skip += 1
        except Exception as e:
            print(f"  ERROR {folder.name}: {e}")
            error += 1

    if not args.dry_run:
        print(f"\n  ✓ {ok} migrated  |  {skip} skipped  |  {error} errors")
    else:
        print(f"\n  Dry-run complete: {ok + skip} products checked.")


if __name__ == "__main__":
    main()
