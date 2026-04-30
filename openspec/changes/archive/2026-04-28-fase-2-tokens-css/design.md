# Design: fase-2-tokens-css

## Technical Approach

Crear `styles/tokens.css` como único `:root` de variables CSS del proyecto. Este archivo se carga antes que cualquier otro CSS local en `index.html`, garantizando que todos los tokens estén disponibles cuando `luxury.css` y `gold-breeze.css` los consuman o los sobreescriban.

`config_new.css` pasa a contener solo un comentario de deprecación — sus variables se reemplazan por aliases en `tokens.css` para compatibilidad durante la transición.

## Architecture Decisions

### Decision: tokens.css como nuevo archivo, no renombrar config_new.css

**Choice**: Crear `styles/tokens.css` limpio, vaciar `config_new.css`  
**Alternatives considered**: Renombrar config_new.css a tokens.css en el filesystem  
**Rationale**: `config_new.css` tiene un historial de variables con naming inconsistente (underscore). Empezar limpio con `tokens.css` de kebab-case evita heredar confusión. El renombre requeriría actualizar todas las referencias en producto pages — innecesario cuando podemos dejarlo vacío.

### Decision: Aliases en tokens.css (NO en config_new.css)

**Choice**: Los aliases `--color_accent → var(--color-accent)` viven en `tokens.css`  
**Alternatives considered**: Dejar aliases en config_new.css linkeado  
**Rationale**: Si los aliases están en config_new.css, habría que linkear config_new.css de nuevo — lo que contradice Fase 1. Los aliases en tokens.css son el único archivo que se agrega, y están claramente marcados para eliminación en Fase 4.

### Decision: Scope exclusivo index.html para esta fase

**Choice**: Solo se modifica el `<head>` de `index.html` (1 link agregado, orden preservado)  
**Alternatives considered**: Agregar tokens.css también a páginas de producto y aviso-de-privacidad  
**Rationale**: Las páginas de producto usan `luxury.css` + `product-v2.css`. `product-v2.css` no consume los tokens nuevos todavía. Agregar tokens.css a páginas de producto es Fase 3. Esta fase solo fija la home.

### Decision: Tokens en una sola regla :root sin @layer

**Choice**: Un bloque `:root { ... }` plano en tokens.css  
**Alternatives considered**: Usar `@layer tokens { :root { ... } }` para cascade control  
**Rationale**: El proyecto no usa `@layer` en ningún lado. Introducirlo podría crear especificidad inesperada con el CSS existente. Keeping it simple — un :root plano tiene la especificidad necesaria y es predecible.

## Data Flow

```
index.html HEAD (carga en orden):
  1. styles/tokens.css      ← :root con todos los tokens + aliases
  2. styles/luxury.css      ← consume tokens (var() calls) o hardcoded hex
  3. styles/gold-breeze.css ← consume tokens (var() calls) o hardcoded hex
  4. [inline styles]        ← 14 refs a var(--color-accent) — ahora resuelven

Browser Computed:
  var(--color-accent) → #D6B55E  ✅  (antes: unresolved → transparent/inherited)
  var(--color_white)  → #ffffff  ✅  (alias de compatibilidad)
  var(--color-gold)   → #D6B55E  ✅  (alias de compatibilidad)
```

## File Changes

| Archivo | Acción | Descripción |
|---------|--------|-------------|
| `styles/tokens.css` | **Create** | Sistema completo de design tokens — 7 categorías + aliases legacy |
| `index.html` | **Modify** | Agregar `<link rel="stylesheet" href="styles/tokens.css">` como primer link local |
| `styles/config_new.css` | **Modify** | Reemplazar todo el contenido con comentario de deprecación |

## Token Structure en tokens.css

```css
/* HomePower PTY — Design Tokens
   Única fuente de verdad CSS. Fase 4 eliminará los aliases legacy.
   ================================================================ */

:root {
  /* ── Paleta base ───────────────────────────────── */
  --color-bg-primary:    #111111;
  --color-bg-secondary:  #1a1a1a;
  --color-bg-surface:    #222222;

  /* ── Acento dorado (brand) ─────────────────────── */
  --color-accent:        #D6B55E;
  --color-accent-hover:  #b49542;
  --color-accent-dim:    rgba(201, 168, 76, 0.15);
  --color-accent-border: rgba(201, 168, 76, 0.25);

  /* ── Texto ─────────────────────────────────────── */
  --color-text:          #f5f5f5;
  --color-text-muted:    rgba(255, 255, 255, 0.55);
  --color-text-disabled: rgba(255, 255, 255, 0.30);

  /* ── Bordes ────────────────────────────────────── */
  --color-border:        rgba(201, 168, 76, 0.20);
  --color-border-strong: rgba(201, 168, 76, 0.40);
  --color-border-subtle: rgba(255, 255, 255, 0.08);

  /* ── Utilidad ──────────────────────────────────── */
  --color-whatsapp:      #25D366;
  --color-error:         #e05a5a;
  --color-success:       #4caf82;

  /* ── Tipografía ────────────────────────────────── */
  --font-heading:  'Playfair Display', Georgia, serif;
  --font-body:     'Inter', system-ui, sans-serif;
  --font-mono:     'JetBrains Mono', monospace;

  --text-xs:   0.75rem;
  --text-sm:   0.875rem;
  --text-base: 1rem;
  --text-lg:   1.125rem;
  --text-xl:   1.25rem;
  --text-2xl:  1.5rem;
  --text-3xl:  2rem;
  --text-4xl:  2.75rem;

  /* ── Espaciado ─────────────────────────────────── */
  --space-1:  4px;
  --space-2:  8px;
  --space-3:  12px;
  --space-4:  16px;
  --space-6:  24px;
  --space-8:  32px;
  --space-12: 48px;
  --space-16: 64px;
  --space-24: 96px;

  /* ── Layout ────────────────────────────────────── */
  --max-width:        1200px;
  --max-width-narrow: 800px;
  --border-radius-sm: 6px;
  --border-radius:    12px;
  --border-radius-lg: 20px;

  /* ── Sombras ───────────────────────────────────── */
  --shadow-sm:   0 1px 3px rgba(0, 0, 0, 0.4);
  --shadow-md:   0 4px 16px rgba(0, 0, 0, 0.5);
  --shadow-lg:   0 8px 32px rgba(0, 0, 0, 0.6);
  --shadow-gold: 0 0 24px rgba(201, 168, 76, 0.15);

  /* ── Transiciones ──────────────────────────────── */
  --transition-fast:  150ms ease;
  --transition-base:  250ms ease;
  --transition-slow:  400ms ease;

  /* ── Z-index ───────────────────────────────────── */
  --z-base:    0;
  --z-above:   10;
  --z-modal:   100;
  --z-toast:   200;
  --z-overlay: 300;

  /* ── Aliases legacy (eliminar en Fase 4) ────────── */
  --color_accent:      var(--color-accent);
  --color_black:       #2c3e50;
  --color_white:       #ffffff;
  --color-gold:        var(--color-accent);
  --color-gold-hover:  var(--color-accent-hover);
  --luxury-accent:     var(--color-accent);
}
```

## Testing Strategy

| Layer | Qué testear | Approach |
|-------|-------------|---------|
| Manual | `--color-accent` resuelve `#D6B55E` en DevTools Computed | Chrome DevTools → Elements → Computed |
| Manual | `--color_white` resuelve `#ffffff` | Chrome DevTools → Elements → Computed |
| Manual | tokens.css aparece primero en Network tab | F12 → Network → filter CSS |
| Manual | Sin errores en Console | F12 → Console, reload limpio |
| E2E | Regresión visual — los 18 tests Playwright siguen en verde | `npm test` |

## Migration / Rollout

1. Crear `styles/tokens.css`
2. Insertar link en `index.html` (primer lugar)
3. Vaciar `styles/config_new.css` con comentario de deprecación
4. Commit atómico: `feat(css): add tokens.css as single source of truth for CSS variables`
5. Verificación manual en DevTools antes de deploy

**Fase 4 (futura)**: Reemplazar hardcoded hex en `luxury.css` / `gold-breeze.css` con tokens. Eliminar aliases legacy de `tokens.css`. Agregar `tokens.css` a páginas de producto.

## Open Questions

- Ninguna — el scope está bien definido y la implementación es directa.
