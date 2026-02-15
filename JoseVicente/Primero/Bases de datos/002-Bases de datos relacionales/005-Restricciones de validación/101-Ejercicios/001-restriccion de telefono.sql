ALTER TABLE clientes
  ADD CONSTRAINT chk_telefono_length
  CHECK (CHAR_LENGTH(telefono) = 9);

