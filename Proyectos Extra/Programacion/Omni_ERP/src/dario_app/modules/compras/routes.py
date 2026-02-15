"""Compras API routes."""

from datetime import datetime
from decimal import Decimal
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, field_validator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import get_org_id, get_tenant_db
from dario_app.modules.inventario.models import Producto, Proveedor
from dario_app.modules.tenants.models import Organization
from dario_app.modules.produccion_ordenes.models import MovimientoAlmacen, OrdenProduccion, SeccionProduccion

from .models import Compra, CompraDetalle

router = APIRouter(prefix="/api/compras", tags=["compras"])
templates = Jinja2Templates(directory="/home/dario/src/dario_app/templates")


class CompraDetalleCreate(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: Decimal

    @field_validator("cantidad")
    @classmethod
    def validate_cantidad(cls, v):
        if v <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        return v

    @field_validator("precio_unitario")
    @classmethod
    def validate_precio(cls, v):
        if v < 0:
            raise ValueError("El precio no puede ser negativo")
        return v


class CompraCreate(BaseModel):
    numero: str
    proveedor_nombre: str
    proveedor_documento: str | None = None
    detalles: List[CompraDetalleCreate]
    notas: str | None = None


class CompraDetalleResponse(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal

    class Config:
        from_attributes = True


class OrdenProduccionInfo(BaseModel):
    op_id: int
    op_numero: str
    cantidad_op: int
    producto_id: int
    producto_nombre: str
    stock_disponible: int
    material_faltante: bool
    tiene_solicitud_material: bool


class CompraDetalleExtendedResponse(BaseModel):
    id: int
    producto_id: int
    producto_codigo: str
    producto_nombre: str
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal
    ordenes_produccion: List[OrdenProduccionInfo] = []

    class Config:
        from_attributes = True


class CompraResponse(BaseModel):
    id: int
    numero: str
    fecha: datetime
    proveedor_nombre: str
    proveedor_documento: str | None
    total: Decimal
    estado: str
    estado_recepcion: str | None = None
    cantidad_items_esperados: int | None = None
    cantidad_items_recibidos: int | None = None
    notas: str | None

    class Config:
        from_attributes = True


class AutoCompraStockBajoRequest(BaseModel):
    reset_stock: bool = False
    proveedor_nombre: str | None = "Proveedor Automático"
    notas: str | None = "Generado automáticamente por stock bajo"
    incluir_necesidades_op: bool = True

class AutoCompraItem(BaseModel):
    producto_id: int
    nombre: str
    faltante: int
    precio_unitario: Decimal

class AutoCompraResponse(BaseModel):
    numero: str
    total: Decimal
    cantidad_items: int
    items: List[AutoCompraItem]


# Helper function for auto-generating purchase orders
async def _generar_compra_automatica(
    org_id: int,
    db: AsyncSession,
    reset_stock: bool = False,
    incluir_necesidades_op: bool = True,
    proveedor_nombre: str | None = None,
    notas: str | None = None,
) -> AutoCompraResponse | None:
    """
    Helper function to auto-generate a purchase order for products below minimum stock.
    Used by both the manual endpoint and automatic triggers.
    Returns AutoCompraResponse if purchase was created, None if no items to purchase.
    """
    # Reset stock si se solicita
    if reset_stock:
        result = await db.execute(select(Producto).where(Producto.organization_id == org_id))
        for producto in result.scalars().all():
            producto.stock_actual = 0
        await db.flush()

    # Buscar productos en bajo stock
    result = await db.execute(
        select(Producto).where(
            Producto.organization_id == org_id,
            Producto.stock_actual < Producto.stock_minimo,
        )
    )
    productos_bajo = result.scalars().all()

    # Map de faltantes base
    faltantes_map: dict[int, int] = {}
    for p in productos_bajo:
        faltantes_map[p.id] = max(p.stock_minimo - p.stock_actual, 0)

    # Incluir necesidades de OP abiertas (BOM)
    if incluir_necesidades_op:
        from sqlalchemy import text
        # Ordenes abiertas
        q_op = text(
            """
            SELECT bom_id, cantidad_ordenada
            FROM ordenes_produccion
            WHERE organization_id = :org AND estado NOT IN ('completada','cancelada')
            """
        )
        op_rows = (await db.execute(q_op.bindparams(org=org_id))).mappings().all()
        bom_ids = {r["bom_id"] for r in op_rows if r["bom_id"]}
        if bom_ids:
            # Use SQLAlchemy select for proper IN clause handling
            from dario_app.modules.oficina_tecnica.models import BOMLine
            result = await db.execute(
                select(BOMLine).where(
                    BOMLine.organization_id == org_id,
                    BOMLine.bom_header_id.in_(bom_ids)
                )
            )
            bom_rows = result.scalars().all()
            # Group components by bom
            comps_by_bom: dict[int, list] = {}
            for row in bom_rows:
                if row.bom_header_id not in comps_by_bom:
                    comps_by_bom[row.bom_header_id] = []
                comps_by_bom[row.bom_header_id].append(row)
            # Sum needs
            for op in op_rows:
                bom_id = op["bom_id"]
                qty = int(op["cantidad_ordenada"] or 0)
                for comp in comps_by_bom.get(bom_id, []):
                    pid = comp.componente_id
                    req_qty = int(comp.cantidad or 0) * qty
                    faltantes_map[pid] = faltantes_map.get(pid, 0) + req_qty

    if not faltantes_map:
        return None  # No items to purchase

    # Generar número de compra
    count_result = await db.execute(select(Compra).where(Compra.organization_id == org_id))
    count = len(count_result.scalars().all()) + 1
    numero = f"PO-AUTO-{count:05d}"

    items: List[AutoCompraItem] = []
    total = Decimal("0")

    # Crear compra
    compra = Compra(
        numero=numero,
        proveedor_nombre=proveedor_nombre or "Proveedor Automático",
        total=Decimal("0"),
        notas=notas,
        organization_id=org_id,
    )
    db.add(compra)
    await db.flush()

    # Crear detalles
    ids = list(faltantes_map.keys())
    if ids:
        result = await db.execute(select(Producto).where(Producto.id.in_(ids)))
        productos_ref = {p.id: p for p in result.scalars().all()}
    else:
        productos_ref = {}

    for pid, faltante in faltantes_map.items():
        if faltante <= 0:
            continue
        p = productos_ref.get(pid)
        precio_unitario = Decimal(str((p.precio_compra if p else 0) or 0))
        subtotal = Decimal(faltante) * precio_unitario
        total += subtotal

        detalle = CompraDetalle(
            compra_id=compra.id,
            producto_id=pid,
            cantidad=faltante,
            precio_unitario=precio_unitario,
            subtotal=subtotal,
        )
        db.add(detalle)

        items.append(
            AutoCompraItem(
                producto_id=pid,
                nombre=(p.nombre if p else f"Producto {pid}"),
                faltante=faltante,
                precio_unitario=precio_unitario,
            )
        )

    compra.total = total
    await db.commit()
    await db.refresh(compra)

    return AutoCompraResponse(
        numero=compra.numero,
        total=compra.total,
        cantidad_items=len(items),
        items=items,
    )


@router.post("/auto-por-stock-bajo", response_model=AutoCompraResponse)
async def generar_compra_por_stock_bajo(
    req: AutoCompraStockBajoRequest,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Genera una compra con todos los productos cuyo stock_actual < stock_minimo.
    Opcionalmente resetea stocks a 0 antes de calcular.
    """
    result = await _generar_compra_automatica(
        org_id=org_id,
        db=db,
        reset_stock=req.reset_stock,
        incluir_necesidades_op=req.incluir_necesidades_op,
        proveedor_nombre=req.proveedor_nombre,
        notas=req.notas,
    )
    
    if result is None:
        raise HTTPException(status_code=400, detail="No hay faltantes para generar compra")
    
    return result


# NOTE: Endpoint de debug sin autenticación eliminado para evitar fugas entre tenants.


@router.get("/", response_model=List[CompraResponse])
async def list_compras(
    org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)
):
    """List all purchases."""
    result = await db.execute(select(Compra).where(Compra.organization_id == org_id))
    return result.scalars().all()


@router.get("/historico", response_model=List[CompraResponse])
async def historico_compras(
    org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)
):
    """List all approved purchases for historical view."""
    result = await db.execute(
        select(Compra).where(
            Compra.organization_id == org_id,
            Compra.estado == 'aprobada'
        ).order_by(Compra.fecha.desc())
    )
    return result.scalars().all()


@router.post("/", response_model=CompraResponse, status_code=status.HTTP_201_CREATED)
async def create_compra(
    compra: CompraCreate,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Create a new purchase."""
    # Validar que todos los productos existan
    for detalle in compra.detalles:
        result = await db.execute(
            select(Producto).where(
                Producto.id == detalle.producto_id, Producto.organization_id == org_id
            )
        )
        producto = result.scalar_one_or_none()
        if not producto:
            raise HTTPException(
                status_code=404, detail=f"Producto {detalle.producto_id} no encontrado"
            )

    total = sum(d.cantidad * d.precio_unitario for d in compra.detalles)

    db_compra = Compra(
        numero=compra.numero,
        proveedor_nombre=compra.proveedor_nombre,
        proveedor_documento=compra.proveedor_documento,
        total=total,
        notas=compra.notas,
        organization_id=org_id,
    )
    db.add(db_compra)
    await db.flush()

    # Crear detalles y actualizar stock
    for detalle in compra.detalles:
        db_detalle = CompraDetalle(
            compra_id=db_compra.id,
            producto_id=detalle.producto_id,
            cantidad=detalle.cantidad,
            precio_unitario=detalle.precio_unitario,
            subtotal=detalle.cantidad * detalle.precio_unitario,
        )
        db.add(db_detalle)

        # Actualizar stock del producto (incrementar en compras)
        result = await db.execute(select(Producto).where(Producto.id == detalle.producto_id))
        producto = result.scalar_one()
        producto.stock_actual += detalle.cantidad

    await db.commit()
    await db.refresh(db_compra)
    return db_compra


@router.get("/{compra_id}", response_model=CompraResponse)
async def get_compra(
    compra_id: int, org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)
):
    """Get a purchase by ID."""
    result = await db.execute(
        select(Compra).where(Compra.id == compra_id, Compra.organization_id == org_id)
    )
    compra = result.scalar_one_or_none()
    if not compra:
        raise HTTPException(status_code=404, detail="Compra no encontrada")
    return compra


# Printable: Pedido de Compra
@router.get("/{compra_id}/print")
async def print_pedido_compra(
    compra_id: int,
    request: Request,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Renderiza un HTML imprimible para el pedido de compra."""
    # Compra
    result = await db.execute(
        select(Compra).where(Compra.id == compra_id, Compra.organization_id == org_id)
    )
    compra = result.scalar_one_or_none()
    if not compra:
        raise HTTPException(status_code=404, detail="Compra no encontrada")

    # Detalles + Productos
    result = await db.execute(
        select(CompraDetalle, Producto)
        .join(Producto, Producto.id == CompraDetalle.producto_id)
        .where(CompraDetalle.compra_id == compra_id)
    )
    rows = result.all()

    # Org
    org = None
    try:
        org_res = await db.execute(select(Organization).where(Organization.id == org_id))
        org = org_res.scalar_one_or_none()
    except Exception:
        org = None

    context = {
        "request": request,
        "compra": compra,
        "items": rows,
        "org": org,
    }
    return templates.TemplateResponse("print/pedido_compra.html", context)


# ================== APROBACIÓN Y EDICIÓN DE COMPRAS ==================
class CompraUpdate(BaseModel):
    proveedor_nombre: str | None = None
    proveedor_documento: str | None = None
    notas: str | None = None


class CompraDetalleUpdate(BaseModel):
    cantidad: int | None = None
    precio_unitario: Decimal | None = None


@router.get("/{compra_id}/detalles", response_model=List[CompraDetalleExtendedResponse])
async def list_detalles(
    compra_id: int, org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)
):
    """Lista los detalles de una compra con info de OPs y materiales faltantes."""
    from sqlalchemy import text
    
    result = await db.execute(
        select(Compra).where(Compra.id == compra_id, Compra.organization_id == org_id)
    )
    compra = result.scalar_one_or_none()
    if not compra:
        raise HTTPException(status_code=404, detail="Compra no encontrada")

    # Obtener detalles con información de productos
    result = await db.execute(
        select(CompraDetalle, Producto)
        .join(Producto, Producto.id == CompraDetalle.producto_id)
        .where(CompraDetalle.compra_id == compra_id)
    )
    detalles_con_producto = result.all()
    
    if not detalles_con_producto:
        return []
    
    # Obtener órdenes de producción con necesidades
    q_op = text("""
        SELECT op.id, op.numero, op.bom_id, bl.componente_id, op.cantidad_ordenada
        FROM ordenes_produccion op
        LEFT JOIN bom_lines bl ON bl.bom_header_id = op.bom_id
        WHERE op.organization_id = :org AND op.estado NOT IN ('completada', 'cancelada')
    """)
    op_rows = (await db.execute(q_op.bindparams(org=org_id))).mappings().all()
    
    # Mapear productos a órdenes
    producto_a_ordenes = {}
    for row in op_rows:
        if row["componente_id"]:
            if row["componente_id"] not in producto_a_ordenes:
                producto_a_ordenes[row["componente_id"]] = []
            producto_a_ordenes[row["componente_id"]].append({
                "op_id": row["id"],
                "op_numero": row["numero"],
                "cantidad_op": row["cantidad_ordenada"]
            })
    
    # Obtener stock actual
    result_stock = await db.execute(
        select(Producto.id, Producto.stock_actual).where(Producto.organization_id == org_id)
    )
    stock_map = {row[0]: row[1] for row in result_stock}
    
    # Obtener solicitudes pendientes
    q_solicitudes = text("""
        SELECT DISTINCT op.id
        FROM solicitudes_material_produccion smp
        JOIN ordenes_produccion op ON op.id = smp.orden_produccion_id
        WHERE smp.organization_id = :org AND smp.estado IN ('pendiente', 'en_proceso')
    """)
    solicitudes_op_ids = set()
    for row in await db.execute(q_solicitudes.bindparams(org=org_id)):
        solicitudes_op_ids.add(row[0])
    
    # Construir respuesta
    result_list = []
    for detalle, producto in detalles_con_producto:
        ordenes_info = []
        
        if detalle.producto_id in producto_a_ordenes:
            for op_info in producto_a_ordenes[detalle.producto_id]:
                stock_disponible = stock_map.get(detalle.producto_id, 0)
                material_faltante = stock_disponible < int(op_info["cantidad_op"] or 0)
                
                ordenes_info.append(
                    OrdenProduccionInfo(
                        op_id=op_info["op_id"],
                        op_numero=op_info["op_numero"],
                        cantidad_op=op_info["cantidad_op"],
                        producto_id=detalle.producto_id,
                        producto_nombre=producto.nombre,
                        stock_disponible=stock_disponible,
                        material_faltante=material_faltante,
                        tiene_solicitud_material=op_info["op_id"] in solicitudes_op_ids
                    )
                )
        
        result_list.append(
            CompraDetalleExtendedResponse(
                id=detalle.id,
                producto_id=detalle.producto_id,
                producto_codigo=producto.codigo if hasattr(producto, 'codigo') else f"PROD-{producto.id}",
                producto_nombre=producto.nombre,
                cantidad=detalle.cantidad,
                precio_unitario=detalle.precio_unitario,
                subtotal=detalle.subtotal,
                ordenes_produccion=ordenes_info
            )
        )
    
    return result_list


@router.put("/{compra_id}", response_model=CompraResponse)
async def update_compra_header(
    compra_id: int,
    data: CompraUpdate,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Actualiza datos de cabecera de la compra. Solo permitido si estado = 'pendiente'."""
    result = await db.execute(
        select(Compra).where(Compra.id == compra_id, Compra.organization_id == org_id)
    )
    compra = result.scalar_one_or_none()
    if not compra:
        raise HTTPException(status_code=404, detail="Compra no encontrada")
    if compra.estado != "pendiente":
        raise HTTPException(status_code=400, detail="La compra ya fue aprobada y no puede editarse")

    if data.proveedor_nombre is not None:
        compra.proveedor_nombre = data.proveedor_nombre
    if data.proveedor_documento is not None:
        compra.proveedor_documento = data.proveedor_documento
    if data.notas is not None:
        compra.notas = data.notas

    await db.commit()
    await db.refresh(compra)
    return compra


@router.put("/{compra_id}/detalles/{detalle_id}", response_model=CompraDetalleResponse)
async def update_compra_detalle(
    compra_id: int,
    detalle_id: int,
    data: CompraDetalleUpdate,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Edita cantidad/precio del detalle en compras pendientes. Recalcula subtotal y total."""
    # Validar compra
    result = await db.execute(
        select(Compra).where(Compra.id == compra_id, Compra.organization_id == org_id)
    )
    compra = result.scalar_one_or_none()
    if not compra:
        raise HTTPException(status_code=404, detail="Compra no encontrada")
    if compra.estado != "pendiente":
        raise HTTPException(status_code=400, detail="La compra ya fue aprobada y no puede editarse")

    # Obtener detalle
    result = await db.execute(
        select(CompraDetalle).where(CompraDetalle.id == detalle_id, CompraDetalle.compra_id == compra_id)
    )
    detalle = result.scalar_one_or_none()
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")

    if data.cantidad is not None:
        if data.cantidad <= 0:
            raise HTTPException(status_code=400, detail="La cantidad debe ser mayor a 0")
        detalle.cantidad = int(data.cantidad)
    if data.precio_unitario is not None:
        if data.precio_unitario < 0:
            raise HTTPException(status_code=400, detail="El precio no puede ser negativo")
        detalle.precio_unitario = Decimal(str(data.precio_unitario))

    # Recalcular subtotal y total
    detalle.subtotal = Decimal(detalle.cantidad) * Decimal(detalle.precio_unitario)

    # Recalcular total de compra sumando todos los detalles
    result = await db.execute(select(CompraDetalle).where(CompraDetalle.compra_id == compra_id))
    detalles = result.scalars().all()
    compra.total = sum(Decimal(d.subtotal) for d in detalles)

    await db.commit()
    await db.refresh(detalle)
    return detalle


class AprobarCompraResponse(BaseModel):
    id: int
    numero: str
    estado: str
    total: Decimal


@router.post("/{compra_id}/aprobar", response_model=AprobarCompraResponse)
async def aprobar_compra(
    compra_id: int,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Aprueba la compra pendiente. El encargado confirma y no se permiten más ediciones."""
    result = await db.execute(
        select(Compra).where(Compra.id == compra_id, Compra.organization_id == org_id)
    )
    compra = result.scalar_one_or_none()
    if not compra:
        raise HTTPException(status_code=404, detail="Compra no encontrada")
    if compra.estado != "pendiente":
        raise HTTPException(status_code=400, detail="La compra ya fue aprobada")

    compra.estado = "aprobada"
    await db.commit()
    await db.refresh(compra)
    return AprobarCompraResponse(id=compra.id, numero=compra.numero, estado=compra.estado, total=compra.total)


# ============ RECEPCIÓN DE COMPRAS ============
class RecepcionItem(BaseModel):
    detalle_id: int
    cantidad_recibida: int
    orden_produccion_id: int | None = None
    destino: str | None = "almacen"  # 'picking' | 'almacen'

class RecepcionCompraRequest(BaseModel):
    items: List[RecepcionItem]
    notas: str | None = None

class RecepcionCompraResponse(BaseModel):
    compra_id: int
    estado_recepcion: str
    cantidad_items_recibidos: int
    mensaje: str

@router.post("/{compra_id}/recibir", response_model=RecepcionCompraResponse)
async def recibir_compra(
    compra_id: int,
    payload: RecepcionCompraRequest,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Registra recepción de compra: actualiza inventario y marcadores de recepción.

    Nota: Los movimientos a picking/almacén específicos de producción requieren contexto de orden,
    que no está disponible para compras generales. Aquí se actualiza el stock y el estado de recepción.
    """
    # Validar compra
    result = await db.execute(select(Compra).where(Compra.id == compra_id, Compra.organization_id == org_id))
    compra = result.scalar_one_or_none()
    if not compra:
        raise HTTPException(status_code=404, detail="Compra no encontrada")
    if compra.estado not in ("pendiente", "aprobada"):
        raise HTTPException(status_code=400, detail="La compra no está en estado recepcionable")

    # Obtener detalles de la compra
    result = await db.execute(select(CompraDetalle).where(CompraDetalle.compra_id == compra_id))
    detalles = {d.id: d for d in result.scalars().all()}
    if not detalles:
        raise HTTPException(status_code=400, detail="La compra no tiene detalles")

    recibidos_total = 0
    for item in payload.items:
        detalle = detalles.get(item.detalle_id)
        if not detalle:
            raise HTTPException(status_code=404, detail=f"Detalle {item.detalle_id} no encontrado")
        if item.cantidad_recibida <= 0:
            raise HTTPException(status_code=400, detail="Cantidad recibida debe ser > 0")

        # Actualizar stock del producto
        prod_res = await db.execute(select(Producto).where(Producto.id == detalle.producto_id, Producto.organization_id == org_id))
        producto = prod_res.scalar_one_or_none()
        if not producto:
            raise HTTPException(status_code=404, detail=f"Producto {detalle.producto_id} no encontrado")
        producto.stock_actual += int(item.cantidad_recibida)
        recibidos_total += int(item.cantidad_recibida)

        # Generar movimiento hacia picking/almacén si se indica orden de producción
        if item.orden_produccion_id:
            orden = (await db.execute(
                select(OrdenProduccion).where(
                    (OrdenProduccion.id == item.orden_produccion_id) &
                    (OrdenProduccion.organization_id == org_id)
                )
            )).scalar_one_or_none()

            if orden:
                seccion = None
                if orden.seccion_produccion_id:
                    seccion = (await db.execute(
                        select(SeccionProduccion).where(
                            (SeccionProduccion.id == orden.seccion_produccion_id) &
                            (SeccionProduccion.organization_id == org_id)
                        )
                    )).scalar_one_or_none()

                tipo = "recepcion_a_picking" if (item.destino or "").lower() == "picking" else "recepcion_a_almacen"
                destino = (
                    (seccion.zona_picking or seccion.ubicacion) if (seccion and tipo == "recepcion_a_picking") else "ALMACEN"
                )

                movimiento = MovimientoAlmacen(
                    organization_id=org_id,
                    orden_produccion_id=orden.id,
                    producto_id=detalle.producto_id,
                    tipo_movimiento=tipo,
                    cantidad=int(item.cantidad_recibida),
                    ubicacion_origen="RECEPCION",
                    ubicacion_destino=destino,
                    estado="pendiente",
                )
                db.add(movimiento)

    # Actualizar compra marcadores de recepción
    compra.cantidad_items_recibidos = (compra.cantidad_items_recibidos or 0) + recibidos_total
    compra.cantidad_items_esperados = compra.cantidad_items_esperados or sum(int(d.cantidad) for d in detalles.values())
    compra.estado_recepcion = (
        "completa" if compra.cantidad_items_recibidos >= compra.cantidad_items_esperados else "parcial"
    )
    if payload.notas:
        compra.notas = (compra.notas or "") + f"\n[Recepción] {payload.notas}"

    await db.commit()
    await db.refresh(compra)

    return RecepcionCompraResponse(
        compra_id=compra.id,
        estado_recepcion=compra.estado_recepcion,
        cantidad_items_recibidos=compra.cantidad_items_recibidos,
        mensaje="Recepción registrada y stock actualizado"
    )
# ============ SOLICITUD DE COMPRA POR EMAIL ============
class ItemSolicitudCompra(BaseModel):
    producto_id: int
    cantidad: int


class SolicitudCompraRequest(BaseModel):
    proveedor_id: int
    items: List[ItemSolicitudCompra]
    notas: str | None = None


class SolicitudCompraResponse(BaseModel):
    email_enviado: bool
    proveedor_nombre: str
    proveedor_email: str
    cantidad_items: int
    items: List[dict]
    mensaje: str


@router.post("/generar-solicitud-email", response_model=SolicitudCompraResponse)
async def generar_solicitud_compra_email(
    solicitud: SolicitudCompraRequest,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """
    Generar y preparar email de solicitud de compra basado en productos y proveedor.
    Incluye detalles del producto, cantidades, precios y términos de pago.
    """
    # Obtener proveedor
    result = await db.execute(
        select(Proveedor).where(
            Proveedor.id == solicitud.proveedor_id, Proveedor.organization_id == org_id
        )
    )
    proveedor = result.scalar_one_or_none()
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    if not proveedor.es_activo:
        raise HTTPException(status_code=400, detail="El proveedor está inactivo")

    if not proveedor.email:
        raise HTTPException(status_code=400, detail="El proveedor no tiene email registrado")

    # Validar y obtener productos
    items_solicitud = []
    total_presupuesto = Decimal("0")

    for item in solicitud.items:
        result = await db.execute(
            select(Producto).where(
                Producto.id == item.producto_id, Producto.organization_id == org_id
            )
        )
        producto = result.scalar_one_or_none()
        if not producto:
            raise HTTPException(
                status_code=404, detail=f"Producto ID {item.producto_id} no encontrado"
            )

        # Usar precio de última compra si existe, sino precio de compra
        precio_ref = producto.precio_ultima_compra or producto.precio_compra
        subtotal = item.cantidad * precio_ref
        total_presupuesto += subtotal

        items_solicitud.append(
            {
                "producto": producto.nombre,
                "codigo": producto.codigo,
                "sku": producto.sku,
                "cantidad": item.cantidad,
                "unidad": producto.unidad_medida,
                "precio_unitario": float(precio_ref),
                "subtotal": float(subtotal),
                "descripcion": producto.descripcion or "",
            }
        )

    # Construir email (aquí solo se prepara, sin enviar aún)
    # TODO: Integrar con servicio de email real (SendGrid, AWS SES, etc.)
    email_body = f"""
    Estimado {proveedor.contacto_nombre or proveedor.nombre},

    Le solicitamos amablemente los siguientes productos según nuestras necesidades actuales:

    """

    for item in items_solicitud:
        email_body += f"""
    • {item['producto']} (Código: {item['codigo']}, SKU: {item['sku']})
      Cantidad: {item['cantidad']} {item['unidad']}
      Precio Unitario: ${item['precio_unitario']:.2f}
      Subtotal: ${item['subtotal']:.2f}
      Descripción: {item['descripcion']}
    """

    email_body += f"""

    RESUMEN:
    --------
    Total Items: {len(items_solicitud)}
    Presupuesto Aproximado: ${float(total_presupuesto):.2f}
    Términos de Pago: {proveedor.terminos_pago}
    Plazo de Entrega Estimado: {proveedor.dias_entrega_promedio} días

    Notas Adicionales:
    {solicitud.notas or 'Ninguna'}

    Favor de confirmar disponibilidad y enviar cotización actualizada.

    Atentamente,
    Sistema ERP Dario
    """

    return SolicitudCompraResponse(
        email_enviado=False,  # Marcar como falso hasta implementar envío real
        proveedor_nombre=proveedor.nombre,
        proveedor_email=proveedor.email,
        cantidad_items=len(items_solicitud),
        items=items_solicitud,
        mensaje=f"Solicitud preparada para {len(items_solicitud)} productos. Email listo para enviar a {proveedor.email} (implementación de envío pendiente)",
    )
