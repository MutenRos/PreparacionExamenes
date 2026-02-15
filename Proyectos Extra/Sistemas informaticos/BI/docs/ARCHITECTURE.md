# Arquitectura del Proyecto

## Visión General

Este documento describe la arquitectura técnica del sitio web de Bombas Ideal, incluyendo decisiones de diseño, patrones utilizados y guías para desarrolladores.

---

## Principios de Diseño

### 1. Modularidad
Cada componente (CSS y JS) tiene una única responsabilidad y puede ser utilizado de forma independiente.

### 2. Simplicidad
No se utilizan frameworks pesados. El stack es vanilla HTML, CSS y JavaScript para máximo rendimiento y control.

### 3. Mantenibilidad
Código bien documentado con JSDoc, nombres descriptivos y separación clara de responsabilidades.

### 4. Rendimiento
- Sin dependencias de build (no webpack, no bundler)
- CSS y JS modulares que pueden cargarse bajo demanda
- Imágenes optimizadas
- Minimal JavaScript en página inicial

---

## Arquitectura CSS

### Sistema de Capas

```
┌─────────────────────────────────────────────┐
│  1. VARIABLES (Design Tokens)               │
│  ├── Colores                                │
│  ├── Tipografía                             │
│  ├── Espaciado                              │
│  └── Sombras, Radios, Transiciones         │
├─────────────────────────────────────────────┤
│  2. BASE (Reset + Defaults)                 │
│  ├── Box-sizing reset                       │
│  ├── Typography defaults                    │
│  └── Accesibilidad base                     │
├─────────────────────────────────────────────┤
│  3. UTILITIES (Clases de utilidad)          │
│  ├── Contenedores                           │
│  ├── Flexbox/Grid helpers                   │
│  ├── Espaciado                              │
│  └── Tipografía                             │
├─────────────────────────────────────────────┤
│  4. COMPONENTS (Componentes UI)             │
│  ├── Buttons                                │
│  ├── Cards                                  │
│  ├── Forms                                  │
│  ├── Navigation                             │
│  └── ...                                    │
├─────────────────────────────────────────────┤
│  5. PAGE-SPECIFIC (Overrides)               │
│  └── Estilos específicos de página          │
└─────────────────────────────────────────────┘
```

### Nomenclatura CSS

Usamos una convención inspirada en BEM pero simplificada:

```css
/* Bloque */
.card { }

/* Elemento (doble guión bajo opcional, pero preferimos guión simple) */
.card-header { }
.card-body { }
.card-footer { }

/* Modificador (doble guión) */
.card--featured { }
.card--horizontal { }

/* Estado (prefijo is-/has-) */
.card.is-active { }
.nav-menu.is-open { }
```

### Variables CSS

Todas las variables usan el prefijo `--bi-` (Bombas Ideal):

```css
/* Formato */
--bi-[categoría]-[variante]

/* Ejemplos */
--bi-primary-500      /* Color primario, tono medio */
--bi-space-4          /* Espaciado nivel 4 (16px) */
--bi-text-lg          /* Texto large */
--bi-radius-md        /* Border radius medium */
```

---

## Arquitectura JavaScript

### Patrón de Módulos

Cada módulo sigue esta estructura:

```javascript
/**
 * =============================================================================
 * BOMBAS IDEAL - [Nombre del Módulo]
 * =============================================================================
 * @description  [Descripción]
 * @module       [nombreModulo]
 */

/* STATE (Estado privado) */
const state = { };

/* PRIVATE FUNCTIONS */
function privateFunction() { }

/* PUBLIC API */
export function init() { }
export function publicMethod() { }

/* DEFAULT EXPORT */
export default { init, publicMethod };
```

### Flujo de Inicialización

```
document.ready
    │
    └── initApp()
        │
        ├── Navigation.init()
        ├── Slider.init()
        ├── Animations.init()
        ├── ScrollTop.init()
        ├── Modals.init()
        └── EasterEggs.init()
```

### Comunicación entre Módulos

Los módulos se comunican a través de:

1. **Eventos del DOM** (Custom Events)
2. **Configuración compartida** (config.js)
3. **Estado global mínimo** (window.BI)

```javascript
// Disparar evento
element.dispatchEvent(new CustomEvent('modal:open', { detail: { id: 'myModal' }}));

// Escuchar evento
document.addEventListener('modal:open', (e) => {
    console.log(e.detail.id);
});
```

---

## Estructura de Archivos

### Convenciones de Nombres

| Tipo | Convención | Ejemplo |
|------|------------|---------|
| Archivos HTML | kebab-case | `aviso-legal.html` |
| Archivos CSS | kebab-case | `buttons.css` |
| Archivos JS | camelCase | `scrollTop.js` |
| Carpetas | kebab-case | `my-folder/` |
| Clases CSS | kebab-case | `.nav-menu` |
| Variables CSS | kebab-case | `--bi-primary-500` |
| Funciones JS | camelCase | `handleClick()` |
| Constantes JS | SCREAMING_SNAKE | `SCROLL_THRESHOLD` |

### Organización de Componentes CSS

Cada archivo de componente contiene:

1. **Header documentation** - Descripción, autor, versión
2. **Estructura HTML** - Ejemplo de uso
3. **Base styles** - Estilos principales
4. **Variants** - Modificadores
5. **States** - Estados (hover, active, disabled)
6. **Responsive** - Media queries

---

## Patrones de Diseño

### Observer Pattern (Animaciones)

```javascript
const observer = new IntersectionObserver(callback, options);
elements.forEach(el => observer.observe(el));
```

### Module Pattern (Encapsulación)

```javascript
const Module = (function() {
    // Privado
    let privateVar = 0;
    
    // Público
    return {
        init: function() { },
        getVar: function() { return privateVar; }
    };
})();
```

### Event Delegation

```javascript
document.addEventListener('click', (e) => {
    const button = e.target.closest('[data-action]');
    if (button) {
        handleAction(button.dataset.action);
    }
});
```

---

## Rendimiento

### Optimizaciones Implementadas

1. **CSS**
   - Custom Properties (menos repetición)
   - Crítico inline (futuro)
   - Sin !important

2. **JavaScript**
   - Event delegation
   - Throttle/Debounce en scroll
   - Lazy loading (Intersection Observer)
   - ES Modules (tree-shaking futuro)

3. **Imágenes**
   - Formato WebP cuando posible
   - Lazy loading nativo
   - Srcset para responsive

### Métricas Objetivo

| Métrica | Objetivo |
|---------|----------|
| First Contentful Paint | < 1.5s |
| Largest Contentful Paint | < 2.5s |
| Time to Interactive | < 3.5s |
| Cumulative Layout Shift | < 0.1 |

---

## Accesibilidad

### Implementaciones

- Skip links
- Focus visible
- ARIA labels donde necesario
- Contraste de colores (WCAG AA)
- Navegación por teclado
- Reduced motion support

### Testing

```javascript
// Verificar preferencias de usuario
if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    // Desactivar animaciones
}
```

---

## Compatibilidad

### Navegadores Soportados

| Navegador | Versión Mínima |
|-----------|----------------|
| Chrome | 80+ |
| Firefox | 75+ |
| Safari | 13+ |
| Edge | 80+ |
| Samsung Internet | 12+ |

### Características Modernas Usadas

- CSS Custom Properties
- CSS Grid / Flexbox
- ES6 Modules
- Intersection Observer
- Fetch API

---

## Desarrollo Futuro

### Mejoras Planificadas

- [ ] Service Worker para offline
- [ ] Build system opcional (Vite)
- [ ] Componentes Web (Web Components)
- [ ] Internacionalización (i18n)
- [ ] Testing automatizado

### Deuda Técnica

- Migrar `bips.js` legacy a módulos
- Unificar estilos de productos
- Optimizar imágenes del catálogo
