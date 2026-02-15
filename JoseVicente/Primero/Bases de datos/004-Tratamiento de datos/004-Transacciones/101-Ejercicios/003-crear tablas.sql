-- ============================
-- 1) Tabla CATEGORIAS
-- ============================
CREATE TABLE categorias (
    id_categoria      INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre            VARCHAR(100) NOT NULL,
    descripcion       TEXT NULL,
    activa            TINYINT(1) NOT NULL DEFAULT 1,
    fecha_creacion    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT uq_categorias_nombre UNIQUE (nombre)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

-- ============================
-- 2) Tabla CLIENTES
-- ============================
CREATE TABLE clientes (
    id_cliente        INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre            VARCHAR(100) NOT NULL,
    apellidos         VARCHAR(150) NOT NULL,
    email             VARCHAR(150) NOT NULL,
    telefono          VARCHAR(30),
    direccion         VARCHAR(255),
    cp                VARCHAR(10),
    ciudad            VARCHAR(100),
    provincia         VARCHAR(100),
    pais              VARCHAR(100),
    fecha_registro    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    activo            TINYINT(1) NOT NULL DEFAULT 1,
    
    CONSTRAINT uq_clientes_email UNIQUE (email)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

-- ============================
-- 3) Tabla PRODUCTOS
-- ============================
CREATE TABLE productos (
    id_producto       INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_categoria      INT UNSIGNED NOT NULL,
    nombre            VARCHAR(150) NOT NULL,
    descripcion       TEXT,
    sku               VARCHAR(50),
    precio            DECIMAL(10,2) NOT NULL,
    impuesto_porcentaje DECIMAL(5,2) NOT NULL DEFAULT 21.00, -- % IVA, por ejemplo
    activo            TINYINT(1) NOT NULL DEFAULT 1,
    fecha_alta        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_productos_categorias
        FOREIGN KEY (id_categoria)
        REFERENCES categorias (id_categoria)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
        
    CONSTRAINT uq_productos_sku UNIQUE (sku),
    INDEX idx_productos_categoria (id_categoria),
    INDEX idx_productos_nombre (nombre)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

-- ============================
-- 4) Tabla PEDIDOS
-- ============================
CREATE TABLE pedidos (
    id_pedido         INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_cliente        INT UNSIGNED NOT NULL,
    fecha_pedido      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado            ENUM('pendiente','pagado','enviado','cancelado','devuelto')
                        NOT NULL DEFAULT 'pendiente',
    total_bruto       DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    total_impuestos   DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    total             DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    observaciones     TEXT,
    
    CONSTRAINT fk_pedidos_clientes
        FOREIGN KEY (id_cliente)
        REFERENCES clientes (id_cliente)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
        
    INDEX idx_pedidos_cliente (id_cliente),
    INDEX idx_pedidos_fecha (fecha_pedido),
    INDEX idx_pedidos_estado (estado)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

-- ============================
-- 5) Tabla GESTION_STOCK
--    (movimientos de stock)
-- ============================
CREATE TABLE gestion_stock (
    id_movimiento     INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_producto       INT UNSIGNED NOT NULL,
    tipo_movimiento   ENUM('entrada','salida','ajuste') NOT NULL,
    cantidad          INT NOT NULL,
    fecha_movimiento  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    referencia        VARCHAR(255) NULL, -- p.ej. "Pedido #123"
    observaciones     TEXT NULL,
    
    CONSTRAINT fk_stock_productos
        FOREIGN KEY (id_producto)
        REFERENCES productos (id_producto)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
        
    INDEX idx_stock_producto (id_producto),
    INDEX idx_stock_fecha (fecha_movimiento),
    INDEX idx_stock_tipo (tipo_movimiento)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

-- ============================
-- 6) Tabla LINEAS_PEDIDO
-- ============================
CREATE TABLE lineas_pedido (
    id_linea_pedido   INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_pedido         INT UNSIGNED NOT NULL,
    id_producto       INT UNSIGNED NOT NULL,
    cantidad          INT NOT NULL,
    precio_unitario   DECIMAL(10,2) NOT NULL, -- copia del precio en el momento del pedido
    impuesto_porcentaje DECIMAL(5,2) NOT NULL,
    total_linea       DECIMAL(10,2) NOT NULL,
    
    CONSTRAINT fk_lineas_pedido_pedidos
        FOREIGN KEY (id_pedido)
        REFERENCES pedidos (id_pedido)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
        
    CONSTRAINT fk_lineas_pedido_productos
        FOREIGN KEY (id_producto)
        REFERENCES productos (id_producto)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
        
    INDEX idx_lineas_pedido_pedido (id_pedido),
    INDEX idx_lineas_pedido_producto (id_producto)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;
