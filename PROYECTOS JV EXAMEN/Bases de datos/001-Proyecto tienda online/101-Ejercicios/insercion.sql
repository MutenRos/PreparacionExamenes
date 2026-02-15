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
-- Pedido 1
(1, 1, 1, '2'),
(2, 1, 5, '1'),
(3, 1, 6, '3'),

-- Pedido 2
(4, 2, 3, '1'),
(5, 2, 4, '1'),

-- Pedido 3
(6, 3, 2, '2'),
(7, 3, 6, '1'),

-- Pedido 4
(8, 4, 7, '1'),
(9, 4, 5, '2'),

-- Pedido 5
(10, 5, 1, '1'),
(11, 5, 2, '1'),
(12, 5, 3, '1'),

-- Pedido 6
(13, 6, 4, '1'),

-- Pedido 7
(14, 7, 6, '4'),
(15, 7, 1, '2'),

-- Pedido 8
(16, 8, 7, '1'),
(17, 8, 3, '2'),
(18, 8, 5, '1');

