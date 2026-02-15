ALTER TABLE `empresarial`.`clientes`
  ADD PRIMARY KEY (`Identificador`);
  
  ALTER TABLE clientes
  MODIFY COLUMN Identificador INT NOT NULL AUTO_INCREMENT;
