CREATE VIEW entradas_con_autores AS 
SELECT 
entradas.titulo,
entradas.contenido,
entradas.fecha,
autores.nombre,
autores.apellidos,
autores.email
 FROM
entradas
LEFT JOIN autores
ON entradas.autor = autores.Identificador;

SELECT
*
FROM
entradas_con_autores;
