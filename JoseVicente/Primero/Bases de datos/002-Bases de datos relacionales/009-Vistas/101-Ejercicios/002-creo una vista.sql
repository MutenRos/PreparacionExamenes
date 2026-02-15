CREATE VIEW vista_pedidos AS 
SELECT 
pedidos.fecha,
clientes.nombre as "nombre de cliente",
clientes.apellidos,
productos.nombre as "nombre de producto",
productos.precio,
productos.precio*0.16 as IVA,
productos.precio*1.16 as Total
FROM pedidos

LEFT JOIN clientes
ON pedidos.id_cliente = clientes.Identificador

LEFT JOIN productos
ON pedidos.id_producto = productos.Identificador
;
