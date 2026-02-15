ALTER TABLE `posts` 
ADD CONSTRAINT `postsaautores` 
FOREIGN KEY (`autor`) 
REFERENCES `autores`(`Identificador`) 
ON DELETE RESTRICT ON UPDATE RESTRICT;
