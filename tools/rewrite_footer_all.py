import os

def update_footer_and_year():
    # El footer premium de index.html
    # Nota: Los enlaces en los productos necesitan ../../../ para llegar a la raíz
    new_footer_template = """    <!-- FOOTER -->
    <footer class="luxury-footer">
        <!-- Franja de marca -->
        <div class="footer-brand">
            <div class="container footer-brand-inner">
                <img src="../../../media/icons/logo/logo_white_premium.png" alt="Home Power" class="luxury-logo">
                <p>Líderes en distribución B2B de electrodomésticos de alta gama en Panamá.</p>
                <div class="social-icons-footer">
                    <a href="https://www.instagram.com/homepowerpty/" class="social-icon-circle" aria-label="Instagram" target="_blank" rel="noopener">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>
                    </a>
                    <a href="https://www.tiktok.com/@homepowerpty" class="social-icon-circle" aria-label="TikTok" target="_blank" rel="noopener">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12.53.02C13.84 0 15.14.01 16.44 0c.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.12-3.44-3.17-3.64-5.46-.22-2.39.81-4.78 2.65-6.22 1.48-1.15 3.39-1.61 5.25-1.34V14c-1.78-.17-3.51.98-4.08 2.66-.54 1.56-.03 3.39 1.19 4.49 1.25 1.13 3.16 1.34 4.74.56 1.72-.85 2.63-2.81 2.5-4.73.04-6.42.02-12.84.02-19.26.04-.01.07-.02.11-.03z"/></svg>
                    </a>
                </div>
            </div>
        </div>

        <div class="container footer-container">
            <div class="footer-col">
                <h4>Navegación</h4>
                <a href="../../../index.html">Inicio</a>
                <a href="../../../index.html#nosotros">Nosotros</a>
                <a href="../../../index.html#clientes">Clientes</a>
                <a href="../../../index.html#contacto">Contacto</a>
            </div>

            <div class="footer-col">
                <h4>Productos</h4>
                <a href="../../../index.html#productos">Electrodomésticos</a>
                <a href="../../../index.html#productos">Novedades</a>
                <a href="../../../index.html#productos">Catálogo Completo</a>
            </div>

            <div class="footer-col">
                <h4>Contacto</h4>
                <p>Ciudad de Panamá, Panamá</p>
                <p>(507) 6983-8322</p>
                <a href="https://wa.me/50769838322" class="btn-support-pill" target="_blank" rel="noopener">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347M12 0C5.373 0 0 5.373 0 12c0 2.123.554 4.117 1.528 5.847L0 24l6.335-1.508A11.954 11.954 0 0 0 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0"/></svg>
                    WhatsApp
                </a>
            </div>
        </div>

        <div class="footer-bottom">
            <div class="container footer-bottom-content">
                <div class="footer-copyright">
                    © 2026 HOMEPOWER PTY. TODOS LOS DERECHOS RESERVADOS.
                </div>
                <div class="footer-legal-links">
                    <a href="../../../aviso-de-privacidad/index.html">Aviso de Privacidad</a>
                    <a href="../../../#">Términos</a>
                </div>
            </div>
        </div>
    </footer>"""

    root = "c:/Users/HP 15/Homepowerpty.com"
    prod_path = os.path.join(root, "productos")

    for dirpath, dirnames, filenames in os.walk(prod_path):
        if "index.html" in filenames:
            file_path = os.path.join(dirpath, "index.html")
            
            # Determinar profundidad para los enlaces relativos
            rel_to_root = os.path.relpath(root, dirpath).replace("\\", "/") + "/"
            
            # Ajustar el footer para esta profundidad específica
            current_footer = new_footer_template.replace("../../../", rel_to_root)

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Reemplazar el footer antiguo (buscamos <footer... </footer>)
            import re
            
            # Intentar encontrar cualquier etiqueta <footer>...</footer>
            new_content = re.sub(r'<footer.*?>.*?</footer>', current_footer, content, flags=re.DOTALL)
            
            if new_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated: {file_path}")

    # Actualizar tmb index.html principal solo el año si no está en 2026
    main_index = os.path.join(root, "index.html")
    with open(main_index, "r", encoding="utf-8") as f:
        main_content = f.read()
    
    # Reemplazar años anteriores por 2026 en el copyright
    new_main = re.sub(r'© \d{4} HOMEPOWER', '© 2026 HOMEPOWER', main_content)
    if new_main != main_content:
        with open(main_index, "w", encoding="utf-8") as f:
            f.write(new_main)
        print("Updated main index year")

update_footer_and_year()
