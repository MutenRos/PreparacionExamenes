-- 1️⃣ Crear la nueva tabla con las claves foráneas
CREATE TABLE "pedidos" (
    "Identificador" INTEGER PRIMARY KEY AUTOINCREMENT,
    "cliente_id" INTEGER,
    "producto_id" INTEGER,
    "fecha" TEXT,
    "cantidad" INTEGER,
    "total" REAL,
    FOREIGN KEY ("cliente_id") REFERENCES "clientes"("Identificador") ON DELETE CASCADE,
    FOREIGN KEY ("producto_id") REFERENCES "productos"("Identificador") ON DELETE CASCADE
);

