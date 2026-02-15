CREATE OR REPLACE VIEW vw_productos_categorias AS
SELECT
    p.id_producto,
    p.nombre              AS producto,
    p.descripcion         AS descripcion_producto,
    p.sku,
    p.precio,
    p.impuesto_porcentaje,
    p.activo              AS producto_activo,
    c.id_categoria,
    c.nombre              AS categoria,
    c.descripcion         AS descripcion_categoria,
    c.activa              AS categoria_activa
FROM productos p
JOIN categorias c ON p.id_categoria = c.id_categoria;


CREATE OR REPLACE VIEW vw_pedidos_clientes AS
SELECT
    pe.id_pedido,
    pe.fecha_pedido,
    pe.estado,
    pe.total_bruto,
    pe.total_impuestos,
    pe.total,
    cl.id_cliente,
    CONCAT(cl.nombre, ' ', cl.apellidos) AS cliente,
    cl.email,
    cl.telefono,
    cl.ciudad,
    cl.provincia,
    cl.pais
FROM pedidos pe
JOIN clientes cl ON pe.id_cliente = cl.id_cliente;


CREATE OR REPLACE VIEW vw_lineas_pedido_detalle AS
SELECT
    lp.id_linea_pedido,
    -- Pedido
    pe.id_pedido,
    pe.fecha_pedido,
    pe.estado,
    pe.total          AS total_pedido,
    
    -- Cliente
    cl.id_cliente,
    CONCAT(cl.nombre, ' ', cl.apellidos) AS cliente,
    cl.email              AS email_cliente,
    
    -- Producto
    pr.id_producto,
    pr.nombre             AS producto,
    pr.sku,
    pr.precio             AS precio_actual_producto,
    
    -- Categoría
    ca.id_categoria,
    ca.nombre             AS categoria,
    
    -- Datos de la línea
    lp.cantidad,
    lp.precio_unitario,
    lp.impuesto_porcentaje,
    lp.total_linea
FROM lineas_pedido lp
JOIN pedidos pe   ON lp.id_pedido   = pe.id_pedido
JOIN clientes cl  ON pe.id_cliente  = cl.id_cliente
JOIN productos pr ON lp.id_producto = pr.id_producto
JOIN categorias ca ON pr.id_categoria = ca.id_categoria;

CREATE OR REPLACE VIEW vw_stock_actual AS
SELECT
    p.id_producto,
    p.nombre          AS producto,
    p.sku,
    c.id_categoria,
    c.nombre          AS categoria,
    
    COALESCE(SUM(
        CASE
            WHEN gs.tipo_movimiento = 'entrada' THEN gs.cantidad
            WHEN gs.tipo_movimiento = 'salida'  THEN -gs.cantidad
            WHEN gs.tipo_movimiento = 'ajuste'  THEN gs.cantidad
            ELSE 0
        END
    ), 0) AS stock_actual
FROM productos p
LEFT JOIN categorias c    ON p.id_categoria = c.id_categoria
LEFT JOIN gestion_stock gs ON p.id_producto = gs.id_producto
GROUP BY
    p.id_producto,
    p.nombre,
    p.sku,
    c.id_categoria,
    c.nombre;


CREATE OR REPLACE VIEW vw_pedidos_resumen AS
SELECT
    pe.id_pedido,
    pe.fecha_pedido,
    pe.estado,
    cl.id_cliente,
    CONCAT(cl.nombre, ' ', cl.apellidos) AS cliente,
    
    SUM(lp.cantidad * lp.precio_unitario)                   AS total_bruto_calculado,
    SUM(lp.cantidad * lp.precio_unitario * lp.impuesto_porcentaje / 100) AS total_impuestos_calculado,
    SUM(lp.total_linea)                                     AS total_calculado
FROM pedidos pe
JOIN clientes cl  ON pe.id_cliente  = cl.id_cliente
LEFT JOIN lineas_pedido lp ON pe.id_pedido = lp.id_pedido
GROUP BY
    pe.id_pedido,
    pe.fecha_pedido,
    pe.estado,
    cl.id_cliente,
    cliente;

CREATE OR REPLACE VIEW vw_movimientos_stock_detalle AS
SELECT
    gs.id_movimiento,
    gs.fecha_movimiento,
    gs.tipo_movimiento,
    gs.cantidad,
    gs.referencia,
    gs.observaciones,
    p.id_producto,
    p.nombre AS producto,
    p.sku,
    c.id_categoria,
    c.nombre AS categoria
FROM gestion_stock gs
JOIN productos p ON gs.id_producto = p.id_producto
JOIN categorias c ON p.id_categoria = c.id_categoria;

