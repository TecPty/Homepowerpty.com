"""
catalog_visual.py
Genera un HTML interactivo para mapear imágenes de PRODUCTOS-IMAGENES/ a SKUs vacíos.
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
STAGING = ROOT / "PRODUCTOS-IMAGENES" / "PRODUCTOS"
PRODUCTOS = ROOT / "productos"
OUT = ROOT / "tools" / "catalog_visual.html"

IMG_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".PNG", ".JPG", ".JPEG", ".WEBP"}

# --- Recolectar imágenes fuente ---
def collect_source_images():
    images = []
    for f in sorted(STAGING.rglob("*")):
        if f.suffix in IMG_EXTS and f.is_file():
            rel = f.relative_to(ROOT)
            rel_fwd = str(rel).replace("\\", "/")   # siempre forward slash
            src = "../" + rel_fwd                    # relativo desde tools/
            group = f.parent.name if f.parent != STAGING else "raíz"
            images.append({"name": f.name, "src": src, "group": group, "path": rel_fwd})
    return images

# --- Recolectar SKUs sin imágenes ---
def collect_empty_skus():
    empty = []
    for cat_dir in sorted(PRODUCTOS.iterdir()):
        if not cat_dir.is_dir():
            continue
        for sku_dir in sorted(cat_dir.iterdir()):
            if not sku_dir.is_dir():
                continue
            img_dir = sku_dir / "img"
            count = len(list(img_dir.glob("*"))) if img_dir.exists() else 0
            if count == 0:
                # Intentar leer nombre del producto desde index.html
                name = _read_product_name(sku_dir / "index.html")
                empty.append({
                    "sku": sku_dir.name,
                    "categoria": cat_dir.name,
                    "nombre": name,
                    "path": str(sku_dir.relative_to(ROOT)).replace("\\", "/")
                })
    return empty

def _read_product_name(html_path):
    if not html_path.exists():
        return ""
    try:
        text = html_path.read_text(encoding="utf-8", errors="ignore")
        import re
        m = re.search(r'<h1[^>]*class="[^"]*pdp-title[^"]*"[^>]*>(.*?)</h1>', text, re.S)
        if m:
            return re.sub(r'<[^>]+>', '', m.group(1)).strip()
        m = re.search(r'<title>(.*?)</title>', text, re.S)
        if m:
            return re.sub(r'<[^>]+>', '', m.group(1)).strip()
    except Exception:
        pass
    return ""

# --- Recolectar SKUs CON imágenes (referencia) ---
def collect_filled_skus():
    filled = []
    for cat_dir in sorted(PRODUCTOS.iterdir()):
        if not cat_dir.is_dir():
            continue
        for sku_dir in sorted(cat_dir.iterdir()):
            if not sku_dir.is_dir():
                continue
            img_dir = sku_dir / "img"
            if not img_dir.exists():
                continue
            imgs = list(img_dir.glob("*"))
            if imgs:
                filled.append({
                    "sku": sku_dir.name,
                    "categoria": cat_dir.name,
                    "count": len(imgs)
                })
    return filled

# --- Generar HTML ---
def generate():
    source_images = collect_source_images()
    empty_skus = collect_empty_skus()
    filled_skus = collect_filled_skus()

    # Grupos de imágenes
    groups = {}
    for img in source_images:
        g = img["group"]
        groups.setdefault(g, []).append(img)

    # Categorías de SKUs vacíos
    cats = {}
    for s in empty_skus:
        cats.setdefault(s["categoria"], []).append(s)

    imgs_json = json.dumps(source_images, ensure_ascii=False)
    skus_json = json.dumps(empty_skus, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Catálogo Visual — Home Power</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: system-ui, sans-serif; background: #0f0f0f; color: #eee; }}
  h1 {{ padding: 20px 24px 8px; font-size: 22px; color: #D6B55E; }}
  .subtitle {{ padding: 0 24px 20px; color: #888; font-size: 13px; }}
  .layout {{ display: grid; grid-template-columns: 1fr 340px; gap: 0; height: calc(100vh - 80px); }}

  /* Panel izquierdo — imágenes */
  .panel-images {{ overflow-y: auto; padding: 16px 20px; border-right: 1px solid #222; }}
  .group-title {{ font-size: 11px; font-weight: 700; text-transform: uppercase; color: #D6B55E;
                  letter-spacing: 1px; margin: 20px 0 10px; border-bottom: 1px solid #333; padding-bottom: 4px; }}
  .img-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 10px; }}
  .img-card {{ background: #1a1a1a; border: 2px solid #333; border-radius: 8px; overflow: hidden;
               cursor: pointer; transition: border-color .2s, transform .15s; position: relative; }}
  .img-card:hover {{ border-color: #D6B55E; transform: translateY(-2px); }}
  .img-card.selected {{ border-color: #D6B55E; background: #1e1a0e; }}
  .img-card.assigned {{ border-color: #4CAF50; opacity: .6; }}
  .img-card img {{ width: 100%; aspect-ratio: 1; object-fit: contain; background: #fff; padding: 4px; }}
  .img-name {{ font-size: 9px; color: #aaa; padding: 4px 6px; line-height: 1.3; word-break: break-word; }}
  .assigned-badge {{ position: absolute; top: 4px; right: 4px; background: #4CAF50;
                     color: #fff; font-size: 9px; padding: 2px 5px; border-radius: 4px; font-weight: 700; }}

  /* Panel derecho — SKUs */
  .panel-skus {{ overflow-y: auto; padding: 16px; background: #111; }}
  .panel-skus h2 {{ font-size: 13px; color: #D6B55E; margin-bottom: 12px; }}
  .sku-cat {{ font-size: 10px; font-weight: 700; text-transform: uppercase; color: #666;
              letter-spacing: 1px; margin: 16px 0 6px; }}
  .sku-item {{ background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 6px;
               padding: 8px 10px; margin-bottom: 6px; cursor: pointer; transition: border-color .2s; }}
  .sku-item:hover {{ border-color: #D6B55E; }}
  .sku-item.drop-target {{ border-color: #D6B55E; background: #1e1a0e; }}
  .sku-item.has-mapping {{ border-color: #4CAF50; background: #0d1a0d; }}
  .sku-code {{ font-size: 12px; font-weight: 700; color: #D6B55E; font-family: monospace; }}
  .sku-name {{ font-size: 11px; color: #aaa; margin-top: 2px; }}
  .sku-mapped {{ font-size: 10px; color: #4CAF50; margin-top: 4px; }}

  /* Toolbar */
  .toolbar {{ padding: 10px 24px; background: #1a1a1a; border-bottom: 1px solid #222;
              display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }}
  .btn {{ background: #D6B55E; color: #000; border: none; padding: 7px 14px;
          border-radius: 6px; font-size: 12px; font-weight: 700; cursor: pointer; }}
  .btn:hover {{ background: #b49542; }}
  .btn-sec {{ background: #333; color: #eee; border: 1px solid #444; }}
  .btn-sec:hover {{ background: #444; }}
  .search-box {{ background: #222; border: 1px solid #333; color: #eee; padding: 6px 10px;
                 border-radius: 6px; font-size: 12px; width: 200px; }}
  .status-bar {{ margin-left: auto; font-size: 11px; color: #666; }}

  /* Modal de asignación */
  .modal {{ display: none; position: fixed; inset: 0; background: rgba(0,0,0,.7);
            align-items: center; justify-content: center; z-index: 100; }}
  .modal.open {{ display: flex; }}
  .modal-box {{ background: #1a1a1a; border: 1px solid #333; border-radius: 12px;
                padding: 24px; max-width: 480px; width: 90%; }}
  .modal-box h3 {{ color: #D6B55E; margin-bottom: 12px; }}
  .modal-img {{ width: 100%; max-height: 200px; object-fit: contain; background: #fff;
                border-radius: 8px; padding: 8px; margin-bottom: 16px; }}
  .modal-skus {{ max-height: 300px; overflow-y: auto; }}
  .modal-sku {{ padding: 8px 12px; border-radius: 6px; cursor: pointer; margin-bottom: 4px;
                border: 1px solid #333; transition: background .15s; }}
  .modal-sku:hover {{ background: #D6B55E22; border-color: #D6B55E; }}
  .modal-sku .code {{ font-family: monospace; font-weight: 700; color: #D6B55E; font-size: 12px; }}
  .modal-sku .name {{ color: #aaa; font-size: 11px; }}
  .close-btn {{ float: right; background: none; border: none; color: #666; font-size: 20px;
                cursor: pointer; line-height: 1; }}

  /* Export */
  .export-box {{ display: none; background: #0d1a0d; border: 1px solid #4CAF50; border-radius: 8px;
                 padding: 16px; margin: 12px 0; }}
  .export-box h4 {{ color: #4CAF50; margin-bottom: 8px; font-size: 13px; }}
  pre {{ font-size: 11px; color: #aaa; white-space: pre-wrap; word-break: break-all; max-height: 300px; overflow-y: auto; }}

  .filters {{ display: flex; gap: 8px; align-items: center; }}
  label {{ font-size: 11px; color: #888; }}
  select {{ background: #222; border: 1px solid #333; color: #eee; padding: 5px 8px;
            border-radius: 6px; font-size: 12px; }}
</style>
</head>
<body>

<h1>Catálogo Visual — Home Power PTY</h1>
<p class="subtitle">{len(source_images)} imágenes fuente · {len(empty_skus)} SKUs sin imágenes · Hacé clic en una imagen y luego en el SKU para mapear</p>

<div class="toolbar">
  <input class="search-box" id="searchBox" placeholder="Buscar imagen..." oninput="filterImages()">
  <div class="filters">
    <label>Grupo:</label>
    <select id="groupFilter" onchange="filterImages()">
      <option value="">Todos</option>
      {chr(10).join(f'<option value="{g}">{g}</option>' for g in sorted(groups.keys()))}
    </select>
  </div>
  <button class="btn btn-sec" onclick="clearAll()">Limpiar selección</button>
  <button class="btn" onclick="exportMappings()">Exportar mappings</button>
  <span class="status-bar" id="statusBar">Seleccioná una imagen para empezar</span>
</div>

<div id="exportBox" class="export-box" style="margin: 0 24px;">
  <h4>Mappings para deploy_images_confident.py</h4>
  <pre id="exportContent"></pre>
  <button class="btn btn-sec" onclick="copyExport()" style="margin-top:8px">Copiar</button>
</div>

<div class="layout">
  <!-- Imágenes fuente -->
  <div class="panel-images" id="imagePanel">
    {_render_groups(groups)}
  </div>

  <!-- SKUs sin imágenes -->
  <div class="panel-skus">
    <h2>SKUs sin imágenes ({len(empty_skus)})</h2>
    {_render_skus(cats)}
  </div>
</div>

<!-- Modal -->
<div class="modal" id="modal">
  <div class="modal-box">
    <button class="close-btn" onclick="closeModal()">×</button>
    <h3 id="modalTitle">Asignar imagen a SKU</h3>
    <img class="modal-img" id="modalImg" src="" alt="">
    <p style="font-size:11px;color:#888;margin-bottom:10px">Elegí el SKU al que corresponde esta imagen:</p>
    <div class="modal-skus" id="modalSkus"></div>
  </div>
</div>

<script>
const SOURCE_IMAGES = {imgs_json};
const EMPTY_SKUS = {skus_json};

let selectedImage = null;
let mappings = {{}};  // img.path -> [sku, ...]

function renderImages(images) {{
  // ya renderizado en servidor, solo inicializar
}}

function selectImage(path) {{
  document.querySelectorAll('.img-card').forEach(c => c.classList.remove('selected'));
  const card = document.querySelector(`[data-path="${{CSS.escape(path)}}"]`);
  if (card) card.classList.add('selected');
  selectedImage = SOURCE_IMAGES.find(i => i.path === path);
  document.getElementById('statusBar').textContent = selectedImage
    ? `Seleccionada: ${{selectedImage.name}}`
    : 'Seleccioná una imagen para empezar';
}}

function assignToSku(skuCode) {{
  if (!selectedImage) return;
  const path = selectedImage.path;
  if (!mappings[path]) mappings[path] = [];
  if (!mappings[path].includes(skuCode)) mappings[path].push(skuCode);

  // Marcar imagen como asignada
  const card = document.querySelector(`[data-path="${{CSS.escape(path)}}"]`);
  if (card) {{
    card.classList.add('assigned');
    let badge = card.querySelector('.assigned-badge');
    if (!badge) {{ badge = document.createElement('div'); badge.className = 'assigned-badge'; card.appendChild(badge); }}
    badge.textContent = mappings[path].join(', ');
  }}

  // Marcar SKU como mapeado
  const skuEl = document.querySelector(`[data-sku="${{skuCode}}"]`);
  if (skuEl) {{
    skuEl.classList.add('has-mapping');
    let mapped = skuEl.querySelector('.sku-mapped');
    if (!mapped) {{ mapped = document.createElement('div'); mapped.className = 'sku-mapped'; skuEl.appendChild(mapped); }}
    const allImgs = Object.entries(mappings).filter(([,v]) => v.includes(skuCode)).map(([k]) => k.split('/').pop());
    mapped.textContent = '→ ' + allImgs.join(', ');
  }}

  document.getElementById('statusBar').textContent =
    `✓ ${{selectedImage.name}} → ${{skuCode}}`;
  closeModal();
}}

function openModal(path) {{
  selectedImage = SOURCE_IMAGES.find(i => i.path === path);
  if (!selectedImage) return;
  document.getElementById('modalImg').src = selectedImage.src;
  document.getElementById('modalTitle').textContent = selectedImage.name;
  const container = document.getElementById('modalSkus');
  container.innerHTML = EMPTY_SKUS.map(s => `
    <div class="modal-sku" onclick="assignToSku('${{s.sku}}')">
      <div class="code">${{s.sku}}</div>
      <div class="name">${{s.categoria}} — ${{s.nombre || '(sin nombre)'}}</div>
    </div>`).join('');
  document.getElementById('modal').classList.add('open');
}}

function closeModal() {{
  document.getElementById('modal').classList.remove('open');
}}

function filterImages() {{
  const q = document.getElementById('searchBox').value.toLowerCase();
  const g = document.getElementById('groupFilter').value;
  document.querySelectorAll('.img-card').forEach(card => {{
    const name = (card.dataset.name || '').toLowerCase();
    const group = card.dataset.group || '';
    const matchQ = !q || name.includes(q);
    const matchG = !g || group === g;
    card.style.display = matchQ && matchG ? '' : 'none';
  }});
}}

function clearAll() {{
  selectedImage = null;
  document.querySelectorAll('.img-card').forEach(c => c.classList.remove('selected'));
  document.getElementById('statusBar').textContent = 'Selección limpiada';
}}

function exportMappings() {{
  if (!Object.keys(mappings).length) {{
    alert('Todavía no asignaste ninguna imagen.');
    return;
  }}
  // Generar fragmento Python para deploy_images_confident.py
  const lines = [];
  for (const [imgPath, skus] of Object.entries(mappings)) {{
    const fname = imgPath.split('/').pop();
    for (const sku of skus) {{
      const skuData = EMPTY_SKUS.find(s => s.sku === sku);
      const cat = skuData ? skuData.categoria : '???';
      lines.push(`    # ${{fname}} -> ${{sku}}`);
      lines.push(`    ("PRODUCTOS-IMAGENES/PRODUCTOS/${{fname}}", "productos/${{cat}}/${{sku}}/img/PRODUCTO_PRINCIPAL"),`);
    }}
  }}
  const box = document.getElementById('exportBox');
  document.getElementById('exportContent').textContent = lines.join('\\n');
  box.style.display = box.style.display === 'none' ? 'block' : 'none';
}}

function copyExport() {{
  const text = document.getElementById('exportContent').textContent;
  navigator.clipboard.writeText(text).then(() => alert('Copiado al portapapeles'));
}}

// Cerrar modal con Escape
document.addEventListener('keydown', e => {{ if (e.key === 'Escape') closeModal(); }});
document.getElementById('modal').addEventListener('click', e => {{ if (e.target === e.currentTarget) closeModal(); }});
</script>
</body>
</html>
"""
    OUT.write_text(html, encoding="utf-8")
    print(f"✅ Catálogo generado: {OUT}")
    print(f"   {len(source_images)} imágenes · {len(empty_skus)} SKUs sin imágenes")
    print(f"   Abrilo en: http://localhost:8080/tools/catalog_visual.html")


def _render_groups(groups, all_images):
    """Renderiza grillas de imágenes usando índice numérico — sin problemas de escaping."""
    # Construir un índice global por path
    idx_map = {img["path"]: i for i, img in enumerate(all_images)}
    html = []
    for group_name in sorted(groups.keys()):
        imgs = groups[group_name]
        safe_group = group_name.replace('"', '&quot;')
        html.append(f'<div class="group-title">{safe_group} ({len(imgs)})</div>')
        html.append('<div class="img-grid">')
        for img in imgs:
            idx = idx_map[img["path"]]
            safe_name = img["name"].replace('"', '&quot;')
            safe_src = img["src"].replace('"', '&quot;')
            safe_group_attr = img["group"].replace('"', '&quot;')
            html.append(
                f'<div class="img-card" id="img-{idx}"'
                f' data-idx="{idx}" data-name="{safe_name.lower()}" data-group="{safe_group_attr}"'
                f' onclick="openModal({idx})">'
                f'<img src="{safe_src}" alt="{safe_name}" loading="lazy" onerror="this.parentElement.style.opacity=\'0.3\'">'
                f'<div class="img-name">{safe_name}</div>'
                f'</div>'
            )
        html.append('</div>')
    return "\n".join(html)


def _render_skus(cats):
    html = []
    for cat in sorted(cats.keys()):
        skus = cats[cat]
        html.append(f'<div class="sku-cat">{cat}</div>')
        for s in skus:
            nombre = s["nombre"].replace('"', '&quot;') if s["nombre"] else "(sin nombre)"
            sku = s["sku"]
            html.append(f'''<div class="sku-item" data-sku="{sku}" onclick="selectImage(null); document.getElementById('statusBar').textContent='SKU seleccionado: {sku}'">
  <div class="sku-code">{sku}</div>
  <div class="sku-name">{nombre}</div>
</div>''')
    return "\n".join(html)


if __name__ == "__main__":
    generate()
