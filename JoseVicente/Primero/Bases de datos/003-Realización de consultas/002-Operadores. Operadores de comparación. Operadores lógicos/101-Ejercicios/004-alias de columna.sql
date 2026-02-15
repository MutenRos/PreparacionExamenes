SELECT 
nombre AS 'Nombre del producto',
precio AS 'Base Imponible',
precio*0.21 AS 'IVA 21%'
FROM productos;
