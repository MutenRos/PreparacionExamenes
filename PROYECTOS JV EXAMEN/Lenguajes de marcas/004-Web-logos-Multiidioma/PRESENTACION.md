# LogoGallery — Galería de Logos Famosos Multiidioma

![LogoGallery](https://mutenros.github.io/Lenguajes-de-marcas-004-Web-logos-Multiidioma/)

## Introducción

LogoGallery es una web de galería de logos famosos con soporte multiidioma (español, inglés y francés). El proyecto demuestra el uso combinado de HTML5 semántico, CSS3 con diseño responsive y JavaScript vanilla para implementar un sistema de internacionalización (i18n) basado en atributos data. La web presenta 6 logos ficticios de diferentes sectores (tecnología, deportes, alimentación, comercio, música y automoción), con tarjetas interactivas, una sección informativa y un formulario de contacto con validación.

## Desarrollo de las partes

### 1. Estructura HTML5 semántica — index.html

La página principal utiliza etiquetas semánticas de HTML5 (`<header>`, `<main>`, `<section>`, `<article>`, `<footer>`, `<nav>`) para estructurar el contenido en secciones claras: cabecera con navegación, hero, galería de logos, información, contacto y pie de página. Cada sección lleva un `id` que permite la navegación por anclas.

```html
<!-- index.html — Líneas 14-31: Cabecera con navegación y selector de idioma -->
<header>
    <h1>Logo<span>Gallery</span></h1>
    <nav aria-label="Navegación principal">
        <a href="#galeria" data-es="Galería" data-en="Gallery" data-fr="Galerie">Galería</a>
        ...
    </nav>
    <div class="selector-idioma">
        <button data-lang="es" class="activo">ES</button>
        <button data-lang="en">EN</button>
        <button data-lang="fr">FR</button>
    </div>
</header>
```

**Archivo:** `index.html` · Líneas 14–31 · Ruta: `/index.html`

### 2. Sistema multiidioma con atributos data — index.html

Todos los textos visibles llevan atributos `data-es`, `data-en` y `data-fr` con la traducción correspondiente. El JavaScript lee estos atributos y actualiza el contenido del DOM dinámicamente. Este enfoque permite añadir idiomas sin modificar la lógica del script.

```html
<!-- index.html — Líneas 35-41: Hero con textos en tres idiomas -->
<h2 data-es="Descubre los logos más icónicos del mundo"
    data-en="Discover the world's most iconic logos"
    data-fr="Découvrez les logos les plus iconiques du monde">
    Descubre los logos más icónicos del mundo
</h2>
```

**Archivo:** `index.html` · Líneas 35–41 · Ruta: `/index.html`

### 3. Tarjetas de logos con datos informativos — index.html

La galería contiene 6 tarjetas (`<article class="tarjeta-logo">`) que muestran: imagen SVG del logo, nombre de la marca, categoría, año de fundación y descripción. Toda la información textual es multiidioma. Las tarjetas usan la estructura semántica `<article>` porque cada una es un contenido independiente.

```html
<!-- index.html — Líneas 50-63: Ejemplo de tarjeta de logo -->
<article class="tarjeta-logo">
    <img src="img/logo-tech.svg" alt="Logo TechCorp">
    <h4>TechCorp</h4>
    <p class="categoria" data-es="Tecnología" data-en="Technology" data-fr="Technologie">Tecnología</p>
    <p class="anio" data-es="Fundada en 1976" data-en="Founded in 1976" data-fr="Fondée en 1976">Fundada en 1976</p>
    <p class="descripcion" data-es="Logo minimalista con forma circular...">...</p>
</article>
```

**Archivo:** `index.html` · Líneas 50–63 · Ruta: `/index.html`

### 4. Formulario de contacto multiidioma — index.html

El formulario incluye campos de nombre, email y mensaje, todos con labels y placeholders traducidos a los tres idiomas mediante atributos data. El botón de envío también cambia de idioma dinámicamente.

```html
<!-- index.html — Líneas 151-172: Formulario de contacto -->
<form>
    <label for="nombre" data-es="Nombre" data-en="Name" data-fr="Nom">Nombre</label>
    <input type="text" id="nombre" placeholder="Tu nombre"
           data-es="Tu nombre" data-en="Your name" data-fr="Votre nom">
    ...
    <input type="submit" data-es="Enviar mensaje" data-en="Send message"
           data-fr="Envoyer le message" value="Enviar mensaje">
</form>
```

**Archivo:** `index.html` · Líneas 151–172 · Ruta: `/index.html`

### 5. Hoja de estilos CSS3 — css/estilos.css

El CSS utiliza un diseño moderno con paleta oscura (`#1a1a2e` cabecera/footer) y acento rojo (`#e94560`). Se emplean Flexbox para layouts, transiciones CSS para hover effects, gradiente en el hero, shadow en la cabecera sticky, y border-radius para tarjetas redondeadas. El reset universal incluye `box-sizing: border-box`.

```css
/* css/estilos.css — Líneas 7-11: Reset universal */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
```

**Archivo:** `css/estilos.css` · Líneas 7–11 · Ruta: `/css/estilos.css`

### 6. Diseño de tarjetas con hover interactivo — css/estilos.css

Las tarjetas de la galería usan Flexbox con `flex-wrap` para ser responsive. Cada tarjeta tiene transiciones de `transform` y `box-shadow` que se activan al pasar el ratón, elevando la tarjeta y creando un efecto de profundidad.

```css
/* css/estilos.css — Líneas 121-128: Hover en tarjetas */
.tarjeta-logo:hover {
    transform: translateY(-6px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}
```

**Archivo:** `css/estilos.css` · Líneas 121–128 · Ruta: `/css/estilos.css`

### 7. Diseño responsive con media queries — css/estilos.css

Se incluye un breakpoint a 768px que adapta la cabecera a vertical, reduce tamaños de fuente en el hero, y fuerza las tarjetas e info-bloques a ancho completo en pantallas pequeñas.

```css
/* css/estilos.css — Líneas 271-291: Media query para móviles */
@media (max-width: 768px) {
    header {
        flex-direction: column;
        gap: 10px;
    }
    .tarjeta-logo {
        width: 100%;
        min-width: auto;
    }
}
```

**Archivo:** `css/estilos.css` · Líneas 271–291 · Ruta: `/css/estilos.css`

### 8. JavaScript — Función cambiarIdioma() — js/idiomas.js

El corazón del sistema multiidioma. La función busca todos los elementos con el atributo `data-[idioma]`, comprueba el tipo de elemento (input/textarea vs. otros) y actualiza `textContent`, `placeholder` o `value` según corresponda. También actualiza el atributo `lang` del `<html>`.

```javascript
// js/idiomas.js — Líneas 16-41: Función cambiarIdioma
function cambiarIdioma(idioma) {
    idiomaActual = idioma;
    var elementos = document.querySelectorAll('[data-' + idioma + ']');
    elementos.forEach(function(el) {
        var texto = el.getAttribute('data-' + idioma);
        if (el.tagName === 'INPUT' && el.type !== 'submit') {
            el.placeholder = texto;
        } else if (el.tagName === 'INPUT' && el.type === 'submit') {
            el.value = texto;
        } else {
            el.textContent = texto;
        }
    });
    document.documentElement.lang = idioma;
}
```

**Archivo:** `js/idiomas.js` · Líneas 16–41 · Ruta: `/js/idiomas.js`

### 9. Validación de formulario con alertas multiidioma — js/idiomas.js

El formulario de contacto tiene validación JavaScript que comprueba campos vacíos y formato de email. Los mensajes de error y confirmación se muestran en el idioma activo utilizando un operador ternario encadenado.

```javascript
// js/idiomas.js — Líneas 69-87: Validación y envío
if (!nombre.value.trim() || !email.value.trim() || !mensaje.value.trim()) {
    alert(idiomaActual === 'es' ? '⚠️ Por favor, rellena todos los campos.' :
          idiomaActual === 'en' ? '⚠️ Please fill in all fields.' :
          '⚠️ Veuillez remplir tous les champs.');
    return;
}
```

**Archivo:** `js/idiomas.js` · Líneas 69–87 · Ruta: `/js/idiomas.js`

### 10. Imágenes SVG como logos placeholder — img/

Se han creado 6 imágenes SVG simples que actúan como logos de ejemplo. Cada SVG usa formas geométricas (círculos y rectángulos redondeados) con colores representativos del sector: azul (tecnología), rojo (deportes), naranja (alimentación), verde (comercio), púrpura (música) y gris oscuro (automoción).

```xml
<!-- img/logo-tech.svg — Logo de ejemplo para TechCorp -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="45" fill="#3498db"/>
  <text x="50" y="62" text-anchor="middle" font-size="40" fill="white" font-weight="bold">T</text>
</svg>
```

**Archivo:** `img/logo-tech.svg` · Ruta: `/img/logo-tech.svg` (6 archivos SVG en total)

### 11. Accesibilidad — index.html

Se han incluido atributos `aria-label` en los elementos `<nav>` para diferenciar la navegación principal de la del footer. Todas las imágenes llevan atributo `alt` descriptivo. Los inputs del formulario están vinculados a sus labels mediante `for`/`id`.

```html
<!-- index.html — Líneas 17, 181: Accesibilidad en navegación -->
<nav aria-label="Navegación principal">
...
<nav aria-label="Enlaces del pie de página">
```

**Archivo:** `index.html` · Líneas 17 y 181 · Ruta: `/index.html`

## Presentación del proyecto

LogoGallery es una galería web interactiva de logos de marcas famosas que he desarrollado con HTML5, CSS3 y JavaScript vanilla. Lo que hace especial a este proyecto es su sistema de internacionalización: toda la interfaz se puede cambiar entre español, inglés y francés con un solo clic, sin recargar la página.

La web presenta 6 logos ficticios de diferentes sectores industriales, cada uno en una tarjeta interactiva con información del sector, año de fundación y una descripción del diseño. Las tarjetas tienen efectos hover con elevación y sombra que dan profundidad a la interfaz.

El diseño es completamente responsive gracias a Flexbox y media queries — se adapta perfectamente desde pantallas de escritorio hasta dispositivos móviles. La paleta de colores usa un esquema oscuro profesional con acento rojo para los elementos destacados.

El formulario de contacto incluye validación en JavaScript con mensajes de error que también cambian de idioma automáticamente. La funcionalidad de cambio de idioma está implementada mediante atributos `data-*` de HTML5 y manipulación del DOM con JavaScript, lo que demuestra la integración entre los tres lenguajes fundamentales de la web.

Las imágenes de los logos son SVG vectoriales ligeros, lo que garantiza calidad en cualquier resolución de pantalla y un rendimiento óptimo de carga.

## Conclusión

Este proyecto demuestra cómo HTML, CSS y JavaScript trabajan juntos para crear una experiencia web completa e interactiva. El sistema multiidioma mediante atributos `data-*` es un patrón real utilizado en proyectos de internacionalización, y su implementación muestra dominio de la manipulación del DOM. El diseño responsive con Flexbox, las transiciones CSS y la validación de formularios con JavaScript cubren las competencias fundamentales del desarrollo web frontend. La estructura del código es limpia, comentada y fácil de mantener, facilitando futuras ampliaciones como añadir nuevos idiomas o nuevos logos a la galería.
