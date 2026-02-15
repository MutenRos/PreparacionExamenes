1.- Abro SQLite Browser / DB Browser
2.-Nueva base de datos
3.-La guardo en la carpeta del proyecto como tiendaonline.db
4.-Creo una tabla

CREATE TABLE "productos" (
	"Identificador"	INTEGER,
	"nombre"	TEXT,
	"descripcion"	TEXT,
	"precio"	TEXT,
	"imagen"	TEXT,
	PRIMARY KEY("Identificador" AUTOINCREMENT)
);

5.-No os olvidéis del boton "guardar cambios"

6.-Inserción de productos

INSERT INTO productos (nombre, descripcion, precio, imagen) VALUES
('Balón de fútbol', 'Balón oficial de tamaño 5 fabricado en cuero sintético resistente al desgaste.', '29.99 €', 'balon_futbol.jpg'),
('Raqueta de tenis', 'Raqueta ligera de grafito ideal para jugadores intermedios y avanzados.', '89.90 €', 'raqueta_tenis.jpg'),
('Zapatillas de running', 'Calzado deportivo con amortiguación y suela antideslizante para correr en asfalto o tierra.', '74.50 €', 'zapatillas_running.jpg'),
('Guantes de portero', 'Guantes con palma de látex para un agarre excepcional bajo cualquier condición.', '39.95 €', 'guantes_portero.jpg'),
('Camiseta deportiva', 'Camiseta transpirable con tecnología de secado rápido, disponible en varios colores.', '19.99 €', 'camiseta_deportiva.jpg'),
('Pantalón corto', 'Pantalón ligero con cintura elástica y bolsillos laterales, ideal para entrenamientos.', '24.50 €', 'pantalon_corto.jpg'),
('Bicicleta de montaña', 'Bicicleta con cuadro de aluminio y suspensión delantera para rutas de montaña.', '499.00 €', 'bicicleta_montana.jpg'),
('Casco de ciclismo', 'Casco ergonómico con ventilación y correa ajustable para máxima seguridad.', '45.00 €', 'casco_ciclismo.jpg'),
('Pelota de baloncesto', 'Balón de baloncesto oficial con superficie rugosa para mejor control.', '34.95 €', 'pelota_baloncesto.jpg'),
('Pesas ajustables', 'Set de pesas ajustables de hasta 20 kg con cierre de seguridad.', '119.00 €', 'pesas_ajustables.jpg'),
('Comba de entrenamiento', 'Cuerda ligera con rodamientos para saltos rápidos y precisos.', '12.99 €', 'comba_entrenamiento.jpg'),
('Colchoneta de yoga', 'Esterilla antideslizante y cómoda, ideal para yoga, pilates o estiramientos.', '22.00 €', 'colchoneta_yoga.jpg'),
('Gafas de natación', 'Gafas antivaho con ajuste de silicona y protección UV.', '15.90 €', 'gafas_natacion.jpg'),
('Gorra deportiva', 'Gorra transpirable con visera curva para proteger del sol durante el entrenamiento.', '9.99 €', 'gorra_deportiva.jpg'),
('Botella de agua deportiva', 'Botella reutilizable con cierre hermético y capacidad de 750 ml.', '8.50 €', 'botella_agua.jpg'),
('Mochila deportiva', 'Mochila resistente al agua con compartimento para calzado y ropa húmeda.', '34.00 €', 'mochila_deportiva.jpg'),
('Cinta elástica de resistencia', 'Cinta de entrenamiento de alta resistencia para ejercicios de fuerza.', '14.99 €', 'cinta_resistencia.jpg'),
('Patines en línea', 'Patines con ruedas de gel y freno trasero, perfectos para principiantes.', '89.00 €', 'patines_linea.jpg'),
('Protector bucal', 'Protector de doble capa para deportes de contacto, moldeable en agua caliente.', '6.99 €', 'protector_bucal.jpg'),
('Balón de voleibol', 'Balón de voleibol de tacto suave y costuras reforzadas.', '27.50 €', 'balon_voleibol.jpg');

7.-No os olvidéis del boton "guardar cambios"




