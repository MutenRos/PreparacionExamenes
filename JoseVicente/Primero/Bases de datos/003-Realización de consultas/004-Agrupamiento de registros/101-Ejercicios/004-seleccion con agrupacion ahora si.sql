SELECT 
localidad,
COUNT(Identificador)
FROM clientes
GROUP BY(localidad)
;
