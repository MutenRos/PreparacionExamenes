SHOW DATABASES;

mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (0,01 sec)

mysql> 

CREATE DATABASE prueba;

mysql> CREATE DATABASE prueba;
Query OK, 1 row affected (0,02 sec)

mysql> 

mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| prueba             |
| sys                |
+--------------------+
5 rows in set (0,00 sec)

mysql> 

Esto quiere decir que no solo quiero crear prueba sino que quiero ENTRAR dentro de prueba
USE prueba;

mysql> USE prueba;
Database changed
mysql> 


SHOW TABLES;
mysql> SHOW TABLES;
Empty set (0,00 sec)

mysql> 

CREATE TABLE `clientes` (
  `Identificador` INT NOT NULL , 
  `nombre` VARCHAR(50) NOT NULL , 
  `apellidos` VARCHAR(100) NOT NULL , 
  `telefono` VARCHAR(50) NOT NULL , 
  `email` VARCHAR(100) NOT NULL 
) ENGINE = InnoDB;

mysql> CREATE TABLE `clientes` (
    ->   `Identificador` INT NOT NULL , 
    ->   `nombre` VARCHAR(50) NOT NULL , 
    ->   `apellidos` VARCHAR(100) NOT NULL , 
    ->   `telefono` VARCHAR(50) NOT NULL , 
    ->   `email` VARCHAR(100) NOT NULL 
    -> ) ENGINE = InnoDB;
Query OK, 0 rows affected (0,06 sec)

mysql> 


ALTER TABLE clientes
  ADD PRIMARY KEY (Identificador);
  
  ALTER TABLE clientes
  MODIFY COLUMN Identificador INT NOT NULL AUTO_INCREMENT;


mysql> ALTER TABLE clientes
    ->   ADD PRIMARY KEY (Identificador);
Query OK, 0 rows affected (0,12 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> ALTER TABLE clientes
    ->   MODIFY COLUMN Identificador INT NOT NULL AUTO_INCREMENT;
Query OK, 0 rows affected (0,14 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> 



