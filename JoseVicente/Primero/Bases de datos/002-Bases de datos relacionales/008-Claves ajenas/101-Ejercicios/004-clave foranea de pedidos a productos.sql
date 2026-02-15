ALTER TABLE `pedidos` ADD CONSTRAINT `pedidosaproductos` FOREIGN KEY (`id_producto`) REFERENCES `productos`(`Identificador`) ON DELETE RESTRICT ON UPDATE RESTRICT;
