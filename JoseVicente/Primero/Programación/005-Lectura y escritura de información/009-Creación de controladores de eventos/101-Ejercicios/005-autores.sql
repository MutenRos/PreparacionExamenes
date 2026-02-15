mysql -u root -p

SHOW DATABASES;

CREATE DATABASE blogexamen;

USE blogexamen;

CREATE TABLE `autores` (
  `Identificador` INT NOT NULL , 
  `nombre` VARCHAR(50) NOT NULL , 
  `apellidos` VARCHAR(100) NOT NULL , 
  `email` VARCHAR(50) NOT NULL 
) ENGINE = InnoDB;

SHOW TABLES;

DESCRIBE autores;

ALTER TABLE autores
  ADD PRIMARY KEY (`Identificador`);
  
ALTER TABLE autores
MODIFY COLUMN Identificador INT NOT NULL AUTO_INCREMENT;

DESCRIBE autores;
