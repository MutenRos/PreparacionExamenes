-- 3️⃣ Añadir la relación 1:1 con productos
ALTER TABLE "pedidos"
ADD FOREIGN KEY ("producto_id") REFERENCES "productos"("Identificador") ON DELETE CASCADE;

