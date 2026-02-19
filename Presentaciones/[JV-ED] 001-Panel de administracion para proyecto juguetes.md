# Panel de Administración para Proyecto Juguetes — recortabl.es

![Vista principal de recortabl.es — Hero con categorías y recortables destacados](docs/img/screenshot-index.png)

> 🔗 **GitHub Pages:** [https://mutenros.github.io/Entornos-001-Panel-de-administracin-para-proyecto-juguetes/](https://mutenros.github.io/Entornos-001-Panel-de-administracin-para-proyecto-juguetes/)

## Introducción

Este proyecto es una **tienda web de recortables de papel** construida con PHP y SQLite. Permite a los usuarios explorar un catálogo de juguetes recortables para imprimir, filtrar por categoría, ver fichas de producto detalladas, registrarse e iniciar sesión, y contactar con la tienda. Además, incluye un **panel de administración** completo con CRUD de categorías y productos. El proyecto pasó por 2 fases: un primer panel de administración básico y luego la adición del sistema de registro de usuarios con autenticación segura (password_hash, CSRF, session_regenerate_id).

---

## Desarrollo de las partes

### 1. Cabecera y estructura HTML — Navegación compartida

Todas las páginas incluyen una cabecera común mediante `include`. La cabecera contiene el logo de la marca, la navegación principal con enlaces a categorías, "sobre nosotros", descargas y login, y un buscador integrado con formulario POST.

- **Archivo:** `002-Creación de registros/inc/cabecera.php` — **Líneas 1–47**
  ```php
  <a class="brand" href="index.php">
    <div class="logo">🤖</div>
    <span><b>rec</b><i>ortabl.es</i></span>
  </a>
  ```
- La búsqueda envía por POST a `catalogo.php` (línea 37): `<form action="catalogo.php" method="POST">`
- **Mejora aplicada** (líneas 6–7): se añadió `<meta name="description">` para SEO y un título más descriptivo.

---

### 2. Página principal — Categorías dinámicas desde SQLite

La página `index.php` muestra un hero, las categorías obtenidas de la base de datos, recortables destacados (estáticos), una galería y una sección informativa.

- **Archivo:** `002-Creación de registros/index.php` — **Líneas 1–113**
- Consulta de categorías (líneas 30–35):
  ```php
  $db = new SQLite3('recortables.db');
  $peticion = "SELECT * FROM categorias";
  $resultado = $db->query($peticion);
  ```
- **Mejora aplicada** (línea 37): se añadió `htmlspecialchars` en la imagen y el título de cada categoría, y un `alt` descriptivo:
  ```php
  <img src="<?= htmlspecialchars($fila['imagen'], ENT_QUOTES, 'UTF-8') ?>"
       alt="<?= htmlspecialchars($fila['titulo'], ENT_QUOTES, 'UTF-8') ?>">
  ```

---

### 3. Catálogo con búsqueda — Prepared statement contra SQL injection

El catálogo muestra todos los productos y permite buscar por título. Incluye un **aside** con filtros (categoría, dificultad, valoración) y una grilla de tarjetas con paginación.

- **Archivo:** `002-Creación de registros/catalogo.php` — **Líneas 81–104**
- **Vulnerabilidad original** (corregida): la búsqueda concatenaba directamente la entrada del usuario en la SQL, permitiendo inyección SQL.
- **Mejora aplicada** (líneas 88–91): prepared statement con `bindValue`:
  ```php
  $stmt = $db->prepare("SELECT * FROM productos WHERE titulo LIKE :buscar");
  $stmt->bindValue(':buscar', '%'.$_POST['buscar'].'%', SQLITE3_TEXT);
  $resultado = $stmt->execute();
  ```
- También se aplica `htmlspecialchars` al título del producto (línea 97).

---

### 4. Ficha de producto — JOIN SQL y detalle completo

La página de producto muestra la imagen, título, categoría, descripción, botones de descarga e instrucciones, y una sección de "recortables similares" con consulta aleatoria.

- **Archivo:** `002-Creación de registros/producto.php` — **Líneas 12–30**
- Consulta con LEFT JOIN entre `productos` y `categorias` (líneas 14–23):
  ```sql
  SELECT productos.titulo AS tituloproducto,
         categorias.titulo AS categoriaproducto,
         productos.imagen AS imagenproducto,
         productos.descripcion AS descripcionproducto
  FROM productos LEFT JOIN categorias
  ON productos.categoria = categorias.Identificador
  WHERE productos.Identificador = :id
  ```
- **Mejora aplicada** (línea 24): el `$_GET['id']` se pasa como parámetro con `bindValue` en vez de concatenar directamente.
- **Mejora XSS** (líneas 42, 46, 63): todos los datos del producto se escapan con `htmlspecialchars`.
- Recortables similares con `ORDER BY RANDOM() LIMIT 4` (líneas 92–108).

---

### 5. Sistema de login y registro — Autenticación segura

El sistema de autenticación usa `password_hash` / `password_verify`, tokens CSRF, validación de email con `filter_var`, y `session_regenerate_id`.

- **Login**: `002-Creación de registros/login.php` — **Líneas 1–97**
  - CSRF token generado con `bin2hex(random_bytes(16))` (línea 11)
  - Función `e()` como alias de `htmlspecialchars` (línea 8)
  - Formulario con `type="email"` y `required` para validación HTML5

- **Auth Login**: `002-Creación de registros/auth_login.php` — **Líneas 1–60**
  - Verifica CSRF con `hash_equals` (línea 15)
  - `password_verify` para comparar contra el hash almacenado (línea 42)
  - `session_regenerate_id(true)` al logear (línea 44)

- **Auth Signup**: `002-Creación de registros/auth_signup.php` — **Líneas 1–77**
  - Validación completa: nombre (2–40 chars), email, contraseña (mín. 8), coincidencia, términos
  - `password_hash($pass, PASSWORD_DEFAULT)` (línea 53)
  - Auto-login tras registro con `session_regenerate_id(true)` (línea 62)

---

### 6. Panel de administración — CRUD de categorías y productos

Panel con login propio, sidebar de navegación, y tablas CRUD para gestionar categorías y productos.

- **Archivo:** `002-Creación de registros/admin/admin.php` — **Líneas 1–123**
- Crea usuario admin `jocarsa` si no existe (líneas 8–16)
- Login con PDO + `password_verify` (líneas 22–37)
- CRUD de categorías: listado en tabla, formulario para añadir (líneas 91–103)
- CRUD de productos: listado con todos los campos, formulario completo (líneas 105–121)
- **Mejoras aplicadas**:
  - `session_regenerate_id(true)` al hacer login (línea 30)
  - Prepared statement en INSERT de categorías (líneas 51–52)
  - `htmlspecialchars` en todas las celdas de la tabla (líneas 98–102, 112–120)
  - `onclick="return confirm('¿Borrar?')"` en enlaces de borrado (líneas 102, 120)

---

### 7. CSS extensivo — 847 líneas de diseño moderno

La hoja de estilos cubre toda la web: header sticky, hero con gradientes y wave SVG, grids responsivos, tarjetas con sombras, filtros del catálogo, ficha de producto, formularios y footer.

- **Archivo:** `002-Creación de registros/estilo/estilo.css` — **847 líneas**
- Custom properties / tokens de diseño (líneas 5–13):
  ```css
  :root{
    --bg: #eef5fb; --ink: #0b2a45; --brand: #2a84d8;
    --card:#ffffff; --shadow: 0 10px 22px rgba(11,42,69,.10);
  }
  ```
- Hero con gradientes y clip-path (líneas 120–165)
- Grid de categorías 7 columnas → 4 → 2 → 1 (responsive, líneas 226, 728, 743)
- Grid del catálogo con sidebar sticky (líneas 395–420)
- **Mejoras aplicadas**:
  - `transition` en nav links (línea 80), botones download (línea 292) y tarjetas article (línea 480)
  - Efecto hover `translateY` en tarjetas (líneas 482–485) y botones (líneas 294–296)
  - Responsive completo en 4 breakpoints: 1100px, 820px, 640px, 520px

---

### 8. Log de visitas — Registro automático de tráfico

El archivo `log.php` se incluye al final del footer y registra cada visita en la base de datos SQLite: IP, user-agent, URL, método HTTP, headers y timestamp.

- **Archivo:** `002-Creación de registros/log.php` — **192 líneas**
- Detección de IP real con soporte para proxies: CF-Connecting-IP, X-Real-IP, X-Forwarded-For (líneas 35–51)
- Tabla `log_visitas` creada automáticamente si no existe
- Registro con prepared statements para seguridad

---

## Presentación del proyecto

Este proyecto es una tienda web completa de recortables de papel llamada **recortabl.es**. Los usuarios pueden navegar por un catálogo de recortables organizados por categorías, buscar por nombre, ver fichas detalladas con descripción e instrucciones de montaje, y descargar los PDFs. También pueden registrarse y hacer login con un sistema de autenticación seguro.

El proyecto incluye un panel de administración donde se pueden añadir, editar y borrar categorías y productos. Todo funciona sobre PHP con SQLite como base de datos, sin necesidad de MySQL ni configuración compleja.

El diseño visual es moderno y amigable, con una estética infantil/artesanal usando la fuente Delius, colores azules pastel, tarjetas con sombras suaves y un hero llamativo con gradientes. Es completamente responsive y se adapta a móviles.

El proyecto evolucionó en dos fases: primero el panel de administración y la web de catálogo, después el sistema completo de registro de usuarios con seguridad (password_hash, CSRF, validaciones).

---

## Conclusión

Con este proyecto hemos aprendido a:

- **Crear una aplicación web completa** con PHP y SQLite: catálogo, búsqueda, detalle de producto, autenticación y panel de administración.
- **Implementar autenticación segura**: `password_hash`, `password_verify`, tokens CSRF, `session_regenerate_id`, validación de email con `filter_var`.
- **Prevenir SQL injection** con prepared statements y `bindValue` en SQLite3.
- **Evitar XSS** con `htmlspecialchars` en toda salida de datos.
- **Diseñar interfaces responsive** con CSS Grid, custom properties, gradientes, clip-path y 4 breakpoints.
- **Registrar visitas** de forma automática y segura con un sistema de logging propio.

El resultado es una tienda de recortables funcional, segura y visualmente atractiva que demuestra conocimientos sólidos de desarrollo web full-stack con tecnologías de primer curso.
