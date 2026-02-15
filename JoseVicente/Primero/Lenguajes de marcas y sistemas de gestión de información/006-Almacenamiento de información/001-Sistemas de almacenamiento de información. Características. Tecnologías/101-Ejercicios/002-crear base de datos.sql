sudo mysql -u root -p

-- 1. Crear base de datos
CREATE DATABASE discos
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- 2. Crear usuario (si no existe)
CREATE USER IF NOT EXISTS 'discos'@'%' IDENTIFIED BY 'discos';

-- 3. Conceder permisos totales sobre la base de datos
GRANT ALL PRIVILEGES ON discos.* TO 'discos'@'%';

FLUSH PRIVILEGES;

-- 4. Usar la base de datos
USE discos;

-- 5. Crear tabla discos (álbumes musicales)
CREATE TABLE discos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    artista VARCHAR(255) NOT NULL,
    anio INT,
    genero VARCHAR(100),
    duracion_minutos INT,
    fecha_compra DATE,
    precio DECIMAL(6,2)
);

-- 6. Insertar datos de ejemplo
INSERT INTO discos (titulo, artista, anio, genero, duracion_minutos, fecha_compra, precio)
VALUES 
('The Dark Side of the Moon', 'Pink Floyd', 1973, 'Rock Progresivo', 43, '2024-01-15', 12.95),
('Thriller', 'Michael Jackson', 1982, 'Pop', 42, '2023-11-01', 9.99),
('Back in Black', 'AC/DC', 1980, 'Rock', 41, '2024-02-10', 11.50),
('Nevermind', 'Nirvana', 1991, 'Grunge', 49, '2024-03-05', 10.00),
('Rumours', 'Fleetwood Mac', 1977, 'Soft Rock', 39, '2024-01-20', 8.75);

