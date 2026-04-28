# Tasks: fase-1-estabilizacion — Corrección de navegación y variables CSS

> **Strict TDD activo**: cada bloque de implementación está precedido por su test.
> Orden de ejecución: las fases deben seguirse en secuencia.

---

## Phase 1: Tests (escribir PRIMERO — Red)

> Escribir los tests antes de tocar `index.html` o `config_new.css`.
> Los tests deben fallar en este punto (comportamiento esperado en TDD).

- [x] 1.1 En `tests/smoke.spec.js`, agregar test: navegación `#testimonios` hace scroll al elemento `#clientes`
  - Click en `a[href="#testimonios"]` del nav
  - Assert: `page.locator('#clientes')` está en el viewport (`isIntersectingViewport`)

- [x] 1.2 En `tests/smoke.spec.js`, agregar test: navegación `#oportunidades` hace scroll al formulario de empleos
  - Click en `a[href="#oportunidades"]` del nav
  - Assert: `page.locator('#careers_form')` está en el viewport

- [x] 1.3 En `tests/smoke.spec.js`, agregar test: sección de empleos tiene todos los campos requeridos por el JS
  - Scroll a `#oportunidades`
  - Assert: `#careers_form`, `input[name="full_name"]`, `input[name="email"]`, `input[name="phone"]`, `input[name="position"]`, `#cv_trigger`, `#cv_file`, `#file_name`, `#careers_form_msg` — todos `exist()` en el DOM

- [x] 1.4 En `tests/smoke.spec.js`, agregar test: `config_new.css` NO está linkeado en el `<head>` de `index.html`
  - Assert: `page.locator('link[href*="config_new"]')` tiene count === 0

- [x] 1.5 Ejecutar `npm test` y confirmar que los 4 tests nuevos fallan (los 5 existentes deben seguir pasando)

---

## Phase 2: CSS Fix — Corregir variables invertidas

> Sin HTML changes todavía. Un archivo, dos líneas.

- [x] 2.1 En `styles/config_new.css`, cambiar:
  - `--color_black: #bec2c4` → `--color_black: #2c3e50`
  - `--color_white: #000000` → `--color_white: #ffffff`
  - Agregar comentario inline: `/* corregido 2026-04-28 — estaban invertidos */`

- [x] 2.2 Verificar que `config_new.css` NO aparece en ningún `<link>` de `index.html` (debe mantenerse desvinculado)
  - Si aparece, eliminar ese `<link>` tag antes de continuar

---

## Phase 3: Anchor alias #testimonios

> Cambio quirúrgico de una sola línea en `index.html`.

- [x] 3.1 En `index.html`, localizar `<section class="client-wall-section" id="clientes">`
- [x] 3.2 Insertar inmediatamente ANTES de esa línea:
  ```html
  <a id="testimonios" style="display:block;height:0;visibility:hidden;" aria-hidden="true" tabindex="-1"></a>
  ```
- [x] 3.3 Ejecutar `npm test` — el test 1.1 debe pasar ahora. Los demás tests deben seguir en su estado actual.

---

## Phase 4: Sección #oportunidades — HTML completo

> Insertar la sección de empleos en `index.html`.

- [x] 4.1 Localizar el cierre `</section>` de la sección `#contacto` en `index.html` (buscar la sección que contiene `id="contacto")`
- [x] 4.2 Insertar inmediatamente DESPUÉS de ese `</section>` (antes de `</main>`):

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

- [x] 4.3 Ejecutar `npm test` — los tests 1.2 y 1.3 deben pasar ahora.

---

## Phase 5: Wiring — agregar script tag

> Conectar `send_careers_form.js` al HTML.

- [x] 5.1 En `index.html`, localizar el bloque de scripts antes de `</body>`:
  ```html
  <script defer src="scripts/send_contact_form.js"></script>
  ```
- [x] 5.2 Agregar inmediatamente DESPUÉS de esa línea:
  ```html
  <script defer src="scripts/send_careers_form.js"></script>
  ```

---

## Phase 6: Green — Verificar todos los tests pasan

- [x] 6.1 Ejecutar `npm test` completo
- [x] 6.2 Verificar que los 9 tests pasan (5 existentes + 4 nuevos)
- [x] 6.3 Si algún test falla, diagnosticar y corregir antes de continuar con sdd-verify

---

## Checklist de IDs críticos

Antes de cerrar el apply, verificar que estos IDs/names existen en el HTML y coinciden exactamente con lo que espera `send_careers_form.js`:

| ID/name en HTML | Usado por JS como |
|-----------------|-------------------|
| `id="careers_form"` | `document.getElementById('careers_form')` |
| `id="careers_form_msg"` | `document.getElementById('careers_form_msg')` |
| `id="cv_file"` | `document.getElementById('cv_file')` |
| `id="cv_trigger"` | `document.getElementById('cv_trigger')` |
| `id="file_name"` | `document.getElementById('file_name')` |
| `name="full_name"` | `formData.get('full_name')` |
| `name="email"` | `formData.get('email')` |
| `name="phone"` | `formData.get('phone')` |
| `name="position"` | `formData.get('position')` |
| `name="experience"` | `formData.get('experience')` |
| `class="careers_submit"` | `form.querySelector('.careers_submit')` |
