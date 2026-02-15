"""Routes for production orders management."""

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func, text
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from pydantic import BaseModel
from dario_app.database import get_db
from dario_app.core.auth import get_org_id as auth_get_org_id
from .models import (
    OrdenProduccion, OperacionProduccion, MovimientoAlmacen,
    EstadoOrdenProduccion, TipoPrioridad, SeccionProduccion, TipoSeccion
)
from .models import RegistroTrabajo, IncidenciaProduccion, SolicitudMaterialProduccion
from .schemas import (
    OrdenProduccionCreate, OrdenProduccionUpdate, OrdenProduccionResponse,
    OrdenProduccionDetailResponse, OrdenProduccionListResponse,
    OperacionProduccionCreate, OperacionProduccionUpdate, OperacionProduccionResponse,
    MovimientoAlmacenCreate, MovimientoAlmacenUpdate, MovimientoAlmacenResponse,
    OrdenProduccionStateChange,
    SeccionProduccionCreate, SeccionProduccionUpdate, SeccionProduccionResponse,
    AsignarSeccionRequest, AceptarOrdenRequest,
    BulkPrioridadRequest
)
from dario_app.modules.oficina_tecnica.models import BOMHeader, BOMOperacion, BOMLine
from dario_app.modules.ventas.models import Venta
from dario_app.modules.inventario.models import Producto
from dario_app.modules.usuarios.models import Role, UserRole, Usuario
from dario_app.modules.tenants.models import Organization

router = APIRouter(prefix="/api/produccion-ordenes", tags=["Producción Ordenes"])
templates = Jinja2Templates(directory="/home/dario/src/dario_app/templates")


def get_org_id(org_id: int = Depends(auth_get_org_id)) -> int:
    """Get organization ID from authenticated context."""
    return org_id


async def get_tenant_db_local(org_id: int = Depends(get_org_id)):
    """Session en la base del tenant actual."""
    async for session in get_db(org_id):
        yield session


async def _ubicacion_almacen_canonica(
    db: AsyncSession,
    org_id: int,
    ubicacion_producto: str | None,
) -> str:
    """Resolve a product's location text into a canonical almacen_ubicaciones.codigo.

    Strategy:
    1) If the given text matches an existing almacen_ubicaciones.codigo for the org, use it.
    2) Try to parse simple patterns like 'A1-P3' -> pasillo=1, estanteria='A', altura=3, parcela='C' (centro).
    3) Fallback to a safe default first location (lowest codigo) in almacen_ubicaciones for the org.
    """
    # Helper to check existence
    async def existe_codigo(cod: str) -> bool:
        res = await db.execute(
            text(
                "SELECT 1 FROM almacen_ubicaciones WHERE organization_id=:org AND codigo=:cod LIMIT 1"
            ),
            {"org": org_id, "cod": cod},
        )
        return res.first() is not None

    # 1) Exact match
    if ubicacion_producto:
        up = ubicacion_producto.strip()
        if await existe_codigo(up):
            return up

        # 2) Try to parse patterns like 'A1-P3'
        #   A1-P3  => pasillo 1, estanteria A, altura 3, parcela C (centro)
        #   A1-P3-IZQ => pasillo 1, estanteria A, altura 3, parcela I
        import re

        m = re.match(r"^([A-Za-z])(\d+)[-_/]P(\d+)(?:[-_/](CEN|DER|IZQ|C|D|I))?$", up, re.IGNORECASE)
        if m:
            est, pasillo, altura, parcela = m.group(1), m.group(2), m.group(3), m.group(4)
            est = est.upper()
            # Map parcela tokens
            mapa_parcela = {"CEN": "C", "DER": "D", "IZQ": "I", "C": "C", "D": "D", "I": "I"}
            letra_parcela = mapa_parcela.get((parcela or "CEN").upper(), "C")
            codigo_candidato = f"{int(pasillo)}/{est}/{int(altura)}/{letra_parcela}"
            if await existe_codigo(codigo_candidato):
                return codigo_candidato

        # Pattern like 'A0-MISC' -> fallback (no direct mapping)

    # 3) Fallback to first available location
    first = await db.execute(
        text(
            "SELECT codigo FROM almacen_ubicaciones WHERE organization_id=:org AND activo=1 ORDER BY codigo LIMIT 1"
        ),
        {"org": org_id},
    )
    row = first.first()
    return row[0] if row else "1/A/1/C"


async def _ubicacion_playa_salida_almacen(
    db: AsyncSession,
    org_id: int,
) -> str:
    """Find outbound staging area specifically for ALMACÉN (not fábrica/expedición).

    Heuristics (case-insensitive):
    - Prefer rows whose codigo/notas contain ('salida' OR 'playa') AND ('alm' OR 'almacen').
    - Exclude rows mentioning ('fab', 'fabrica', 'expedicion', 'shipping', 'envio').
    - Fallback to any 'salida'/'playa' that does NOT mention excluded terms.
    - Ultimately fallback to the first active location.
    """
    q1 = await db.execute(
        text(
            """
            SELECT codigo FROM almacen_ubicaciones
            WHERE organization_id=:org AND activo=1
            AND (
              (lower(codigo) LIKE '%salida%' OR lower(codigo) LIKE '%playa%' OR lower(coalesce(notas,'')) LIKE '%salida%' OR lower(coalesce(notas,'')) LIKE '%playa%')
            )
            AND (
              (lower(codigo) LIKE '%alm%' OR lower(codigo) LIKE '%almacen%' OR lower(coalesce(notas,'')) LIKE '%alm%' OR lower(coalesce(notas,'')) LIKE '%almacen%')
            )
            AND (
              lower(codigo) NOT LIKE '%fab%' AND lower(codigo) NOT LIKE '%fabrica%' AND lower(codigo) NOT LIKE '%expedicion%'
              AND lower(codigo) NOT LIKE '%shipping%' AND lower(codigo) NOT LIKE '%envio%'
              AND lower(coalesce(notas,'')) NOT LIKE '%fab%' AND lower(coalesce(notas,'')) NOT LIKE '%fabrica%'
              AND lower(coalesce(notas,'')) NOT LIKE '%expedicion%' AND lower(coalesce(notas,'')) NOT LIKE '%shipping%'
              AND lower(coalesce(notas,'')) NOT LIKE '%envio%'
            )
            ORDER BY codigo LIMIT 1
            """
        ),
        {"org": org_id},
    )
    r1 = q1.first()
    if r1:
        return r1[0]

    # Fallback: salida/playa sin términos excluidos
    q2 = await db.execute(
        text(
            """
            SELECT codigo FROM almacen_ubicaciones
            WHERE organization_id=:org AND activo=1
            AND (
              (lower(codigo) LIKE '%salida%' OR lower(codigo) LIKE '%playa%' OR lower(coalesce(notas,'')) LIKE '%salida%' OR lower(coalesce(notas,'')) LIKE '%playa%')
            )
            AND (
              lower(codigo) NOT LIKE '%fab%' AND lower(codigo) NOT LIKE '%fabrica%' AND lower(codigo) NOT LIKE '%expedicion%'
              AND lower(codigo) NOT LIKE '%shipping%' AND lower(codigo) NOT LIKE '%envio%'
              AND lower(coalesce(notas,'')) NOT LIKE '%fab%' AND lower(coalesce(notas,'')) NOT LIKE '%fabrica%'
              AND lower(coalesce(notas,'')) NOT LIKE '%expedicion%' AND lower(coalesce(notas,'')) NOT LIKE '%shipping%'
              AND lower(coalesce(notas,'')) NOT LIKE '%envio%'
            )
            ORDER BY codigo LIMIT 1
            """
        ),
        {"org": org_id},
    )
    r2 = q2.first()
    if r2:
        return r2[0]

    # Fallback to first active
    first = await db.execute(
        text(
            "SELECT codigo FROM almacen_ubicaciones WHERE organization_id=:org AND activo=1 ORDER BY codigo LIMIT 1"
        ),
        {"org": org_id},
    )
    row = first.first()
    return row[0] if row else "1/A/1/C"


async def seleccionar_carretillero(db: AsyncSession, org_id: int) -> Optional[int]:
    """Select a carretillero (forklift operator) for the org. Picks the one with fewer assigned movements."""
    role_ids = (await db.execute(
        select(Role.id).where(
            (Role.organization_id == org_id) &
            (Role.nombre.ilike("%carretillero%"))
        )
    )).scalars().all()
    if not role_ids:
        return None

    user_ids = (await db.execute(
        select(UserRole.usuario_id).where(UserRole.role_id.in_(role_ids))
    )).scalars().all()
    if not user_ids:
        return None

    counts = (await db.execute(
        select(MovimientoAlmacen.usuario_asignado_id, func.count().label("cnt"))
        .where(MovimientoAlmacen.usuario_asignado_id.in_(user_ids))
        .group_by(MovimientoAlmacen.usuario_asignado_id)
    )).all()
    count_map = {row[0]: row[1] for row in counts}
    return sorted(user_ids, key=lambda uid: count_map.get(uid, 0))[0]


async def generar_codigo_seccion(
    db: AsyncSession,
    org_id: int,
    tipo: TipoSeccion,
) -> str:
    """Build sequential code for production sections."""
    prefix_map = {
        TipoSeccion.CORTE: "CORTE",
        TipoSeccion.ENSAMBLAJE: "ENSAM",
        TipoSeccion.SOLDADURA: "SOLD",
        TipoSeccion.PINTURA: "PINTU",
        TipoSeccion.ACABADO: "ACABA",
        TipoSeccion.CONTROL_CALIDAD: "CALID",
        TipoSeccion.EMPAQUE: "EMPAQ",
        TipoSeccion.OTRO: "OTRO",
    }

    prefix = prefix_map.get(tipo, "OTRO")
    last_code = (await db.execute(
        select(SeccionProduccion.codigo).where(
            (SeccionProduccion.organization_id == org_id) &
            (SeccionProduccion.codigo.like(f"SEC-{prefix}-%"))
        ).order_by(desc(SeccionProduccion.codigo))
    )).scalar_one_or_none()

    next_seq = 1
    if last_code:
        try:
            next_seq = int(last_code.split("-")[-1]) + 1
        except ValueError:
            next_seq = 1

    return f"SEC-{prefix}-{next_seq:02d}"


# ============ PAYLOADS RÁPIDOS PARA SUPERVISORES ============

class RegistroInicioPayload(BaseModel):
    trabajador_nombre: str
    hora_inicio: str
    fecha: str


class IncidenciaPayload(BaseModel):
    tipo_incidencia: str
    descripcion: str
    fecha_reporte: str


class SolicitudMaterialPayload(BaseModel):
    producto_descripcion: str
    cantidad: float
    urgencia: str
    motivo: str
    fecha_solicitud: str


# ============ PAYLOADS RÁPIDOS PARA SUPERVISORES ============

class RegistroInicioPayload(BaseModel):
    trabajador_nombre: str
    hora_inicio: str
    fecha: str


class IncidenciaPayload(BaseModel):
    tipo_incidencia: str
    descripcion: str
    fecha_reporte: str


class SolicitudMaterialPayload(BaseModel):
    producto_descripcion: str
    cantidad: float
    urgencia: str
    motivo: str
    fecha_solicitud: str


# ============ SECCIÓN PRODUCCIÓN ENDPOINTS ============

@router.get("/secciones", response_model=List[SeccionProduccionResponse])
async def list_secciones_produccion(
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
    activas_solo: bool = Query(False),
):
    """List production sections."""
    query = select(SeccionProduccion).where(
        SeccionProduccion.organization_id == org_id
    ).order_by(SeccionProduccion.codigo)
    
    if activas_solo:
        query = query.where(SeccionProduccion.activa == True)
    
    secciones = (await db.execute(query)).scalars().all()
    
    # Add count of active orders
    for seccion in secciones:
        count_result = await db.execute(
            select(OrdenProduccion).where(
                (OrdenProduccion.seccion_produccion_id == seccion.id) &
                (OrdenProduccion.estado.in_([
                    EstadoOrdenProduccion.ASIGNADA,
                    EstadoOrdenProduccion.ACEPTADA,
                    EstadoOrdenProduccion.ADQUISICION_MATERIALES,
                    EstadoOrdenProduccion.EN_PROCESO
                ]))
            )
        )
        seccion.ordenes_activas = len(count_result.scalars().all())
    
    return secciones


@router.get("/supervisores", response_model=List[dict])
async def list_supervisores(
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """List available supervisors from HR module."""
    from dario_app.modules.usuarios.models import Usuario
    
    usuarios = (await db.execute(
        select(Usuario.id, Usuario.username, Usuario.email).where(
            Usuario.organization_id == org_id
        ).order_by(Usuario.username)
    )).all()
    
    return [{
        "id": u.id,
        "username": u.username,
        "email": u.email
    } for u in usuarios]


@router.post("/secciones", response_model=SeccionProduccionResponse)
async def create_seccion_produccion(
    payload: SeccionProduccionCreate,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Create a new production section."""
    codigo = await generar_codigo_seccion(db, org_id, payload.tipo or TipoSeccion.OTRO)

    seccion = SeccionProduccion(
        organization_id=org_id,
        codigo=codigo,
        **payload.dict(exclude={"codigo"})
    )
    
    db.add(seccion)
    await db.commit()
    await db.refresh(seccion)
    seccion.ordenes_activas = 0
    
    return seccion


# ============ ACCIONES RÁPIDAS SOBRE ÓRDENES (UI SUPERVISOR) ============

@router.post("/{orden_id}/registrar-inicio")
async def registrar_inicio_trabajo(
    orden_id: int,
    payload: RegistroInicioPayload,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Registrar inicio de trabajo y persistir en BD."""

    orden = (await db.execute(
        select(OrdenProduccion.id).where(
            (OrdenProduccion.id == orden_id) & (OrdenProduccion.organization_id == org_id)
        )
    )).scalar_one_or_none()

    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada")

    # Persist simple work log
    try:
        fecha_payload = datetime.fromisoformat(payload.fecha)
    except Exception:
        fecha_payload = datetime.utcnow()

    registro = RegistroTrabajo(
        organization_id=org_id,
        orden_produccion_id=orden_id,
        trabajador_nombre=payload.trabajador_nombre,
        hora_inicio=payload.hora_inicio,
        fecha=fecha_payload,
    )
    db.add(registro)
    await db.commit()
    await db.refresh(registro)

    return {
        "success": True,
        "orden_id": orden_id,
        "registro_trabajo_id": registro.id,
        "trabajador": registro.trabajador_nombre,
        "hora_inicio": registro.hora_inicio,
        "fecha": registro.fecha.isoformat(),
        "mensaje": "Inicio de trabajo registrado"
    }


@router.post("/{orden_id}/reportar-incidencia")
async def reportar_incidencia(
    orden_id: int,
    payload: IncidenciaPayload,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Registrar una incidencia básica sobre la orden y persistir en BD."""

    orden = (await db.execute(
        select(OrdenProduccion.id).where(
            (OrdenProduccion.id == orden_id) & (OrdenProduccion.organization_id == org_id)
        )
    )).scalar_one_or_none()

    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada")

    # Persist incident
    try:
        fecha_rep = datetime.fromisoformat(payload.fecha_reporte)
    except Exception:
        fecha_rep = datetime.utcnow()

    inc = IncidenciaProduccion(
        organization_id=org_id,
        orden_produccion_id=orden_id,
        tipo_incidencia=payload.tipo_incidencia,
        descripcion=payload.descripcion,
        fecha_reporte=fecha_rep,
        estado="reportada",
    )
    db.add(inc)
    await db.commit()
    await db.refresh(inc)

    return {
        "success": True,
        "orden_id": orden_id,
        "incidencia_id": inc.id,
        "tipo": inc.tipo_incidencia,
        "descripcion": inc.descripcion,
        "fecha_reporte": inc.fecha_reporte.isoformat(),
        "mensaje": "Incidencia registrada"
    }


@router.post("/{orden_id}/solicitar-material")
async def solicitar_material(
    orden_id: int,
    payload: SolicitudMaterialPayload,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Crear y persistir una solicitud rápida de material."""

    orden = (await db.execute(
        select(OrdenProduccion.id).where(
            (OrdenProduccion.id == orden_id) & (OrdenProduccion.organization_id == org_id)
        )
    )).scalar_one_or_none()

    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada")

    # Persist request
    try:
        fecha_sol = datetime.fromisoformat(payload.fecha_solicitud)
    except Exception:
        fecha_sol = datetime.utcnow()

    solicitud = SolicitudMaterialProduccion(
        organization_id=org_id,
        orden_produccion_id=orden_id,
        producto_descripcion=payload.producto_descripcion,
        cantidad=payload.cantidad,
        urgencia=payload.urgencia,
        motivo=payload.motivo,
        fecha_solicitud=fecha_sol,
        estado="pendiente",
    )
    db.add(solicitud)
    await db.commit()
    await db.refresh(solicitud)

    return {
        "success": True,
        "orden_id": orden_id,
        "solicitud_material_id": solicitud.id,
        "producto_descripcion": solicitud.producto_descripcion,
        "cantidad": solicitud.cantidad,
        "urgencia": solicitud.urgencia,
        "motivo": solicitud.motivo,
        "fecha_solicitud": solicitud.fecha_solicitud.isoformat(),
        "estado": solicitud.estado,
        "mensaje": "Solicitud de material creada"
    }


# (duplicated stub endpoints removed; persisted versions above are authoritative)


@router.get("/secciones/{seccion_id}", response_model=SeccionProduccionResponse)
async def get_seccion_produccion(
    seccion_id: int,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Get production section details."""
    seccion = (await db.execute(
        select(SeccionProduccion).where(
            (SeccionProduccion.id == seccion_id) &
            (SeccionProduccion.organization_id == org_id)
        )
    )).scalar_one_or_none()
    
    if not seccion:
        raise HTTPException(status_code=404, detail="Sección no encontrada")
    
    # Count active orders
    count_result = await db.execute(
        select(OrdenProduccion).where(
            (OrdenProduccion.seccion_produccion_id == seccion.id) &
            (OrdenProduccion.estado.in_([
                EstadoOrdenProduccion.ASIGNADA,
                EstadoOrdenProduccion.ACEPTADA,
                EstadoOrdenProduccion.ADQUISICION_MATERIALES,
                EstadoOrdenProduccion.EN_PROCESO
            ]))
        )
    )
    seccion.ordenes_activas = len(count_result.scalars().all())
    
    return seccion


@router.put("/secciones/{seccion_id}", response_model=SeccionProduccionResponse)
async def update_seccion_produccion(
    seccion_id: int,
    payload: SeccionProduccionUpdate,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Update production section."""
    seccion = (await db.execute(
        select(SeccionProduccion).where(
            (SeccionProduccion.id == seccion_id) &
            (SeccionProduccion.organization_id == org_id)
        )
    )).scalar_one_or_none()
    
    if not seccion:
        raise HTTPException(status_code=404, detail="Sección no encontrada")
    
    update_data = payload.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(seccion, field, value)
    
    await db.commit()
    await db.refresh(seccion)
    seccion.ordenes_activas = 0
    
    return seccion


@router.delete("/secciones/{seccion_id}")
async def delete_seccion_produccion(
    seccion_id: int,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Delete production section."""
    seccion = (await db.execute(
        select(SeccionProduccion).where(
            (SeccionProduccion.id == seccion_id) &
            (SeccionProduccion.organization_id == org_id)
        )
    )).scalar_one_or_none()
    
    if not seccion:
        raise HTTPException(status_code=404, detail="Sección no encontrada")
    
    # Check if has active orders
    has_orders = (await db.execute(
        select(OrdenProduccion).where(
            (OrdenProduccion.seccion_produccion_id == seccion.id) &
            (OrdenProduccion.estado.in_([
                EstadoOrdenProduccion.ASIGNADA,
                EstadoOrdenProduccion.ACEPTADA,
                EstadoOrdenProduccion.ADQUISICION_MATERIALES,
                EstadoOrdenProduccion.EN_PROCESO
            ]))
        )
    )).scalar_one_or_none()
    
    if has_orders:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar sección con órdenes activas. Desactívala en su lugar."
        )
    
    await db.delete(seccion)
    await db.commit()
    
    return {"message": "Sección eliminada"}


# ============ WORKFLOW ENDPOINTS ============

@router.post("/{orden_id}/asignar-seccion", response_model=OrdenProduccionResponse)
async def asignar_seccion(
    orden_id: int,
    payload: AsignarSeccionRequest,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Assign production order to a section."""
    orden = (await db.execute(
        select(OrdenProduccion)
        .options(
            selectinload(OrdenProduccion.venta),
            selectinload(OrdenProduccion.operaciones)
        )
        .where(
            (OrdenProduccion.id == orden_id) &
            (OrdenProduccion.organization_id == org_id)
        )
    )).scalar_one_or_none()
    
    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    # Validate section exists
    seccion = (await db.execute(
        select(SeccionProduccion).where(
            (SeccionProduccion.id == payload.seccion_produccion_id) &
            (SeccionProduccion.organization_id == org_id) &
            (SeccionProduccion.activa == True)
        )
    )).scalar_one_or_none()
    
    if not seccion:
        raise HTTPException(status_code=404, detail="Sección no encontrada o inactiva")
    
    # Update order
    now = datetime.utcnow()
    orden.seccion_produccion_id = payload.seccion_produccion_id
    orden.asignado_a = payload.asignado_a or seccion.supervisor_nombre
    orden.estado = EstadoOrdenProduccion.ADQUISICION_MATERIALES  # Automáticamente pasa a reunir materiales
    orden.fecha_asignacion = now
    
    if payload.notas:
        orden.notas_internas = (orden.notas_internas or "") + f"\n[Asignación] {payload.notas}"
    
    # Generate picking movements if none exist yet
    existing_movs = (await db.execute(
        select(MovimientoAlmacen.id).where(
            (MovimientoAlmacen.orden_produccion_id == orden.id) &
            (MovimientoAlmacen.organization_id == org_id)
        )
    )).scalars().first()

    if not existing_movs:
        bom_lines = (await db.execute(
            select(BOMLine, Producto).join(Producto, BOMLine.componente_id == Producto.id).where(
                (BOMLine.bom_header_id == orden.bom_id) & (BOMLine.organization_id == org_id)
            )
        )).all()

        playa_salida = await _ubicacion_playa_salida_almacen(db, org_id)

        for bom_line, componente in bom_lines:
            cantidad_base = bom_line.cantidad * orden.cantidad_ordenada
            desperdicio = bom_line.factor_desperdicio or 0
            cantidad_total = cantidad_base * (1 + desperdicio)
            ubic_origen = await _ubicacion_almacen_canonica(db, org_id, getattr(componente, 'ubicacion_almacen', None))
            
            # FASE 1: almacén -> playa de salida (ÚNICA FASE INICIAL)
            # El carretillero lleva TODO a la playa primero
            m1 = MovimientoAlmacen(
                organization_id=org_id,
                orden_produccion_id=orden.id,
                producto_id=componente.id,
                tipo_movimiento="salida_almacen",
                cantidad=cantidad_total,
                ubicacion_origen=ubic_origen,
                ubicacion_destino=playa_salida,
                estado="asignado" if orden.carretillero_id else "pendiente",
                usuario_asignado_id=orden.carretillero_id,
                fecha_asignacion=datetime.utcnow() if orden.carretillero_id else None,
            )
            db.add(m1)

    await db.commit()
    await db.refresh(orden, ["venta", "operaciones"])
    
    return orden


# Printable: Orden de Producción
@router.get("/ordenes/{orden_id}/print")
async def print_orden_produccion(
    orden_id: int,
    request: Request,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Renderiza un HTML imprimible para una orden de producción."""
    query = select(OrdenProduccion).where(
        (OrdenProduccion.id == orden_id) &
        (OrdenProduccion.organization_id == org_id)
    ).options(
        selectinload(OrdenProduccion.operaciones),
        selectinload(OrdenProduccion.movimientos_material),
        selectinload(OrdenProduccion.producto),
        selectinload(OrdenProduccion.venta),
        selectinload(OrdenProduccion.seccion_produccion),
    )
    orden = (await db.execute(query)).scalar_one_or_none()
    if not orden:
        raise HTTPException(status_code=404, detail="Orden de producción no encontrada")

    # Organización (branding)
    org = None
    try:
        org_res = await db.execute(select(Organization).where(Organization.id == org_id))
        org = org_res.scalar_one_or_none()
    except Exception:
        org = None

    context = {
        "request": request,
        "orden": orden,
        "producto": getattr(orden, "producto", None),
        "venta": getattr(orden, "venta", None),
        "seccion": getattr(orden, "seccion_produccion", None),
        "operaciones": getattr(orden, "operaciones", []),
        "movimientos": getattr(orden, "movimientos_material", []),
        "org": org,
    }
    return templates.TemplateResponse("print/orden_produccion.html", context)


# Printable: Movimiento de Almacén (Carretillero)
@router.get("/movimientos/{movimiento_id}/print")
async def print_movimiento_almacen(
    movimiento_id: int,
    request: Request,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Renderiza un HTML imprimible para un movimiento de almacén (carretillero)."""
    movimiento = (await db.execute(
        select(MovimientoAlmacen)
        .options(
            selectinload(MovimientoAlmacen.producto),
            selectinload(MovimientoAlmacen.usuario_asignado),
            selectinload(MovimientoAlmacen.orden_produccion).selectinload(OrdenProduccion.seccion_produccion),
            selectinload(MovimientoAlmacen.orden_produccion).selectinload(OrdenProduccion.venta),
        )
        .where(
            (MovimientoAlmacen.id == movimiento_id) &
            (MovimientoAlmacen.organization_id == org_id)
        )
    )).scalar_one_or_none()

    if not movimiento:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")

    # Organización
    org = None
    try:
        org_res = await db.execute(select(Organization).where(Organization.id == org_id))
        org = org_res.scalar_one_or_none()
    except Exception:
        org = None

    context = {
        "request": request,
        "mov": movimiento,
        "orden": getattr(movimiento, "orden_produccion", None),
        "producto": getattr(movimiento, "producto", None),
        "carretillero": getattr(movimiento, "usuario_asignado", None),
        "seccion": getattr(getattr(movimiento, "orden_produccion", None), "seccion_produccion", None),
        "venta": getattr(getattr(movimiento, "orden_produccion", None), "venta", None),
        "org": org,
    }
    return templates.TemplateResponse("print/movimiento.html", context)


# Printable: Reporte de Producción (Orden)
@router.get("/ordenes/{orden_id}/print-reporte")
async def print_reporte_produccion(
    orden_id: int,
    request: Request,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Renderiza un HTML imprimible con el informe de producción: operaciones, registros, incidencias y solicitudes."""
    query = select(OrdenProduccion).where(
        (OrdenProduccion.id == orden_id) &
        (OrdenProduccion.organization_id == org_id)
    ).options(
        selectinload(OrdenProduccion.operaciones),
        selectinload(OrdenProduccion.producto),
        selectinload(OrdenProduccion.venta),
        selectinload(OrdenProduccion.seccion_produccion),
    )
    orden = (await db.execute(query)).scalar_one_or_none()
    if not orden:
        raise HTTPException(status_code=404, detail="Orden de producción no encontrada")

    # Organización
    org = None
    try:
        org_res = await db.execute(select(Organization).where(Organization.id == org_id))
        org = org_res.scalar_one_or_none()
    except Exception:
        org = None

    # Registros, incidencias y solicitudes
    registros = (await db.execute(
        select(RegistroTrabajo).where(
            (RegistroTrabajo.orden_produccion_id == orden_id) &
            (RegistroTrabajo.organization_id == org_id)
        ).order_by(RegistroTrabajo.fecha)
    )).scalars().all()

    incidencias = (await db.execute(
        select(IncidenciaProduccion).where(
            (IncidenciaProduccion.orden_produccion_id == orden_id) &
            (IncidenciaProduccion.organization_id == org_id)
        ).order_by(IncidenciaProduccion.fecha_reporte)
    )).scalars().all()

    solicitudes = (await db.execute(
        select(SolicitudMaterialProduccion).where(
            (SolicitudMaterialProduccion.orden_produccion_id == orden_id) &
            (SolicitudMaterialProduccion.organization_id == org_id)
        ).order_by(SolicitudMaterialProduccion.fecha_solicitud)
    )).scalars().all()

    context = {
        "request": request,
        "orden": orden,
        "producto": getattr(orden, "producto", None),
        "venta": getattr(orden, "venta", None),
        "seccion": getattr(orden, "seccion_produccion", None),
        "operaciones": getattr(orden, "operaciones", []),
        "registros": registros,
        "incidencias": incidencias,
        "solicitudes": solicitudes,
        "org": org,
    }
    return templates.TemplateResponse("print/reporte_produccion.html", context)


# Printable: Packing List (Orden)
@router.get("/ordenes/{orden_id}/packing/print")
async def print_packing_list(
    orden_id: int,
    request: Request,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Renderiza un HTML imprimible para la lista de embalaje de la orden."""
    query = select(OrdenProduccion).where(
        (OrdenProduccion.id == orden_id) &
        (OrdenProduccion.organization_id == org_id)
    ).options(
        selectinload(OrdenProduccion.producto),
        selectinload(OrdenProduccion.venta),
        selectinload(OrdenProduccion.movimientos_material),
        selectinload(OrdenProduccion.seccion_produccion),
    )
    orden = (await db.execute(query)).scalar_one_or_none()
    if not orden:
        raise HTTPException(status_code=404, detail="Orden de producción no encontrada")

    org = None
    try:
        org_res = await db.execute(select(Organization).where(Organization.id == org_id))
        org = org_res.scalar_one_or_none()
    except Exception:
        org = None

    context = {
        "request": request,
        "orden": orden,
        "producto": getattr(orden, "producto", None),
        "venta": getattr(orden, "venta", None),
        "seccion": getattr(orden, "seccion_produccion", None),
        "movimientos": getattr(orden, "movimientos_material", []),
        "org": org,
    }
    return templates.TemplateResponse("print/packing_list.html", context)


@router.post("/{orden_id}/aceptar-supervisor", response_model=OrdenProduccionResponse)
async def aceptar_orden_supervisor(
    orden_id: int,
    payload: AceptarOrdenRequest,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Supervisor accepts the order and moves to material acquisition."""
    orden = (await db.execute(
        select(OrdenProduccion).where(
            (OrdenProduccion.id == orden_id) &
            (OrdenProduccion.organization_id == org_id)
        )
    )).scalar_one_or_none()
    
    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    if orden.estado != EstadoOrdenProduccion.ASIGNADA:
        raise HTTPException(
            status_code=400,
            detail=f"Orden debe estar en estado 'asignada'. Estado actual: {orden.estado}"
        )
    
    # Accept and move to material acquisition
    orden.estado = EstadoOrdenProduccion.ACEPTADA
    orden.fecha_aceptacion = datetime.utcnow()
    
    if payload.notas:
        orden.notas_internas = (orden.notas_internas or "") + f"\n[Aceptación] {payload.notas}"
    
    await db.commit()
    await db.refresh(orden)
    
    return orden


@router.post("/{orden_id}/iniciar-adquisicion", response_model=OrdenProduccionResponse)
async def iniciar_adquisicion_materiales(
    orden_id: int,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Start material acquisition phase."""
    orden = (await db.execute(
        select(OrdenProduccion).where(
            (OrdenProduccion.id == orden_id) &
            (OrdenProduccion.organization_id == org_id)
        )
    )).scalar_one_or_none()
    
    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    if orden.estado != EstadoOrdenProduccion.ACEPTADA:
        raise HTTPException(
            status_code=400,
            detail=f"Orden debe estar aceptada. Estado actual: {orden.estado}"
        )

    # Require seccion to route materials to its picking zone
    if not orden.seccion_produccion_id:
        raise HTTPException(status_code=400, detail="La orden no tiene sección asignada")

    seccion = (await db.execute(
        select(SeccionProduccion).where(
            (SeccionProduccion.id == orden.seccion_produccion_id) &
            (SeccionProduccion.organization_id == org_id)
        )
    )).scalar_one_or_none()

    if not seccion:
        raise HTTPException(status_code=404, detail="Sección no encontrada")

    # Generate picking movements for each BOM component - SOLO FASE 1
    bom_lines = (await db.execute(
        select(BOMLine, Producto).join(Producto, BOMLine.componente_id == Producto.id).where(
            (BOMLine.bom_header_id == orden.bom_id) & (BOMLine.organization_id == org_id)
        )
    )).all()

    playa_salida = await _ubicacion_playa_salida_almacen(db, org_id)
    
    for bom_line, componente in bom_lines:
        cantidad_base = bom_line.cantidad * orden.cantidad_ordenada
        desperdicio = bom_line.factor_desperdicio or 0
        cantidad_total = cantidad_base * (1 + desperdicio)
        ubic_origen = await _ubicacion_almacen_canonica(db, org_id, getattr(componente, 'ubicacion_almacen', None))
        
        # FASE 1 SOLO: almacén -> playa
        # Fase 2 (playa -> picking) se crea automáticamente cuando se completa Fase 1
        m1 = MovimientoAlmacen(
            organization_id=org_id,
            orden_produccion_id=orden.id,
            producto_id=componente.id,
            tipo_movimiento="salida_almacen",
            cantidad=cantidad_total,
            ubicacion_origen=ubic_origen,
            ubicacion_destino=playa_salida,
            estado="asignado" if orden.carretillero_id else "pendiente",
            usuario_asignado_id=orden.carretillero_id,
            fecha_asignacion=datetime.utcnow() if orden.carretillero_id else None,
        )
        db.add(m1)
    
    orden.estado = EstadoOrdenProduccion.ADQUISICION_MATERIALES

    await db.commit()
    await db.refresh(orden)
    
    return orden

# ============ ORDEN PRODUCCIÓN ENDPOINTS ============

@router.get("/", response_model=List[dict])
async def list_ordenes_produccion(
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
    estado: str = Query(None),
    producto_id: int = Query(None),
    prioridad: str = Query(None),
    solo_con_seccion: bool = Query(False, description="Si es true, solo devuelve órdenes con sección asignada"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
):
    """List production orders with filters."""
    query = select(OrdenProduccion).where(
        OrdenProduccion.organization_id == org_id
    ).order_by(desc(OrdenProduccion.fecha_creacion))
    
    if estado:
        query = query.where(OrdenProduccion.estado == estado)
    if producto_id:
        query = query.where(OrdenProduccion.producto_id == producto_id)
    if prioridad:
        query = query.where(OrdenProduccion.prioridad == prioridad)
    if solo_con_seccion:
        query = query.where(OrdenProduccion.seccion_produccion_id.isnot(None))
    
    ordenes = (await db.execute(
        query.options(
            selectinload(OrdenProduccion.producto),
            selectinload(OrdenProduccion.venta),
            selectinload(OrdenProduccion.seccion_produccion),
            selectinload(OrdenProduccion.carretillero)
        ).offset(skip).limit(limit)
    )).scalars().all()
    
    # Return simple data without validation
    resultado = []
    for orden in ordenes:
        # Related data helpers
        producto = getattr(orden, "producto", None)
        venta = getattr(orden, "venta", None)
        seccion = getattr(orden, "seccion_produccion", None)
        usuario = getattr(orden, "carretillero", None)

        orden_dict = {
            'id': orden.id,
            'numero': orden.numero,
            'venta_id': orden.venta_id,
            'producto_id': orden.producto_id,
            'cantidad_ordenada': orden.cantidad_ordenada,
            'cantidad_completada': orden.cantidad_completada,
            'estado': str(orden.estado),
            'prioridad': str(orden.prioridad),
            'fecha_creacion': orden.fecha_creacion.isoformat() if orden.fecha_creacion else None,
            'carretillero_id': orden.carretillero_id,
            'carretillero_nombre': (getattr(usuario, 'nombre_completo', None) or getattr(usuario, 'nombre', None) or getattr(usuario, 'username', None)),
            'seccion_produccion_id': orden.seccion_produccion_id,
            'seccion_produccion_nombre': (
                f"{getattr(seccion, 'codigo', '')} - {getattr(seccion, 'nombre', '')}".strip(" -") if seccion else None
            ),
            'movimientos_material': [],
            # Enriched fields used by UI cards
            'producto_codigo': getattr(producto, 'codigo', None),
            'producto_nombre': getattr(producto, 'nombre', None),
            'venta_numero': getattr(venta, 'numero', None),
            'cliente_nombre': getattr(venta, 'cliente_nombre', None),
            'porcentaje_completado': (
                float(orden.cantidad_completada) / float(orden.cantidad_ordenada) * 100.0
                if (orden.cantidad_ordenada or 0) > 0 else 0.0
            ),
        }
        resultado.append(orden_dict)

    return resultado


@router.post("/{orden_id}/asignar-carretillero")
async def asignar_carretillero_a_orden(
    orden_id: int,
    usuario_asignado_id: int,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Assign a carretillero to *all* movimientos of a production order.

    This matches the flow where the order is assigned once and the related
    warehouse movements inherit that assignment automatically.
    """
    orden = (await db.execute(
        select(OrdenProduccion).where(
            (OrdenProduccion.id == orden_id) & (OrdenProduccion.organization_id == org_id)
        )
    )).scalar_one_or_none()

    if not orden:
        raise HTTPException(status_code=404, detail="Orden de producción no encontrada")

    movimientos = (await db.execute(
        select(MovimientoAlmacen).where(
            (MovimientoAlmacen.orden_produccion_id == orden_id) &
            (MovimientoAlmacen.organization_id == org_id)
        )
    )).scalars().all()

    if not movimientos:
        return {"message": "Orden sin movimientos de almacén para asignar", "asignados": 0}

    now = datetime.utcnow()
    
    # Update the order with the carretillero assignment FIRST
    orden.carretillero_id = usuario_asignado_id
    
    asignados = 0
    for mov in movimientos:
        mov.usuario_asignado_id = usuario_asignado_id
        mov.fecha_asignacion = now
        if mov.estado == "pendiente":
            mov.estado = "asignado"
        asignados += 1

    await db.flush()  # Force flush changes before commit
    await db.commit()
    await db.refresh(orden)

    return {
        "message": "Carretillero asignado a todos los movimientos de la orden",
        "asignados": asignados,
        "orden_id": orden.id,
        "carretillero_id": orden.carretillero_id
    }


# ============ BULK ACTIONS ============

@router.post("/bulk-prioridad")
async def actualizar_prioridad_masiva(
    payload: BulkPrioridadRequest,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Update priority for multiple orders in a single transaction."""
    ids = list(set(payload.ids or []))
    if not ids:
        return {"updated": 0}

    ordenes = (await db.execute(
        select(OrdenProduccion).where(
            (OrdenProduccion.organization_id == org_id) & (OrdenProduccion.id.in_(ids))
        )
    )).scalars().all()

    for orden in ordenes:
        orden.prioridad = payload.prioridad.value if hasattr(payload.prioridad, 'value') else str(payload.prioridad)

    await db.commit()
    return {"updated": len(ordenes)}


# ============ MOVIMIENTOS DE ALMACÉN (Carretilleros) ============

@router.get("/movimientos", response_model=List[MovimientoAlmacenResponse])
async def listar_movimientos_pendientes(
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
    estado: Optional[str] = Query(None, description="Filter by status"),
    usuario_asignado_id: Optional[int] = Query(None, description="Filter by assigned carretillero"),
):
    """List pending warehouse movements for carretilleros."""
    query = select(MovimientoAlmacen).where(MovimientoAlmacen.organization_id == org_id)
    
    if estado:
        query = query.where(MovimientoAlmacen.estado == estado)
    
    if usuario_asignado_id:
        query = query.where(MovimientoAlmacen.usuario_asignado_id == usuario_asignado_id)
    
    result = await db.execute(
        query.order_by(desc(MovimientoAlmacen.fecha_creacion))
        .options(
            selectinload(MovimientoAlmacen.orden_produccion),
            selectinload(MovimientoAlmacen.producto),
            selectinload(MovimientoAlmacen.usuario_asignado)
        )
    )
    
    movimientos = result.scalars().all()
    
    # Enrich with producto details
    for mov in movimientos:
        if mov.producto:
            mov.producto_codigo = mov.producto.codigo
            mov.producto_nombre = mov.producto.nombre
    
    return movimientos


@router.post("/movimientos/{movimiento_id}/asignar")
async def asignar_movimiento_a_carretillero(
    movimiento_id: int,
    usuario_asignado_id: int,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Assign a warehouse movement to a carretillero (forklift operator)."""
    movimiento = await db.get(MovimientoAlmacen, movimiento_id)
    if not movimiento or movimiento.organization_id != org_id:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    
    movimiento.usuario_asignado_id = usuario_asignado_id
    movimiento.fecha_asignacion = datetime.utcnow()
    movimiento.estado = "asignado"
    
    db.add(movimiento)
    await db.commit()
    await db.refresh(movimiento, ["usuario_asignado", "orden_produccion", "producto"])
    
    return {"message": "Movimiento asignado", "movimiento": MovimientoAlmacenResponse.from_orm(movimiento)}


@router.post("/movimientos/{movimiento_id}/iniciar")
async def iniciar_movimiento(
    movimiento_id: int,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Mark movement as started (en_transito)."""
    movimiento = await db.get(MovimientoAlmacen, movimiento_id)
    if not movimiento or movimiento.organization_id != org_id:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    
    if movimiento.estado not in ["pendiente", "asignado"]:
        raise HTTPException(status_code=400, detail=f"No se puede iniciar movimiento en estado {movimiento.estado}")
    
    movimiento.estado = "en_transito"
    movimiento.fecha_movimiento = datetime.utcnow()
    
    db.add(movimiento)
    await db.commit()
    await db.refresh(movimiento, ["usuario_asignado", "orden_produccion", "producto"])
    
    return {"message": "Movimiento iniciado", "movimiento": MovimientoAlmacenResponse.from_orm(movimiento)}


@router.post("/movimientos/{movimiento_id}/completar")
async def completar_movimiento(
    movimiento_id: int,
    observaciones: str = Query(None, description="Completion notes"),
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Mark movement as completed (entregado).
    
    Si es un movimiento Fase 1 (almacén→playa), automáticamente crea el movimiento Fase 2 (playa→picking)
    para el mismo producto/cantidad en la misma orden.
    """
    movimiento = await db.get(MovimientoAlmacen, movimiento_id)
    if not movimiento or movimiento.organization_id != org_id:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    
    if movimiento.estado not in ["en_transito", "asignado", "pendiente"]:
        raise HTTPException(status_code=400, detail=f"No se puede completar movimiento en estado {movimiento.estado}")
    
    movimiento.estado = "entregado"
    movimiento.fecha_movimiento = datetime.utcnow()
    if observaciones:
        movimiento.observaciones = observaciones
    
    # Si es Fase 1 (salida_almacen), crear automáticamente Fase 2 (a_picking)
    if movimiento.tipo_movimiento == "salida_almacen":
        orden = await db.get(OrdenProduccion, movimiento.orden_produccion_id)
        if orden and orden.seccion_produccion_id:
            seccion = await db.get(SeccionProduccion, orden.seccion_produccion_id)
            if seccion:
                # Crear Fase 2: playa → picking de la sección
                m2 = MovimientoAlmacen(
                    organization_id=org_id,
                    orden_produccion_id=movimiento.orden_produccion_id,
                    producto_id=movimiento.producto_id,
                    tipo_movimiento="a_picking",
                    cantidad=movimiento.cantidad,
                    ubicacion_origen=movimiento.ubicacion_destino,  # La playa es el origen
                    ubicacion_destino=seccion.zona_picking or seccion.ubicacion,
                    estado="asignado" if orden.carretillero_id else "pendiente",
                    usuario_asignado_id=orden.carretillero_id,
                    fecha_asignacion=datetime.utcnow() if orden.carretillero_id else None,
                )
                db.add(m2)
    
    db.add(movimiento)
    await db.commit()
    await db.refresh(movimiento, ["usuario_asignado", "orden_produccion", "producto"])
    
    return {"message": "Movimiento completado", "movimiento": MovimientoAlmacenResponse.from_orm(movimiento)}


@router.post("/movimientos/{movimiento_id}/rechazar")
async def rechazar_movimiento(
    movimiento_id: int,
    motivo: str = Query(None, description="Rejection reason"),
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Mark movement as rejected."""
    movimiento = await db.get(MovimientoAlmacen, movimiento_id)
    if not movimiento or movimiento.organization_id != org_id:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    
    movimiento.estado = "rechazado"
    if motivo:
        movimiento.observaciones = motivo
    
    db.add(movimiento)
    await db.commit()
    await db.refresh(movimiento, ["usuario_asignado", "orden_produccion", "producto"])
    
    return {"message": "Movimiento rechazado", "movimiento": MovimientoAlmacenResponse.from_orm(movimiento)}
@router.get("/carretillero/{carretillero_id}", response_model=List[OrdenProduccionListResponse])
async def list_ordenes_por_carretillero(
    carretillero_id: int,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """List production orders assigned to a specific carretillero."""
    query = select(OrdenProduccion).where(
        (OrdenProduccion.organization_id == org_id) &
        (OrdenProduccion.carretillero_id == carretillero_id)
    ).order_by(desc(OrdenProduccion.fecha_creacion))
    
    ordenes = (await db.execute(query)).scalars().all()
    
    for orden in ordenes:
        if orden.venta:
            orden.venta_numero = getattr(orden.venta, "numero", None)
            orden.cliente_nombre = getattr(orden.venta, "cliente_nombre", None) or getattr(orden.venta, "cliente", None)
    
    return ordenes


@router.get("/{orden_id}", response_model=OrdenProduccionDetailResponse)
async def get_orden_produccion(
    orden_id: int,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Get production order details."""
    query = select(OrdenProduccion).where(
        (OrdenProduccion.id == orden_id) &
        (OrdenProduccion.organization_id == org_id)
    ).options(
        selectinload(OrdenProduccion.operaciones),
        selectinload(OrdenProduccion.movimientos_material)
    )
    
    orden = (await db.execute(query)).scalar_one_or_none()
    if not orden:
        raise HTTPException(status_code=404, detail="Orden de producción no encontrada")

    return orden


@router.post("/", response_model=OrdenProduccionResponse)
async def create_orden_produccion(
    payload: OrdenProduccionCreate,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Create a new production order."""
    # Validate references exist
    venta = (await db.execute(
        select(Venta).where((Venta.id == payload.venta_id) & (Venta.organization_id == org_id))
    )).scalar_one_or_none()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    
    bom = (await db.execute(
        select(BOMHeader).where((BOMHeader.id == payload.bom_id) & (BOMHeader.organization_id == org_id))
    )).scalar_one_or_none()
    if not bom:
        raise HTTPException(status_code=404, detail="BOM no encontrado")
    
    producto = (await db.execute(
        select(Producto).where((Producto.id == payload.producto_id) & (Producto.organization_id == org_id))
    )).scalar_one_or_none()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Generate order number
    last_order = (await db.execute(
        select(OrdenProduccion).where(OrdenProduccion.organization_id == org_id)
        .order_by(desc(OrdenProduccion.id)).limit(1)
    )).scalar_one_or_none()
    
    order_number = f"OP-{datetime.utcnow().year}-{(last_order.id + 1 if last_order else 1):05d}"

    carretillero_id = payload.carretillero_id or await seleccionar_carretillero(db, org_id)
    
    # Create order
    nueva_orden = OrdenProduccion(
        organization_id=org_id,
        venta_id=payload.venta_id,
        bom_id=payload.bom_id,
        producto_id=payload.producto_id,
        numero=order_number,
        cantidad_ordenada=payload.cantidad_ordenada,
        descripcion=payload.descripcion,
        prioridad=payload.prioridad,
        carretillero_id=carretillero_id,
    )
    
    db.add(nueva_orden)
    await db.flush()

    # Auto-assign to VIP section if available and start acquisition immediately
    vip_seccion = (await db.execute(
        select(SeccionProduccion).where(
            (SeccionProduccion.organization_id == org_id) &
            (SeccionProduccion.activa == True) &
            (
                SeccionProduccion.codigo.ilike("%vip%") |
                SeccionProduccion.nombre.ilike("%vip%")
            )
        )
    )).scalar_one_or_none()

    if vip_seccion:
        nueva_orden.seccion_produccion_id = vip_seccion.id
        nueva_orden.asignado_a = vip_seccion.supervisor_nombre
        nueva_orden.fecha_asignacion = datetime.utcnow()
        # Generate picking movements based on BOM lines
        bom_lines = (await db.execute(
            select(BOMLine, Producto).join(Producto, BOMLine.componente_id == Producto.id).where(
                (BOMLine.bom_header_id == payload.bom_id) & (BOMLine.organization_id == org_id)
            )
        )).all()

        playa_salida = await _ubicacion_playa_salida_almacen(db, org_id)
        for bom_line, componente in bom_lines:
            cantidad_base = bom_line.cantidad * payload.cantidad_ordenada
            desperdicio = bom_line.factor_desperdicio or 0
            cantidad_total = cantidad_base * (1 + desperdicio)
            ubic_origen = await _ubicacion_almacen_canonica(db, org_id, getattr(componente, 'ubicacion_almacen', None))
            # M1: almacén -> playa
            m1 = MovimientoAlmacen(
                organization_id=org_id,
                orden_produccion_id=nueva_orden.id,
                producto_id=componente.id,
                tipo_movimiento="salida_almacen",
                cantidad=cantidad_total,
                ubicacion_origen=ubic_origen,
                ubicacion_destino=playa_salida,
                estado="asignado" if carretillero_id else "pendiente",
                usuario_asignado_id=carretillero_id,
                fecha_asignacion=datetime.utcnow() if carretillero_id else None,
            )
            db.add(m1)
            # M2: playa -> picking sección VIP
            m2 = MovimientoAlmacen(
                organization_id=org_id,
                orden_produccion_id=nueva_orden.id,
                producto_id=componente.id,
                tipo_movimiento="a_picking",
                cantidad=cantidad_total,
                ubicacion_origen=playa_salida,
                ubicacion_destino=vip_seccion.zona_picking or vip_seccion.ubicacion,
                estado="asignado" if carretillero_id else "pendiente",
                usuario_asignado_id=carretillero_id,
                fecha_asignacion=datetime.utcnow() if carretillero_id else None,
            )
            db.add(m2)

        nueva_orden.estado = EstadoOrdenProduccion.ADQUISICION_MATERIALES
    
    # Create operations from BOM
    bom_operaciones = (await db.execute(
        select(BOMOperacion).where(BOMOperacion.bom_id == payload.bom_id)
        .order_by(BOMOperacion.secuencia)
    )).scalars().all()
    
    for idx, bom_op in enumerate(bom_operaciones, 1):
        operacion = OperacionProduccion(
            organization_id=org_id,
            orden_produccion_id=nueva_orden.id,
            bom_operacion_id=bom_op.id,
            secuencia=idx * 10,
            duracion_estimada=bom_op.duracion_estimada,
        )
        db.add(operacion)
    
    # Update venta estado
    venta.estado = "en_produccion"
    
    await db.commit()
    await db.refresh(nueva_orden, ["operaciones"])
    
    return nueva_orden


@router.put("/{orden_id}", response_model=OrdenProduccionResponse)
async def update_orden_produccion(
    orden_id: int,
    payload: OrdenProduccionUpdate,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Update production order."""
    orden = (await db.execute(
        select(OrdenProduccion).where(
            (OrdenProduccion.id == orden_id) &
            (OrdenProduccion.organization_id == org_id)
        )
    )).scalar_one_or_none()
    
    if not orden:
        raise HTTPException(status_code=404, detail="Orden de producción no encontrada")
    
    update_data = payload.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(orden, field, value)
    
    await db.commit()
    await db.refresh(orden)
    
    return orden


@router.post("/{orden_id}/cambiar-estado", response_model=OrdenProduccionResponse)
async def cambiar_estado_orden(
    orden_id: int,
    payload: OrdenProduccionStateChange,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Change production order state."""
    orden = (await db.execute(
        select(OrdenProduccion).where(
            (OrdenProduccion.id == orden_id) &
            (OrdenProduccion.organization_id == org_id)
        )
    )).scalar_one_or_none()
    
    if not orden:
        raise HTTPException(status_code=404, detail="Orden de producción no encontrada")
    
    # Validate state transitions
    estado_actual = orden.estado
    nuevo_estado = payload.nuevo_estado
    
    # Track timing
    if nuevo_estado == EstadoOrdenProduccion.EN_PROCESO and not orden.fecha_inicio_real:
        orden.fecha_inicio_real = datetime.utcnow()
    elif nuevo_estado == EstadoOrdenProduccion.COMPLETADA and not orden.fecha_fin_real:
        orden.fecha_fin_real = datetime.utcnow()
        orden.cantidad_completada = orden.cantidad_ordenada
        # Update venta
        orden.venta.estado = "completado"
    
    orden.estado = nuevo_estado
    if payload.notas:
        orden.notas_produccion = (orden.notas_produccion or "") + f"\n{payload.notas}"
    
    await db.commit()
    await db.refresh(orden)
    
    return orden


@router.delete("/{orden_id}")
async def delete_orden_produccion(
    orden_id: int,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Delete production order."""
    orden = (await db.execute(
        select(OrdenProduccion).where(
            (OrdenProduccion.id == orden_id) &
            (OrdenProduccion.organization_id == org_id)
        )
    )).scalar_one_or_none()
    
    if not orden:
        raise HTTPException(status_code=404, detail="Orden de producción no encontrada")
    
    await db.delete(orden)
    await db.commit()
    
    return {"message": "Orden de producción eliminada"}


# ============ OPERACIÓN PRODUCCIÓN ENDPOINTS ============

@router.post("/{orden_id}/operaciones", response_model=OperacionProduccionResponse)
async def add_operacion_produccion(
    orden_id: int,
    payload: OperacionProduccionCreate,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Add operation to production order."""
    orden = (await db.execute(
        select(OrdenProduccion).where(
            (OrdenProduccion.id == orden_id) &
            (OrdenProduccion.organization_id == org_id)
        )
    )).scalar_one_or_none()
    
    if not orden:
        raise HTTPException(status_code=404, detail="Orden de producción no encontrada")
    
    operacion = OperacionProduccion(
        organization_id=org_id,
        orden_produccion_id=orden_id,
        **payload.dict()
    )
    
    db.add(operacion)
    await db.commit()
    await db.refresh(operacion)
    
    return operacion


@router.put("/operaciones/{op_id}", response_model=OperacionProduccionResponse)
async def update_operacion_produccion(
    op_id: int,
    payload: OperacionProduccionUpdate,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Update production operation."""
    operacion = (await db.execute(
        select(OperacionProduccion).where(
            (OperacionProduccion.id == op_id) &
            (OperacionProduccion.organization_id == org_id)
        )
    )).scalar_one_or_none()
    
    if not operacion:
        raise HTTPException(status_code=404, detail="Operación no encontrada")
    
    update_data = payload.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(operacion, field, value)
    
    await db.commit()
    await db.refresh(operacion)
    
    return operacion


# ============ MOVIMIENTO ALMACÉN ENDPOINTS ============

@router.post("/{orden_id}/movimientos", response_model=MovimientoAlmacenResponse)
async def create_movimiento_almacen(
    orden_id: int,
    payload: MovimientoAlmacenCreate,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Create material movement for production order."""
    orden = (await db.execute(
        select(OrdenProduccion).where(
            (OrdenProduccion.id == orden_id) &
            (OrdenProduccion.organization_id == org_id)
        )
    )).scalar_one_or_none()
    
    if not orden:
        raise HTTPException(status_code=404, detail="Orden de producción no encontrada")
    
    movimiento = MovimientoAlmacen(
        organization_id=org_id,
        orden_produccion_id=orden_id,
        **payload.dict()
    )
    
    db.add(movimiento)
    await db.commit()
    await db.refresh(movimiento)
    
    return movimiento


@router.get("/{orden_id}/movimientos", response_model=List[MovimientoAlmacenResponse])
async def list_movimientos_orden(
    orden_id: int,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """List material movements for production order."""
    orden = (await db.execute(
        select(OrdenProduccion).where(
            (OrdenProduccion.id == orden_id) &
            (OrdenProduccion.organization_id == org_id)
        )
    )).scalar_one_or_none()
    
    if not orden:
        raise HTTPException(status_code=404, detail="Orden de producción no encontrada")
    
    movimientos = (await db.execute(
        select(MovimientoAlmacen).where(
            MovimientoAlmacen.orden_produccion_id == orden_id
        ).order_by(MovimientoAlmacen.fecha_creacion)
    )).scalars().all()
    
    return movimientos


# ============ OPERACIONES - ENDPOINTS PARA OPERARIOS ============

@router.put("/operaciones/{operacion_id}/estado")
async def actualizar_estado_operacion(
    operacion_id: int,
    payload: dict,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Actualizar estado de una operación (para operarios)."""
    operacion = (await db.execute(
        select(OperacionProduccion).where(
            (OperacionProduccion.id == operacion_id) &
            (OperacionProduccion.organization_id == org_id)
        )
    )).scalar_one_or_none()
    
    if not operacion:
        raise HTTPException(status_code=404, detail="Operación no encontrada")
    
    nuevo_estado = payload.get("estado")
    if not nuevo_estado:
        raise HTTPException(status_code=400, detail="Estado requerido")
    
    # Validate state transition
    valid_states = ["pendiente", "en_proceso", "pausada", "completada", "cancelada"]
    if nuevo_estado not in valid_states:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Estados válidos: {valid_states}")
    
    operacion.estado = nuevo_estado
    operacion.fecha_modificacion = datetime.utcnow()
    
    if nuevo_estado == "en_proceso" and not operacion.fecha_inicio_real:
        operacion.fecha_inicio_real = datetime.utcnow()
    
    if nuevo_estado == "completada" and not operacion.fecha_fin_real:
        operacion.fecha_fin_real = datetime.utcnow()
    
    await db.commit()
    await db.refresh(operacion)
    
    return {
        "success": True,
        "operacion_id": operacion.id,
        "estado": operacion.estado,
        "message": f"Operación actualizada a {nuevo_estado}"
    }


@router.post("/operaciones/{operacion_id}/completar")
async def completar_operacion(
    operacion_id: int,
    payload: dict,
    db: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Marcar operación como completada con notas opcionales."""
    operacion = (await db.execute(
        select(OperacionProduccion).where(
            (OperacionProduccion.id == operacion_id) &
            (OperacionProduccion.organization_id == org_id)
        )
    )).scalar_one_or_none()
    
    if not operacion:
        raise HTTPException(status_code=404, detail="Operación no encontrada")
    
    operacion.estado = "completada"
    operacion.fecha_fin_real = datetime.utcnow()
    operacion.fecha_modificacion = datetime.utcnow()
    
    if payload.get("notas"):
        operacion.notas = payload["notas"]
    
    await db.commit()
    await db.refresh(operacion)
    
    return {
        "success": True,
        "operacion_id": operacion.id,
        "estado": operacion.estado,
        "message": "Operación completada exitosamente"
    }


