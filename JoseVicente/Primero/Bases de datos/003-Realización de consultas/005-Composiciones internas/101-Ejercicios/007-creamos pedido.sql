-- el cliente hace un pedido
INSERT INTO `pedidosconlineas` (`Identificador`, `fecha`, `id_cliente`) VALUES (NULL, '2025-09-25', '12');

-- insertamos lineas de pedido

INSERT INTO `lineaspedido` (`Identificador`, `producto_id`, `unidades`, `pedidos_id`) VALUES (NULL, '17', '2', '1');
