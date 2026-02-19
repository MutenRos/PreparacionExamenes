# Tienda de juguetes recortables — recortabl.es

![Página principal recortabl.es](imgcategoria.png)

> 🔗 **GitHub Pages:** [https://mutenros.github.io/Lenguajes-de-marcas-003-Tienda-de-juguetes/](https://mutenros.github.io/Lenguajes-de-marcas-003-Tienda-de-juguetes/)

## Introducción

Este proyecto consiste en la creación progresiva de una página web para una tienda online de juguetes recortables llamada **recortabl.es**. A lo largo de 12 ejercicios evolutivos, se construye desde cero una landing page completa utilizando únicamente HTML y CSS (con estilos inline en `<style>`). La web presenta categorías de recortables, productos destacados con valoración, una galería de imágenes, sección informativa y un footer con enlaces legales y redes sociales. Todo el proyecto utiliza una fuente personalizada de Google Fonts (Delius) y un esquema de colores basado en azul (#267eca).

## Desarrollo de las partes

### 1. Estructura HTML vacía

Se parte de la estructura más básica posible: un documento HTML5 con `<!doctype html>`, `<head>` y `<body>` vacíos.

```html
<!doctype html>
<html>
    <head>
    </head>
    <body>
    </body>
</html>
```

- **Archivo:** `001-inicio.html`
- **Líneas:** 1-8
- **Ruta:** `001-inicio.html`

### 2. Datos iniciales y estructura semántica

Se añade el esqueleto semántico completo: `lang="es"`, `<title>`, `<meta charset>`, `<header>` con logo y navegación (5 enlaces + buscador), `<main>` con 5 secciones vacías (héroe, categorías, destacados, galería, información) y `<footer>` con enlaces legales y redes sociales.

```html
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

- **Archivo:** `002-datos iniciales.html`
- **Líneas:** 8-16 (header), 17-31 (main con secciones), 32-43 (footer)
- **Ruta:** `002-datos iniciales.html`

### 3. Sección héroe

Se rellena la sección héroe con un título principal (`<h3>`), un subtítulo (`<h4>`) con el flujo de uso del producto ("Descarga - Imprime - Recorta - Pega - Juega") y dos botones CTA.

```html
<section id="heroe">
    <h3>Juguetes recortables para imprimir y jugar</h3>
    <h4>Descarga - Imprime - Recorta - Pega - Juega</h4>
    <a href="">Explorar recortables</a>
    <a href="">Cómo funciona</a>
</section>
```

- **Archivo:** `003-heroe.html`
- **Líneas:** 19-24
- **Ruta:** `003-heroe.html`

### 4. Categorías principales

Se crean 7 categorías de productos usando `<article>` dentro de un `<div class="contenedor">`: Vehículos, Edificios, Robots, Animales, Navidad, Educativos y Muñecos. Cada categoría tiene una imagen y un nombre.

```html
<section id="categoriasprincipales">
    <h3>Categorías principales</h3>
    <div class="contenedor">
        <article>
            <img src="">
            <p>Vehículos</p>
        </article>
        <!-- ... 6 categorías más -->
    </div>
</section>
```

- **Archivo:** `004-categorias principales.html`
- **Líneas:** 25-60
- **Ruta:** `004-categorias principales.html`

### 5. Recortables destacados con valoración

Se añaden 4 productos destacados, cada uno con imagen, nombre y una valoración de 5 estrellas usando emojis ⭐.

```html
<section id="recortablesdestacados">
    <h3>Recortables destacados</h3>
    <div class="contenedor">
        <article>
            <img src="imgcategoria.png">
            <p>Castillo medieval</p>
            <p>⭐⭐⭐⭐⭐</p>
        </article>
        <!-- Coche fórmula 1, Dinosaurio T-Rex, Robot XL -->
    </div>
</section>
```

- **Archivo:** `005-reccotables destacados.html`
- **Líneas:** 61-85
- **Ruta:** `005-reccotables destacados.html`

### 6. Galería de imágenes

Se crea una galería con 5 enlaces que contienen imágenes, simulando una cuadrícula de recortables.

```html
<section id="galeria">
    <a href=""><img src="imgcategoria.png"></a>
    <a href=""><img src="imgcategoria.png"></a>
    <!-- ... 3 imágenes más -->
</section>
```

- **Archivo:** `006-galeria.html`
- **Líneas:** 87-107
- **Ruta:** `006-galeria.html`

### 7. Sección de información

Se añade un bloque informativo para familias y educación con 4 puntos clave usando emojis ✅.

```html
<section id="informacion">
    <div class="contenedor">
        <h3>Para familias y educación</h3>
        <p>✅ Manualidades educativas</p>
        <p>✅ Desarrollo de psicomotricidad</p>
        <p>✅ Uso en aula y en casa</p>
        <p>✅ PDFs listos para imprimir</p>
    </div>
</section>
```

- **Archivo:** `007-informacion.html`
- **Líneas:** 109-118
- **Ruta:** `007-informacion.html`

### 8. Fuente personalizada Google Fonts

Se importa la fuente "Delius" de Google Fonts con preconnect para optimizar la carga, y se aplica al body. Se añaden los primeros estilos CSS: reset de body y cabecera con flexbox y sombra.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Delius&display=swap" rel="stylesheet">
<style>
    body{font-family:Delius,sans-serif;}
    header{display:flex;justify-content:space-between;align-items:center;padding:10px;box-shadow:0px 5px 10px rgba(0,0,0,0.2);}
</style>
```

- **Archivo:** `008-importo fuente.html`
- **Líneas:** 6-14
- **Ruta:** `008-importo fuente.html`

### 9-11. Estilos CSS progresivos

En los archivos 009, 010 y 011 se van añadiendo estilos CSS progresivamente para cada sección: héroe (fondo azul, texto centrado, sombras), categorías (flexbox con gap), destacados (mismo layout que categorías) y galería (flexbox con imágenes con borde).

- **Archivos:** `009-heroe.html`, `010-categorias principales.html`, `011-destacados.html`
- **Ruta:** Raíz del proyecto

### 12. CSS galería e información (versión final)

La versión más avanzada incluye todos los estilos CSS completos: galería con imágenes con borde blanco, sección información con fondo amarillo pálido y borde punteado, y un reset CSS global.

```css
#galeria a img{
    background:white;
    border-radius:5px;
    width:100%;
    padding:20px;
    border:5px solid white;
}
#informacion .contenedor{
    padding:20px;
    border:1px dashed grey;
    background:#faf4db;
    border-radius:10px;
}
```

- **Archivo:** `012-css galeria.html`
- **Líneas:** 55-72 (galería CSS), 73-78 (información CSS)
- **Ruta:** `012-css galeria.html`

### 13. Mejoras aplicadas por el alumno

- **HTML**: Añadido `<meta name="viewport">` para diseño responsive.
- **CSS**: `box-sizing:border-box` en el reset global.
- **HTML**: Atributos `alt` en todas las imágenes (accesibilidad).
- **CSS**: Transiciones `hover` en artículos de categorías y destacados (`translateY`, `box-shadow`).
- **CSS**: Efecto `scale` hover en imágenes de la galería.
- **CSS**: Transición en botones CTA del héroe.
- **CSS**: Footer estilizado (fondo azul, flex centrado, hover underline).
- **HTML**: Comentarios descriptivos por sección.
- **HTML**: `aria-label` en navegación principal y footer.

- **Archivo:** `012-css galeria.html`
- **Líneas:** 10 (viewport), 12 (box-sizing), 20-21 (hover hero), 35-38 (hover categorías), 47-50 (hover destacados), 60-63 (hover galería), 82-102 (footer CSS)
- **Ruta:** `012-css galeria.html`

## Presentación del proyecto

Este proyecto es una tienda online de juguetes recortables llamada **recortabl.es**, construida paso a paso con HTML y CSS puro.

La web tiene las siguientes secciones:

1. **Cabecera** con el nombre de la tienda y una barra de navegación con enlaces a categorías, "Sobre nosotros", descargas, inicio de sesión y un campo de búsqueda.
2. **Sección héroe** con el eslogan "Juguetes recortables para imprimir y jugar", el flujo de uso del producto y dos botones de acción.
3. **7 categorías principales** (Vehículos, Edificios, Robots, Animales, Navidad, Educativos, Muñecos) presentadas en tarjetas con imagen y nombre.
4. **4 recortables destacados** (Castillo medieval, Coche fórmula 1, Dinosaurio T-Rex, Robot XL) con imágenes y valoración de 5 estrellas.
5. **Galería** con 5 imágenes enlazadas de recortables.
6. **Sección informativa** para familias y educación, destacando los valores del producto: manualidades educativas, desarrollo de psicomotricidad, uso en aula y PDFs listos para imprimir.
7. **Footer** con enlaces legales (Acerca de, Contacto, Licencias, Aviso Legal) y redes sociales (FB, X.com, YT, Insta).

El diseño usa una paleta azul (#267eca) para el héroe y el footer, fondos claros (#ecf2f8) para las secciones alternas, tarjetas blancas con bordes redondeados y la fuente "Delius" de Google Fonts que le da un aspecto informal y divertido, acorde con la temática de juguetes.

Las mejoras aplicadas añaden interactividad visual (hover transitions en todas las tarjetas y la galería), accesibilidad (alt en imágenes, aria-label en navegaciones) y preparación responsive (viewport meta, box-sizing).

## Conclusión

Este proyecto demuestra cómo se construye una página web completa desde cero, iterando archivo tras archivo. Cada uno de los 12 ejercicios añade una pieza nueva: primero la estructura HTML semántica, luego el contenido de cada sección, después la fuente personalizada y finalmente los estilos CSS progresivos para cada componente.

La principal lección es la importancia de la construcción incremental: no se intenta hacer todo de golpe sino que se va añadiendo complejidad poco a poco. Esto permite entender cada parte del HTML y del CSS por separado antes de combinarlas. Las mejoras aplicadas (hover effects, accesibilidad, responsive) demuestran cómo pequeños detalles de CSS y HTML pueden elevar significativamente la calidad percibida de una web sin cambiar su estructura fundamental.
