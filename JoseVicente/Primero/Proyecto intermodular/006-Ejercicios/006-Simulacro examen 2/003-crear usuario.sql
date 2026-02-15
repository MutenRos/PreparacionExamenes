CREATE USER 
'portafolio'@'localhost' 
IDENTIFIED BY 'portafolio';

GRANT USAGE ON *.* TO 'portafolio'@'localhost';

ALTER USER 'portafolio'@'localhost' 
REQUIRE NONE 
WITH MAX_QUERIES_PER_HOUR 0 
MAX_CONNECTIONS_PER_HOUR 0 
MAX_UPDATES_PER_HOUR 0 
MAX_USER_CONNECTIONS 0;

GRANT ALL PRIVILEGES ON `portafolio`.* 
TO 'portafolio'@'localhost';

FLUSH PRIVILEGES;
