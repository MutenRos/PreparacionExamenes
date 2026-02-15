CREATE TABLE entradas (
  `Identificador` INT NOT NULL , 
  `titulo` VARCHAR(150) NOT NULL , 
  `contenido` VARCHAR(255) NOT NULL , 
  `fecha` VARCHAR(50) NOT NULL , 
  `autor` INT NOT NULL 
) ENGINE = InnoDB;

CREATE TABLE autores (
  `Identificador` INT NOT NULL , 
  `nombre` VARCHAR(150) NOT NULL , 
  `apellidos` VARCHAR(255) NOT NULL , 
  `email` VARCHAR(150) NOT NULL 
) ENGINE = InnoDB;


