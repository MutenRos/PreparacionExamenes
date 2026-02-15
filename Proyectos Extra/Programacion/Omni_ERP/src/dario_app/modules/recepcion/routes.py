"""Routes for purchase receipt and logistics management."""

from datetime import datetime
from typing import Optional, List
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from dario_app.database import get_db
from dario_app.core.auth import get_org_id, get_current_user_org
from dario_app.modules.recepcion.models import (
    Albaran,
    AlbaranDetalle,
    MovimientoLogistico,
    FacturaExterna,
    EstadoAlbaran,
    EstadoMovimiento,
    UbicacionAlmacen,
)
from dario_app.modules.compras.models import Compra, CompraDetalle
from dario_app.modules.inventario.models import Producto
from dario_app.modules.produccion_ordenes.models import OrdenProduccion
from dario_app.modules.usuarios.models import Usuario

router = APIRouter(prefix="/api/recepcion", tags=["recepcion"])


async def get_org_id_or_default(request: Request) -> int:
    """Obtiene org_id del token JWT si existe, o usa tenant 1 para vistas públicas."""
    ctx = await get_current_user_org(request)
    if ctx and ctx.get("org_id"):
        return ctx["org_id"]
    return 1


async def get_db_public(org_id: int = Depends(get_org_id_or_default)) -> AsyncSession:
    """Sesión en base de datos del tenant, permitiendo org 1 por defecto."""
    async for session in get_db(org_id):
        yield session


# ============================================================================
# SCHEMAS
# ============================================================================


class AlbaranDetalleRecibido(BaseModel):
    """Item received in a purchase order."""
    compra_detalle_id: int
    cantidad_recibida: int
    lotes_recibidos: Optional[str] = None
    fechas_vencimiento: Optional[str] = None
    notas: Optional[str] = None


class CrearAlbaranRequest(BaseModel):
    """Request to create receipt for a purchase order."""
    compra_id: int
    items_recibidos: List[AlbaranDetalleRecibido]
    usuario_id: Optional[int] = None
    notas: Optional[str] = None


class AlbaranDetalleResponse(BaseModel):
    """Response model for receipt items."""
    id: int
    producto_id: int
    producto_codigo: str | None = None
    producto_nombre: str | None = None
    cantidad_ordenada: int
    cantidad_recibida: int
    cantidad_diferencia: int
    lotes_recibidos: Optional[str] = None
    fechas_vencimiento: Optional[str] = None

    class Config:
        from_attributes = True


class AlbaranResponse(BaseModel):
    """Response model for receipt document."""
    id: int
    numero: str
    compra_id: int
    compra_numero: str | None = None
    proveedor_nombre: str | None = None
    total_compra: Decimal | None = None
    estado: str
    fecha_recepcion: datetime
    total_items: int
    items_recibidos: int
    items: List[AlbaranDetalleResponse] = []

    class Config:
        from_attributes = True


class MovimientoLogisticoResponse(BaseModel):
    """Response for logistics movement."""
    id: int
    numero: str
    producto_id: int
    cantidad: int
    ubicacion_origen: str
    ubicacion_destino: str
    estado: str
    orden_produccion_id: Optional[int] = None
    carretillero_id: Optional[int] = None

    class Config:
        from_attributes = True


class FacturaExternaResponse(BaseModel):
    """Response for external invoice."""
    id: int
    numero: str
    albaran_id: Optional[int] = None
    compra_id: int
    monto_total: Decimal
    estado_reconciliacion: str
    diferencia_cantidad: Optional[str] = None
    diferencia_precio: Optional[Decimal] = None

    class Config:
        from_attributes = True


# ============================================================================
# BUSINESS LOGIC HELPERS
# ============================================================================


async def _generar_numero_albaran(db: AsyncSession, org_id: int) -> str:
    """Generate unique receipt number."""
    result = await db.execute(
        select(func.count(Albaran.id)).where(Albaran.organization_id == org_id)
    )
    count = result.scalar() or 0
    return f"ALB-{org_id}-{datetime.utcnow().strftime('%Y%m%d')}-{count + 1:04d}"


async def _generar_numero_movimiento(db: AsyncSession, org_id: int) -> str:
    """Generate unique movement number."""
    result = await db.execute(
        select(func.count(MovimientoLogistico.id)).where(
            MovimientoLogistico.organization_id == org_id
        )
    )
    count = result.scalar() or 0
    return f"MOV-{org_id}-{datetime.utcnow().strftime('%Y%m%d')}-{count + 1:04d}"


async def _obtener_ordenes_produccion_activas(
    db: AsyncSession, org_id: int, producto_id: int
) -> List[OrdenProduccion]:
    """Get active production orders for a product."""
    result = await db.execute(
        select(OrdenProduccion).where(
            OrdenProduccion.organization_id == org_id,
            OrdenProduccion.producto_id == producto_id,
            OrdenProduccion.estado.in_(["pendiente_asignacion", "asignada", "aceptada", "en_proceso"]),
        )
    )
    return result.scalars().all()


async def _crear_movimientos_logisticos(
    db: AsyncSession,
    albaran_detalle_id: int,
    producto_id: int,
    cantidad: int,
    org_id: int,
    ordenes_produccion: List[OrdenProduccion],
    compra_id: int,
) -> List[MovimientoLogistico]:
    """Create logistics movements for received items.
    
    Strategy:
    1. If active production orders exist, allocate needed quantity to picking zone
    2. Remaining quantity goes to main storage
    3. Don't assign to specific warehouse worker yet
    """
    movimientos = []
    cantidad_restante = cantidad

    # First: Check if any production orders need this product
    if ordenes_produccion:
        for orden in ordenes_produccion:
            if cantidad_restante <= 0:
                break

            # Calculate needed quantity for this order
            cantidad_necesaria = int(orden.cantidad_ordenada - orden.cantidad_completada)
            if cantidad_necesaria > 0:
                cantidad_a_picking = min(cantidad_necesaria, cantidad_restante)

                # Create movement to picking zone
                mov_picking = MovimientoLogistico(
                    organization_id=org_id,
                    numero=await _generar_numero_movimiento(db, org_id),
                    albaran_detalle_id=albaran_detalle_id,
                    producto_id=producto_id,
                    orden_produccion_id=orden.id,
                    seccion_produccion=getattr(orden, 'seccion_asignada', None),
                    cantidad=cantidad_a_picking,
                    ubicacion_origen=UbicacionAlmacen.PLAYA_ENTRADA.value,
                    ubicacion_destino=UbicacionAlmacen.PICKING.value,
                    estado=EstadoMovimiento.PENDIENTE.value,
                )
                db.add(mov_picking)
                movimientos.append(mov_picking)
                cantidad_restante -= cantidad_a_picking

    # Second: Remaining quantity goes to main storage
    if cantidad_restante > 0:
        mov_almacen = MovimientoLogistico(
            organization_id=org_id,
            numero=await _generar_numero_movimiento(db, org_id),
            albaran_detalle_id=albaran_detalle_id,
            producto_id=producto_id,
            cantidad=cantidad_restante,
            ubicacion_origen=UbicacionAlmacen.PLAYA_ENTRADA.value,
            ubicacion_destino=UbicacionAlmacen.ALMACEN.value,
            estado=EstadoMovimiento.PENDIENTE.value,
        )
        db.add(mov_almacen)
        movimientos.append(mov_almacen)

    return movimientos


# ============================================================================
# ENDPOINTS
# ============================================================================


@router.post("/albaranes", response_model=AlbaranResponse, status_code=status.HTTP_201_CREATED)
async def crear_albaran(
    request: CrearAlbaranRequest,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db),
) -> AlbaranResponse:
    """
    Create receipt (albarán) for purchase order.
    
    - Generates internal receipt document
    - Adds items to inventory at entry dock
    - Creates logistics movements (to picking or storage)
    - Creates accounting record for later invoice reconciliation
    
    Returns the created receipt document.
    """
    # Validate purchase order exists and belongs to org
    result = await db.execute(
        select(Compra).where(
            Compra.id == request.compra_id,
            Compra.organization_id == org_id,
        )
    )
    compra = result.scalar_one_or_none()
    if not compra:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purchase order not found",
        )

    # Create receipt document
    numero_albaran = await _generar_numero_albaran(db, org_id)
    albaran = Albaran(
        organization_id=org_id,
        numero=numero_albaran,
        compra_id=request.compra_id,
        usuario_id=request.usuario_id,
        notas=request.notas,
        total_items=len(request.items_recibidos),
    )
    db.add(albaran)
    await db.flush()  # Get the ID without committing

    # Process each received item
    total_movimientos = 0
    for item_recibido in request.items_recibidos:
        # Get purchase detail and product
        result = await db.execute(
            select(CompraDetalle).where(
                CompraDetalle.id == item_recibido.compra_detalle_id,
                CompraDetalle.compra_id == request.compra_id,
            )
        )
        compra_detalle = result.scalar_one_or_none()
        if not compra_detalle:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Purchase detail {item_recibido.compra_detalle_id} not found",
            )

        # Get product
        result = await db.execute(
            select(Producto).where(
                Producto.id == compra_detalle.producto_id,
                Producto.organization_id == org_id,
            )
        )
        producto = result.scalar_one_or_none()
        if not producto:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product not found",
            )

        # Validate quantity
        if item_recibido.cantidad_recibida < 0:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Received quantity cannot be negative",
            )

        # Create receipt detail line
        cantidad_diferencia = compra_detalle.cantidad - item_recibido.cantidad_recibida
        albaran_detalle = AlbaranDetalle(
            albaran_id=albaran.id,
            compra_detalle_id=item_recibido.compra_detalle_id,
            producto_id=compra_detalle.producto_id,
            cantidad_ordenada=compra_detalle.cantidad,
            cantidad_recibida=item_recibido.cantidad_recibida,
            cantidad_diferencia=cantidad_diferencia,
            lotes_recibidos=item_recibido.lotes_recibidos,
            fechas_vencimiento=item_recibido.fechas_vencimiento,
            notas=item_recibido.notas,
        )
        db.add(albaran_detalle)
        await db.flush()

        # Update product inventory (add to entry dock location)
        producto.stock_actual += item_recibido.cantidad_recibida
        producto.ubicacion_almacen = UbicacionAlmacen.PLAYA_ENTRADA.value

        # Get active production orders for this product
        ordenes_activas = await _obtener_ordenes_produccion_activas(
            db, org_id, compra_detalle.producto_id
        )

        # Create logistics movements
        movimientos = await _crear_movimientos_logisticos(
            db=db,
            albaran_detalle_id=albaran_detalle.id,
            producto_id=compra_detalle.producto_id,
            cantidad=item_recibido.cantidad_recibida,
            org_id=org_id,
            ordenes_produccion=ordenes_activas,
            compra_id=request.compra_id,
        )
        total_movimientos += len(movimientos)

        albaran.items_recibidos += 1

    # Determine receipt status
    if albaran.items_recibidos == albaran.total_items:
        # Check if all quantities match
        diferencias = await db.execute(
            select(AlbaranDetalle).where(
                AlbaranDetalle.albaran_id == albaran.id,
                AlbaranDetalle.cantidad_diferencia != 0,
            )
        )
        if diferencias.scalars().all():
            albaran.estado = EstadoAlbaran.PARCIAL.value
        else:
            albaran.estado = EstadoAlbaran.COMPLETO.value
    else:
        albaran.estado = EstadoAlbaran.PARCIAL.value

    # ========================================================================
    # UPDATE PURCHASE ORDER STATUS (NUEVO)
    # ========================================================================
    
    # Get total items ordered for this purchase
    result = await db.execute(
        select(func.sum(CompraDetalle.cantidad)).where(
            CompraDetalle.compra_id == request.compra_id
        )
    )
    total_ordenado = result.scalar() or 0
    
    # Get total items already received for this purchase
    result = await db.execute(
        select(func.sum(AlbaranDetalle.cantidad_recibida)).where(
            AlbaranDetalle.albaran_id.in_(
                select(Albaran.id).where(Albaran.compra_id == request.compra_id)
            )
        )
    )
    total_recibido = result.scalar() or 0
    
    # Update purchase order state
    compra.cantidad_items_esperados = int(total_ordenado)
    compra.cantidad_items_recibidos = int(total_recibido)
    
    if compra.fecha_primera_recepcion is None:
        compra.fecha_primera_recepcion = datetime.utcnow()
    
    if total_recibido == 0:
        compra.estado_recepcion = "no_recibida"
    elif total_recibido >= total_ordenado:
        compra.estado_recepcion = "completa"
    else:
        compra.estado_recepcion = "parcial"

    await db.commit()
    await db.refresh(albaran)
    await db.refresh(compra)

    return AlbaranResponse(
        id=albaran.id,
        numero=albaran.numero,
        compra_id=albaran.compra_id,
        estado=albaran.estado,
        fecha_recepcion=albaran.fecha_recepcion,
        total_items=albaran.total_items,
        items_recibidos=albaran.items_recibidos,
    )


@router.get("/albaranes", response_model=List[AlbaranResponse])
async def listar_albaranes(
    org_id: int = Depends(get_org_id_or_default),
    db: AsyncSession = Depends(get_db_public),
) -> List[AlbaranResponse]:
    """List all receipt documents for the organization."""
    result = await db.execute(
        select(Albaran).where(
            Albaran.organization_id == org_id
        ).order_by(Albaran.fecha_recepcion.desc())
    )
    albaranes = result.scalars().all()
    
    respuestas = []
    for albaran in albaranes:
        # Get details with product info
        result = await db.execute(
            select(AlbaranDetalle, Producto)
            .outerjoin(Producto, Producto.id == AlbaranDetalle.producto_id)
            .where(AlbaranDetalle.albaran_id == albaran.id)
        )
        detalles_con_producto = result.all()

        # Fetch purchase info to enrich response
        compra_info = None
        if albaran.compra_id:
            result_compra = await db.execute(
                select(Compra).where(Compra.id == albaran.compra_id)
            )
            compra_info = result_compra.scalar_one_or_none()
        
        respuestas.append(AlbaranResponse(
            id=albaran.id,
            numero=albaran.numero,
            compra_id=albaran.compra_id,
            compra_numero=getattr(compra_info, "numero", None),
            proveedor_nombre=getattr(compra_info, "proveedor_nombre", None),
            total_compra=getattr(compra_info, "total", None),
            estado=albaran.estado,
            fecha_recepcion=albaran.fecha_recepcion,
            total_items=albaran.total_items,
            items_recibidos=albaran.items_recibidos,
            items=[
                AlbaranDetalleResponse(
                    id=d[0].id,
                    producto_id=d[0].producto_id,
                    producto_codigo=d[1].codigo if d[1] else None,
                    producto_nombre=d[1].nombre if d[1] else None,
                    cantidad_ordenada=d[0].cantidad_ordenada,
                    cantidad_recibida=d[0].cantidad_recibida,
                    cantidad_diferencia=d[0].cantidad_diferencia,
                )
                for d in detalles_con_producto
            ],
        ))
    
    return respuestas


@router.get("/albaranes/{albaran_id}", response_model=AlbaranResponse)
async def obtener_albaran(
    albaran_id: int,
    org_id: int = Depends(get_org_id_or_default),
    db: AsyncSession = Depends(get_db_public),
) -> AlbaranResponse:
    """Get receipt document details."""
    result = await db.execute(
        select(Albaran).where(
            Albaran.id == albaran_id,
            Albaran.organization_id == org_id,
        )
    )
    albaran = result.scalar_one_or_none()
    if not albaran:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receipt not found",
        )

    # Get details
    result = await db.execute(
        select(AlbaranDetalle, Producto)
        .outerjoin(Producto, Producto.id == AlbaranDetalle.producto_id)
        .where(AlbaranDetalle.albaran_id == albaran_id)
    )
    detalles_con_producto = result.all()

    # Purchase info
    compra_info = None
    if albaran.compra_id:
        result_compra = await db.execute(
            select(Compra).where(Compra.id == albaran.compra_id)
        )
        compra_info = result_compra.scalar_one_or_none()

    return AlbaranResponse(
        id=albaran.id,
        numero=albaran.numero,
        compra_id=albaran.compra_id,
        compra_numero=getattr(compra_info, "numero", None),
        proveedor_nombre=getattr(compra_info, "proveedor_nombre", None),
        total_compra=getattr(compra_info, "total", None),
        estado=albaran.estado,
        fecha_recepcion=albaran.fecha_recepcion,
        total_items=albaran.total_items,
        items_recibidos=albaran.items_recibidos,
        items=[
            AlbaranDetalleResponse(
                id=d[0].id,
                producto_id=d[0].producto_id,
                producto_codigo=d[1].codigo if d[1] else None,
                producto_nombre=d[1].nombre if d[1] else None,
                cantidad_ordenada=d[0].cantidad_ordenada,
                cantidad_recibida=d[0].cantidad_recibida,
                cantidad_diferencia=d[0].cantidad_diferencia,
                lotes_recibidos=d[0].lotes_recibidos,
                fechas_vencimiento=d[0].fechas_vencimiento,
            )
            for d in detalles_con_producto
        ],
    )


@router.get("/movimientos", response_model=List[MovimientoLogisticoResponse])
async def listar_movimientos(
    estado: Optional[str] = None,
    ubicacion_destino: Optional[str] = None,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db),
) -> List[MovimientoLogisticoResponse]:
    """
    List logistics movements.
    
    Filter by:
    - estado: Movement status (pendiente, en_transito, en_picking, completado)
    - ubicacion_destino: Destination (playa_entrada, picking, almacen)
    """
    query = select(MovimientoLogistico).where(MovimientoLogistico.organization_id == org_id)

    if estado:
        query = query.where(MovimientoLogistico.estado == estado)

    if ubicacion_destino:
        query = query.where(MovimientoLogistico.ubicacion_destino == ubicacion_destino)

    result = await db.execute(query)
    movimientos = result.scalars().all()

    return [
        MovimientoLogisticoResponse(
            id=m.id,
            numero=m.numero,
            producto_id=m.producto_id,
            cantidad=m.cantidad,
            ubicacion_origen=m.ubicacion_origen,
            ubicacion_destino=m.ubicacion_destino,
            estado=m.estado,
            orden_produccion_id=m.orden_produccion_id,
            carretillero_id=m.carretillero_id,
        )
        for m in movimientos
    ]


@router.post("/movimientos/{movimiento_id}/asignar-carretillero")
async def asignar_carretillero_a_movimiento(
    movimiento_id: int,
    carretillero_id: int,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db),
) -> MovimientoLogisticoResponse:
    """Assign warehouse worker to a movement."""
    # Get movement
    result = await db.execute(
        select(MovimientoLogistico).where(
            MovimientoLogistico.id == movimiento_id,
            MovimientoLogistico.organization_id == org_id,
        )
    )
    movimiento = result.scalar_one_or_none()
    if not movimiento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movement not found",
        )

    # Verify worker exists
    result = await db.execute(select(Usuario).where(Usuario.id == carretillero_id))
    if not result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Worker not found",
        )

    # Update movement
    movimiento.carretillero_id = carretillero_id
    movimiento.estado = EstadoMovimiento.EN_TRANSITO.value
    movimiento.fecha_inicio = datetime.utcnow()

    await db.commit()
    await db.refresh(movimiento)

    return MovimientoLogisticoResponse(
        id=movimiento.id,
        numero=movimiento.numero,
        producto_id=movimiento.producto_id,
        cantidad=movimiento.cantidad,
        ubicacion_origen=movimiento.ubicacion_origen,
        ubicacion_destino=movimiento.ubicacion_destino,
        estado=movimiento.estado,
        orden_produccion_id=movimiento.orden_produccion_id,
        carretillero_id=movimiento.carretillero_id,
    )


@router.post("/movimientos/{movimiento_id}/completar")
async def completar_movimiento(
    movimiento_id: int,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db),
) -> MovimientoLogisticoResponse:
    """Mark movement as completed."""
    result = await db.execute(
        select(MovimientoLogistico).where(
            MovimientoLogistico.id == movimiento_id,
            MovimientoLogistico.organization_id == org_id,
        )
    )
    movimiento = result.scalar_one_or_none()
    if not movimiento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movement not found",
        )

    movimiento.estado = EstadoMovimiento.COMPLETADO.value
    movimiento.fecha_completado = datetime.utcnow()

    await db.commit()
    await db.refresh(movimiento)

    return MovimientoLogisticoResponse(
        id=movimiento.id,
        numero=movimiento.numero,
        producto_id=movimiento.producto_id,
        cantidad=movimiento.cantidad,
        ubicacion_origen=movimiento.ubicacion_origen,
        ubicacion_destino=movimiento.ubicacion_destino,
        estado=movimiento.estado,
        orden_produccion_id=movimiento.orden_produccion_id,
        carretillero_id=movimiento.carretillero_id,
    )


@router.post("/albaranes/{albaran_id}/reconciliar-factura")
async def reconciliar_con_factura_externa(
    albaran_id: int,
    numero_factura: str,
    monto_factura: Decimal,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db),
) -> AlbaranResponse:
    """
    Reconcile receipt with external invoice.
    
    Called from accounting module when supplier invoice arrives.
    Compares quantities and amounts.
    """
    result = await db.execute(
        select(Albaran).where(
            Albaran.id == albaran_id,
            Albaran.organization_id == org_id,
        )
    )
    albaran = result.scalar_one_or_none()
    if not albaran:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receipt not found",
        )

    # Update receipt with external invoice info
    albaran.numero_factura_externa = numero_factura
    albaran.fecha_factura_externa = datetime.utcnow()
    albaran.estado = EstadoAlbaran.VERIFICADO.value

    # Check for discrepancies
    result = await db.execute(
        select(AlbaranDetalle).where(
            AlbaranDetalle.albaran_id == albaran_id,
            AlbaranDetalle.cantidad_diferencia != 0,
        )
    )
    diferencias = result.scalars().all()
    if diferencias:
        albaran.diferencias_observadas = f"{len(diferencias)} items with quantity differences"

    await db.commit()
    await db.refresh(albaran)

    return AlbaranResponse(
        id=albaran.id,
        numero=albaran.numero,
        compra_id=albaran.compra_id,
        estado=albaran.estado,
        fecha_recepcion=albaran.fecha_recepcion,
        total_items=albaran.total_items,
        items_recibidos=albaran.items_recibidos,
    )


@router.get("/reportes/pendientes-asignacion")
async def listar_movimientos_pendientes_asignacion(
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db),
):
    """Get movements pending warehouse worker assignment."""
    result = await db.execute(
        select(MovimientoLogistico).where(
            MovimientoLogistico.organization_id == org_id,
            MovimientoLogistico.estado == EstadoMovimiento.PENDIENTE.value,
            MovimientoLogistico.carretillero_id.is_(None),
        )
    )
    movimientos = result.scalars().all()

    return {
        "total": len(movimientos),
        "movimientos": [
            MovimientoLogisticoResponse(
                id=m.id,
                numero=m.numero,
                producto_id=m.producto_id,
                cantidad=m.cantidad,
                ubicacion_origen=m.ubicacion_origen,
                ubicacion_destino=m.ubicacion_destino,
                estado=m.estado,
                orden_produccion_id=m.orden_produccion_id,
                carretillero_id=m.carretillero_id,
            )
            for m in movimientos
        ],
    }


# ============================================================================
# NUEVOS ENDPOINTS PARA SEGUIMIENTO DE COMPRAS
# ============================================================================


class CompraConEstadoRecepcion(BaseModel):
    """Purchase order with reception status."""
    id: int
    numero: str
    proveedor_nombre: str
    estado_recepcion: str  # no_recibida, parcial, completa
    cantidad_items_esperados: int
    cantidad_items_recibidos: int
    porcentaje_recibido: float
    fecha_primera_recepcion: Optional[datetime] = None
    total: Decimal

    class Config:
        from_attributes = True


@router.get("/api/recepcion/compras/pendientes", response_model=List[CompraConEstadoRecepcion])
async def listar_compras_pendientes_recepcion(
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db),
) -> List[CompraConEstadoRecepcion]:
    """
    List purchase orders that are NOT fully received.
    
    Shows:
    - Completely unreceived (no_recibida)
    - Partially received (parcial)
    - Qty received vs qty expected
    - Percentage progress
    
    Perfect for the reception dashboard.
    """
    result = await db.execute(
        select(Compra).where(
            Compra.organization_id == org_id,
            Compra.estado_recepcion.in_(["no_recibida", "parcial"]),
        ).order_by(Compra.fecha.desc())
    )
    compras = result.scalars().all()
    
    respuesta = []
    for compra in compras:
        porcentaje = 0.0
        if compra.cantidad_items_esperados > 0:
            porcentaje = (compra.cantidad_items_recibidos / compra.cantidad_items_esperados) * 100
        
        respuesta.append(CompraConEstadoRecepcion(
            id=compra.id,
            numero=compra.numero,
            proveedor_nombre=compra.proveedor_nombre,
            estado_recepcion=compra.estado_recepcion,
            cantidad_items_esperados=compra.cantidad_items_esperados,
            cantidad_items_recibidos=compra.cantidad_items_recibidos,
            porcentaje_recibido=porcentaje,
            fecha_primera_recepcion=compra.fecha_primera_recepcion,
            total=compra.total,
        ))
    
    return respuesta


@router.get("/api/recepcion/compras/{compra_id}/estado")
async def obtener_estado_recepcion_compra(
    compra_id: int,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_db),
):
    """Get detailed reception status for a purchase order."""
    result = await db.execute(
        select(Compra).where(
            Compra.id == compra_id,
            Compra.organization_id == org_id,
        )
    )
    compra = result.scalar_one_or_none()
    if not compra:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purchase order not found",
        )
    
    porcentaje = 0.0
    if compra.cantidad_items_esperados > 0:
        porcentaje = (compra.cantidad_items_recibidos / compra.cantidad_items_esperados) * 100
    
    # Get all receipts for this purchase
    result = await db.execute(
        select(Albaran).where(
            Albaran.compra_id == compra_id,
        ).order_by(Albaran.fecha_recepcion.desc())
    )
    albaranes = result.scalars().all()
    
    return {
        "compra_id": compra.id,
        "numero": compra.numero,
        "proveedor": compra.proveedor_nombre,
        "estado_recepcion": compra.estado_recepcion,
        "cantidad_esperada": compra.cantidad_items_esperados,
        "cantidad_recibida": compra.cantidad_items_recibidos,
        "cantidad_pendiente": compra.cantidad_items_esperados - compra.cantidad_items_recibidos,
        "porcentaje_recibido": porcentaje,
        "fecha_primera_recepcion": compra.fecha_primera_recepcion,
        "albaranes": [
            {
                "numero": a.numero,
                "fecha": a.fecha_recepcion,
                "estado": a.estado,
                "items": a.items_recibidos,
            }
            for a in albaranes
        ],
    }

