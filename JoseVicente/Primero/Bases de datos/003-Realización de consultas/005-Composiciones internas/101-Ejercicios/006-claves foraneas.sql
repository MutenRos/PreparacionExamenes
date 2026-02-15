ALTER TABLE `lineaspedido` ADD CONSTRAINT `lineaspedidoaproductos` FOREIGN KEY (`producto_id`) REFERENCES `productos`(`Identificador`) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE `lineaspedido` ADD `pedidos_id` INT NOT NULL AFTER `unidades`;

ALTER TABLE `lineaspedido` ADD CONSTRAINT `lineapedidoapedido` FOREIGN KEY (`pedidos_id`) REFERENCES `pedidos`(`Identificador`) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE `lineaspedido` DROP FOREIGN KEY `lineapedidoapedido`; ALTER TABLE `lineaspedido` ADD CONSTRAINT `lineapedidoapedido` FOREIGN KEY (`pedidos_id`) REFERENCES `pedidosconlineas`(`Identificador`) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE `pedidosconlineas` ADD  CONSTRAINT `pedidosaclientes2` FOREIGN KEY (`id_cliente`) REFERENCES `clientes`(`Identificador`) ON DELETE RESTRICT ON UPDATE RESTRICT;

