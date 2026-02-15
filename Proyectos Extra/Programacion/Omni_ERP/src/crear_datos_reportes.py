"""Script para crear datos de prueba para reportes."""

import asyncio
from datetime import datetime, timedelta

from sqlalchemy import select

from dario_app.database import async_session_maker
from dario_app.modules.compras.models import Compra, CompraDetalle
from dario_app.modules.inventario.models import Producto
from dario_app.modules.pos.models import VentaPOS
from dario_app.modules.tenants.models import Organization
from dario_app.modules.ventas.models import Venta, VentaDetalle


async def crear_datos_prueba():
    """Crear datos de prueba para reportes."""
    async with async_session_maker() as session:
        try:
            # Obtener o crear organización
            result = await session.execute(select(Organization).limit(1))
            org = result.scalar()

            if not org:
                print("Creando organización...")
                org = Organization(
                    nombre="ERP Dario Admin", slug="admin", email="admin@erpdario.com"
                )
                session.add(org)
                await session.flush()

            org_id = org.id
            print(f"✓ Usando organización: {org.nombre} (ID: {org_id})")

            # Crear productos si no existen
            result = await session.execute(
                select(Producto).where(Producto.organization_id == org_id)
            )
            productos = result.scalars().all()

            if not productos:
                print("Creando productos de prueba...")
                productos_data = [
                    {
                        "codigo": "P001",
                        "nombre": "Laptop Dell",
                        "precio_venta": 3500,
                        "precio_compra": 2000,
                        "stock_actual": 5,
                        "stock_minimo": 2,
                    },
                    {
                        "codigo": "P002",
                        "nombre": "Mouse Logitech",
                        "precio_venta": 150,
                        "precio_compra": 80,
                        "stock_actual": 50,
                        "stock_minimo": 10,
                    },
                    {
                        "codigo": "P003",
                        "nombre": "Teclado Mecánico",
                        "precio_venta": 250,
                        "precio_compra": 150,
                        "stock_actual": 30,
                        "stock_minimo": 5,
                    },
                    {
                        "codigo": "P004",
                        "nombre": "Monitor LG",
                        "precio_venta": 800,
                        "precio_compra": 500,
                        "stock_actual": 1,
                        "stock_minimo": 3,
                    },  # Bajo stock
                    {
                        "codigo": "P005",
                        "nombre": "Webcam HD",
                        "precio_venta": 200,
                        "precio_compra": 120,
                        "stock_actual": 20,
                        "stock_minimo": 5,
                    },
                ]

                for p in productos_data:
                    producto = Producto(organization_id=org_id, **p)
                    session.add(producto)
                    productos.append(producto)

                await session.commit()
                print(f"✓ {len(productos)} productos creados")
            else:
                print(f"✓ {len(productos)} productos ya existen")

            # Crear ventas de prueba para últimos 7 días
            print("Creando ventas de prueba...")
            ventas_creadas = []
            contador = 1000
            for i in range(7):
                fecha = datetime.utcnow() - timedelta(days=i)

                # 2-3 ventas por día
                for j in range(2 + (i % 2)):
                    venta = Venta(
                        organization_id=org_id,
                        numero=f"V-{contador}",
                        cliente_nombre=f"Cliente {i}-{j}",
                        total=1000 + (i * 100) + (j * 500),
                        estado="completada",
                        creado_en=fecha,
                    )
                    session.add(venta)
                    ventas_creadas.append(venta)
                    contador += 1

            await session.flush()  # Flush para que se asignen los IDs

            # Agregar detalles de venta
            for venta in ventas_creadas:
                for k in range(2):
                    if k < len(productos):
                        detalle = VentaDetalle(
                            venta_id=venta.id,
                            producto_id=productos[k].id,
                            cantidad=2 + k,
                            precio_unitario=productos[k].precio_venta,
                            subtotal=(2 + k) * productos[k].precio_venta,
                        )
                        session.add(detalle)

            await session.commit()
            print("✓ Ventas de prueba creadas")

            # Crear compras de prueba
            print("Creando compras de prueba...")
            compras_creadas = []
            contador_compras = 5000
            for i in range(5):
                fecha = datetime.utcnow() - timedelta(days=i * 2)
                compra = Compra(
                    organization_id=org_id,
                    numero=f"C-{contador_compras}",
                    proveedor_nombre=f"Proveedor {i}",
                    total=2000 + (i * 500),
                    estado="completada",
                    creado_en=fecha,
                )
                session.add(compra)
                compras_creadas.append(compra)
                contador_compras += 1

            await session.flush()  # Flush para que se asignen los IDs

            # Detalles de compra
            for compra in compras_creadas:
                for k in range(2):
                    if k < len(productos):
                        detalle = CompraDetalle(
                            compra_id=compra.id,
                            producto_id=productos[k].id,
                            cantidad=5 + k,
                            precio_unitario=productos[k].precio_compra,
                            subtotal=(5 + k) * productos[k].precio_compra,
                        )
                        session.add(detalle)

            await session.commit()
            print("✓ Compras de prueba creadas")

            # Crear ventas POS
            print("Creando ventas POS de prueba...")
            for i in range(10):
                fecha = datetime.utcnow() - timedelta(days=i % 7)
                venta_pos = VentaPOS(
                    organization_id=org_id,
                    numero=f"POS-{1000 + i}",
                    total=500 + (i * 100),
                    estado="pagada",
                    creado_en=fecha,
                )
                session.add(venta_pos)

            await session.commit()
            print("✓ Ventas POS de prueba creadas")

            print("\n✅ Datos de prueba creados exitosamente!")
            print("\nResumen:")
            print(f"  - Productos: {len(productos)}")

            # Contar ventas
            result = await session.execute(select(Venta).where(Venta.organization_id == org_id))
            ventas_count = len(result.scalars().all())
            print(f"  - Ventas: {ventas_count}")

            # Contar compras
            result = await session.execute(select(Compra).where(Compra.organization_id == org_id))
            compras_count = len(result.scalars().all())
            print(f"  - Compras: {compras_count}")

            # Contar bajo stock
            result = await session.execute(
                select(Producto).where(
                    Producto.organization_id == org_id,
                    Producto.stock_actual <= Producto.stock_minimo,
                )
            )
            bajo_stock = len(result.scalars().all())
            print(f"  - Productos bajo stock: {bajo_stock}")

        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback

            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(crear_datos_prueba())
