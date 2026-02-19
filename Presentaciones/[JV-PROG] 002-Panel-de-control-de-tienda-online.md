# Panel de Control — Tienda Online

![Panel de Control](https://mutenros.github.io/Programacion-002-Panel-de-control-de-tienda-online/)

> 🔗 **GitHub Pages:** [https://mutenros.github.io/Programacion-002-Panel-de-control-de-tienda-online/](https://mutenros.github.io/Programacion-002-Panel-de-control-de-tienda-online/)

## Introducción

Este proyecto es un panel de control de consola en Java que permite gestionar la tienda online desarrollada en el proyecto de Bases de Datos (Bases-de-datos-001-Proyecto-tienda-online). El panel se conecta a la base de datos MySQL `tiendadam` mediante JDBC y permite realizar operaciones CRUD sobre productos y clientes, consultar pedidos con detalle de líneas (usando JOINs SQL), buscar productos y visualizar estadísticas de facturación. El proyecto demuestra la intermodularidad entre Java y MySQL, aplicando Programación Orientada a Objetos, consultas SQL preparadas y el patrón Singleton para la conexión.

## Desarrollo de las partes

### 1. Clase Conexion — Patrón Singleton y JDBC

La clase `Conexion` encapsula toda la lógica de conexión a MySQL usando JDBC. Implementa un patrón Singleton: solo mantiene una conexión activa a la vez. Usa `Class.forName()` para cargar el driver MySQL y `DriverManager.getConnection()` con los datos del usuario `tiendadam` creado en el proyecto de Bases de Datos.

```java
// src/Conexion.java — Líneas 25-47: Constantes y método obtener()
private static final String URL = "jdbc:mysql://localhost:3306/tiendadam";
private static final String USUARIO = "tiendadam";
private static final String PASSWORD = "Tiendadam123$";

public static Connection obtener() {
    if (conexion == null || conexion.isClosed()) {
        Class.forName("com.mysql.cj.jdbc.Driver");
        conexion = DriverManager.getConnection(URL, USUARIO, PASSWORD);
    }
    return conexion;
}
```

**Archivo:** `src/Conexion.java` · Líneas 25–47 · Ruta: `/src/Conexion.java`

### 2. Clase Producto — Modelo de datos con formato EUR

La clase `Producto` mapea la tabla `producto` de la BD. Sus atributos (`id`, `titulo`, `descripcion`, `precio`, `imagen`) corresponden a las columnas SQL. El método `toString()` formatea el precio con 2 decimales y símbolo EUR usando `String.format()`.

```java
// src/Producto.java — Líneas 46-54: toString con formato EUR
@Override
public String toString() {
    String precioFormateado = String.format("%.2f EUR", precio);
    return "| " + String.format("%-4d", id) +
           " | " + String.format("%-22s", titulo) +
           " | " + String.format("%-30s", descripcion) +
           " | " + String.format("%10s", precioFormateado) +
           " | " + String.format("%-20s", imagen) + " |";
}
```

**Archivo:** `src/Producto.java` · Líneas 46–54 · Ruta: `/src/Producto.java`

### 3. Clase Cliente — Modelo con getters/setters

La clase `Cliente` encapsula los datos de la tabla `cliente` (id, nombre, apellidos, email) con atributos privados, constructor y métodos de acceso. Demuestra el principio de encapsulamiento de la OOP.

```java
// src/Cliente.java — Líneas 16-23: Atributos encapsulados
public class Cliente {
    private int id;
    private String nombre;
    private String apellidos;
    private String email;
}
```

**Archivo:** `src/Cliente.java` · Líneas 16–23 · Ruta: `/src/Cliente.java`

### 4. Clase Pedido — Modelo con datos de JOIN

La clase `Pedido` incluye un atributo extra `nombreCliente` que no existe en la tabla, sino que se carga mediante un JOIN SQL entre `pedido` y `cliente`. Esto muestra cómo el modelo Java puede enriquecer los datos que vienen de varias tablas relacionadas.

```java
// src/Pedido.java — Líneas 18-22: Atributos con dato de JOIN
private int id;
private String fecha;
private int clienteId;
private String nombreCliente; // Viene del JOIN con tabla cliente
```

**Archivo:** `src/Pedido.java` · Líneas 18–22 · Ruta: `/src/Pedido.java`

### 5. Listar productos — SELECT con Statement

El método `listarProductos()` ejecuta un `SELECT * FROM producto` usando `Statement` y recorre el `ResultSet` con un `while (rs.next())`. Crea objetos `Producto` desde cada fila y los muestra en tabla formateada con bordes Unicode.

```java
// src/GestorPanel.java — Líneas 28-61: Listar productos con ResultSet
Statement stmt = con.createStatement();
ResultSet rs = stmt.executeQuery("SELECT * FROM producto ORDER BY id");
while (rs.next()) {
    Producto p = new Producto(
        rs.getInt("id"),
        rs.getString("titulo"),
        rs.getString("descripcion"),
        Double.parseDouble(rs.getString("precio")),
        rs.getString("imagen")
    );
    System.out.println("  " + p.toString());
}
```

**Archivo:** `src/GestorPanel.java` · Líneas 28–61 · Ruta: `/src/GestorPanel.java`

### 6. Alta de producto — INSERT con PreparedStatement

El formulario de alta valida el título (obligatorio) y el precio (positivo, numérico). Usa `PreparedStatement` con marcadores `?` para insertar datos de forma segura, previniendo inyección SQL. Si no se indica imagen, usa una por defecto.

```java
// src/GestorPanel.java — Líneas 108-119: INSERT preparado
String sql = "INSERT INTO producto (titulo, descripcion, precio, imagen) VALUES (?, ?, ?, ?)";
PreparedStatement pstmt = con.prepareStatement(sql);
pstmt.setString(1, titulo);
pstmt.setString(2, descripcion);
pstmt.setString(3, String.format("%.2f", precio));
pstmt.setString(4, imagen);
int filas = pstmt.executeUpdate();
```

**Archivo:** `src/GestorPanel.java` · Líneas 108–119 · Ruta: `/src/GestorPanel.java`

### 7. Eliminar producto — DELETE con confirmación

La eliminación primero busca el producto por ID con un SELECT, muestra sus datos, pide confirmación al usuario y solo entonces ejecuta el DELETE. Captura la excepción SQL por si hay pedidos asociados (integridad referencial).

```java
// src/GestorPanel.java — Líneas 148-164: DELETE con control de FK
System.out.print("  ¿Confirmar eliminacion? (s/n): ");
if (conf.equals("s") || conf.equals("si")) {
    PreparedStatement del = con.prepareStatement("DELETE FROM producto WHERE id = ?");
    del.setInt(1, id);
    del.executeUpdate();
}
```

**Archivo:** `src/GestorPanel.java` · Líneas 148–164 · Ruta: `/src/GestorPanel.java`

### 8. Listar pedidos — SELECT con JOIN

El listado de pedidos usa un JOIN entre las tablas `pedido` y `cliente` para mostrar el nombre del cliente junto con cada pedido. La función `CONCAT()` de MySQL une nombre y apellidos en un solo campo.

```java
// src/GestorPanel.java — Líneas 253-263: JOIN pedido-cliente
String sql = "SELECT p.id, p.fecha, p.cliente_id, " +
             "CONCAT(c.nombre, ' ', c.apellidos) AS nombre_cliente " +
             "FROM pedido p " +
             "JOIN cliente c ON p.cliente_id = c.id " +
             "ORDER BY p.id";
```

**Archivo:** `src/GestorPanel.java` · Líneas 253–263 · Ruta: `/src/GestorPanel.java`

### 9. Detalle de pedido — JOIN doble con cálculo de subtotales

El detalle muestra las líneas de un pedido específico usando un JOIN entre `lineapedido` y `producto`. Calcula el subtotal (cantidad × precio) de cada línea y acumula el total del pedido. Demuestra aritmética en Java con datos procedentes de SQL.

```java
// src/GestorPanel.java — Líneas 315-338: Detalle con subtotales
PreparedStatement pstmt2 = con.prepareStatement(
    "SELECT lp.cantidad, pr.titulo, pr.precio " +
    "FROM lineapedido lp JOIN producto pr ON lp.producto_id = pr.id " +
    "WHERE lp.pedido_id = ?");
double totalPedido = 0;
while (rsLineas.next()) {
    int cantidad = Integer.parseInt(rsLineas.getString("cantidad"));
    double precio = Double.parseDouble(rsLineas.getString("precio"));
    double subtotal = cantidad * precio;
    totalPedido += subtotal;
}
```

**Archivo:** `src/GestorPanel.java` · Líneas 315–338 · Ruta: `/src/GestorPanel.java`

### 10. Estadísticas — Consultas agregadas COUNT, SUM, MAX

Las estadísticas ejecutan múltiples consultas con funciones de agregación SQL: `COUNT(*)` para totales, `ORDER BY ... LIMIT 1` para máximos/mínimos, `GROUP BY` con `COUNT(*)` para el mejor cliente, y `SUM(cantidad * precio)` para facturación total.

```java
// src/GestorPanel.java — Líneas 381-409: Facturación con SUM y CAST
ResultSet rs7 = stmt.executeQuery(
    "SELECT SUM(CAST(lp.cantidad AS DECIMAL) * CAST(pr.precio AS DECIMAL(10,2))) " +
    "AS facturacion FROM lineapedido lp JOIN producto pr ON lp.producto_id = pr.id");
if (rs7.next()) {
    double facturacion = rs7.getDouble("facturacion");
    System.out.println("  Facturacion total: " + String.format("%.2f EUR", facturacion));
}
```

**Archivo:** `src/GestorPanel.java` · Líneas 381–409 · Ruta: `/src/GestorPanel.java`

### 11. Búsqueda de productos — LIKE con PreparedStatement

La búsqueda usa `LIKE` con comodines `%` en PreparedStatement para encontrar productos cuyo título o descripción contenga el texto buscado. Es case-insensitive gracias al collation de MySQL.

```java
// src/GestorPanel.java — Líneas 440-451: Búsqueda con LIKE
PreparedStatement pstmt = con.prepareStatement(
    "SELECT * FROM producto WHERE titulo LIKE ? OR descripcion LIKE ?");
pstmt.setString(1, "%" + busqueda + "%");
pstmt.setString(2, "%" + busqueda + "%");
ResultSet rs = pstmt.executeQuery();
```

**Archivo:** `src/GestorPanel.java` · Líneas 440–451 · Ruta: `/src/GestorPanel.java`

### 12. Clase Principal — Menú con 10 opciones

El punto de entrada muestra un menú organizado por secciones (Productos, Clientes, Pedidos, Resumen) con 10 opciones (0-9). Un `switch` delega cada acción en el `GestorPanel`. Al salir, cierra la conexión MySQL.

```java
// src/Principal.java — Líneas 38-73: Menú y switch
while (!salir) {
    System.out.println("  1. Listar productos");
    System.out.println("  2. Buscar producto");
    ...
    switch (opcion) {
        case "1": panel.listarProductos(); break;
        ...
        case "0": salir = true; break;
    }
}
Conexion.cerrar();
```

**Archivo:** `src/Principal.java` · Líneas 38–73 · Ruta: `/src/Principal.java`

### 13. Script SQL de referencia

Se incluye una copia del SQL de la tienda online con las 4 tablas (producto, cliente, pedido, lineapedido) y sus datos de inserción. Este fichero documenta la estructura de la BD a la que se conecta el panel y permite recrearla si es necesario.

```sql
-- sql/referencia_tiendadam.sql — Líneas 18-44: Tablas con FK
CREATE TABLE IF NOT EXISTS pedido (
  id INT AUTO_INCREMENT,
  fecha VARCHAR(255),
  cliente_id INT,
  PRIMARY KEY (id),
  CONSTRAINT fk_pedido_1 FOREIGN KEY (cliente_id) REFERENCES cliente(id)
);
```

**Archivo:** `sql/referencia_tiendadam.sql` · Líneas 18–44 · Ruta: `/sql/referencia_tiendadam.sql`

### 14. Intermodularidad — Java + MySQL + Proyecto BD

Este panel de control demuestra la conexión entre asignaturas: la base de datos fue diseñada y creada en el proyecto de Bases de Datos (tablas, relaciones FK, datos de inserción, usuario MySQL), y aquí se accede desde Java con JDBC. El panel consume la misma BD que utiliza la tienda online PHP, mostrando cómo diferentes tecnologías pueden compartir los mismos datos.

## Presentación del proyecto

Este es un panel de control de consola desarrollado en Java que gestiona la tienda online creada en el proyecto de Bases de Datos. El panel se conecta a la base de datos `tiendadam` en MySQL mediante JDBC y permite administrar productos, clientes y pedidos desde la línea de comandos.

El menú ofrece 9 funcionalidades agrupadas en 4 secciones: en Productos se pueden listar, buscar, añadir y eliminar artículos del catálogo. En Clientes se puede ver el listado y registrar nuevos. En Pedidos se pueden ver todos los pedidos con el nombre del cliente (usando JOIN SQL) y consultar el detalle de cada uno con sus líneas, cantidades, precios y subtotales. Finalmente, las Estadísticas muestran un resumen con totales, el producto más caro y más barato, el cliente con más pedidos y la facturación acumulada.

La arquitectura separa responsabilidades en 6 clases Java: `Conexion` gestiona la conexión MySQL con patrón Singleton, `Producto`, `Cliente` y `Pedido` son los modelos de datos que mapean las tablas SQL, `GestorPanel` contiene toda la lógica CRUD con PreparedStatement para seguridad, y `Principal` gestiona el menú.

Lo más relevante es la intermodularidad: este proyecto Java trabaja con los mismos datos que el proyecto PHP de la tienda online y que el proyecto SQL de Bases de Datos. Las tres asignaturas convergen en la misma base de datos `tiendadam`, demostrando cómo las diferentes capas de una aplicación real se conectan entre sí.

## Conclusión

Este panel de control demuestra las competencias fundamentales de Programación: diseño orientado a objetos con clases especializadas, conexión a bases de datos mediante JDBC, consultas SQL con JOINs y funciones de agregación ejecutadas desde Java, validación de entrada del usuario, uso de PreparedStatement para prevenir inyección SQL, y control de excepciones. La conexión con el proyecto de Bases de Datos muestra la intermodularidad entre asignaturas y cómo un sistema real se compone de múltiples piezas que colaboran a través de una base de datos compartida.
