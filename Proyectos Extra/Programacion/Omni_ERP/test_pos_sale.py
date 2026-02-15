import asyncio
import sys
import os
from sqlalchemy import select
from sqlalchemy.orm import selectinload

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

from dario_app.database import get_db
from dario_app.modules.pos.models import VentaPOS, VentaPOSDetalle
from dario_app.modules.inventario.models import Producto
from dario_app.modules.clientes.models import Cliente
from dario_app.modules.tenants.models import Organization
from dario_app.modules.calendario.models import Evento
from dario_app.modules.ventas.models import Venta
from dario_app.modules.compras.models import Compra

async def test_create_sale():
    print("Testing POS sale creation...")
    
    org_id = 1
    
    async for db in get_db(org_id):
        try:
            # 1. Get a product
            result = await db.execute(select(Producto).limit(1))
            producto = result.scalar_one_or_none()
            
            if not producto:
                print("No products found!")
                return

            print(f"Found product: {producto.nombre} (ID: {producto.id})")

            # 2. Generate number
            result = await db.execute(select(VentaPOS).where(VentaPOS.organization_id == org_id))
            count = len(result.scalars().all())
            numero = f"TEST-POS-{org_id}-{count + 1:06d}"
            print(f"Generated number: {numero}")

            # 3. Create VentaPOS
            venta = VentaPOS(
                organization_id=org_id,
                numero=numero,
                cliente_id=None,
                subtotal=100.0,
                descuento=0.0,
                impuesto=18.0,
                total=118.0,
                metodo_pago="efectivo",
                monto_pagado=120.0,
                cambio=2.0,
                estado="pendiente_aprobacion",
                observaciones="Test sale",
            )
            db.add(venta)
            await db.flush()
            print(f"Created VentaPOS with ID: {venta.id}")

            # 4. Create VentaPOSDetalle
            detalle = VentaPOSDetalle(
                venta_pos_id=venta.id,
                producto_id=producto.id,
                cantidad=1,
                precio_unitario=100.0,
                descuento=0.0,
                subtotal=100.0,
            )
            db.add(detalle)
            print("Added detail")

            await db.commit()
            print("Committed transaction")

            # 5. Load with relationship
            result = await db.execute(
                select(VentaPOS).options(selectinload(VentaPOS.detalles)).where(VentaPOS.id == venta.id)
            )
            loaded_venta = result.scalar_one()
            print(f"Loaded sale with {len(loaded_venta.detalles)} details")
            
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
            await db.rollback()

if __name__ == "__main__":
    asyncio.run(test_create_sale())
