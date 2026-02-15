# CRM de Clientes — Proyecto Formularios en Java

![CRM de Clientes](https://mutenros.github.io/Programacion-001-Proyecto-formularios-CRM/)

## Introducción

Este proyecto es un sistema CRM (Customer Relationship Management) de gestión de clientes desarrollado en Java como aplicación de consola. Permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre una base de datos de clientes mediante formularios de texto interactivos. Los datos se persisten automáticamente en un fichero CSV, lo que permite mantener la información entre sesiones. El proyecto aplica conceptos fundamentales de Programación Orientada a Objetos: encapsulamiento, clases, constructores, ArrayList, entrada/salida de ficheros, validación de datos y estructura modular.

## Desarrollo

### 1. Clase Cliente — Modelo de datos con OOP

La clase `Cliente` encapsula los datos de cada cliente con atributos privados, getters, setters y un constructor completo. Implementa `Serializable` para posibilitar futuras ampliaciones de persistencia y métodos de conversión CSV para la lectura/escritura en fichero.

```java
// src/Cliente.java — Líneas 12-24: Atributos encapsulados
public class Cliente implements Serializable {
    private static final long serialVersionUID = 1L;
    private int id;
    private String nombre;
    private String email;
    private String telefono;
    private String empresa;
    private String categoria; // "particular", "empresa" o "vip"
}
```

**Archivo:** `src/Cliente.java` · Líneas 12–24 · Ruta: `/src/Cliente.java`

### 2. Método toString() — Formato tabla para consola

El método `toString()` sobreescribe el de la clase Object para generar una representación formateada del cliente que se alinea en columnas. Usa `String.format()` con ancho fijo para que la tabla quede alineada visualmente en la consola.

```java
// src/Cliente.java — Líneas 85-91: toString con formato tabla
@Override
public String toString() {
    return "| " + String.format("%-4d", id) +
           " | " + String.format("%-20s", nombre) +
           " | " + String.format("%-25s", email) +
           " | " + String.format("%-12s", telefono) +
           " | " + String.format("%-15s", empresa) +
           " | " + String.format("%-10s", categoria) + " |";
}
```

**Archivo:** `src/Cliente.java` · Líneas 85–91 · Ruta: `/src/Cliente.java`

### 3. Conversión CSV — Persistencia sin base de datos

Los métodos `toCSV()` y `fromCSV()` permiten convertir objetos Cliente a líneas de texto y viceversa, usando punto y coma como separador. El método estático `fromCSV()` incluye validación del número de campos y control de excepciones con `try-catch` para parseo de enteros.

```java
// src/Cliente.java — Líneas 106-124: Lectura desde CSV con validación
public static Cliente fromCSV(String linea) {
    String[] partes = linea.split(";");
    if (partes.length != 6) {
        System.out.println("  [!] Linea con formato incorrecto: " + linea);
        return null;
    }
    try {
        int id = Integer.parseInt(partes[0].trim());
        ...
        return new Cliente(id, nombre, email, telefono, empresa, categoria);
    } catch (NumberFormatException e) {
        return null;
    }
}
```

**Archivo:** `src/Cliente.java` · Líneas 106–124 · Ruta: `/src/Cliente.java`

### 4. GestorCRM — Alta de clientes con validación

El método `altaCliente()` implementa un formulario interactivo que pide datos por consola con validaciones: nombre obligatorio (bucle while), email con comprobación de `@`, teléfono con mínimo 9 caracteres, y categoría mediante submenú de opciones. Los datos se guardan automáticamente tras cada alta.

```java
// src/GestorCRM.java — Líneas 44-95: Formulario de alta con validaciones
public void altaCliente(Scanner scanner) {
    String nombre = "";
    while (nombre.isEmpty()) {
        System.out.print("  Nombre completo: ");
        nombre = scanner.nextLine().trim();
        if (nombre.isEmpty()) {
            System.out.println("  [!] El nombre no puede estar vacio.");
        }
    }
    String email = "";
    while (email.isEmpty() || !email.contains("@")) {
        System.out.print("  Email: ");
        email = scanner.nextLine().trim();
    }
    ...
    guardarDatos();
}
```

**Archivo:** `src/GestorCRM.java` · Líneas 44–95 · Ruta: `/src/GestorCRM.java`

### 5. Listado de clientes — Tabla formateada

El método `listarClientes()` recorre el ArrayList con un `for-each` y muestra los datos en una tabla con bordes Unicode. Comprueba si la lista está vacía antes de mostrar la tabla, mostrando un mensaje informativo si no hay datos.

```java
// src/GestorCRM.java — Líneas 101-127: Listado con tabla formateada
public void listarClientes() {
    if (clientes.isEmpty()) {
        System.out.println("  [i] No hay clientes registrados en el CRM.");
        return;
    }
    for (Cliente c : clientes) {
        System.out.println("  " + c.toString());
    }
    System.out.println("  Total: " + clientes.size() + " cliente(s)");
}
```

**Archivo:** `src/GestorCRM.java` · Líneas 101–127 · Ruta: `/src/GestorCRM.java`

### 6. Búsqueda de clientes — Filtrado con ArrayList

La búsqueda permite encontrar clientes por nombre o email. Utiliza `toLowerCase()` para hacer la comparación case-insensitive y `contains()` para buscar coincidencias parciales. Los resultados se almacenan en un ArrayList auxiliar.

```java
// src/GestorCRM.java — Líneas 139-159: Búsqueda con filtro
ArrayList<Cliente> resultados = new ArrayList<Cliente>();
for (Cliente c : clientes) {
    if (c.getNombre().toLowerCase().contains(busqueda) ||
        c.getEmail().toLowerCase().contains(busqueda)) {
        resultados.add(c);
    }
}
```

**Archivo:** `src/GestorCRM.java` · Líneas 139–159 · Ruta: `/src/GestorCRM.java`

### 7. Modificación de clientes — UPDATE interactivo

El formulario de modificación busca primero por ID, muestra los datos actuales entre corchetes como referencia, y permite cambiar cada campo individualmente. Si el usuario deja un campo vacío, se mantiene el valor anterior. Incluye validación de email y teléfono en los campos modificados.

```java
// src/GestorCRM.java — Líneas 173-213: Formulario de modificación
System.out.print("  Nuevo nombre [" + cliente.getNombre() + "]: ");
String nombre = scanner.nextLine().trim();
if (!nombre.isEmpty()) {
    cliente.setNombre(nombre);
}
```

**Archivo:** `src/GestorCRM.java` · Líneas 173–213 · Ruta: `/src/GestorCRM.java`

### 8. Eliminación con confirmación — DELETE seguro

La eliminación requiere confirmación del usuario ("s/n") antes de proceder. Esto previene borrados accidentales y es una buena práctica de UX en aplicaciones de gestión de datos.

```java
// src/GestorCRM.java — Líneas 225-247: Eliminación con confirmación
System.out.print("  ¿Confirmar eliminacion? (s/n): ");
String confirmacion = scanner.nextLine().trim().toLowerCase();
if (confirmacion.equals("s") || confirmacion.equals("si")) {
    clientes.remove(cliente);
    guardarDatos();
}
```

**Archivo:** `src/GestorCRM.java` · Líneas 225–247 · Ruta: `/src/GestorCRM.java`

### 9. Estadísticas con switch — Conteo por categoría

El método de estadísticas recorre todos los clientes y usa un `switch` para contar cuántos hay de cada categoría (particular, empresa, VIP). Muestra un resumen numérico útil para la gestión del CRM.

```java
// src/GestorCRM.java — Líneas 255-280: Estadísticas con switch
int particulares = 0, empresas = 0, vips = 0;
for (Cliente c : clientes) {
    switch (c.getCategoria().toLowerCase()) {
        case "particular": particulares++; break;
        case "empresa": empresas++; break;
        case "vip": vips++; break;
    }
}
```

**Archivo:** `src/GestorCRM.java` · Líneas 255–280 · Ruta: `/src/GestorCRM.java`

### 10. Persistencia en fichero CSV — E/S con Java

Los métodos `guardarDatos()` y `cargarDatos()` implementan la persistencia usando `PrintWriter`/`FileWriter` para escritura y `BufferedReader`/`FileReader` para lectura. El método de carga actualiza automáticamente el `siguienteId` para no repetir IDs tras reiniciar el programa.

```java
// src/GestorCRM.java — Líneas 347-388: Carga de datos con BufferedReader
BufferedReader lector = new BufferedReader(new FileReader(fichero));
String linea;
while ((linea = lector.readLine()) != null) {
    if (linea.trim().isEmpty()) continue;
    Cliente c = Cliente.fromCSV(linea);
    if (c != null) {
        clientes.add(c);
        if (c.getId() >= siguienteId) {
            siguienteId = c.getId() + 1;
        }
    }
}
```

**Archivo:** `src/GestorCRM.java` · Líneas 347–388 · Ruta: `/src/GestorCRM.java`

### 11. Clase Principal — Menú y bucle del programa

La clase `Principal` contiene el `main()` que muestra el menú con 7 opciones (0-6), lee la selección del usuario y la procesa con un `switch`. El bucle `while (!salir)` mantiene el programa activo hasta que el usuario elige salir.

```java
// src/Principal.java — Líneas 47-77: Menú principal con switch
while (!salir) {
    System.out.println("  1. Dar de alta un cliente");
    System.out.println("  2. Listar todos los clientes");
    ...
    String opcion = scanner.nextLine().trim();
    switch (opcion) {
        case "1": crm.altaCliente(scanner); break;
        case "2": crm.listarClientes(); break;
        ...
        case "0": salir = true; break;
    }
}
```

**Archivo:** `src/Principal.java` · Líneas 47–77 · Ruta: `/src/Principal.java`

### 12. Fichero de datos CSV — Datos de ejemplo

El fichero `datos/clientes.csv` almacena los clientes en formato texto plano, un cliente por línea, con campos separados por punto y coma. Incluye 6 clientes de ejemplo con distintas categorías para poder probar todas las funcionalidades del CRM.

```csv
1;Maria Garcia;maria.garcia@email.com;612345678;Consultora López;empresa
2;Carlos Ruiz;carlos.ruiz@gmail.com;698765432;-;particular
3;Ana Martinez;ana.martinez@empresa.es;611222333;TechSoluciones;vip
```

**Archivo:** `datos/clientes.csv` · Líneas 1–6 · Ruta: `/datos/clientes.csv`

## Presentación

Este proyecto es un CRM de gestión de clientes desarrollado completamente en Java como aplicación de consola. El usuario interactúa con el programa a través de un menú con 6 opciones: dar de alta clientes rellenando un formulario con validaciones, listar todos los clientes en una tabla formateada, buscar por nombre o email, modificar datos existentes, eliminar con confirmación, y ver estadísticas por categoría.

La arquitectura sigue los principios de Programación Orientada a Objetos: la clase `Cliente` encapsula los datos con atributos privados y métodos de acceso, mientras que `GestorCRM` contiene toda la lógica de negocio (CRUD) y la persistencia. La clase `Principal` solo se ocupa del menú y la interacción con el usuario.

Los datos se guardan automáticamente en un fichero CSV cada vez que se realiza una modificación. Al arrancar el programa, los datos se cargan del fichero para mantener la información entre sesiones. Esto demuestra el manejo de entrada/salida de ficheros en Java con BufferedReader y PrintWriter.

Las validaciones del formulario aseguran que el nombre no esté vacío, que el email contenga una arroba, y que el teléfono tenga al menos 9 caracteres. La eliminación de clientes requiere confirmación por parte del usuario para evitar borrados accidentales.

## Conclusión

Este CRM de clientes demuestra las competencias fundamentales de la asignatura de Programación: diseño de clases con encapsulamiento, uso de ArrayList para colecciones dinámicas, control de flujo con bucles y switch, validación de entrada del usuario, manejo de excepciones con try-catch, y persistencia de datos mediante lectura/escritura de ficheros. El resultado es una aplicación funcional y completa que podría escalarse fácilmente añadiendo nuevas funcionalidades como exportación a otros formatos, ordenación de clientes o autenticación de usuarios.
