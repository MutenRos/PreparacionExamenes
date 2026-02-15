import java.sql.*;
import java.util.ArrayList;
import java.util.Scanner;

/**
 * Clase GestorPanel — Logica principal del panel de control.
 * Contiene todas las operaciones CRUD sobre la base de datos
 * de la tienda online: productos, clientes, pedidos y estadisticas.
 *
 * Usa consultas SQL preparadas (PreparedStatement) para evitar
 * inyeccion SQL y consultas directas (Statement) para lecturas.
 *
 * @author Alumno
 * @version 1.0
 */
public class GestorPanel {

    // ============================================================
    // GESTION DE PRODUCTOS
    // ============================================================

    /**
     * Lista todos los productos de la tienda.
     * Ejecuta: SELECT * FROM producto ORDER BY id
     */
    public void listarProductos() {
        System.out.println();
        Connection con = Conexion.obtener();
        if (con == null) return;

        try {
            Statement stmt = con.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT * FROM producto ORDER BY id");

            System.out.println("  ╔═══════════════════════════════════════════════════════════════════════════════════════════════════════╗");
            System.out.println("  ║                                    CATALOGO DE PRODUCTOS                                             ║");
            System.out.println("  ╠═══════════════════════════════════════════════════════════════════════════════════════════════════════╣");
            System.out.println("  | " + String.format("%-4s", "ID") +
                               " | " + String.format("%-22s", "TITULO") +
                               " | " + String.format("%-30s", "DESCRIPCION") +
                               " | " + String.format("%10s", "PRECIO") +
                               " | " + String.format("%-20s", "IMAGEN") + " |");
            System.out.println("  |------|------------------------|--------------------------------|------------|----------------------|");

            int total = 0;
            while (rs.next()) {
                // Leer cada columna del ResultSet
                Producto p = new Producto(
                    rs.getInt("id"),
                    rs.getString("titulo"),
                    rs.getString("descripcion"),
                    Double.parseDouble(rs.getString("precio")),
                    rs.getString("imagen")
                );
                System.out.println("  " + p.toString());
                total++;
            }

            System.out.println("  ╚═══════════════════════════════════════════════════════════════════════════════════════════════════════╝");
            System.out.println("  Total: " + total + " producto(s)");

            rs.close();
            stmt.close();

        } catch (SQLException e) {
            System.out.println("  [!] Error SQL: " + e.getMessage());
        }
    }

    /**
     * Formulario para dar de alta un nuevo producto.
     * Usa PreparedStatement para insertar de forma segura.
     *
     * @param scanner Scanner para leer entrada del usuario
     */
    public void altaProducto(Scanner scanner) {
        System.out.println();
        System.out.println("  ╔══════════════════════════════════════╗");
        System.out.println("  ║   FORMULARIO: NUEVO PRODUCTO         ║");
        System.out.println("  ╚══════════════════════════════════════╝");
        System.out.println();

        Connection con = Conexion.obtener();
        if (con == null) return;

        // Pedir titulo (obligatorio)
        String titulo = "";
        while (titulo.isEmpty()) {
            System.out.print("  Titulo del producto: ");
            titulo = scanner.nextLine().trim();
            if (titulo.isEmpty()) {
                System.out.println("  [!] El titulo no puede estar vacio.");
            }
        }

        // Pedir descripcion
        System.out.print("  Descripcion: ");
        String descripcion = scanner.nextLine().trim();

        // Pedir precio (debe ser un numero positivo)
        double precio = 0;
        while (precio <= 0) {
            System.out.print("  Precio (EUR): ");
            try {
                precio = Double.parseDouble(scanner.nextLine().trim());
                if (precio <= 0) {
                    System.out.println("  [!] El precio debe ser mayor que 0.");
                }
            } catch (NumberFormatException e) {
                System.out.println("  [!] Introduce un numero valido (ej: 19.99).");
            }
        }

        // Pedir imagen (nombre del fichero)
        System.out.print("  Nombre de imagen (ej: camiseta.jpg): ");
        String imagen = scanner.nextLine().trim();
        if (imagen.isEmpty()) {
            imagen = "producto.webp"; // Imagen por defecto
        }

        try {
            // INSERT con PreparedStatement (previene inyeccion SQL)
            String sql = "INSERT INTO producto (titulo, descripcion, precio, imagen) VALUES (?, ?, ?, ?)";
            PreparedStatement pstmt = con.prepareStatement(sql);
            pstmt.setString(1, titulo);
            pstmt.setString(2, descripcion);
            pstmt.setString(3, String.format("%.2f", precio));
            pstmt.setString(4, imagen);

            int filas = pstmt.executeUpdate();
            if (filas > 0) {
                System.out.println("  [OK] Producto '" + titulo + "' anadido al catalogo.");
            }

            pstmt.close();

        } catch (SQLException e) {
            System.out.println("  [!] Error al insertar producto: " + e.getMessage());
        }
    }

    /**
     * Elimina un producto por su ID.
     * Pide confirmacion antes de ejecutar el DELETE.
     *
     * @param scanner Scanner para leer entrada del usuario
     */
    public void eliminarProducto(Scanner scanner) {
        System.out.println();
        System.out.print("  ID del producto a eliminar: ");
        int id = leerEntero(scanner);
        if (id < 0) return;

        Connection con = Conexion.obtener();
        if (con == null) return;

        try {
            // Primero comprobar que el producto existe
            PreparedStatement check = con.prepareStatement("SELECT titulo FROM producto WHERE id = ?");
            check.setInt(1, id);
            ResultSet rs = check.executeQuery();

            if (!rs.next()) {
                System.out.println("  [!] No existe un producto con ID " + id);
                rs.close();
                check.close();
                return;
            }

            String titulo = rs.getString("titulo");
            rs.close();
            check.close();

            // Pedir confirmacion
            System.out.println("  Producto: " + titulo);
            System.out.print("  ¿Confirmar eliminacion? (s/n): ");
            String conf = scanner.nextLine().trim().toLowerCase();

            if (conf.equals("s") || conf.equals("si")) {
                PreparedStatement del = con.prepareStatement("DELETE FROM producto WHERE id = ?");
                del.setInt(1, id);
                del.executeUpdate();
                del.close();
                System.out.println("  [OK] Producto '" + titulo + "' eliminado.");
            } else {
                System.out.println("  [i] Eliminacion cancelada.");
            }

        } catch (SQLException e) {
            System.out.println("  [!] Error SQL: " + e.getMessage());
            System.out.println("      (Puede haber pedidos asociados a este producto)");
        }
    }

    // ============================================================
    // GESTION DE CLIENTES
    // ============================================================

    /**
     * Lista todos los clientes registrados.
     * Ejecuta: SELECT * FROM cliente ORDER BY id
     */
    public void listarClientes() {
        System.out.println();
        Connection con = Conexion.obtener();
        if (con == null) return;

        try {
            Statement stmt = con.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT * FROM cliente ORDER BY id");

            System.out.println("  ╔════════════════════════════════════════════════════════════════════════════╗");
            System.out.println("  ║                          LISTADO DE CLIENTES                              ║");
            System.out.println("  ╠════════════════════════════════════════════════════════════════════════════╣");
            System.out.println("  | " + String.format("%-4s", "ID") +
                               " | " + String.format("%-15s", "NOMBRE") +
                               " | " + String.format("%-20s", "APELLIDOS") +
                               " | " + String.format("%-25s", "EMAIL") + " |");
            System.out.println("  |------|-----------------|----------------------|---------------------------|");

            int total = 0;
            while (rs.next()) {
                Cliente c = new Cliente(
                    rs.getInt("id"),
                    rs.getString("nombre"),
                    rs.getString("apellidos"),
                    rs.getString("email")
                );
                System.out.println("  " + c.toString());
                total++;
            }

            System.out.println("  ╚════════════════════════════════════════════════════════════════════════════╝");
            System.out.println("  Total: " + total + " cliente(s)");

            rs.close();
            stmt.close();

        } catch (SQLException e) {
            System.out.println("  [!] Error SQL: " + e.getMessage());
        }
    }

    /**
     * Formulario para registrar un nuevo cliente.
     * Valida nombre y formato de email.
     *
     * @param scanner Scanner para leer entrada del usuario
     */
    public void altaCliente(Scanner scanner) {
        System.out.println();
        System.out.println("  ╔══════════════════════════════════════╗");
        System.out.println("  ║   FORMULARIO: NUEVO CLIENTE          ║");
        System.out.println("  ╚══════════════════════════════════════╝");
        System.out.println();

        Connection con = Conexion.obtener();
        if (con == null) return;

        // Pedir nombre (obligatorio)
        String nombre = "";
        while (nombre.isEmpty()) {
            System.out.print("  Nombre: ");
            nombre = scanner.nextLine().trim();
            if (nombre.isEmpty()) {
                System.out.println("  [!] El nombre no puede estar vacio.");
            }
        }

        // Pedir apellidos
        System.out.print("  Apellidos: ");
        String apellidos = scanner.nextLine().trim();

        // Pedir email (debe contener @)
        String email = "";
        while (email.isEmpty() || !email.contains("@")) {
            System.out.print("  Email: ");
            email = scanner.nextLine().trim();
            if (!email.contains("@")) {
                System.out.println("  [!] El email debe contener '@'.");
            }
        }

        try {
            String sql = "INSERT INTO cliente (nombre, apellidos, email) VALUES (?, ?, ?)";
            PreparedStatement pstmt = con.prepareStatement(sql);
            pstmt.setString(1, nombre);
            pstmt.setString(2, apellidos);
            pstmt.setString(3, email);

            int filas = pstmt.executeUpdate();
            if (filas > 0) {
                System.out.println("  [OK] Cliente '" + nombre + " " + apellidos + "' registrado.");
            }

            pstmt.close();

        } catch (SQLException e) {
            System.out.println("  [!] Error al insertar cliente: " + e.getMessage());
        }
    }

    // ============================================================
    // GESTION DE PEDIDOS
    // ============================================================

    /**
     * Lista todos los pedidos con el nombre del cliente (JOIN).
     * Ejecuta: SELECT p.*, c.nombre, c.apellidos FROM pedido p
     *          JOIN cliente c ON p.cliente_id = c.id
     */
    public void listarPedidos() {
        System.out.println();
        Connection con = Conexion.obtener();
        if (con == null) return;

        try {
            // Consulta con JOIN para obtener el nombre del cliente
            String sql = "SELECT p.id, p.fecha, p.cliente_id, " +
                         "CONCAT(c.nombre, ' ', c.apellidos) AS nombre_cliente " +
                         "FROM pedido p " +
                         "JOIN cliente c ON p.cliente_id = c.id " +
                         "ORDER BY p.id";

            Statement stmt = con.createStatement();
            ResultSet rs = stmt.executeQuery(sql);

            System.out.println("  ╔═══════════════════════════════════════════════════════════╗");
            System.out.println("  ║                    LISTADO DE PEDIDOS                     ║");
            System.out.println("  ╠═══════════════════════════════════════════════════════════╣");
            System.out.println("  | " + String.format("%-4s", "ID") +
                               " | " + String.format("%-12s", "FECHA") +
                               " | " + String.format("%-4s", "CLI") +
                               " | " + String.format("%-25s", "NOMBRE CLIENTE") + " |");
            System.out.println("  |------|--------------|------|---------------------------|");

            int total = 0;
            while (rs.next()) {
                Pedido p = new Pedido(
                    rs.getInt("id"),
                    rs.getString("fecha"),
                    rs.getInt("cliente_id"),
                    rs.getString("nombre_cliente")
                );
                System.out.println("  " + p.toString());
                total++;
            }

            System.out.println("  ╚═══════════════════════════════════════════════════════════╝");
            System.out.println("  Total: " + total + " pedido(s)");

            rs.close();
            stmt.close();

        } catch (SQLException e) {
            System.out.println("  [!] Error SQL: " + e.getMessage());
        }
    }

    /**
     * Muestra el detalle de un pedido: sus lineas con producto, cantidad y subtotal.
     * Usa JOIN entre lineapedido y producto para obtener titulo y precio.
     *
     * @param scanner Scanner para leer el ID del pedido
     */
    public void detallePedido(Scanner scanner) {
        System.out.println();
        System.out.print("  ID del pedido a consultar: ");
        int id = leerEntero(scanner);
        if (id < 0) return;

        Connection con = Conexion.obtener();
        if (con == null) return;

        try {
            // Datos del pedido con JOIN a cliente
            PreparedStatement pstmt = con.prepareStatement(
                "SELECT p.fecha, CONCAT(c.nombre, ' ', c.apellidos) AS cliente " +
                "FROM pedido p JOIN cliente c ON p.cliente_id = c.id WHERE p.id = ?");
            pstmt.setInt(1, id);
            ResultSet rsPedido = pstmt.executeQuery();

            if (!rsPedido.next()) {
                System.out.println("  [!] No existe un pedido con ID " + id);
                rsPedido.close();
                pstmt.close();
                return;
            }

            String fecha = rsPedido.getString("fecha");
            String cliente = rsPedido.getString("cliente");
            rsPedido.close();
            pstmt.close();

            System.out.println();
            System.out.println("  ╔══════════════════════════════════════════════════════════════════╗");
            System.out.println("  ║  DETALLE DEL PEDIDO #" + id + "                                          ║");
            System.out.println("  ╠══════════════════════════════════════════════════════════════════╣");
            System.out.println("  Fecha:   " + fecha);
            System.out.println("  Cliente: " + cliente);
            System.out.println();

            // Lineas del pedido con JOIN a producto
            PreparedStatement pstmt2 = con.prepareStatement(
                "SELECT lp.cantidad, pr.titulo, pr.precio " +
                "FROM lineapedido lp " +
                "JOIN producto pr ON lp.producto_id = pr.id " +
                "WHERE lp.pedido_id = ?");
            pstmt2.setInt(1, id);
            ResultSet rsLineas = pstmt2.executeQuery();

            System.out.println("  | " + String.format("%-22s", "PRODUCTO") +
                               " | " + String.format("%-8s", "CANT.") +
                               " | " + String.format("%-10s", "PRECIO") +
                               " | " + String.format("%-10s", "SUBTOTAL") + " |");
            System.out.println("  |------------------------|----------|------------|------------|");

            double totalPedido = 0;
            while (rsLineas.next()) {
                String titulo = rsLineas.getString("titulo");
                int cantidad = Integer.parseInt(rsLineas.getString("cantidad"));
                double precio = Double.parseDouble(rsLineas.getString("precio"));
                double subtotal = cantidad * precio;
                totalPedido += subtotal;

                System.out.println("  | " + String.format("%-22s", titulo) +
                                   " | " + String.format("%-8d", cantidad) +
                                   " | " + String.format("%8.2f €", precio) +
                                   " | " + String.format("%8.2f €", subtotal) + " |");
            }

            System.out.println("  |------------------------|----------|------------|------------|");
            System.out.println("  |                                     TOTAL: " +
                               String.format("%8.2f €", totalPedido) + " |");
            System.out.println("  ╚══════════════════════════════════════════════════════════════════╝");

            rsLineas.close();
            pstmt2.close();

        } catch (SQLException e) {
            System.out.println("  [!] Error SQL: " + e.getMessage());
        }
    }

    // ============================================================
    // ESTADISTICAS DE LA TIENDA
    // ============================================================

    /**
     * Muestra estadisticas generales de la tienda:
     * - Total de productos, clientes, pedidos
     * - Producto mas caro y mas barato
     * - Cliente con mas pedidos
     * - Facturacion total
     */
    public void mostrarEstadisticas() {
        System.out.println();
        Connection con = Conexion.obtener();
        if (con == null) return;

        System.out.println("  ╔══════════════════════════════════════╗");
        System.out.println("  ║     ESTADISTICAS DE LA TIENDA       ║");
        System.out.println("  ╚══════════════════════════════════════╝");
        System.out.println();

        try {
            Statement stmt = con.createStatement();

            // Total de productos
            ResultSet rs1 = stmt.executeQuery("SELECT COUNT(*) AS total FROM producto");
            if (rs1.next()) {
                System.out.println("  Productos en catalogo:  " + rs1.getInt("total"));
            }
            rs1.close();

            // Total de clientes
            ResultSet rs2 = stmt.executeQuery("SELECT COUNT(*) AS total FROM cliente");
            if (rs2.next()) {
                System.out.println("  Clientes registrados:   " + rs2.getInt("total"));
            }
            rs2.close();

            // Total de pedidos
            ResultSet rs3 = stmt.executeQuery("SELECT COUNT(*) AS total FROM pedido");
            if (rs3.next()) {
                System.out.println("  Pedidos realizados:     " + rs3.getInt("total"));
            }
            rs3.close();

            System.out.println("  ─────────────────────────────────────");

            // Producto mas caro
            ResultSet rs4 = stmt.executeQuery(
                "SELECT titulo, precio FROM producto ORDER BY CAST(precio AS DECIMAL(10,2)) DESC LIMIT 1");
            if (rs4.next()) {
                System.out.println("  Producto mas caro:      " +
                    rs4.getString("titulo") + " (" + rs4.getString("precio") + " EUR)");
            }
            rs4.close();

            // Producto mas barato
            ResultSet rs5 = stmt.executeQuery(
                "SELECT titulo, precio FROM producto ORDER BY CAST(precio AS DECIMAL(10,2)) ASC LIMIT 1");
            if (rs5.next()) {
                System.out.println("  Producto mas barato:    " +
                    rs5.getString("titulo") + " (" + rs5.getString("precio") + " EUR)");
            }
            rs5.close();

            System.out.println("  ─────────────────────────────────────");

            // Cliente con mas pedidos
            ResultSet rs6 = stmt.executeQuery(
                "SELECT CONCAT(c.nombre, ' ', c.apellidos) AS cliente, COUNT(*) AS num " +
                "FROM pedido p JOIN cliente c ON p.cliente_id = c.id " +
                "GROUP BY p.cliente_id ORDER BY num DESC LIMIT 1");
            if (rs6.next()) {
                System.out.println("  Mejor cliente:          " +
                    rs6.getString("cliente") + " (" + rs6.getInt("num") + " pedidos)");
            }
            rs6.close();

            // Facturacion total
            ResultSet rs7 = stmt.executeQuery(
                "SELECT SUM(CAST(lp.cantidad AS DECIMAL) * CAST(pr.precio AS DECIMAL(10,2))) AS facturacion " +
                "FROM lineapedido lp JOIN producto pr ON lp.producto_id = pr.id");
            if (rs7.next()) {
                double facturacion = rs7.getDouble("facturacion");
                System.out.println("  Facturacion total:      " + String.format("%.2f EUR", facturacion));
            }
            rs7.close();

            stmt.close();

        } catch (SQLException e) {
            System.out.println("  [!] Error SQL: " + e.getMessage());
        }
    }

    // ============================================================
    // BUSQUEDA DE PRODUCTOS
    // ============================================================

    /**
     * Busca productos por titulo o descripcion.
     * Usa LIKE con comodines para busqueda parcial.
     *
     * @param scanner Scanner para leer el texto de busqueda
     */
    public void buscarProducto(Scanner scanner) {
        System.out.println();
        System.out.print("  Buscar producto (titulo o descripcion): ");
        String busqueda = scanner.nextLine().trim();

        if (busqueda.isEmpty()) {
            System.out.println("  [!] Debes escribir algo para buscar.");
            return;
        }

        Connection con = Conexion.obtener();
        if (con == null) return;

        try {
            // Busqueda con LIKE y comodines %
            PreparedStatement pstmt = con.prepareStatement(
                "SELECT * FROM producto WHERE titulo LIKE ? OR descripcion LIKE ?");
            pstmt.setString(1, "%" + busqueda + "%");
            pstmt.setString(2, "%" + busqueda + "%");

            ResultSet rs = pstmt.executeQuery();

            int encontrados = 0;
            while (rs.next()) {
                if (encontrados == 0) {
                    System.out.println("  Resultados:");
                    System.out.println();
                }
                Producto p = new Producto(
                    rs.getInt("id"),
                    rs.getString("titulo"),
                    rs.getString("descripcion"),
                    Double.parseDouble(rs.getString("precio")),
                    rs.getString("imagen")
                );
                System.out.println("  " + p.toString());
                encontrados++;
            }

            if (encontrados == 0) {
                System.out.println("  [i] No se encontraron productos con '" + busqueda + "'.");
            } else {
                System.out.println("  Encontrados: " + encontrados + " producto(s)");
            }

            rs.close();
            pstmt.close();

        } catch (SQLException e) {
            System.out.println("  [!] Error SQL: " + e.getMessage());
        }
    }

    // ============================================================
    // METODO AUXILIAR
    // ============================================================

    /**
     * Lee un numero entero de la entrada del usuario.
     * Devuelve -1 si el texto no es un numero valido.
     */
    private int leerEntero(Scanner scanner) {
        String texto = scanner.nextLine().trim();
        try {
            return Integer.parseInt(texto);
        } catch (NumberFormatException e) {
            System.out.println("  [!] '" + texto + "' no es un numero valido.");
            return -1;
        }
    }
}
