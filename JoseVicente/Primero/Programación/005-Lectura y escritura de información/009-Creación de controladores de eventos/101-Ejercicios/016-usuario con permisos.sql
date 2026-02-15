CREATE USER 
'blogexamen'@'localhost' 
IDENTIFIED BY 'Blogexamen123$';

GRANT USAGE ON *.* TO 'blogexamen'@'localhost';

ALTER USER 'blogexamen'@'localhost' 
REQUIRE NONE 
WITH MAX_QUERIES_PER_HOUR 0 
MAX_CONNECTIONS_PER_HOUR 0 
MAX_UPDATES_PER_HOUR 0 
MAX_USER_CONNECTIONS 0;

GRANT ALL PRIVILEGES ON `blogexamen`.* 
TO 'blogexamen'@'localhost';


