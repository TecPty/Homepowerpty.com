import os
import sys
from PIL import Image

SUPPORTED_EXTS = ('.webp', '.jpg', '.jpeg', '.png')
# Favicons y apple-touch-icons nunca se tocan
SKIP_PATTERNS = ('favicon', 'apple-touch', 'og-image')

def optimize_images(directories, max_size=1200, quality=82, threshold_kb=80):
    """
    Optimiza imágenes en las carpetas indicadas.
    - max_size: dimensión máxima (ancho o alto) en px
    - quality: calidad WebP (0-100)
    - threshold_kb: solo procesa archivos > threshold_kb KB
    """
    total_saved = 0
    total_orig = 0
    count = 0
    skipped = 0
    errors = 0

    for directory in directories:
        if not os.path.isdir(directory):
            print(f"[SKIP] Directorio no encontrado: {directory}")
            continue
        print(f"\n📁 Procesando: {directory}/")

        for root, dirs, files in os.walk(directory):
            # Excluir node_modules, .git, dist
            dirs[:] = [d for d in dirs if d not in ('node_modules', '.git', 'dist', '__pycache__')]
            for file in sorted(files):
                ext = os.path.splitext(file)[1].lower()
                if ext not in SUPPORTED_EXTS:
                    continue
                # Saltar favicons y assets especiales
                if any(p in file.lower() for p in SKIP_PATTERNS):
                    skipped += 1
                    continue

                file_path = os.path.join(root, file)
                orig_size = os.path.getsize(file_path)

                if orig_size <= threshold_kb * 1024:
                    skipped += 1
                    continue

                try:
                    with Image.open(file_path) as img:
                        orig_w, orig_h = img.size
                        # Convertir a RGB si es necesario (para PNG con canal alpha, mantener RGBA)
                        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                            img = img.convert('RGBA')
                        elif img.mode != 'RGB':
                            img = img.convert('RGB')

                        # Redimensionar si excede max_size
                        resized = False
                        if img.width > max_size or img.height > max_size:
                            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                            resized = True

                        # Siempre guardar como WebP
                        out_path = os.path.splitext(file_path)[0] + '.webp'
                        img.save(out_path, 'webp', quality=quality, method=4)

                    new_size = os.path.getsize(out_path)
                    saved = orig_size - new_size
                    total_saved += saved
                    total_orig += orig_size
                    count += 1

                    resize_tag = f" [{orig_w}x{orig_h}→{img.width}x{img.height}]" if resized else ""
                    direction = "✅" if saved > 0 else "⚠️ +bigger"
                    print(f"  {direction} {file}{resize_tag}: {orig_size/1024:.0f}KB → {new_size/1024:.0f}KB (Δ {saved/1024:+.0f}KB)")

                    # Si el output es WebP y el original era otro formato, eliminar el original
                    if ext != '.webp' and os.path.exists(file_path) and out_path != file_path:
                        os.remove(file_path)
                        print(f"     🗑  Eliminado original: {file}")

                except Exception as e:
                    errors += 1
                    print(f"  ❌ Error en {file}: {e}")

    print(f"\n{'='*50}")
    print(f"📊 Resumen de optimización")
    print(f"{'='*50}")
    print(f"  Imágenes procesadas : {count}")
    print(f"  Saltadas (pequeñas) : {skipped}")
    print(f"  Errores             : {errors}")
    if total_orig > 0:
        print(f"  Peso original       : {total_orig/1024/1024:.2f} MB")
        print(f"  Ahorro total        : {total_saved/1024/1024:.2f} MB ({total_saved/total_orig*100:.1f}%)")
    print(f"{'='*50}")

if __name__ == '__main__':
    # Directorios a optimizar
    targets = ['media', 'productos']
    optimize_images(targets, max_size=1200, quality=82, threshold_kb=80)

