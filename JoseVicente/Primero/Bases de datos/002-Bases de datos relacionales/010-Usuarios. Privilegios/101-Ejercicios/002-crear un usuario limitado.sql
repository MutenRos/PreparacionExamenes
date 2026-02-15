CREATE USER 
'usuariosololectura'@'localhost' 
IDENTIFIED WITH 
caching_sha2_password BY '***';

GRANT 
SELECT 
ON *.* 
TO 'usuariosololectura'@'localhost';

ALTER USER 
'usuariosololectura'@'localhost' 
REQUIRE NONE 
WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0;

GRANT ALL PRIVILEGES ON 
`empresarial`.* 
TO 'usuariosololectura'@'localhost';
