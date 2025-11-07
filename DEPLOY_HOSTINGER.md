Despliegue a Hostinger (hPanel/cPanel)

Resumen rápido
- Genera un ZIP limpio del proyecto con `scripts/deploy_hostinger.ps1`.
- Sube el ZIP al servidor (hPanel/cPanel → File Manager → `public_html`).
- Extrae el ZIP en `public_html` (o el docroot de tu dominio).

1) Crear ZIP listo para producción
- Requisitos: Windows PowerShell 5+.
- Ejecuta en la raíz del proyecto:
  - `powershell -ExecutionPolicy Bypass -File scripts/deploy_hostinger.ps1`
- El script:
  - Crea un staging temporal (excluye `.git`, `.vscode`, `node_modules`, `deploy`, etc.).
  - Genera `deploy/site_YYYYMMDD_HHMM.zip`.

2) Subir y extraer en Hostinger hPanel
- Inicia sesión en hPanel → Archivos → File Manager.
- Ve a `public_html` (o el docroot del dominio).
- Pulsa “Upload” y selecciona el ZIP generado.
- Cuando termine, selecciona el ZIP y usa “Extract” (Extraer) para desplegar los archivos.
- Si el sitio vive en un subdirectorio, extrae allí.

3) (Opcional) Subir por FTP/SFTP
- Recomendado: FileZilla o WinSCP.
- Protocolo: FTPS (explícito) o SFTP según tu plan.
- Host, usuario y contraseña: en hPanel → Cuentas FTP o Acceso SSH.
- Sube el contenido del ZIP ya extraído localmente hacia `public_html`.

4) Verificaciones
- Navega a tu dominio → verifica que carga `index.html` correcto.
- Revisa consola del navegador (F12) para detectar rutas 404.
- Borra caché/Cloudflare si aplicase.

5) cPanel (si tu plan lo usa)
- cPanel → File Manager → `public_html` → Upload ZIP → Extract.
- Asegúrate de que `.htaccess` (si existe) está en `public_html`.

Resolución de problemas
- Pantalla en blanco o 404: confirma que los archivos quedaron en `public_html` y no dentro de una carpeta intermedia del ZIP.
- Recursos que no cargan (imágenes/CSS/JS): verifica rutas relativas en `index.html` y subcarpetas `media/`, `styles/`, `scripts/`.
- Permisos/propiedad: por defecto no se requieren cambios, pero si migraste desde otro hosting, revisa permisos 644/755.

