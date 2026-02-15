SELECT 
autores.nombre,
autores.apellidos,
autores.email,
piezas.titulo,
piezas.descripcion,
piezas.fecha,
piezas.imagen
 FROM piezas
LEFT JOIN autores
ON piezas.id_autor = autores.Identificador;

Ahora creamos la vista
CREATE VIEW piezas_con_autores AS 
SELECT 
autores.nombre,
autores.apellidos,
autores.email,
piezas.titulo,
piezas.descripcion,
piezas.fecha,
piezas.imagen
 FROM piezas
LEFT JOIN autores
ON piezas.id_autor = autores.Identificador;

SELECT * FROM piezas_con_autores;

