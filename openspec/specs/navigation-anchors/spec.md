# Spec: navigation-anchors

## Requirements

### Requirement: Anchor target #testimonios

The `#testimonios` ID MUST exist in the DOM so that the nav link `href="#testimonios"` scrolls the page to the social proof area.

Because no dedicated testimonials section exists yet, the system SHALL expose the existing `#clientes` section via an alias anchor placed immediately before it. This anchor MUST NOT affect layout or accessibility.

#### Scenario: Usuario hace click en "Testimonios" desde el nav principal

- GIVEN el usuario está en la página de inicio (`/`)
- WHEN hace click en el link `href="#testimonios"` del menú de navegación de escritorio
- THEN el viewport hace scroll hacia la sección de clientes
- AND el URL cambia a `/#testimonios`
- AND ningún contenido queda oculto detrás del header fijo

#### Scenario: Usuario hace click en "Testimonios" desde el menú fullscreen mobile

- GIVEN el usuario está en mobile y tiene el menú fullscreen abierto
- WHEN hace click en el link `href="#testimonios"`
- THEN el menú se cierra
- AND el viewport hace scroll hacia la sección de clientes
- AND el elemento destino es visible en el viewport

#### Scenario: El anchor alias no afecta el layout

- GIVEN la página renderiza normalmente
- WHEN el DOM se inspecciona
- THEN el anchor `<a id="testimonios">` tiene `display: block`, `height: 0`, `visibility: hidden`, y `aria-hidden="true"`
- AND no desplaza ningún elemento circundante

---

### Requirement: Anchor target #oportunidades

El `#oportunidades` ID MUST existir en el DOM como parte de una sección de oportunidades laborales, de forma que el link `href="#oportunidades"` del nav lleve al usuario al formulario de aplicación.

#### Scenario: Usuario hace click en "Oportunidades" desde el nav principal

- GIVEN el usuario está en la página de inicio (`/`)
- WHEN hace click en el link `href="#oportunidades"` del menú de navegación de escritorio
- THEN el viewport hace scroll hacia la sección de oportunidades laborales
- AND el URL cambia a `/#oportunidades`
- AND el formulario de aplicación es visible en el viewport

#### Scenario: Usuario hace click en "Oportunidades" desde el menú fullscreen mobile

- GIVEN el usuario está en mobile y tiene el menú fullscreen abierto
- WHEN hace click en el link `href="#oportunidades"`
- THEN el menú se cierra
- AND el viewport hace scroll hacia la sección de oportunidades laborales

#### Scenario: El footer NO incluye el link a #oportunidades si no está en el nav principal

- GIVEN el footer tiene su propio bloque de navegación
- WHEN se renderiza la página
- THEN el footer solo incluye los links que ya existían: `#inicio`, `#nosotros`, `#clientes`, `#contacto`
- AND no se agrega `#oportunidades` al footer en este change (fuera de scope)
