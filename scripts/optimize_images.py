import os
from PIL import Image

def optimize_images(directory, max_size=1000, quality=80):
    total_saved = 0
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.webp'):
                file_path = os.path.join(root, file)
                orig_size = os.path.getsize(file_path)
                
                # Only process files larger than 150KB
                if orig_size > 150 * 1024:
                    try:
                        with Image.open(file_path) as img:
                            # Resize if larger than max_size while maintaining aspect ratio
                            if img.width > max_size or img.height > max_size:
                                img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                            
                            # Save back with lower quality
                            img.save(file_path, 'webp', quality=quality, method=4)
                            
                        new_size = os.path.getsize(file_path)
                        saved = orig_size - new_size
                        total_saved += saved
                        count += 1
                        print(f"Optimized {file}: saved {saved / 1024:.1f} KB")
                    except Exception as e:
                        print(f"Failed to process {file}: {e}")
                        
    print(f"\nOptimization complete! Processed {count} images.")
    print(f"Total space saved: {total_saved / (1024 * 1024):.2f} MB")

if __name__ == '__main__':
    optimize_images('productos')
