# Design: fase-1-estabilizacion — Corrección de navegación y variables CSS

## Technical Approach

Tres cambios quirúrgicos de bajo riesgo que no introducen nuevas dependencias ni cambian la arquitectura existente. La estrategia es reutilizar al máximo las clases CSS y patrones HTML ya presentes en el sitio.

---

## Architecture Decisions

### Decision: Alias anchor para #testimonios

**Choice**: Insertar `<a id="testimonios" ...>` invisible antes de `<section id="clientes">`, en lugar de crear una sección de testimonios completa.

**Alternatives considered**:
- Crear una sección de testimonios HTML completa con contenido placeholder
- Renombrar `id="clientes"` a `id="testimonios"`

**Rationale**: El sitio no tiene cotizaciones de clientes reales disponibles hoy. Crear contenido placeholder degrada la credibilidad B2B del catálogo. Renombrar `#clientes` rompería los links del footer que ya apuntan a `#clientes`. El alias anchor es la solución de cero-riesgo que satisface el contrato de navegación sin comprometer el contenido.

---

### Decision: Sección #oportunidades reutiliza .contact-section y .luxury-form

**Choice**: Usar `class="contact-section"` en el `<section>` y `class="luxury-form"` en el `<form>`, con el mismo patrón visual que la sección de contacto existente.

**Alternatives considered**:
- Crear nuevas clases CSS específicas para la sección de empleos
- Usar un layout diferente (tarjetas, steps wizard)

**Rationale**: `luxury.css` ya define estilos completos para `.contact-section` y `.luxury-form` (líneas 947–980). Reutilizarlos garantiza consistencia visual sin agregar código nuevo. La sección de contacto ya es el patrón establecido para formularios en este sitio.

---

### Decision: Posición de la sección #oportunidades en el DOM

**Choice**: Insertar la sección inmediatamente después de `</section>` de `#contacto` (línea ~3150 de `index.html`) y antes de `</main>`.

**Alternatives considered**:
- Antes de la sección `#contacto`
- Dentro del `<footer>`
- En una página separada

**Rationale**: El flujo del recorrido del usuario es: catálogo → clientes → contacto → oportunidades. Quien llega hasta el final de la página es el candidato ideal: ya conoce el producto y la empresa. El flujo lineal es consistente con el patrón de single-page catalog.

---

### Decision: El submit button usa class="careers_submit" (input[type="submit"])

**Choice**: `<input type="submit" class="careers_submit" value="Enviar Aplicación">` — no un `<button>`.

**Rationale**: `send_careers_form.js` línea 6 usa `form.querySelector('.careers_submit')` para deshabilitar el botón durante el envío. Debe ser un elemento que tenga `.disabled` funcionalmente. El JS espera específicamente esta clase.

---

### Decision: Corrección directa de variables en config_new.css (no se crea tokens.css)

**Choice**: Corregir los 2 valores erróneos directamente en `config_new.css`, sin crear un nuevo archivo de tokens ni linkear el archivo.

**Alternatives considered**:
- Crear `styles/tokens.css` como fuente de verdad (Fase 2 del roadmap)
- Eliminar `config_new.css` completamente
- Marcar el archivo con un comentario de advertencia

**Rationale**: La creación de `tokens.css` es Fase 2 del roadmap de arquitectura — hacer eso ahora expande el scope innecesariamente. Eliminar el archivo podría interrumpir trabajo en progreso. La corrección in-place + comentario de advertencia es la acción de menor riesgo para este change.

---

## Data Flow

### Formulario de empleos (send_careers_form.js)

```
Usuario → DOM (#careers_form)
          │
          ├── input event → validateField() → agrega clase .valid / .invalid
          │
          └── submit event
                │
                ├── CSRF fetch → GET php/get_csrf_token.php → { token }
                │
                ├── FormData (full_name, email, phone, position, experience)
                │     + cv_file (si fue seleccionado)
                │     + csrf_token
                │
                └── POST → php/upload_cv.php
                              │
                              ├── success → showMessage('...', 'success')
                              └── error  → showMessage('...', 'error')
```

### Navegación por anchor

```
Click href="#testimonios"
    │
    └── Browser scroll → <a id="testimonios"> (alias, height: 0)
                              │
                              └── viewport muestra inicio de <section id="clientes">

Click href="#oportunidades"
    │
    └── Browser scroll → <section id="oportunidades"> → form visible
```

---

## File Changes

| Archivo | Acción | Descripción |
|---------|--------|-------------|
| `index.html` | Modify | (1) Anchor alias `#testimonios` antes de `#clientes`; (2) Sección `#oportunidades` con form completo; (3) Script tag `send_careers_form.js` |
| `styles/config_new.css` | Modify | Corregir `--color_black` y `--color_white` |
| `tests/smoke.spec.js` | Modify | Agregar test de navegación de anchors (Strict TDD: test PRIMERO) |

---

## Interfaces / Contracts

### HTML markup — anchor alias (index.html)

```html
<!-- Insertar inmediatamente antes de <section class="client-wall-section" id="clientes"> -->
<a id="testimonios" style="display:block;height:0;visibility:hidden;" aria-hidden="true" tabindex="-1"></a>
```

### HTML markup — sección #oportunidades (index.html)

Insertar después del cierre de `</section>` de `#contacto`, antes de `</main>`:

```html
<!-- SECCIÓN OPORTUNIDADES LABORALES -->
<section class="contact-section" id="oportunidades">
    <div class="container contact-container">
        <div class="contact-info">
            <h2 style="color:var(--color-accent); font-family:var(--font-heading); margin-bottom:20px; font-size:2.5rem;">
                Oportunidades Laborales
            </h2>
            <p>¿Querés formar parte del equipo de <strong>HomePower PTY</strong>? Somos una empresa en crecimiento que busca personas apasionadas por el servicio al cliente y la distribución de productos de calidad.</p>
            <br>
            <p>Completá el formulario y te contactaremos si hay una posición disponible que se ajuste a tu perfil.</p>
        </div>
        <div class="contact-form-wrapper">
            <form id="careers_form" action="php/upload_cv.php" method="post" enctype="multipart/form-data" class="luxury-form">
                <div class="form-row">
                    <input type="text" name="full_name" placeholder="Nombre completo" class="form_input" required>
                </div>
                <div class="form-row">
                    <input type="email" name="email" placeholder="Correo electrónico" class="form_input" required>
                    <input type="tel" name="phone" placeholder="Teléfono" class="form_input" required>
                </div>
                <div class="form-row">
                    <input type="text" name="position" placeholder="Posición de interés" class="form_input" required>
                </div>
                <div class="form-row">
                    <textarea name="experience" placeholder="Experiencia previa (opcional)" rows="3" class="form_input"></textarea>
                </div>
                <div class="form-row" style="align-items:center; gap:12px;">
                    <button type="button" id="cv_trigger" class="btn-whatsapp-submit" style="flex:0 0 auto;">
                        Adjuntar CV
                    </button>
                    <span id="file_name" style="color:var(--color-text-secondary, #999); font-size:0.875rem;">
                        Ningún archivo seleccionado
                    </span>
                    <input type="file" id="cv_file" name="cv_file" accept=".pdf,.doc,.docx" style="display:none;">
                </div>
                <div id="careers_form_msg" role="alert"></div>
                <input type="submit" class="careers_submit btn-whatsapp-submit" value="Enviar Aplicación">
            </form>
        </div>
    </div>
</section>
```

### Script tag (index.html — bloque de scripts antes de `</body>`)

```html
<script defer src="scripts/send_careers_form.js"></script>
```

Agregar después de `<script defer src="scripts/send_contact_form.js"></script>`.

### CSS fix (styles/config_new.css)

```css
/* ANTES */
--color_black: #bec2c4;
--color_white: #000000;

/* DESPUÉS */
--color_black: #2c3e50;
--color_white: #ffffff;
```

---

## Testing Strategy

| Layer | Qué testear | Enfoque |
|-------|-------------|---------|
| E2E | `href="#testimonios"` hace scroll a `#clientes` | Playwright: `page.click('a[href="#testimonios"]')` + assert `#clientes` en viewport |
| E2E | `href="#oportunidades"` hace scroll al form | Playwright: click + assert `#careers_form` visible |
| E2E | Formulario careers tiene los campos requeridos | Playwright: assert existence de `#careers_form`, `input[name="full_name"]`, `#cv_trigger` |
| E2E | `config_new.css` NO está linkeado en index.html | Playwright: assert que no hay `link[href*="config_new"]` en el DOM |

**Strict TDD**: los tests de Playwright se escriben PRIMERO en `tests/smoke.spec.js`, luego se implementan los cambios hasta que pasen.

---

## Migration / Rollout

Sin migración de datos. Sin feature flags. Cambio directo en rama.

Rollback: `git revert` del commit — no hay efectos secundarios.

---

## Open Questions

- [ ] ¿`php/upload_cv.php` valida el tipo MIME del archivo CV además de la extensión? Si no, es un riesgo de seguridad menor a resolver en Fase 2.
