# Delta for css-tokens

## MODIFIED Requirements

### Requirement: Variables --color_black y --color_white con valores correctos en config_new.css

`styles/config_new.css` MUST contener un comentario de deprecación y NO MUST definir variables `:root` activas. Todas las variables han sido migradas a `styles/tokens.css`, que es la única fuente de verdad.

(Previously: config_new.css definía las variables directamente en :root. Ahora se depreca — el contenido es reemplazado por un comentario, las variables viven en tokens.css)

#### Scenario: Valores semánticos correctos en el archivo

- GIVEN el archivo `styles/config_new.css` existe en el repositorio
- WHEN se inspeccionan sus variables CSS
- THEN `--color_black` NO aparece definida en config_new.css (migrada a tokens.css como alias)
- AND `--color_white` NO aparece definida en config_new.css (migrada a tokens.css como alias)
- AND el archivo contiene solo un comentario de deprecación

#### Scenario: No hay regresión visual cuando el archivo se linkea

- GIVEN `config_new.css` contiene solo el comentario de deprecación
- WHEN el archivo se linkea en un contexto HTML
- THEN no aporta ninguna variable ni reset CSS
- AND las variables son resueltas por tokens.css

#### Scenario: El archivo NO está linkeado en index.html (invariante)

- GIVEN el estado actual del sitio
- WHEN se inspeccionan los `<link>` tags del `<head>` de `index.html`
- THEN `config_new.css` NO aparece como stylesheet linkeado
- AND ningún change agrega ese link sin una decisión explícita (fuera de scope)

---

## ADDED Requirements

### Requirement: tokens.css — única fuente de verdad de variables CSS

El archivo `styles/tokens.css` MUST existir y MUST ser el único archivo que define variables CSS en `:root`. Ningún otro archivo CSS del proyecto MUST definir variables en `:root`.

#### Scenario: El archivo existe con todas las categorías de tokens

- GIVEN el proyecto HomePower PTY
- WHEN se inspecciona `styles/tokens.css`
- THEN el archivo existe en `styles/tokens.css`
- AND contiene tokens de paleta base (`--color-bg-primary`, `--color-bg-secondary`, `--color-bg-surface`)
- AND contiene tokens de acento dorado (`--color-accent`, `--color-accent-hover`, `--color-accent-dim`, `--color-accent-border`)
- AND contiene tokens de texto (`--color-text`, `--color-text-muted`, `--color-text-disabled`)
- AND contiene tokens de bordes (`--color-border`, `--color-border-strong`, `--color-border-subtle`)
- AND contiene tokens de utilidad (`--color-whatsapp`, `--color-error`, `--color-success`)
- AND contiene tokens de tipografía (`--font-heading`, `--font-body`, escala de texto)
- AND contiene tokens de espaciado (`--space-1` a `--space-24`)
- AND contiene tokens de layout (`--max-width`, `--border-radius`, `--border-radius-sm`, `--border-radius-lg`)
- AND contiene tokens de sombras (`--shadow-sm`, `--shadow-md`, `--shadow-lg`, `--shadow-gold`)
- AND contiene tokens de transición (`--transition-fast`, `--transition-base`, `--transition-slow`)
- AND contiene tokens de z-index (`--z-base`, `--z-above`, `--z-modal`, `--z-toast`, `--z-overlay`)

#### Scenario: --color-accent resuelve al valor dorado correcto

- GIVEN `styles/tokens.css` está linkeado en `index.html`
- WHEN se evalúa `--color-accent` en el contexto del documento
- THEN su valor computado es `#D6B55E`

#### Scenario: --color-text resuelve a un valor claro (sitio oscuro)

- GIVEN `styles/tokens.css` está linkeado en `index.html`
- WHEN se evalúa `--color-text` en el contexto del documento
- THEN su valor computado es `#f5f5f5`

---

### Requirement: tokens.css cargado antes que todos los demás CSS en index.html

`styles/tokens.css` MUST ser el primer `<link rel="stylesheet">` local en el `<head>` de `index.html`, antes de `luxury.css` y `gold-breeze.css`. El orden de carga garantiza que los tokens estén disponibles para cualquier CSS que los consuma.

#### Scenario: Orden correcto en el head de index.html

- GIVEN el archivo `index.html`
- WHEN se inspeccionan los `<link rel="stylesheet">` locales en orden de aparición
- THEN el primer stylesheet local es `styles/tokens.css`
- AND `styles/luxury.css` aparece después de `styles/tokens.css`
- AND `styles/gold-breeze.css` aparece después de `styles/luxury.css`

#### Scenario: No hay override de --color-accent por archivos posteriores

- GIVEN `tokens.css` carga antes que `luxury.css` y `gold-breeze.css`
- WHEN el browser parsea los stylesheets en orden
- THEN ningún archivo posterior redefine `--color-accent` con un valor diferente en `:root`
- AND el valor computado final de `--color-accent` es `#D6B55E`

---

### Requirement: Aliases de compatibilidad para variables legacy

`styles/tokens.css` MUST incluir aliases que mapeen los nombres de variables legacy (underscore) a los tokens nuevos (hyphen). Esto garantiza que código existente que use nombres viejos no se rompa durante la transición.

Los aliases MUST ser:

| Alias (legacy) | Resuelve a |
|----------------|-----------|
| `--color_accent` | `var(--color-accent)` |
| `--color_black` | `#2c3e50` |
| `--color_white` | `#ffffff` |
| `--color-gold` | `var(--color-accent)` |
| `--color-gold-hover` | `var(--color-accent-hover)` |
| `--luxury-accent` | `var(--color-accent)` |

#### Scenario: Alias --color_white resuelve al blanco correcto

- GIVEN `styles/tokens.css` está linkeado
- WHEN se evalúa `--color_white` en el documento
- THEN su valor computado es `#ffffff` (NO `#000000`)

#### Scenario: Alias --color_accent resuelve al dorado

- GIVEN `styles/tokens.css` está linkeado
- WHEN se evalúa `--color_accent` en el documento
- THEN su valor computado es `#D6B55E`

#### Scenario: Los aliases se eliminan en Fase 4

- GIVEN que tokens.css fue creado con aliases
- WHEN se complete la Fase 4 (limpieza CSS legacy)
- THEN los aliases MUST ser eliminados de tokens.css
- AND todo el código que usaba nombres legacy MUST haber sido migrado a los nombres nuevos

---

### Requirement: Las referencias --color-accent en index.html resuelven correctamente

El archivo `index.html` contiene 14 referencias inline a `var(--color-accent)`. Con `tokens.css` linkeado, TODAS estas referencias MUST resolver a `#D6B55E`.

#### Scenario: Color de acento visible en elementos decorativos

- GIVEN `index.html` cargado en el browser con `tokens.css` activo
- WHEN el usuario visualiza la página
- THEN los SVG de iconos con `stroke="var(--color-accent)"` muestran color dorado `#D6B55E`
- AND los títulos con `color:var(--color-accent)` muestran el color dorado
- AND los bordes y separadores con el token dorado son visibles
