# Web con panel de control — CMS JocarsaPress

![JocarsaPress](docs/img/banner.png)

## Introducción

Este proyecto construye un CMS (sistema de gestión de contenidos) completo desde cero usando PHP y MySQL. La web pública muestra una página personal con navegación dinámica y un blog con entradas en Markdown que se renderizan a HTML. El panel de administración permite crear, editar y eliminar tanto páginas como entradas del blog. Todo el estilo se genera con un framework CSS propio llamado JVestilo que crea miles de clases de utilidad desde PHP.

## Desarrollo de las partes

### 1. Estructura HTML y CSS framework propio (JVestilo)

JVestilo es un framework CSS generado dinámicamente por PHP. Recorre arrays de colores, tamaños y familias tipográficas para generar clases de utilidad como `.b-teal`, `.p-20`, `.flex`, `.fd-column`, etc.

- **Archivo:** `002-empezamos a atar/JVestilo/JVestilo.php`, líneas 1–80
- **Ruta:** `002-empezamos a atar/JVestilo/JVestilo.php`

```php
foreach($colores as $color){
    echo ".b-".strtolower($color)."{background:".strtolower($color).";}";
    echo ".c-".strtolower($color)."{color:".strtolower($color).";}";
}
for($i = 0;$i<2000;$i++){
    echo ".p-".$i."{padding:".$i."px;}";
    echo ".m-".$i."{margin:".$i."px;}";
    echo ".w-".$i."{width:".$i."px;}";
    // ... width%, height, font-size, gap, border-radius, flex
}
```

Genera más de 150 colores CSS nombrados, 2000 niveles de padding/margin/width/height, utilidades flex/grid, alineaciones de texto y estilos de borde combinatorios.

### 2. CSS personalizado con variables

Un archivo CSS adicional define variables de diseño (color corporativo teal, superficies, texto) y estilos específicos para la web: botones, badges, tarjetas Markdown.

- **Archivo:** `002-empezamos a atar/estilo/estilo.css`, líneas 1–50
- **Ruta:** `002-empezamos a atar/estilo/estilo.css`

```css
:root{
  --brand:#0f766e;
  --brand-soft:#d1faf5;
  --bg:#f6f7fb;
  --surface:#f1f5f9;
  --text:#0f172a;
  --muted:#64748b;
}
.btn{ display:inline-block; padding:10px 12px; border-radius:12px;
      text-decoration:none; font-size:12px;
      transition: border-color 0.2s, color 0.2s, background 0.2s; }
```

### 3. Renderizador Markdown → HTML

La función `markdown_to_html()` convierte texto Markdown almacenado en la base de datos a HTML seguro. Soporta headings, listas, bloques de código, blockquotes, negrita, cursiva, links y código inline.

- **Archivo:** `002-empezamos a atar/index.php`, líneas 8–130
- **Ruta:** `002-empezamos a atar/index.php`

```php
function markdown_to_html($md){
    $lines = explode("\n", $md);
    // Headings #, ##, ###
    if (preg_match('/^(#{1,6})\s+(.*)$/', $line, $m)) {
        $lvl = strlen($m[1]);
        $html .= "<h$lvl>$txt</h$lvl>\n";
    }
    // Listas, bloques de código, blockquotes...
    // Sanitizado final con strip_tags y tags permitidos
    $allowed = '<p><br><h1><h2><h3><ul><ol><li><strong><em><code><pre><a><blockquote>';
    $html = strip_tags($html, $allowed);
}
```

Incluye `htmlspecialchars()` para prevenir XSS y `strip_tags()` como sanitizado final.

### 4. Web pública con navegación dinámica

La página principal carga las páginas existentes desde MySQL y crea automáticamente el menú de navegación. El parámetro `?p=` selecciona la página o el blog.

- **Archivo:** `002-empezamos a atar/index.php`, líneas 152–248
- **Ruta:** `002-empezamos a atar/index.php`

```php
<nav class="flex g-10 fa-center fw-wrap">
    <a href="?" class="btn btn-ghost">Inicio</a>
    <?php
      $r = $c->query("SELECT * FROM paginas ORDER BY Identificador ASC;");
      while($f = $r->fetch_assoc()){
    ?>
      <a href="?p=<?= urlencode($f['titulo']) ?>" class="btn btn-ghost">
        <?= htmlspecialchars($f['titulo']) ?>
      </a>
    <?php } ?>
    <a href="?p=blog" class="btn btn-brand">Blog</a>
</nav>
```

### 5. Blog con entradas en Markdown

Las entradas del blog se muestran en una rejilla de 3 columnas. Cada entrada contiene título, fecha y contenido renderizado desde Markdown.

- **Archivo:** `002-empezamos a atar/index.php`, líneas 206–224
- **Ruta:** `002-empezamos a atar/index.php`

```php
$r = $c->query("SELECT * FROM entradas ORDER BY fecha DESC;");
while($f = $r->fetch_assoc()){
    $contenido_html = markdown_to_html($f['contenido']);
?>
  <article class="b-surface p-16 bradius-16 flex fd-column g-10">
    <h3><?= htmlspecialchars($f['titulo']) ?></h3>
    <time><?= htmlspecialchars($f['fecha']) ?></time>
    <div class="markdown"><?= $contenido_html ?></div>
  </article>
```

### 6. Panel de administración — Login

El acceso al panel requiere autenticación con sesiones PHP. Se validan usuario y contraseña y se redirige al escritorio.

- **Archivo:** `002-empezamos a atar/admin/index.php`, líneas 1–46
- **Ruta:** `002-empezamos a atar/admin/index.php`

```php
session_start();
if($_SERVER['REQUEST_METHOD'] === 'POST'){
    $u = isset($_POST['usuario']) ? (string)$_POST['usuario'] : "";
    $p = isset($_POST['contrasena']) ? (string)$_POST['contrasena'] : "";
    if($u === "jocarsa" && $p === "jocarsa"){
        $_SESSION['admin_ok'] = 1;
        header("Location: escritorio.php");
    }
}
```

Se añadieron atributos `required` y `minlength` en los inputs del formulario.

### 7. Panel de administración — CRUD completo

El escritorio permite gestionar páginas y entradas con operaciones CRUD completas. Usa prepared statements para prevenir SQL injection y detecta automáticamente la clave primaria de cada tabla.

- **Archivo:** `002-empezamos a atar/admin/escritorio.php`, líneas 1–276
- **Ruta:** `002-empezamos a atar/admin/escritorio.php`

```php
// INSERT con prepared statements
$sql = "INSERT INTO `$tabla` ($cols) VALUES ($qs)";
$stmt = $c->prepare($sql);
$stmt->bind_param($types, ...$vals);
$stmt->execute();

// UPDATE
$sql = "UPDATE `$tabla` SET $set WHERE `$pk` = ? LIMIT 1";

// DELETE con confirmación JS mejorada
onclick="return confirm('¿Seguro que quieres eliminar este registro?')"
```

### 8. Mejoras aplicadas

- **Transitions CSS** en botones y tarjetas del blog (0.2s suaves).
- **`focus-visible`** en botones para accesibilidad con teclado.
- **Responsive** con media queries: grid a 1 columna en pantallas pequeñas, ancho fluido < 960px.
- **`prefers-reduced-motion`** para respetar preferencias del usuario.
- **Hover en tarjetas** del blog con elevación y sombra.
- **`required` y `minlength`** en el formulario de login.
- **Confirmación de borrado mejorada** con mensaje más descriptivo.
- **Focus teal** en inputs del panel admin.
- **`tr:hover`** en las tablas del listado.

## Presentación del proyecto

El proyecto **JocarsaPress** es un CMS construido desde cero que demuestra cómo funciona un gestor de contenidos por dentro. La web pública sirve como portafolio personal con un blog integrado donde las entradas se escriben en Markdown y se renderizan a HTML de forma segura.

El panel de administración es un CRUD completo con dos secciones — páginas y entradas — que usa prepared statements para prevenir inyecciones SQL. El login con sesiones PHP protege el acceso al panel.

Lo más singular del proyecto es el framework CSS JVestilo: un generador PHP que crea miles de clases de utilidad (colores, paddings, margins, flexbox, grid, bordes) de forma dinámica. Esto permite construir la interfaz sin escribir CSS personalizado, usando solo clases en el HTML al estilo de Tailwind pero generadas con PHP.

El front-end combina JVestilo con un CSS adicional que define variables de diseño y componentes específicos como botones, badges y estilos de Markdown.

## Conclusión

Este proyecto muestra que un CMS funcional no necesita frameworks complejos. Con PHP puro, MySQL, sesiones y un renderizador Markdown propio se consigue un sistema capaz de gestionar contenidos dinámicos con un panel de administración completo. El framework CSS JVestilo añade una capa de originalidad al generar todas las utilidades desde PHP, demostrando que los principios de CSS utility-first pueden implementarse de formas creativas. Las mejoras de accesibilidad, responsive y seguridad añadidas complementan un proyecto que cubre front, back, base de datos y estilos.
