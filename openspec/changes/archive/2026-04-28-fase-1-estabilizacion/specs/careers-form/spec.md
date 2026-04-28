# Delta for careers-form

## ADDED Requirements

### Requirement: Sección de oportunidades laborales visible en el DOM

Una sección con `id="oportunidades"` MUST existir en `index.html` y contener el formulario de aplicación laboral. La sección MUST estar posicionada después de la sección `#contacto` y antes del `<footer>`.

#### Scenario: La sección existe y es accesible

- GIVEN el usuario navega a la página de inicio
- WHEN el DOM carga completamente
- THEN existe un elemento con `id="oportunidades"`
- AND contiene un `<form id="careers_form">`
- AND la sección es visible (no está oculta con `display: none` ni `visibility: hidden`)

---

### Requirement: Formulario de aplicación laboral

El formulario MUST contener exactamente los campos que `send_careers_form.js` requiere. Cualquier campo faltante provocará que el script retorne silenciosamente (el guard `if (!form) return` en el JS).

Los campos REQUERIDOS con sus `name` attributes:

| Campo | `name` | `type` | Requerido |
|-------|--------|--------|-----------|
| Nombre completo | `full_name` | text | Sí |
| Correo electrónico | `email` | email | Sí |
| Teléfono | `phone` | tel | Sí |
| Posición de interés | `position` | text | Sí |
| Experiencia previa | `experience` | textarea | No |
| CV / Hoja de vida | `cv_file` | file | No |

Los IDs REQUERIDOS por el JS:

| ID | Elemento | Propósito |
|----|----------|-----------|
| `careers_form` | `<form>` | Entry point del módulo JS |
| `careers_form_msg` | `<div>` | Zona de mensajes de éxito/error |
| `cv_file` | `<input type="file">` | Input de CV |
| `cv_trigger` | `<button>` o `<label>` | Disparador visual del file input |
| `file_name` | `<span>` o `<div>` | Nombre del archivo seleccionado |

#### Scenario: Submit con campos requeridos completos

- GIVEN el usuario está en la sección `#oportunidades`
- AND ha llenado `full_name`, `email`, `phone`, y `position`
- WHEN hace submit del formulario
- THEN `send_careers_form.js` envía los datos a `php/upload_cv.php`
- AND el elemento `#careers_form_msg` muestra un mensaje de resultado
- AND el submit button queda deshabilitado durante el envío

#### Scenario: Submit sin campo requerido

- GIVEN el usuario no completó `email`
- WHEN intenta hacer submit del formulario
- THEN el campo inválido recibe la clase `invalid` via el módulo JS
- AND `#careers_form_msg` muestra un mensaje de error descriptivo
- AND no se envía ninguna petición al servidor

#### Scenario: Upload de CV (campo opcional)

- GIVEN el usuario hace click en `#cv_trigger`
- WHEN selecciona un archivo `.pdf` o `.docx`
- THEN el nombre del archivo se muestra en `#file_name`
- AND el `input[name="cv_file"]` tiene el archivo seleccionado

#### Scenario: El módulo JS se carga correctamente

- GIVEN `index.html` contiene `<script defer src="scripts/send_careers_form.js">`
- WHEN el DOM carga
- THEN el módulo encuentra `document.getElementById('careers_form')` y lo inicializa
- AND no produce errores en la consola del navegador

---

### Requirement: El script send_careers_form.js MUST estar cargado en index.html

`send_careers_form.js` MUST tener un `<script defer>` tag en `index.html`. Sin este tag, el formulario renderiza pero no tiene comportamiento.

#### Scenario: Script tag presente

- GIVEN el código fuente de `index.html`
- WHEN se inspecciona el bloque de scripts antes de `</body>`
- THEN existe `<script defer src="scripts/send_careers_form.js"></script>`
- AND está posicionado después de los otros script tags existentes
