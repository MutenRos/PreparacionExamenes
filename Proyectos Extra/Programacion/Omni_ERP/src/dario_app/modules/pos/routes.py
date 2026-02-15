"""POS API routes."""

from datetime import datetime
from typing import List
import secrets
import json

from fastapi import APIRouter, Depends, status, HTTPException, Header, Query
from pydantic import BaseModel, field_validator
from sqlalchemy import select, or_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from dario_app.core.auth import get_org_id, get_tenant_db
from dario_app.modules.inventario.models import Producto
from dario_app.database import get_db

from .models import VentaPOS, VentaPOSDetalle, PosWidget
from dario_app.modules.ventas.models import Venta, VentaDetalle
from dario_app.modules.oficina_tecnica.models import BOMHeader, BOMOperacion
from dario_app.modules.produccion_ordenes.models import (
    OrdenProduccion,
    OperacionProduccion,
    EstadoOrdenProduccion,
    TipoPrioridad,
)
# Ensure all dependencies are registered to avoid SQLAlchemy errors
from dario_app.modules.clientes.models import Cliente
from dario_app.modules.tenants.models import Organization
from dario_app.modules.calendario.models import Evento
from dario_app.modules.compras.models import Compra

router = APIRouter(prefix="/api/pos", tags=["pos"])


class VentaPOSDetalleCreate(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: float
    descuento: float = 0

    @field_validator("cantidad")
    @classmethod
    def validate_cantidad(cls, v):
        if v <= 0:
            raise ValueError("Cantidad debe ser mayor a 0")
        return v

    @field_validator("precio_unitario")
    @classmethod
    def validate_precio(cls, v):
        if v < 0:
            raise ValueError("Precio no puede ser negativo")
        return v

    @field_validator("descuento")
    @classmethod
    def validate_descuento(cls, v):
        if v < 0:
            raise ValueError("Descuento no puede ser negativo")
        return v


class VentaPOSCreate(BaseModel):
    cliente_id: int | None = None
    detalles: List[VentaPOSDetalleCreate]
    metodo_pago: str = "efectivo"
    monto_pagado: float
    descuento: float = 0
    observaciones: str | None = None


class VentaPOSDetalleResponse(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_unitario: float
    descuento: float
    subtotal: float

    class Config:
        from_attributes = True


class VentaPOSResponse(BaseModel):
    id: int
    numero: str
    cliente_id: int | None
    subtotal: float
    descuento: float
    impuesto: float
    total: float
    metodo_pago: str
    monto_pagado: float
    cambio: float
    estado: str
    observaciones: str | None = None
    creado_en: datetime
    detalles: List[VentaPOSDetalleResponse]

    class Config:
        from_attributes = True


@router.post("/", response_model=VentaPOSResponse, status_code=status.HTTP_201_CREATED)
async def create_venta_pos(
    venta: VentaPOSCreate,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Create a new POS sale transaction."""
    # Calculate totals
    subtotal = 0
    for detalle in venta.detalles:
        item_subtotal = (detalle.cantidad * detalle.precio_unitario) - detalle.descuento
        subtotal += item_subtotal

    total_descuento = venta.descuento
    impuesto = (subtotal - total_descuento) * 0.18  # 18% tax
    total = subtotal - total_descuento + impuesto
    cambio = venta.monto_pagado - total

    # Generate transaction number
    result = await db.execute(select(VentaPOS).where(VentaPOS.organization_id == org_id))
    count = len(result.scalars().all())
    numero = f"POS-{org_id}-{count + 1:06d}"

    # Create sale
    db_venta = VentaPOS(
        organization_id=org_id,
        numero=numero,
        cliente_id=venta.cliente_id,
        subtotal=subtotal,
        descuento=total_descuento,
        impuesto=impuesto,
        total=total,
        metodo_pago=venta.metodo_pago,
        monto_pagado=venta.monto_pagado,
        cambio=cambio,
        estado="pendiente_aprobacion",
        observaciones=venta.observaciones,
    )
    db.add(db_venta)
    await db.flush()

    # Create line items and update stock
    for detalle in venta.detalles:
        item_subtotal = (detalle.cantidad * detalle.precio_unitario) - detalle.descuento
        db_detalle = VentaPOSDetalle(
            venta_pos_id=db_venta.id,
            producto_id=detalle.producto_id,
            cantidad=detalle.cantidad,
            precio_unitario=detalle.precio_unitario,
            descuento=detalle.descuento,
            subtotal=item_subtotal,
        )
        db.add(db_detalle)

        # Update stock
        producto_result = await db.execute(
            select(Producto).where(
                Producto.id == detalle.producto_id, Producto.organization_id == org_id
            )
        )
        producto = producto_result.scalar_one_or_none()
        if producto:
            producto.stock_actual -= detalle.cantidad

    await db.commit()
    await db.refresh(db_venta)

    # Load relationships
    result = await db.execute(
        select(VentaPOS).options(selectinload(VentaPOS.detalles)).where(VentaPOS.id == db_venta.id)
    )
    return result.scalar_one()


@router.post("/demo", response_model=VentaPOSResponse, status_code=status.HTTP_201_CREATED)
async def create_venta_pos_demo(
    venta: VentaPOSCreate,
    db: AsyncSession = Depends(get_tenant_db),
):
    """Create a new POS sale transaction (demo - no auth required, uses org_id=1)."""
    org_id = 1  # Demo organization
    
    # Calculate totals
    subtotal = 0
    for detalle in venta.detalles:
        item_subtotal = (detalle.cantidad * detalle.precio_unitario) - detalle.descuento
        subtotal += item_subtotal

    total_descuento = venta.descuento
    impuesto = (subtotal - total_descuento) * 0.18  # 18% tax
    total = subtotal - total_descuento + impuesto
    cambio = venta.monto_pagado - total

    # Generate transaction number
    result = await db.execute(select(VentaPOS).where(VentaPOS.organization_id == org_id))
    count = len(result.scalars().all())
    numero = f"POS-{org_id}-{count + 1:06d}"

    # Create sale
    db_venta = VentaPOS(
        organization_id=org_id,
        numero=numero,
        cliente_id=venta.cliente_id,
        subtotal=subtotal,
        descuento=total_descuento,
        impuesto=impuesto,
        total=total,
        metodo_pago=venta.metodo_pago,
        monto_pagado=venta.monto_pagado,
        cambio=cambio,
        estado="pendiente_aprobacion",
        observaciones=venta.observaciones,
    )
    db.add(db_venta)
    await db.flush()

    # Create line items and update stock
    for detalle in venta.detalles:
        item_subtotal = (detalle.cantidad * detalle.precio_unitario) - detalle.descuento
        db_detalle = VentaPOSDetalle(
            venta_pos_id=db_venta.id,
            producto_id=detalle.producto_id,
            cantidad=detalle.cantidad,
            precio_unitario=detalle.precio_unitario,
            descuento=detalle.descuento,
            subtotal=item_subtotal,
        )
        db.add(db_detalle)

        # Update stock
        producto_result = await db.execute(
            select(Producto).where(
                Producto.id == detalle.producto_id, Producto.organization_id == org_id
            )
        )
        producto = producto_result.scalar_one_or_none()
        if producto:
            producto.stock_actual -= detalle.cantidad

    await db.commit()
    await db.refresh(db_venta)

    # Load relationships
    result = await db.execute(
        select(VentaPOS).options(selectinload(VentaPOS.detalles)).where(VentaPOS.id == db_venta.id)
    )
    return result.scalar_one()


@router.post("/{venta_pos_id}/aprobar")
async def aprobar_venta_pos(
    venta_pos_id: int,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Approve a pending POS sale (sets estado to 'completada')."""
    result = await db.execute(
        select(VentaPOS).where(VentaPOS.id == venta_pos_id, VentaPOS.organization_id == org_id)
    )
    venta = result.scalar_one_or_none()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta POS no encontrada")
    venta.estado = "completada"
    await db.flush()

    # Crear una Venta tradicional para vincular órdenes de producción
    # Generar número secuencial para Venta
    existing_ventas = await db.execute(select(Venta).where(Venta.organization_id == org_id))
    ventas_count = len(existing_ventas.scalars().all())
    venta_numero = f"V-{org_id}-{ventas_count + 1:06d}"

    db_venta = Venta(
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
    db.add(db_venta)
    await db.flush()

    # Crear detalles de venta (no ajustar stock nuevamente)
    detalles_res = await db.execute(
        select(VentaPOSDetalle).where(VentaPOSDetalle.venta_pos_id == venta.id)
    )
    detalles = detalles_res.scalars().all()
    for d in detalles:
        db_det = VentaDetalle(
            venta_id=db_venta.id,
            producto_id=d.producto_id,
            cantidad=d.cantidad,
            precio_unitario=d.precio_unitario,
            subtotal=d.cantidad * d.precio_unitario,
        )
        db.add(db_det)

    await db.flush()

    # Crear órdenes de producción por cada línea con BOM principal
    created_orders = []
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
            # No BOM principal para este producto; omitir creación
            continue

        # Generar número de orden
        last_order = (await db.execute(
            select(OrdenProduccion).where(OrdenProduccion.organization_id == org_id).order_by(desc(OrdenProduccion.id)).limit(1)
        )).scalar_one_or_none()
        order_number = f"OP-{datetime.utcnow().year}-{(last_order.id + 1 if last_order else 1):05d}"

        nueva_orden = OrdenProduccion(
            organization_id=org_id,
            venta_id=db_venta.id,
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

        # Crear operaciones desde BOM
        ops = (await db.execute(
            select(BOMOperacion).where(BOMOperacion.bom_header_id == bom.id).order_by(BOMOperacion.secuencia)
        )).scalars().all()
        for idx, bom_op in enumerate(ops, 1):
            operacion = OperacionProduccion(
                organization_id=org_id,
                orden_produccion_id=nueva_orden.id,
                bom_operacion_id=bom_op.id,
                secuencia=idx * 10,
                duracion_estimada=bom_op.duracion_estimada,
            )
            db.add(operacion)

        created_orders.append({"orden_id": nueva_orden.id, "numero": nueva_orden.numero})

    await db.commit()

    return {
        "success": True,
        "message": "Venta aprobada",
        "venta_id": venta_pos_id,
        "venta_creada_id": db_venta.id,
        "ordenes_produccion": created_orders,
    }


@router.post("/{venta_pos_id}/rechazar")
async def rechazar_venta_pos(
    venta_pos_id: int,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Reject a pending POS sale (sets estado to 'cancelada')."""
    result = await db.execute(
        select(VentaPOS).where(VentaPOS.id == venta_pos_id, VentaPOS.organization_id == org_id)
    )
    venta = result.scalar_one_or_none()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta POS no encontrada")
    venta.estado = "cancelada"
    await db.commit()
    return {"success": True, "message": "Venta rechazada", "venta_id": venta_pos_id}


@router.get("/", response_model=List[VentaPOSResponse])
async def list_ventas_pos(
    org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)
):
    """List all POS transactions."""
    result = await db.execute(
        select(VentaPOS)
        .options(selectinload(VentaPOS.detalles))
        .where(VentaPOS.organization_id == org_id)
        .order_by(VentaPOS.creado_en.desc())
    )
    return result.scalars().all()


@router.get("/ventas", response_model=List[VentaPOSResponse], include_in_schema=False)
async def list_ventas_pos_alias(
    org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)
):
    """Alias para compatibilidad con /api/pos/ventas."""
    return await list_ventas_pos(org_id=org_id, db=db)


@router.get("", response_model=List[VentaPOSResponse], include_in_schema=False)
async def list_ventas_pos_no_slash(
    org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)
):
    """Alias sin slash final para evitar redirects."""
    return await list_ventas_pos(org_id=org_id, db=db)


# ==================== POS WIDGETS (PRO FEATURE) ====================


class PosWidgetCreate(BaseModel):
    nombre: str
    descripcion: str | None = None
    url_permitida: str
    color_primario: str = "#2563eb"
    color_boton: str = "#10b981"
    icono_carrito: bool = True
    mostrar_precio: bool = True
    mostrar_stock: bool = True
    categorias_ids: list[int] | None = None
    productos_ids: list[int] | None = None
    solo_disponibles: bool = True

    @field_validator("nombre")
    @classmethod
    def validate_nombre(cls, v):
        if len(v) < 3:
            raise ValueError("Nombre debe tener al menos 3 caracteres")
        return v

    @field_validator("url_permitida")
    @classmethod
    def validate_url(cls, v):
        if not v.startswith(("http://", "https://")):
            raise ValueError("URL debe empezar con http:// o https://")
        return v


class PosWidgetUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    url_permitida: str | None = None
    color_primario: str | None = None
    color_boton: str | None = None
    icono_carrito: bool | None = None
    mostrar_precio: bool | None = None
    mostrar_stock: bool | None = None
    categorias_ids: list[int] | None = None
    productos_ids: list[int] | None = None
    solo_disponibles: bool | None = None
    activo: bool | None = None


class PosWidgetResponse(BaseModel):
    id: int
    nombre: str
    token: str
    slug: str
    descripcion: str | None
    url_permitida: str
    color_primario: str
    color_boton: str
    icono_carrito: bool
    mostrar_precio: bool
    mostrar_stock: bool
    categorias_ids: str | None
    productos_ids: str | None
    solo_disponibles: bool
    activo: bool
    creado_en: datetime
    actualizado_en: datetime

    class Config:
        from_attributes = True


# Validar suscripción PRO
async def require_pro(org_id: int = Depends(get_org_id)):
    """Validate that organization has PRO subscription."""
    from dario_app.modules.tenants.models import Organization
    from dario_app.database import master_session_maker
    
    async with master_session_maker() as master_db:
        result = await master_db.execute(
            select(Organization).where(Organization.id == org_id)
        )
        org = result.scalar_one_or_none()
        
        if not org or org.plan != "pro":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This feature is only available for PRO subscriptions"
            )
        return org


@router.post("/widgets", response_model=PosWidgetResponse, status_code=status.HTTP_201_CREATED)
async def create_pos_widget(
    widget_data: PosWidgetCreate,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
    org = Depends(require_pro),
):
    """Create a new POS widget (PRO feature)."""
    
    # Generate unique token and slug
    token = secrets.token_urlsafe(48)
    slug = widget_data.nombre.lower().replace(" ", "-")[:100]
    
    # Check slug uniqueness
    existing = await db.execute(
        select(PosWidget).where(PosWidget.slug == slug, PosWidget.organization_id == org_id)
    )
    if existing.scalar_one_or_none():
        slug = f"{slug}-{secrets.token_hex(4)}"
    
    # Convert lists to JSON strings
    categorias_json = json.dumps(widget_data.categorias_ids) if widget_data.categorias_ids else None
    productos_json = json.dumps(widget_data.productos_ids) if widget_data.productos_ids else None
    
    db_widget = PosWidget(
        organization_id=org_id,
        nombre=widget_data.nombre,
        token=token,
        slug=slug,
        descripcion=widget_data.descripcion,
        url_permitida=widget_data.url_permitida,
        color_primario=widget_data.color_primario,
        color_boton=widget_data.color_boton,
        icono_carrito=widget_data.icono_carrito,
        mostrar_precio=widget_data.mostrar_precio,
        mostrar_stock=widget_data.mostrar_stock,
        categorias_ids=categorias_json,
        productos_ids=productos_json,
        solo_disponibles=widget_data.solo_disponibles,
    )
    
    db.add(db_widget)
    await db.commit()
    await db.refresh(db_widget)
    return db_widget


@router.get("/widgets", response_model=List[PosWidgetResponse])
async def list_pos_widgets(
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
    org = Depends(require_pro),
):
    """List all POS widgets for organization (PRO feature)."""
    result = await db.execute(
        select(PosWidget)
        .where(PosWidget.organization_id == org_id)
        .order_by(PosWidget.creado_en.desc())
    )
    return result.scalars().all()


@router.get("/{venta_pos_id}/detalles", response_model=List[VentaPOSDetalleResponse])
async def get_venta_pos_detalles(
    venta_pos_id: int,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Obtener detalles de una venta POS (aislado por organización)."""
    # Verify venta belongs to org
    venta = (await db.execute(
        select(VentaPOS).where(VentaPOS.id == venta_pos_id, VentaPOS.organization_id == org_id)
    )).scalar_one_or_none()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta POS no encontrada")

    result = await db.execute(
        select(VentaPOSDetalle)
        .where(VentaPOSDetalle.venta_pos_id == venta_pos_id)
        .order_by(VentaPOSDetalle.id.desc())
    )
    return result.scalars().all()


@router.get("/widgets/{widget_id}", response_model=PosWidgetResponse)
async def get_pos_widget(
    widget_id: int,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
    org = Depends(require_pro),
):
    """Get POS widget details (PRO feature)."""
    result = await db.execute(
        select(PosWidget).where(
            PosWidget.id == widget_id,
            PosWidget.organization_id == org_id
        )
    )
    widget = result.scalar_one_or_none()
    
    if not widget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Widget not found")
    
    return widget


@router.put("/widgets/{widget_id}", response_model=PosWidgetResponse)
async def update_pos_widget(
    widget_id: int,
    widget_data: PosWidgetUpdate,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
    org = Depends(require_pro),
):
    """Update POS widget (PRO feature)."""
    result = await db.execute(
        select(PosWidget).where(
            PosWidget.id == widget_id,
            PosWidget.organization_id == org_id
        )
    )
    widget = result.scalar_one_or_none()
    
    if not widget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Widget not found")
    
    # Update fields
    update_data = widget_data.dict(exclude_unset=True)
    
    # Convert lists to JSON if provided
    if "categorias_ids" in update_data and update_data["categorias_ids"]:
        update_data["categorias_ids"] = json.dumps(update_data["categorias_ids"])
    if "productos_ids" in update_data and update_data["productos_ids"]:
        update_data["productos_ids"] = json.dumps(update_data["productos_ids"])
    
    for field, value in update_data.items():
        setattr(widget, field, value)
    
    await db.commit()
    await db.refresh(widget)
    return widget


@router.delete("/widgets/{widget_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pos_widget(
    widget_id: int,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
    org = Depends(require_pro),
):
    """Delete POS widget (PRO feature)."""
    result = await db.execute(
        select(PosWidget).where(
            PosWidget.id == widget_id,
            PosWidget.organization_id == org_id
        )
    )
    widget = result.scalar_one_or_none()
    
    if not widget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Widget not found")
    
    await db.delete(widget)
    await db.commit()
    return None


# ==================== PUBLIC WIDGET API (NO AUTH) ====================


class ProductoWidgetResponse(BaseModel):
    id: int
    nombre: str
    precio_venta: float
    stock_actual: int
    imagen_url: str | None

    class Config:
        from_attributes = True


@router.get("/public/widget/{token}/productos", response_model=List[ProductoWidgetResponse])
async def get_widget_productos(
    token: str,
    origin: str | None = Header(None),
):
    """Get products for widget (public, token-based). No authentication needed."""
    
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Public widget endpoints will be available in v1.1"
    )


class VentaWidgetCreate(BaseModel):
    detalles: List[VentaPOSDetalleCreate]
    metodo_pago: str = "online"


@router.post("/public/widget/{token}/compra", response_model=dict)
async def create_widget_sale(
    token: str,
    venta: VentaWidgetCreate,
    origin: str | None = Header(None),
):
    """Create a sale from widget (public, token-based). No authentication needed."""
    
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Public widget endpoints will be available in v1.1"
    )
