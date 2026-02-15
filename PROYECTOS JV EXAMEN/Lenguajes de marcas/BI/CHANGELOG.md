# CHANGELOG - Bombas Ideal Website

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [4.1.0] - 2026-02-05

### 🎉 Major Refactor - "Professional Edition"

Esta versión representa una refactorización completa del codebase para transformarlo
de un proyecto "vibecoded" a una arquitectura profesional y mantenible.

### Añadido

#### Arquitectura CSS Modular
- `src/css/variables.css` - Sistema de design tokens con CSS Custom Properties
- `src/css/base.css` - Reset CSS y estilos base con accesibilidad
- `src/css/utilities.css` - Clases utilitarias (container, flex, grid, spacing)
- `src/css/main.css` - Punto de entrada que importa todos los módulos

#### Componentes CSS
- `src/css/components/buttons.css` - Sistema de botones con variantes y estados
- `src/css/components/navbar.css` - Navegación responsive con dropdowns
- `src/css/components/hero.css` - Hero slider con animaciones
- `src/css/components/cards.css` - Sistema de tarjetas (producto, servicio, noticia)
- `src/css/components/forms.css` - Formularios con validación visual
- `src/css/components/sections.css` - Layouts de secciones
- `src/css/components/modals.css` - Sistema de modales accesible
- `src/css/components/footer.css` - Footer multi-columna
- `src/css/components/bips.css` - Estilos específicos del selector BIPS

#### Arquitectura JavaScript ES6 Modules
- `src/js/config.js` - Configuración centralizada
- `src/js/main.js` - Punto de entrada principal
- `src/js/bundle.js` - Bundle con exposición global para compatibilidad

#### Módulos JavaScript
- `src/js/modules/utils.js` - Utilidades DOM, eventos, debounce/throttle
- `src/js/modules/navigation.js` - Navegación sticky, menú móvil, dropdowns
- `src/js/modules/slider.js` - Hero slider con touch/swipe y teclado
- `src/js/modules/animations.js` - Animaciones con Intersection Observer
- `src/js/modules/scrollTop.js` - Botón volver arriba
- `src/js/modules/modals.js` - Sistema de modales con focus trap
- `src/js/modules/easterEggs.js` - Konami code y secretos

#### Sistema BIPS Modular
- `src/js/bips/data.js` - Base de datos de series de bombas
- `src/js/bips/filter.js` - Motor de filtrado con scoring
- `src/js/bips/ui.js` - Interfaz de usuario del selector
- `src/js/bips/index.js` - Punto de entrada del sistema BIPS

#### Documentación
- `docs/README.md` - Documentación principal del proyecto
- `docs/ARCHITECTURE.md` - Arquitectura técnica detallada
- `docs/COMPONENTS.md` - Guía de uso de componentes
- `CHANGELOG.md` - Este archivo

#### HTML Actualizado
- `index-v4.html` - Nueva versión del index con estructura semántica
- `bips-v4.html` - Nueva versión del selector BIPS

### Cambiado
- Migración de CSS monolítico (3521 líneas) a arquitectura modular
- Migración de JavaScript monolítico (454 + 2190 líneas) a ES6 modules
- Mejora de accesibilidad (ARIA roles, focus management, skip links)
- Optimización de rendimiento (lazy loading, throttle, debounce)
- Nomenclatura BEM-inspired para clases CSS
- JSDoc en todos los módulos JavaScript

### Mejorado
- Soporte completo para `prefers-reduced-motion`
- Focus visible mejorado para navegación por teclado
- Semántica HTML5 correcta
- Separación de concerns (data/logic/UI)

### Técnico
- Stack: HTML5, CSS3 Custom Properties, Vanilla JavaScript ES6
- Sin dependencias de runtime (excepto Font Awesome)
- Compatibilidad: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- Fallback con `nomodule` para navegadores legacy

---

## [3.0.0] - 2026-01-20

### Añadido
- Sistema BIPS (Bombas Ideal Pump Selector)
- Calculadora hidráulica
- Exportación a PDF/Excel
- Historial de búsquedas
- Tema oscuro
- Comparador de series

---

## [2.5.0] - 2025-11-15

### Añadido
- Slider del hero con autoplay
- Animaciones al scroll
- Banner de cookies RGPD
- Páginas de productos individuales

### Cambiado
- Rediseño de la navegación
- Mejoras responsive

---

## [2.0.0] - 2025-08-01

### Añadido
- Rediseño completo del sitio
- Sección de noticias
- Formulario de contacto
- Integración con redes sociales

---

## [1.0.0] - 2024-01-01

### Añadido
- Versión inicial del sitio web
- Catálogo básico de productos
- Información corporativa
- Contacto

---

## Leyenda

- 🎉 **Añadido** - Nuevas funcionalidades
- 🔄 **Cambiado** - Cambios en funcionalidades existentes
- 🗑️ **Eliminado** - Funcionalidades eliminadas
- 🐛 **Corregido** - Corrección de bugs
- 🔒 **Seguridad** - Vulnerabilidades corregidas
- ⚡ **Rendimiento** - Mejoras de rendimiento
- ♿ **Accesibilidad** - Mejoras de accesibilidad

---

## Próximas versiones

### [4.2.0] - Planificado
- [ ] Internacionalización (i18n) - ES, EN, FR, PT
- [ ] PWA con service worker
- [ ] Modo offline para catálogos
- [ ] Backend PHP para formularios

### [5.0.0] - Futuro
- [ ] CMS headless (Strapi/Directus)
- [ ] API REST para integraciones
- [ ] Área de clientes
- [ ] Configurador 3D de bombas
