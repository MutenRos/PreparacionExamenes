# Bombas Ideal — Rediseño Web Completo

![Bombas Ideal Hero](assets/images/hero-fabrica.jpg)

> 🔗 **GitHub Pages:** [https://mutenros.github.io/BI/](https://mutenros.github.io/BI/)

## Introducción

Este proyecto es una propuesta de rediseño completo de la página web corporativa de **Bombas Ideal S.A.U.**, empresa fabricante de bombas de agua fundada en 1902 con presencia en más de 72 países. Se ha construido un sitio moderno, responsive y accesible utilizando únicamente HTML5, CSS3 y JavaScript ES6+ (vanilla, sin frameworks). La web incluye una página principal con hero slider, catálogo de más de 35 series de productos, herramienta innovadora de selección de bombas (BIPS), sistema de noticias, formulario de contacto con validación, y centro de descargas con PDFs reales de catálogos y manuales. La arquitectura ha sido refactorizada a un sistema modular profesional tanto en CSS (design tokens + componentes) como en JavaScript (ES6 modules con patrón init/state).

---

## Desarrollo de las partes

### 1. Estructura HTML y página principal (`index.html`)

La página principal es un documento HTML5 semántico de más de 1300 líneas que contiene todas las secciones corporativas: hero con slider, quick features, sobre la empresa con timeline histórica, catálogo de productos con filtrado por categoría, sección de aplicaciones, centro de descargas PDF, noticias, formulario de contacto y footer multinivel.

```
Archivo: index.html — líneas 1-16
Se define el DOCTYPE, la etiqueta <html lang="es"> para accesibilidad, viewport responsive
y metadatos SEO (description y favicon SVG). Se enlazan los estilos legacy (styles.css),
Google Fonts (Montserrat + Roboto) y Font Awesome 6.4.0 como iconografía.
```

```
Archivo: index.html — líneas 19-29
Preloader con animación CSS de gota de agua. Se muestra mientras los recursos se cargan
y se oculta tras 1.5 segundos vía JavaScript.
```

```
Archivo: index.html — líneas 113-233
Sección Hero completa: slider con 3 slides (bombeo, innovación, calidad), cada uno con badge,
título, subtítulo y botones CTA. Incluye estadísticas animadas (120+ años, 72 países,
38+ series, 4 generaciones) y un indicador de scroll.
```

### 2. Sistema de variables CSS y design tokens (`src/css/variables.css`)

Se ha creado un sistema centralizado de diseño con más de 100 custom properties CSS organizadas en 9 categorías: colores de marca (azul primario #0066cc con escala de 50-900), color secundario (cian/turquesa), colores semánticos (success, warning, error, info), tipografía (Montserrat para títulos, Roboto para cuerpo), espaciado (escala de 4px a 96px), sombras (4 niveles), transiciones, bordes y z-index.

```
Archivo: src/css/variables.css — líneas 30-55
:root con paleta de azules corporativos: desde --bi-primary-50 (#e6f0fa) hasta
--bi-primary-900 (#001429), más gradientes corporativos para hero y fondos oscuros.
```

```
Archivo: src/css/variables.css — líneas 57-70
Color secundario cian/turquesa (#00a8e8) con escala completa, representando el agua,
y acento cian brillante (#00d4ff) para highlights y focus.
```

### 3. Módulo de navegación responsive (`src/js/modules/navigation.js`)

El módulo de navegación es un componente JavaScript ES6 de 345 líneas que gestiona: navbar sticky con cambio de estilo al hacer scroll (pasado un umbral de 100px), menú hamburguesa para móvil con apertura animada, dropdowns con mega-menú de productos, smooth scroll para enlaces ancla, y ocultación del top bar al bajar. Usa un patrón state/elements/init con funciones privadas puras.

```
Archivo: src/js/modules/navigation.js — líneas 26-48
Estado interno (state) con isMenuOpen, lastScrollY e isScrollingDown, y objeto elements
que cachea referencias DOM al navbar, hamburger, navMenu, navLinks y dropdowns.
```

```
Archivo: src/js/modules/navigation.js — líneas 74-99
Función handleScroll(): lee scrollY, determina dirección del scroll, añade clase 'scrolled'
al navbar si supera el umbral configurable, y oculta el topBar si hideTopBarOnScroll está activo.
```

### 4. BIPS — Selector Inteligente de Bombas (`src/js/bips/`)

BIPS (Bombas Ideal Pump Selector) es la herramienta estrella del proyecto: un selector interactivo que permite al usuario introducir parámetros hidráulicos (caudal, altura, sector, instalación, material, fase eléctrica) y obtiene las series de bombas compatibles ordenadas por puntuación de relevancia. Consta de tres módulos: data.js (base de datos de 30+ series reales con specs técnicas), filter.js (motor de filtrado con sistema de pesos) y ui.js (interfaz con renderizado dinámico).

```
Archivo: src/js/bips/data.js — líneas 93-130
Array SERIES_DATABASE con objetos de series (ej: NXA con caudal 0.3-20 m³/h, altura 10-100m,
potencia 0.37-7.5kW, material inox AISI 304, eficiencia 65%, sectores y catálogo PDF asociado).
```

```
Archivo: src/js/bips/filter.js — líneas 21-39
Configuración del filtro: margen de tolerancia 15%, pesos (flow 30, head 30, sector 25,
efficiency 10, material 5), score mínimo de 40 para considerarse match.
```

```
Archivo: src/js/bips/filter.js — líneas 73-90
Función isInRange(): verifica si un valor está dentro del rango de la serie con tolerancia
configurable. calculateRangeMatch() calcula el porcentaje de coincidencia respecto al punto
óptimo (centro del rango) con penalización máxima del 30%.
```

### 5. Hero Slider con autoplay (`src/js/modules/slider.js` y `script.js`)

El slider del hero implementa un carrusel con 3 slides que rota automáticamente cada 6 segundos. Tiene doble implementación: la versión legacy en script.js (funcional, con dots e intervalo) y la versión modular en slider.js (con soporte de swipe táctil, pause on hover, y respeto a prefers-reduced-motion).

```
Archivo: script.js — líneas 380-420
Versión legacy: función showSlide(index) que alterna clases 'active' en los slides y dots,
nextSlide() que avanza circularmente, startSlider()/stopSlider() con setInterval de 6000ms.
Event listeners en cada dot para cambiar slide manualmente.
```

```
Archivo: src/js/modules/slider.js — líneas 23-50
Versión modular: estado con currentIndex, slidesCount, isPlaying, intervalId, y coordenadas
táctiles (touchStartX/touchEndX) para detectar swipe en dispositivos móviles.
```

### 6. Animaciones por Intersection Observer (`src/js/modules/animations.js`)

El módulo de animaciones (397 líneas) utiliza la API Intersection Observer para detectar cuándo los elementos entran en el viewport y aplicarles clases de animación CSS. Soporta 12 tipos de animación (fadeIn, fadeUp, fadeDown, slideUp, scaleIn, bounce, flip…) configurables vía data-attributes en el HTML. Respeta la preferencia del usuario `prefers-reduced-motion`.

```
Archivo: src/js/modules/animations.js — líneas 39-56
Diccionario ANIMATIONS que mapea nombres de animación a clases CSS: fadeIn→'animate-fade-in',
fadeUp→'animate-fade-up', scaleIn→'animate-scale-in', etc. Se usan con data-animate="fadeUp".
```

```
Archivo: script.js — líneas 243-272
Versión legacy: IntersectionObserver con threshold 0.1, observa cards de producto, servicio,
contacto, etc. Les pone opacity:0 y transform:translateY(30px) iniciales, y al intersectar
añade la clase .animate-in que los muestra con transición de 0.6s.
```

### 7. Formulario de contacto con validación (`index.html` + `script.js`)

El formulario de contacto incluye campos de nombre, empresa, email, teléfono (con patrón de validación), asunto (select con 7 opciones) y mensaje (con maxlength de 1000 caracteres). La validación incluye tanto atributos HTML5 (required, pattern, type="email") como validación JavaScript adicional con expresión regular de email antes del envío simulado.

```
Archivo: index.html — líneas 1271-1296
Formulario con form-row (dos columnas responsive), input floating labels, select de asunto,
textarea con límite 1000 chars, checkbox de privacidad con enlace a la política, y botón
de envío con icono paper-plane.
```

```
Archivo: script.js — líneas 178-207
En el submit: se previene el envío real (preventDefault), se valida el email con regex
/^[^\s@]+@[^\s@]+\.[^\s@]+$/, se cambia el texto del botón a "Enviando..." con spinner,
y tras 1.5s se muestra "¡Mensaje Enviado!" con fondo verde de éxito.
```

### 8. Páginas de producto (`productos/serie-*.html`)

El proyecto incluye 35+ páginas de producto individuales, una por cada serie de bombas. Cada página sigue un template consistente: navbar con enlace activo en Productos, breadcrumb de navegación, hero con imagen de la bomba, especificaciones técnicas en tabla, descripción comercial y enlace al catálogo PDF.

```
Archivo: productos/serie-nxa.html — líneas 35-55
Hero del producto con imagen, breadcrumb (Inicio > Productos > Bombas Multicelulares),
tag de serie, título "Bombas Multicelulares Compactas", y descripción técnica indicando
que es de acero inoxidable con conexiones roscadas para uso doméstico e industrial.
```

```
Archivo: productos/producto.css
Estilos específicos para las páginas de producto: layout de hero en dos columnas,
tabla de especificaciones con zebra striping, y responsive para móvil con imagen a ancho completo.
```

### 9. Configuración centralizada y easter eggs (`src/js/config.js`)

El archivo de configuración (135 líneas) centraliza todos los parámetros ajustables del sitio en un único objeto CONFIG exportado como módulo ES6. Incluye datos de empresa, URLs, configuración del slider (autoplay, intervalo, duración de transición), navegación (umbral de scroll, breakpoint móvil), animaciones (habilitadas, umbral del observer) y hasta el código Konami como easter egg.

```
Archivo: src/js/config.js — líneas 18-34
Objeto company con datos reales: nombre, año de fundación (1902), teléfono, email,
dirección del polígono industrial, y datos de empresa en Barberà del Vallès.
```

```
Archivo: src/js/config.js — líneas 83-95
Código Konami: secuencia [ArrowUp x2, ArrowDown x2, ArrowLeft, ArrowRight, ArrowLeft,
ArrowRight, b, a] que al completarse redirige al usuario a un Matrix hallway en
mutenros.github.io como easter egg oculto.
```

### 10. CSS modular con componentes (`src/css/main.css` + `src/css/components/`)

La arquitectura CSS sigue un patrón de importación ordenado: primero variables/tokens de diseño, luego reset base, utilidades, y finalmente 9 componentes independientes (buttons, navbar, hero, cards, forms, sections, modals, footer, bips). Cada componente es autónomo y reutilizable. El archivo main.css (161 líneas) actúa como punto de entrada que importa todo en el orden correcto, incluyendo estilos de impresión al final.

```
Archivo: src/css/main.css — líneas 22-44
Imports de foundation: variables.css (tokens), base.css (reset), utilities.css (helpers).
Orden crítico: las variables deben cargarse primero para que los componentes las usen.
```

```
Archivo: src/css/main.css — líneas 129-161
@media print: oculta topbar, navbar, footer, scroll-top y modales. Establece fondo blanco,
texto negro y font-size 12pt para impresión limpia del contenido.
```

---

## Presentación del proyecto

Bombas Ideal es una propuesta de rediseño web completo para una empresa industrial real con más de 120 años de historia. El sitio se ha construido desde cero con tecnologías web estándar — HTML5 semántico, CSS3 con Custom Properties y JavaScript ES6 modular — sin depender de ningún framework.

La página principal recibe al usuario con un hero slider animado que destaca los tres pilares de la empresa: soluciones de bombeo, innovación tecnológica y calidad certificada. Un contador animado muestra las cifras clave al entrar en el viewport. La navegación es sticky y se adapta a móvil con menú hamburguesa y mega-menú desplegable para los productos.

El catálogo completo organiza más de 35 series de bombas en categorías (horizontales, verticales, sumergidas, multicelulares, residuales, contra incendios, grupos hydro, solar). Cada serie tiene su página individual con especificaciones técnicas, imagen y enlace directo al catálogo PDF.

La herramienta BIPS (Bombas Ideal Pump Selector) es la funcionalidad más avanzada: un selector interactivo donde el usuario introduce sus parámetros hidráulicos y el sistema devuelve las series compatibles ordenadas por puntuación, conjugando caudal, altura, sector, eficiencia e instalación con un motor de filtrado configurable.

El sitio incluye sistema de noticias, formulario de contacto con validación frontend y backend simulado, banner de cookies con localStorage, centro de descargas con 16 documentos PDF reales, y detalles de cuidado como preloader animado, efecto parallax en el hero, animaciones de entrada con Intersection Observer, y un código Konami oculto como easter egg.

La refactorización v4.1.0 migró todo el código a una arquitectura profesional: CSS con design tokens (100+ variables), módulos JavaScript ES6 con imports/exports, y convención JSDoc para documentación. Todo responsive y con accesibilidad mejorada (skip link, aria labels, focus-visible, prefers-reduced-motion).

---

## Conclusión

Este proyecto demuestra que es posible construir un sitio web corporativo completo, profesional y moderno utilizando exclusivamente tecnologías estándar del navegador. No se ha necesitado React, Vue ni ningún framework — solo HTML5, CSS3 y JavaScript vanilla bien estructurados.

Los puntos fuertes del proyecto son:
- **Arquitectura modular real**: CSS con design tokens y componentes separados, JS con ES6 modules y patrón estado/init
- **BIPS**: herramienta de selección técnica con motor de filtrado ponderado sobre datos reales
- **Contenido real**: 16 PDFs de catálogos y manuales oficiales, imágenes de productos, datos técnicos extraídos de documentación real de Bombas Ideal
- **Accesibilidad**: skip link, aria-labels, focus-visible, prefers-reduced-motion, lazy loading
- **UX cuidada**: preloader, slider con swipe táctil, counters animados, parallax, validación progresiva del formulario, y un easter egg Konami

El resultado es un sitio que podría desplegarse en producción para una empresa industrial real, con más de 40 páginas HTML, un sistema CSS de 316+ variables y un ecosistema JavaScript modular de 2000+ líneas documentadas con JSDoc.
