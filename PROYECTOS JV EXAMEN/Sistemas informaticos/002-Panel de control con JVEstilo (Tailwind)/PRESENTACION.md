# Panel de control con JVEstilo (Tailwind) — Framework CSS con PHP

![Panel de administración con tabla de clientes](004-vamos%20con%20la%20tabla.php)

## Introducción

Este proyecto desarrolla un **framework CSS tipo Tailwind generado dinámicamente con PHP** llamado **JVEstilo**. A diferencia de Tailwind que se compila con Node.js, JVEstilo genera todas las clases utilitarias (colores, tamaños, flex, grid, bordes, tipografía…) directamente desde PHP, incluyéndolas mediante `<?php include("JVestilo/JVestilo.php"); ?>` dentro de una etiqueta `<style>`.

Con JVEstilo se construye progresivamente un panel de administración de clientes: empezando por un formulario de login básico, mejorándolo con estilos, añadiendo un layout de admin con sidebar, y finalmente una tabla de datos de clientes con 20 registros.

---

## Desarrollo

### 1. JVEstilo.php — El motor del framework CSS

El archivo `JVestilo.php` es el corazón del proyecto. Genera miles de clases CSS utilitarias dinámicamente usando bucles PHP. Incluye los colores de `colores.php` y genera clases para fondos (`.b-`), colores de texto (`.c-`), padding (`.p-`), margin (`.m-`), width (`.w-`), height (`.h-`), font-size (`.fs-`), gap (`.g-`), border-radius (`.bradius-`), flex (`.f-`), y bordes combinados.

```php
// JVestilo/JVestilo.php — líneas 4-21
// Ruta: JVestilo/JVestilo.php
include "colores.php";
foreach($colores as $color){
  echo ".b-".strtolower($color)."{background:".strtolower($color).";}";
  echo ".c-".strtolower($color)."{color:".strtolower($color).";}";
}
for($i = 0;$i<2000;$i++){
  echo ".p-".$i."{padding:".$i."px;}"; 
  echo ".m-".$i."{margin:".$i."px;}";
  echo ".w-".$i."{width:".$i."px;}";
  echo ".w-".$i."pc{width:".$i."%;}";
  echo ".h-".$i."{height:".$i."px;}";
  echo ".h-".$i."pc{height:".$i."%;}";
  echo ".fs-".$i."{font-size:".$i."px;}";
  echo ".g-".$i."{gap:".$i."px;}";
  echo ".bradius-".$i."{border-radius:".$i."px;}";
  echo ".f-".$i."{flex:".$i.";}";
}
```

También genera clases para flexbox (`flex`, `fd-row`, `fd-column`, `fj-center`, `fa-center`), grid con columnas (`.gc-N`), text-align, text-decoration, familias de fuentes y bordes combinados (tipo-grosor-color).

---

### 2. colores.php — Paleta de 154 colores CSS

El archivo `colores.php` define un array PHP con los 154 colores estándar de CSS (AliceBlue a YellowGreen). Este array alimenta al generador de JVEstilo para crear clases de fondo y color de texto para cada color.

```php
// JVestilo/colores.php — líneas 3-12
// Ruta: JVestilo/colores.php
$colores = [
    "AliceBlue",
    "AntiqueWhite",
    "Aqua",
    "Aquamarine",
    "Azure",
    "Beige",
    "Bisque",
    "Black",
    // ... 154 colores CSS en total
];
```

Cada color genera 2 clases (fondo + texto) más las combinaciones de borde (20 grosores × 10 tipos de línea × 154 colores = ~30.800 clases de borde).

---

### 3. familiasfuentes.php — Familias tipográficas

Define las 6 familias genéricas de CSS para generar clases de fuente como `.ff-serif`, `.ff-sans-serif`, `.ff-monospace`, etc.

```php
// JVestilo/familiasfuentes.php — líneas 2-9
// Ruta: JVestilo/familiasfuentes.php
$familias = [
    'serif',
    'sans-serif',
    'monospace',
    'cursive',
    'fantasy',
    'system-ui'
];
```

---

### 4. 001-login.php — Login básico sin estilos

El primer ejercicio crea un formulario de login mínimo usando solo clases de JVEstilo. Demuestra el concepto básico: incluir el framework via PHP `include` y usar clases utilitarias para flex centering, dimensiones y colores.

```html
<!-- 001-login.php — líneas 8-13 -->
<!-- Ruta: 001-login.php -->
<body class="b-lightgray flex fa-center fj-center w-100pc h-100pc p-0 m-0">
  <form class="w-200 h-200 b-white p-20">
    <input type="text" placeholder="usuario">
    <input type="password" placeholder="contraseña">
    <input type="submit">
  </form>
</body>
```

Las clases `flex fa-center fj-center` centran el formulario horizontal y verticalmente, `w-100pc h-100pc` ocupa toda la pantalla, y `b-lightgray` pone fondo gris claro.

---

### 5. 002-sigo maquetando el login.php — Login con estilos mejorados

El segundo ejercicio mejora el login añadiendo más clases de JVEstilo: flexbox column con gap, bordes redondeados, y padding en los inputs. Se añadió validación JavaScript que comprueba longitud mínima de usuario y contraseña.

```html
<!-- 002-sigo maquetando el login.php — líneas 20-25 -->
<!-- Ruta: 002-sigo maquetando el login.php -->
<form class="w-200 h-200 b-white p-20 flex fd-column g-20 fj-center bradius-10"
      onsubmit="return validarLogin(this)">
  <input type="text" placeholder="usuario" class="p-10 br-1-solid-lightgray bradius-5" required>
  <input type="password" placeholder="contraseña" class="p-10 br-1-solid-lightgray bradius-5" required>
  <input type="submit" value="Entrar" class="p-10 br-1-solid-lightgray b-lightgray bradius-5">
</form>
```

```javascript
// 002-sigo maquetando el login.php — líneas 28-40
// Ruta: 002-sigo maquetando el login.php
function validarLogin(form) {
  var usuario = form.querySelector('[type="text"]');
  var password = form.querySelector('[type="password"]');
  if (usuario.value.trim().length < 3) {
    alert('El usuario debe tener al menos 3 caracteres.');
    usuario.focus();
    return false;
  }
  if (password.value.length < 4) {
    alert('La contraseña debe tener al menos 4 caracteres.');
    password.focus();
    return false;
  }
  return true;
}
```

---

### 6. 003-vamos con el admin.php — Layout del panel de administración

El tercer ejercicio crea un layout de 2 columnas usando flex: un `<nav>` lateral (sidebar) con fondo teal y enlaces blancos, y un `<main>` como área de contenido. La proporción es 1:5 gracias a las clases `.f-1` y `.f-5`.

```html
<!-- 003-vamos con el admin.php — líneas 9-18 -->
<!-- Ruta: 003-vamos con el admin.php -->
<body class="w-100pc h-100pc p-0 m-0 flex">
  <nav class="f-1 b-teal p-20 flex fd-column g-20">
    <a href="clientes" class="b-white p-10 c-teal td-none">Clientes</a>
    <a href="clientes" class="b-white p-10 c-teal td-none">Productos</a>
    <a href="clientes" class="b-white p-10 c-teal td-none">Pedidos</a>
    <a href="clientes" class="b-white p-10 c-teal td-none">Almacen</a>
  </nav>
  <main class="f-5 b-white p-20">
    Contenido
  </main>
</body>
```

El sidebar teal con enlaces blancos crea un contraste visual profesional. Las clases `flex fd-column g-20` organizan los enlaces verticalmente con separación de 20px.

---

### 7. 004-vamos con la tabla.php — Tabla de clientes con datos

El ejercicio más avanzado combina el layout del admin con una tabla HTML de 20 clientes con nombre, apellidos, email y teléfono. La tabla usa clases JVEstilo para ancho completo y borde teal, con cabecera destacada.

```html
<!-- 004-vamos con la tabla.php — líneas 27-33 -->
<!-- Ruta: 004-vamos con la tabla.php -->
<table class="w-100pc br-2-solid-teal p-10">
  <thead class="b-teal c-white p-10">
    <tr><th>Nombre</th><th>Apellidos</th><th>Email</th><th>Telefono</th></tr>
  </thead>
  <tbody>
    <tr><td>Ana</td><td>Martínez López</td><td>ana.martinez@example.com</td><td>612345678</td></tr>
    <!-- ... 20 filas en total ... -->
  </tbody>
</table>
```

Se añadieron filas alternadas con `nth-child(even)`, hover en filas, transiciones en los enlaces de navegación, un título "Clientes" con estilo y un contador de registros al pie de la tabla.

---

### 8. Generación dinámica de bordes en JVEstilo

Una de las secciones más interesantes del framework es la generación combinatoria de clases de borde: 20 grosores × 10 tipos de línea CSS × 154 colores = más de 30.000 clases de borde.

```php
// JVestilo/JVestilo.php — líneas 54-64
// Ruta: JVestilo/JVestilo.php
$tiposLineaCss = ["none","hidden","solid","dashed","dotted","double","groove","ridge","inset","outset"];
for($i = 0;$i<20;$i++){
  foreach($tiposLineaCss as $tipo){
    foreach($colores as $color){
      echo ".br-".$i."-".$tipo."-".strtolower($color)."{border:".$i."px ".$tipo." ".$color.";}";
    }
  }
}
```

Esto permite usar clases como `.br-2-solid-teal` o `.br-1-dashed-red` directamente en el HTML, imitando la filosofía utility-first de Tailwind.

---

### 9. Mejoras aplicadas

Se aplicaron mejoras mixtas sobre el código original:

- **Meta tags** (`charset`, `viewport`) y `<title>` en login y tabla para HTML correcto.
- **CSS transitions** en el botón de login, enlaces de navegación y filas de la tabla.
- **Hover effects**: botón se eleva al pasar, enlaces del sidebar se desplazan, filas se iluminan.
- **Focus styles** en inputs del login con `border-color` teal y `box-shadow`.
- **Filas alternadas** (`nth-child(even)`) en la tabla para mejor legibilidad.
- **Validación JavaScript** en el formulario de login (longitud mínima).
- **Atributo `required`** en inputs del login.
- **Título de sección** "Clientes" y contador de registros en la tabla.
- **Comentarios** explicativos en JVestilo.php y clase utilitaria `.cursor-pointer`.

---

## Presentación

Este proyecto muestra cómo construir un framework CSS desde cero utilizando PHP como generador. JVEstilo funciona como una versión simplificada de Tailwind CSS: en lugar de compilar con Node.js, genera todas las clases utilitarias en tiempo de ejecución mediante bucles PHP que recorren arrays de colores, tamaños y propiedades CSS.

El resultado es un sistema donde puedes aplicar cualquier estilo directamente en el HTML con clases como `b-teal`, `p-20`, `flex`, `fd-column`, `bradius-10` o `br-2-solid-teal`. Con estas clases se construye progresivamente un panel de administración: primero un login centrado, luego un layout con sidebar, y finalmente una tabla de datos de 20 clientes con cabecera destacada y filas alternadas.

Las 4 fases del proyecto demuestran cómo un framework utility-first permite construir interfaces complejas sin escribir CSS personalizado, solo combinando clases utilitarias.

---

## Conclusión

JVEstilo demuestra que los principios detrás de frameworks como Tailwind CSS son accesibles y replicables: un bucle que genera clases para cada valor posible de una propiedad CSS. El enfoque PHP, aunque menos eficiente que la compilación estática de Tailwind, tiene la ventaja de ser totalmente dinámico y comprensible para un estudiante que conoce PHP.

El proyecto progresa de forma lógica: framework → login → layout → tabla con datos, mostrando cómo cada capa se construye sobre la anterior. Las mejoras aplicadas — validación JS, hover/transitions, filas alternadas, meta tags — complementan el trabajo original con buenas prácticas web que mejoran la experiencia de usuario y la accesibilidad.
