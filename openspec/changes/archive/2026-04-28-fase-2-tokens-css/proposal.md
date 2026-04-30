# Proposal: fase-2-tokens-css
**Fecha**: 2026-04-28  
**Status**: proposed

## Intent
Crear `styles/tokens.css` como única fuente de verdad del sistema visual de HomePower PTY, eliminando el conflicto de nombres de variables entre `config_new.css` y `styles.css`.

## Contexto actual
- `index.html` carga: `luxury.css` + `gold-breeze.css` (2 archivos locales)
- `config_new.css` **no está linkeado** en index.html (fue removido en Fase 1)
- `config_new.css` tiene variables con naming underscore (`--color_accent`) que no coinciden con los usos de hyphen (`--color-accent`) en el HTML
- No existe `styles/tokens.css` todavía
- Las referencias a `--color-accent` en index.html (14 ocurrencias inline) actualmente no resuelven a ninguna variable definida

## Scope
1. Crear `styles/tokens.css` — sistema completo de design tokens
2. Insertar `tokens.css` como **primer** CSS en `index.html` (antes de luxury.css)
3. Vaciar `config_new.css` → solo comentario de deprecación
4. Verificación visual en DevTools

## Out of scope (Fase 4)
- Reemplazar hardcoded hex values en luxury.css / gold-breeze.css
- Eliminar `config_new.css` definitivamente

## Token system
### Paleta base
- `--color-bg-primary: #111111`
- `--color-bg-secondary: #1a1a1a`
- `--color-bg-surface: #222222`

### Acento dorado (brand)
- `--color-accent: #D6B55E`
- `--color-accent-hover: #b49542`
- `--color-accent-dim: rgba(201,168,76,0.15)`
- `--color-accent-border: rgba(201,168,76,0.25)`

### Texto
- `--color-text: #f5f5f5`
- `--color-text-muted: rgba(255,255,255,0.55)`
- `--color-text-disabled: rgba(255,255,255,0.30)`

### Utilidad
- `--color-whatsapp: #25D366`
- `--color-error: #e05a5a`
- `--color-success: #4caf82`

### Tipografía, espaciado, layout, sombras, transiciones, z-index
(ver tokens.css completo en tab del attachment)

### Aliases de compatibilidad (se eliminan en Fase 4)
- `--color_accent` → `var(--color-accent)`
- `--color_black: #2c3e50`
- `--color_white: #ffffff`
- `--color-gold` → `var(--color-accent)`
- `--luxury-accent` → `var(--color-accent)`

## Validación de éxito
- `--color-accent` resuelve `#D6B55E` en Chrome DevTools Computed
- `--color_white` resuelve `#ffffff` (no `#000000`)
- tokens.css aparece primero en Network tab
- Cero errores CSS en Console
- Visual: dorado visible en hero, CTAs, bordes de cards
