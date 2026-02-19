# Mejora de la Web de Juguetes — recortabl.es

![Web de recortables de papel](012-css%20galeria.html)

> 🔗 **GitHub Pages:** [https://mutenros.github.io/Sistemas-informaticos-004-Mejora-de-la-web-de-juguetes/](https://mutenros.github.io/Sistemas-informaticos-004-Mejora-de-la-web-de-juguetes/)

## Introducción

Este proyecto mejora la web de una tienda de juguetes recortables de papel — **recortabl.es** — construida en las asignaturas de Lenguajes de Marcas (maquetación HTML/CSS) y Entornos de Desarrollo (panel de administración). En Sistemas Informáticos se trabaja sobre el front-end, refinando progresivamente la página principal desde un HTML vacío hasta una web completa con hero, categorías, productos destacados, galería de imágenes e información educativa.

El proyecto consta de 12 archivos HTML que representan cada paso iterativo de construcción: desde la estructura básica hasta el diseño final con CSS completo, fuente Google Fonts (Delius) y todas las secciones estilizadas.

---

## Desarrollo de las partes

### 1. 001-inicio.html — El esqueleto HTML vacío

El primer archivo es el punto de partida absoluto: un documento HTML5 vacío con solo las etiquetas `<html>`, `<head>` y `<body>`. Representa el momento cero antes de escribir cualquier contenido.

```html
<!-- 001-inicio.html — líneas 1-9 -->
<!-- Ruta: 001-inicio.html -->
<!doctype html>
<html>
  <head>
  </head>
  <body>
  </body>
</html>
```

Este archivo demuestra que todo proyecto web empieza con una estructura mínima que luego se irá rellenando paso a paso.

---

### 2. 002-datos iniciales.html — Estructura semántica completa

El segundo archivo añade toda la estructura semántica: `lang="es"`, `<title>`, `<meta charset>`, y el esqueleto completo con `<header>` (logo h1 + nav con enlaces y buscador), `<main>` (5 secciones vacías: heroe, categorías, destacados, galería, información) y `<footer>` (nav con enlaces legales y redes sociales).

```html
<!-- 002-datos iniciales.html — líneas 7-18 -->
<!-- Ruta: 002-datos iniciales.html -->
<header>
  <h1>recortabl.es</h1>
  <nav>
    <a href="">Categorias</a>
    <a href="">Sobre nosotros</a>
    <a href="">Descargas</a>
    <a href="">Iniciar sesión</a>
    <input type="search" placeholder="buscar">
  </nav>
</header>
```

La estructura semántica usa `<header>`, `<main>`, `<section>`, `<footer>` y `<nav>`, que son etiquetas HTML5 que aportan significado al contenido.

---

### 3. 003 a 007 — Contenido progresivo de cada sección

Los archivos del 003 al 007 van rellenando secciones una a una:
- **003-heroe.html**: Añade h3 (título), h4 (subtítulo) y dos botones CTA al héroe.
- **004-categorias principales.html**: Crea 7 tarjetas de categoría (Vehículos, Edificios, Robots, Animales, Navidad, Educativos, Muñecos) usando `<article>` + `<img>` + `<p>`.
- **005-recortables destacados.html**: Añade 4 productos destacados con estrellas ⭐⭐⭐⭐⭐.
- **006-galeria.html**: Galería de 5 imágenes enlazadas.
- **007-informacion.html**: Sección informativa con 4 checkmarks ✅.

```html
<!-- 004-categorias principales.html — líneas 22-30 -->
<!-- Ruta: 004-categorias principales.html -->
<section id="categoriasprincipales">
  <h3>Categorías principales</h3>
  <div class="contenedor">
    <article>
      <img src="">
      <p>Vehículos</p>
    </article>
    <!-- ... 7 categorías en total -->
  </div>
</section>
```

Cada archivo acumula el contenido de los anteriores, mostrando una construcción incremental.

---

### 4. 008-importo fuente.html — Google Fonts y primeros estilos

Este archivo marca el inicio del CSS: importa la fuente **Delius** de Google Fonts y añade los primeros estilos básicos: reset de margin/padding en el body, `font-family: Delius, sans-serif`, flexbox en el header con `justify-content: space-between`, y el fondo azul `#267eca` del héroe.

```html
<!-- 008-importo fuente.html — líneas 6-14 -->
<!-- Ruta: 008-importo fuente.html -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Delius&display=swap" rel="stylesheet">
<style>
  body{padding:0px;margin:0px;
  font-family:Delius,sans-serif;}
  header{display:flex;justify-content:space-between;align-items:center;padding:10px;
  box-shadow:0px 5px 10px rgba(0,0,0,0.2);}
  #heroe{background:#267eca;}
</style>
```

El `preconnect` a Google Fonts mejora la velocidad de carga al iniciar la conexión antes de pedir la fuente.

---

### 5. 009 a 011 — CSS progresivo para cada sección

- **009-heroe.html**: Estilos del héroe — texto centrado blanco con text-shadow, botones azules con border-radius y box-shadow, altura 200px.
- **010-categorias principales.html**: Flexbox para las tarjetas de categoría con gap de 10px, fondo blanco y border-radius 5px. También se estila recortables destacados con la misma estructura.
- **011-destacados.html**: Se repite el patrón flex para destacados (este archivo también incluye la galería y la información sin CSS todavía).

```css
/* 009-heroe.html — líneas 15-19 */
/* Ruta: 009-heroe.html */
#heroe{background:#267eca;text-align:center;color:white;font-weight:bold;
  padding:20px;height:200px;}
#heroe h3{font-size:36px;text-shadow:0px 3px 6px rgba(0,0,0,0.3);}
#heroe h4{font-size:22px;text-shadow:0px 3px 6px rgba(0,0,0,0.3);
  margin-bottom:20px;}
#heroe a{background:blue;padding:10px 20px;border:1px solid darkblue;
  border-radius:5px;box-shadow:0px 2px 4px rgba(0,0,0,0.3);}
```

El uso de `text-shadow` y `box-shadow` da profundidad visual al héroe sin necesitar imágenes.

---

### 6. 012-css galeria.html — La versión final completa

El archivo más avanzado integra todos los estilos CSS: galería con imágenes en flex con borde blanco, sección informativa con borde dashed y fondo amarillo claro `#faf4db`. Este es el archivo que recibió las mejoras del PASO 2.

```css
/* 012-css galeria.html — líneas 57-66 */
/* Ruta: 012-css galeria.html */
#galeria{
  display:flex;
  justify-content:space-between;
  gap:10px;
  flex-wrap:wrap;
}
#galeria a img{
  background:white;
  border-radius:5px;
  width:100%;
  padding:20px;
  border:5px solid white;
  transition:border-color .2s;
}
#galeria a:hover img{border-color:#267eca;}
```

---

### 7. Mejoras aplicadas — CSS, HTML y JavaScript

Se aplicaron mejoras que demuestran aprendizaje en varias capas:

**HTML**: `<meta name="viewport">` para responsive, `<meta name="description">` para SEO, atributos `alt` en todas las imágenes para accesibilidad, `href="#seccion"` en vez de `href=""` para navegación interna funcional.

**CSS**: `position:sticky` en el header, transitions en tarjetas de categoría y destacados (`transform:translateY(-4px)` + `box-shadow` en hover), hover en botones del héroe, en enlaces de galería (`scale(1.03)`), borde azul en galería hover, footer con fondo `#2c3e50` y enlaces blancos, media query `@media(max-width:768px)` que apila las secciones en columna.

```css
/* 012-css galeria.html — líneas mejoradas */
/* Ruta: 012-css galeria.html */
#categoriasprincipales .contenedor article{
  transition:transform .2s,box-shadow .2s;
  cursor:pointer;
}
#categoriasprincipales .contenedor article:hover{
  transform:translateY(-4px);
  box-shadow:0 6px 16px rgba(0,0,0,0.12);
}
```

**JavaScript**: Buscador funcional que filtra los recortables destacados por nombre en tiempo real con `oninput`.

```javascript
// 012-css galeria.html — script final
// Ruta: 012-css galeria.html
function filtrarRecortables(){
  var q = document.getElementById('buscador').value.toLowerCase();
  var cards = document.querySelectorAll('#recortablesdestacados .contenedor article');
  cards.forEach(function(card){
    var nombre = card.querySelector('p').textContent.toLowerCase();
    card.style.display = nombre.includes(q) ? '' : 'none';
  });
}
```

---

## Presentación del proyecto

recortabl.es es una web de juguetes recortables de papel para familias y educación. El proyecto demuestra la construcción progresiva de una página web desde cero: empezando por un HTML vacío y añadiendo paso a paso la estructura semántica, el contenido de cada sección, la fuente tipográfica, y finalmente el CSS de cada componente.

La página final tiene 5 secciones: un héroe azul con título y CTAs, 7 categorías principales (Vehículos, Edificios, Robots, Animales, Navidad, Educativos, Muñecos), 4 productos destacados con estrellas, una galería de imágenes y una sección informativa educativa. Todo construido con HTML semántico, CSS flexbox y la fuente Delius de Google Fonts.

Los 12 archivos forman una secuencia que va desde `001-inicio.html` (vacío) hasta `012-css galeria.html` (completo con todo el CSS). Las mejoras añaden interactividad (hover, transitions, responsive, buscador JS), accesibilidad (alt en imágenes, viewport), navegación funcional, y un footer profesional.

Este proyecto es la parte front-end de un proyecto más grande que incluye un panel de administración PHP (Entornos de Desarrollo) y la maquetación HTML/CSS original (Lenguajes de Marcas).

---

## Conclusión

recortabl.es demuestra que una web profesional se puede construir paso a paso sin frameworks: solo HTML semántico, CSS con flexbox y una buena fuente tipográfica. Los 12 archivos muestran un proceso de desarrollo real donde cada iteración añade una funcionalidad nueva — exactamente como se trabaja en un proyecto real.

Las mejoras aplicadas — responsive design, interactividad con hover/transitions, buscador JavaScript, atributos de accesibilidad, navegación interna y footer estilizado — refuerzan buenas prácticas web que complementan el trabajo original sin cambiar su estructura ni su filosofía de diseño iterativo.
