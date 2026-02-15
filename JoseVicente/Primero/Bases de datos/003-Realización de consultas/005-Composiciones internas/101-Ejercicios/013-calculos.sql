SELECT 
pedidosconlineas.fecha,
clientes.nombre,
clientes.apellidos,
lineaspedido.unidades,
productos.nombre,
productos.precio,
productos.precio*lineaspedido.unidades AS Subtotal,
productos.precio*lineaspedido.unidades * 0.16 AS IVA,
productos.precio*lineaspedido.unidades * 1.16 AS Total

FROM `pedidosconlineas`

LEFT JOIN clientes 
ON pedidosconlineas.id_cliente = clientes.Identificador

LEFT JOIN lineaspedido
ON lineaspedido.pedidos_id = pedidosconlineas.Identificador

LEFT JOIN productos
ON lineaspedido.producto_id = productos.Identificador
;

