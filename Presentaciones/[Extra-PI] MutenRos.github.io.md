# MUTENROS // Portfolio Personal

![Synthwave Portfolio](https://img.shields.io/badge/Theme-Synthwave-ff2a6d?style=for-the-badge)

> 🔗 **GitHub Pages:** [https://mutenros.github.io/](https://mutenros.github.io/)

## Introducción

Portfolio personal interactivo con estética **Synthwave/Retrowave** de los años 80. El proyecto es una single-page application que muestra mis habilidades como desarrollador web, integra la API de GitHub para mostrar proyectos en tiempo real, incluye un formulario de contacto con backend PHP y contiene un easter egg temático de Matrix activable mediante el código Konami.

El stack tecnológico abarca **HTML5 semántico, CSS3 modular con Custom Properties, JavaScript ES6 con módulos nativos, PHP para la API de contacto y Python para generación de estadísticas**. Todo con un diseño responsive, accesible y optimizado en rendimiento.

---

## Desarrollo de las partes

### 1. Estructura HTML5 semántica y SEO

La página principal utiliza etiquetas semánticas de HTML5 (`<header>`, `<main>`, `<section>`, `<article>`, `<footer>`) junto con atributos ARIA para asegurar accesibilidad. Incluye meta tags Open Graph para redes sociales y preconnect para optimizar la carga de recursos externos.

```html
<!-- index.html, líneas 31-52 -->
<meta name="description" content="Portfolio de Dario (MutenRos) - Desarrollador Web Full Stack...">
<meta property="og:type" content="website">
<meta property="og:title" content="MUTENROS // Portfolio">
<meta property="og:url" content="https://mutenros.github.io">
<meta name="theme-color" content="#0d0221">

<!-- Preconnect para rendimiento -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdnjs.cloudflare.com">
```

Las secciones usan `aria-labelledby` para vincular cada section con su título, y los elementos decorativos llevan `aria-hidden="true"` para que los lectores de pantalla los ignoren.

```html
<!-- index.html, líneas 129-130 -->
<section id="about" class="about section" aria-labelledby="about-title">
    <h2 id="about-title" class="section__title">SOBRE <span class="section__title-highlight">MÍ</span></h2>
```

---

### 2. Sistema de diseño CSS con Custom Properties

Todo el diseño se basa en un sistema de variables CSS centralizado en `variables.css`. Define una paleta de colores neon (pink, cyan, purple), tipografías (Orbitron para títulos, Rajdhani para cuerpo), espaciados, sombras, transiciones y una escala de z-index organizada.

```css
/* assets/css/variables.css, líneas 27-50 */
:root {
    --color-neon-pink: #ff2a6d;
    --color-neon-cyan: #05d9e8;
    --color-neon-purple: #d300c5;
    --color-neon-blue: #7b61ff;
    --color-bg-primary: #0d0221;
    --color-bg-secondary: #1a0533;
    --color-text-primary: #ffffff;
    --color-text-muted: rgba(255, 255, 255, 0.6);

    /* Tipografía */
    --font-display: 'Orbitron', sans-serif;
    --font-body: 'Rajdhani', sans-serif;

    /* Efectos neon */
    --glow-pink: 0 0 30px var(--color-neon-pink), 0 0 60px var(--color-neon-pink);
    --glow-cyan: 0 0 30px var(--color-neon-cyan);
}
```

La arquitectura CSS es modular: un archivo `main.css` importa 6 archivos especializados en orden (variables → base → layout → components → sections → background), siguiendo una metodología de separación de responsabilidades.

```css
/* assets/css/main.css, líneas 25-57 */
@import url('variables.css');
@import url('base.css');
@import url('layout.css');
@import url('components.css');
@import url('sections.css');
@import url('background.css');
```

---

### 3. JavaScript ES6 Modules — Arquitectura modular

La aplicación JavaScript usa una arquitectura de módulos ES6 nativos con un punto de entrada (`main.js`) que instancia la clase `PortfolioApp` y coordina la inicialización de todos los módulos: background, navigation, projects y easter egg.

```javascript
// assets/js/main.js, líneas 22-27
import CONFIG from './config.js';
import backgroundEffects from './modules/background.js';
import navigation from './modules/navigation.js';
import githubProjects from './modules/projects.js';
import matrixEasterEgg from './modules/matrix-easter-egg.js';
```

```javascript
// assets/js/main.js, líneas 56-63
async init() {
    this.initBackground();
    this.initNavigation();
    await this.initProjects();
    this.initEasterEgg();
    this.isInitialized = true;
    console.log('[PortfolioApp] Initialization complete');
}
```

Cada módulo es una clase con patrón Singleton que se exporta como instancia única, lo que permite un diseño limpio y testeable.

---

### 4. Configuración centralizada y congelada

Toda la configuración de la aplicación reside en `config.js`: datos de GitHub API, proyectos privados con demos, mapeo de iconos por lenguaje, puertas del easter egg Matrix, ajustes de animación y datos de contacto. El objeto se congela con `Object.freeze()` para evitar modificaciones accidentales.

```javascript
// assets/js/config.js, líneas 147-154
Object.freeze(CONFIG);
Object.freeze(CONFIG.github);
Object.freeze(CONFIG.languageIcons);
Object.freeze(CONFIG.animations);
Object.freeze(CONFIG.contact);
Object.freeze(CONFIG.meta);
export default CONFIG;
```

Los proyectos privados se definen aquí con nombre, descripción, lenguaje, URL de demo e icono Font Awesome, y se combinan con los repos públicos de la API de GitHub.

```javascript
// assets/js/config.js, líneas 38-46
privateProjects: [
    {
        name: 'Tedeer',
        description: 'Mi proyecto principal. Plataforma completa de gestion y servicios.',
        language: 'Python',
        homepage: 'http://tedeer.duckdns.org:8001/',
        icon: 'fa-solid fa-leaf'
    },
    // ... más proyectos privados
],
```

---

### 5. Integración con GitHub API — Carga dinámica de proyectos

El módulo `projects.js` implementa la clase `GitHubProjects` que consume la API pública de GitHub para mostrar repositorios. Combina repos públicos (filtrados: sin forks, sin el propio portfolio) con proyectos privados definidos en config. Cada tarjeta muestra nombre, descripción, lenguaje, estrellas, forks y enlaces a código/demo.

```javascript
// assets/js/modules/projects.js, líneas 95-114
async fetchGitHubRepos() {
    const url = `${CONFIG.github.apiBaseUrl}/users/${this.options.username}/repos` +
                `?sort=${this.options.sortBy}&per_page=${this.options.perPage}`;
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`GitHub API error: ${response.status}`);
    }
    const repos = await response.json();
    return repos.filter(repo => {
        if (this.options.excludeRepos.includes(repo.name)) return false;
        if (this.options.excludeForks && repo.fork) return false;
        return true;
    });
}
```

La función `escapeHtml()` del módulo utils se usa para sanitizar todos los datos antes de insertarlos en el DOM, previniendo ataques XSS.

```javascript
// assets/js/modules/utils.js, líneas 150-154
export function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
```

---

### 6. Fondo animado Synthwave con parallax

El módulo `background.js` genera dinámicamente estrellas titilantes usando `DocumentFragment` para rendimiento óptimo, y aplica parallax al sol y las montañas con `throttle` a ~60fps.

```javascript
// assets/js/modules/background.js, líneas 65-86
generateStars() {
    const fragment = document.createDocumentFragment();
    for (let i = 0; i < this.options.starsCount; i++) {
        const star = document.createElement('div');
        star.className = 'bg-star';
        star.style.left = `${randomRange(0, 100)}%`;
        star.style.top = `${randomRange(0, 100)}%`;
        star.style.animationDelay = `${randomRange(0, 2)}s`;
        const size = randomRange(1, 3);
        star.style.width = `${size}px`;
        star.style.height = `${size}px`;
        fragment.appendChild(star);
    }
    this.starsContainer.appendChild(fragment);
}
```

El CSS del fondo incluye un sol neón con líneas horizontales estilo VHS, un grid en perspectiva con animación infinita, montañas como siluetas triangulares con CSS puro y un overlay de scanlines CRT.

```css
/* assets/css/background.css, líneas 97-109 */
.bg-grid {
    background-image:
        linear-gradient(var(--color-grid) 2px, transparent 2px),
        linear-gradient(90deg, var(--color-grid) 2px, transparent 2px);
    background-size: 80px 40px;
    transform: rotateX(60deg);
    animation: grid-move 2s linear infinite;
}
```

---

### 7. Navegación con Smooth Scroll y Scroll Spy

El módulo `navigation.js` implementa smooth scrolling para las anclas del menú y un scroll spy que resalta la sección activa. Usa `throttle` del módulo utils para limitar las llamadas del evento scroll.

```javascript
// assets/js/modules/navigation.js, líneas 99-110
initScrollSpy() {
    const handleScroll = throttle(() => {
        this.updateActiveSection();
    }, 100);
    window.addEventListener('scroll', handleScroll, { passive: true });
    this.updateActiveSection();
}

updateActiveSection() {
    let currentSection = '';
    this.sections.forEach(section => {
        const sectionTop = section.offsetTop - this.options.headerOffset - 50;
        if (window.pageYOffset >= sectionTop) {
            currentSection = section.getAttribute('id');
        }
    });
    // Actualiza clase 'is-active' en los nav links
}
```

Se usa `history.pushState` para actualizar el hash de la URL sin provocar scroll, y `{ passive: true }` en el listener de scroll para mejorar rendimiento.

---

### 8. Easter Egg Matrix — Mini-juego con código Konami

El módulo más complejo (1003 líneas): un mini-juego temático de The Matrix que se activa introduciendo el código Konami (↑↑↓↓←→←→BA). Incluye una escena de sala blanca con personajes pixel art (Neo, Morpheus, Keymaker), sistema de diálogos tipo máquina de escribir y un pasillo de puertas que llevan a los proyectos.

```javascript
// assets/js/modules/matrix-easter-egg.js, líneas 35-44
this.konamiCode = [
    'ArrowUp', 'ArrowUp',
    'ArrowDown', 'ArrowDown',
    'ArrowLeft', 'ArrowRight',
    'ArrowLeft', 'ArrowRight',
    'b', 'a'
];
```

El canvas renderiza gráficos pixel art programados directamente con la API Canvas 2D, incluyendo animaciones de respiración para los personajes y efecto "lluvia Matrix" de caracteres verdes cayendo.

---

### 9. API PHP de contacto con validación y rate limiting

El backend `contact.php` es un endpoint REST que valida, sanitiza y envía emails. Incluye protección CORS con whitelist de orígenes, rate limiting por IP (5 peticiones/hora con hash MD5 para privacidad), y cabeceras de seguridad.

```php
// api/contact.php, líneas 82-87
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');
header('X-XSS-Protection: 1; mode=block');
header('Referrer-Policy: strict-origin-when-cross-origin');
```

La validación comprueba longitudes mínimas/máximas y formato de email, y la función `sanitizeString()` aplica `trim`, `stripslashes` y `htmlspecialchars` a todas las entradas.

```php
// api/contact.php, líneas 131-136
function sanitizeString(string $input): string {
    $input = trim($input);
    $input = stripslashes($input);
    $input = htmlspecialchars($input, ENT_QUOTES, 'UTF-8');
    return $input;
}
```

---

### 10. Utilidades reutilizables y diseño responsive

El módulo `utils.js` exporta funciones puras sin efectos secundarios: `debounce`, `throttle`, `randomRange`, `clamp`, `lerp`, `smoothScrollTo`, `isInViewport`, `escapeHtml`, `formatNumber`, `delay` y `createElement`. Todo documentado con JSDoc.

```javascript
// assets/js/modules/utils.js, líneas 47-55
export function throttle(func, limit) {
    let inThrottle;
    return function executedFunction(...args) {
        if (!inThrottle) {
            func(...args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}
```

El CSS incluye media query para `prefers-reduced-motion` que desactiva todas las animaciones, y responsive overrides en variables.css que reducen tamaños de fuente y espaciados en móvil.

```css
/* assets/css/base.css, líneas 82-91 */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
}
```

---

## Presentación del proyecto

Este portfolio es una **aplicación web de página única** que sirve como carta de presentación profesional con una estética visual muy marcada: el movimiento Synthwave de los años 80.

Al cargar la página, el usuario se encuentra con un **fondo animado inmersivo**: un cielo degradado del púrpura al rosa, un sol neón con líneas horizontales estilo VHS que pulsa suavemente, montañas triangulares como siluetas oscuras, un grid en perspectiva que avanza como una carretera infinita y 100 estrellas que titilan aleatoriamente. Todo esto se renderiza con CSS puro y JavaScript, sin dependencias de librerías externas de animación.

La navegación superior permite acceder a las cuatro secciones principales: **About** (presentación personal con avatar estilizado), **Skills** (tarjetas de habilidades en Frontend, Backend y Databases con iconos Font Awesome y efectos hover de elevación), **Projects** (grid dinámico que carga automáticamente los repositorios desde la API de GitHub y los combina con proyectos privados que tienen demo pública) y **Contact** (enlaces directos a GitHub, email y LinkedIn con botones neon interactivos).

El scroll spy resalta la sección activa en el menú, y el smooth scrolling proporciona una transición suave entre secciones. El diseño se adapta completamente a dispositivos móviles, tablets y pantallas grandes, ajustando fuentes, espaciados y layouts con media queries y variables CSS responsivas.

El detalle más especial es el **easter egg Matrix**: al introducir la secuencia Konami (↑↑↓↓←→←→BA), se despliega un mini-juego completo en Canvas con gráficos pixel art de Neo, Morpheus y el Keymaker. El jugador puede moverse por una sala blanca, interactuar con los personajes mediante diálogos y descubrir un pasillo de puertas que llevan a los distintos proyectos.

Técnicamente, la arquitectura es completamente **modular**: 6 archivos CSS con responsabilidades separadas importados en cascada, 5 módulos JavaScript con ES6 imports/exports nativos, una clase principal `PortfolioApp` que orquesta toda la inicialización, y un backend PHP independiente para el formulario de contacto.

---

## Conclusión

Este portfolio demuestra competencias en múltiples capas del desarrollo web moderno: **HTML5 semántico con accesibilidad ARIA**, un **sistema de diseño CSS organizado** con Custom Properties y arquitectura modular, **JavaScript ES6** con clases, módulos nativos, async/await y patrones de diseño (Singleton, Observer), **integración con APIs externas** (GitHub), un **backend PHP** con seguridad y validación profesional, y un dominio del **Canvas API** para renderizado gráfico.

El resultado es una web que no solo muestra proyectos, sino que es en sí misma una demostración técnica de todo lo aprendido: rendimiento optimizado con throttle/debounce, accesibilidad con ARIA y teclado, responsive design con media queries, seguridad con sanitización XSS y CORS, y creatividad con el easter egg interactivo de Matrix.

La estética Synthwave unifica todo el diseño y crea una experiencia memorable que diferencia este portfolio de soluciones genéricas, demostrando que el desarrollo web puede ser tanto técnicamente sólido como visualmente impactante.
