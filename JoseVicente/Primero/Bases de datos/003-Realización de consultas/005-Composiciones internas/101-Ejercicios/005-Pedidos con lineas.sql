CREATE TABLE `empresarial`.`pedidosconlineas` (`Identificador` INT NOT NULL AUTO_INCREMENT , `fecha` DATE NOT NULL , `id_cliente` INT NOT NULL , PRIMARY KEY (`Identificador`)) ENGINE = InnoDB;

CREATE TABLE `empresarial`.`lineaspedido` (`Identificador` INT NOT NULL AUTO_INCREMENT , `producto_id` INT NOT NULL , `unidades` INT NOT NULL , PRIMARY KEY (`Identificador`)) ENGINE = InnoDB;
