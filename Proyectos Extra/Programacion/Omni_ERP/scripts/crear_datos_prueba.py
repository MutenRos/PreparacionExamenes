"""Crear datos de prueba para el sistema ERP."""

import asyncio
from decimal import Decimal

from dario_app.database import async_session_maker
from dario_app.modules.clientes.models import Cliente
from dario_app.modules.inventario.models import Producto

# Import all models to ensure they're registered with SQLAlchemy


async def crear_datos_prueba():
    """Crea datos de prueba en la base de datos."""
    async with async_session_maker() as db:
        # Verificar si ya hay datos
        from sqlalchemy import select

        result = await db.execute(select(Producto).limit(1))
        if result.scalar_one_or_none():
            print("⚠️  Ya existen datos en la base de datos")
            return

        # Productos de prueba
        productos = [
            Producto(
                codigo="PROD001",
                nombre="Laptop HP 15",
                descripcion="Laptop HP 15 pulgadas, 8GB RAM, 256GB SSD",
                categoria="Electrónica",
                precio_compra=Decimal("450.00"),
                precio_venta=Decimal("599.99"),
                stock_actual=15,
                stock_minimo=5,
                unidad_medida="unidad",
                organization_id=1,
            ),
            Producto(
                codigo="PROD002",
                nombre="Mouse Logitech",
                descripcion="Mouse inalámbrico Logitech",
                categoria="Electrónica",
                precio_compra=Decimal("12.00"),
                precio_venta=Decimal("19.99"),
                stock_actual=50,
                stock_minimo=10,
                unidad_medida="unidad",
                organization_id=1,
            ),
            Producto(
                codigo="PROD003",
                nombre="Teclado Mecánico",
                descripcion="Teclado mecánico RGB",
                categoria="Electrónica",
                precio_compra=Decimal("35.00"),
                precio_venta=Decimal("59.99"),
                stock_actual=25,
                stock_minimo=8,
                unidad_medida="unidad",
                organization_id=1,
            ),
            Producto(
                codigo="PROD004",
                nombre="Monitor 24 pulgadas",
                descripcion="Monitor LED 24 pulgadas Full HD",
                categoria="Electrónica",
                precio_compra=Decimal("120.00"),
                precio_venta=Decimal("179.99"),
                stock_actual=12,
                stock_minimo=5,
                unidad_medida="unidad",
                organization_id=1,
            ),
            Producto(
                codigo="PROD005",
                nombre="Cable HDMI",
                descripcion="Cable HDMI 2.0 de 2 metros",
                categoria="Accesorios",
                precio_compra=Decimal("3.00"),
                precio_venta=Decimal("7.99"),
                stock_actual=100,
                stock_minimo=20,
                unidad_medida="unidad",
                organization_id=1,
            ),
            Producto(
                codigo="PROD006",
                nombre="Mochila para Laptop",
                descripcion="Mochila resistente para laptop hasta 15 pulgadas",
                categoria="Accesorios",
                precio_compra=Decimal("15.00"),
                precio_venta=Decimal("29.99"),
                stock_actual=30,
                stock_minimo=10,
                unidad_medida="unidad",
                organization_id=1,
            ),
            Producto(
                codigo="PROD007",
                nombre="Auriculares Bluetooth",
                descripcion="Auriculares inalámbricos con cancelación de ruido",
                categoria="Electrónica",
                precio_compra=Decimal("45.00"),
                precio_venta=Decimal("79.99"),
                stock_actual=20,
                stock_minimo=8,
                unidad_medida="unidad",
                organization_id=1,
            ),
            Producto(
                codigo="PROD008",
                nombre="Webcam HD",
                descripcion="Webcam 1080p con micrófono integrado",
                categoria="Electrónica",
                precio_compra=Decimal("25.00"),
                precio_venta=Decimal("44.99"),
                stock_actual=18,
                stock_minimo=6,
                unidad_medida="unidad",
                organization_id=1,
            ),
            Producto(
                codigo="PROD009",
                nombre="USB 32GB",
                descripcion="Memoria USB 3.0 de 32GB",
                categoria="Almacenamiento",
                precio_compra=Decimal("5.00"),
                precio_venta=Decimal("12.99"),
                stock_actual=80,
                stock_minimo=15,
                unidad_medida="unidad",
                organization_id=1,
            ),
            Producto(
                codigo="PROD010",
                nombre="Disco Duro Externo 1TB",
                descripcion="Disco duro externo portátil 1TB USB 3.0",
                categoria="Almacenamiento",
                precio_compra=Decimal("40.00"),
                precio_venta=Decimal("69.99"),
                stock_actual=10,
                stock_minimo=4,
                unidad_medida="unidad",
                organization_id=1,
            ),
        ]

        # Clientes de prueba
        clientes = [
            Cliente(
                nombre="Juan Pérez",
                email="juan.perez@email.com",
                telefono="555-0101",
                direccion="Calle Principal 123",
                organization_id=1,
            ),
            Cliente(
                nombre="María García",
                email="maria.garcia@email.com",
                telefono="555-0102",
                direccion="Av. Central 456",
                organization_id=1,
            ),
            Cliente(
                nombre="Carlos López",
                email="carlos.lopez@email.com",
                telefono="555-0103",
                direccion="Plaza Mayor 789",
                organization_id=1,
            ),
            Cliente(
                nombre="Ana Martínez",
                email="ana.martinez@email.com",
                telefono="555-0104",
                direccion="Calle Secundaria 321",
                organization_id=1,
            ),
            Cliente(
                nombre="Pedro Sánchez",
                email="pedro.sanchez@email.com",
                telefono="555-0105",
                direccion="Av. Libertad 654",
                organization_id=1,
            ),
        ]

        # Agregar a la sesión
        for producto in productos:
            db.add(producto)

        for cliente in clientes:
            db.add(cliente)

        await db.commit()

        print("✅ Datos de prueba creados exitosamente:")
        print(f"   - {len(productos)} productos")
        print(f"   - {len(clientes)} clientes")


if __name__ == "__main__":
    asyncio.run(crear_datos_prueba())
