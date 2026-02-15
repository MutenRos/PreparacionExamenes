/**
 * Clase Pedido — Modelo de datos que representa un pedido de la tienda.
 * Corresponde a la tabla 'pedido' de la base de datos 'tiendadam'.
 *
 * Campos de la tabla:
 *   - id INT AUTO_INCREMENT (PK)
 *   - fecha VARCHAR(255)
 *   - cliente_id INT (FK -> cliente)
 *
 * @author Alumno
 * @version 1.0
 */
public class Pedido {

    // Atributos del pedido
    private int id;
    private String fecha;
    private int clienteId;

    // Datos del cliente (cargados con JOIN)
    private String nombreCliente;

    /**
     * Constructor con los datos basicos del pedido.
     */
    public Pedido(int id, String fecha, int clienteId, String nombreCliente) {
        this.id = id;
        this.fecha = fecha;
        this.clienteId = clienteId;
        this.nombreCliente = nombreCliente;
    }

    // ============ Getters ============

    public int getId() { return id; }
    public String getFecha() { return fecha; }
    public int getClienteId() { return clienteId; }
    public String getNombreCliente() { return nombreCliente; }

    // ============ Setters ============

    public void setId(int id) { this.id = id; }
    public void setFecha(String fecha) { this.fecha = fecha; }
    public void setClienteId(int clienteId) { this.clienteId = clienteId; }
    public void setNombreCliente(String nombreCliente) { this.nombreCliente = nombreCliente; }

    /**
     * Formato tabla para consola.
     */
    @Override
    public String toString() {
        return "| " + String.format("%-4d", id) +
               " | " + String.format("%-12s", fecha) +
               " | " + String.format("%-4d", clienteId) +
               " | " + String.format("%-25s", nombreCliente) + " |";
    }
}
