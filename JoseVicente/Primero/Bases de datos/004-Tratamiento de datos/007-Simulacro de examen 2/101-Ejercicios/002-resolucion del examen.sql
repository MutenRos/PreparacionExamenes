Recomiendo enormemente hacer el examen de bases de datos dentro de la maquina virtual

ssh josevicente@192.168.1.176

sudo mysql -u root -p

CREATE DATABASE portafolio;

SHOW DATABASES;

USE portafolio;

SHOW TABLES;

CREATE TABLE piezas(
  Identificador INT auto_increment PRIMARY KEY,
  titulo VARCHAR(255),
  descripcion TEXT,
  fecha VARCHAR(255),
  id_autor INT
);

SHOW TABLES;

DESCRIBE piezas;

CREATE TABLE autores(
  Identificador INT auto_increment PRIMARY KEY,
  nombre VARCHAR(255),
  apellidos VARCHAR(255),
  email VARCHAR(255)
);

SHOW TABLES;

DESCRIBE autores;

ALTER TABLE piezas 
ADD CONSTRAINT autores_a_piezas 
FOREIGN KEY (id_autor) 
REFERENCES autores(Identificador) 
ON DELETE RESTRICT 
ON UPDATE RESTRICT;

SELECT * FROM piezas;

SELECT * FROM autores;
