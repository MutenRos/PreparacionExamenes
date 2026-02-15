SELECT 
pedidosconlineas.fecha,
clientes.nombre,
clientes.apellidos,
lineaspedido.unidades,
lineaspedido.producto_id

FROM `pedidosconlineas`

LEFT JOIN clientes 
ON pedidosconlineas.id_cliente = clientes.Identificador

LEFT JOIN lineaspedido
ON lineaspedido.pedidos_id = pedidosconlineas.Identificador
;

