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
