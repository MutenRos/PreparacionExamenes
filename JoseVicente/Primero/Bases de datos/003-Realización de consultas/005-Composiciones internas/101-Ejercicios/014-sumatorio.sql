SELECT 
pedidosconlineas.fecha,
clientes.nombre,
clientes.apellidos,
SUM(productos.precio*lineaspedido.unidades * 1.16) AS Total

FROM `pedidosconlineas`

LEFT JOIN clientes 
ON pedidosconlineas.id_cliente = clientes.Identificador

LEFT JOIN lineaspedido
ON lineaspedido.pedidos_id = pedidosconlineas.Identificador

LEFT JOIN productos
ON lineaspedido.producto_id = productos.Identificador

GROUP BY pedidosconlineas.Identificador
;

