# Delta for css-tokens

## ADDED Requirements

### Requirement: Variables --color_black y --color_white con valores correctos en config_new.css

`styles/config_new.css` MUST definir `--color_black` y `--color_white` con valores semánticamente correctos. Invertir estos valores genera texto invisible cuando el archivo es linkeado.

Los valores correctos MUST ser:

| Variable | Valor correcto | Valor incorrecto actual |
|----------|---------------|------------------------|
| `--color_black` | `#2c3e50` (dark navy) | `#bec2c4` (light gray — INVERTIDO) |
| `--color_white` | `#ffffff` (blanco) | `#000000` (negro — INVERTIDO) |

#### Scenario: Valores semánticos correctos en el archivo

- GIVEN el archivo `styles/config_new.css` existe en el repositorio
- WHEN se inspeccionan sus variables CSS
- THEN `--color_black` tiene valor `#2c3e50`
- AND `--color_white` tiene valor `#ffffff`

#### Scenario: No hay regresión visual cuando el archivo se linkea

- GIVEN `config_new.css` tiene los valores corregidos
- WHEN el archivo se linkea en un contexto HTML
- THEN el texto sobre fondo oscuro es claro (legible)
- AND el texto sobre fondo claro es oscuro (legible)
- AND no hay elementos con contraste invertido

#### Scenario: El archivo NO está linkeado en index.html (invariante a mantener)

- GIVEN el estado actual del sitio
- WHEN se inspeccionan los `<link>` tags del `<head>` de `index.html`
- THEN `config_new.css` NO aparece como stylesheet linkeado
- AND este change NO agrega ese link (fuera de scope — solo se corrigen los valores)
