from typing import Optional

class Cliente:
    def __init__(self, id: Optional[int] = None, nombre: Optional[str] = None, apellidos: Optional[str] = None, email: Optional[str] = None, direccion: Optional[str] = None):
        self.id = id
        self.nombre = nombre
        self.apellidos = apellidos
        self.email = email
        self.direccion = direccion

    def __repr__(self):
        return f"Cliente(id={self.id!r}, nombre={self.nombre!r}, apellidos={self.apellidos!r}, email={self.email!r}, direccion={self.direccion!r})"

class Producto:
    def __init__(self, id: Optional[int] = None, nombre: Optional[str] = None, descripcion: Optional[str] = None, precio: Optional[str] = None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio

    def __repr__(self):
        return f"Producto(id={self.id!r}, nombre={self.nombre!r}, descripcion={self.descripcion!r}, precio={self.precio!r})"

class Pedido:
    def __init__(self, id: Optional[int] = None, fecha: Optional[str] = None, id_cliente: Optional[str] = None):
        self.id = id
        self.fecha = fecha
        self.id_cliente = id_cliente

    def __repr__(self):
        return f"Pedido(id={self.id!r}, fecha={self.fecha!r}, id_cliente={self.id_cliente!r})"

    # FK1: id_cliente -> cliente.id

class Lineapedido:
    def __init__(self, id: Optional[int] = None, pedido_id: Optional[int] = None, producto_id: Optional[int] = None, cantidad: Optional[str] = None):
        self.id = id
        self.pedido_id = pedido_id
        self.producto_id = producto_id
        self.cantidad = cantidad

    def __repr__(self):
        return f"Lineapedido(id={self.id!r}, pedido_id={self.pedido_id!r}, producto_id={self.producto_id!r}, cantidad={self.cantidad!r})"

    # FK1: pedido_id -> pedido.id
    # FK2: producto_id -> producto.id
