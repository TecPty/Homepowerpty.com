"""
catalog_visual.py  v2
Genera un HTML interactivo para mapear imágenes de PRODUCTOS-IMAGENES/ a SKUs vacíos.
Usa índices numéricos para evitar problemas de escaping con paths de Windows.
"""
import json
import re
from pathlib import Path

ROOT    = Path(__file__).parent.parent
STAGING = ROOT / "PRODUCTOS-IMAGENES" / "PRODUCTOS"
PRODUCTOS = ROOT / "productos"
OUT     = ROOT / "tools" / "catalog_visual.html"

IMG_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".PNG", ".JPG", ".JPEG", ".WEBP"}


# ---------------------------------------------------------------------------
# Recolección de datos
# ---------------------------------------------------------------------------

def collect_source_images():
    images = []
    for f in sorted(STAGING.rglob("*")):
        if f.suffix in IMG_EXTS and f.is_file():
            rel_fwd = str(f.relative_to(ROOT)).replace("\\", "/")
            src     = "../" + rel_fwd           # relativo desde tools/
            group   = f.parent.name if f.parent != STAGING else "raíz"
            images.append({"name": f.name, "src": src, "group": group, "path": rel_fwd})
    return images


def collect_empty_skus():
    empty = []
    for cat_dir in sorted(PRODUCTOS.iterdir()):
        if not cat_dir.is_dir():
            continue
        for sku_dir in sorted(cat_dir.iterdir()):
            if not sku_dir.is_dir():
                continue
            img_dir = sku_dir / "img"
            count   = len(list(img_dir.glob("*"))) if img_dir.exists() else 0
            if count == 0:
                empty.append({
                    "sku":       sku_dir.name,
                    "categoria": cat_dir.name,
                    "nombre":    _read_product_name(sku_dir / "index.html"),
                    "path":      str(sku_dir.relative_to(ROOT)).replace("\\", "/"),
                })
    return empty


def _read_product_name(html_path):
    if not html_path.exists():
        return ""
    try:
        text = html_path.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r'<h1[^>]*class="[^"]*pdp-title[^"]*"[^>]*>(.*?)</h1>', text, re.S)
        if m:
            return re.sub(r'<[^>]+>', '', m.group(1)).strip()
        m = re.search(r'<title>(.*?)</title>', text, re.S)
        if m:
            return re.sub(r'<[^>]+>', '', m.group(1)).strip()
    except Exception:
        pass
    return ""


# ---------------------------------------------------------------------------
# Renderizado HTML
# ---------------------------------------------------------------------------

def render_groups(groups: dict, idx_map: dict) -> str:
    """Grillas de imágenes usando data-idx numérico — sin escaping de paths."""
    parts = []
    for group_name in sorted(groups.keys()):
        imgs = groups[group_name]
        parts.append(f'<div class="group-title">{_esc(group_name)} ({len(imgs)})</div>')
        parts.append('<div class="img-grid">')
        for img in imgs:
            idx  = idx_map[img["path"]]
            parts.append(
                f'<div class="img-card" id="img-{idx}" data-idx="{idx}"'
                f' data-name="{_esc(img["name"].lower())}" data-group="{_esc(img["group"])}"'
                f' onclick="openModal({idx})">'
                f'<img src="{_esc(img["src"])}" alt="{_esc(img["name"])}" loading="lazy"'
                f' onerror="this.parentElement.style.opacity=\'0.4\'">'
                f'<div class="img-name">{_esc(img["name"])}</div>'
                f'</div>'
            )
        parts.append('</div>')
    return "\n".join(parts)


def render_skus(cats: dict) -> str:
    parts = []
    for cat in sorted(cats.keys()):
        parts.append(f'<div class="sku-cat">{_esc(cat)}</div>')
        for s in cats[cat]:
            nombre = _esc(s["nombre"]) if s["nombre"] else "(sin nombre)"
            parts.append(
                f'<div class="sku-item" data-sku="{_esc(s["sku"])}">'
                f'<div class="sku-code">{_esc(s["sku"])}</div>'
                f'<div class="sku-name">{nombre}</div>'
                f'</div>'
            )
    return "\n".join(parts)


def _esc(s: str) -> str:
    """Escapa caracteres HTML básicos para atributos y contenido."""
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------------------
# Generación del HTML final
# ---------------------------------------------------------------------------

def generate():
    source_images = collect_source_images()
    empty_skus    = collect_empty_skus()

    groups  = {}
    for img in source_images:
        groups.setdefault(img["group"], []).append(img)

    cats = {}
    for s in empty_skus:
        cats.setdefault(s["categoria"], []).append(s)

    idx_map     = {img["path"]: i for i, img in enumerate(source_images)}
    imgs_json   = json.dumps(source_images, ensure_ascii=False)
    skus_json   = json.dumps(empty_skus,    ensure_ascii=False)
    groups_opts = "\n".join(
        f'<option value="{_esc(g)}">{_esc(g)}</option>'
        for g in sorted(groups.keys())
    )

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Catálogo Visual — Home Power</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: system-ui, sans-serif; background: #0f0f0f; color: #eee; }}
h1 {{ padding: 18px 24px 6px; font-size: 20px; color: #D6B55E; }}
.subtitle {{ padding: 0 24px 14px; color: #888; font-size: 12px; }}

/* Toolbar */
.toolbar {{ padding: 9px 20px; background: #1a1a1a; border-bottom: 1px solid #222;
            display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }}
.search-box {{ background: #222; border: 1px solid #333; color: #eee; padding: 6px 10px;
               border-radius: 6px; font-size: 12px; width: 190px; }}
select {{ background: #222; border: 1px solid #333; color: #eee; padding: 5px 8px;
          border-radius: 6px; font-size: 12px; }}
label {{ font-size: 11px; color: #888; }}
.btn {{ background: #D6B55E; color: #000; border: none; padding: 7px 13px;
        border-radius: 6px; font-size: 12px; font-weight: 700; cursor: pointer; }}
.btn:hover {{ background: #b49542; }}
.btn-sec {{ background: #333; color: #eee; border: 1px solid #444; }}
.btn-sec:hover {{ background: #444; }}
.status-bar {{ margin-left: auto; font-size: 11px; color: #888;
               max-width: 280px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}

/* Layout */
.layout {{ display: grid; grid-template-columns: 1fr 320px; height: calc(100vh - 106px); }}

/* Panel imágenes */
.panel-images {{ overflow-y: auto; padding: 14px 18px; border-right: 1px solid #222; }}
.group-title {{ font-size: 11px; font-weight: 700; text-transform: uppercase; color: #D6B55E;
                letter-spacing: 1px; margin: 18px 0 8px; border-bottom: 1px solid #2a2a2a; padding-bottom: 4px; }}
.img-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 8px; }}
.img-card {{ background: #1a1a1a; border: 2px solid #2a2a2a; border-radius: 8px; overflow: hidden;
             cursor: pointer; transition: border-color .2s, transform .15s; position: relative; }}
.img-card:hover {{ border-color: #D6B55E; transform: translateY(-2px); }}
.img-card.assigned {{ border-color: #4CAF50; }}
.img-card img {{ width: 100%; aspect-ratio: 1; object-fit: contain; background: #fff; padding: 4px; display: block; }}
.img-name {{ font-size: 9px; color: #999; padding: 3px 5px; line-height: 1.3; word-break: break-word; }}
.badge {{ position: absolute; top: 4px; right: 4px; background: #4CAF50;
          color: #fff; font-size: 9px; padding: 1px 5px; border-radius: 3px; font-weight: 700;
          max-width: 88%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}

/* Panel SKUs */
.panel-skus {{ overflow-y: auto; padding: 14px; background: #111; }}
.panel-skus h2 {{ font-size: 13px; color: #D6B55E; margin-bottom: 10px; }}
.sku-cat {{ font-size: 10px; font-weight: 700; text-transform: uppercase; color: #555;
            letter-spacing: 1px; margin: 14px 0 5px; }}
.sku-item {{ background: #1a1a1a; border: 1px solid #252525; border-radius: 6px;
             padding: 7px 10px; margin-bottom: 5px; }}
.sku-item.has-mapping {{ border-color: #4CAF50; background: #0d1a0d; }}
.sku-code {{ font-size: 12px; font-weight: 700; color: #D6B55E; font-family: monospace; }}
.sku-name {{ font-size: 11px; color: #999; margin-top: 2px; }}
.sku-mapped {{ font-size: 10px; color: #4CAF50; margin-top: 3px; }}

/* Modal */
.modal {{ display: none; position: fixed; inset: 0; background: rgba(0,0,0,.78);
          align-items: center; justify-content: center; z-index: 100; }}
.modal.open {{ display: flex; }}
.modal-box {{ background: #1c1c1c; border: 1px solid #3a3a3a; border-radius: 12px;
              padding: 22px; max-width: 480px; width: 92%; max-height: 88vh; overflow-y: auto; }}
.modal-box h3 {{ color: #D6B55E; margin-bottom: 10px; font-size: 14px;
                 word-break: break-all; padding-right: 28px; }}
.close-btn {{ float: right; background: none; border: none; color: #777; font-size: 22px;
              cursor: pointer; margin: -4px -4px 0 0; line-height: 1; }}
.close-btn:hover {{ color: #eee; }}
.modal-img {{ width: 100%; max-height: 170px; object-fit: contain; background: #fff;
              border-radius: 8px; padding: 8px; margin-bottom: 12px; display: block; }}
.modal-hint {{ font-size: 11px; color: #777; margin-bottom: 10px; }}
.modal-sku {{ padding: 8px 12px; border-radius: 6px; cursor: pointer; margin-bottom: 5px;
              border: 1px solid #2a2a2a; transition: background .15s, border-color .15s; }}
.modal-sku:hover {{ background: rgba(214,181,94,.12); border-color: #D6B55E; }}
.modal-sku.done {{ border-color: #4CAF50; }}
.modal-sku .code {{ font-family: monospace; font-weight: 700; color: #D6B55E; font-size: 12px; }}
.modal-sku .mname {{ color: #888; font-size: 11px; margin-top: 2px; }}

/* Export */
.export-area {{ display: none; padding: 12px 22px; background: #0b170b; border-top: 1px solid #1e3a1e; }}
.export-area h4 {{ color: #4CAF50; margin-bottom: 8px; font-size: 12px; }}
pre {{ font-size: 11px; color: #bbb; white-space: pre-wrap; word-break: break-all;
       background: #111; padding: 10px; border-radius: 6px; max-height: 180px; overflow-y: auto; }}
</style>
</head>
<body>

<h1>Catálogo Visual — Home Power PTY</h1>
<p class="subtitle">{len(source_images)} imágenes fuente &nbsp;·&nbsp; {len(empty_skus)} SKUs sin imágenes &nbsp;·&nbsp; Clic en imagen → elegís el SKU</p>

<div class="toolbar">
  <input class="search-box" id="searchBox" placeholder="Buscar imagen..." oninput="filterImages()">
  <label>Grupo:</label>
  <select id="groupFilter" onchange="filterImages()">
    <option value="">Todos</option>
    {groups_opts}
  </select>
  <button class="btn btn-sec" onclick="clearSelection()">Limpiar</button>
  <button class="btn" onclick="toggleExport()">Exportar mappings</button>
  <span class="status-bar" id="statusBar">Clic en una imagen para asignarla a un SKU</span>
</div>

<div id="exportArea" class="export-area">
  <h4>Mappings listos para deploy_images_confident.py</h4>
  <pre id="exportContent"></pre>
  <button class="btn btn-sec" onclick="copyExport()" style="margin-top:8px">Copiar al portapapeles</button>
</div>

<div class="layout">
  <div class="panel-images" id="imagePanel">
    {render_groups(groups, idx_map)}
  </div>
  <div class="panel-skus">
    <h2>SKUs sin imágenes ({len(empty_skus)})</h2>
    {render_skus(cats)}
  </div>
</div>

<!-- Modal -->
<div class="modal" id="modal" onclick="if(event.target===this)closeModal()">
  <div class="modal-box">
    <button class="close-btn" onclick="closeModal()">&#x2715;</button>
    <h3 id="modalTitle"></h3>
    <img class="modal-img" id="modalImg" src="" alt="">
    <p class="modal-hint">&#191;A cu&#225;l SKU pertenece esta imagen?</p>
    <div id="modalSkuList"></div>
  </div>
</div>

<script>
const SOURCE_IMAGES = {imgs_json};
const EMPTY_SKUS    = {skus_json};

const mappings = {{}};   // {{imgIdx: [skuCode, ...]}}
let selectedIdx = null;

// Abrir modal al clicar imagen
function openModal(idx) {{
  const img = SOURCE_IMAGES[idx];
  if (!img) {{ console.error('No image at idx', idx); return; }}
  selectedIdx = idx;

  document.getElementById('modalImg').src = img.src;
  document.getElementById('modalTitle').textContent = img.name;

  const assigned = mappings[idx] || [];
  document.getElementById('modalSkuList').innerHTML = EMPTY_SKUS.map(function(s) {{
    const done = assigned.includes(s.sku) ? ' done' : '';
    const check = assigned.includes(s.sku) ? ' ✓' : '';
    return '<div class="modal-sku' + done + '" onclick="assignToSku(\'' + esc(s.sku) + '\')">'
         + '<div class="code">' + esc(s.sku) + check + '</div>'
         + '<div class="mname">' + esc(s.categoria) + ' — ' + esc(s.nombre || '(sin nombre)') + '</div>'
         + '</div>';
  }}).join('');

  document.getElementById('modal').classList.add('open');
  document.getElementById('statusBar').textContent = 'Elegí el SKU al que pertenece esta imagen';
}}

function closeModal() {{
  document.getElementById('modal').classList.remove('open');
}}

// Asignar imagen seleccionada a un SKU
function assignToSku(skuCode) {{
  if (selectedIdx === null) return;

  if (!mappings[selectedIdx]) mappings[selectedIdx] = [];
  if (!mappings[selectedIdx].includes(skuCode)) mappings[selectedIdx].push(skuCode);

  // Actualizar tarjeta de imagen
  const card = document.getElementById('img-' + selectedIdx);
  if (card) {{
    card.classList.add('assigned');
    let badge = card.querySelector('.badge');
    if (!badge) {{ badge = document.createElement('div'); badge.className = 'badge'; card.appendChild(badge); }}
    badge.textContent = mappings[selectedIdx].join(', ');
  }}

  // Actualizar fila del SKU en panel derecho
  const skuEl = document.querySelector('[data-sku="' + skuCode + '"]');
  if (skuEl) {{
    skuEl.classList.add('has-mapping');
    let mapped = skuEl.querySelector('.sku-mapped');
    if (!mapped) {{ mapped = document.createElement('div'); mapped.className = 'sku-mapped'; skuEl.appendChild(mapped); }}
    const names = Object.keys(mappings)
      .filter(function(k) {{ return mappings[k].includes(skuCode); }})
      .map(function(k) {{ return SOURCE_IMAGES[k].name; }});
    mapped.textContent = '→ ' + names.join(', ');
  }}

  document.getElementById('statusBar').textContent =
    '✓ ' + SOURCE_IMAGES[selectedIdx].name + ' → ' + skuCode;
  closeModal();
}}

// Filtros
function filterImages() {{
  const q = document.getElementById('searchBox').value.toLowerCase();
  const g = document.getElementById('groupFilter').value;
  document.querySelectorAll('.img-card').forEach(function(card) {{
    const ok = (!q || card.dataset.name.includes(q)) && (!g || card.dataset.group === g);
    card.style.display = ok ? '' : 'none';
  }});
}}

function clearSelection() {{
  selectedIdx = null;
  document.getElementById('statusBar').textContent = 'Selección limpiada';
}}

// Export
function toggleExport() {{
  if (Object.keys(mappings).length === 0) {{ alert('Todavía no asignaste ninguna imagen.'); return; }}
  const lines = [];
  Object.keys(mappings).forEach(function(k) {{
    const img  = SOURCE_IMAGES[parseInt(k)];
    mappings[k].forEach(function(sku) {{
      const s   = EMPTY_SKUS.find(function(x){{return x.sku===sku;}});
      const cat = s ? s.categoria : '???';
      lines.push('    # ' + img.name + ' -> ' + sku);
      lines.push('    ("' + img.path + '", "productos/' + cat + '/' + sku + '/img/PRODUCTO_PRINCIPAL"),');
    }});
  }});
  document.getElementById('exportContent').textContent = lines.join('\\n');
  const area = document.getElementById('exportArea');
  area.style.display = area.style.display === 'block' ? 'none' : 'block';
}}

function copyExport() {{
  navigator.clipboard.writeText(document.getElementById('exportContent').textContent)
    .then(function(){{ alert('¡Copiado!'); }});
}}

// Helpers
function esc(s) {{
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}}

document.addEventListener('keydown', function(e) {{ if (e.key === 'Escape') closeModal(); }});
</script>
</body>
</html>
"""
    OUT.write_text(html, encoding="utf-8")
    print(f"✅  Catálogo generado: {OUT}")
    print(f"    {len(source_images)} imágenes · {len(empty_skus)} SKUs sin imágenes")
    print(f"    Abrilo en: http://localhost:8080/tools/catalog_visual.html")


if __name__ == "__main__":
    generate()
