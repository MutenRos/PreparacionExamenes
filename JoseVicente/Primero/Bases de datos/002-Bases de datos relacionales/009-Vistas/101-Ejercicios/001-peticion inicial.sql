SELECT 
pedidos.fecha,
clientes.nombre,
clientes.apellidos,
productos.nombre,
productos.precio,
productos.precio*0.16 as IVA,
productos.precio*1.16 as Total
FROM pedidos

LEFT JOIN clientes
ON pedidos.id_cliente = clientes.Identificador

LEFT JOIN productos
ON pedidos.id_producto = productos.Identificador
;
