mysql -u root -p

SHOW DATABASES;

CREATE DATABASE blogexamen;

USE blogexamen;

CREATE TABLE `posts` (
  `Identificador` INT NOT NULL , 
  `titulo` VARCHAR(50) NOT NULL , 
  `fecha` VARCHAR(100) NOT NULL , 
  `contenido` VARCHAR(50) NOT NULL , 
  `autor` INT(255) NOT NULL 
) ENGINE = InnoDB;

SHOW TABLES;

DESCRIBE posts;

ALTER TABLE posts
  ADD PRIMARY KEY (`Identificador`);
  
ALTER TABLE posts
MODIFY COLUMN Identificador INT NOT NULL AUTO_INCREMENT;

DESCRIBE posts;
