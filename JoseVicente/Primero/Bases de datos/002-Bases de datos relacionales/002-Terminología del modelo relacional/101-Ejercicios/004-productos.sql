CREATE TABLE `empresarial`.`productos` (
  `Identificador` INT NOT NULL , 
  `nombre` VARCHAR(50) NOT NULL , 
  `descripcion` TEXT NOT NULL , 
  `precio` DOUBLE(10,2) NOT NULL , 
  `peso` DOUBLE(10,2) NOT NULL 
) ENGINE = InnoDB;
