# Panel de control con GET y POST

![Panel de control PHP MySQL](https://img.shields.io/badge/PHP-MySQL_Admin-777BB4?style=for-the-badge&logo=php&logoColor=white)

> 🔗 **GitHub Pages:** [https://mutenros.github.io/Entornos-004-Panel-de-control-con-GET-y-POST/](https://mutenros.github.io/Entornos-004-Panel-de-control-con-GET-y-POST/)

## Introducción

Este proyecto construye un panel de administración web que permite explorar cualquier base de datos MySQL de forma visual. Utilizando PHP y el objeto MySQLi, la aplicación lista automáticamente todas las tablas de una base de datos y muestra su contenido en una interfaz con barra lateral y tabla de datos. A lo largo de 7 archivos evolutivos se estudian los métodos GET y POST de HTTP, desde pasar un simple parámetro por URL hasta construir un panel completo con estilos avanzados y protección contra inyecciones.

## Desarrollo de las partes

### 1. Paso de parámetros por GET

**Archivo:** `101-Ejercicios/001-get.php` · **Líneas:** 1-7

```php
echo $_GET['nombre'];
```

El primer ejercicio demuestra cómo PHP recibe datos a través de la URL. El array superglobal `$_GET` captura los parámetros que se escriben después del signo `?` en la dirección (por ejemplo `?nombre=Jose`). Es la base de toda la navegación del panel posterior.

### 2. Múltiples parámetros GET

**Archivo:** `101-Ejercicios/002-pasar varios parametros.php` · **Líneas:** 1-8

```php
echo $_GET['nombre'];
echo "<br>";
echo $_GET['apellidos'];
```

Se amplía el concepto para recibir varios parámetros separados por `&` en la URL (`?nombre=Jose&apellidos=Garcia`). La etiqueta `<br>` separa visualmente los valores. Este patrón de múltiples parámetros es el que luego usa el panel para indicar qué tabla mostrar.

### 3. Formulario con método POST

**Archivo:** `101-Ejercicios/003-metodo post.php` · **Líneas:** 1-7

```html
<form action="004-procesa.php" method="POST">
  <input type="text" name="nombre" placeholder="Introduce tu nombre" required>
  <input type="text" name="apellidos" placeholder="Introduce tus apellidos" required>
  <input type="submit" value="Enviar">
</form>
```

A diferencia de GET, el método POST envía los datos en el cuerpo de la petición HTTP (no aparecen en la URL). El atributo `action` indica a qué archivo PHP se envían los datos. Se añadió el atributo `required` para que el navegador valide que los campos no estén vacíos antes de enviar.

### 4. Procesamiento de datos POST

**Archivo:** `101-Ejercicios/004-procesa.php` · **Líneas:** 1-7

```php
echo "Tu nombre es: ".htmlspecialchars($_POST['nombre'], ENT_QUOTES, 'UTF-8');
echo "<br>";
echo "Tus apellidos son: ".htmlspecialchars($_POST['apellidos'], ENT_QUOTES, 'UTF-8');
```

El archivo complementario al formulario: recibe los datos de `$_POST` y los muestra. Se usa `htmlspecialchars()` para evitar ataques XSS (si alguien escribiera código HTML o JavaScript en el formulario, se mostraría como texto plano en vez de ejecutarse).

### 5. Panel de control — primera versión

**Archivo:** `101-Ejercicios/005-continuamos con el panel de control.php` · **Líneas:** 1-65

```php
$mysqli = new mysqli("localhost", "miempresa", "miempresa", "miempresa");
$sql = "SHOW TABLES";
$resultado = $mysqli->query($sql);
while ($fila = $resultado->fetch_assoc()) {
    echo '<a href="?tabla='.$fila['Tables_in_miempresa'].'">'.$fila['Tables_in_miempresa'].'</a>';
}
```

Aquí nace el panel de control real. Con `new mysqli()` se conecta a la base de datos `miempresa`. El comando SQL `SHOW TABLES` devuelve todas las tablas existentes, que se muestran como enlaces en la barra lateral. Al pulsar un enlace se genera un parámetro GET (`?tabla=clientes`) que provoca que el contenido de esa tabla se cargue en la zona principal. El layout usa **flexbox**: `nav` (flex:1) a la izquierda y `main` (flex:5) a la derecha.

### 6. Consultas SQL dinámicas y visualización de datos

**Archivo:** `101-Ejercicios/012-mas ajustes esteticos.php` · **Líneas:** 85-122

```php
$sql = "SELECT * FROM `" . $mysqli->real_escape_string($tablaSeleccionada) . "` LIMIT 1;";
$resultado = $mysqli->query($sql);
if ($resultado) {
    while ($fila = $resultado->fetch_assoc()) {
        foreach($fila as $clave=>$valor){
            echo "<th>".htmlspecialchars($clave, ENT_QUOTES, 'UTF-8')."</th>";
        }
    }
}
```

Se ejecutan dos consultas: una con `LIMIT 1` para obtener los nombres de las columnas (cabeceras de la tabla HTML) y otra sin límite para los datos. El resultado se recorre con `fetch_assoc()` que devuelve cada fila como array asociativo. Se usa `real_escape_string()` para proteger el nombre de la tabla contra inyección SQL y `htmlspecialchars()` en cada celda para evitar XSS.

### 7. Diseño CSS del panel

**Archivo:** `101-Ejercicios/012-mas ajustes esteticos.php` · **Líneas:** 13-60

```css
body{display:flex;}
nav{flex:1;background:indigo;color:white;padding:20px;display:flex;flex-direction:column;gap:20px;}
main{flex:5;background:aliceblue;padding:20px;}
nav a{border:none;background:white;padding:20px;text-decoration:none;color:indigo;text-transform:uppercase;
      font-weight:bold;border-radius:5px;display:flex;align-items:center;gap:20px;}

.inicial{
    display:block; width:20px; height:20px;
    background:indigo; color:white; text-align:center;
    padding:10px; border-radius:5px; line-height:20px;
}

nav a:hover{
    background:#e0d0ff;
    transform:scale(1.03);
}
nav a.activo{
    background:#c7b3ff;
    border:2px solid white;
}
```

El menú lateral usa color **indigo** con botones blancos redondeados. Cada enlace tiene un avatar cuadrado (`.inicial`) que muestra la primera letra del nombre de la tabla. La tabla de datos usa la clase `.redondeado` con `border-collapse: separate` para conseguir esquinas redondeadas. Las filas pares tienen fondo blanco (`nth-child(even)`) para facilitar la lectura. Se añadió efecto hover con transición CSS y una clase `.activo` que resalta la tabla actualmente seleccionada.

### 8. Adaptación responsive

**Archivo:** `101-Ejercicios/012-mas ajustes esteticos.php` · **Líneas:** 57-60

```css
@media (max-width: 768px){
    body{flex-direction:column;}
    nav{flex-direction:row;flex-wrap:wrap;}
}
```

En pantallas menores a 768 px, el layout cambia de horizontal a vertical: el menú pasa de columna lateral a fila superior con `flex-wrap` para que los botones se ajusten automáticamente. El área principal ocupa todo el ancho debajo.

## Presentación del proyecto

El proyecto final es un panel de administración de bases de datos construido con PHP y MySQL. Al abrir `012-mas ajustes esteticos.php` en un navegador con servidor PHP, la aplicación se conecta automáticamente a la base de datos `miempresa` y genera un menú lateral dinámico con todas las tablas disponibles.

Al seleccionar una tabla del menú:
- La tabla seleccionada se resalta con un borde blanco y fondo lila claro
- Las **cabeceras** de la tabla SQL se muestran como encabezados (`<th>`) con fondo indigo
- Todos los **registros** aparecen en filas alternadas (blanco y aliceblue) para facilitar la lectura
- Los nombres de tabla llevan un avatar con su inicial

Si no se ha seleccionado ninguna tabla, aparece un mensaje indicando que se elija una del menú lateral. Todo el contenido se genera dinámicamente con PHP — no hay datos hardcodeados.

El proyecto demuestra el recorrido completo desde recibir un parámetro GET simple hasta construir una aplicación de gestión real con consultas SQL dinámicas y diseño responsive.

## Conclusión

Este proyecto ilustra de forma progresiva cómo los métodos HTTP GET y POST se combinan con PHP y MySQL para crear aplicaciones web dinámicas. Desde un simple `echo $_GET['nombre']` hasta un panel completo que recorre tablas automáticamente, cada fase añade complejidad de forma controlada.

Los conceptos clave trabajados han sido:
- La diferencia entre **GET** (parámetros en URL, visible) y **POST** (datos en cuerpo, oculto)
- La conexión a MySQL con **MySQLi** orientado a objetos
- La generación dinámica de HTML desde resultados de consultas SQL
- La **seguridad web**: `htmlspecialchars()` contra XSS, `real_escape_string()` contra SQL injection, validación con `isset()` y `required`
- El diseño con **CSS flexbox** para crear layouts de panel sidebar + contenido
- Los **ajustes estéticos progresivos**: bordes redondeados, avatares, alternancia de filas, hover y estados activos

El resultado es un explorador de bases de datos funcional que puede adaptarse a cualquier base de datos MySQL simplemente cambiando los datos de conexión.
