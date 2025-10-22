# Copilot Instructions for Homepowerpty.com

## Visión general del proyecto
Este repositorio es un sitio web estático para Home Power Pty, estructurado principalmente con HTML, CSS y JavaScript. No utiliza frameworks modernos ni sistemas de construcción automatizados. El backend se limita a formularios PHP simples para el envío de datos.

## Estructura principal
- `index.html`: Página principal y punto de entrada. Contiene la estructura base y referencias a scripts y estilos.
- `default.php`, `php/send_form.php`: Archivos PHP para manejo de formularios con validación CSRF y sanitización.
- `scripts/`: JavaScript para interactividad (sliders, filtros, formularios, validación en tiempo real).
- `styles/` y `styles/templates/`: Hojas de estilo CSS, organizadas por componentes y secciones.
- `media/` y `images/`: Recursos gráficos, íconos y fotos de productos/clientes.

## Convenciones y patrones de diseño
- **Nomenclatura**: Los archivos y carpetas usan nombres descriptivos en español e inglés. Los scripts están en minúsculas y separados por guiones bajos.
- **Interactividad**: Toda la lógica de UI está en archivos JS dentro de `scripts/`. No hay frameworks; todo es vanilla JS con manejo de eventos y validación en tiempo real.
- **Estilos**: Los estilos globales están en `styles/styles.css`. Los formularios tienen diseño moderno con efectos glassmorphism, animaciones CSS y validación visual.
- **Formularios**: Usan labels flotantes, validación en tiempo real, estados visuales (valid/invalid), y animaciones suaves.
- **Responsividad**: Diseño mobile-first con breakpoints en 768px y 480px.

## Patrones específicos del formulario
- **Labels flotantes**: Se activan con las clases `.active` cuando hay contenido o focus
- **Validación visual**: Clases `.valid`/`.invalid` en inputs con colores y animaciones
- **Estados de envío**: Botones se deshabilitan durante envío con cambio de texto
- **Mensajes**: Sistema de notificaciones con clases `.success`/`.error` y timeouts automáticos

## Flujos de desarrollo
- **No hay sistema de build**: Los cambios se reflejan directamente en los archivos fuente.
- **Debugging**: Se realiza en el navegador usando DevTools.
- **Pruebas**: Manuales, validando funcionalidad y diseño responsivo.

## Integraciones y dependencias
- **PHP**: Solo para formularios con seguridad CSRF, rate limiting y validación backend
- **Recursos estáticos**: Todos los recursos se sirven directamente desde el sistema de archivos
- **Fonts**: Google Fonts (Montserrat, Lato) definidas en variables CSS

## Ejemplo de patrón típico
- Para agregar una nueva funcionalidad de UI:
  1. Crear HTML semántico con clases descriptivas
  2. Definir estilos en `styles/styles.css` usando variables CSS existentes
  3. Agregar interactividad en `scripts/` con vanilla JS
  4. Implementar validación tanto frontend como backend si es necesario
  5. Asegurar responsividad en todos los breakpoints

## Variables CSS principales
```css
:root {
    --color_orange: #FF9F1C;
    --color_green: #4CAF50;
    --font_title: "Montserrat", sans-serif;
    --font_text: "Lato", sans-serif;
}
```

## Recomendaciones para agentes AI
- Mantener la estructura y convenciones existentes
- Usar las variables CSS definidas para consistencia visual
- Implementar validación tanto frontend como backend para formularios
- Seguir el patrón de labels flotantes y animaciones suaves
- Asegurar accesibilidad y responsividad en todas las implementaciones
- Documentar cambios relevantes en comentarios dentro de los archivos modificados

## Archivos clave
- `index.html`, `styles/styles.css`, `scripts/send_contact_form.js`, `php/send_form.php`

---
¿Falta alguna convención, flujo o integración importante? Por favor, indícalo para mejorar estas instrucciones.