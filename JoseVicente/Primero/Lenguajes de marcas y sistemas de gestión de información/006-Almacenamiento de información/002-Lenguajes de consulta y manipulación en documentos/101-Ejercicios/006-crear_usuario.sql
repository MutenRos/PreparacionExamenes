CREATE USER 
'training_center'@'localhost' 
IDENTIFIED  BY 'training_center';

GRANT USAGE ON *.* TO 'training_center'@'localhost';

ALTER USER 'training_center'@'localhost' 
REQUIRE NONE 
WITH MAX_QUERIES_PER_HOUR 0 
MAX_CONNECTIONS_PER_HOUR 0 
MAX_UPDATES_PER_HOUR 0 
MAX_USER_CONNECTIONS 0;

GRANT ALL PRIVILEGES ON `training_center`.* 
TO 'training_center'@'localhost';

FLUSH PRIVILEGES;
