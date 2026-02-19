# Tienda Online DAM — Proyecto de Bases de Datos

![Cabecera de la tienda online](101-Ejercicios/009-mejoras%20en%20el%20CSS/front/img/cabeceratienda.avif)


> 🔗 **GitHub Pages:** [https://mutenros.github.io/Bases-de-datos-001-Proyecto-tienda-online/](https://mutenros.github.io/Bases-de-datos-001-Proyecto-tienda-online/)
---

## Introducción

![Vista del catálogo de productos](101-Ejercicios/009-mejoras%20en%20el%20CSS/front/img/producto.webp)

Tienda Online DAM es una aplicación web de comercio electrónico desarrollada de forma incremental a lo largo de 9 fases, desde una página estática hasta una tienda funcional con catálogo dinámico, carrito de compra con sesiones PHP y persistencia de pedidos en MySQL. El proyecto demuestra cómo integrar front-end (HTML/CSS) con back-end (PHP/MySQL) para construir un flujo completo de compra: el usuario navega el catálogo, consulta los detalles de un producto, lo añade al carrito, introduce sus datos de envío y finaliza el pedido, que queda registrado en la base de datos.

---

## Desarrollo de las partes

### 1. Modelo de datos — Diseño de la base de datos

Se parte de un esquema relacional con cuatro tablas que modelan productos, clientes, pedidos y líneas de pedido, relacionadas con claves foráneas para garantizar la integridad referencial.

**Código relevante:**

- Creación de las 4 tablas (`producto`, `cliente`, `pedido`, `lineapedido`) con sus claves primarias y foráneas:
  - **Archivo:** `diagrama.sql` · **Líneas 1-53** · **Ruta:** `101-Ejercicios/diagrama.sql`
- Creación del usuario MySQL dedicado con permisos restringidos a la BD `tiendadam`:
  - **Archivo:** `usuario.sql` · **Líneas 1-17** · **Ruta:** `101-Ejercicios/usuario.sql`
- Inserción de datos de prueba (5 clientes, 7 productos, 8 pedidos y sus líneas):
  - **Archivo:** `insercion.sql` · **Líneas 1-64** · **Ruta:** `101-Ejercicios/insercion.sql`

> 📸 *Incluir aquí captura del diagrama E-R (`101-Ejercicios/diagrama.svg`) y de phpMyAdmin mostrando las tablas creadas.*

---

### 2. Punto de entrada y enrutamiento — `index.php`

El archivo principal inicializa la sesión PHP, crea el carrito si no existe y actúa como router: según el parámetro `operacion` de la URL, incluye la vista correspondiente (catálogo, producto, carrito o finalización).

**Código relevante:**

- Inicio de sesión e inicialización del carrito vacío:
  - **Archivo:** `index.php` · **Líneas 2-6** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/index.php`
- Contador de productos en el carrito para el badge del header:
  - **Archivo:** `index.php` · **Línea 7** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/index.php`
- Lógica de enrutamiento con `include` condicional:
  - **Archivo:** `index.php` · **Líneas 30-40** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/index.php`
- Badge del carrito en el header con enlace directo:
  - **Archivo:** `index.php` · **Líneas 21-25** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/index.php`

> 📸 *Incluir captura del header con el badge del carrito mostrando el número de artículos.*

---

### 3. Catálogo de productos — `catalogo.php`

Conecta con MySQL, consulta todos los productos de la tabla `producto` y los presenta en un grid de tarjetas con imagen, título, descripción y precio, enlazando a la ficha del producto.

**Código relevante:**

- Conexión a la base de datos con control de errores:
  - **Archivo:** `catalogo.php` · **Líneas 3-7** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/inc/catalogo.php`
- Consulta SQL y bucle `while` que genera las tarjetas:
  - **Archivo:** `catalogo.php` · **Líneas 8-23** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/inc/catalogo.php`
- Escape de datos con `htmlspecialchars()` para evitar XSS:
  - **Archivo:** `catalogo.php` · **Líneas 10-11** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/inc/catalogo.php`
- Formato de precio con `number_format()` y separador de decimales español:
  - **Archivo:** `catalogo.php` · **Línea 12** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/inc/catalogo.php`
- Imagen de respaldo si el producto no tiene imagen asignada:
  - **Archivo:** `catalogo.php` · **Línea 13** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/inc/catalogo.php`

> 📸 *Incluir captura del catálogo con las tarjetas de los 7 productos renderizadas en grid.*

---

### 4. Ficha de producto — `producto.php`

Muestra la información detallada de un producto concreto. Valida el `id` recibido por GET, usa una **consulta preparada** para prevenir inyección SQL y presenta un formulario para elegir las unidades antes de añadir al carrito.

**Código relevante:**

- Validación del id del producto con `filter_input()`:
  - **Archivo:** `producto.php` · **Líneas 3-6** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/inc/producto.php`
- Consulta preparada con `prepare()` / `bind_param()`:
  - **Archivo:** `producto.php` · **Líneas 13-16** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/inc/producto.php`
- Control de producto no encontrado (num_rows === 0):
  - **Archivo:** `producto.php` · **Líneas 18-21** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/inc/producto.php`
- Formulario con `input hidden` para enviar datos al carrito:
  - **Archivo:** `producto.php` · **Líneas 31-38** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/inc/producto.php`
- Alt text en la imagen para accesibilidad:
  - **Archivo:** `producto.php` · **Línea 29** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/inc/producto.php`

> 📸 *Incluir captura de la ficha de un producto con la imagen, selector de unidades y botón comprar.*

---

### 5. Carrito de compra — `carrito.php`

Recibe los datos por POST, los valida y los añade a la sesión. Muestra una tabla con las líneas del carrito (unidades, producto, precio unitario, subtotal) y calcula el total. Incluye un formulario para datos de entrega y un botón para vaciar el carrito con confirmación JavaScript.

**Código relevante:**

- Validación del POST y sanitización de la cantidad (min/max):
  - **Archivo:** `carrito.php` · **Líneas 2-13** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/inc/carrito.php`
- Detección de carrito vacío para mostrar aviso:
  - **Archivo:** `carrito.php` · **Línea 15** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/inc/carrito.php`
- Tabla HTML con `<thead>`, `<tbody>` y `<tfoot>` para la fila de totales:
  - **Archivo:** `carrito.php` · **Líneas 37-69** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/inc/carrito.php`
- Cálculo de subtotal y total acumulado dentro del bucle `foreach`:
  - **Archivo:** `carrito.php` · **Líneas 49-54** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/inc/carrito.php`
- Formulario de datos de entrega con campos `required`:
  - **Archivo:** `carrito.php` · **Líneas 19-28** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/inc/carrito.php`
- Confirmación JavaScript antes de vaciar el carrito (`confirm()`):
  - **Archivo:** `carrito.php` · **Líneas 75-81** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/inc/carrito.php`

> 📸 *Incluir captura del carrito con productos, tabla de totales y formulario de datos.*

---

### 6. Finalización y persistencia del pedido — `finalizacion.php`

Recibe los datos del cliente por POST, inserta el registro en la tabla `cliente`, luego crea el `pedido` y finalmente inserta cada producto del carrito como `lineapedido`. Al terminar, vacía el carrito de la sesión.

**Código relevante:**

- Inserción del cliente y obtención del `insert_id`:
  - **Archivo:** `finalizacion.php` · **Líneas 4-11** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/inc/finalizacion.php`
- Inserción del pedido con la fecha actual (`date('Y-m-d H:i:s')`):
  - **Archivo:** `finalizacion.php` · **Líneas 13-18** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/inc/finalizacion.php`
- Bucle `foreach` para insertar las líneas de pedido:
  - **Archivo:** `finalizacion.php` · **Líneas 20-27** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/inc/finalizacion.php`
- Vaciado del carrito tras la compra:
  - **Archivo:** `finalizacion.php` · **Línea 29** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/inc/finalizacion.php`

> 📸 *Incluir captura de la pantalla de "Pedido finalizado" y de phpMyAdmin mostrando un pedido recién insertado.*

---

### 7. Utilidad — Vaciar carrito (`borrar.php`)

Script auxiliar que reinicia el carrito en la sesión y redirige al usuario de vuelta a la vista de carrito usando `header('Location')` + `exit` para evitar ejecución posterior.

**Código relevante:**

- Vaciado de sesión y redirección limpia:
  - **Archivo:** `borrar.php` · **Líneas 1-6** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/util/borrar.php`

---

### 8. Estilos y diseño responsive — `estilo.css`

Hoja de estilos completa (585 líneas) que aplica un diseño moderno con gradientes, sombras, bordes redondeados y transiciones suaves. Se usa CSS Grid para el catálogo, Flexbox para las vistas de producto/carrito, y media queries para adaptarse a pantallas móviles.

**Código relevante:**

- Reset universal y tipografía base:
  - **Archivo:** `estilo.css` · **Líneas 4-23** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/css/estilo.css`
- Header con imagen de fondo, gradiente y efecto de desenfoque (`backdrop-filter`):
  - **Archivo:** `estilo.css` · **Líneas 29-63** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/css/estilo.css`
- Badge del carrito con pill shape (`border-radius: 999px`):
  - **Archivo:** `estilo.css` · **Líneas 81-100** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/css/estilo.css`
- Grid del catálogo con `auto-fit` y `minmax` para responsividad automática:
  - **Archivo:** `estilo.css` · **Líneas 132-135** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/css/estilo.css`
- Tarjetas con efecto hover (`translateY` + sombra amplificada):
  - **Archivo:** `estilo.css` · **Líneas 155-160** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/css/estilo.css`
- Botones con gradiente lineal y transiciones suaves:
  - **Archivo:** `estilo.css` · **Líneas 190-210** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/css/estilo.css`
- Tabla del carrito con filas alternas y fila de total resaltada:
  - **Archivo:** `estilo.css` · **Líneas 462-508** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/css/estilo.css`
- Media query para móviles (max-width: 768px):
  - **Archivo:** `estilo.css` · **Líneas 566-585** · **Ruta:** `101-Ejercicios/009-mejoras en el CSS/front/css/estilo.css`

> 📸 *Incluir captura comparando la vista escritorio vs móvil.*

---

## Presentación del proyecto

La Tienda Online DAM es un e-commerce completo que permite al usuario realizar todo el flujo de compra desde el navegador. Al acceder se muestra un catálogo con todos los productos disponibles en forma de tarjetas visuales. Cada tarjeta incluye imagen, nombre, descripción y precio, con un botón que lleva a la ficha detallada del producto.

Dentro de la ficha, el usuario puede seleccionar la cantidad de unidades que desea y añadirlas al carrito. El header muestra en todo momento un badge con el número de artículos en el carrito, permitiendo acceder a él en cualquier momento.

En la vista del carrito se presenta una tabla desglosada con cada producto añadido, sus unidades, precio unitario, subtotal por línea y un total general. A la izquierda, un formulario recoge los datos de entrega (nombre, apellidos y email). El usuario puede vaciar el carrito (con confirmación JavaScript) o proceder a finalizar la compra.

Al finalizar, el sistema persiste toda la información en MySQL: crea el registro del cliente, genera el pedido con la fecha actual y almacena cada línea de pedido con su producto y cantidad. El carrito se vacía automáticamente y se muestra un mensaje de confirmación.

Todo el front-end está diseñado con un CSS moderno que incluye gradientes, sombras, transiciones y un diseño totalmente responsive que se adapta a dispositivos móviles.

> 📸 *Incluir aquí capturas secuenciales del flujo completo: Catálogo → Ficha de producto → Carrito con productos → Formulario rellenado → Pantalla de confirmación.*

> 🎥 *Opcionalmente, un video corto de screencast recorriendo todo el flujo de compra.*

---

## Conclusión

Este proyecto demuestra la capacidad de construir una aplicación web funcional integrando las tres capas fundamentales: **presentación** (HTML/CSS responsive), **lógica de negocio** (PHP con sesiones) y **persistencia de datos** (MySQL con esquema relacional).

A lo largo de las 9 fases de desarrollo se han aplicado buenas prácticas como:

- **Seguridad:** escape de salidas con `htmlspecialchars()`, validación de entradas con `filter_input()`, consultas preparadas con `prepare()`/`bind_param()` para prevenir inyección SQL.
- **Usabilidad:** badge del carrito siempre visible, mensaje de carrito vacío, confirmación antes de vaciar, campos de formulario con `required`.
- **Mantenibilidad:** separación en archivos PHP reutilizables (`inc/`, `util/`), CSS organizado por secciones con comentarios, estructura de carpetas limpia.
- **Diseño:** interfaz moderna con CSS Grid, Flexbox, gradientes, sombras y media queries para responsive.

El resultado es una tienda que, partiendo de una estructura sencilla y mantenible, cubre un flujo de compra real de principio a fin, desde el catálogo hasta el almacenamiento del pedido en base de datos.
