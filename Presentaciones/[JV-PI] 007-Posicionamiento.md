# recortabl.es — Tienda de recortables infantiles con SEO y panel de administración

![PHP](https://img.shields.io/badge/PHP-8.x-blue)
![SQLite](https://img.shields.io/badge/SQLite-3-green)
![SEO](https://img.shields.io/badge/SEO-Schema.org+OpenGraph-orange)

> 🔗 **GitHub Pages:** [https://mutenros.github.io/Proyecto-intermodular-007-posicionamiento/](https://mutenros.github.io/Proyecto-intermodular-007-posicionamiento/)

## Introducción

Este proyecto es una tienda online de recortables infantiles en PDF llamada **recortabl.es**. Permite explorar un catálogo de productos por categorías, ver detalles de cada recortable, descargar PDFs, registrarse, iniciar sesión y contactar. Además, incluye un panel de administración completo (CRUD de categorías y productos) y un sistema de SEO avanzado con Open Graph, JSON-LD Schema.org, canonical URLs, sitemap.xml dinámico y logging de visitas. Todo ello usando PHP con SQLite como base de datos y un diseño visual limpio y responsive.

## Desarrollo de las partes

### 1. Sistema SEO en cabecera PHP

Cada página define un array `$SEO` con título, descripción, tipo Open Graph e imagen antes del include de la cabecera. La cabecera genera automáticamente todas las meta tags necesarias para posicionamiento.

```php
// Archivo: 002-admin/inc/cabecera.php, líneas 1-100
$SEO = [
  "title" => "Recortables para imprimir | Juguetes de papel en PDF – recortabl.es",
  "description" => "Recortables infantiles y educativos en PDF...",
  "og_type" => "website",
];
```

La cabecera calcula automáticamente la URL canónica (`$canonical`), genera metatags Open Graph (`og:title`, `og:description`, `og:url`, `og:image`), Twitter Card, robots, hreflang y JSON-LD (WebSite + Organization). Usa la función `seo_e()` como wrapper de `htmlspecialchars` para escapar todos los valores en atributos HTML.

### 2. JSON-LD Schema.org para productos

En la página de detalle de producto, se genera un bloque JSON-LD de tipo `Product` con datos estructurados: nombre, imagen, marca, categoría y oferta con precio y disponibilidad.

```php
// Archivo: 002-admin/producto.php, líneas 1-30
$SEO = [
  "jsonld" => [
    "@context" => "https://schema.org",
    "@type" => "Product",
    "name" => $titulo,
    "brand" => [ "@type" => "Brand", "name" => "recortabl.es" ],
    "offers" => [
      "@type" => "Offer",
      "price" => "0.00",
      "priceCurrency" => "EUR",
      "availability" => "https://schema.org/InStock"
    ]
  ]
];
```

Esto permite que Google muestre rich snippets de producto en los resultados de búsqueda.

### 3. Sitemap XML dinámico con caché

El archivo `sitemap.php` se incluye silenciosamente en el footer y genera/actualiza `sitemap.xml` automáticamente. Usa un sistema de caché con fingerprint de la base de datos.

```php
// Archivo: 002-admin/sitemap.php, líneas 1-160
$fingerprint = hash('sha256', $prodCount.'|'.$catCount.'|'.$prodMaxId.'|'.$catMaxId);
// Compara con caché anterior → solo regenera si hay cambios
// Incluye URLs estáticas con prioridad + categorías + productos dinámicos
```

El sitemap incluye URLs estáticas (index, catálogo, contacto…) con prioridades configuradas, más todas las categorías y productos dinámicos desde SQLite. Se usa escritura atómica con `rename()` para evitar corrupciones.

### 4. Sistema de logging de visitas

El archivo `log.php` registra cada visita en la tabla `logs` de SQLite con información detallada: IP (con soporte de proxies como Cloudflare), user-agent, referer, método HTTP, path, query string, cabeceras completas y cookies hasheadas.

```php
// Archivo: 002-admin/log.php, líneas 1-100
function _log_client_ip(array $headers): string {
  $candidates = ['CF-Connecting-IP', 'True-Client-IP', 'X-Real-IP', 'X-Forwarded-For'];
  foreach ($candidates as $h) {
    // Busca IP real detrás de proxies/CDN
  }
  return (string)($_SERVER['REMOTE_ADDR'] ?? '');
}
```

Los valores de cookies se almacenan hasheados con SHA-256 para no guardar datos sensibles en claro.

### 5. Catálogo con búsqueda y filtros

La página `catalogo.php` muestra todos los productos con un sidebar de filtros (búsqueda, categoría, dificultad, valoración, checkboxes) y toolbar de ordenación. La búsqueda usa prepared statements para evitar SQL injection.

```php
// Archivo: 002-admin/catalogo.php, líneas 80-93
$stmt = $db->prepare("SELECT * FROM productos WHERE titulo LIKE :buscar");
$stmt->bindValue(':buscar', '%'.$_POST['buscar'].'%', SQLITE3_TEXT);
$resultado = $stmt->execute();
```

Los resultados se muestran en un grid responsive de 4 columnas que se adapta a 3, 2 y 1 columna según el viewport.

### 6. Página de producto con detalle completo

La página `producto.php` muestra la ficha completa del recortable: galería de imágenes, título, categoría, metadatos (dificultad, páginas, valoración), botones de descarga, descripción, qué incluye y consejos de impresión. También muestra recortables similares aleatorios.

```php
// Archivo: 002-admin/producto.php, líneas 35-65
$stmt = $db->prepare("SELECT ... FROM productos LEFT JOIN categorias ... WHERE productos.Identificador = :id");
$stmt->bindValue(':id', (int)$_GET['id'], SQLITE3_INTEGER);
// Migas de pan, galería con thumbnails, botones CTA, sección de similares (ORDER BY RANDOM() LIMIT 4)
```

### 7. Panel de administración (CRUD)

El archivo `admin/admin.php` implementa un panel completo con login seguro (password_hash + password_verify), CSRF, y CRUD de categorías y productos usando PDO con prepared statements.

```php
// Archivo: 002-admin/admin/admin.php, líneas 130-170
// Login con session_regenerate_id para evitar session fixation
if ($user && password_verify($password, (string)$user['password_hash'])) {
  session_regenerate_id(true);
  $_SESSION['admin_user_id'] = (int)$user['id'];
}
```

El panel tiene sidebar con navegación, sección de categorías (lista + formulario crear/editar + borrado con protección referencial), productos (CRUD completo con categoría asociada) y analítica de logs (KPIs, páginas vistas, IPs únicas).

### 8. Autenticación de usuarios (registro + login)

La web pública tiene sistema de registro y login con CSRF token, validación de email, `password_hash`, `password_verify` y `session_regenerate_id`.

```php
// Archivo: 002-admin/auth_login.php, líneas 1-55
if (empty($_POST['csrf']) || !hash_equals($_SESSION['csrf'], (string)$_POST['csrf'])) {
  redirect_with('Sesión caducada.');
}
// Valida email con filter_var, verifica password con password_verify
// Regenera session ID tras login exitoso
```

El registro (`auth_signup.php`) valida nombre, email único, contraseña mínima de 7 caracteres, repetición de contraseña y aceptación de términos.

### 9. Mejoras aplicadas

Se aplicaron las siguientes mejoras al código original:

- **Prepared statements** en `catalogo.php` y `producto.php` para eliminar vulnerabilidades de SQL injection por concatenación directa
- **`htmlspecialchars`** en las salidas de `index.php` (categorías y productos) y `catalogo.php` para prevenir XSS
- **`alt` descriptivos** en imágenes: cada `<img>` ahora incluye el título del producto/categoría en el atributo `alt`
- **CSS transitions** en botones (`.btn`): `transform .2s` + `:hover translateY(-2px)` + `:active translateY(0)`
- **CSS transitions** en cards de catálogo y productos: hover con `translateY(-4px)` y sombra más intensa

## Presentación del proyecto

recortabl.es es una tienda online de recortables infantiles donde los usuarios pueden navegar por categorías, buscar productos, ver fichas detalladas y descargar PDFs. El proyecto está pensado para familias y educadores que buscan actividades manuales accesibles.

Lo que distingue este proyecto es su enfoque en el posicionamiento web: cada página genera automáticamente meta tags Open Graph, Twitter Card, URL canónica, hreflang y datos estructurados JSON-LD de Schema.org. El sitemap XML se regenera dinámicamente cuando cambian los datos. Además, se registra cada visita con un sistema de logging completo.

El panel de administración permite gestionar categorías y productos sin tocar código, con autenticación segura y protección CSRF. La interfaz es responsive y usa un diseño visual consistente con variables CSS y un grid system propio.

## Conclusión

Este proyecto integra múltiples aspectos del desarrollo web: frontend responsive con CSS Grid, backend PHP con SQLite, autenticación segura con hash de contraseñas y CSRF, SEO técnico con Schema.org y sitemap dinámico, y un panel de administración CRUD completo. Las mejoras aplicadas refuerzan la seguridad (prepared statements, htmlspecialchars) y la experiencia de usuario (transitions, alt texts descriptivos), demostrando buenas prácticas de desarrollo web en un proyecto real y funcional.
