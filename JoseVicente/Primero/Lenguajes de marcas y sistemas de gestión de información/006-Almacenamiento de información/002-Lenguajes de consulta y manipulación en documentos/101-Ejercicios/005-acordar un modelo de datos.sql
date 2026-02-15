-- 1. CREATE DATABASE
CREATE DATABASE IF NOT EXISTS training_center
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE training_center;

-- 2. CREATE TABLE WITH MANY FIELD TYPES
CREATE TABLE inscripciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telefono VARCHAR(20),

    curso VARCHAR(200) NOT NULL,                 -- Example of VARCHAR
    fecha_inscripcion DATE NOT NULL,             -- DATE type
    edad INT,                                    -- INT type
    precio DECIMAL(10,2),                        -- DECIMAL type
    pagado BOOLEAN DEFAULT 0,                    -- BOOLEAN
    modalidad ENUM('presencial','online','mixto'),   -- ENUM type

    notas TEXT,                                  -- TEXT type
    documento BLOB,                              -- BLOB (left empty in inserts)

    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. INSERT SAMPLE DATA (BLOB field left empty)
INSERT INTO inscripciones (
    nombre, apellidos, email, telefono, curso,
    fecha_inscripcion, edad, precio, pagado, modalidad, notas, documento
) VALUES
(
    'Laura', 'Martínez López', 'laura.martinez@example.com', '600123123',
    'Curso de Python Básico',
    '2025-02-01', 28, 199.99, 1, 'online',
    'Interesada en horario de tarde.',
    NULL
),
(
    'Carlos', 'Gómez Ruiz', 'carlos.gomez@example.com', '611456789',
    'Introducción a Linux',
    '2025-02-12', 34, 149.00, 0, 'presencial',
    'Solicita factura para empresa.',
    NULL
),
(
    'Ana', 'Serrano Torres', 'ana.serrano@example.com', '699222333',
    'Desarrollo Web Full Stack',
    '2025-02-15', 22, 499.50, 1, 'mixto',
    'Tiene conocimientos previos de HTML.',
    NULL
);

