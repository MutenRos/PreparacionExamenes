ALTER TABLE `empresarial`.`productos`
  ADD PRIMARY KEY (`Identificador`);
  
  ALTER TABLE productos
  MODIFY COLUMN Identificador INT NOT NULL AUTO_INCREMENT;
