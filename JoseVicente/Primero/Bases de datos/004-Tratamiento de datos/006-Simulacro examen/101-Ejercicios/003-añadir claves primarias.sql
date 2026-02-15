DESCRIBE entradas;

ALTER TABLE entradas
  ADD PRIMARY KEY (`Identificador`);
  
  ALTER TABLE entradas
  MODIFY COLUMN Identificador INT NOT NULL AUTO_INCREMENT;
  
  DESCRIBE entradas;
  
  
DESCRIBE autores;

ALTER TABLE autores
  ADD PRIMARY KEY (`Identificador`);
  
  ALTER TABLE autores
  MODIFY COLUMN Identificador INT NOT NULL AUTO_INCREMENT;
  
  DESCRIBE autores;
