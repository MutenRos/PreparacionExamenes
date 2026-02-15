-- 1️⃣ Crear la tabla pedidos (sin relaciones todavía)
CREATE TABLE "pedidos" (
    "Identificador" INTEGER PRIMARY KEY AUTOINCREMENT,
    "cliente_id" INTEGER UNIQUE,
    "producto_id" INTEGER UNIQUE,
    "fecha" TEXT,
    "cantidad" INTEGER,
    "total" REAL
);

