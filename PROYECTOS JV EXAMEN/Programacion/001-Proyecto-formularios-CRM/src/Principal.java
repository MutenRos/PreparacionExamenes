import java.util.Scanner;

/**
 * Clase Principal — Punto de entrada de la aplicacion CRM.
 * Muestra el menu principal y gestiona la navegacion del usuario
 * por las diferentes opciones del CRM de clientes.
 * 
 * Este es un programa de consola que permite gestionar clientes
 * mediante formularios de texto: alta, listado, busqueda,
 * modificacion, eliminacion y estadisticas.
 * 
 * Los datos se guardan automaticamente en un fichero CSV
 * en la carpeta datos/clientes.csv.
 * 
 * @author Alumno
 * @version 1.0
 */
public class Principal {

    /**
     * Metodo main — Arranca la aplicacion.
     * Crea el gestor CRM, muestra el menu y entra en el bucle principal.
     */
    public static void main(String[] args) {

        // Crear el Scanner para leer entrada del usuario
        Scanner scanner = new Scanner(System.in);

        // Crear el gestor del CRM (carga datos del fichero si existen)
        GestorCRM crm = new GestorCRM();

        // Variable para controlar el bucle del menu
        boolean salir = false;

        // Mostrar bienvenida
        System.out.println();
        System.out.println("  ╔══════════════════════════════════════╗");
        System.out.println("  ║     BIENVENIDO AL CRM DE CLIENTES   ║");
        System.out.println("  ║     Gestion de Formularios v1.0     ║");
        System.out.println("  ╚══════════════════════════════════════╝");

        // Bucle principal del programa
        while (!salir) {

            // Mostrar el menu
            System.out.println();
            System.out.println("  ═══════════════════════════════════════");
            System.out.println("         MENU PRINCIPAL DEL CRM");
            System.out.println("  ═══════════════════════════════════════");
            System.out.println("  1. Dar de alta un cliente");
            System.out.println("  2. Listar todos los clientes");
            System.out.println("  3. Buscar cliente");
            System.out.println("  4. Modificar cliente");
            System.out.println("  5. Eliminar cliente");
            System.out.println("  6. Estadisticas");
            System.out.println("  0. Salir");
            System.out.println("  ═══════════════════════════════════════");
            System.out.print("  Elige una opcion: ");

            // Leer la opcion del usuario
            String opcion = scanner.nextLine().trim();

            // Ejecutar la opcion seleccionada con switch
            switch (opcion) {
                case "1":
                    crm.altaCliente(scanner);
                    break;
                case "2":
                    crm.listarClientes();
                    break;
                case "3":
                    crm.buscarCliente(scanner);
                    break;
                case "4":
                    crm.modificarCliente(scanner);
                    break;
                case "5":
                    crm.eliminarCliente(scanner);
                    break;
                case "6":
                    crm.mostrarEstadisticas();
                    break;
                case "0":
                    salir = true;
                    break;
                default:
                    System.out.println("  [!] Opcion no valida. Introduce un numero del 0 al 6.");
            }
        }

        // Mensaje de despedida
        System.out.println();
        System.out.println("  ╔══════════════════════════════════════╗");
        System.out.println("  ║     GRACIAS POR USAR EL CRM         ║");
        System.out.println("  ║     Hasta la proxima!                ║");
        System.out.println("  ╚══════════════════════════════════════╝");
        System.out.println();

        // Cerrar el Scanner
        scanner.close();
    }
}
