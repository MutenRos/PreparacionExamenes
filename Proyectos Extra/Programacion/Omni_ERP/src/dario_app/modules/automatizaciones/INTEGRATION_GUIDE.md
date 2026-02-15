"""
EJEMPLO DE INTEGRACIÓN: Cómo agregar automatizaciones a un módulo existente

Este archivo muestra cómo integrar los hooks de automatizaciones en los módulos
existentes como ventas, compras, etc.

PASOS A SEGUIR:
1. En el endpoint donde se crea una venta (POST /api/ventas), agregar:

    from dario_app.modules.automatizaciones.hooks import trigger_venta_creada
    
    # ... código para crear la venta ...
    
    # NUEVO: Ejecutar automatizaciones
    try:
        await trigger_venta_creada(db, org_id, {
            "venta_id": db_venta.id,
            "venta_numero": db_venta.numero,
            "cliente_nombre": db_venta.cliente_nombre,
            "cliente_email": db_venta.cliente_email,
            "monto": float(db_venta.total),
            "fecha": db_venta.fecha.isoformat(),
            "estado": db_venta.estado
        })
    except Exception as e:
        print(f"⚠️ Error ejecutando automatizaciones: {e}")
    
    return db_venta

2. Repetir para otros eventos: compras creadas, pagos recibidos, etc.

3. Para eventos que ocurren en background (ej: pago atrasado), se pueden
   usar tasks periódicas con APScheduler o Celery.
"""

# EJEMPLO COMPLETO de integración en ventas/routes.py:

EJEMPLO_CODIGO = """
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from dario_app.modules.automatizaciones.hooks import trigger_venta_creada

@router.post("/", response_model=VentaResponse, status_code=status.HTTP_201_CREATED)
async def create_venta(
    venta: VentaCreate,
    background_tasks: BackgroundTasks,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db)
):
    # ... código existente para crear venta ...
    
    db_venta = Venta(...)
    db.add(db_venta)
    await db.commit()
    await db.refresh(db_venta)
    
    # 🆕 AQUÍ: Ejecutar automatizaciones en background
    async def ejecutar_autos():
        try:
            await trigger_venta_creada(db, org_id, {
                "venta_id": db_venta.id,
                "venta_numero": db_venta.numero,
                "cliente_nombre": db_venta.cliente_nombre,
                "cliente_email": db_venta.cliente_email,
                "monto": float(db_venta.total),
                "fecha": db_venta.fecha.isoformat(),
                "estado": db_venta.estado
            })
        except Exception as e:
            print(f"⚠️ Automatizaciones: {e}")
    
    # Ejecutar en background sin bloquear
    background_tasks.add_task(ejecutar_autos)
    
    return db_venta
"""

print(__doc__)
print("\n" + "="*80 + "\n")
print("EJEMPLO DE IMPLEMENTACIÓN:")
print("="*80 + "\n")
print(EJEMPLO_CODIGO)
