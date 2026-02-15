SELECT 
  nombre,
  precio,
  IF(precio < 500, 'Sí', 'No') AS `carga transporte`,
  IF(precio < 500, 200, 0) AS `precio transporte`,
  IF(precio < 500, (200+precio), precio) AS `Total pedido`
FROM productos;
