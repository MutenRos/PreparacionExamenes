# Web Curso IA en Directo

![Página principal del curso IA](img/destacado1.png)

> 🔗 **GitHub Pages:** [https://mutenros.github.io/Lenguajes-de-marcas-002-Web-curso-IA/](https://mutenros.github.io/Lenguajes-de-marcas-002-Web-curso-IA/)

## Introducción

Este proyecto consiste en la creación progresiva de una web promocional para un curso de Inteligencia Artificial en directo, orientada a la conversión de visitantes en alumnos inscritos. Se parte de una estructura HTML básica con marcadores de posición (placeholders `{{clave}}`) y se evoluciona hasta una web con SEO avanzado, estilos CSS profesionales, datos dinámicos vía JSON y un motor de plantillas PHP que sustituye los placeholders por contenido real. El resultado es una landing page completa con héroe, secciones destacadas, formulario de contacto y pie de página, lista para ser desplegada o servida por un servidor web.

## Desarrollo de las partes

### 1. Introducción teórica — Objetivo del proyecto

El punto de partida es la definición del objetivo empresarial: crear una web promocional que convierta visitantes en leads a través de un formulario de contacto. El flujo es: Web → Formulario → Correo.

```
Queremos:
1.-Promocionar un servicio o producto
2.-Crear una web pero desde el punto de vista empresarial
3.-Queremos una conversión
Web -> Formulario -> Correo
```

- **Archivo:** `001-introduccion.md`
- **Líneas:** 1-7
- **Ruta:** `001-introduccion.md`

### 2. Estructura HTML base con placeholders

Se construye la estructura semántica HTML de toda la web usando marcadores `{{clave}}` en lugar de contenido real. Incluye: header con logo y navegación, sección héroe, 9 secciones destacadas (con imágenes, textos y CTAs), formulario de contacto y footer.

```html
<header>
  <div id="corporativo">
    <img src="logo.png">
    <div class="texto">
      {{titulo1}}
      {{titulo2}}
    </div>
  </div>
  <nav>
    <a href="">{{enlace 1}}</a>
    ...
  </nav>
</header>
```

- **Archivo:** `002-web estatica.html`
- **Líneas:** 6-22 (header), 91-103 (formulario de contacto)
- **Ruta:** `002-web estatica.html`

### 3. Plantilla con clases CSS y estructura mejorada

Se refina la estructura HTML añadiendo clases CSS semánticas (`container`, `topbar`, `pill-card`, `section-grid`, etc.), etiquetas `aria-label` para accesibilidad y una organización más clara con comentarios HTML para cada sección.

```html
<section id="destacado1" class="soft" aria-label="Destacado 1">
  <div class="container">
    <div class="pill-card">
      <div class="left">
        <img src="destacado1.jpg" alt="">
      </div>
      <div class="right">
        <h4>{{destacado1titulo}}</h4>
        <p>{{destacado1texto}}</p>
      </div>
    </div>
  </div>
</section>
```

- **Archivo:** `003-con estilo.html`
- **Líneas:** 52-65 (destacado 1 con clases)
- **Ruta:** `003-con estilo.html`

### 4. Plantilla con CSS externo

Se separa la estructura HTML del estilo, vinculando una hoja de estilos CSS externa (`estilochatgpt.css`). La plantilla HTML queda limpia y reutilizable.

```html
<link rel="stylesheet" href="estilochatgpt.css">
```

- **Archivo:** `004-soloplantilla.html`
- **Líneas:** 7
- **Ruta:** `004-soloplantilla.html`

### 5. Plantilla con SEO avanzado (versión final)

La versión más avanzada de la plantilla HTML incorpora todas las meta etiquetas necesarias para SEO: `description`, `robots`, `theme-color`, `canonical`, Open Graph, Twitter Cards, un skip-link de accesibilidad, JSON-LD para datos estructurados (Organization, WebSite, WebPage, Course), precarga de recursos y un formulario con labels y autocomplete.

```html
<meta name="description" content="{{meta_description}}">
<meta name="robots" content="{{meta_robots}}">
<meta property="og:title" content="{{og_title}}">
<meta property="og:image" content="{{og_image}}">
<script type="application/ld+json">
{{raw:jsonld}}
</script>
```

- **Archivo:** `005-plantillaSEO.html`
- **Líneas:** 7-9 (meta SEO), 19-27 (Open Graph), 29-33 (Twitter), 43-46 (JSON-LD)
- **Ruta:** `005-plantillaSEO.html`

### 6. Hojas de estilo CSS (generadas por IA)

El proyecto incluye 4 hojas de estilo CSS diferentes, presumiblemente generadas por distintas IAs (ChatGPT, Claude, Mistral y una genérica). Todas siguen la misma estructura de variables CSS, sistema de grid, y componentes, pero con diferentes valores de radio de borde, sombras y proporciones.

```css
:root{
  --bg: #ffffff;
  --bg-soft: #f2f4f4;
  --text: #1b1f23;
  --orange: #f39a1a;
  --radius: 10px;
  --container: 1120px;
}
```

- **Archivo:** `estilochatgpt.css` (500 líneas, diseño principal usado por 005)
- **Líneas:** 1-22 (variables CSS)
- **Ruta:** `estilochatgpt.css`, `estiloclaude.css`, `estilomistral.css`, `estilo.css`

### 7. Datos del contenido en JSON

Todo el contenido textual de la web se almacena en un archivo JSON independiente: títulos, textos, URLs, metadatos SEO, datos de contacto, redes sociales y el bloque JSON-LD de datos estructurados. Esto permite cambiar el contenido sin tocar el HTML.

```json
{
  "titulo1": "Curso IA en Directo",
  "titulo2": "Programación · Streaming · Práctico",
  "heroetitulo": "IA para Programadores, en Directo: aprende creando proyectos reales.",
  "meta_description": "Curso online de IA para programadores en streaming...",
  "raw:jsonld": "{...Schema.org Course...}"
}
```

- **Archivo:** `datos.json`
- **Líneas:** 1-10 (cabecera), 42-50 (héroe), 120-140 (JSON-LD)
- **Ruta:** `datos.json`

### 8. Motor de plantillas PHP (index.php)

El archivo PHP carga la plantilla HTML y el JSON, y reemplaza todos los `{{placeholders}}` por el contenido real. Incluye: enrutador para robots.txt y sitemap.xml, compresión gzip, cabeceras de caché con ETag, y un sistema de reemplazo que escapa HTML por defecto (seguridad contra XSS) excepto para las claves que empiezan por `raw:`.

```php
$template = file_get_contents($templateFile);
$data = json_decode($raw, true);
$out = apply_placeholders($template, $data);

function apply_placeholders(string $template, array $data): string {
  foreach ($data as $key => $value) {
    if (str_starts_with($k, 'raw:')) {
      $template = str_replace($needle, $v, $template);
    } else {
      $template = str_replace($needle, e($v), $template);
    }
  }
  return $template;
}
```

- **Archivo:** `index.php`
- **Líneas:** 65-96 (carga de archivos), 107-120 (reemplazo), 130-139 (funciones helper)
- **Ruta:** `index.php`

### 9. Mejoras aplicadas por el alumno

Se han aplicado mejoras mixtas en varios lenguajes y capas:

- **HTML (002):** Corregido el cierre del form roto (`</form` → `</form>`) y el id duplicado `destacado8` → `destacado9`.
- **CSS:** Añadido `scroll-behavior:smooth` en `html` para navegación suave entre secciones; transiciones CSS en los enlaces del `nav` y el botón CTA.
- **PHP:** Añadidas cabeceras de seguridad `X-Content-Type-Options: nosniff` y `X-Frame-Options: SAMEORIGIN`.
- **HTML/SEO (005):** Uso de entidad HTML `&mdash;` en el footer para el guión largo.
- **JS (005):** Validación básica del formulario de contacto con `confirm()` antes de enviar y comprobación de campos vacíos.

- **Archivos:** `002-web estatica.html` (L94-101), `estilochatgpt.css` (L25, L107, L120), `index.php` (L53-56), `005-plantillaSEO.html` (L315-340)
- **Ruta:** Raíz del proyecto

## Presentación del proyecto

Este proyecto demuestra cómo se construye paso a paso una web promocional para un curso de Inteligencia Artificial, pensada para convertir visitantes en alumnos inscritos.

![Sección destacada de la web](img/destacado2.png)

La web final tiene la siguiente estructura:

1. **Cabecera** con logo, nombre del curso ("Curso IA en Directo") y barra de navegación con 5 enlaces internos, incluyendo un botón CTA destacado de "Inscripción".
2. **Sección héroe** con el título principal, una descripción del curso y un botón de acción que invita a reservar plaza.
3. **9 secciones destacadas** que presentan las ventajas del curso: talleres en vivo, enfoque profesional, proyectos end-to-end, temario, comparativa con otros formatos, llamadas a la acción intermedias, etc.
4. **Formulario de contacto** con campos de nombre, email y mensaje, acompañado de datos de contacto y redes sociales.
5. **Pie de página** con copyright y enlaces a política de privacidad y términos de uso.

![Imagen de proyecto destacado](img/destacado4.png)

Lo más interesante del proyecto es su arquitectura de plantillas: el HTML contiene placeholders `{{clave}}` que PHP sustituye en tiempo real por el contenido del JSON. Esto permite:

- Cambiar todo el contenido textual sin tocar el HTML.
- Comparar distintas hojas de estilo CSS (se incluyen 4 versiones generadas por diferentes IAs) simplemente cambiando una línea del `<link>`.
- Mantener el SEO separado en metadatos JSON, incluyendo datos estructurados Schema.org (JSON-LD).

La versión más avanzada (005-plantillaSEO.html) cumple con todas las buenas prácticas de SEO: meta description, Open Graph, Twitter Cards, canonical URL, robots, JSON-LD con esquema Course, skip-link de accesibilidad, y optimización de imágenes con `loading="lazy"` y `decoding="async"`.

## Conclusión

Este proyecto es un ejemplo completo de cómo construir una landing page profesional de forma progresiva, aplicando buenas prácticas de desarrollo web moderno. Desde una estructura HTML semántica con placeholders hasta un sistema de plantillas PHP con SEO avanzado, el proyecto cubre todas las capas del desarrollo frontend y backend de una web promocional.

Las mejoras aplicadas (corrección de HTML roto, transiciones CSS, cabeceras de seguridad HTTP, validación JS del formulario) demuestran comprensión de las diferentes capas del desarrollo web y la importancia de la calidad en cada una de ellas. La arquitectura de separar contenido (JSON), presentación (CSS) y estructura (HTML) permite mantener y escalar el proyecto con facilidad, y es un patrón aplicable a cualquier web empresarial.
