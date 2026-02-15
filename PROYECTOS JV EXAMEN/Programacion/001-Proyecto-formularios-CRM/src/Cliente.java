import java.io.Serializable;

/**
 * Clase Cliente — Representa un cliente del CRM.
 * Almacena los datos basicos del cliente: nombre, email, telefono,
 * empresa y categoria (particular, empresa, VIP).
 * Implementa Serializable para poder guardar objetos en fichero.
 * 
 * @author Alumno
 * @version 1.0
 */
public class Cliente implements Serializable {

    // Numero de version para la serializacion
    private static final long serialVersionUID = 1L;

    // Atributos del cliente
    private int id;
    private String nombre;
    private String email;
    private String telefono;
    private String empresa;
    private String categoria; // "particular", "empresa" o "vip"

    /**
     * Constructor con todos los parametros.
     * 
     * @param id        Identificador unico del cliente
     * @param nombre    Nombre completo del cliente
     * @param email     Correo electronico
     * @param telefono  Numero de telefono
     * @param empresa   Nombre de la empresa (puede estar vacio)
     * @param categoria Categoria: particular, empresa o vip
     */
    public Cliente(int id, String nombre, String email, String telefono, String empresa, String categoria) {
        this.id = id;
        this.nombre = nombre;
        this.email = email;
        this.telefono = telefono;
        this.empresa = empresa;
        this.categoria = categoria;
    }

    // ============ Getters ============

    public int getId() {
        return id;
    }

    public String getNombre() {
        return nombre;
    }

    public String getEmail() {
        return email;
    }

    public String getTelefono() {
        return telefono;
    }

    public String getEmpresa() {
        return empresa;
    }

    public String getCategoria() {
        return categoria;
    }

    // ============ Setters ============

    public void setId(int id) {
        this.id = id;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public void setTelefono(String telefono) {
        this.telefono = telefono;
    }

    public void setEmpresa(String empresa) {
        this.empresa = empresa;
    }

    public void setCategoria(String categoria) {
        this.categoria = categoria;
    }

    /**
     * Devuelve una representacion en texto del cliente,
     * formateada para mostrar en consola.
     */
    @Override
    public String toString() {
        return "| " + String.format("%-4d", id) +
               " | " + String.format("%-20s", nombre) +
               " | " + String.format("%-25s", email) +
               " | " + String.format("%-12s", telefono) +
               " | " + String.format("%-15s", empresa) +
               " | " + String.format("%-10s", categoria) + " |";
    }

    /**
     * Convierte el cliente a una linea CSV para guardar en fichero.
     * Formato: id;nombre;email;telefono;empresa;categoria
     */
    public String toCSV() {
        return id + ";" + nombre + ";" + email + ";" + telefono + ";" + empresa + ";" + categoria;
    }

    /**
     * Crea un objeto Cliente a partir de una linea CSV.
     * 
     * @param linea Linea en formato id;nombre;email;telefono;empresa;categoria
     * @return Objeto Cliente creado, o null si el formato es incorrecto
     */
    public static Cliente fromCSV(String linea) {
        // Separar la linea por punto y coma
        String[] partes = linea.split(";");

        // Comprobar que tiene exactamente 6 campos
        if (partes.length != 6) {
            System.out.println("  [!] Linea con formato incorrecto: " + linea);
            return null;
        }

        try {
            int id = Integer.parseInt(partes[0].trim());
            String nombre = partes[1].trim();
            String email = partes[2].trim();
            String telefono = partes[3].trim();
            String empresa = partes[4].trim();
            String categoria = partes[5].trim();

            return new Cliente(id, nombre, email, telefono, empresa, categoria);
        } catch (NumberFormatException e) {
            System.out.println("  [!] Error al leer el ID: " + partes[0]);
            return null;
        }
    }
}
