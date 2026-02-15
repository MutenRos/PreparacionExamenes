import asyncio
import sys
import os
from sqlalchemy import select, desc
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

from dario_app.database import get_db
from dario_app.modules.pos.models import VentaPOS, VentaPOSDetalle
from dario_app.modules.ventas.models import Venta, VentaDetalle
from dario_app.modules.inventario.models import Producto
from dario_app.modules.clientes.models import Cliente
from dario_app.modules.tenants.models import Organization
from dario_app.modules.calendario.models import Evento
from dario_app.modules.compras.models import Compra
from dario_app.modules.oficina_tecnica.models import BOMHeader, BOMOperacion
from dario_app.modules.produccion_ordenes.models import (
    OrdenProduccion,
    OperacionProduccion,
    EstadoOrdenProduccion,
    TipoPrioridad,
)

async def test_approve_sale():
    print("Testing POS sale approval...")
    
    # Mock dependencies
    org_id = 1
    
    async for db in get_db():
        try:
            # 1. Create a pending POS sale
            print("Creating pending POS sale...")
            result = await db.execute(select(VentaPOS).where(VentaPOS.organization_id == org_id))
            count = len(result.scalars().all())
            numero = f"POS-{org_id}-{count + 1:06d}"
            
            # Get a product
            producto_result = await db.execute(select(Producto).limit(1))
            producto = producto_result.scalar_one()
            print(f"Found product: {producto.nombre} (ID: {producto.id})")

            db_venta = VentaPOS(
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
                observaciones="Test approval",
            )
            db.add(db_venta)
            await db.flush()
            
            db_detalle = VentaPOSDetalle(
                venta_pos_id=db_venta.id,
                producto_id=producto.id,
                cantidad=1,
                precio_unitario=100.0,
                descuento=0.0,
                subtotal=100.0,
            )
            db.add(db_detalle)
            await db.commit()
            await db.refresh(db_venta)
            print(f"Created pending sale ID: {db_venta.id}")
            
            # 2. Simulate approval logic
            print("Simulating approval...")
            venta_pos_id = db_venta.id
            
            result = await db.execute(
                select(VentaPOS).where(VentaPOS.id == venta_pos_id, VentaPOS.organization_id == org_id)
            )
            venta = result.scalar_one_or_none()
            if not venta:
                print("Venta POS no encontrada")
                return
            venta.estado = "completada"
            await db.flush()

            # Crear una Venta tradicional
            existing_ventas = await db.execute(select(Venta).where(Venta.organization_id == org_id))
            ventas_count = len(existing_ventas.scalars().all())
            venta_numero = f"V-{org_id}-{ventas_count + 1:06d}"

            db_venta_trad = Venta(
                organization_id=org_id,
                numero=venta_numero,
                cliente_nombre="Cliente POS" if not venta.cliente_id else "Cliente",
                cliente_id=venta.cliente_id,
                total=venta.total,
                subtotal=venta.subtotal,
                iva=venta.impuesto,
                notas=(venta.observaciones or "") + f" | Generada desde POS {venta.numero}",
                estado="pendiente",
            )
            db.add(db_venta_trad)
            await db.flush()
            print(f"Created traditional sale ID: {db_venta_trad.id}")

            # Crear detalles de venta
            detalles_res = await db.execute(
                select(VentaPOSDetalle).where(VentaPOSDetalle.venta_pos_id == venta.id)
            )
            detalles = detalles_res.scalars().all()
            for d in detalles:
                db_det = VentaDetalle(
                    venta_id=db_venta_trad.id,
                    producto_id=d.producto_id,
                    cantidad=d.cantidad,
                    precio_unitario=d.precio_unitario,
                    subtotal=d.cantidad * d.precio_unitario,
                )
                db.add(db_det)

            await db.flush()
            print("Details added.")

            # Crear órdenes de producción
            print("Checking for BOMs...")
            for d in detalles:
                bom_q = await db.execute(
                    select(BOMHeader).where(
                        (BOMHeader.producto_id == d.producto_id) &
                        (BOMHeader.organization_id == org_id) &
                        (BOMHeader.activo == True) &
                        (BOMHeader.es_principal == True)
                    ).order_by(BOMHeader.id.desc())
                )
                bom = bom_q.scalar_one_or_none()
                if not bom:
                    print(f"No BOM for product {d.producto_id}")
                    continue
                
                print(f"Found BOM {bom.id} for product {d.producto_id}")

                # Generar número de orden
                last_order = (await db.execute(
                    select(OrdenProduccion).where(OrdenProduccion.organization_id == org_id).order_by(desc(OrdenProduccion.id)).limit(1)
                )).scalar_one_or_none()
                
                # FIX: Handle case where last_order is None correctly for ID access
                last_id = last_order.id if last_order else 0
                order_number = f"OP-{datetime.utcnow().year}-{last_id + 1:05d}"

                nueva_orden = OrdenProduccion(
                    organization_id=org_id,
                    venta_id=db_venta_trad.id,
                    bom_id=bom.id,
                    producto_id=d.producto_id,
                    numero=order_number,
                    cantidad_ordenada=d.cantidad,
                    descripcion=f"POS {venta.numero} → producto {d.producto_id}",
                    prioridad=TipoPrioridad.MEDIA.value,
                    estado=EstadoOrdenProduccion.PENDIENTE_ASIGNACION.value,
                )
                db.add(nueva_orden)
                await db.flush()
                print(f"Created Production Order {nueva_orden.id}")

                # Crear operaciones desde BOM
                ops = (await db.execute(
                    select(BOMOperacion).where(BOMOperacion.bom_header_id == bom.id).order_by(BOMOperacion.secuencia)
                )).scalars().all()
                for idx, bom_op in enumerate(ops, 1):
                    operacion = OperacionProduccion(
                        organization_id=org_id,
                        orden_produccion_id=nueva_orden.id,
                        # ... (simplified for test)
                        nombre=bom_op.nombre,
                        descripcion=bom_op.descripcion,
                        centro_trabajo_id=bom_op.centro_trabajo_id,
                        tiempo_estimado=bom_op.tiempo_estimado,
                        secuencia=bom_op.secuencia,
                        estado="pendiente"
                    )
                    db.add(operacion)
            
            await db.commit()
            print("Approval simulation completed successfully.")

        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
            await db.rollback()
        break

if __name__ == "__main__":
    asyncio.run(test_approve_sale())