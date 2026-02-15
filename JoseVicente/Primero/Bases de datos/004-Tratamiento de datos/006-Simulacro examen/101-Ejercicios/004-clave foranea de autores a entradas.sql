ALTER TABLE entradas 
ADD CONSTRAINT `autoresaentradas` 
FOREIGN KEY (`autor`) REFERENCES `autores`(`Identificador`) 
ON DELETE RESTRICT 
ON UPDATE RESTRICT;
