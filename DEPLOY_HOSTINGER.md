Despliegue a Hostinger (hPanel/cPanel)

Resumen rápido
- `scripts/deploy_hostinger.ps1` corre `npm run build` (Vite) y empaqueta `dist/` en un ZIP.
- Subís el ZIP al servidor (hPanel/cPanel → File Manager → `public_html`).
- Extraés el ZIP **directo en `public_html`**, no en una subcarpeta.

⚠️ Por qué es así (y no un ZIP del repo tal cual)
Hasta 2026-07 este script generaba un ZIP mirror del repo completo (rutas relativas,
sin build). En este hosting ese enfoque dejó el sitio sin estilos — el CSS no se
aplicaba y quedaba una página sin ningún estilo, con el menú duplicado sin ocultar.
Además el mirror completo incluía ~400MB de contenido que nunca debió salir del repo:
dos entornos virtuales de Python con binarios compilados, documentación interna
(incluyendo un doc que lista bugs del sitio) y una planilla de negocio confidencial.
El build de Vite (`dist/`) sí funcionó en producción, verificado con Playwright contra
el sitio en vivo: CSS con status 200 y `content-type: text/css`, estilos computados
reales aplicados (fuente, colores, layout). Por eso `dist/` es ahora el único método
soportado.

Importante: el build de Vite usa rutas absolutas desde la raíz (`/assets/...`). Esto
significa que **el sitio tiene que quedar servido exactamente en la raíz del dominio**
(`public_html/index.html`, no `public_html/algo/index.html`). Si tu sitio vive en un
subdominio con su propio docroot, no hay problema; si vive en una subcarpeta de un
dominio compartido, este método no te sirve tal cual — avisá antes de desplegar así.

1) Generar el ZIP de deploy
- Requisitos: Windows PowerShell 5+, Node/npm instalado.
- Ejecutá en la raíz del proyecto:
  - `powershell -ExecutionPolicy Bypass -File scripts/deploy_hostinger.ps1`
- El script:
  - Corre `npm run build` (podés saltear el build con `-SkipBuild` si ya tenés un
    `dist/` fresco y solo querés re-empaquetarlo).
  - Empaqueta el contenido de `dist/` (no el repo) en `deploy/site_YYYYMMDD_HHMM.zip`.
  - El build ya excluye automáticamente lo que no es parte del sitio: `.venv`,
    `.claude`, `tools/`, `backups/`, `tests/`, docs internos, etc. (ver
    `vite.config.js` → `EXCLUDED_DIRS`/`EXCLUDED_FILES`).

2) Subir y extraer en Hostinger hPanel
- Inicia sesión en hPanel → Archivos → File Manager.
- Ve a `public_html` (o el docroot del dominio).
- Pulsa "Upload" y selecciona el ZIP generado.
- Cuando termine, selecciona el ZIP y usa "Extract" (Extraer) **estando parado en
  `public_html`** — el contenido del ZIP debe quedar directo ahí (`index.html`,
  `assets/`, `styles/`, etc. a la vista), no adentro de una carpeta con el nombre
  del ZIP.

3) (Opcional) Subir por FTP/SFTP
- Recomendado: FileZilla o WinSCP.
- Protocolo: FTPS (explícito) o SFTP según tu plan.
- Host, usuario y contraseña: en hPanel → Cuentas FTP o Acceso SSH.
- Subí el contenido de `dist/` (no el ZIP, el contenido ya extraído localmente)
  directo a `public_html`.

4) Verificaciones
- Navega a tu dominio → verifica que carga `index.html` correcto.
- Revisa consola del navegador (F12) → pestaña Network → filtrá por `.css` y
  confirmá que las hojas de estilo devuelven `200` con `content-type: text/css`,
  no `404` ni `text/html`.
- Borra caché/Cloudflare si aplicase.

5) cPanel (si tu plan lo usa)
- cPanel → File Manager → `public_html` → Upload ZIP → Extract.
- Asegúrate de que `.htaccess` (si existe) está en `public_html`.

Resolución de problemas
- Sitio sin estilos / CSS no carga: casi siempre es que el ZIP quedó extraído
  dentro de una subcarpeta en vez de en `public_html` directo — las rutas del
  build son absolutas (`/assets/...`) y necesitan estar en la raíz. Revisá
  File Manager y, si corresponde, movés el contenido hacia afuera de la subcarpeta.
- Pantalla en blanco o 404: confirma que los archivos quedaron en `public_html`
  y no dentro de una carpeta intermedia del ZIP.
- Recursos que no cargan (imágenes/CSS/JS): verificá con DevTools → Network qué
  status/content-type devuelve cada recurso. Un 404 puntual en `styles/hero.css`
  es un problema preexistente del código (ese archivo no existe en el repo, no
  tiene que ver con el deploy) — no bloquea el resto del sitio.
- Permisos/propiedad: por defecto no se requieren cambios, pero si migraste desde
  otro hosting, revisá permisos 644/755.
