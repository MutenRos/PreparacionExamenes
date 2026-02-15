CREATE TABLE "pedidos" (
    "Identificador" INTEGER PRIMARY KEY AUTOINCREMENT,
    "cliente_id" INTEGER UNIQUE,
    "producto_id" INTEGER UNIQUE,
    "fecha" TEXT,
    "cantidad" INTEGER,
    "total" REAL,
    FOREIGN KEY("cliente_id") REFERENCES "clientes"("Identificador") ON DELETE CASCADE,
    FOREIGN KEY("producto_id") REFERENCES "productos"("Identificador") ON DELETE CASCADE
);
