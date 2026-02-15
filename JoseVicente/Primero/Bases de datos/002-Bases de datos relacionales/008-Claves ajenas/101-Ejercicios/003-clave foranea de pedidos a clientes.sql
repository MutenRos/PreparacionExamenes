ALTER TABLE `pedidos` ADD CONSTRAINT `pedidosaclientes` FOREIGN KEY (`id_cliente`) REFERENCES `clientes`(`Identificador`) ON DELETE RESTRICT ON UPDATE RESTRICT;
