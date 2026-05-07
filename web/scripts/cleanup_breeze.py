import os

def cleanup_breeze_from_files():
    base_dir = r'c:\Users\HP 15\Homepowerpty.com\productos'
    
    # CSS to remove
    css_link = '    <link rel="stylesheet" href="../../styles/gold-breeze.css">\n'
    
    # Elements after <body> to remove
    body_elements = '\n    <canvas id="particle-canvas"></canvas>\n    <div id="vignette-effect"></div>\n'
    
    # Elements before </body> to remove
    footer_elements = '\n    <div id="luxury-cursor"></div>\n    <div id="luxury-cursor-ring"></div>\n\n    <script src="../../scripts/gold-breeze.js"></script>\n'

    for root, dirs, files in os.walk(base_dir):
        if 'index.html' in files:
            file_path = os.path.join(root, 'index.html')
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove injections
            new_content = content.replace(css_link, "")
            new_content = new_content.replace(body_elements, "")
            new_content = new_content.replace(footer_elements, "")
            
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Cleaned up {file_path}")

if __name__ == "__main__":
    cleanup_breeze_from_files()
