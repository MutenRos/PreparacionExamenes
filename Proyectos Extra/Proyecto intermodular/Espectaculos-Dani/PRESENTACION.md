# 🎪 Espectáculos Dani — Sitio Web Oficial

![Espectáculos Dani Logo](https://espectaculosdani.es/wp-content/uploads/2019/08/Especaculos-Dani.png)

## Introducción

Espectáculos Dani es una empresa de entretenimiento y alquiler de atracciones con sede en Valencia, activa desde 1998. Este proyecto consiste en el desarrollo de su sitio web completo: una landing page pública con catálogo de servicios, galería, formulario de contacto y un dashboard de administración para gestionar eventos, clientes, inventario y facturación.

El stack tecnológico es **HTML5 semántico + CSS3 con Custom Properties + JavaScript ES6+ modular + PHP 7.4+** para la API de contacto. No se usa ningún framework: todo es código nativo, lo que lo convierte en un ejercicio ideal para demostrar dominio de las bases del desarrollo web full-stack.

---

## Desarrollo de las partes

### 1. Estructura HTML5 semántica y SEO

La página principal (`index.html`, 645 líneas) utiliza HTML5 semántico con etiquetas `<header>`, `<main>`, `<section>`, `<article>`, `<nav>`, `<aside>` y `<footer>`. Todas las secciones llevan `aria-labelledby` vinculado a sus encabezados, y los elementos interactivos tienen `role` y `aria-label` para accesibilidad.

```html
<!-- index.html, líneas 83-107 — Navegación principal con roles ARIA -->
<header id="header" role="banner">
    <nav class="navbar" role="navigation" aria-label="Navegación principal">
        <div class="nav-container">
            <a href="index.html" class="logo" aria-label="Espectáculos Dani - Ir al inicio">
                <img src="..." alt="Logo Espectáculos Dani" class="logo-img" width="400" height="auto">
            </a>
            <button class="nav-toggle" id="nav-toggle"
                aria-label="Abrir menú de navegación"
                aria-expanded="false" aria-controls="nav-menu" type="button">
                <span></span><span></span><span></span>
            </button>
            <ul class="nav-menu" id="nav-menu" role="menubar">
                <li role="none"><a href="#inicio" class="nav-link active" role="menuitem">Inicio</a></li>
                <!-- ... -->
            </ul>
        </div>
    </nav>
</header>
```

El `<head>` incluye meta tags de SEO, Open Graph y Twitter Cards para compartir en redes sociales, además de preconnect a fuentes externas para optimizar la carga.

---

### 2. Sistema de diseño CSS con Custom Properties

El archivo `css/styles.css` (1944 líneas) implementa un sistema de diseño completo basado en variables CSS. Define una paleta de colores de marca, sombras con múltiples capas, transiciones con curvas de Bézier profesionales, tipografía, espaciado y escala z-index.

```css
/* css/styles.css, líneas 37-73 — Variables de diseño principales */
:root {
    --primary: #ff6b35;
    --primary-dark: #e55a2b;
    --primary-light: #ff8c5a;
    --primary-glow: rgba(255, 107, 53, 0.4);
    --secondary: #1a1a2e;
    --accent: #ffd93d;
    --success: #4ecdc4;
    --danger: #ff6b6b;
    --font-primary: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    --shadow-lg: 0 12px 24px rgba(0, 0, 0, 0.1), 0 6px 12px rgba(0, 0, 0, 0.06);
    --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
    --transition: 300ms var(--ease-out-expo);
}
```

Incluye soporte para `prefers-reduced-motion` para accesibilidad, `scroll-margin-top` para compensar el header fijo y `glassmorphism` con backdrop-filter.

---

### 3. JavaScript modular (Module Pattern) — app.js

El archivo `js/app.js` (1240 líneas) implementa una arquitectura modular con el patrón IIFE (Immediately Invoked Function Expression). Encapsula toda la lógica en módulos independientes: `CONFIG`, `Utils`, `DOM`, `Navigation`, `Gallery`, `Forms` y `App`.

```javascript
/* js/app.js, líneas 86-120 — Módulo de utilidades con throttle, debounce y escapeHtml */
const Utils = {
    throttle(callback, delay) {
        let lastCall = 0;
        return function(...args) {
            const now = Date.now();
            if (now - lastCall >= delay) {
                lastCall = now;
                callback.apply(this, args);
            }
        };
    },
    debounce(callback, delay) {
        let timeoutId;
        return function(...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => callback.apply(this, args), delay);
        };
    },
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
};
```

El módulo `Forms` gestiona la validación en tiempo real, el envío asíncrono al servidor PHP y un fallback a localStorage si la API no está disponible. También incluye un contador de caracteres con aviso visual al acercarse al límite.

---

### 4. Galería con filtros y lightbox

La sección de galería permite filtrar imágenes por categoría (hinchables, disco, eventos) y abrirlas en un lightbox modal. Los filtros usan `data-filter` en los botones y `data-category` en las imágenes.

```html
<!-- index.html, líneas 408-414 — Filtros de galería con roles ARIA -->
<nav class="gallery-filters" role="tablist" aria-label="Filtrar galería">
    <button class="filter-btn active" data-filter="all" role="tab" aria-selected="true">Todos</button>
    <button class="filter-btn" data-filter="hinchables" role="tab" aria-selected="false">Hinchables</button>
    <button class="filter-btn" data-filter="disco" role="tab" aria-selected="false">Disco Móvil</button>
    <button class="filter-btn" data-filter="eventos" role="tab" aria-selected="false">Eventos</button>
</nav>
```

```javascript
/* js/app.js, líneas 555-575 — Filtrado de galería con animación */
filterGallery(category) {
    const { galleryItems } = DOM.elements;
    galleryItems.forEach(item => {
        const itemCategory = item.dataset.category;
        const shouldShow = category === 'all' || itemCategory === category;
        item.style.display = shouldShow ? '' : 'none';
    });
}
```

---

### 5. API de contacto en PHP con validación robusta

El archivo `api/contact.php` (592 líneas) es un endpoint REST que procesa el formulario de contacto. Incluye validación estricta, sanitización con `strip_tags` y `htmlspecialchars`, rate limiting por IP, honeypot anti-spam, logging y backup en JSON.

```php
/* api/contact.php, líneas 163-173 — Sanitización de entrada */
function sanitizeString($input): string {
    if (!is_string($input)) return '';
    $clean = strip_tags($input);
    $clean = preg_replace('/[\x00-\x1F\x7F]/u', '', $clean);
    $clean = preg_replace('/\s+/', ' ', $clean);
    return trim($clean);
}
```

```php
/* api/contact.php, líneas 236-256 — Rate limiting por IP con ventana temporal */
function checkRateLimit(string $ip): bool {
    $limits = json_decode(file_get_contents($rateFile), true) ?? [];
    $ipHash = md5($ip);
    if (isset($limits[$ipHash]) && $limits[$ipHash]['count'] >= $maxRequests) {
        return false;
    }
    // ...
}
```

Los headers de seguridad incluyen `X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection` y `Referrer-Policy`.

---

### 6. Dashboard de administración

El dashboard (`dashboard.html`, 813 líneas + `js/dashboard.js`, 1031 líneas) es un panel completo con sidebar lateral, navegación por secciones, estadísticas en cards, calendario interactivo, gestión CRUD de eventos/clientes/facturas y control de inventario (hinchables, atracciones, mobiliario, equipos de sonido).

```javascript
/* js/dashboard.js, líneas 91-114 — Navegación entre secciones del dashboard */
function switchSection(section) {
    currentSection = section;
    document.querySelectorAll('.sidebar-menu a').forEach(link => {
        link.classList.remove('active');
        if (link.dataset.section === section) link.classList.add('active');
    });
    document.querySelectorAll('.dashboard-section').forEach(sec => {
        sec.classList.remove('active');
    });
    const targetSection = document.getElementById(`section-${section}`);
    if (targetSection) targetSection.classList.add('active');
}
```

Toda la persistencia se gestiona con `localStorage` usando claves prefijadas (`ed_events`, `ed_clients`, etc.), lo que permite funcionar sin backend.

---

### 7. Páginas de servicios con catálogo de productos

Cada servicio tiene su propia página en `servicios/` (hinchables, atracciones, disco-móvil, etc.) con un hero de fondo completo, grid de productos con precios y botón de reserva, y sección de características.

```html
<!-- servicios/hinchables.html, líneas 80-96 — Tarjeta de producto con precio -->
<article class="catalog-item">
    <div class="catalog-image">
        <img src="https://espectaculosdani.es/.../PATRULLA-CANINA_1.jpg"
             alt="Hinchable Patrulla Canina" loading="lazy">
    </div>
    <div class="catalog-content">
        <h3>Patrulla Canina</h3>
        <p>Hinchable temático de la Patrulla Canina. ¡El favorito de los más peques!</p>
        <div class="catalog-meta">
            <span class="catalog-price">Desde 80€<span>/día</span></span>
            <a href="../index.html#contacto" class="catalog-btn" aria-label="Reservar Patrulla Canina">Reservar</a>
        </div>
    </div>
</article>
```

Los estilos del catálogo (`css/services.css`, 502 líneas) incluyen hover con `translateY` y `scale`, parallax en el hero, y responsive adaptado a móvil.

---

### 8. Formulario de contacto con validación frontend + backend

El formulario combina validación en JavaScript (blur/input en tiempo real) con validación en PHP. Incluye campos de nombre, email, teléfono, servicio (dropdown), fecha del evento, mensaje con contador de caracteres y checkbox de llamada. Un input honeypot oculto detecta bots de spam.

```html
<!-- index.html, líneas 534-572 — Formulario completo con honeypot antispam -->
<form class="contact-form" id="contact-form" action="api/contact.php" method="POST" novalidate>
    <div class="form-group">
        <input type="text" id="nombre" name="nombre" required placeholder=" " autocomplete="name">
        <label for="nombre">Nombre completo *</label>
    </div>
    <!-- ... más campos ... -->
    <!-- Honeypot anti-spam -->
    <div style="display:none;" aria-hidden="true">
        <input type="text" name="website" tabindex="-1" autocomplete="off">
    </div>
    <button type="submit" class="btn btn-primary btn-full">
        <i class="fas fa-paper-plane"></i> Enviar mensaje
    </button>
</form>
```

---

### 9. Animaciones y micro-interacciones

El proyecto usa animaciones CSS y contadores numéricos animados con JavaScript. El hero muestra contadores que cuentan desde 0 hasta el valor final (35 eventos, 27 años). Los botones de servicio tienen efecto `hover` con `translateY`, los cards del dashboard escalan al pasar el ratón, y el preloader usa una animación de carga con pulso.

```css
/* css/styles.css, líneas 139-148 — Accesibilidad: reducir animaciones */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
```

Se respeta `prefers-reduced-motion` para usuarios que prefieren movimiento reducido.

---

### 10. Responsive Design Mobile-First

Todo el sitio es responsive. La navegación se convierte en un menú hamburguesa para móvil, el grid de servicios pasa de 3 columnas a 1, el dashboard oculta la sidebar y la muestra como overlay, y los formularios se adaptan a pantallas pequeñas.

```css
/* css/services.css, líneas 115-120 — Grid adaptable */
.catalog-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}
@media (max-width: 640px) {
    .catalog-grid { grid-template-columns: 1fr; }
}
```

---

## Presentación del proyecto

Espectáculos Dani es un sitio web profesional completo que cubre todas las necesidades de una empresa de entretenimiento. Al acceder a la página principal, el usuario recibe un héroe visual con estadísticas animadas que generan confianza inmediata: 35 eventos simultáneos, 27 años de experiencia, desde 1998.

La navegación es fluida y accesible: el menú se pliega en móvil, los enlaces ancla desplazan suavemente a cada sección, y un botón flotante de WhatsApp permite contactar al instante. La sección de servicios detalla los 8 servicios principales con links a sus catálogos individuales, donde el usuario puede ver fotos, precios y reservar directamente.

La galería con filtros permite explorar visualmente el trabajo de la empresa, y el formulario de contacto valida los datos en tiempo real, cuenta los caracteres del mensaje y envía la información al servidor PHP, que además la respalda en JSON.

El dashboard de administración proporciona un panel completo para gestionar el negocio: calendario de eventos, base de datos de clientes, sistema de facturas e inventario categorizado (hinchables, atracciones, mobiliario, equipos de sonido), todo persistido en localStorage para funcionar sin servidor.

---

## Conclusión

Este proyecto demuestra el desarrollo de un sitio web completo sin dependencias de frameworks, utilizando exclusivamente las tecnologías base del desarrollo web. Se han trabajado **HTML5 semántico** con accesibilidad WCAG, **CSS3** con Custom Properties y diseño responsive, **JavaScript ES6+** con patrones de diseño modulares, y **PHP** con buenas prácticas de seguridad y validación.

Los puntos más destacados del proyecto son la arquitectura modular del JavaScript (Module Pattern con IIFE), el sistema de diseño basado en variables CSS reutilizables, la API REST en PHP con rate limiting y sanitización, y la integración frontend-backend en el formulario de contacto. Todo ello forma un producto final pulido, funcional y listo para producción.
