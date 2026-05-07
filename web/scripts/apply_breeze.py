import os

def apply_breeze_to_files():
    base_dir = r'c:\Users\HP 15\Homepowerpty.com\productos'
    
    # CSS to inject in <head>
    css_link = '    <link rel="stylesheet" href="../../styles/gold-breeze.css">\n'
    
    # Elements to inject after <body>
    body_elements = '\n    <canvas id="particle-canvas"></canvas>\n    <div id="vignette-effect"></div>\n'
    
    # Elements to inject before </body>
    footer_elements = '\n    <div id="luxury-cursor"></div>\n    <div id="luxury-cursor-ring"></div>\n\n    <script src="../../scripts/gold-breeze.js"></script>\n'

    for root, dirs, files in os.walk(base_dir):
        if 'index.html' in files:
            file_path = os.path.join(root, 'index.html')
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 1. Inject CSS link before </head>
            if 'gold-breeze.css' not in content:
                content = content.replace('</head>', css_link + '</head>')
            
            # 2. Inject body elements after <body>
            if 'particle-canvas' not in content:
                # Find the <body> tag (it might have classes)
                if '<body' in content:
                    parts = content.split('>', 1)
                    if len(parts) > 1:
                        # Reconstruct with elements after the first > of the body tag
                        # We need to be careful with the first > if it's in <head>
                        # Better approach: find <body and then the first > after it
                        body_index = content.find('<body')
                        closing_bracket_index = content.find('>', body_index)
                        content = content[:closing_bracket_index+1] + body_elements + content[closing_bracket_index+1:]

            # 3. Inject footer elements before </body>
            if 'gold-breeze.js' not in content:
                content = content.replace('</body>', footer_elements + '</body>')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Applied to {file_path}")

if __name__ == "__main__":
    apply_breeze_to_files()
