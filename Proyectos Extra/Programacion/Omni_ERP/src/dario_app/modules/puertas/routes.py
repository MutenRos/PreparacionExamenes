"""Puertas (Doors) API routes."""

from datetime import datetime
from typing import List
from dario_app.modules.recepcion.models import Albaran, AlbaranDetalle, EstadoAlbaran

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, field_validator
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.database import get_db, get_tenant_engine, Base

from .models import Puerta, MovimientoPuerta, TipoPuerta, RecepcionDetalle

router = APIRouter(prefix="/api/puertas", tags=["puertas"])


async def ensure_puertas_tables():
    """Ensure puertas tables exist in the database."""
    try:
        engine = get_tenant_engine(1)
        async with engine.begin() as conn:
            # Create tables if they don't exist
            await conn.run_sync(Puerta.__table__.create, checkfirst=True)
            await conn.run_sync(MovimientoPuerta.__table__.create, checkfirst=True)
            await conn.run_sync(RecepcionDetalle.__table__.create, checkfirst=True)
    except Exception as e:
        print(f"Warning: Could not create puertas tables: {e}")


def get_org_id() -> int:
    """Get organization ID - for now hardcoded to 1 (local tenant)."""
    return 1


async def get_tenant_db_local(org_id: int = Depends(get_org_id)):
    """Session en la base del tenant actual (local helper)."""
    async for session in get_db(org_id):
        yield session


# ============ PUERTA SCHEMAS ============
class PuertaCreate(BaseModel):
    nombre: str
    codigo: str
    tipo: TipoPuerta
    ubicacion: str | None = None
    descripcion: str | None = None
    responsable_id: int | None = None
    responsable_nombre: str | None = None
    es_activa: bool = True
    requiere_autorizacion: bool = True
    horario_apertura: str | None = None
    horario_cierre: str | None = None
    notas: str | None = None

    @field_validator("codigo")
    @classmethod
    def validate_codigo(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("El código de puerta es requerido")
        return v.upper().strip()

    @field_validator("nombre")
    @classmethod
    def validate_nombre(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("El nombre de puerta es requerido")
        return v.strip()


class PuertaUpdate(BaseModel):
    nombre: str | None = None
    ubicacion: str | None = None
    descripcion: str | None = None
    responsable_id: int | None = None
    responsable_nombre: str | None = None
    es_activa: bool | None = None
    requiere_autorizacion: bool | None = None
    horario_apertura: str | None = None
    horario_cierre: str | None = None
    notas: str | None = None


class PuertaResponse(BaseModel):
    id: int
    nombre: str
    codigo: str
    tipo: str
    ubicacion: str | None
    descripcion: str | None
    responsable_id: int | None
    responsable_nombre: str | None
    es_activa: bool
    requiere_autorizacion: bool
    horario_apertura: str | None
    horario_cierre: str | None
    notas: str | None
    creado_en: datetime
    actualizado_en: datetime

    class Config:
        from_attributes = True


# ============ MOVIMIENTO PUERTA SCHEMAS ============
class MovimientoPuertaCreate(BaseModel):
    puerta_id: int
    usuario_id: int | None = None
    usuario_nombre: str | None = None
    referencia_documento: str | None = None
    tipo_documento: str | None = None
    documento_id: int | None = None
    cantidad_items: int | None = None
    descripcion: str | None = None
    notas: str | None = None


class MovimientoPuertaAutorizar(BaseModel):
    autorizado_por_id: int
    autorizado_por_nombre: str | None = None
    estado: str = "autorizado"  # autorizado, rechazado, etc.
    notas: str | None = None


class MovimientoPuertaResponse(BaseModel):
    id: int
    puerta_id: int
    usuario_id: int | None
    usuario_nombre: str | None
    referencia_documento: str | None
    tipo_documento: str | None
    documento_id: int | None
    cantidad_items: int | None
    descripcion: str | None
    autorizado_por_id: int | None
    autorizado_por_nombre: str | None
    estado: str
    notas: str | None
    creado_en: datetime
    completado_en: datetime | None

    class Config:
        from_attributes = True


# ============ PUERTAS ENDPOINTS ============

@router.get("/", response_model=List[PuertaResponse])
async def listar_puertas(
    tipo: TipoPuerta | None = Query(None),
    es_activa: bool | None = Query(None),
    session: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """List all doors (entry and exit points)."""
    # Ensure tables exist to avoid querying non-existent tables in fresh setups
    await ensure_puertas_tables()
    query = select(Puerta).where(Puerta.organization_id == org_id)
    
    if tipo:
        query = query.where(Puerta.tipo == tipo.value)
    
    if es_activa is not None:
        query = query.where(Puerta.es_activa == es_activa)
    
    result = await session.execute(query)
    return result.scalars().all()


@router.post("/", response_model=PuertaResponse, status_code=status.HTTP_201_CREATED)
async def crear_puerta(
    puerta_data: PuertaCreate,
    session: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Create a new door (entry or exit point)."""
    # Verificar que el código sea único
    existing = await session.execute(
        select(Puerta).where(
            and_(
                Puerta.organization_id == org_id,
                Puerta.codigo == puerta_data.codigo.upper()
            )
        )
    )
    if existing.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una puerta con el código {puerta_data.codigo}"
        )
    
    new_puerta = Puerta(
        organization_id=org_id,
        nombre=puerta_data.nombre,
        codigo=puerta_data.codigo.upper(),
        tipo=puerta_data.tipo.value,
        ubicacion=puerta_data.ubicacion,
        descripcion=puerta_data.descripcion,
        responsable_id=puerta_data.responsable_id,
        responsable_nombre=puerta_data.responsable_nombre,
        es_activa=puerta_data.es_activa,
        requiere_autorizacion=puerta_data.requiere_autorizacion,
        horario_apertura=puerta_data.horario_apertura,
        horario_cierre=puerta_data.horario_cierre,
        notas=puerta_data.notas,
    )
    
    session.add(new_puerta)
    await session.commit()
    await session.refresh(new_puerta)
    
    return new_puerta


@router.get("/{puerta_id}", response_model=PuertaResponse)
async def obtener_puerta(
    puerta_id: int,
    session: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Get a specific door."""
    result = await session.execute(
        select(Puerta).where(
            and_(
                Puerta.id == puerta_id,
                Puerta.organization_id == org_id
            )
        )
    )
    puerta = result.scalars().first()
    if not puerta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Puerta no encontrada"
        )
    return puerta


@router.put("/{puerta_id}", response_model=PuertaResponse)
async def actualizar_puerta(
    puerta_id: int,
    puerta_data: PuertaUpdate,
    session: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Update a door."""
    result = await session.execute(
        select(Puerta).where(
            and_(
                Puerta.id == puerta_id,
                Puerta.organization_id == org_id
            )
        )
    )
    puerta = result.scalars().first()
    if not puerta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Puerta no encontrada"
        )
    
    # Actualizar campos
    update_data = puerta_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(puerta, field, value)
    
    await session.commit()
    await session.refresh(puerta)
    return puerta


@router.delete("/{puerta_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_puerta(
    puerta_id: int,
    session: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Delete a door (soft delete by marking as inactive)."""
    result = await session.execute(
        select(Puerta).where(
            and_(
                Puerta.id == puerta_id,
                Puerta.organization_id == org_id
            )
        )
    )
    puerta = result.scalars().first()
    if not puerta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Puerta no encontrada"
        )
    
    puerta.es_activa = False
    await session.commit()


# ============ MOVIMIENTOS PUERTAS ENDPOINTS ============

@router.get("/{puerta_id}/movimientos", response_model=List[MovimientoPuertaResponse])
async def listar_movimientos_puerta(
    puerta_id: int,
    estado: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    session: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """List movements for a specific door."""
    # Verificar que la puerta exista
    puerta_result = await session.execute(
        select(Puerta).where(
            and_(
                Puerta.id == puerta_id,
                Puerta.organization_id == org_id
            )
        )
    )
    if not puerta_result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Puerta no encontrada"
        )
    
    query = select(MovimientoPuerta).where(
        and_(
            MovimientoPuerta.organization_id == org_id,
            MovimientoPuerta.puerta_id == puerta_id
        )
    )
    
    if estado:
        query = query.where(MovimientoPuerta.estado == estado)
    
    query = query.offset(skip).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()


@router.post("/{puerta_id}/movimientos", response_model=MovimientoPuertaResponse, status_code=status.HTTP_201_CREATED)
async def registrar_movimiento(
    puerta_id: int,
    movimiento_data: MovimientoPuertaCreate,
    session: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Register a movement at a door."""
    # Verificar que la puerta exista
    puerta_result = await session.execute(
        select(Puerta).where(
            and_(
                Puerta.id == puerta_id,
                Puerta.organization_id == org_id
            )
        )
    )
    puerta = puerta_result.scalars().first()
    if not puerta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Puerta no encontrada"
        )
    
    # Determinar estado inicial basado en si requiere autorización
    estado_inicial = "pendiente" if puerta.requiere_autorizacion else "completado"
    
    new_movimiento = MovimientoPuerta(
        organization_id=org_id,
        puerta_id=puerta_id,
        usuario_id=movimiento_data.usuario_id,
        usuario_nombre=movimiento_data.usuario_nombre,
        referencia_documento=movimiento_data.referencia_documento,
        tipo_documento=movimiento_data.tipo_documento,
        documento_id=movimiento_data.documento_id,
        cantidad_items=movimiento_data.cantidad_items,
        descripcion=movimiento_data.descripcion,
        estado=estado_inicial,
        notas=movimiento_data.notas,
    )
    
    session.add(new_movimiento)
    await session.commit()
    await session.refresh(new_movimiento)
    
    return new_movimiento


@router.get("/movimientos/{movimiento_id}", response_model=MovimientoPuertaResponse)
async def obtener_movimiento(
    movimiento_id: int,
    session: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Get a specific movement record."""
    result = await session.execute(
        select(MovimientoPuerta).where(
            and_(
                MovimientoPuerta.id == movimiento_id,
                MovimientoPuerta.organization_id == org_id
            )
        )
    )
    movimiento = result.scalars().first()
    if not movimiento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movimiento no encontrado"
        )
    return movimiento


@router.post("/{puerta_id}/movimientos/{movimiento_id}/autorizar", response_model=MovimientoPuertaResponse)
async def autorizar_movimiento(
    puerta_id: int,
    movimiento_id: int,
    autorizar_data: MovimientoPuertaAutorizar,
    session: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Authorize or reject a door movement."""
    result = await session.execute(
        select(MovimientoPuerta).where(
            and_(
                MovimientoPuerta.id == movimiento_id,
                MovimientoPuerta.puerta_id == puerta_id,
                MovimientoPuerta.organization_id == org_id
            )
        )
    )
    movimiento = result.scalars().first()
    if not movimiento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movimiento no encontrado"
        )
    
    movimiento.autorizado_por_id = autorizar_data.autorizado_por_id
    movimiento.autorizado_por_nombre = autorizar_data.autorizado_por_nombre
    movimiento.estado = autorizar_data.estado
    if autorizar_data.notas:
        movimiento.notas = autorizar_data.notas
    
    if autorizar_data.estado == "completado":
        movimiento.completado_en = datetime.utcnow()
    
    await session.commit()
    await session.refresh(movimiento)
    return movimiento


@router.post("/{puerta_id}/movimientos/{movimiento_id}/completar", response_model=MovimientoPuertaResponse)
async def completar_movimiento(
    puerta_id: int,
    movimiento_id: int,
    session: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Mark a movement as completed."""
    result = await session.execute(
        select(MovimientoPuerta).where(
            and_(
                MovimientoPuerta.id == movimiento_id,
                MovimientoPuerta.puerta_id == puerta_id,
                MovimientoPuerta.organization_id == org_id
            )
        )
    )
    movimiento = result.scalars().first()
    if not movimiento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movimiento no encontrado"
        )
    
    movimiento.estado = "completado"
    movimiento.completado_en = datetime.utcnow()
    
    await session.commit()
    await session.refresh(movimiento)
    return movimiento


# ============ DASHBOARD ENTRADA - PENDIENTES DE RECEPCIÓN ============

class DocumentoPendienteResponse(BaseModel):
    """Response schema for pending documents awaiting reception."""
    id: int
    tipo_documento: str  # orden_compra, devolucion, orden_produccion_externa
    numero_documento: str
    fecha: datetime
    proveedor_nombre: str | None = None
    total_items: int
    items_recibidos: int
    estado: str
    detalles: list | None = None

    class Config:
        from_attributes = True


@router.get("/entrada/pendientes", response_model=List[DocumentoPendienteResponse])
async def obtener_pendientes_entrada(
    tipo: str | None = Query(None),
    busqueda: str | None = Query(None),
    session: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Get all pending documents for reception at entry doors.
    
    Returns:
    - Órdenes de compra pendientes/parciales
    - Devoluciones autorizadas pendientes
    - Órdenes de producción externas pendientes
    """
    # Ensure tables exist
    await ensure_puertas_tables()
    
    from dario_app.modules.compras.models import Compra, CompraDetalle
    from dario_app.modules.produccion_ordenes.models import OrdenProduccion
    
    pendientes = []
    
    # 1. Órdenes de compra pendientes de recepción (aprobadas y no completas)
    if not tipo or tipo == "orden_compra":
        query_compras = select(Compra).where(
            and_(
                Compra.organization_id == org_id,
                # Mostrar aprobadas o en recepción parcial (cuando estado cambia a recepcion_parcial)
                Compra.estado.in_(["aprobada", "recepcion_parcial", "recepcion_completa"]),
                # Mostrar si está sin recibir O parcialmente recibida
                Compra.estado_recepcion.in_(["no_recibida", "parcial"])
            )
        )
        
        if busqueda:
            query_compras = query_compras.where(
                Compra.numero.ilike(f"%{busqueda}%") | 
                Compra.proveedor_nombre.ilike(f"%{busqueda}%")
            )
        
        result_compras = await session.execute(query_compras)
        compras = result_compras.scalars().all()
        
        for compra in compras:
            # Contar detalles con información del producto
            from dario_app.modules.inventario.models import Producto
            from dario_app.modules.puertas.models import RecepcionDetalle
            from sqlalchemy import func
            
            detalles_query = select(CompraDetalle, Producto).join(
                Producto, CompraDetalle.producto_id == Producto.id
            ).where(
                CompraDetalle.compra_id == compra.id
            )
            detalles_result = await session.execute(detalles_query)
            detalles_rows = detalles_result.all()
            
            detalles_info = []
            total_items_completos = 0
            
            for detalle, producto in detalles_rows:
                # Calcular cantidad recibida de este producto en esta compra
                recibido_query = select(func.sum(RecepcionDetalle.cantidad_recibida)).where(
                    and_(
                        RecepcionDetalle.organization_id == org_id,
                        RecepcionDetalle.tipo_documento == "orden_compra",
                        RecepcionDetalle.documento_id == compra.id,
                        RecepcionDetalle.producto_id == detalle.producto_id,
                        RecepcionDetalle.estado_recepcion.in_(["recibido", "dañado"])
                    )
                )
                recibido_result = await session.execute(recibido_query)
                cantidad_recibida = recibido_result.scalar() or 0
                
                # Contar items completamente recibidos
                if cantidad_recibida >= detalle.cantidad:
                    total_items_completos += 1
                
                detalles_info.append({
                    "producto_id": detalle.producto_id,
                    "producto_codigo": producto.codigo,
                    "producto_nombre": producto.nombre,
                    "cantidad": detalle.cantidad,
                    "recibido": int(cantidad_recibida),
                    "pendiente": max(0, detalle.cantidad - int(cantidad_recibida))
                })
            
            # Mostrar todas las compras aprobadas que no estén completa
            # (usando el campo estado_recepcion que ya está actualizado automáticamente)
            if compra.estado_recepcion in ["no_recibida", "parcial"]:
                pendientes.append({
                    "id": compra.id,
                    "tipo_documento": "orden_compra",
                    "numero_documento": compra.numero,
                    "fecha": compra.fecha,
                    "proveedor_nombre": compra.proveedor_nombre,
                    "total_items": compra.cantidad_items_esperados or len(detalles_info),
                    "items_recibidos": compra.cantidad_items_recibidos or total_items_completos,
                    "estado": compra.estado_recepcion,  # Cambiar a estado_recepcion
                    "detalles": detalles_info
                })
    
    # 2. Órdenes de producción externas con operaciones externas
    if not tipo or tipo == "orden_produccion_externa":
        query_op = select(OrdenProduccion).where(
            and_(
                OrdenProduccion.organization_id == org_id,
                OrdenProduccion.costo_operaciones_externas > 0,
                OrdenProduccion.estado.in_(["en_proceso", "adquisicion_materiales"])
            )
        )
        
        if busqueda:
            query_op = query_op.where(
                OrdenProduccion.numero.ilike(f"%{busqueda}%")
            )
        
        result_op = await session.execute(query_op)
        ordenes = result_op.scalars().all()
        
        for orden in ordenes:
            pendientes.append({
                "id": orden.id,
                "tipo_documento": "orden_produccion_externa",
                "numero_documento": orden.numero,
                "fecha": orden.fecha_creacion,
                "proveedor_nombre": "Producción Externa",
                "total_items": 1,
                "items_recibidos": 0,
                "estado": orden.estado,
                "detalles": [
                    {
                        "producto_id": orden.producto_id,
                        "cantidad": orden.cantidad_ordenada,
                        "recibido": orden.cantidad_completada
                    }
                ]
            })
    
    # TODO: Agregar devoluciones autorizadas cuando se implemente el módulo
    
    return pendientes


class RecepcionCreate(BaseModel):
    """Schema for creating a reception record."""
    puerta_id: int
    tipo_documento: str
    documento_id: int
    usuario_nombre: str | None = None
    items_recibidos: list
    notas: str | None = None


class ItemRecibido(BaseModel):
    """Schema for received items."""
    producto_id: int
    cantidad_recibida: int
    estado: str = "recibido"  # recibido, dañado, rechazado
    notas: str | None = None

async def _generar_numero_albaran(session: AsyncSession, org_id: int) -> str:
    """Genera un número único de albarán para la organización."""
    result = await session.execute(
        select(func.count(Albaran.id)).where(Albaran.organization_id == org_id)
    )
    count = result.scalar() or 0
    return f"ALB-{org_id}-{datetime.utcnow().strftime('%Y%m%d')}-{count + 1:04d}"


@router.post("/entrada/recepcionar")
async def registrar_recepcion(
    recepcion: RecepcionCreate,
    session: AsyncSession = Depends(get_tenant_db_local),
    org_id: int = Depends(get_org_id),
):
    """Register reception of materials at entry door.
    
    This will:
    1. Create a movement record
    2. Save detailed reception tracking
    3. Update the document status (partial/complete)
    4. Update inventory levels (if configured)
    """
    from dario_app.modules.puertas.models import RecepcionDetalle
    from dario_app.modules.compras.models import Compra, CompraDetalle
    from sqlalchemy import func
    
    # Verificar que la puerta existe y es de entrada
    puerta_result = await session.execute(
        select(Puerta).where(
            and_(
                Puerta.id == recepcion.puerta_id,
                Puerta.organization_id == org_id,
                Puerta.tipo == TipoPuerta.ENTRADA.value
            )
        )
    )
    puerta = puerta_result.scalars().first()
    if not puerta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Puerta de entrada no encontrada"
        )
    
    # Crear movimiento
    new_movimiento = MovimientoPuerta(
        organization_id=org_id,
        puerta_id=recepcion.puerta_id,
        usuario_nombre=recepcion.usuario_nombre,
        referencia_documento=f"{recepcion.tipo_documento}-{recepcion.documento_id}",
        tipo_documento=recepcion.tipo_documento,
        documento_id=recepcion.documento_id,
        cantidad_items=len(recepcion.items_recibidos),
        descripcion=f"Recepción de {len(recepcion.items_recibidos)} items",
        estado="completado" if not puerta.requiere_autorizacion else "pendiente",
        notas=recepcion.notas,
        completado_en=datetime.utcnow() if not puerta.requiere_autorizacion else None,
    )
    
    session.add(new_movimiento)
    await session.flush()  # Get movimiento ID
    
    # Guardar detalles de recepción
    for item in recepcion.items_recibidos:
        if item.get('cantidad_recibida', 0) > 0:
            detalle = RecepcionDetalle(
                organization_id=org_id,
                movimiento_id=new_movimiento.id,
                tipo_documento=recepcion.tipo_documento,
                documento_id=recepcion.documento_id,
                producto_id=item['producto_id'],
                cantidad_esperada=item.get('cantidad_esperada', item['cantidad_recibida']),
                cantidad_recibida=item['cantidad_recibida'],
                estado_recepcion=item.get('estado', 'recibido'),
                notas=item.get('notas')
            )
            session.add(detalle)
    
    # Actualizar estado del documento si es orden de compra
    if recepcion.tipo_documento == "orden_compra":
        compra = await session.get(Compra, recepcion.documento_id)
        if compra:
            # Asegurar que los detalles de recepción recién añadidos estén disponibles para las agregaciones
            await session.flush()

            # Traer detalles de compra para validar y calcular estados
            detalles_compra_result = await session.execute(
                select(CompraDetalle).where(CompraDetalle.compra_id == compra.id)
            )
            detalles_compra = detalles_compra_result.scalars().all()

            # Crear albarán interno para contabilidad/logística
            items_validos = [i for i in recepcion.items_recibidos if i.get('cantidad_recibida', 0) > 0]
            if items_validos:
                numero_albaran = await _generar_numero_albaran(session, org_id)
                albaran = Albaran(
                    organization_id=org_id,
                    numero=numero_albaran,
                    compra_id=compra.id,
                    usuario_id=None,
                    estado=EstadoAlbaran.PARCIAL.value,
                    total_items=len(items_validos),
                    items_recibidos=0,
                    notas=recepcion.notas,
                )
                session.add(albaran)
                await session.flush()

                hay_diferencias = False
                for item in items_validos:
                    cantidad_recibida = item.get('cantidad_recibida', 0)
                    # Vincular con el detalle de compra por producto
                    det_result = await session.execute(
                        select(CompraDetalle).where(
                            and_(
                                CompraDetalle.compra_id == compra.id,
                                CompraDetalle.producto_id == item['producto_id'],
                            )
                        )
                    )
                    compra_detalle = det_result.scalars().first()
                    if not compra_detalle:
                        continue

                    cantidad_diferencia = compra_detalle.cantidad - cantidad_recibida
                    if cantidad_diferencia != 0:
                        hay_diferencias = True

                    detalle_albaran = AlbaranDetalle(
                        albaran_id=albaran.id,
                        compra_detalle_id=compra_detalle.id,
                        producto_id=compra_detalle.producto_id,
                        cantidad_ordenada=compra_detalle.cantidad,
                        cantidad_recibida=cantidad_recibida,
                        cantidad_diferencia=cantidad_diferencia,
                        lotes_recibidos=item.get('lotes_recibidos'),
                        fechas_vencimiento=item.get('fechas_vencimiento'),
                        notas=item.get('notas'),
                    )
                    session.add(detalle_albaran)
                    albaran.items_recibidos += 1

                # Estado del albarán
                if albaran.items_recibidos == albaran.total_items and not hay_diferencias:
                    albaran.estado = EstadoAlbaran.COMPLETO.value
                elif albaran.items_recibidos > 0:
                    albaran.estado = EstadoAlbaran.PARCIAL.value

            # Sincronizar cantidades agregadas en la compra
            total_ordenado_q = await session.execute(
                select(func.sum(CompraDetalle.cantidad)).where(CompraDetalle.compra_id == compra.id)
            )
            total_recibido_q = await session.execute(
                select(func.sum(AlbaranDetalle.cantidad_recibida)).where(
                    AlbaranDetalle.albaran_id.in_(select(Albaran.id).where(Albaran.compra_id == compra.id))
                )
            )
            total_ordenado = total_ordenado_q.scalar() or 0
            total_recibido = total_recibido_q.scalar() or 0

            compra.cantidad_items_esperados = int(total_ordenado)
            compra.cantidad_items_recibidos = int(total_recibido)
            if compra.fecha_primera_recepcion is None and total_recibido > 0:
                compra.fecha_primera_recepcion = datetime.utcnow()
            if total_recibido == 0:
                compra.estado_recepcion = "no_recibida"
            elif total_recibido >= total_ordenado:
                compra.estado_recepcion = "completa"
            else:
                compra.estado_recepcion = "parcial"

            # Verificar si todos los items están completamente recibidos usando los detalles de recepción
            todo_recibido = True
            algo_recibido = False
            for detalle_compra in detalles_compra:
                recibido_query = select(func.sum(RecepcionDetalle.cantidad_recibida)).where(
                    and_(
                        RecepcionDetalle.organization_id == org_id,
                        RecepcionDetalle.tipo_documento == "orden_compra",
                        RecepcionDetalle.documento_id == compra.id,
                        RecepcionDetalle.producto_id == detalle_compra.producto_id,
                        RecepcionDetalle.estado_recepcion.in_(["recibido", "dañado"])
                    )
                )
                recibido_result = await session.execute(recibido_query)
                total_recibido_producto = recibido_result.scalar() or 0

                if total_recibido_producto > 0:
                    algo_recibido = True
                if total_recibido_producto < detalle_compra.cantidad:
                    todo_recibido = False

            # Actualizar estado de la compra
            if todo_recibido:
                compra.estado = "recibido"
            elif algo_recibido:
                compra.estado = "recepcion_parcial"
    
    await session.commit()
    await session.refresh(new_movimiento)
    
    return {
        "success": True,
        "movimiento_id": new_movimiento.id,
        "message": f"Recepción registrada exitosamente. Estado: {new_movimiento.estado}"
    }
