CREATE USER 
'tiendaonline2526'@'localhost' 
IDENTIFIED  BY 'tiendaonline2526';

GRANT USAGE ON *.* TO 'tiendaonline2526'@'localhost';

ALTER USER 'tiendaonline2526'@'localhost' 
REQUIRE NONE 
WITH MAX_QUERIES_PER_HOUR 0 
MAX_CONNECTIONS_PER_HOUR 0 
MAX_UPDATES_PER_HOUR 0 
MAX_USER_CONNECTIONS 0;

GRANT ALL PRIVILEGES ON `tiendaonline2526`.* 
TO 'tiendaonline2526'@'localhost';

FLUSH PRIVILEGES;
