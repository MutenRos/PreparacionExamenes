sudo mysql -u root -p

CREATE DATABASE portafolio;

USE portafolio;

CREATE TABLE portafolio (
  `Identificador` INT NOT NULL , 
  `titulo` VARCHAR(150) NOT NULL , 
  `descripcion` VARCHAR(255) NOT NULL , 
  `imagen` VARCHAR(255) NOT NULL , 
  `video` VARCHAR(255) ,
  `url` VARCHAR(255) 
) ENGINE = InnoDB;

ALTER TABLE portafolio
  ADD PRIMARY KEY (`Identificador`);
  
  ALTER TABLE portafolio
  MODIFY COLUMN Identificador INT NOT NULL AUTO_INCREMENT;
  
  DESCRIBE portafolio;
