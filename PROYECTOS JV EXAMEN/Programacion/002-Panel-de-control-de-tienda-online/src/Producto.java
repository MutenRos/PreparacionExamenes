/**
 * Clase Producto — Modelo de datos que representa un producto de la tienda.
 * Corresponde a la tabla 'producto' de la base de datos 'tiendadam'.
 *
 * Campos de la tabla:
 *   - id INT AUTO_INCREMENT (PK)
 *   - titulo VARCHAR(255)
 *   - descripcion VARCHAR(255)
 *   - precio VARCHAR(255)
 *   - imagen VARCHAR(255)
 *
 * @author Alumno
 * @version 1.0
 */
public class Producto {

    // Atributos que mapean las columnas de la tabla 'producto'
    private int id;
    private String titulo;
    private String descripcion;
    private double precio;
    private String imagen;

    /**
     * Constructor con todos los parametros.
     */
    public Producto(int id, String titulo, String descripcion, double precio, String imagen) {
        this.id = id;
        this.titulo = titulo;
        this.descripcion = descripcion;
        this.precio = precio;
        this.imagen = imagen;
    }

    // ============ Getters ============

    public int getId() { return id; }
    public String getTitulo() { return titulo; }
    public String getDescripcion() { return descripcion; }
    public double getPrecio() { return precio; }
    public String getImagen() { return imagen; }

    // ============ Setters ============

    public void setId(int id) { this.id = id; }
    public void setTitulo(String titulo) { this.titulo = titulo; }
    public void setDescripcion(String descripcion) { this.descripcion = descripcion; }
    public void setPrecio(double precio) { this.precio = precio; }
    public void setImagen(String imagen) { this.imagen = imagen; }

    /**
     * Formato tabla para mostrar en consola.
     * Usa String.format para alinear columnas.
     */
    @Override
    public String toString() {
        // Formatear el precio con 2 decimales y simbolo EUR
        String precioFormateado = String.format("%.2f EUR", precio);

        return "| " + String.format("%-4d", id) +
               " | " + String.format("%-22s", titulo) +
               " | " + String.format("%-30s", descripcion) +
               " | " + String.format("%10s", precioFormateado) +
               " | " + String.format("%-20s", imagen) + " |";
    }
}
