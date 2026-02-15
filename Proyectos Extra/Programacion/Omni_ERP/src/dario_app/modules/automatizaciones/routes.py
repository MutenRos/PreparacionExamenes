"""API routes para automatizaciones."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.dependencies import get_db, get_org_id
from dario_app.modules.automatizaciones.models import (
    Automatizacion,
    Accion,
    RegistroAutomatizacion,
    TipoTrigger,
    TipoAccion,
)
from dario_app.modules.automatizaciones.schemas import (
    AutomatizacionCreateSchema,
    AutomatizacionUpdateSchema,
    AutomatizacionResponseSchema,
    RegistroAutomatizacionResponseSchema,
    TEMPLATES_AUTOMATIZACIONES,
)

router = APIRouter(prefix="/api/automatizaciones", tags=["automatizaciones"])


@router.get("/templates", tags=["automatizaciones"])
async def listar_templates():
    """Obtiene templates predefinidos de automatizaciones."""
    return {
        nombre: {
            "nombre": template.nombre,
            "descripcion": template.descripcion,
            "tipo_trigger": template.tipo_trigger.value,
            "acciones": [
                {
                    "tipo_accion": a.tipo_accion.value,
                    "parametros": a.parametros,
                    "orden": a.orden
                }
                for a in template.acciones
            ]
        }
        for nombre, template in TEMPLATES_AUTOMATIZACIONES.items()
    }


@router.get("/", response_model=List[AutomatizacionResponseSchema])
async def listar_automatizaciones(
    estado: Optional[str] = Query(None),
    trigger: Optional[str] = Query(None),
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Obtiene todas las automatizaciones de la organización."""
    query = select(Automatizacion).where(Automatizacion.organization_id == org_id)
    
    if estado:
        query = query.where(Automatizacion.estado == estado)
    if trigger:
        query = query.where(Automatizacion.tipo_trigger == trigger)
    
    query = query.order_by(Automatizacion.creado_en.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/", response_model=AutomatizacionResponseSchema, status_code=201)
async def crear_automatizacion(
    data: AutomatizacionCreateSchema,
    org_id: int = Depends(get_org_id),
    user_id: int = Depends(get_org_id),  # Simplificado
    db: AsyncSession = Depends(get_db)
):
    """Crea una nueva automatización."""
    
    # Crear automatización
    automatizacion = Automatizacion(
        organization_id=org_id,
        nombre=data.nombre,
        descripcion=data.descripcion,
        tipo_trigger=data.tipo_trigger,
        condiciones={"condiciones": []} if not data.condiciones else data.condiciones,
        continuar_en_error=data.continuar_en_error,
        tiempo_espera_minutos=data.tiempo_espera_minutos,
        creado_por=user_id
    )
    db.add(automatizacion)
    await db.flush()
    
    # Crear acciones
    for idx, accion_data in enumerate(data.acciones):
        accion = Accion(
            automatizacion_id=automatizacion.id,
            organization_id=org_id,
            tipo_accion=accion_data.tipo_accion,
            parametros=accion_data.parametros,
            orden=accion_data.orden or idx,
            activa=accion_data.activa
        )
        db.add(accion)
    
    await db.commit()
    await db.refresh(automatizacion)
    
    # Cargar acciones
    query = select(Accion).where(Accion.automatizacion_id == automatizacion.id)
    result = await db.execute(query)
    automatizacion.acciones = result.scalars().all()
    
    return automatizacion


@router.get("/{automatizacion_id}", response_model=AutomatizacionResponseSchema)
async def obtener_automatizacion(
    automatizacion_id: int,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Obtiene una automatización específica."""
    automatizacion = await db.get(Automatizacion, automatizacion_id)
    
    if not automatizacion or automatizacion.organization_id != org_id:
        raise HTTPException(status_code=404, detail="Automatización no encontrada")
    
    # Cargar acciones
    query = select(Accion).where(Accion.automatizacion_id == automatizacion.id)
    result = await db.execute(query)
    automatizacion.acciones = result.scalars().all()
    
    return automatizacion


@router.put("/{automatizacion_id}", response_model=AutomatizacionResponseSchema)
async def actualizar_automatizacion(
    automatizacion_id: int,
    data: AutomatizacionUpdateSchema,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Actualiza una automatización."""
    automatizacion = await db.get(Automatizacion, automatizacion_id)
    
    if not automatizacion or automatizacion.organization_id != org_id:
        raise HTTPException(status_code=404, detail="Automatización no encontrada")
    
    # Actualizar campos
    if data.nombre:
        automatizacion.nombre = data.nombre
    if data.descripcion is not None:
        automatizacion.descripcion = data.descripcion
    if data.estado:
        automatizacion.estado = data.estado
    if data.activa is not None:
        automatizacion.activa = data.activa
    if data.condiciones is not None:
        automatizacion.condiciones = data.condiciones
    if data.continuar_en_error is not None:
        automatizacion.continuar_en_error = data.continuar_en_error
    if data.tiempo_espera_minutos is not None:
        automatizacion.tiempo_espera_minutos = data.tiempo_espera_minutos
    
    # Actualizar acciones si se proporcionan
    if data.acciones:
        # Eliminar acciones antiguas
        query = select(Accion).where(Accion.automatizacion_id == automatizacion.id)
        result = await db.execute(query)
        for accion in result.scalars().all():
            await db.delete(accion)
        
        # Crear nuevas acciones
        for idx, accion_data in enumerate(data.acciones):
            accion = Accion(
                automatizacion_id=automatizacion.id,
                organization_id=org_id,
                tipo_accion=accion_data.tipo_accion,
                parametros=accion_data.parametros,
                orden=accion_data.orden or idx,
                activa=accion_data.activa
            )
            db.add(accion)
    
    await db.commit()
    await db.refresh(automatizacion)
    
    # Cargar acciones
    query = select(Accion).where(Accion.automatizacion_id == automatizacion.id)
    result = await db.execute(query)
    automatizacion.acciones = result.scalars().all()
    
    return automatizacion


@router.delete("/{automatizacion_id}")
async def eliminar_automatizacion(
    automatizacion_id: int,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Elimina una automatización."""
    automatizacion = await db.get(Automatizacion, automatizacion_id)
    
    if not automatizacion or automatizacion.organization_id != org_id:
        raise HTTPException(status_code=404, detail="Automatización no encontrada")
    
    await db.delete(automatizacion)
    await db.commit()
    
    return {"detail": "Automatización eliminada"}


@router.post("/{automatizacion_id}/activar")
async def activar_automatizacion(
    automatizacion_id: int,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Activa una automatización."""
    automatizacion = await db.get(Automatizacion, automatizacion_id)
    
    if not automatizacion or automatizacion.organization_id != org_id:
        raise HTTPException(status_code=404, detail="Automatización no encontrada")
    
    automatizacion.activa = True
    await db.commit()
    
    return {"detail": "Automatización activada"}


@router.post("/{automatizacion_id}/desactivar")
async def desactivar_automatizacion(
    automatizacion_id: int,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Desactiva una automatización."""
    automatizacion = await db.get(Automatizacion, automatizacion_id)
    
    if not automatizacion or automatizacion.organization_id != org_id:
        raise HTTPException(status_code=404, detail="Automatización no encontrada")
    
    automatizacion.activa = False
    await db.commit()
    
    return {"detail": "Automatización desactivada"}


# ═══════════════════════════════════════════════════════════════════════════════
# REGISTROS Y ESTADÍSTICAS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/{automatizacion_id}/registros", response_model=List[RegistroAutomatizacionResponseSchema])
async def obtener_registros_automatizacion(
    automatizacion_id: int,
    limite: int = Query(50, le=100),
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Obtiene los registros de ejecución de una automatización."""
    # Verificar que la automatización pertenece a la org
    automatizacion = await db.get(Automatizacion, automatizacion_id)
    if not automatizacion or automatizacion.organization_id != org_id:
        raise HTTPException(status_code=404, detail="Automatización no encontrada")
    
    query = select(RegistroAutomatizacion).where(
        RegistroAutomatizacion.automatizacion_id == automatizacion_id
    ).order_by(RegistroAutomatizacion.ejecutado_en.desc()).limit(limite)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{automatizacion_id}/estadisticas")
async def obtener_estadisticas_automatizacion(
    automatizacion_id: int,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db)
):
    """Obtiene estadísticas de ejecución."""
    automatizacion = await db.get(Automatizacion, automatizacion_id)
    
    if not automatizacion or automatizacion.organization_id != org_id:
        raise HTTPException(status_code=404, detail="Automatización no encontrada")
    
    return {
        "automatizacion_id": automatizacion.id,
        "nombre": automatizacion.nombre,
        "total_ejecuciones": automatizacion.total_ejecuciones,
        "ejecuciones_exitosas": automatizacion.ejecuciones_exitosas,
        "ejecuciones_fallidas": automatizacion.ejecuciones_fallidas,
        "tasa_exito": (
            automatizacion.ejecuciones_exitosas / automatizacion.total_ejecuciones * 100
            if automatizacion.total_ejecuciones > 0
            else 0
        ),
        "ultima_ejecucion": automatizacion.ultima_ejecucion
    }
