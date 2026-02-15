SELECT 
pedidosconlineas.fecha,
clientes.nombre,
clientes.apellidos
FROM `pedidosconlineas`
LEFT JOIN clientes 
ON pedidosconlineas.id_cliente = clientes.Identificador
;

