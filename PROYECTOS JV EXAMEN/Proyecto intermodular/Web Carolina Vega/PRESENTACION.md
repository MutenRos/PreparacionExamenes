# Web Carolina Vega — Sitio web de artista musical

![Captura del hero de la web de Carolina Vega](heroe.png)

## Introducción

Este proyecto consiste en un sitio web completo para la cantautora ficticia **Carolina Vega**. La web funciona como carta de presentación profesional de la artista: muestra su biografía, discografía, próximas fechas de conciertos, galería fotográfica y un formulario de contacto para contrataciones y prensa.

El sitio está construido íntegramente con **HTML5 semántico** y **CSS3** avanzado (variables custom, grid, flexbox, media queries), sin necesidad de JavaScript frameworks ni backend. Incluye una tipografía personalizada (@font-face), elementos multimedia `<audio>`, diseño responsive completo y una estética cuidada que combina transparencias, sombras y fondos fotográficos.

---

## Desarrollo de las partes

### 1. Estructura HTML semántica y accesibilidad

El proyecto utiliza HTML5 semántico en todas las páginas. Cada sección tiene su atributo `aria-label` y los enlaces de navegación usan `aria-current="page"` para indicar la página activa. Esto mejora la accesibilidad para lectores de pantalla.

```html
<!-- index.html — líneas 16-36 -->
<!-- Ruta: index.html -->
<section id="heroe" aria-label="Portada">
  <header>
    <h1>Carolina<br>Vega</h1>
    <nav aria-label="Navegación principal">
      <a href="index.html#inicio">Inicio</a>
      <a href="biografia.html">Biografía</a>
      <a href="musica.html">Música</a>
      <a href="tour.html">Tour</a>
      <a href="galeria.html">Galería</a>
      <a href="contacto.html">Contacto</a>
      <span></span>
      <a href="#" aria-label="Facebook">f</a>
      <a href="#" aria-label="X">x</a>
      <a href="#" aria-label="YouTube">▶</a>
    </nav>
  </header>
```

La navegación se repite de forma consistente en las 6 páginas del sitio (index, biografía, música, tour, galería y contacto), manteniendo siempre la misma estructura pero marcando la página activa con `aria-current`.

---

### 2. Sistema de diseño CSS con variables custom

El archivo `style.css` define un sistema de diseño basado en variables CSS (custom properties) que permiten mantener la coherencia visual en toda la web. Los colores, sombras y bordes se definen una sola vez y se reutilizan.

```css
/* style.css — líneas 7-14 */
/* Ruta: style.css */
:root{
  --papel: rgba(255,255,255,.78);
  --papel2: rgba(255,255,255,.62);
  --marron: rgba(35,18,12,.72);
  --marron2: rgba(35,18,12,.52);
  --negro: rgba(0,0,0,.65);
  --sombra: 0 10px 30px rgba(0,0,0,.35);
  --borde: rgba(80,45,30,.25);
}
```

Las variables se aplican en secciones como `#contenido`, `.panel`, `.card`, `#tienda`, etc. para lograr un efecto visual de "papel" translúcido sobre fondo fotográfico, con bordes suaves y sombras consistentes.

---

### 3. Hero con tipografía personalizada y overlay

La sección hero es el elemento visual más impactante de la web. Utiliza una tipografía @font-face (Magiera Script), un fondo fotográfico con overlay radial-gradient y linear-gradient, y una disposición flexible que separa el logotipo de la navegación.

```css
/* style.css — líneas 1-6, 30-50 */
/* Ruta: style.css */
@font-face{
  font-family: magiera;
  src: url("Magiera Script.ttf");
}

#heroe{
  min-height: 660px;
  background: url("heroe.png") center top / cover no-repeat;
  position: relative;
  overflow: hidden;
}
#heroe::after{
  content:"";
  position:absolute; inset:0;
  background:
    radial-gradient(1200px 520px at 55% 30%, rgba(255,210,160,.25), transparent 60%),
    linear-gradient(180deg, rgba(0,0,0,.35), rgba(0,0,0,.10) 40%, rgba(0,0,0,.18));
  pointer-events:none;
}
```

El pseudo-elemento `::after` crea una capa de iluminación cinematográfica que da profundidad al hero sin oscurecer demasiado la foto de fondo. El texto del nombre de la artista tiene `transform: rotate(-10deg)` y `text-shadow` para un efecto manuscrito y dinámico.

---

### 4. Discografía con layout de álbumes

La sección de discografía muestra los álbumes en una lista horizontal con imagen de portada, título, año y botón de escucha. Usa flexbox para alinear los elementos y se repite tanto en `index.html` como en `musica.html`.

```html
<!-- index.html — líneas 67-99 -->
<!-- Ruta: index.html -->
<section id="albumes" aria-label="Discos publicados">
  <h4>DISCOS PUBLICADOS</h4>
  <article>
    <img src="portada.png" alt="Portada Entre Luces y Sombras">
    <h5>Entre Luces y Sombras</h5>
    <p>2024</p>
    <a class="boton" href="#">Escuchar</a>
  </article>
  <!-- ... más álbumes ... -->
</section>
```

Cada álbum tiene una transición CSS al hacer hover que lo eleva ligeramente (`translateY(-3px)`) para dar feedback visual al usuario.

---

### 5. Reproductor de canciones con audio HTML5

La sección de últimas canciones integra el elemento `<audio>` nativo de HTML5 con controles del navegador. Cada canción tiene un botón de reproducción, título y enlace de opciones, organizados en un grid de 4 columnas.

```html
<!-- index.html — líneas 105-128 -->
<!-- Ruta: index.html -->
<section id="canciones" aria-label="Últimas canciones">
  <h4>ÚLTIMAS CANCIONES</h4>
  <article>
    <button aria-label="Reproducir Entre Luces y Sombras">▶</button>
    <h5>Entre Luces y Sombras</h5>
    <audio src="A Long Weekend.mp3" controls></audio>
    <a href="#" aria-label="Más opciones">···</a>
  </article>
</section>
```

```css
/* style.css — líneas 241-254 */
/* Ruta: style.css */
#canciones article{
  display:grid;
  grid-template-columns: 42px 1fr 180px 44px;
  align-items:center;
  gap: 10px;
  transition: background .2s ease;
}
#canciones article:hover{
  background: rgba(255,255,255,.72);
}
```

---

### 6. Tabla de conciertos (Tour)

La página `tour.html` presenta las fechas de conciertos en un layout tipo tabla construido con divs y roles ARIA (`role="table"`, `role="row"`, `role="cell"`). Incluye filtros de búsqueda por ciudad y estado, y chips visuales (Próximas, Agotado, Anunciado).

```html
<!-- tour.html — líneas 71-109 -->
<!-- Ruta: tour.html -->
<div class="tabla-tour" role="table" aria-label="Tabla de conciertos">
  <div class="fila cabecera" role="row">
    <div role="columnheader">Fecha</div>
    <div role="columnheader">Ciudad</div>
    <div role="columnheader">Sala / Evento</div>
    <div role="columnheader">Estado</div>
    <div role="columnheader">Entradas</div>
  </div>
  <div class="fila" role="row">
    <div role="cell">09 · MAR · 2026</div>
    <div role="cell">Valencia</div>
    <div role="cell">Sala Example</div>
    <div role="cell"><span class="chip">Próximas</span></div>
    <div role="cell"><a class="boton" href="#">Entradas</a></div>
  </div>
</div>
```

Los chips cambian de estilo según el estado: `.chip.agotado` tiene un fondo más oscuro para señalar que no hay entradas disponibles.

---

### 7. Galería fotográfica con grid y hover

La página `galeria.html` muestra una cuadrícula de 4 columnas con fotos que hacen zoom sutil al pasar el ratón (`transform: scale(1.02)`). Incluye filtros por categoría (Todas, Promocional, Directo, Backstage) con chips interactivos.

```css
/* style.css — líneas 594-610 */
/* Ruta: style.css */
.grid-galeria{
  display:grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}
.grid-galeria img{
  width: 100%;
  height: 170px;
  object-fit: cover;
  display:block;
  transition: transform .2s ease;
}
.grid-galeria .foto:hover img{transform: scale(1.02)}
```

Cada imagen tiene un atributo `alt` descriptivo para mejorar SEO y accesibilidad (por ejemplo `alt="Carolina Vega en directo en sala"`).

---

### 8. Formulario de contacto con validación

La página `contacto.html` incluye un formulario con grid de 2 columnas para nombre, email, asunto (select) y mensaje (textarea), más un aside con información de gestión y redes. Se añadió validación JavaScript que comprueba la longitud mínima del mensaje y pide confirmación antes de enviar.

```html
<!-- contacto.html — líneas 68-81 -->
<!-- Ruta: contacto.html -->
<form class="form-contacto" action="#" method="post">
  <label>Nombre <input type="text" name="nombre" required></label>
  <label>Email <input type="email" name="email" required></label>
  <label>Asunto
    <select name="asunto" required>
      <option value="">Selecciona…</option>
      <option>Contratación</option>
      <option>Prensa / Presskit</option>
      <option>Colaboración</option>
    </select>
  </label>
  <label class="ancho">Mensaje <textarea name="mensaje" rows="7" required></textarea></label>
</form>
```

```javascript
// contacto.html — líneas 109-119
// Ruta: contacto.html
document.querySelector('.form-contacto').addEventListener('submit', function(e) {
  var email = this.querySelector('[name="email"]');
  var mensaje = this.querySelector('[name="mensaje"]');
  if (mensaje.value.trim().length < 10) {
    e.preventDefault();
    alert('Por favor, escribe un mensaje de al menos 10 caracteres.');
    mensaje.focus();
    return;
  }
  if (!confirm('¿Enviar el mensaje a Carolina Vega?')) {
    e.preventDefault();
  }
});
```

---

### 9. Diseño responsive con media queries

El CSS incluye breakpoints a 980px, 720px y 520px que reorganizan los layouts de grid y flexbox para adaptarse a pantallas pequeñas. La tabla de tour pasa de 5 a 3 columnas, la galería de 4 a 2 y luego a 1 columna, y la biografía pasa de 2 columnas a 1.

```css
/* style.css — líneas 387-414 */
/* Ruta: style.css */
@media (max-width: 980px){
  #heroe > header{flex-direction:column;align-items:flex-start}
  #destacado{margin: 40px 0 0 22px}
  #bloques{grid-template-columns: 1fr}
  .bio{grid-template-columns: 1fr}
  .cards{grid-template-columns: 1fr}
  .contacto-grid{grid-template-columns: 1fr}
  .grid-galeria{grid-template-columns: repeat(2, 1fr)}
}

@media (max-width: 520px){
  .grid-galeria{grid-template-columns: 1fr}
  .form-contacto{grid-template-columns: 1fr}
}
```

---

### 10. Mejoras aplicadas

Se aplicaron mejoras mixtas que tocan CSS, HTML y JavaScript:

- **Meta descriptions** en las 6 páginas para mejorar SEO (`<meta name="description">`).
- **CSS transitions** en botones (`.boton`), álbumes (`#albumes article`), canciones (`#canciones article`), y tarjetas (`.card`) con efectos hover.
- **Focus styles** en los inputs del newsletter y formulario de contacto con `box-shadow` y `border-color`.
- **`scroll-behavior: smooth`** en `html` para navegación suave dentro de la página.
- **Alt descriptivos** en las 12 imágenes de la galería (antes eran genéricos "Foto 1", "Foto 2"…).
- **Validación JS** en el formulario de contacto (longitud mínima + confirmación) y en el newsletter (formato email).

---

## Presentación del proyecto

La web de Carolina Vega es un sitio de 6 páginas que funciona como carta de presentación profesional de una artista musical. La página principal muestra un hero cinematográfico con tipografía manuscrita, la discografía con portadas, un reproductor integrado de canciones y una sección de newsletter.

Desde la navegación se accede a la biografía con datos de la artista y presskit, la página de música con plataformas de streaming, un calendario de tour con tabla de fechas y estados (próximas/agotado), una galería filtrable de fotos y un formulario de contacto para contrataciones.

Todo está construido con HTML semántico con etiquetas ARIA para accesibilidad, CSS con variables custom para mantener coherencia visual, grid y flexbox para los layouts, tipografía @font-face personalizada, y diseño responsive con 3 breakpoints que adaptan la web a móvil, tablet y escritorio.

---

## Conclusión

Este proyecto demuestra la capacidad de construir un sitio web profesional completo utilizando únicamente HTML5 y CSS3, sin dependencias de frameworks ni backend. La combinación de semántica HTML con ARIA, un sistema de diseño basado en variables CSS, layouts modernos (grid + flexbox), tipografía personalizada y diseño responsive produce un resultado visual atractivo y funcional.

Las mejoras aplicadas — meta descriptions para SEO, transiciones CSS para interactividad, focus styles para accesibilidad, y validación JavaScript en formularios — añaden capas de calidad profesional al proyecto original. El sitio es completamente estático, lo que facilita su despliegue en GitHub Pages y demuestra que se puede lograr un diseño sofisticado sin complejidad innecesaria.
