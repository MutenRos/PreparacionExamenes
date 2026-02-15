-- ============================================
-- 1. CREACIÓN DE TABLA PRODUCTO
-- ============================================
CREATE TABLE producto (
  id INT AUTO_INCREMENT,
  titulo VARCHAR(255),
  descripcion VARCHAR(255),
  precio VARCHAR(255),
  imagen VARCHAR(255),
  PRIMARY KEY (id)
);

-- ============================================
-- 2. CREACIÓN DE TABLA CLIENTE
-- ============================================
CREATE TABLE cliente (
  id INT AUTO_INCREMENT,
  nombre VARCHAR(255),
  apellidos VARCHAR(255),
  email VARCHAR(255),
  PRIMARY KEY (id)
);

-- ============================================
-- 3. CREACIÓN DE TABLA PEDIDO
--    (depende de cliente)
-- ============================================
CREATE TABLE pedido (
  id INT AUTO_INCREMENT,
  fecha VARCHAR(255),
  cliente_id INT,
  PRIMARY KEY (id),
  CONSTRAINT fk_pedido_1 FOREIGN KEY (cliente_id) REFERENCES cliente(id)
);

-- ============================================
-- 4. CREACIÓN DE TABLA LINEAPEDIDO
--    (depende de pedido y producto)
-- ============================================
CREATE TABLE lineapedido (
  id INT AUTO_INCREMENT,
  pedido_id INT,
  producto_id INT,
  cantidad VARCHAR(255),
  PRIMARY KEY (id),
  CONSTRAINT fk_lineapedido_1 FOREIGN KEY (pedido_id) REFERENCES pedido(id),
  CONSTRAINT fk_lineapedido_2 FOREIGN KEY (producto_id) REFERENCES producto(id)
);

