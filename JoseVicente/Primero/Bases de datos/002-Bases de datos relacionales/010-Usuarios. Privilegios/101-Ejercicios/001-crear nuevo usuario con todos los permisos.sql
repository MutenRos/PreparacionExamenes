CREATE USER 
'usuarioempresarial'@'localhost' 
IDENTIFIED WITH 
caching_sha2_password BY '***';

GRANT USAGE ON *.* TO 'usuarioempresarial'@'localhost';

ALTER USER 'usuarioempresarial'@'localhost' 
REQUIRE NONE 
WITH MAX_QUERIES_PER_HOUR 0 
MAX_CONNECTIONS_PER_HOUR 0 
MAX_UPDATES_PER_HOUR 0 
MAX_USER_CONNECTIONS 0;

GRANT ALL PRIVILEGES ON `empresarial`.* 
TO 'usuarioempresarial'@'localhost';

FLUSH PRIVILEGES;
