SELECT
posts.titulo,
posts.fecha,
posts.contenido,
autores.nombre,
autores.apellidos 
FROM posts
LEFT JOIN autores
ON posts.autor = autores.Identificador;

