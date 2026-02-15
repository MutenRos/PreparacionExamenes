import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

/**
 * Clase Conexion — Gestiona la conexion a la base de datos MySQL.
 * Usa los datos de la tienda online (base de datos 'tiendadam')
 * creada en el proyecto de Bases de Datos.
 *
 * Patron Singleton: solo se crea una conexion a la vez.
 *
 * Datos de conexion:
 *   - Host: localhost
 *   - Puerto: 3306
 *   - Base de datos: tiendadam
 *   - Usuario: tiendadam
 *   - Password: Tiendadam123$
 *
 * @author Alumno
 * @version 1.0
 */
public class Conexion {

    // Constantes de configuracion de la base de datos
    private static final String URL = "jdbc:mysql://localhost:3306/tiendadam";
    private static final String USUARIO = "tiendadam";
    private static final String PASSWORD = "Tiendadam123$";

    // Instancia unica de la conexion (Singleton)
    private static Connection conexion = null;

    /**
     * Obtiene la conexion a la base de datos.
     * Si no existe o esta cerrada, crea una nueva.
     *
     * @return Objeto Connection conectado a MySQL
     */
    public static Connection obtener() {
        try {
            // Comprobar si la conexion ya esta abierta
            if (conexion == null || conexion.isClosed()) {
                // Cargar el driver de MySQL
                Class.forName("com.mysql.cj.jdbc.Driver");

                // Crear la conexion
                conexion = DriverManager.getConnection(URL, USUARIO, PASSWORD);
                System.out.println("  [OK] Conectado a la base de datos 'tiendadam'");
            }
        } catch (ClassNotFoundException e) {
            System.out.println("  [!] Error: Driver MySQL no encontrado.");
            System.out.println("      Asegurate de tener mysql-connector-j en el classpath.");
        } catch (SQLException e) {
            System.out.println("  [!] Error de conexion a MySQL: " + e.getMessage());
            System.out.println("      Comprueba que el servidor MySQL esta arrancado.");
        }

        return conexion;
    }

    /**
     * Cierra la conexion a la base de datos.
     */
    public static void cerrar() {
        try {
            if (conexion != null && !conexion.isClosed()) {
                conexion.close();
                System.out.println("  [OK] Conexion a MySQL cerrada.");
            }
        } catch (SQLException e) {
            System.out.println("  [!] Error al cerrar la conexion: " + e.getMessage());
        }
    }
}
