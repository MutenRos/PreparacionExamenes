/**
 * Clase Cliente — Modelo de datos que representa un cliente de la tienda.
 * Corresponde a la tabla 'cliente' de la base de datos 'tiendadam'.
 *
 * Campos de la tabla:
 *   - id INT AUTO_INCREMENT (PK)
 *   - nombre VARCHAR(255)
 *   - apellidos VARCHAR(255)
 *   - email VARCHAR(255)
 *
 * @author Alumno
 * @version 1.0
 */
public class Cliente {

    // Atributos que mapean las columnas de la tabla 'cliente'
    private int id;
    private String nombre;
    private String apellidos;
    private String email;

    /**
     * Constructor con todos los parametros.
     */
    public Cliente(int id, String nombre, String apellidos, String email) {
        this.id = id;
        this.nombre = nombre;
        this.apellidos = apellidos;
        this.email = email;
    }

    // ============ Getters ============

    public int getId() { return id; }
    public String getNombre() { return nombre; }
    public String getApellidos() { return apellidos; }
    public String getEmail() { return email; }

    // ============ Setters ============

    public void setId(int id) { this.id = id; }
    public void setNombre(String nombre) { this.nombre = nombre; }
    public void setApellidos(String apellidos) { this.apellidos = apellidos; }
    public void setEmail(String email) { this.email = email; }

    /**
     * Formato tabla para mostrar en consola.
     */
    @Override
    public String toString() {
        return "| " + String.format("%-4d", id) +
               " | " + String.format("%-15s", nombre) +
               " | " + String.format("%-20s", apellidos) +
               " | " + String.format("%-25s", email) + " |";
    }
}
