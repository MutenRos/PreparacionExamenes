import java.util.ArrayList;
import java.util.Scanner;
import java.io.*;

/**
 * Clase GestorCRM — Logica principal del CRM.
 * Gestiona la lista de clientes con operaciones CRUD
 * (Crear, Leer, Actualizar, Eliminar) y persistencia en fichero CSV.
 * 
 * @author Alumno
 * @version 1.0
 */
public class GestorCRM {

    // Lista de clientes en memoria
    private ArrayList<Cliente> clientes;

    // Contador para asignar IDs automaticamente
    private int siguienteId;

    // Nombre del fichero donde se guardan los datos
    private static final String FICHERO_DATOS = "datos/clientes.csv";

    /**
     * Constructor — Inicializa la lista y carga datos del fichero.
     */
    public GestorCRM() {
        clientes = new ArrayList<Cliente>();
        siguienteId = 1;
        cargarDatos();
    }

    // ============================================================
    // OPERACION: Dar de alta un nuevo cliente (CREATE)
    // ============================================================
    /**
     * Formulario para dar de alta un nuevo cliente.
     * Pide los datos por consola y los valida antes de guardar.
     * 
     * @param scanner Objeto Scanner para leer la entrada del usuario
     */
    public void altaCliente(Scanner scanner) {
        System.out.println();
        System.out.println("  ╔══════════════════════════════════════╗");
        System.out.println("  ║    FORMULARIO: NUEVO CLIENTE         ║");
        System.out.println("  ╚══════════════════════════════════════╝");
        System.out.println();

        // Pedir nombre (obligatorio)
        String nombre = "";
        while (nombre.isEmpty()) {
            System.out.print("  Nombre completo: ");
            nombre = scanner.nextLine().trim();
            if (nombre.isEmpty()) {
                System.out.println("  [!] El nombre no puede estar vacio.");
            }
        }

        // Pedir email (debe contener @)
        String email = "";
        while (email.isEmpty() || !email.contains("@")) {
            System.out.print("  Email: ");
            email = scanner.nextLine().trim();
            if (!email.contains("@")) {
                System.out.println("  [!] El email debe contener '@'.");
            }
        }

        // Pedir telefono (debe tener al menos 9 digitos)
        String telefono = "";
        while (telefono.length() < 9) {
            System.out.print("  Telefono (min 9 digitos): ");
            telefono = scanner.nextLine().trim();
            if (telefono.length() < 9) {
                System.out.println("  [!] El telefono debe tener al menos 9 digitos.");
            }
        }

        // Pedir empresa (opcional)
        System.out.print("  Empresa (dejar vacio si es particular): ");
        String empresa = scanner.nextLine().trim();
        if (empresa.isEmpty()) {
            empresa = "-";
        }

        // Pedir categoria con menu de opciones
        String categoria = elegirCategoria(scanner);

        // Crear el cliente y anadirlo a la lista
        Cliente nuevo = new Cliente(siguienteId, nombre, email, telefono, empresa, categoria);
        clientes.add(nuevo);
        siguienteId++;

        // Guardar en fichero automaticamente
        guardarDatos();

        System.out.println();
        System.out.println("  [OK] Cliente '" + nombre + "' dado de alta con ID " + nuevo.getId());
    }

    // ============================================================
    // OPERACION: Listar todos los clientes (READ)
    // ============================================================
    /**
     * Muestra todos los clientes en formato de tabla.
     * Si no hay clientes muestra un mensaje informativo.
     */
    public void listarClientes() {
        System.out.println();

        if (clientes.isEmpty()) {
            System.out.println("  [i] No hay clientes registrados en el CRM.");
            return;
        }

        System.out.println("  ╔══════════════════════════════════════════════════════════════════════════════════════════════════════╗");
        System.out.println("  ║                                    LISTADO DE CLIENTES                                              ║");
        System.out.println("  ╠══════════════════════════════════════════════════════════════════════════════════════════════════════╣");
        System.out.println("  | " + String.format("%-4s", "ID") +
                           " | " + String.format("%-20s", "NOMBRE") +
                           " | " + String.format("%-25s", "EMAIL") +
                           " | " + String.format("%-12s", "TELEFONO") +
                           " | " + String.format("%-15s", "EMPRESA") +
                           " | " + String.format("%-10s", "CATEGORIA") + " |");
        System.out.println("  |----- ---------------------- -------------------------- ------------- ---------------- -----------|");

        // Recorrer la lista con un bucle for-each
        for (Cliente c : clientes) {
            System.out.println("  " + c.toString());
        }

        System.out.println("  ╚══════════════════════════════════════════════════════════════════════════════════════════════════════╝");
        System.out.println("  Total: " + clientes.size() + " cliente(s)");
    }

    // ============================================================
    // OPERACION: Buscar cliente por nombre o email (READ)
    // ============================================================
    /**
     * Busca clientes cuyo nombre o email contenga el texto buscado.
     * La busqueda es case-insensitive (ignora mayusculas/minusculas).
     * 
     * @param scanner Objeto Scanner para leer la entrada del usuario
     */
    public void buscarCliente(Scanner scanner) {
        System.out.println();
        System.out.print("  Texto a buscar (nombre o email): ");
        String busqueda = scanner.nextLine().trim().toLowerCase();

        if (busqueda.isEmpty()) {
            System.out.println("  [!] Debes escribir algo para buscar.");
            return;
        }

        // Crear una lista auxiliar con los resultados
        ArrayList<Cliente> resultados = new ArrayList<Cliente>();

        for (Cliente c : clientes) {
            // Comparar en minusculas para ignorar mayusculas
            if (c.getNombre().toLowerCase().contains(busqueda) ||
                c.getEmail().toLowerCase().contains(busqueda)) {
                resultados.add(c);
            }
        }

        // Mostrar resultados
        if (resultados.isEmpty()) {
            System.out.println("  [i] No se encontraron clientes con '" + busqueda + "'.");
        } else {
            System.out.println("  Encontrados " + resultados.size() + " resultado(s):");
            System.out.println();
            for (Cliente c : resultados) {
                System.out.println("  " + c.toString());
            }
        }
    }

    // ============================================================
    // OPERACION: Modificar un cliente existente (UPDATE)
    // ============================================================
    /**
     * Permite modificar los datos de un cliente existente.
     * Primero busca por ID, luego muestra los datos actuales y
     * permite cambiar cada campo (dejando vacio para mantener).
     * 
     * @param scanner Objeto Scanner para leer la entrada del usuario
     */
    public void modificarCliente(Scanner scanner) {
        System.out.println();
        System.out.println("  ╔══════════════════════════════════════╗");
        System.out.println("  ║    FORMULARIO: MODIFICAR CLIENTE     ║");
        System.out.println("  ╚══════════════════════════════════════╝");
        System.out.println();

        // Pedir el ID del cliente a modificar
        System.out.print("  ID del cliente a modificar: ");
        int id = leerEntero(scanner);

        // Buscar el cliente por ID
        Cliente cliente = buscarPorId(id);

        if (cliente == null) {
            System.out.println("  [!] No se encontro un cliente con ID " + id);
            return;
        }

        // Mostrar datos actuales
        System.out.println("  Datos actuales:");
        System.out.println("  " + cliente.toString());
        System.out.println();
        System.out.println("  (Deja vacio para mantener el valor actual)");
        System.out.println();

        // Pedir nuevos datos
        System.out.print("  Nuevo nombre [" + cliente.getNombre() + "]: ");
        String nombre = scanner.nextLine().trim();
        if (!nombre.isEmpty()) {
            cliente.setNombre(nombre);
        }

        System.out.print("  Nuevo email [" + cliente.getEmail() + "]: ");
        String email = scanner.nextLine().trim();
        if (!email.isEmpty() && email.contains("@")) {
            cliente.setEmail(email);
        }

        System.out.print("  Nuevo telefono [" + cliente.getTelefono() + "]: ");
        String telefono = scanner.nextLine().trim();
        if (!telefono.isEmpty() && telefono.length() >= 9) {
            cliente.setTelefono(telefono);
        }

        System.out.print("  Nueva empresa [" + cliente.getEmpresa() + "]: ");
        String empresa = scanner.nextLine().trim();
        if (!empresa.isEmpty()) {
            cliente.setEmpresa(empresa);
        }

        System.out.println("  Nueva categoria [" + cliente.getCategoria() + "]:");
        String categoria = elegirCategoria(scanner);
        if (!categoria.isEmpty()) {
            cliente.setCategoria(categoria);
        }

        // Guardar cambios
        guardarDatos();

        System.out.println();
        System.out.println("  [OK] Cliente con ID " + id + " modificado correctamente.");
    }

    // ============================================================
    // OPERACION: Eliminar un cliente (DELETE)
    // ============================================================
    /**
     * Elimina un cliente del CRM, pidiendo confirmacion antes.
     * 
     * @param scanner Objeto Scanner para leer la entrada del usuario
     */
    public void eliminarCliente(Scanner scanner) {
        System.out.println();
        System.out.print("  ID del cliente a eliminar: ");
        int id = leerEntero(scanner);

        // Buscar el cliente
        Cliente cliente = buscarPorId(id);

        if (cliente == null) {
            System.out.println("  [!] No se encontro un cliente con ID " + id);
            return;
        }

        // Mostrar datos y pedir confirmacion
        System.out.println("  Cliente encontrado:");
        System.out.println("  " + cliente.toString());
        System.out.println();
        System.out.print("  ¿Confirmar eliminacion? (s/n): ");
        String confirmacion = scanner.nextLine().trim().toLowerCase();

        if (confirmacion.equals("s") || confirmacion.equals("si")) {
            clientes.remove(cliente);
            guardarDatos();
            System.out.println("  [OK] Cliente '" + cliente.getNombre() + "' eliminado.");
        } else {
            System.out.println("  [i] Eliminacion cancelada.");
        }
    }

    // ============================================================
    // OPERACION: Estadisticas del CRM
    // ============================================================
    /**
     * Muestra un resumen con el numero de clientes por categoria
     * y el total de registros en el CRM.
     */
    public void mostrarEstadisticas() {
        System.out.println();
        System.out.println("  ╔══════════════════════════════════════╗");
        System.out.println("  ║         ESTADISTICAS DEL CRM        ║");
        System.out.println("  ╚══════════════════════════════════════╝");
        System.out.println();

        // Contadores por categoria
        int particulares = 0;
        int empresas = 0;
        int vips = 0;

        for (Cliente c : clientes) {
            switch (c.getCategoria().toLowerCase()) {
                case "particular":
                    particulares++;
                    break;
                case "empresa":
                    empresas++;
                    break;
                case "vip":
                    vips++;
                    break;
            }
        }

        System.out.println("  Total de clientes:    " + clientes.size());
        System.out.println("  ─────────────────────────────");
        System.out.println("  Particulares:          " + particulares);
        System.out.println("  Empresas:              " + empresas);
        System.out.println("  VIP:                   " + vips);
        System.out.println();

        // Mostrar si hay clientes o no
        if (clientes.isEmpty()) {
            System.out.println("  [i] El CRM esta vacio. Anade clientes para ver estadisticas.");
        } else {
            System.out.println("  [i] Ultima ID asignada: " + (siguienteId - 1));
        }
    }

    // ============================================================
    // METODOS AUXILIARES PRIVADOS
    // ============================================================

    /**
     * Busca un cliente por su ID en la lista.
     * 
     * @param id ID del cliente a buscar
     * @return El cliente encontrado o null si no existe
     */
    private Cliente buscarPorId(int id) {
        for (Cliente c : clientes) {
            if (c.getId() == id) {
                return c;
            }
        }
        return null;
    }

    /**
     * Muestra un sub-menu para elegir la categoria del cliente.
     * 
     * @param scanner Objeto Scanner para leer la entrada del usuario
     * @return La categoria seleccionada como String
     */
    private String elegirCategoria(Scanner scanner) {
        System.out.println("  Categoria:");
        System.out.println("    1. Particular");
        System.out.println("    2. Empresa");
        System.out.println("    3. VIP");
        System.out.print("  Opcion (1-3): ");

        String opcion = scanner.nextLine().trim();

        switch (opcion) {
            case "1": return "particular";
            case "2": return "empresa";
            case "3": return "vip";
            default:
                System.out.println("  [!] Opcion no valida, se asigna 'particular'.");
                return "particular";
        }
    }

    /**
     * Lee un numero entero de la entrada del usuario.
     * Si el texto no es un numero valido, devuelve -1.
     * 
     * @param scanner Objeto Scanner para leer la entrada
     * @return El entero leido o -1 si no es valido
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

    // ============================================================
    // PERSISTENCIA: Guardar y cargar datos en fichero CSV
    // ============================================================

    /**
     * Guarda todos los clientes en un fichero CSV.
     * Crea la carpeta 'datos/' si no existe.
     */
    private void guardarDatos() {
        try {
            // Crear la carpeta datos/ si no existe
            File carpeta = new File("datos");
            if (!carpeta.exists()) {
                carpeta.mkdirs();
            }

            // Abrir el fichero para escritura
            PrintWriter escritor = new PrintWriter(new FileWriter(FICHERO_DATOS));

            // Escribir cada cliente como una linea CSV
            for (Cliente c : clientes) {
                escritor.println(c.toCSV());
            }

            escritor.close();

        } catch (IOException e) {
            System.out.println("  [!] Error al guardar datos: " + e.getMessage());
        }
    }

    /**
     * Carga los clientes desde el fichero CSV al iniciar el programa.
     * Si el fichero no existe, simplemente empieza con la lista vacia.
     */
    private void cargarDatos() {
        File fichero = new File(FICHERO_DATOS);

        // Si no existe el fichero, no hay nada que cargar
        if (!fichero.exists()) {
            System.out.println("  [i] No se encontro fichero de datos. Empezando con CRM vacio.");
            return;
        }

        try {
            BufferedReader lector = new BufferedReader(new FileReader(fichero));
            String linea;
            int contador = 0;

            // Leer linea a linea
            while ((linea = lector.readLine()) != null) {
                // Ignorar lineas vacias
                if (linea.trim().isEmpty()) {
                    continue;
                }

                // Crear cliente desde la linea CSV
                Cliente c = Cliente.fromCSV(linea);
                if (c != null) {
                    clientes.add(c);
                    contador++;

                    // Actualizar el siguienteId para no repetir IDs
                    if (c.getId() >= siguienteId) {
                        siguienteId = c.getId() + 1;
                    }
                }
            }

            lector.close();
            System.out.println("  [OK] Cargados " + contador + " clientes desde " + FICHERO_DATOS);

        } catch (IOException e) {
            System.out.println("  [!] Error al cargar datos: " + e.getMessage());
        }
    }
}
