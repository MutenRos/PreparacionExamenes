CREATE USER 
'tiendadam'@'localhost' 
IDENTIFIED BY 'Tiendadam123$';

GRANT USAGE ON *.* TO 'tiendadam'@'localhost';

ALTER USER 'tiendadam'@'localhost' 
REQUIRE NONE 
WITH MAX_QUERIES_PER_HOUR 0 
MAX_CONNECTIONS_PER_HOUR 0 
MAX_UPDATES_PER_HOUR 0 
MAX_USER_CONNECTIONS 0;

GRANT ALL PRIVILEGES ON `tiendadam`.* 
TO 'tiendadam'@'localhost';

FLUSH PRIVILEGES;
