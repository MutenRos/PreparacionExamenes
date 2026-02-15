-- 2️⃣ Añadir la relación 1:1 con clientes
ALTER TABLE "pedidos"
ADD FOREIGN KEY ("cliente_id") REFERENCES "clientes"("Identificador") ON DELETE CASCADE;

