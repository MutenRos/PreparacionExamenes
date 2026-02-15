-- ============================================
-- SCRIPT SQL DE REFERENCIA
-- Base de datos: tiendadam
-- Origen: Bases-de-datos-001-Proyecto-tienda-online
-- ============================================
-- Este fichero es una copia de referencia de la base de datos
-- que utiliza el Panel de Control. No es necesario ejecutarlo
-- si ya se ha creado la BD en el proyecto de Bases de Datos.
-- ============================================

-- Crear usuario y base de datos
-- CREATE DATABASE tiendadam;
-- CREATE USER 'tiendadam'@'localhost' IDENTIFIED BY 'Tiendadam123$';
-- GRANT ALL PRIVILEGES ON tiendadam.* TO 'tiendadam'@'localhost';

USE tiendadam;

-- 1. TABLA PRODUCTO
CREATE TABLE IF NOT EXISTS producto (
  id INT AUTO_INCREMENT,
  titulo VARCHAR(255),
  descripcion VARCHAR(255),
  precio VARCHAR(255),
  imagen VARCHAR(255),
  PRIMARY KEY (id)
);

-- 2. TABLA CLIENTE
CREATE TABLE IF NOT EXISTS cliente (
  id INT AUTO_INCREMENT,
  nombre VARCHAR(255),
  apellidos VARCHAR(255),
  email VARCHAR(255),
  PRIMARY KEY (id)
);

-- 3. TABLA PEDIDO (FK -> cliente)
CREATE TABLE IF NOT EXISTS pedido (
  id INT AUTO_INCREMENT,
  fecha VARCHAR(255),
  cliente_id INT,
  PRIMARY KEY (id),
  CONSTRAINT fk_pedido_1 FOREIGN KEY (cliente_id) REFERENCES cliente(id)
);

-- 4. TABLA LINEAPEDIDO (FK -> pedido, producto)
CREATE TABLE IF NOT EXISTS lineapedido (
  id INT AUTO_INCREMENT,
  pedido_id INT,
  producto_id INT,
  cantidad VARCHAR(255),
  PRIMARY KEY (id),
  CONSTRAINT fk_lineapedido_1 FOREIGN KEY (pedido_id) REFERENCES pedido(id),
  CONSTRAINT fk_lineapedido_2 FOREIGN KEY (producto_id) REFERENCES producto(id)
);

-- ============================================
-- DATOS DE EJEMPLO
-- ============================================

INSERT INTO cliente (id, nombre, apellidos, email) VALUES
(1, 'Laura', 'Martínez López', 'laura@example.com'),
(2, 'Carlos', 'Gómez Ruiz', 'carlos@example.com'),
(3, 'María', 'Serrano Díaz', 'maria@example.com'),
(4, 'Jorge', 'Pérez Sánchez', 'jorge@example.com'),
(5, 'Elena', 'Ruiz Navarro', 'elena@example.com');

INSERT INTO producto (id, titulo, descripcion, precio, imagen) VALUES
(1, 'Camiseta Azul', 'Camiseta de algodón talla M', '19.99', 'camiseta_azul.jpg'),
(2, 'Pantalón Negro', 'Pantalón vaquero negro unisex', '39.90', 'pantalon_negro.jpg'),
(3, 'Sudadera Roja', 'Sudadera con capucha talla L', '29.95', 'sudadera_roja.jpg'),
(4, 'Zapatillas Deportivas', 'Calzado deportivo ligero', '59.99', 'zapatillas.jpg'),
(5, 'Gorra Negra', 'Gorra ajustable con visera', '12.50', 'gorra_negra.jpg'),
(6, 'Calcetines Técnicos', 'Pack de 3 pares', '8.99', 'calcetines.jpg'),
(7, 'Chaqueta Impermeable', 'Chaqueta cortavientos unisex', '79.99', 'chaqueta.jpg');

INSERT INTO pedido (id, fecha, cliente_id) VALUES
(1, '2025-02-01', 1),
(2, '2025-02-02', 3),
(3, '2025-02-02', 2),
(4, '2025-02-03', 5),
(5, '2025-02-04', 1),
(6, '2025-02-05', 4),
(7, '2025-02-06', 2),
(8, '2025-02-07', 3);

INSERT INTO lineapedido (id, pedido_id, producto_id, cantidad) VALUES
(1, 1, 1, '2'), (2, 1, 5, '1'), (3, 1, 6, '3'),
(4, 2, 3, '1'), (5, 2, 4, '1'),
(6, 3, 2, '2'), (7, 3, 6, '1'),
(8, 4, 7, '1'), (9, 4, 5, '2'),
(10, 5, 1, '1'), (11, 5, 2, '1'), (12, 5, 3, '1'),
(13, 6, 4, '1'),
(14, 7, 6, '4'), (15, 7, 1, '2'),
(16, 8, 7, '1'), (17, 8, 3, '2'), (18, 8, 5, '1');
