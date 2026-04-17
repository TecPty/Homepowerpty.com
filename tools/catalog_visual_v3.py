"""
catalog_visual_v3.py
Genera una tabla editable: imagen | nombre | dropdown SKU | notas.
Sin modal, sin clicks dobles. Directo.
"""
import json
import re
from pathlib import Path

ROOT      = Path(__file__).parent.parent
STAGING   = ROOT / "PRODUCTOS-IMAGENES" / "PRODUCTOS"
PRODUCTOS = ROOT / "productos"
OUT       = ROOT / "tools" / "catalog_visual.html"

IMG_EXTS  = {".png", ".jpg", ".jpeg", ".webp", ".PNG", ".JPG", ".JPEG", ".WEBP"}


def collect_source_images():
    images = []
    for f in sorted(STAGING.rglob("*")):
        if f.suffix in IMG_EXTS and f.is_file():
            rel_fwd = str(f.relative_to(ROOT)).replace("\\", "/")
            src     = "../" + rel_fwd
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


def _esc(s):
    return str(s).replace("&","&amp;").replace('"',"&quot;").replace("<","&lt;").replace(">","&gt;")


def build_sku_options(empty_skus):
    opts = ['<option value="">— sin asignar —</option>']
    cur_cat = None
    for s in empty_skus:
        if s["categoria"] != cur_cat:
            if cur_cat:
                opts.append("</optgroup>")
            opts.append(f'<optgroup label="{_esc(s["categoria"])}">')
            cur_cat = s["categoria"]
        label = f'{_esc(s["sku"])} — {_esc(s["nombre"])}' if s["nombre"] else _esc(s["sku"])
        opts.append(f'<option value="{_esc(s["sku"])}" data-cat="{_esc(s["categoria"])}">{label}</option>')
    if cur_cat:
        opts.append("</optgroup>")
    return "\n".join(opts)


def build_rows(images, sku_options_html):
    rows = []
    for i, img in enumerate(images):
        rows.append(
            f'<tr id="row-{i}" data-idx="{i}" data-name="{_esc(img["name"].lower())}" data-group="{_esc(img["group"])}">'
            f'<td class="td-img"><img src="{_esc(img["src"])}" alt="" loading="lazy" onerror="this.style.opacity=\'0.2\'"></td>'
            f'<td class="td-name"><div class="fname">{_esc(img["name"])}</div>'
            f'<div class="fgroup">{_esc(img["group"])}</div></td>'
            f'<td class="td-sku"><select class="sku-sel" data-idx="{i}" onchange="onSkuChange({i})">'
            f'{sku_options_html}</select></td>'
            f'<td class="td-notes"><input class="notes-inp" type="text" placeholder="Notas opcionales..." data-idx="{i}"></td>'
            f'<td class="td-status"><span class="status-dot" id="dot-{i}">—</span></td>'
            f'</tr>'
        )
    return "\n".join(rows)


def generate():
    source_images = collect_source_images()
    empty_skus    = collect_empty_skus()

    groups = sorted({img["group"] for img in source_images})
    sku_options_html = build_sku_options(empty_skus)
    rows_html        = build_rows(source_images, sku_options_html)
    imgs_json        = json.dumps(source_images, ensure_ascii=False)
    skus_json        = json.dumps(empty_skus,    ensure_ascii=False)

    groups_opts = '<option value="">Todos los grupos</option>\n' + "\n".join(
        f'<option value="{_esc(g)}">{_esc(g)}</option>' for g in groups
    )

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Catálogo de Imágenes — Home Power</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: system-ui, sans-serif; background: #0f0f0f; color: #eee; font-size: 13px; }}
h1 {{ padding: 16px 20px 4px; font-size: 19px; color: #D6B55E; }}
.subtitle {{ padding: 0 20px 12px; color: #777; font-size: 12px; }}

/* Toolbar */
.toolbar {{ background: #181818; border-bottom: 1px solid #252525; padding: 10px 20px;
            display: flex; gap: 10px; align-items: center; flex-wrap: wrap; position: sticky; top: 0; z-index: 10; }}
input[type=text].search {{ background: #222; border: 1px solid #333; color: #eee;
                           padding: 6px 10px; border-radius: 6px; font-size: 12px; width: 200px; }}
select.filter {{ background: #222; border: 1px solid #333; color: #eee;
                 padding: 6px 8px; border-radius: 6px; font-size: 12px; }}
.btn {{ background: #D6B55E; color: #000; border: none; padding: 7px 14px;
        border-radius: 6px; font-size: 12px; font-weight: 700; cursor: pointer; }}
.btn:hover {{ background: #b49542; }}
.btn-sec {{ background: #2a2a2a; color: #eee; border: 1px solid #3a3a3a; }}
.btn-sec:hover {{ background: #333; }}
.counter {{ font-size: 11px; color: #666; margin-left: auto; }}

/* Tabla */
.wrap {{ padding: 0 20px 40px; }}
table {{ width: 100%; border-collapse: collapse; margin-top: 14px; }}
th {{ background: #181818; color: #888; font-size: 11px; font-weight: 600; text-transform: uppercase;
      letter-spacing: .5px; padding: 8px 10px; border-bottom: 1px solid #252525; text-align: left;
      position: sticky; top: 53px; z-index: 5; }}
tr {{ border-bottom: 1px solid #1e1e1e; transition: background .1s; }}
tr:hover {{ background: #151515; }}
tr.assigned {{ background: #0c160c; }}
td {{ padding: 6px 10px; vertical-align: middle; }}

/* Columnas */
.td-img {{ width: 72px; }}
.td-img img {{ width: 64px; height: 64px; object-fit: contain; background: #fff;
               border-radius: 6px; padding: 3px; display: block; }}
.td-name {{ width: 280px; }}
.fname {{ color: #ddd; font-size: 12px; word-break: break-word; }}
.fgroup {{ color: #555; font-size: 10px; margin-top: 2px; }}
.td-sku {{ width: 320px; }}
.sku-sel {{ width: 100%; background: #1e1e1e; border: 1px solid #333; color: #eee;
            padding: 7px 8px; border-radius: 6px; font-size: 12px; cursor: pointer; }}
.sku-sel:focus {{ outline: none; border-color: #D6B55E; }}
.sku-sel.active {{ border-color: #4CAF50; background: #0d1a0d; color: #8BC34A; font-weight: 600; }}
.td-notes {{ }}
.notes-inp {{ width: 100%; background: #1a1a1a; border: 1px solid #2a2a2a; color: #bbb;
              padding: 6px 8px; border-radius: 6px; font-size: 11px; }}
.notes-inp:focus {{ outline: none; border-color: #555; }}
.td-status {{ width: 50px; text-align: center; }}
.status-dot {{ font-size: 16px; color: #333; }}
.status-dot.ok {{ color: #4CAF50; }}

/* Export */
.export-box {{ display: none; margin: 16px 20px; background: #0b170b; border: 1px solid #1e3a1e;
               border-radius: 8px; padding: 16px; }}
.export-box h4 {{ color: #4CAF50; margin-bottom: 10px; font-size: 13px; }}
pre {{ font-size: 11px; color: #bbb; white-space: pre-wrap; word-break: break-all;
       background: #0a0a0a; padding: 12px; border-radius: 6px; max-height: 220px; overflow-y: auto; }}
</style>
</head>
<body>

<h1>Catálogo de Imágenes — Home Power PTY</h1>
<p class="subtitle">{len(source_images)} imágenes &nbsp;·&nbsp; {len(empty_skus)} SKUs sin imágenes &nbsp;·&nbsp;
Usá el dropdown para asignar cada imagen a su SKU</p>

<div class="toolbar">
  <input type="text" class="search" id="searchBox" placeholder="Buscar por nombre..." oninput="filterRows()">
  <select class="filter" id="groupFilter" onchange="filterRows()">
    {groups_opts}
  </select>
  <select class="filter" id="statusFilter" onchange="filterRows()">
    <option value="">Todos</option>
    <option value="assigned">Solo asignadas</option>
    <option value="unassigned">Sin asignar</option>
  </select>
  <button class="btn btn-sec" onclick="clearAll()">Limpiar todo</button>
  <button class="btn" onclick="exportMappings()">Exportar mappings</button>
  <span class="counter" id="counter">0 asignadas</span>
</div>

<div id="exportBox" class="export-box">
  <h4>Mappings listos para deploy_images_confident.py</h4>
  <pre id="exportContent"></pre>
  <button class="btn btn-sec" onclick="copyExport()" style="margin-top:10px">Copiar al portapapeles</button>
</div>

<div class="wrap">
<table id="mainTable">
  <thead>
    <tr>
      <th></th>
      <th>Archivo</th>
      <th>SKU destino</th>
      <th>Notas</th>
      <th>✓</th>
    </tr>
  </thead>
  <tbody>
    {rows_html}
  </tbody>
</table>
</div>

<script>
const SOURCE_IMAGES = {imgs_json};
const EMPTY_SKUS    = {skus_json};
let assignedCount   = 0;

function onSkuChange(idx) {{
  const sel = document.querySelector('.sku-sel[data-idx="' + idx + '"]');
  const dot = document.getElementById('dot-' + idx);
  const row = document.getElementById('row-' + idx);

  if (sel.value) {{
    sel.classList.add('active');
    dot.textContent = '✓';
    dot.classList.add('ok');
    row.classList.add('assigned');
  }} else {{
    sel.classList.remove('active');
    dot.textContent = '—';
    dot.classList.remove('ok');
    row.classList.remove('assigned');
  }}
  updateCounter();
}}

function updateCounter() {{
  const n = document.querySelectorAll('.sku-sel.active').length;
  document.getElementById('counter').textContent = n + ' asignadas';
}}

function filterRows() {{
  const q      = document.getElementById('searchBox').value.toLowerCase();
  const g      = document.getElementById('groupFilter').value;
  const status = document.getElementById('statusFilter').value;

  document.querySelectorAll('#mainTable tbody tr').forEach(function(row) {{
    const nameOk   = !q      || row.dataset.name.includes(q);
    const groupOk  = !g      || row.dataset.group === g;
    const assigned = row.classList.contains('assigned');
    const statusOk = !status
                     || (status === 'assigned'   &&  assigned)
                     || (status === 'unassigned' && !assigned);
    row.style.display = nameOk && groupOk && statusOk ? '' : 'none';
  }});
}}

function clearAll() {{
  if (!confirm('¿Limpiar todas las asignaciones?')) return;
  document.querySelectorAll('.sku-sel').forEach(function(sel) {{
    sel.value = '';
    sel.classList.remove('active');
  }});
  document.querySelectorAll('.status-dot').forEach(function(d) {{
    d.textContent = '—'; d.classList.remove('ok');
  }});
  document.querySelectorAll('#mainTable tbody tr').forEach(function(r) {{
    r.classList.remove('assigned');
  }});
  document.querySelectorAll('.notes-inp').forEach(function(n) {{ n.value = ''; }});
  updateCounter();
}}

function exportMappings() {{
  const rows = [];
  document.querySelectorAll('.sku-sel.active').forEach(function(sel) {{
    const idx   = parseInt(sel.dataset.idx);
    const sku   = sel.value;
    const img   = SOURCE_IMAGES[idx];
    const skuD  = EMPTY_SKUS.find(function(s) {{ return s.sku === sku; }});
    const cat   = skuD ? skuD.categoria : '???';
    const notes = document.querySelector('.notes-inp[data-idx="' + idx + '"]').value;
    const note  = notes ? '  # NOTA: ' + notes : '';
    rows.push('    # ' + img.name + ' -> ' + sku + note);
    rows.push('    ("' + img.path + '", "productos/' + cat + '/' + sku + '/img/PRODUCTO_PRINCIPAL"),');
  }});

  if (!rows.length) {{ alert('Todavía no asignaste ninguna imagen.'); return; }}

  document.getElementById('exportContent').textContent = rows.join('\\n');
  const box = document.getElementById('exportBox');
  box.style.display = box.style.display === 'block' ? 'none' : 'block';
  if (box.style.display === 'block') box.scrollIntoView({{ behavior: 'smooth' }});
}}

function copyExport() {{
  navigator.clipboard.writeText(document.getElementById('exportContent').textContent)
    .then(function() {{ alert('¡Copiado al portapapeles!'); }});
}}
</script>
</body>
</html>
"""
    OUT.write_text(html, encoding="utf-8")
    print(f"✅  Catálogo v3 generado: {OUT}")
    print(f"    {len(source_images)} imágenes · {len(empty_skus)} SKUs sin imágenes")
    print(f"    Abrilo en: http://localhost:8080/tools/catalog_visual.html")


if __name__ == "__main__":
    generate()
