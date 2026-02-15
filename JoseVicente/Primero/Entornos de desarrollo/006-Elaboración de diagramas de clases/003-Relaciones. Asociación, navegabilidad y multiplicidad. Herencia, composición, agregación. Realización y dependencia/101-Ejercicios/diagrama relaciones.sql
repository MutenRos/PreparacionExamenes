CREATE TABLE cliente (
  id INT,
  nombre VARCHAR(255),
  apellidos VARCHAR(255),
  email VARCHAR(255),
  direccion VARCHAR(255),
  PRIMARY KEY (id)
);

CREATE TABLE producto (
  id INT,
  nombre VARCHAR(255),
  descripcion VARCHAR(255),
  precio VARCHAR(255),
  PRIMARY KEY (id)
);

CREATE TABLE pedido (
  id INT,
  fecha VARCHAR(255),
  id_cliente VARCHAR(255),
  PRIMARY KEY (id),
  CONSTRAINT fk_pedido_1 FOREIGN KEY (id_cliente) REFERENCES cliente(id)
);

CREATE TABLE lineapedido (
  id INT,
  pedido_id INT,
  producto_id INT,
  cantidad VARCHAR(255),
  PRIMARY KEY (id),
  CONSTRAINT fk_lineapedido_1 FOREIGN KEY (pedido_id) REFERENCES pedido(id),
  CONSTRAINT fk_lineapedido_2 FOREIGN KEY (producto_id) REFERENCES producto(id)
);
