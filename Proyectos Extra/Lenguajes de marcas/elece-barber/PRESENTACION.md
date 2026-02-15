# ELECE Barber — Barbería Profesional en Albuixech

![ELECE Barber Logo](images/elece-logo.png)

## Introducción

ELECE Barber es una página web profesional diseñada para una barbería real ubicada en Albuixech, Valencia. El proyecto presenta la imagen de marca de la barbería, sus servicios y precios, reseñas reales de clientes desde Booksy y Google Maps, información de contacto con mapa interactivo y un sistema de reserva de citas online integrado con la plataforma Booksy.

La web está desarrollada íntegramente con HTML5, CSS3 y JavaScript vanilla, sin frameworks ni dependencias de servidor. Además, cuenta con soporte PWA (Progressive Web App) mediante Service Worker y manifest.json, y ofrece dos versiones optimizadas: una para navegador de escritorio y otra para dispositivos móviles con interacciones táctiles nativas.

---

## Desarrollo de las partes

### 1. Estructura HTML y SEO Avanzado

La estructura del sitio sigue los estándares de HTML5 semántico con etiquetas `<nav>`, `<main>`, `<section>`, `<footer>` y atributos ARIA para accesibilidad. El archivo principal incluye un completo conjunto de meta tags para SEO, Open Graph para redes sociales, Twitter Cards, geo-tags y datos estructurados Schema.org de tipo `HairSalon`.

```html
<!-- Archivo: index.html, líneas 46-97 -->
<!-- Ruta: /index.html -->
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "HairSalon",
    "name": "ELECE Barber",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "C/ Miguel Hernández, 23",
        "addressLocality": "Albuixech",
        "postalCode": "46110",
        "addressRegion": "Valencia"
    },
    "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "5.0",
        "reviewCount": "124"
    }
}
</script>
```

Se incluyen también etiquetas de precarga (`preload`) para recursos críticos y prefetch DNS para CDNs externos, optimizando el rendimiento de carga.

### 2. Sistema de Navegación y Menú Responsive

La navegación se implementa con un menú de escritorio horizontal que se transforma en un menú hamburguesa animado para móviles. El JavaScript controla la apertura/cierre con animación de las barras del icono (rotación 45° para formar una X) y cierra el menú automáticamente al pulsar un enlace.

```javascript
// Archivo: js/script.js, líneas 42-80
// Ruta: /js/script.js
function initMobileMenu() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');

    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
            
            const bars = hamburger.querySelectorAll('.bar');
            bars.forEach((bar, index) => {
                if (hamburger.classList.contains('active')) {
                    if (index === 0) bar.style.transform = 'rotate(45deg) translate(5px, 5px)';
                    if (index === 1) bar.style.opacity = '0';
                    if (index === 2) bar.style.transform = 'rotate(-45deg) translate(7px, -6px)';
                }
            });
        });
    }
}
```

El CSS maneja la transición con `position: fixed` y un deslizamiento desde la izquierda mediante `left: -100%` a `left: 0`.

### 3. Diseño Visual y Animaciones CSS

El diseño utiliza una paleta monocromática elegante basada en negro (`#000000`), gris (`#333333`) y blanco (`#ffffff`), con variables CSS definidas en `:root`. Se implementan múltiples animaciones con `@keyframes` (fadeInUp, fadeInDown, fadeInLeft, fadeInRight, scaleIn, float, pulse, shimmer) y clases de revelación scroll (.reveal, .reveal-left, .reveal-right, .reveal-scale) con transiciones cubic-bezier.

```css
/* Archivo: css/styles.css, líneas 207-216 */
/* Ruta: /css/styles.css */
:root {
    --primary-color: #000000;
    --secondary-color: #333333;
    --accent-color: #ffffff;
    --text-light: #ffffff;
    --text-dark: #000000;
    --bg-light: #f8f8f8;
    --bg-dark: #000000;
    --gradient: linear-gradient(135deg, #000000 0%, #333333 100%);
}
```

Se incluye soporte para `prefers-reduced-motion` que desactiva todas las animaciones cuando el usuario tiene configurada esa preferencia en su sistema operativo, mejorando la accesibilidad.

### 4. Carrusel de Reseñas con Autoplay

El carrusel de reseñas muestra opiniones reales de clientes de Booksy y Google Maps. Implementa scroll horizontal con controles prev/next, indicadores de página, auto-scroll cada 5 segundos (que se pausa al pasar el ratón), soporte táctil para móvil y recalculación dinámica al redimensionar la ventana.

```javascript
// Archivo: js/script.js, líneas 370-400
// Ruta: /js/script.js
function initReviewsCarousel() {
    const carousel = document.getElementById('reviews-carousel');
    const prevBtn = document.querySelector('.carousel-btn-prev');
    const nextBtn = document.querySelector('.carousel-btn-next');
    
    if (!carousel) return;
    
    const cards = carousel.querySelectorAll('.review-card');
    const cardWidth = 350 + 30; // ancho card + gap
    let currentIndex = 0;
    
    // Auto-scroll cada 5 segundos
    let autoScrollInterval = setInterval(autoScroll, 5000);
    
    // Pausar auto-scroll al pasar el ratón
    carousel.addEventListener('mouseenter', () => {
        clearInterval(autoScrollInterval);
    });
}
```

El HTML incluye 16 reseñas reales con nombre del cliente, servicio contratado, fecha y plataforma de origen (Booksy o Google Maps).

### 5. Versión Móvil Optimizada

El proyecto incluye una versión específica para móviles en `mobile-version/` con un diseño completamente diferente al de escritorio: header compacto fijo, drawer de navegación lateral con gesto de deslizar para cerrar, acciones rápidas (Reservar, Llamar, Instagram, Ubicación), sección de servicios tipo lista con precios, y un botón CTA fijo en la parte inferior.

```css
/* Archivo: mobile-version/css/mobile.css, líneas 30-39 */
/* Ruta: /mobile-version/css/mobile.css */
:root {
    --primary: #000000;
    --secondary: #333333;
    --accent: #ffffff;
    --text-light: #ffffff;
    --text-dark: #000000;
    --bg-light: #f8f8f8;
    --shadow: 0 2px 10px rgba(0,0,0,0.1);
    --shadow-lg: 0 4px 20px rgba(0,0,0,0.15);
    --vh: 1vh;
}
```

El JavaScript móvil incluye feedback háptico con `navigator.vibrate()`, observadores de intersección para animaciones al scroll, gestión del viewport height para iOS Safari y prevención de zoom por doble tap.

### 6. Progressive Web App (PWA)

La aplicación está configurada como PWA con un Service Worker que cachea los recursos estáticos (HTML, CSS, JS, imágenes) para funcionamiento offline, y un manifest.json que permite instalación en la pantalla de inicio del dispositivo.

```javascript
// Archivo: sw.js, líneas 1-21
// Ruta: /sw.js
const CACHE_NAME = 'elece-barber-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/css/styles.css',
  '/js/script.js',
  '/images/elece-logo.png',
  '/manifest.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});
```

El Service Worker implementa estrategia cache-first con fallback a red, y actualización del caché al activarse nuevas versiones.

### 7. Interactividad Avanzada en JavaScript

El script principal (825 líneas) implementa múltiples funcionalidades interactivas: efecto parallax en el hero con `scrollY`, barra de progreso de scroll, efecto de escritura (typewriter) en el título principal (respetando `prefers-reduced-motion`), resaltado automático del día actual en los horarios con indicador "(HOY)", botón back-to-top con aparición suave, lightbox para galería y efectos hover dinámicos en tarjetas de servicio.

```javascript
// Archivo: js/script.js, líneas 587-604
// Ruta: /js/script.js
function initBusinessHours() {
    const scheduleDays = document.querySelectorAll('.schedule-day');
    const today = new Date().getDay();
    
    const dayMapping = {
        1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 0: 6
    };
    
    if (scheduleDays.length > 0 && dayMapping.hasOwnProperty(today)) {
        const todayElement = scheduleDays[dayMapping[today]];
        if (todayElement) {
            todayElement.style.background = 'rgba(0, 0, 0, 0.1)';
            todayElement.style.border = '2px solid var(--primary-color)';
            const daySpan = todayElement.querySelector('.day');
            if (daySpan && !daySpan.textContent.includes('(HOY)')) {
                daySpan.innerHTML += ' <span style="color: var(--primary-color);">(HOY)</span>';
            }
        }
    }
}
```

### 8. Diseño Responsive Multi-Breakpoint

El CSS implementa un sistema responsive con breakpoints para pantallas grandes (>1600px), tablets (768px) y móviles (480px), además de estilos de impresión. Se utilizan CSS Grid con `auto-fit` y `minmax()` para layouts adaptativos que recolocan automáticamente las tarjetas de servicio, la galería y el contenido de contacto.

```css
/* Archivo: css/styles.css, líneas 1577-1615 */
/* Ruta: /css/styles.css */
@media (max-width: 768px) {
    .hamburger { display: flex; }
    .nav-menu {
        position: fixed;
        left: -100%;
        top: 100px;
        flex-direction: column;
        background: var(--primary-color);
        width: 100%;
    }
    .nav-menu.active { left: 0; }
    .hero { flex-direction: column; text-align: center; }
    .services-grid { grid-template-columns: 1fr; }
    .about-content { grid-template-columns: 1fr; }
    .contact-content { grid-template-columns: 1fr; }
}
```

---

## Presentación del proyecto

ELECE Barber es la web de una barbería real en Albuixech (Valencia), creada para dar visibilidad online al negocio y facilitar la reserva de citas a los clientes. La web está pensada para funcionar como carta de presentación digital del negocio.

Al entrar en la página, el usuario se encuentra con un hero a pantalla completa con el nombre de la barbería y dos botones de acción: reservar cita online (enlace directo a Booksy) y ver los servicios. La sección de servicios muestra las cuatro opciones principales con sus precios: corte caballero (13€), recorte de barba (6€), corte y lavado (15€) y corte y barba (16€).

La galería enlaza directamente con el Instagram de la barbería (@elecebarber_) donde se pueden ver los trabajos realizados. La sección "Sobre Nosotros" presenta estadísticas del negocio: más de 500 clientes satisfechos, más de 5 años de experiencia y 100% de profesionalidad.

Uno de los puntos fuertes del sitio es el carrusel de reseñas con 16 opiniones reales de clientes tanto de Booksy como de Google Maps, todas con valoración de 5 estrellas. El nombre del barbero, Néstor, aparece mencionado en varias de ellas, aportando credibilidad y confianza.

La sección de contacto incluye la ubicación con mapa de Google Maps integrado, horarios detallados con resaltado automático del día actual y enlace directo a Booksy para reservar. El footer ofrece enlaces rápidos a todas las secciones y redes sociales.

La versión móvil está diseñada específicamente para la experiencia táctil: menú drawer lateral, acciones rápidas de un toque (llamar, reservar, Instagram, ubicación), botón flotante fijo para reservar y gestos de deslizar. Además, la web funciona como PWA, pudiendo instalarse en la pantalla de inicio del teléfono.

---

## Conclusión

ELECE Barber demuestra cómo se puede crear una web profesional completa para un negocio real utilizando únicamente tecnologías front-end estándar: HTML5, CSS3 y JavaScript. El proyecto integra múltiples aspectos clave del desarrollo web moderno: SEO con Schema.org y Open Graph, accesibilidad con ARIA y `prefers-reduced-motion`, rendimiento con precarga de recursos y Service Worker, diseño responsive con CSS Grid y media queries, y experiencia de usuario optimizada con dos versiones diferenciadas para escritorio y móvil.

La integración con plataformas externas como Booksy para reservas e Instagram para contenido visual, junto con las reseñas reales de Google Maps, convierten este proyecto en una solución funcional y completa para la presencia online de una barbería real. El resultado es una web que no solo presenta bien el negocio, sino que facilita activamente la captación de clientes a través de múltiples canales digitales.
