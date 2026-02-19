# Recuperación de emails con IMAP

![Blog de correos con PHP e IMAP](https://img.shields.io/badge/PHP-IMAP-777BB4?style=for-the-badge&logo=php&logoColor=white)

> 🔗 **GitHub Pages:** [https://mutenros.github.io/Entornos-003-Recuperacin-de-emails-con-IMAP/](https://mutenros.github.io/Entornos-003-Recuperacin-de-emails-con-IMAP/)

## Introducción

Este proyecto convierte una bandeja de correo electrónico en un blog personal completamente funcional. Utilizando PHP y la extensión IMAP, nos conectamos a un servidor de correo real (IONOS) y presentamos cada mensaje como una entrada de blog moderna, con imágenes destacadas, extractos, vista de detalle y enlaces a redes sociales. El resultado es una aplicación web dinámica que demuestra cómo aplicar protocolos de red clásicos (IMAP) para construir interfaces actuales con HTML5 y CSS3.

## Desarrollo de las partes

### 1. Fundamentos: POP3 frente a IMAP

**Archivo:** `101-Ejercicios/001-Introduccion.md`

El punto de partida teórico distingue los dos protocolos principales de acceso al correo:

- **POP3** descarga los mensajes al cliente y (opcionalmente) los borra del servidor.
- **IMAP** trabaja directamente sobre el servidor, permitiendo leer sin descargar ni eliminar.

Esta diferencia justifica la elección de IMAP: necesitamos leer los correos repetidamente cada vez que se carga la página, sin modificar la bandeja.

### 2. Conexión IMAP y decodificación de contenido

**Archivo:** `101-Ejercicios/002-leercorreos.php` · **Líneas clave:** 1-26

```php
$hostname = '{imap.ionos.es:993/imap/ssl}INBOX';
$username = 'python@jocarsa.com';
$password = 'TAME123$';

function decodePart($content, $encoding) {
    switch ($encoding) {
        case 3: return base64_decode($content);       // BASE64
        case 4: return quoted_printable_decode($content); // QUOTED-PRINTABLE
        default: return $content;
    }
}
```

La cadena de conexión especifica el servidor, el puerto **993** (IMAPS con SSL), y el buzón INBOX. La función `decodePart()` resuelve las dos codificaciones de transferencia más frecuentes en correos: BASE64 y QUOTED-PRINTABLE. Los mensajes se obtienen con `imap_open()`, `imap_search()` e `imap_fetch_overview()`.

### 3. Recorrido recursivo de partes MIME

**Archivo:** `101-Ejercicios/007-vinculos.php` · **Líneas:** 40-140

```php
function extractEmailParts($imap, $msgno) {
    $structure = imap_fetchstructure($imap, $msgno);
    $result = ['html' => null, 'text' => null, 'image' => null];
    // ...
    traverseParts($imap, $msgno, $structure, '', $result);
    return $result;
}

function traverseParts($imap, $msgno, $structure, $prefix, &$result) {
    foreach ($structure->parts as $idx => $part) {
        // Tipo 0 = texto, Tipo 5 = imagen
        // Recursión para multipart anidado
    }
}
```

Los correos modernos son **multipart**: contienen texto plano, HTML e imágenes como partes separadas. `extractEmailParts()` devuelve un array con las tres variantes. `traverseParts()` recorre recursivamente la estructura MIME usando `imap_fetchbody()` y extrae la primera imagen como **data URI** en base64 para usarla como imagen destacada del post.

### 4. Generación de extractos y vista detalle

**Archivo:** `101-Ejercicios/007-vinculos.php` · **Líneas:** 157-196

```php
define('EXCERPT_LENGTH', 400);

function makeExcerpt($html, $length = EXCERPT_LENGTH) {
    $text = trim(preg_replace('/\s+/', ' ', strip_tags($html)));
    if (function_exists('mb_strlen') && function_exists('mb_substr')) {
        return mb_strlen($text) <= $length ? $text : mb_substr($text, 0, $length) . '…';
    }
    return strlen($text) <= $length ? $text : substr($text, 0, $length) . '…';
}

$selectedId = isset($_GET['id']) ? (int)$_GET['id'] : null;
```

La portada muestra un resumen de 400 caracteres de cada correo. Al pulsar "Leer más →", el parámetro `?id=NNN` activa la **vista detalle** donde se renderiza el cuerpo HTML completo del mensaje. El casting `(int)` protege contra inyección de parámetros.

### 5. Diseño CSS con custom properties

**Archivo:** `101-Ejercicios/007-vinculos.php` · **Líneas:** 209-310

```css
:root {
    --bg: #f4f4f5;
    --bg-card: #ffffff;
    --border: #e4e4e7;
    --text: #18181b;
    --muted: #71717a;
    --accent: #2563eb;
}

article.post {
    background: var(--bg-card);
    border-radius: 16px;
    border: 1px solid var(--border);
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
}
```

Todo el tema visual se controla desde **6 custom properties** en `:root`. Las tarjetas usan `border-radius: 16px` y sombras sutiles. La imagen destacada tiene efecto `scale(1.03)` al pasar el ratón. La tipografía usa `system-ui` para coincidir con la fuente nativa del sistema operativo.

### 6. Cabecera personalizada con enlaces sociales

**Archivo:** `101-Ejercicios/007-vinculos.php` · **Líneas:** 236-422

```html
<header class="site-header">
  <div class="corporativo">
    <h1 class="site-title">Jose Vicente Carratala Sanchis</h1>
    <p class="site-subtitle">Programador, profesor y diseñador…</p>
  </div>
  <div class="social">
    <a href="https://facebook.com/carratala" title="Facebook">
      <img src="logos/facebook.png" alt="Facebook">
    </a>
    <!-- instagram, email, github, home, linkedin, whatsapp, youtube -->
  </div>
</header>
```

El header usa **flexbox** con `justify-content: space-between` para separar la identidad corporativa de los iconos sociales. Los iconos (35 px) tienen transición `transform 0.2s` y `opacity 0.2s` en hover. Cada enlace incluye atributos `title` y `alt` para accesibilidad.

### 7. Adaptación móvil y mejoras de accesibilidad

**Archivo:** `101-Ejercicios/007-vinculos.php` · **Líneas:** 205, 377-402

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
```

```css
@media (max-width: 640px) {
    .layout { padding-inline: 1rem; }
    header.site-header {
        flex-direction: column;
        text-align: center;
        gap: 1rem;
    }
}
```

La media query a 640 px reorganiza la cabecera en columna y centra el contenido. El meta viewport asegura que el navegador móvil no escale la página. Se añadió un **footer** con créditos (`footer.site-footer`) y atributos `alt` descriptivos en todos los iconos de redes sociales.

### 8. Evolución progresiva del proyecto

| Fase | Archivo | Funcionalidad añadida |
|------|---------|-----------------------|
| 1 | `001-Introduccion.md` | Teoría POP3 vs IMAP |
| 2 | `002-leercorreos.php` | Lectura básica de 20 correos |
| 3 | `003-correos como blog.php` | Diseño blog, imágenes, CSS moderno |
| 4 | `004-leer correos con mejoras.php` | Extractos y vista detalle |
| 5 | `005-personalizar.php` | Cabecera personalizada |
| 6 | `006-version movil.php` | Soporte responsive |
| 7 | `007-vinculos.php` | Enlaces sociales con iconos |

Cada fase incorpora todo lo anterior y añade una funcionalidad nueva, demostrando un flujo de desarrollo **incremental** real.

## Presentación del proyecto

El proyecto final es una aplicación PHP que se ejecuta en cualquier servidor con la extensión IMAP habilitada. Al acceder a `007-vinculos.php` desde un navegador, la página se conecta al servidor de correo IONOS y presenta los 15 mensajes más recientes como tarjetas de blog.

Cada tarjeta muestra:
- La **imagen destacada** extraída del correo (primer adjunto de tipo imagen)
- El **asunto** como título enlazable
- El **remitente** y la **fecha**
- Un **extracto** de 400 caracteres del contenido

Al pulsar "Leer más →", se abre la vista completa del mensaje con todo el HTML original renderizado. La cabecera incluye el nombre del autor, su descripción profesional y 8 iconos de redes sociales con enlaces directos.

El diseño es completamente responsive: en móvil la cabecera se reorganiza en columna, los iconos se centran y el contenido se adapta a pantallas pequeñas. No se utiliza JavaScript — toda la lógica se ejecuta en el servidor con PHP.

## Conclusión

Este proyecto demuestra cómo un protocolo de los años 80 (IMAP, RFC 3501) puede alimentar una interfaz moderna y atractiva. La combinación de PHP para la lógica de servidor, IMAP para la obtención de datos y CSS3 con custom properties para la presentación resulta en una solución completa sin dependencias externas ni frameworks.

Los puntos más destacados del desarrollo han sido:
- El **recorrido recursivo de partes MIME** para extraer contenido y adjuntos
- La **codificación segura** con `htmlspecialchars` y casting de tipos para prevenir XSS y parámetros maliciosos
- El **diseño progresivo** en 7 fases que refleja un ciclo real de desarrollo iterativo
- La **accesibilidad** con atributos `alt`, `title` y adaptación responsive

El resultado final es un blog funcional alimentado directamente por una bandeja de entrada, listo para desplegarse en cualquier hosting PHP con soporte IMAP.
