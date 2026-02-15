"""Rutas API para el módulo de calendario."""

from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from dario_app.core.auth import get_tenant_db, require_auth

from .models import Evento
from .schemas import EventoCreate, EventoResponse, EventoUpdate

router = APIRouter(prefix="/api/calendario", tags=["calendario"])


@router.get("/eventos", response_model=List[EventoResponse])
async def listar_eventos(
    inicio: Optional[str] = Query(None, description="Fecha inicio YYYY-MM-DD"),
    fin: Optional[str] = Query(None, description="Fecha fin YYYY-MM-DD"),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo"),
    completado: Optional[bool] = Query(None, description="Filtrar por completado"),
    db: AsyncSession = Depends(get_tenant_db),
    user_context: dict = Depends(require_auth),
):
    """Obtener eventos del calendario con filtros opcionales."""
    query = select(Evento).where(Evento.organization_id == user_context["org_id"])

    # Filtro de fechas
    if inicio:
        fecha_inicio = datetime.fromisoformat(inicio)
        query = query.where(Evento.fecha_inicio >= fecha_inicio)
    if fin:
        fecha_fin = datetime.fromisoformat(fin)
        query = query.where(Evento.fecha_inicio <= fecha_fin)

    # Filtro por tipo
    if tipo:
        query = query.where(Evento.tipo == tipo)

    # Filtro por completado
    if completado is not None:
        query = query.where(Evento.completado == completado)

    query = query.order_by(Evento.fecha_inicio.desc())
    result = await db.execute(query)
    eventos = result.scalars().all()
    return eventos


@router.post("/eventos-publico", response_model=EventoResponse)
async def crear_evento_publico(
    evento: EventoCreate,
    org: int = Query(..., description="ID de la organización"),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Crear un evento desde widget público (sin autenticación)."""
    db_evento = Evento(**evento.model_dump(), organization_id=org)
    db.add(db_evento)
    await db.commit()
    await db.refresh(db_evento)
    return db_evento


@router.post("/eventos", response_model=EventoResponse)
async def crear_evento(
    evento: EventoCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user_context: dict = Depends(require_auth),
):
    """Crear un nuevo evento en el calendario."""
    db_evento = Evento(**evento.model_dump(), organization_id=user_context["org_id"])
    db.add(db_evento)
    await db.commit()
    await db.refresh(db_evento)
    return db_evento


@router.get("/eventos/{evento_id}", response_model=EventoResponse)
async def obtener_evento(
    evento_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user_context: dict = Depends(require_auth),
):
    """Obtener un evento específico."""
    query = select(Evento).where(
        and_(Evento.id == evento_id, Evento.organization_id == user_context["org_id"])
    )
    result = await db.execute(query)
    evento = result.scalar_one_or_none()

    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    return evento


@router.put("/eventos/{evento_id}", response_model=EventoResponse)
async def actualizar_evento(
    evento_id: int,
    evento_update: EventoUpdate,
    db: AsyncSession = Depends(get_tenant_db),
    user_context: dict = Depends(require_auth),
):
    """Actualizar un evento existente."""
    query = select(Evento).where(
        and_(Evento.id == evento_id, Evento.organization_id == user_context["org_id"])
    )
    result = await db.execute(query)
    db_evento = result.scalar_one_or_none()

    if not db_evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    # Actualizar campos
    update_data = evento_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_evento, field, value)

    db_evento.actualizado_en = datetime.utcnow()
    await db.commit()
    await db.refresh(db_evento)
    return db_evento


@router.delete("/eventos/{evento_id}")
async def eliminar_evento(
    evento_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user_context: dict = Depends(require_auth),
):
    """Eliminar un evento."""
    query = select(Evento).where(
        and_(Evento.id == evento_id, Evento.organization_id == user_context["org_id"])
    )
    result = await db.execute(query)
    evento = result.scalar_one_or_none()

    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    await db.delete(evento)
    await db.commit()
    return {"detail": "Evento eliminado"}


@router.get("/proximos", response_model=List[EventoResponse])
async def proximos_eventos(
    dias: int = Query(7, description="Días hacia adelante"),
    db: AsyncSession = Depends(get_tenant_db),
    user_context: dict = Depends(require_auth),
):
    """Obtener eventos próximos (para dashboard)."""
    ahora = datetime.utcnow()
    limite = ahora + timedelta(days=dias)

    query = (
        select(Evento)
        .where(
            and_(
                Evento.organization_id == user_context["org_id"],
                Evento.fecha_inicio >= ahora,
                Evento.fecha_inicio <= limite,
                Evento.completado is False,
            )
        )
        .order_by(Evento.fecha_inicio.asc())
        .limit(10)
    )

    result = await db.execute(query)
    eventos = result.scalars().all()
    return eventos
