# Bombas Ideal - Documentación Técnica

<p align="center">
  <img src="assets/images/logo.png" alt="Bombas Ideal" width="200">
</p>

<p align="center">
  <strong>Sistema web corporativo de Bombas Ideal S.A.</strong><br>
  Fabricantes de bombas y grupos de presión desde 1902
</p>

<p align="center">
  <a href="#estructura">Estructura</a> •
  <a href="#instalación">Instalación</a> •
  <a href="#desarrollo">Desarrollo</a> •
  <a href="#componentes">Componentes</a> •
  <a href="#despliegue">Despliegue</a>
</p>

---

## 📋 Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Arquitectura CSS](#arquitectura-css)
- [Arquitectura JavaScript](#arquitectura-javascript)
- [Sistema BIPS](#sistema-bips)
- [Guía de Componentes](#guía-de-componentes)
- [Guía de Estilos](#guía-de-estilos)
- [Despliegue](#despliegue)
- [Mantenimiento](#mantenimiento)

---

## 📝 Descripción General

Este proyecto es el sitio web corporativo de **Bombas Ideal S.A.**, una empresa española fundada en 1902 especializada en la fabricación de bombas de agua y grupos de presión.

### Stack Tecnológico

| Tecnología | Uso |
|------------|-----|
| HTML5 | Estructura semántica |
| CSS3 | Estilos con Custom Properties |
| JavaScript ES6+ | Interactividad modular |
| GitHub Pages | Hosting estático |

### Características Principales

- ✅ Diseño responsive (mobile-first)
- ✅ Arquitectura CSS modular (BEM-inspired)
- ✅ JavaScript modular con ES Modules
- ✅ Sistema de diseño con CSS Custom Properties
- ✅ Accesibilidad (WCAG 2.1 AA)
- ✅ Optimización de rendimiento
- ✅ Sistema BIPS (selector de productos)

---

## 📁 Estructura del Proyecto

```
BI/
├── index.html              # Página principal
├── bips.html               # Selector de productos BIPS
├── noticias.html           # Página de noticias
├── aviso-legal.html        # Aviso legal
├── politica-privacidad.html
├── politica-cookies.html
│
├── assets/
│   ├── images/             # Imágenes del sitio
│   └── docs/               # Catálogos PDF
│
├── productos/              # Páginas de productos
│   ├── producto.css        # Estilos específicos
│   ├── serie-*.html        # Páginas de series
│   └── ...
│
├── src/                    # Código fuente modular
│   ├── css/
│   │   ├── variables.css   # Design tokens
│   │   ├── base.css        # Reset y base
│   │   ├── utilities.css   # Clases de utilidad
│   │   ├── main.css        # Entry point CSS
│   │   └── components/     # Componentes CSS
│   │       ├── buttons.css
│   │       ├── navbar.css
│   │       ├── hero.css
│   │       ├── cards.css
│   │       ├── forms.css
│   │       ├── sections.css
│   │       ├── modals.css
│   │       ├── footer.css
│   │       └── bips.css
│   │
│   └── js/
│       ├── config.js       # Configuración
│       ├── main.js         # Entry point JS
│       └── modules/        # Módulos JS
│           ├── utils.js
│           ├── navigation.js
│           ├── slider.js
│           ├── animations.js
│           ├── scrollTop.js
│           ├── modals.js
│           └── easterEggs.js
│
├── docs/                   # Documentación
│   └── ...
│
└── README.md               # Este archivo
```

---

## 🎨 Arquitectura CSS

### Design Tokens (variables.css)

Todas las propiedades visuales están centralizadas en custom properties:

```css
/* Ejemplo de uso */
.button {
    background-color: var(--bi-primary-500);
    padding: var(--bi-space-4);
    border-radius: var(--bi-radius-md);
    font-size: var(--bi-text-base);
}
```

### Categorías de Variables

| Prefijo | Descripción | Ejemplo |
|---------|-------------|---------|
| `--bi-primary-*` | Colores principales (azul) | `--bi-primary-500` |
| `--bi-secondary-*` | Colores secundarios (cyan) | `--bi-secondary-500` |
| `--bi-gray-*` | Escala de grises | `--bi-gray-100` |
| `--bi-space-*` | Espaciado (4px base) | `--bi-space-4` = 16px |
| `--bi-text-*` | Tamaños de texto | `--bi-text-lg` |
| `--bi-radius-*` | Border radius | `--bi-radius-md` |
| `--bi-shadow-*` | Box shadows | `--bi-shadow-lg` |
| `--bi-z-*` | Z-index layers | `--bi-z-modal` |

### Orden de Importación

```css
/* main.css - Orden correcto */
@import './variables.css';    /* 1. Tokens */
@import './base.css';         /* 2. Reset */
@import './utilities.css';    /* 3. Utilidades */
@import './components/*.css'; /* 4. Componentes */
```

---

## ⚡ Arquitectura JavaScript

### Módulos

El JavaScript está organizado en módulos ES6:

```javascript
// Importar módulo
import { $, $$, addClass } from './modules/utils.js';

// Usar funciones
const button = $('.btn');
addClass(button, 'active');
```

### Módulos Disponibles

| Módulo | Descripción |
|--------|-------------|
| `config.js` | Configuración centralizada |
| `utils.js` | Funciones de utilidad (DOM, eventos, etc.) |
| `navigation.js` | Navbar, menú móvil, dropdowns |
| `slider.js` | Hero slider con autoplay |
| `animations.js` | Animaciones de entrada (Intersection Observer) |
| `scrollTop.js` | Botón scroll to top |
| `modals.js` | Sistema de ventanas modales |
| `easterEggs.js` | Secretos ocultos 🎮 |

### Configuración (config.js)

```javascript
import { CONFIG } from './config.js';

// Acceder a configuración
console.log(CONFIG.company.name); // "Bombas Ideal S.A."
console.log(CONFIG.slider.interval); // 6000
```

---

## 🔍 Sistema BIPS

**BIPS** (Bombas Ideal Product Selector) es el sistema de selección de productos basado en parámetros hidráulicos.

### Funcionamiento

1. Usuario introduce parámetros (caudal, altura, aplicación)
2. Sistema filtra productos compatibles
3. Muestra resultados ordenados por coincidencia

### Archivos

- `bips.html` - Página del selector
- `bips.js` - Lógica de filtrado (legacy)
- `bips.css` - Estilos específicos
- `src/css/components/bips.css` - Estilos refactorizados

---

## 🧩 Guía de Componentes

### Botones

```html
<!-- Botón primario -->
<a href="#" class="btn btn-primary">Contactar</a>

<!-- Botón secundario -->
<a href="#" class="btn btn-secondary">Ver más</a>

<!-- Botón outline -->
<a href="#" class="btn btn-outline">Descargar</a>

<!-- Con icono -->
<a href="#" class="btn btn-primary btn-icon">
    <i class="fas fa-download"></i>
    Catálogo
</a>

<!-- Tamaños -->
<button class="btn btn-primary btn-sm">Pequeño</button>
<button class="btn btn-primary btn-lg">Grande</button>
```

### Cards

```html
<div class="card card--product">
    <div class="card-image">
        <img src="producto.jpg" alt="Producto">
        <span class="card-badge">Nuevo</span>
    </div>
    <div class="card-body">
        <span class="card-category">Serie NXA</span>
        <h3 class="card-title">Bomba centrífuga</h3>
        <p class="card-text">Descripción del producto...</p>
    </div>
    <div class="card-footer">
        <a href="#" class="btn btn-primary btn-sm">Ver detalles</a>
    </div>
</div>
```

### Formularios

```html
<form class="form form--grid">
    <div class="form-group">
        <label class="form-label form-label--required">Nombre</label>
        <input type="text" class="form-control" placeholder="Tu nombre">
    </div>
    
    <div class="form-group">
        <label class="form-label">Email</label>
        <div class="input-group">
            <i class="input-group-icon fas fa-envelope"></i>
            <input type="email" class="form-control" placeholder="email@ejemplo.com">
        </div>
    </div>
    
    <div class="form-group form-group--full">
        <label class="form-label">Mensaje</label>
        <textarea class="form-control" rows="4"></textarea>
    </div>
    
    <button type="submit" class="btn btn-primary">Enviar</button>
</form>
```

### Animaciones

```html
<!-- Elementos que se animan al entrar en viewport -->
<div data-animate="fadeUp">Contenido 1</div>
<div data-animate="fadeUp" data-animate-delay="200">Contenido 2</div>
<div data-animate="scaleIn">Contenido 3</div>
```

### Modales

```html
<!-- Trigger -->
<button data-modal-open="contactModal">Abrir Modal</button>

<!-- Modal -->
<div class="modal" id="contactModal">
    <div class="modal-overlay"></div>
    <div class="modal-container">
        <div class="modal-header">
            <h3 class="modal-title">Contacto</h3>
            <button class="modal-close" data-modal-close>&times;</button>
        </div>
        <div class="modal-body">
            <!-- Contenido -->
        </div>
        <div class="modal-footer">
            <button class="btn btn-secondary" data-modal-close>Cancelar</button>
            <button class="btn btn-primary">Enviar</button>
        </div>
    </div>
</div>
```

---

## 🎯 Guía de Estilos

### Colores

| Color | Variable | Uso |
|-------|----------|-----|
| Azul oscuro | `--bi-primary-500` | Elementos principales |
| Cyan | `--bi-accent` | Acentos, CTAs |
| Gris oscuro | `--bi-bg-dark` | Fondos oscuros |
| Blanco | `--bi-bg-primary` | Fondos claros |

### Tipografía

- **Font Principal:** Montserrat (headings, UI)
- **Fallback:** system-ui, sans-serif

### Espaciado

Sistema de 4px base:
- `--bi-space-1` = 4px
- `--bi-space-2` = 8px
- `--bi-space-4` = 16px
- `--bi-space-8` = 32px

---

## 🚀 Despliegue

### GitHub Pages

El sitio se despliega automáticamente en GitHub Pages:

```bash
# Push a main para desplegar
git push origin main
```

URL: `https://mutenros.github.io/BI`

### Checklist Pre-Despliegue

- [ ] Validar HTML (W3C Validator)
- [ ] Verificar responsive en móviles
- [ ] Comprobar links rotos
- [ ] Optimizar imágenes
- [ ] Testear en múltiples navegadores
- [ ] Verificar accesibilidad

---

## 🔧 Mantenimiento

### Añadir Nuevo Producto

1. Crear archivo en `productos/serie-xxx.html`
2. Usar template existente
3. Añadir imágenes a `assets/images/`
4. Actualizar navegación si necesario
5. Añadir a sistema BIPS si aplica

### Modificar Estilos

1. Identificar componente en `src/css/components/`
2. Seguir convenciones BEM
3. Usar variables de `variables.css`
4. Documentar cambios

### Añadir Nueva Funcionalidad JS

1. Crear módulo en `src/js/modules/`
2. Exportar funciones públicas
3. Importar en `main.js`
4. Inicializar en `initApp()`

---

## 📄 Licencia

Propiedad de **Bombas Ideal S.A.** - Todos los derechos reservados.

---

<p align="center">
  <sub>Desarrollado con 💙 para Bombas Ideal S.A.</sub>
</p>
