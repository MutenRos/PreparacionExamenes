-- Tabla Alumno
CREATE TABLE Alumno (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre     VARCHAR(100) NOT NULL,
    apellidos  VARCHAR(150) NOT NULL,
    email      VARCHAR(150) NOT NULL
) ENGINE=InnoDB;

-- Tabla Asignatura
CREATE TABLE Asignatura (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre       VARCHAR(150) NOT NULL,
    descripcion  TEXT
) ENGINE=InnoDB;

-- Tabla Matricula
CREATE TABLE Matricula (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    alumno_id INT NOT NULL,
    asignatura_id INT NOT NULL,

    CONSTRAINT fk_matricula_alumno
        FOREIGN KEY (alumno_id)
        REFERENCES Alumno(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_matricula_asignatura
        FOREIGN KEY (asignatura_id)
        REFERENCES Asignatura(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB;

