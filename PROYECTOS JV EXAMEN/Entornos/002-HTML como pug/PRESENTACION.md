# HTML como Pug — Motor de plantillas JVpug

![Vista de la web personal renderizada con JVpug](img_preview.png)

## Introducción

Este proyecto consiste en la creación de un **motor de plantillas tipo Pug** escrito íntegramente en PHP. El objetivo es simplificar la escritura de HTML mediante una sintaxis basada en indentación (sin etiquetas de cierre), similar a lo que hace Pug en el ecosistema Node.js, pero implementado de forma nativa en PHP.

El proyecto evoluciona en varias fases: desde un parser básico que convierte una plantilla sencilla a HTML, hasta un sistema completo con directivas (`@if`, `@foreach`, `@include`), interpolación de variables, un framework CSS utility-first generado dinámicamente (JVestilo), y un controlador que conecta con MySQL para renderizar una web personal real con páginas y entradas de blog.

## Desarrollo

### 1. Parser básico de Pug a HTML (fase 001)

La primera versión implementa un conversor mínimo que recorre líneas con indentación de 2 espacios y genera HTML con apertura/cierre de tags automáticos. Soporta atributos `class="..."` y texto inline.

```php
// Archivo: 001-libreria de conversion de pug a html.php — líneas 14-20
// Comprobación de existencia de la plantilla antes de leerla
$archivoPlantilla = "index.jvpug";
if (!file_exists($archivoPlantilla)) {
    die("Error: no se encontró la plantilla " . htmlspecialchars($archivoPlantilla, ENT_QUOTES, 'UTF-8'));
}
$pug = file_get_contents($archivoPlantilla);
```

La función `render_mini_pug()` usa una pila (`$stack`) para gestionar los tags abiertos y cerrarlos automáticamente al reducir el nivel de indentación, eliminando así la necesidad de escribir `</tag>` manualmente.

```php
// Archivo: 001-libreria de conversion de pug a html.php — líneas 37-43
// Cierre automático de tags cuando la indentación retrocede
while (count($stack) > $level) {
    $tag = array_pop($stack);
    $out[] = str_repeat("  ", count($stack)) . "</{$tag}>";
}
```

### 2. Plantilla JVpug básica (index.jvpug)

La plantilla de ejemplo demuestra la sintaxis Pug simplificada: cada línea es un tag, la indentación define la jerarquía padre-hijo, y los atributos van después del tag.

```
// Archivo: index.jvpug — líneas 2-8
html
  head
    title La web de Jose Vicente
  body
    h1 class="rojo" La web de Jose Vicente
    h2 Profesor, diseñador, desarrollador en Valencia
    p Esto es un texto de párrafo
```

Esto genera automáticamente `<html><head><title>...</title></head><body><h1 class="rojo">...</h1>...</body></html>` sin necesidad de escribir ninguna etiqueta de cierre.

### 3. Librería JVpug avanzada (507 líneas)

El core del proyecto es `jvpug.php`, una clase PHP de 507 líneas que implementa un motor de plantillas completo con:

- **Parser por indentación** que genera un árbol de nodos (`parseToTree`)
- **Directivas**: `@if / @elseif / @else`, `@foreach`, `@for`, `@include`
- **Interpolación**: `#{expr}` (con escape HTML) y `!{expr}` (sin escape)
- **Atributos dinámicos** evaluados con `eval()`
- **Tags auto-cerrados** (br, img, hr, input, meta...)

```php
// Archivo: jvpug.php — líneas 18-26
// Método principal: lee un archivo .jvpug y lo renderiza con variables
public static function renderFile(string $file, array $vars = []): string
{
    $src = @file_get_contents($file);
    if ($src === false) {
        throw new RuntimeException("No se pudo leer: {$file}");
    }
    $baseDir = dirname($file);
    return self::render($src, $vars, $baseDir);
}
```

```php
// Archivo: jvpug.php — líneas 84-100
// Tolerancia: detecta directivas escritas sin @ (if, foreach...)
// para evitar que se rendericen como tags HTML
if (preg_match('/^(if|elseif|else|for|foreach|include)\b(.*)$/i', $line, $dm)) {
    $name = strtolower($dm[1]);
    $rest = trim($dm[2]);
    return [
        'type' => 'dir',
        'name' => $name,
        'args' => $rest,
    ];
}
```

### 4. Plantilla perfil.jvpug — Variables e iteración

Esta plantilla demuestra el uso de variables interpoladas y bucles `@for`:

```
// Archivo: perfil.jvpug — líneas 5-20
html
  head
    meta charset="utf-8"
    meta name="viewport" content="width=device-width,initial-scale=1"
    title Jose Vicente Carratalá
  body
    header
      h1 #{nombre}
      h2 #{titulo}
    section
      p #{descripcion}
    section
      h3 Áreas de trabajo
      ul
        @for area in $areas
          li #{area}
```

El controlador `002-perfil.php` la invoca pasando un array de variables:

```php
// Archivo: 002-perfil.php — líneas 3-10
echo JVpug::renderFile(__DIR__ . '/perfil.jvpug', [
    'nombre' => 'Jose Vicente Carratalá',
    'titulo' => 'Desarrollador, profesor y diseñador de software',
    'areas' => [
        'Desarrollo de software',
        'Formación técnica y docencia',
        ...
    ],
]);
```

### 5. Plantilla completa miweb.jvpug — Directivas y layout

La plantilla final construye una web completa con navegación dinámica, condicionales y bucles:

```
// Archivo: miweb.jvpug — líneas 7-16
  body class="flex fd-column fj-center fa-center b-lightgrey ff-sans-serif p-20"
    header class="w-800 b-white p-20 ta-center flex fd-column g-20"
      h1 class="p-0 m-0 fs-36" Jose Vicente Carratala
      h2 class="p-0 m-0 fs-16" Desarrollador, profesor y diseñador
      nav class="flex g-1 fa-center fj-center"
        a href="?" class="b-lightgray p-10 c-black td-none fs-10 w-70" Inicio
        @foreach $paginas as $f
          a href="?p=#{urlencode($f['titulo'])}" class="b-lightgray p-10 c-black td-none fs-10 w-70" #{ $f['titulo'] }
        a href="?p=blog" class="b-lightgray p-10 c-black td-none fs-10 w-70" Blog
```

El bloque condicional `@if !$p / @else` controla si se muestra la página de inicio (con hero + grid de artículos) o el contenido de una página/blog específica.

### 6. JVestilo — Framework CSS utility-first generado con PHP

JVestilo genera dinámicamente clases CSS utilitarias similares a Tailwind, pero mediante bucles PHP:

```php
// Archivo: JVestilo/JVestilo.php — líneas 3-16
include "colores.php";
foreach($colores as $color){
    echo ".b-".strtolower($color)."{background:".strtolower($color).";}";
    echo ".c-".strtolower($color)."{color:".strtolower($color).";}";
}
for($i = 0;$i<2000;$i++){
    echo ".p-".$i."{padding:".$i."px;}"; 
    echo ".m-".$i."{margin:".$i."px;}";
    echo ".w-".$i."{width:".$i."px;}";
    echo ".h-".$i."{height:".$i."px;}";
    echo ".fs-".$i."{font-size:".$i."px;}";
    echo ".g-".$i."{gap:".$i."px;}";
}
```

Genera clases para los 154 colores CSS con nombre (`colores.php`), 6 familias de fuentes (`familiasfuentes.php`), flexbox, grid, alineación, y hasta 2000 valores numéricos para padding, margin, width, height, font-size y gap.

### 7. Controlador con MySQL (fase 004)

El controlador final conecta a MySQL, obtiene las páginas y entradas del blog, y renderiza la plantilla:

```php
// Archivo: 004-controlador.php — líneas 5-12
// Manejo de errores en la conexión a base de datos
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);
try {
    $c = new mysqli("localhost", "jocarsapress", "jocarsapress", "jocarsapress");
    $c->set_charset("utf8mb4");
} catch (mysqli_sql_exception $e) {
    die("Error de conexión a la base de datos: " . htmlspecialchars($e->getMessage()));
}
```

Usa prepared statements para la consulta de páginas por título (prevención SQL injection):

```php
// Archivo: 004-controlador.php — líneas 30-34
$stmt = $c->prepare("SELECT * FROM paginas WHERE titulo = ?");
$stmt->bind_param("s", $p);
$stmt->execute();
$res = $stmt->get_result();
while ($f = $res->fetch_assoc()) $pagina[] = $f;
```

### 8. Mejoras aplicadas al proyecto

Se han aplicado mejoras mixtas en varias capas:

- **PHP (004-controlador.php)**: Manejo de errores con try/catch en conexión MySQL, sanitización del parámetro GET, cabecera Content-Type UTF-8, cierre de conexión al finalizar
- **PHP (001-libreria)**: Validación de existencia de la plantilla con `file_exists()` antes de leerla, y generación de `<!DOCTYPE html>` al inicio
- **JVpug (miweb.jvpug)**: Añadido `meta viewport` para responsive y `meta description` para SEO
- **JVpug (perfil.jvpug)**: Añadido `meta viewport`, comentarios descriptivos de variables esperadas
- **CSS (JVestilo.php)**: Transiciones suaves en enlaces (`transition`), efecto hover de opacidad, clases utilitarias extra (shadow, border-radius, box-sizing, margin reset)

## Presentación

Este proyecto demuestra cómo se puede construir un motor de plantillas completo desde cero en PHP, inspirado en la filosofía de Pug: escribir HTML de forma más limpia usando indentación en lugar de etiquetas de cierre.

La web resultante es una página personal que carga dinámicamente sus secciones desde una base de datos MySQL. El usuario navega entre la página de inicio con su hero y grid de artículos, las páginas de contenido individual, y un blog con entradas. Todo renderizado a partir de archivos `.jvpug` que el motor convierte a HTML estándar.

El framework CSS JVestilo complementa el sistema generando miles de clases utilitarias automáticamente usando PHP, permitiendo maquetar directamente en la plantilla con clases como `w-800`, `p-20`, `fs-36` o `b-lightgrey`, sin necesidad de escribir CSS personalizado.

El proyecto recorre un camino evolutivo claro: desde un parser mínimo de 70 líneas hasta un motor completo de 507 líneas con directivas, condicionales, bucles e includes.

## Conclusión

Este proyecto es un ejercicio práctico de cómo funciona por dentro un motor de plantillas. Entender el parsing por indentación, la generación de un árbol de nodos, la evaluación de expresiones y la renderización recursiva son conceptos fundamentales que aplican tanto a Pug como a cualquier sistema de templates moderno (Blade, Twig, Jinja).

La evolución desde un mini-parser hasta un sistema con MySQL, directivas y un framework CSS propio muestra cómo se puede abordar un problema complejo dividiéndolo en pasos incrementales. El resultado final es un sistema funcional que transforma código limpio y legible en HTML válido y bien estructurado.
