"""Rutas API para el módulo de calendario."""

from datetime import datetime, timedelta
from typing import List, Optional
import secrets
import json

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.auth import get_tenant_db, require_auth
from core.dependencies import get_db, get_org_id
from services.email_service import email_service

from .models import Evento, Cita, ConfiguracionCitas
from .schemas import (
    EventoCreate, EventoResponse, EventoUpdate,
    CitaCreate, CitaResponse, CitaUpdate,
    ConfiguracionCitasCreate, ConfiguracionCitasResponse, ConfiguracionCitasUpdate,
    DisponibilidadDia, DisponibilidadSlot
)

router = APIRouter(prefix="/api/calendario", tags=["calendario"])
templates = Jinja2Templates(directory="dario_app/templates")


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


# ═══════════════════════════════════════════════════════════════════════════════
# CITAS - Sistema de agendamiento (Funcionalidad PRO)
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/citas", response_model=List[CitaResponse])
async def listar_citas(
    fecha_desde: Optional[str] = Query(None),
    fecha_hasta: Optional[str] = Query(None),
    estado: Optional[str] = Query(None),
    servicio: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_tenant_db),
    user_context: dict = Depends(require_auth),
):
    """Listar todas las citas con filtros opcionales."""
    query = select(Cita).where(Cita.organization_id == user_context["org_id"])

    if fecha_desde:
        query = query.where(Cita.fecha_hora >= datetime.fromisoformat(fecha_desde))
    if fecha_hasta:
        query = query.where(Cita.fecha_hora <= datetime.fromisoformat(fecha_hasta))
    if estado:
        query = query.where(Cita.estado == estado)
    if servicio:
        query = query.where(Cita.servicio.ilike(f"%{servicio}%"))

    query = query.order_by(Cita.fecha_hora.asc())
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/citas", response_model=CitaResponse)
async def crear_cita(
    cita: CitaCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user_context: dict = Depends(require_auth),
):
    """Crear una nueva cita (desde el panel admin)."""
    token = secrets.token_urlsafe(32)
    
    db_cita = Cita(
        **cita.model_dump(),
        organization_id=user_context["org_id"],
        token_confirmacion=token,
        origen="manual"
    )
    
    db.add(db_cita)
    await db.commit()
    await db.refresh(db_cita)
    return db_cita


@router.post("/citas/publico", response_model=CitaResponse)
async def crear_cita_publica(
    cita: CitaCreate,
    org_id: int = Query(..., description="ID de organización"),
    request: Request = None,
    db: AsyncSession = Depends(get_tenant_db),
):
    """Crear cita desde widget público (sin autenticación)."""
    # Verificar que el widget esté activo
    query = select(ConfiguracionCitas).where(ConfiguracionCitas.organization_id == org_id)
    result = await db.execute(query)
    config = result.scalar_one_or_none()
    
    if not config or not config.widget_activo:
        raise HTTPException(status_code=403, detail="El widget de citas no está activo")
    
    # Validar anticipación
    ahora = datetime.now()
    dias_diferencia = (cita.fecha_hora.date() - ahora.date()).days
    
    if dias_diferencia < config.dias_anticipacion_min:
        raise HTTPException(
            status_code=400,
            detail=f"La cita debe ser agendada con al menos {config.dias_anticipacion_min} día(s) de anticipación"
        )
    
    if dias_diferencia > config.dias_anticipacion_max:
        raise HTTPException(
            status_code=400,
            detail=f"No se pueden agendar citas con más de {config.dias_anticipacion_max} días de anticipación"
        )
    
    # Verificar disponibilidad
    query_citas_dia = select(func.count(Cita.id)).where(
        and_(
            Cita.organization_id == org_id,
            func.date(Cita.fecha_hora) == cita.fecha_hora.date(),
            Cita.estado != "cancelada"
        )
    )
    result = await db.execute(query_citas_dia)
    citas_del_dia = result.scalar()
    
    if citas_del_dia >= config.citas_por_dia_max:
        raise HTTPException(status_code=400, detail="No hay disponibilidad para este día")
    
    # Crear cita
    token = secrets.token_urlsafe(32)
    
    db_cita = Cita(
        **cita.model_dump(),
        organization_id=org_id,
        token_confirmacion=token,
        origen="widget",
        ip_creacion=request.client.host if request else None,
        user_agent=request.headers.get("user-agent") if request else None
    )
    
    db.add(db_cita)
    await db.commit()
    await db.refresh(db_cita)
    
    # Enviar email de confirmación si el cliente proporciona email
    if db_cita.email_cliente:
        try:
            await email_service.send_cita_confirmacion_email(
                cliente_email=db_cita.email_cliente,
                cliente_nombre=db_cita.nombre_cliente,
                titulo_servicio=db_cita.titulo,
                fecha_cita=db_cita.fecha_hora.strftime("%d/%m/%Y"),
                hora_cita=db_cita.fecha_hora.strftime("%H:%M"),
                notas=db_cita.notas
            )
        except Exception as e:
            # Log error pero no fallar la creación de la cita
            print(f"⚠️ Error enviando email de confirmación: {str(e)}")
    
    return db_cita


@router.get("/citas/{cita_id}", response_model=CitaResponse)
async def obtener_cita(
    cita_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user_context: dict = Depends(require_auth),
):
    """Obtener una cita específica."""
    query = select(Cita).where(
        and_(
            Cita.id == cita_id,
            Cita.organization_id == user_context["org_id"]
        )
    )
    result = await db.execute(query)
    cita = result.scalar_one_or_none()
    
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    
    return cita


@router.put("/citas/{cita_id}", response_model=CitaResponse)
async def actualizar_cita(
    cita_id: int,
    cita_update: CitaUpdate,
    db: AsyncSession = Depends(get_tenant_db),
    user_context: dict = Depends(require_auth),
):
    """Actualizar una cita existente."""
    query = select(Cita).where(
        and_(
            Cita.id == cita_id,
            Cita.organization_id == user_context["org_id"]
        )
    )
    result = await db.execute(query)
    db_cita = result.scalar_one_or_none()
    
    if not db_cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    
    update_data = cita_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_cita, field, value)
    
    db_cita.actualizado_en = datetime.utcnow()
    await db.commit()
    await db.refresh(db_cita)
    return db_cita


@router.delete("/citas/{cita_id}")
async def eliminar_cita(
    cita_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user_context: dict = Depends(require_auth),
):
    """Eliminar/cancelar una cita."""
    query = select(Cita).where(
        and_(
            Cita.id == cita_id,
            Cita.organization_id == user_context["org_id"]
        )
    )
    result = await db.execute(query)
    cita = result.scalar_one_or_none()
    
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    
    cita.estado = "cancelada"
    cita.cancelado_en = datetime.utcnow()
    await db.commit()
    
    return {"detail": "Cita cancelada"}


@router.post("/citas/{cita_id}/confirmar")
async def confirmar_cita(
    cita_id: int,
    token: str = Query(...),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Confirmar una cita usando el token (endpoint público)."""
    query = select(Cita).where(
        and_(
            Cita.id == cita_id,
            Cita.token_confirmacion == token
        )
    )
    result = await db.execute(query)
    cita = result.scalar_one_or_none()
    
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada o token inválido")
    
    cita.confirmado = True
    cita.estado = "confirmada"
    cita.actualizado_en = datetime.utcnow()
    await db.commit()
    
    return {"detail": "Cita confirmada exitosamente"}


# ═══════════════════════════════════════════════════════════════════════════════
# DISPONIBILIDAD
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/disponibilidad", response_model=List[DisponibilidadDia])
async def obtener_disponibilidad(
    fecha_inicio: str = Query(..., description="YYYY-MM-DD"),
    dias: int = Query(7, ge=1, le=30),
    org_id: int = Query(...),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Obtener disponibilidad de slots para el widget público."""
    # Obtener configuración
    query = select(ConfiguracionCitas).where(ConfiguracionCitas.organization_id == org_id)
    result = await db.execute(query)
    config = result.scalar_one_or_none()
    
    if not config or not config.widget_activo:
        raise HTTPException(status_code=403, detail="Widget no disponible")
    
    fecha_actual = datetime.strptime(fecha_inicio, "%Y-%M-%d").date()
    disponibilidad = []
    
    # Parsear días disponibles
    dias_disponibles = [int(d) for d in config.dias_disponibles.split(",")]
    
    for i in range(dias):
        fecha = fecha_actual + timedelta(days=i)
        dia_semana = fecha.isoweekday()  # 1=Lunes, 7=Domingo
        
        if dia_semana not in dias_disponibles:
            continue
        
        # Generar slots del día
        slots = []
        hora_inicio = datetime.strptime(config.horario_inicio, "%H:%M").time()
        hora_fin = datetime.strptime(config.horario_fin, "%H:%M").time()
        
        hora_actual = datetime.combine(fecha, hora_inicio)
        hora_limite = datetime.combine(fecha, hora_fin)
        
        # Obtener citas del día
        query_citas = select(Cita).where(
            and_(
                Cita.organization_id == org_id,
                func.date(Cita.fecha_hora) == fecha,
                Cita.estado != "cancelada"
            )
        )
        result = await db.execute(query_citas)
        citas_del_dia = result.scalars().all()
        
        while hora_actual < hora_limite:
            # Verificar si el slot está ocupado
            ocupado = any(
                c.fecha_hora.hour == hora_actual.hour and
                c.fecha_hora.minute == hora_actual.minute
                for c in citas_del_dia
            )
            
            slots.append(DisponibilidadSlot(
                fecha=fecha.isoformat(),
                hora=hora_actual.strftime("%H:%M"),
                disponible=not ocupado,
                citas_ocupadas=1 if ocupado else 0
            ))
            
            hora_actual += timedelta(minutes=config.duracion_slot_minutos + config.buffer_minutos)
        
        disponibilidad.append(DisponibilidadDia(
            fecha=fecha.isoformat(),
            dia_semana=dia_semana,
            slots=slots,
            total_slots=len(slots),
            slots_disponibles=sum(1 for s in slots if s.disponible)
        ))
    
    return disponibilidad


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE CITAS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/configuracion-citas", response_model=ConfiguracionCitasResponse)
async def obtener_configuracion_citas(
    db: AsyncSession = Depends(get_tenant_db),
    user_context: dict = Depends(require_auth),
):
    """Obtener configuración de citas de la organización."""
    query = select(ConfiguracionCitas).where(
        ConfiguracionCitas.organization_id == user_context["org_id"]
    )
    result = await db.execute(query)
    config = result.scalar_one_or_none()
    
    if not config:
        # Crear configuración por defecto
        config = ConfiguracionCitas(organization_id=user_context["org_id"])
        db.add(config)
        await db.commit()
        await db.refresh(config)
    
    return config


@router.put("/configuracion-citas", response_model=ConfiguracionCitasResponse)
async def actualizar_configuracion_citas(
    config_update: ConfiguracionCitasUpdate,
    db: AsyncSession = Depends(get_tenant_db),
    user_context: dict = Depends(require_auth),
):
    """Actualizar configuración de citas."""
    query = select(ConfiguracionCitas).where(
        ConfiguracionCitas.organization_id == user_context["org_id"]
    )
    result = await db.execute(query)
    config = result.scalar_one_or_none()
    
    if not config:
        # Crear si no existe
        config = ConfiguracionCitas(
            organization_id=user_context["org_id"],
            **config_update.model_dump(exclude_unset=True)
        )
        db.add(config)
    else:
        # Actualizar
        update_data = config_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(config, field, value)
        config.actualizado_en = datetime.utcnow()
    
    await db.commit()
    await db.refresh(config)
    return config


@router.get("/configuracion-citas/publico", response_model=ConfiguracionCitasResponse)
async def obtener_configuracion_publica(
    org_id: int = Query(...),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Obtener configuración pública del widget (sin autenticación)."""
    query = select(ConfiguracionCitas).where(
        and_(
            ConfiguracionCitas.organization_id == org_id,
            ConfiguracionCitas.widget_activo == True
        )
    )
    result = await db.execute(query)
    config = result.scalar_one_or_none()
    
    if not config:
        raise HTTPException(status_code=404, detail="Widget no disponible")
    
    return config


# Ruta para servir el widget HTML
@router.get("/widget", response_class=HTMLResponse, include_in_schema=False)
async def widget_html(request: Request):
    """Servir el widget público de citas."""
    return templates.TemplateResponse("widget_citas.html", {"request": request})

    
    return config
