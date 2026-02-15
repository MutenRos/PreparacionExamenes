import java.util.Scanner;

/**
 * Clase Principal — Punto de entrada del Panel de Control.
 * Muestra el menu principal con las opciones de gestion
 * de la tienda online y delega en GestorPanel.
 *
 * Este panel de control se conecta a la base de datos MySQL
 * 'tiendadam' creada en el proyecto de Bases de Datos
 * (Bases-de-datos-001-Proyecto-tienda-online).
 *
 * Requisitos para ejecutar:
 *   - MySQL Server arrancado con la BD 'tiendadam'
 *   - mysql-connector-j.jar en el classpath
 *   - Compilar: javac -cp .:mysql-connector-j.jar src/*.java
 *   - Ejecutar: java -cp .:mysql-connector-j.jar Principal
 *
 * @author Alumno
 * @version 1.0
 */
public class Principal {

    public static void main(String[] args) {

        Scanner scanner = new Scanner(System.in);
        GestorPanel panel = new GestorPanel();
        boolean salir = false;

        // Bienvenida
        System.out.println();
        System.out.println("  ╔══════════════════════════════════════════╗");
        System.out.println("  ║   PANEL DE CONTROL — TIENDA ONLINE      ║");
        System.out.println("  ║   Base de datos: tiendadam               ║");
        System.out.println("  ╚══════════════════════════════════════════╝");

        // Bucle principal del menu
        while (!salir) {
            System.out.println();
            System.out.println("  ═══════════════════════════════════════════");
            System.out.println("            MENU PANEL DE CONTROL");
            System.out.println("  ═══════════════════════════════════════════");
            System.out.println("  --- PRODUCTOS ---");
            System.out.println("  1. Listar productos");
            System.out.println("  2. Buscar producto");
            System.out.println("  3. Anadir producto");
            System.out.println("  4. Eliminar producto");
            System.out.println("  --- CLIENTES ---");
            System.out.println("  5. Listar clientes");
            System.out.println("  6. Registrar cliente");
            System.out.println("  --- PEDIDOS ---");
            System.out.println("  7. Listar pedidos");
            System.out.println("  8. Detalle de pedido");
            System.out.println("  --- RESUMEN ---");
            System.out.println("  9. Estadisticas de la tienda");
            System.out.println("  0. Salir");
            System.out.println("  ═══════════════════════════════════════════");
            System.out.print("  Opcion: ");

            String opcion = scanner.nextLine().trim();

            switch (opcion) {
                case "1": panel.listarProductos(); break;
                case "2": panel.buscarProducto(scanner); break;
                case "3": panel.altaProducto(scanner); break;
                case "4": panel.eliminarProducto(scanner); break;
                case "5": panel.listarClientes(); break;
                case "6": panel.altaCliente(scanner); break;
                case "7": panel.listarPedidos(); break;
                case "8": panel.detallePedido(scanner); break;
                case "9": panel.mostrarEstadisticas(); break;
                case "0": salir = true; break;
                default:
                    System.out.println("  [!] Opcion no valida. Elige del 0 al 9.");
            }
        }

        // Cerrar conexion y despedida
        Conexion.cerrar();
        System.out.println();
        System.out.println("  ╔══════════════════════════════════════════╗");
        System.out.println("  ║   Panel de control cerrado.              ║");
        System.out.println("  ║   Hasta la proxima!                      ║");
        System.out.println("  ╚══════════════════════════════════════════╝");
        System.out.println();

        scanner.close();
    }
}
