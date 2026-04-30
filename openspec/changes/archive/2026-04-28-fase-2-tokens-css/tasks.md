# Tasks: fase-2-tokens-css

## Phase 1: Crear styles/tokens.css

- [x] 1.1 Crear `styles/tokens.css` con bloque `:root` completo — categorías: paleta base, acento dorado, texto, bordes, utilidad, tipografía (fonts + escala), espaciado, layout, sombras, transiciones, z-index
- [x] 1.2 Agregar sección de aliases legacy al final del `:root` en `tokens.css`: `--color_accent`, `--color_black`, `--color_white`, `--color-gold`, `--color-gold-hover`, `--luxury-accent`
- [x] 1.3 Verificar que el archivo no tiene errores de sintaxis (llaves balanceadas, punto y coma, no hay `;` dobles)

## Phase 2: Actualizar index.html

- [x] 2.1 Insertar `<link rel="stylesheet" href="styles/tokens.css">` en `index.html` como **primer** stylesheet local, antes de `styles/luxury.css`
- [x] 2.2 Confirmar que el orden resultante es: `tokens.css` → `luxury.css` → `gold-breeze.css`

## Phase 3: Deprecar config_new.css

- [x] 3.1 Reemplazar TODO el contenido de `styles/config_new.css` con el comentario de deprecación:
  ```css
  /* DEPRECATED — Fase 2 (2026-04-28)
     Las variables de este archivo han sido migradas a styles/tokens.css.
     Este archivo se eliminará en Fase 4 una vez que todos los consumers
     usen los nombres kebab-case de tokens.css.
     NO agregar variables aquí. */
  ```

## Phase 4: Verificación

- [ ] 4.1 Abrir `index.html` en browser, abrir DevTools → Elements → panel Computed → buscar `--color-accent` → verificar valor `#D6B55E` *(verificación manual pendiente)*
- [ ] 4.2 En DevTools Computed buscar `--color_white` → verificar valor `#ffffff` (NO `#000000`) *(verificación manual pendiente)*
- [ ] 4.3 En DevTools Computed buscar `--color-text` → verificar valor `#f5f5f5` *(verificación manual pendiente)*
- [ ] 4.4 DevTools → Console → reload → confirmar cero errores CSS *(verificación manual pendiente)*
- [ ] 4.5 DevTools → Network → filtrar CSS → confirmar `tokens.css` aparece primero en la lista de stylesheets locales *(verificación manual pendiente)*
- [ ] 4.6 Verificación visual: color dorado visible en hero (títulos, CTAs), bordes de cards, separadores decorativos *(verificación manual pendiente)*

## Phase 5: Commit

- [x] 5.1 Correr `npm test` (Playwright) → 9/9 tests en verde ✅
- [x] 5.2 Commit atómico: `89b24f3`
  ```
  feat(css): add tokens.css as single source of truth for CSS variables

  - Create styles/tokens.css with full design token system (7 categories)
  - Add backward-compatible aliases for legacy underscore variable names
  - Insert tokens.css as first CSS link in index.html
  - Deprecate styles/config_new.css (content replaced with comment)

  Fixes --color-accent resolving to nothing (14 inline refs in index.html)
  Part of Fase 2 CSS token unification
  ```
