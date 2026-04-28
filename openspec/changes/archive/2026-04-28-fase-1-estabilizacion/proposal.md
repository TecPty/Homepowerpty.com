# Proposal: fase-1-estabilizacion — Corrección de navegación y variables CSS

## Intent

El menú de navegación del sitio tiene dos ítems — **Testimonios** y **Oportunidades** — que al hacer click no llevan a ninguna parte: los `href="#testimonios"` y `href="#oportunidades"` no tienen elemento destino en el DOM. Para un cliente B2B que visita el catálogo, un menú con links rotos erosiona la confianza antes de que llegue a hacer una consulta.

Adicionalmente, `styles/config_new.css` tiene `--color_black` y `--color_white` con valores **invertidos** (gris claro y negro respectivamente). El archivo no está linkeado hoy, pero es una trampa: si alguien lo incluye en cualquier contexto, el contraste texto/fondo se invierte en todo el sitio.

El diagnóstico original listaba 6 fixes, pero la exploración confirmó que **4 ya estaban resueltos**. Este change cubre los 3 problemas reales que quedan.

---

## Scope

### In Scope

1. **Anchor `#testimonios`** — Agregar un anchor alias `<a id="testimonios">` inmediatamente antes de la sección `#clientes`, de modo que el link del menú navegue al área de clientes (que es la prueba social del sitio).
2. **Sección `#oportunidades`** — Crear la sección HTML del formulario de empleos usando los campos que `send_careers_form.js` ya espera (`full_name`, `email`, `phone`, `position`, `experience`, `cv_file`), y agregar su `<script defer>` tag. El JS y el backend PHP ya existen completos — solo falta la UI.
3. **CSS variable fix** — Corregir `--color_black` (`#bec2c4` → `#2c3e50`) y `--color_white` (`#000000` → `#ffffff`) en `styles/config_new.css`.

### Out of Scope

- Crear contenido de testimonios real (cotizaciones de clientes, stars, etc.) — eso es contenido, no infraestructura
- Estilos de la sección `#oportunidades` más allá de reutilizar las clases `luxury-form` existentes
- Linkear `config_new.css` en `index.html` (ese archivo sigue sin cargarse — solo se corrigen sus valores)
- Cualquier cambio a los otros 4 fixes originales (ya están resueltos)

---

## Capabilities

### New Capabilities
*(ninguna — estas son correcciones e integración de infraestructura ya existente)*

### Modified Capabilities

- `navigation-anchors` — Restaurar targets `#testimonios` y `#oportunidades` en el DOM
- `css-tokens` — Corregir valores invertidos en `config_new.css`
- `careers-form` — Completar la integración de la sección de oportunidades laborales (JS + PHP ya existen, HTML faltaba)

---

## Approach

### Fix 1 — Anchor `#testimonios` (1 línea)

Agregar un anchor invisible justo antes del `<section id="clientes">`:

```html
<a id="testimonios" style="display:block;height:0;visibility:hidden;" aria-hidden="true"></a>
```

Esto hace que `href="#testimonios"` navegue al inicio del bloque de clientes, que es el equivalente semántico más cercano a "testimonios" en el sitio actual.

### Fix 2 — Sección `#oportunidades` (HTML + script tag)

Crear la sección de empleos reutilizando `.contact-section` / `.luxury-form` como base visual. Los campos deben tener exactamente los `name` attributes que `send_careers_form.js` espera:
- `full_name`, `email`, `phone`, `position`, `experience`, `cv_file`
- IDs requeridos: `careers_form`, `careers_form_msg`, `cv_file`, `cv_trigger`, `file_name`

Agregar al bloque de scripts antes de `</body>`:
```html
<script defer src="scripts/send_careers_form.js"></script>
```

### Fix 3 — `config_new.css` (2 líneas)

```css
/* antes */
--color_black: #bec2c4;
--color_white: #000000;

/* después */
--color_black: #2c3e50;
--color_white: #ffffff;
```

---

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `index.html` | Modified | Anchor alias antes de `#clientes`, nueva sección `#oportunidades`, script tag |
| `styles/config_new.css` | Modified | 2 valores de variables corregidos |
| `scripts/send_careers_form.js` | None | Sin cambios — ya tiene la lógica completa |
| `php/upload_cv.php` | None | Sin cambios — ya funcional |
| `php/get_csrf_token.php` | None | Sin cambios — ya funcional |
| `tests/smoke.spec.js` | Modified | Agregar test de navegación de anchors (TDD: test primero) |

---

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| La sección `#oportunidades` queda visualmente inconsistente | Low | Reutilizar clases `.contact-section` y `.luxury-form` que ya tienen estilos |
| `send_careers_form.js` espera más elementos que los que creamos | Low | La exploración identificó todos los IDs requeridos: `careers_form`, `careers_form_msg`, `cv_file`, `cv_trigger`, `file_name` — todos se crearán |
| El anchor alias `#testimonios` puede quedar afectado por futuros cambios en la estructura de sección | Low | Es un alias de display:none — no afecta layout. Si se crea una sección de testimonios real, se reemplaza este nodo |
| Conflicto CSRF en el form de oportunidades | Low | `get_csrf_token.php` ya existe y es el mismo endpoint que usa `send_contact_form.js` |

---

## Rollback Plan

Los tres cambios son completamente reversibles con `git revert` o manual:

1. **Anchor `#testimonios`** — Eliminar 1 línea HTML
2. **Sección `#oportunidades`** — Eliminar el bloque `<section>` y el `<script defer>` tag  
3. **CSS variables** — Revertir 2 líneas en `config_new.css`

Sin migraciones de datos, sin cambios de esquema, sin dependencias externas nuevas.

---

## Dependencies

- `scripts/send_careers_form.js` — ya existe ✅
- `php/upload_cv.php` — ya existe ✅
- `php/get_csrf_token.php` — ya existe ✅
- `styles/luxury.css` (clases `.contact-section`, `.luxury-form`) — ya cargado en `<head>` ✅
