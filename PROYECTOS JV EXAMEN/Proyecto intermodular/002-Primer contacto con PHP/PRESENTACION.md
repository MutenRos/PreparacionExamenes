# Primer contacto con PHP — Catálogo de productos JOCARSA

![Catálogo JOCARSA](docs/img/banner.png)

## Introducción

Este proyecto construye paso a paso un catálogo web de productos de la empresa JOCARSA utilizando PHP y XML. Partiendo de un esqueleto HTML básico, cada iteración añade una funcionalidad nueva: cabecera, lectura dinámica de datos desde XML, estilos CSS, layout en rejilla y tarjetas con color de fondo dinámico. El resultado final es una página de catálogo totalmente funcional que lee sus datos de un fichero XML y los presenta con un diseño visual atractivo.

## Desarrollo de las partes

### 1. Esqueleto HTML básico

El punto de partida es una estructura HTML5 mínima con las etiquetas semánticas `<header>`, `<main>` y `<footer>`.

- **Archivo:** `001-web basica.php`, líneas 1–18
- **Ruta:** `001-web basica.php`

```html
<!doctype html>
<html lang="es">
  <head>
    <title>JOCARSA</title>
    <meta charset="utf-8">
  </head>
  <body>
    <header></header>
    <main></main>
    <footer></footer>
  </body>
</html>
```

Este fichero establece la base sobre la que se construirán todas las versiones posteriores.

### 2. Cabecera con navegación

Se añade el título de la empresa y un enlace de navegación dentro de `<header>`.

- **Archivo:** `002-cabecera.php`, líneas 9–13
- **Ruta:** `002-cabecera.php`

```html
<header>
  <h1>JOCARSA | Soluciones de software empresarial</h1>
  <nav>
    <a href="">Quienes somos</a>
  </nav>
</header>
```

### 3. Lectura dinámica de productos desde XML

La funcionalidad central del proyecto: PHP carga el fichero `productos.xml` con `simplexml_load_file()` y recorre cada `<producto>` con un `foreach`.

- **Archivo:** `004-productos desde xml.php`, líneas 15–29
- **Ruta:** `004-productos desde xml.php`

```php
$xml = simplexml_load_file("productos.xml");
foreach ($xml->producto as $producto) {
    $nombre      = (string)$producto->nombre;
    $descripcion = (string)$producto->descripcion;
    $logo        = (string)$producto->logo;
    $enlace      = (string)$producto->enlace;
    echo "<div class='producto'>";
    echo "<img src='$logo' alt='$nombre' style='width:80px'><br>";
    echo "<strong>$nombre</strong><br>";
    echo "<em>$descripcion</em><br>";
    echo "</div>";
}
```

### 4. Fichero XML de datos

Los 19 productos se definen en un fichero XML independiente, cada uno con nombre, descripción, logo y enlace.

- **Archivo:** `productos.xml`, líneas 1–100
- **Ruta:** `productos.xml`

```xml
<producto>
    <nombre>jocarsa | teal</nombre>
    <descripcion>Software de gestión de empresa low-code</descripcion>
    <logo>https://static.jocarsa.com/logos/teal.png</logo>
    <enlace>?producto=jocarsa | teal</enlace>
</producto>
```

Los productos incluyen software de facturación, reservas, correo electrónico, calendarios, fichaje laboral y más.

### 5. Estilos CSS y cabecera estilizada

Se añade CSS inline para dar estilo a la cabecera: fondo negro, texto blanco, flexbox para centrar y separar elementos.

- **Archivo:** `005-css bonito.php`, líneas 7–11
- **Ruta:** `005-css bonito.php`

```css
body,html{padding:0px;margin:0px;}
header{background:black;color:white;display:flex;
  justify-content:center;align-items:center;
  font-size:12px;gap:20px;}
header a{color:inherit;text-decoration:none;font-size:1em;}
```

### 6. Semántica HTML: articles en vez de divs

Se sustituye `<div class='producto'>` por `<article>`, mejorando la semántica del documento. Se añade también el enlace «Más información».

- **Archivo:** `006-quiero articles.php`, líneas 27–33
- **Ruta:** `006-quiero articles.php`

```php
echo "<article>";
echo "<img src='$logo' alt='$nombre' style='width:80px'><br>";
echo "<strong>$nombre</strong><br>";
echo "<em>$descripcion</em><br>";
echo "<a href='$enlace'>Más información</a><br>";
echo "</article>";
```

### 7. Layout en rejilla con flexbox

Se crea una rejilla compleja usando `nth-child`: los 4 primeros productos ocupan el 100% del ancho, los siguientes 4 el 50%, y el resto el 33%.

- **Archivo:** `007-rejilla compleja.php`, líneas 42–56
- **Ruta:** `007-rejilla compleja.php`

```css
main > article:nth-child(-n+4) {
  flex: 0 0 100%;
}
main > article:nth-child(n+5):nth-child(-n+8) {
  flex: 0 0 calc(50% - 10px);
}
main > article:nth-child(n+9) {
  flex: 0 0 calc(33.333% - 10px);
}
```

### 8. Fondo dinámico por producto

La versión final extrae el nombre del color del producto y lo aplica como `background` del `<article>`, creando un catálogo visualmente llamativo con tarjetas de colores y botones redondeados.

- **Archivo:** `008-estilo de la web.php`, líneas 89–97
- **Ruta:** `008-estilo de la web.php`

```php
echo "<article style='background:".str_replace("jocarsa |","",$nombre).";'>";
echo "  <img src='$logo' alt='$nombre' style='width:80px'>";
echo "  <strong>$nombre</strong>";
echo "  <em>$descripcion</em>";
echo "  <a href='$enlace' style='color:".str_replace("jocarsa |","",$nombre).";'>Más información</a>";
echo "</article>";
```

### 9. Mejoras aplicadas

Se añadieron mejoras transversales en la versión final:

- **`htmlspecialchars()`** en nombre, descripción, logo y enlace para prevenir ataques XSS.
- **`<meta name="viewport">`** para responsive design en móviles.
- **`transition` y `:hover`** en las tarjetas con elevación y sombra.
- **`focus-visible`** en los enlaces para accesibilidad con teclado.
- **`prefers-reduced-motion`** para respetar preferencias del usuario.
- **Footer dinámico** con el año actual usando `date('Y')`.
- **Error handling** para `simplexml_load_file` con comprobación de fallo.
- **Corrección del logo** del producto «grey» que apuntaba erróneamente a `chartreuse.png`.

## Presentación del proyecto

El proyecto **Primer contacto con PHP** es un recorrido didáctico completo por la creación de una página web dinámica. Se parte de un HTML vacío y se llega hasta un catálogo de 19 productos con colores dinámicos, rejilla adaptable y datos leídos de un fichero XML externo.

La web muestra el catálogo de productos de JOCARSA, una suite de software empresarial. Cada producto se identifica por un color (teal, rosybrown, royalblue...) que se usa tanto para el fondo de la tarjeta como para el logo. El resultado es una página visualmente impactante donde cada tarjeta tiene su propio color de identidad.

El flujo es sencillo pero efectivo: PHP lee `productos.xml`, recorre cada producto y genera el HTML correspondiente con estilos inline dinámicos. No se necesita base de datos — el XML actúa como fuente de datos ligera y portable.

## Conclusión

Este proyecto demuestra que con PHP básico y un fichero XML se puede construir una web dinámica completa sin necesidad de bases de datos ni frameworks. Las 8 iteraciones muestran una progresión lógica desde el HTML puro hasta un catálogo con estilos avanzados, buen uso de semántica y un layout responsive con flexbox. Las mejoras de seguridad (htmlspecialchars), accesibilidad (focus-visible, prefers-reduced-motion) y robustez (manejo de errores XML) elevan el proyecto por encima de un simple ejercicio y lo convierten en un ejemplo sólido de buenas prácticas en desarrollo web.
