USE tienda_online;

-- =========================================
-- 1) CATEGORÍAS
--    (sin dependencias)
-- =========================================
-- Tras este INSERT:
--  id_categoria = 1 -> Electrónica
--  id_categoria = 2 -> Libros
--  id_categoria = 3 -> Ropa
--  id_categoria = 4 -> Hogar

INSERT INTO categorias (nombre, descripcion, activa) VALUES
('Electrónica', 'Ordenadores, periféricos y gadgets', 1),
('Libros', 'Libros y material de lectura', 1),
('Ropa', 'Ropa y complementos', 1),
('Hogar', 'Artículos para el hogar y decoración', 1);

-- =========================================
-- 2) CLIENTES
--    (sin dependencias)
-- =========================================
-- Tras este INSERT:
--  id_cliente = 1 -> Ana García
--  id_cliente = 2 -> Luis Martínez
--  id_cliente = 3 -> Marta López
--  id_cliente = 4 -> Carlos Sánchez

INSERT INTO clientes 
(nombre, apellidos, email, telefono, direccion, cp, ciudad, provincia, pais, activo) VALUES
('Ana',   'García Pérez',   'ana.garcia@example.com',   '+34 600 111 111', 'Calle Mayor 1',      '46001', 'Valencia',   'Valencia',   'España', 1),
('Luis',  'Martínez Ruiz',  'luis.martinez@example.com','+34 600 222 222', 'Av. Constitución 23','28001', 'Madrid',     'Madrid',     'España', 1),
('Marta', 'López Sánchez',  'marta.lopez@example.com',  '+34 600 333 333', 'Calle Colón 45',     '08001', 'Barcelona',  'Barcelona',  'España', 1),
('Carlos','Sánchez Vidal',  'carlos.sanchez@example.com','+34 600 444 444','Calle Paz 10',       '30001', 'Murcia',     'Murcia',     'España', 1);

-- =========================================
-- 3) PRODUCTOS
--    (dependen de categorías)
-- =========================================
-- Tras este INSERT:
--  id_producto = 1 -> Portátil 14" básico (cat 1)
--  id_producto = 2 -> Ratón inalámbrico (cat 1)
--  id_producto = 3 -> Libro "Aprende Python" (cat 2)
--  id_producto = 4 -> Libro "HTML y CSS" (cat 2)
--  id_producto = 5 -> Camiseta básica (cat 3)
--  id_producto = 6 -> Sudadera con capucha (cat 3)
--  id_producto = 7 -> Lámpara de escritorio (cat 4)
--  id_producto = 8 -> Taza de café (cat 4)

INSERT INTO productos
(id_categoria, nombre, descripcion, sku, precio, impuesto_porcentaje, activo) VALUES
(1, 'Portátil 14" básico', 'Portátil de 14 pulgadas para uso ofimático', 'ELEC-001', 600.00, 21.00, 1),
(1, 'Ratón inalámbrico',   'Ratón óptico inalámbrico con receptor USB', 'ELEC-002',  20.00, 21.00, 1),
(2, 'Libro "Aprende Python"', 'Libro de programación en Python para principiantes', 'LIB-001', 30.00, 21.00, 1),
(2, 'Libro "HTML y CSS"',  'Guía práctica de maquetación web',             'LIB-002', 25.00, 21.00, 1),
(3, 'Camiseta básica',     'Camiseta de algodón unisex',                    'ROP-001', 15.00, 21.00, 1),
(3, 'Sudadera con capucha','Sudadera gruesa con capucha',                   'ROP-002', 40.00, 21.00, 1),
(4, 'Lámpara de escritorio','Lámpara LED articulada para escritorio',       'HOG-001', 35.00, 21.00, 1),
(4, 'Taza de café',        'Taza de cerámica 300ml',                        'HOG-002',  8.00, 21.00, 1);

-- =========================================
-- 4) GESTIÓN DE STOCK
--    (depende de productos)
-- =========================================
-- Para cada producto:
--   - 1 movimiento de ENTRADA (100 uds, carga inicial)
--   - varios movimientos de SALIDA asociados a pedidos demo

-- Entradas iniciales de stock (100 uds de cada producto)
INSERT INTO gestion_stock (id_producto, tipo_movimiento, cantidad, referencia, observaciones) VALUES
(1, 'entrada', 100, 'Carga inicial', 'Stock inicial del almacén'),
(2, 'entrada', 100, 'Carga inicial', 'Stock inicial del almacén'),
(3, 'entrada', 100, 'Carga inicial', 'Stock inicial del almacén'),
(4, 'entrada', 100, 'Carga inicial', 'Stock inicial del almacén'),
(5, 'entrada', 100, 'Carga inicial', 'Stock inicial del almacén'),
(6, 'entrada', 100, 'Carga inicial', 'Stock inicial del almacén'),
(7, 'entrada', 100, 'Carga inicial', 'Stock inicial del almacén'),
(8, 'entrada', 100, 'Carga inicial', 'Stock inicial del almacén');

-- Salidas de stock ligadas a las líneas de pedido que crearemos después
-- Pedido #1: (id_pedido = 1)
--   - 1x producto 1 (Portátil 14")
--   - 2x producto 2 (Ratón inalámbrico)
INSERT INTO gestion_stock (id_producto, tipo_movimiento, cantidad, referencia, observaciones) VALUES
(1, 'salida', 1, 'Pedido #1', 'Venta al cliente Ana García'),
(2, 'salida', 2, 'Pedido #1', 'Venta al cliente Ana García');

-- Pedido #2: (id_pedido = 2)
--   - 1x producto 3 (Libro Python)
--   - 1x producto 4 (Libro HTML y CSS)
--   - 2x producto 8 (Taza de café)
INSERT INTO gestion_stock (id_producto, tipo_movimiento, cantidad, referencia, observaciones) VALUES
(3, 'salida', 1, 'Pedido #2', 'Venta al cliente Luis Martínez'),
(4, 'salida', 1, 'Pedido #2', 'Venta al cliente Luis Martínez'),
(8, 'salida', 2, 'Pedido #2', 'Venta al cliente Luis Martínez');

-- Pedido #3: (id_pedido = 3)
--   - 3x producto 5 (Camiseta básica)
--   - 1x producto 6 (Sudadera con capucha)
INSERT INTO gestion_stock (id_producto, tipo_movimiento, cantidad, referencia, observaciones) VALUES
(5, 'salida', 3, 'Pedido #3', 'Venta al cliente Marta López'),
(6, 'salida', 1, 'Pedido #3', 'Venta al cliente Marta López');

-- Pedido #4: (id_pedido = 4)
--   - 1x producto 7 (Lámpara de escritorio)
--   - 1x producto 1 (Portátil 14")
INSERT INTO gestion_stock (id_producto, tipo_movimiento, cantidad, referencia, observaciones) VALUES
(7, 'salida', 1, 'Pedido #4', 'Venta al cliente Ana García'),
(1, 'salida', 1, 'Pedido #4', 'Venta al cliente Ana García');

-- =========================================
-- 5) PEDIDOS
--    (dependen de clientes)
-- =========================================
-- IMPORTANTE: asumimos tablas vacías, así que:
--   id_pedido = 1,2,3,4 en este orden.
-- Los totales están calculados a partir de las líneas
-- (21% de IVA sobre el bruto).

-- Pedido 1: cliente 1 (Ana García)
-- Líneas:
--   1x Portátil 14" (600.00)
--   2x Ratón inalámbrico (20.00)
-- Bruto: 640.00
-- IVA (21%): 134.40
-- Total: 774.40

INSERT INTO pedidos
(id_cliente, fecha_pedido, estado, total_bruto, total_impuestos, total, observaciones) VALUES
(1, '2025-01-10 10:30:00', 'pagado',   640.00, 134.40, 774.40, 'Compra online paga con tarjeta'),

-- Pedido 2: cliente 2 (Luis Martínez)
-- Líneas:
--   1x Libro "Aprende Python" (30.00)
--   1x Libro "HTML y CSS" (25.00)
--   2x Taza de café (8.00)
-- Bruto: 71.00
-- IVA (21%): 14.91
-- Total: 85.91
(2, '2025-01-12 16:45:00', 'enviado',   71.00,  14.91,  85.91, 'Envío por mensajería 24h'),

-- Pedido 3: cliente 3 (Marta López)
-- Líneas:
--   3x Camiseta básica (15.00)
--   1x Sudadera con capucha (40.00)
-- Bruto: 85.00
-- IVA (21%): 17.85
-- Total: 102.85
(3, '2025-01-15 09:15:00', 'pagado',    85.00,  17.85, 102.85, 'Pedido recogida en tienda'),

-- Pedido 4: cliente 1 (Ana García)
-- Líneas:
--   1x Lámpara de escritorio (35.00)
--   1x Portátil 14" (600.00)
-- Bruto: 635.00
-- IVA (21%): 133.35
-- Total: 768.35
(1, '2025-01-20 18:20:00', 'pendiente', 635.00, 133.35, 768.35, 'Pendiente de pago por transferencia');

-- =========================================
-- 6) LÍNEAS DE PEDIDO
--    (dependen de pedidos y productos)
-- =========================================
-- Recordatorio:
--   Pedido 1 -> id_pedido = 1
--   Pedido 2 -> id_pedido = 2
--   Pedido 3 -> id_pedido = 3
--   Pedido 4 -> id_pedido = 4
--
-- Todos los productos tienen impuesto_porcentaje = 21.00
-- total_linea = bruto_linea + IVA_linea

INSERT INTO lineas_pedido
(id_pedido, id_producto, cantidad, precio_unitario, impuesto_porcentaje, total_linea) VALUES

-- Pedido 1 (id_pedido = 1)
--  1x producto 1 (600.00) -> bruto 600, IVA 126.00, total 726.00
(1, 1, 1, 600.00, 21.00, 726.00),
--  2x producto 2 (20.00)  -> bruto 40, IVA 8.40, total 48.40
(1, 2, 2,  20.00, 21.00,  48.40),

-- Pedido 2 (id_pedido = 2)
--  1x producto 3 (30.00)  -> bruto 30, IVA 6.30, total 36.30
(2, 3, 1,  30.00, 21.00,  36.30),
--  1x producto 4 (25.00)  -> bruto 25, IVA 5.25, total 30.25
(2, 4, 1,  25.00, 21.00,  30.25),
--  2x producto 8 (8.00)   -> bruto 16, IVA 3.36, total 19.36
(2, 8, 2,   8.00, 21.00,  19.36),

-- Pedido 3 (id_pedido = 3)
--  3x producto 5 (15.00)  -> bruto 45, IVA 9.45, total 54.45
(3, 5, 3,  15.00, 21.00,  54.45),
--  1x producto 6 (40.00)  -> bruto 40, IVA 8.40, total 48.40
(3, 6, 1,  40.00, 21.00,  48.40),

-- Pedido 4 (id_pedido = 4)
--  1x producto 7 (35.00)  -> bruto 35, IVA 7.35, total 42.35
(4, 7, 1,  35.00, 21.00,  42.35),
--  1x producto 1 (600.00) -> bruto 600, IVA 126.00, total 726.00
(4, 1, 1, 600.00, 21.00, 726.00);

