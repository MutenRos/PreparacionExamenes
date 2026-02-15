"""Ventas API routes."""
from typing import List, Union, Optional
from decimal import Decimal
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, union_all, desc
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, field_validator
from dario_app.core.auth import get_tenant_db
from dario_app.core.auth import get_org_id
from dario_app.core.email_service import EmailService
from dario_app.core.pdf_service import PDFGenerator
from dario_app.core.spain_tax_compliance import SpainTaxCompliance
from dario_app.modules.inventario.models import Producto
from dario_app.modules.pos.models import VentaPOS
from dario_app.modules.clientes.models import Cliente
from dario_app.modules.tenants.models import Organization
from dario_app.modules.documentos.models import DocumentTemplate
from dario_app.modules.oficina_tecnica.models import BOMHeader, BOMOperacion
from dario_app.modules.produccion_ordenes.models import OrdenProduccion, OperacionProduccion
from .models import Venta, VentaDetalle

router = APIRouter(prefix="/api/ventas", tags=["ventas"])
email_service = EmailService()
tax_compliance = SpainTaxCompliance()
templates = Jinja2Templates(directory="/home/dario/src/dario_app/templates")


class VentaDetalleCreate(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: Decimal
    
    @field_validator('cantidad')
    @classmethod
    def validate_cantidad(cls, v):
        if v <= 0:
            raise ValueError('La cantidad debe ser mayor a 0')
        return v
    
    @field_validator('precio_unitario')
    @classmethod
    def validate_precio(cls, v):
        if v < 0:
            raise ValueError('El precio no puede ser negativo')
        return v


class VentaCreate(BaseModel):
    """Esquema para crear una nueva orden de venta.
    
    Incluye datos del cliente (nombre, NIF, email, dirección fiscal)
    y la lista de productos con cantidades y precios.
    """
    numero: str
    cliente_nombre: str
    cliente_nif_nie: str | None = None  # NIF/NIE cliente (España)
    cliente_email: str | None = None
    cliente_id: int | None = None
    cliente_domicilio: str | None = None  # Dirección fiscal
    cliente_municipio: str | None = None
    cliente_provincia: str | None = None
    cliente_codigo_postal: str | None = None
    detalles: List[VentaDetalleCreate]
    notas: str | None = None
    template_id: int | None = None  # Template for invoice generation
    auto_send_invoice: bool = True  # Auto send invoice to client email


class VentaDetalleResponse(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal
    
    class Config:
        from_attributes = True


class VentaResponse(BaseModel):
    id: int
    numero: str
    fecha: datetime
    cliente_nombre: str
    cliente_documento: str | None
    cliente_email: str | None
    total: Decimal
    estado: str
    notas: str | None
    factura_generada: bool
    factura_numero: str | None
    factura_enviada: bool
    
    class Config:
        from_attributes = True


class VentaCombinada(BaseModel):
    """Response model for both Venta and VentaPOS."""
    id: int
    numero: str
    cliente_nombre: str
    cliente_email: str | None = None
    total: float | Decimal
    estado: str
    tipo: str  # "venta" o "suscripcion"
    observaciones: str | None = None
    creado_en: datetime | None = None
    fecha: datetime | None = None
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[VentaCombinada])
async def list_ventas(
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db)
):
    """List all sales (both Venta and VentaPOS)."""
    ventas_list = []
    
    # Get traditional sales (Venta)
    result = await db.execute(
        select(Venta).where(Venta.organization_id == org_id).order_by(Venta.fecha.desc())
    )
    for venta in result.scalars().all():
        ventas_list.append(VentaCombinada(
            id=venta.id,
            numero=venta.numero,
            cliente_nombre=venta.cliente_nombre,
            total=venta.total,
            estado=venta.estado,
            tipo="venta",
            fecha=venta.fecha
        ))
    
    # Get POS sales (VentaPOS)
    result = await db.execute(
        select(VentaPOS).where(VentaPOS.organization_id == org_id).order_by(VentaPOS.creado_en.desc())
    )
    for venta in result.scalars().all():
        # Get client name
        cliente_nombre = "Cliente desconocido"
        cliente_email = None
        if venta.cliente_id:
            result_cliente = await db.execute(
                select(Cliente).where(Cliente.id == venta.cliente_id)
            )
            cliente = result_cliente.scalar_one_or_none()
            if cliente:
                cliente_nombre = cliente.nombre
                cliente_email = cliente.email
        
        ventas_list.append(VentaCombinada(
            id=venta.id,
            numero=venta.numero,
            cliente_nombre=cliente_nombre,
            cliente_email=cliente_email,
            total=venta.total,
            estado=venta.estado,
            observaciones=venta.observaciones,
            tipo="suscripcion",
            creado_en=venta.creado_en
        ))
    
    # Sort by date descending
    ventas_list.sort(key=lambda x: x.creado_en or x.fecha or datetime.now(), reverse=True)
    return ventas_list


# Printable: Presupuesto (Quote)
@router.get("/presupuestos/{venta_id}/print")
async def print_presupuesto(
    venta_id: int,
    request: Request,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Render a printable HTML document for a sales quote (presupuesto)."""
    res = await db.execute(select(Venta).where(Venta.organization_id == org_id, Venta.id == venta_id))
    venta = res.scalar_one_or_none()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta/Presupuesto no encontrado")

    res_items = await db.execute(select(VentaDetalle).where(VentaDetalle.venta_id == venta.id))
    items = res_items.scalars().all()

    # Organization
    org = None
    try:
        org_res = await db.execute(select(Organization).where(Organization.id == org_id))
        org = org_res.scalar_one_or_none()
    except Exception:
        org = None

    context = {
        "request": request,
        "venta": venta,
        "items": items,
        "tipo": "Presupuesto",
        "org": org,
    }
    return templates.TemplateResponse("print/presupuesto.html", context)


# Printable: Pedido de Venta (Sales Order)
@router.get("/pedidos/{venta_id}/print")
async def print_pedido_venta(
    venta_id: int,
    request: Request,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Render a printable HTML document for a sales order (pedido de venta)."""
    res = await db.execute(select(Venta).where(Venta.organization_id == org_id, Venta.id == venta_id))
    venta = res.scalar_one_or_none()
    if not venta:
        raise HTTPException(status_code=404, detail="Pedido de venta no encontrado")

    res_items = await db.execute(select(VentaDetalle).where(VentaDetalle.venta_id == venta.id))
    items = res_items.scalars().all()

    org = None
    try:
        org_res = await db.execute(select(Organization).where(Organization.id == org_id))
        org = org_res.scalar_one_or_none()
    except Exception:
        org = None

    context = {
        "request": request,
        "venta": venta,
        "items": items,
        "tipo": "Pedido de Venta",
        "org": org,
    }
    return templates.TemplateResponse("print/pedido_venta.html", context)


# Printable: Albarán (Delivery Note)
@router.get("/albaranes/{venta_id}/print")
async def print_albaran(
    venta_id: int,
    request: Request,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Render a printable HTML document for delivery note (albarán)."""
    res = await db.execute(select(Venta).where(Venta.organization_id == org_id, Venta.id == venta_id))
    venta = res.scalar_one_or_none()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")

    res_items = await db.execute(select(VentaDetalle).where(VentaDetalle.venta_id == venta.id))
    items = res_items.scalars().all()

    org = None
    try:
        org_res = await db.execute(select(Organization).where(Organization.id == org_id))
        org = org_res.scalar_one_or_none()
    except Exception:
        org = None

    context = {
        "request": request,
        "venta": venta,
        "items": items,
        "tipo": "Albarán",
        "org": org,
    }
    return templates.TemplateResponse("print/albaran.html", context)


# Printable: Factura (HTML)
@router.get("/facturas/{venta_id}/print")
async def print_factura_html(
    venta_id: int,
    request: Request,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Render a printable HTML document for invoice (factura)."""
    res = await db.execute(select(Venta).where(Venta.organization_id == org_id, Venta.id == venta_id))
    venta = res.scalar_one_or_none()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")

    res_items = await db.execute(select(VentaDetalle, Producto).join(Producto, VentaDetalle.producto_id == Producto.id).where(VentaDetalle.venta_id == venta.id))
    rows = res_items.all()

    # IVA 21%
    subtotal = Decimal("0")
    for det, prod in rows:
        subtotal += det.cantidad * det.precio_unitario
    iva = subtotal * Decimal("0.21")
    total = subtotal + iva

    org = None
    try:
        org_res = await db.execute(select(Organization).where(Organization.id == org_id))
        org = org_res.scalar_one_or_none()
    except Exception:
        org = None

    context = {
        "request": request,
        "venta": venta,
        "items": rows,
        "subtotal": subtotal,
        "iva": iva,
        "total": total,
        "porcentaje_iva": 21,
        "org": org,
    }
    return templates.TemplateResponse("print/factura.html", context)


# Confirmar pedido y generar órdenes de producción
@router.post("/pedidos/{venta_id}/confirmar")
async def confirmar_pedido_y_generar_ordenes(
    venta_id: int,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Confirma el pedido de venta y genera órdenes de producción basadas en BOM principal de cada producto.

    - Busca la `Venta` y sus `VentaDetalle`.
    - Para cada línea, obtiene el `BOMHeader` principal activo del producto.
    - Genera una `OrdenProduccion` con cantidad igual a la cantidad del pedido.
    - Crea operaciones (`OperacionProduccion`) desde las operaciones del BOM.
    - Actualiza el estado de la venta a `en_produccion`.
    """
    # Obtener venta
    res_venta = await db.execute(
        select(Venta).where(Venta.organization_id == org_id, Venta.id == venta_id)
    )
    venta = res_venta.scalar_one_or_none()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")

    # Obtener detalles
    res_det = await db.execute(select(VentaDetalle).where(VentaDetalle.venta_id == venta.id))
    detalles = res_det.scalars().all()
    if not detalles:
        raise HTTPException(status_code=400, detail="La venta no tiene líneas de detalle")

    nuevas_ordenes: list[dict] = []

    # Base para numeración de órdenes
    last_order = (await db.execute(
        select(OrdenProduccion).where(OrdenProduccion.organization_id == org_id).order_by(desc(OrdenProduccion.id)).limit(1)
    )).scalar_one_or_none()
    next_seq = (last_order.id + 1) if last_order else 1

    from datetime import datetime

    for det in detalles:
        # BOM principal para el producto
        res_bom = await db.execute(
            select(BOMHeader).where(
                (BOMHeader.organization_id == org_id) &
                (BOMHeader.producto_id == det.producto_id) &
                (BOMHeader.es_principal == True) &
                (BOMHeader.activo == True)
            ).order_by(BOMHeader.id)
        )
        bom = res_bom.scalar_one_or_none()
        if not bom:
            # Si no hay BOM, saltar o lanzar error; aquí lanzamos error para consistencia
            raise HTTPException(status_code=400, detail=f"No hay BOM principal activo para el producto {det.producto_id}")

        # Generar número de orden
        order_number = f"OP-{datetime.utcnow().year}-{next_seq:05d}"
        next_seq += 1

        # Crear orden básica
        nueva_orden = OrdenProduccion(
            organization_id=org_id,
            venta_id=venta.id,
            bom_id=bom.id,
            producto_id=det.producto_id,
            numero=order_number,
            cantidad_ordenada=float(det.cantidad),
            descripcion=f"Orden desde pedido {venta.numero}",
        )
        db.add(nueva_orden)
        await db.flush()

        # Crear operaciones desde BOM
        res_ops = await db.execute(
            select(BOMOperacion).where(BOMOperacion.bom_header_id == bom.id).order_by(BOMOperacion.secuencia)
        )
        bom_ops = res_ops.scalars().all()
        for idx, bom_op in enumerate(bom_ops, 1):
            op = OperacionProduccion(
                organization_id=org_id,
                orden_produccion_id=nueva_orden.id,
                bom_operacion_id=bom_op.id,
                secuencia=idx * 10,
                duracion_estimada=bom_op.duracion_estimada,
            )
            db.add(op)

        nuevas_ordenes.append({
            "id": nueva_orden.id,
            "numero": nueva_orden.numero,
            "producto_id": nueva_orden.producto_id,
            "cantidad": nueva_orden.cantidad_ordenada,
        })

    # Actualizar venta a en_produccion
    venta.estado = "en_produccion"

    await db.commit()

    return {"venta_id": venta.id, "venta_numero": venta.numero, "ordenes": nuevas_ordenes}


@router.get("/pendientes-aprobacion", response_model=List[VentaCombinada])
async def list_pendientes_aprobacion(
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db)
):
    """List POS sales pending approval."""
    pendientes = []
    result = await db.execute(
        select(VentaPOS).where(VentaPOS.organization_id == org_id, VentaPOS.estado == "pendiente_aprobacion").order_by(VentaPOS.creado_en.desc())
    )
    for venta in result.scalars().all():
        cliente_nombre = "Cliente desconocido"
        cliente_email = None
        if venta.cliente_id:
            result_cliente = await db.execute(select(Cliente).where(Cliente.id == venta.cliente_id))
            cliente = result_cliente.scalar_one_or_none()
            if cliente:
                cliente_nombre = cliente.nombre
                cliente_email = cliente.email
        pendientes.append(VentaCombinada(
            id=venta.id,
            numero=venta.numero,
            cliente_nombre=cliente_nombre,
            cliente_email=cliente_email,
            total=venta.total,
            estado=venta.estado,
            observaciones=venta.observaciones,
            tipo="suscripcion",
            creado_en=venta.creado_en
        ))
    return pendientes


@router.get("", response_model=List[VentaCombinada], include_in_schema=False)
async def list_ventas_no_slash(
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Alias without trailing slash to avoid redirects (307)."""
    return await list_ventas(org_id=org_id, db=db)


@router.post("/", response_model=VentaResponse, status_code=status.HTTP_201_CREATED)
async def create_venta(
    venta: VentaCreate,
    background_tasks: BackgroundTasks,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db)
):
    """Create a new sale and auto-generate invoice."""
    # Validar stock disponible para todos los productos
    for detalle in venta.detalles:
        result = await db.execute(
            select(Producto).where(
                Producto.id == detalle.producto_id,
                Producto.organization_id == org_id
            )
        )
        producto = result.scalar_one_or_none()
        if not producto:
            raise HTTPException(
                status_code=404,
                detail=f"Producto {detalle.producto_id} no encontrado"
            )
        if producto.stock_actual < detalle.cantidad:
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente para {producto.nombre}. Disponible: {producto.stock_actual}, Solicitado: {detalle.cantidad}"
            )
    
    # Get client email if cliente_id provided
    cliente_email = venta.cliente_email
    if venta.cliente_id and not cliente_email:
        result_cliente = await db.execute(
            select(Cliente).where(
                Cliente.id == venta.cliente_id,
                Cliente.organization_id == org_id
            )
        )
        cliente = result_cliente.scalar_one_or_none()
        if cliente:
            cliente_email = cliente.email
    
    total = sum(d.cantidad * d.precio_unitario for d in venta.detalles)
    
    # Generate invoice number
    factura_numero = f"F-{venta.numero}"
    
    db_venta = Venta(
        numero=venta.numero,
        cliente_nombre=venta.cliente_nombre,
        cliente_nif_nie=venta.cliente_nif_nie,  # NIF/NIE (Spain compliance)
        cliente_email=cliente_email,
        cliente_id=venta.cliente_id,
        cliente_domicilio=venta.cliente_domicilio,  # Fiscal address
        cliente_municipio=venta.cliente_municipio,
        cliente_provincia=venta.cliente_provincia,
        cliente_codigo_postal=venta.cliente_codigo_postal,
        total=total,
        notas=venta.notas,
        organization_id=org_id,
        template_id=venta.template_id,
        factura_numero=factura_numero
    )
    db.add(db_venta)
    await db.flush()
    
    # Crear detalles y actualizar stock
    detalles_list = []
    for detalle in venta.detalles:
        db_detalle = VentaDetalle(
            venta_id=db_venta.id,
            producto_id=detalle.producto_id,
            cantidad=detalle.cantidad,
            precio_unitario=detalle.precio_unitario,
            subtotal=detalle.cantidad * detalle.precio_unitario
        )
        db.add(db_detalle)
        detalles_list.append(db_detalle)
        
        # Actualizar stock del producto
        result = await db.execute(
            select(Producto).where(Producto.id == detalle.producto_id)
        )
        producto = result.scalar_one()
        producto.stock_actual -= detalle.cantidad
    
    await db.commit()
    await db.refresh(db_venta)
    
    # Generate and send invoice in background
    if cliente_email and venta.auto_send_invoice:
        background_tasks.add_task(
            generate_and_send_invoice,
            db_venta.id,
            org_id,
            cliente_email,
            venta.template_id
        )
    
    return db_venta


async def generate_and_send_invoice(
    venta_id: int,
    org_id: int,
    cliente_email: str,
    template_id: Optional[int] = None
):
    """Background task to generate PDF invoice and send via email."""
    from dario_app.database import async_session_maker
    
    async with async_session_maker() as db:
        try:
            # Get venta with details
            result = await db.execute(
                select(Venta).where(Venta.id == venta_id)
            )
            venta = result.scalar_one_or_none()
            if not venta:
                print(f"[INVOICE] Venta {venta_id} not found")
                return
            
            # Get organization
            org_result = await db.execute(
                select(Organization).where(Organization.id == org_id)
            )
            organization = org_result.scalar_one_or_none()
            if not organization:
                print(f"[INVOICE] Organization {org_id} not found")
                return
            
            # Check fiscal data
            if not organization.datos_fiscales_completos:
                print(f"[INVOICE] Organization {org_id} fiscal data incomplete")
                venta.factura_generada = False
                await db.commit()
                return
            
            # Get or use default template
            template = None
            if template_id:
                template_result = await db.execute(
                    select(DocumentTemplate).where(
                        DocumentTemplate.id == template_id,
                        DocumentTemplate.organization_id == org_id
                    )
                )
                template = template_result.scalar_one_or_none()
            
            # If no template specified or not found, get first factura template
            if not template:
                template_result = await db.execute(
                    select(DocumentTemplate).where(
                        DocumentTemplate.organization_id == org_id,
                        DocumentTemplate.tipo_documento == "factura"
                    ).limit(1)
                )
                template = template_result.scalar_one_or_none()
            
            if not template:
                print(f"[INVOICE] No factura template found for org {org_id}")
                venta.factura_generada = False
                await db.commit()
                return
            
            # Get venta details
            detalles_result = await db.execute(
                select(VentaDetalle, Producto).join(
                    Producto, VentaDetalle.producto_id == Producto.id
                ).where(VentaDetalle.venta_id == venta_id)
            )
            detalles_rows = detalles_result.all()
            
            # Prepare items for PDF
            items = []
            subtotal = Decimal("0")
            for detalle, producto in detalles_rows:
                item_subtotal = detalle.cantidad * detalle.precio_unitario
                items.append({
                    'descripcion': producto.nombre,
                    'cantidad': detalle.cantidad,
                    'precio_unitario': float(detalle.precio_unitario),
                    'subtotal': float(item_subtotal)
                })
                subtotal += item_subtotal
            
            # Calculate IVA (21% for Spain)
            porcentaje_iva = 21
            iva = subtotal * Decimal("0.21")
            total = subtotal + iva
            
            # Prepare data for PDF (Spain tax compliance)
            venta_data = {
                'numero': venta.factura_numero,
                'items': items,
                'base_imponible': float(subtotal),
                'subtotal': float(subtotal),
                'descuento': 0,
                'iva': float(iva),
                'porcentaje_iva': porcentaje_iva,
                'total': float(total),
                'notas': venta.notas or ''
            }
            
            cliente_data = {
                'nombre': venta.cliente_nombre,
                'documento': venta.cliente_documento or 'N/A',
                'email': cliente_email,
                'telefono': 'N/A'
            }
            
            # Generate PDF
            generator = PDFGenerator(template, organization)
            pdf_buffer = generator.generate_invoice_pdf(venta_data, cliente_data)
            pdf_content = pdf_buffer.getvalue()
            
            # Send email
            pdf_filename = f"{venta.factura_numero}.pdf"
            email_sent = email_service.send_invoice_email(
                to_email=cliente_email,
                customer_name=venta.cliente_nombre,
                invoice_number=venta.factura_numero,
                pdf_content=pdf_content,
                pdf_filename=pdf_filename,
                organization_name=organization.razon_social or organization.nombre
            )
            
            # Update venta status
            venta.factura_generada = True
            venta.factura_enviada = email_sent
            await db.commit()
            
            print(f"[INVOICE] Generated and sent invoice {venta.factura_numero} to {cliente_email}")
            
        except Exception as e:
            print(f"[INVOICE ERROR] Failed to generate/send invoice for venta {venta_id}: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Mark as failed
            try:
                venta.factura_generada = False
                venta.factura_enviada = False
                await db.commit()
            except:
                pass


@router.get("/{venta_id}", response_model=VentaResponse)
async def get_venta(
    venta_id: int,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db)
):
    """Get a sale by ID."""
    result = await db.execute(
        select(Venta).where(
            Venta.id == venta_id,
            Venta.organization_id == org_id
        )
    )
    venta = result.scalar_one_or_none()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta


@router.post("/{venta_id}/reenviar-factura")
async def reenviar_factura(
    venta_id: int,
    background_tasks: BackgroundTasks,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db)
):
    """Resend invoice for a sale."""
    result = await db.execute(
        select(Venta).where(
            Venta.id == venta_id,
            Venta.organization_id == org_id
        )
    )
    venta = result.scalar_one_or_none()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    
    if not venta.cliente_email:
        raise HTTPException(status_code=400, detail="No hay email de cliente registrado")
    
    # Regenerate and send invoice
    background_tasks.add_task(
        generate_and_send_invoice,
        venta_id,
        org_id,
        venta.cliente_email,
        venta.template_id
    )
    
    return {"message": "Factura será reenviada en breve", "email": venta.cliente_email}


@router.get("/{venta_id}/factura-pdf")
async def descargar_factura(
    venta_id: int,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db)
):
    """Download invoice PDF for a sale."""
    from fastapi.responses import StreamingResponse
    
    # Get venta
    result = await db.execute(
        select(Venta).where(
            Venta.id == venta_id,
            Venta.organization_id == org_id
        )
    )
    venta = result.scalar_one_or_none()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    
    # Get organization
    org_result = await db.execute(
        select(Organization).where(Organization.id == org_id)
    )
    organization = org_result.scalar_one_or_none()
    if not organization or not organization.datos_fiscales_completos:
        raise HTTPException(
            status_code=400,
            detail="Complete los datos fiscales antes de generar facturas"
        )
    
    # Get template
    template = None
    if venta.template_id:
        template_result = await db.execute(
            select(DocumentTemplate).where(
                DocumentTemplate.id == venta.template_id,
                DocumentTemplate.organization_id == org_id
            )
        )
        template = template_result.scalar_one_or_none()
    
    if not template:
        template_result = await db.execute(
            select(DocumentTemplate).where(
                DocumentTemplate.organization_id == org_id,
                DocumentTemplate.tipo_documento == "factura"
            ).limit(1)
        )
        template = template_result.scalar_one_or_none()
    
    if not template:
        raise HTTPException(status_code=404, detail="No hay plantilla de factura disponible")
    
    # Get venta details
    detalles_result = await db.execute(
        select(VentaDetalle, Producto).join(
            Producto, VentaDetalle.producto_id == Producto.id
        ).where(VentaDetalle.venta_id == venta_id)
    )
    detalles_rows = detalles_result.all()
    
    # Prepare items for PDF
    items = []
    subtotal = Decimal("0")
    for detalle, producto in detalles_rows:
        item_subtotal = detalle.cantidad * detalle.precio_unitario
        items.append({
            'descripcion': producto.nombre,
            'cantidad': detalle.cantidad,
            'precio_unitario': float(detalle.precio_unitario),
            'subtotal': float(item_subtotal)
        })
        subtotal += item_subtotal
    
    # Calculate IVA (21% for Spain)
    porcentaje_iva = 21
    iva = subtotal * Decimal("0.21")
    total = subtotal + iva
    
    # Prepare data
    venta_data = {
        'numero': venta.factura_numero or f"F-{venta.numero}",
        'items': items,
        'subtotal': float(subtotal),
        'descuento': 0,
        'impuesto': float(impuesto),
        'total': float(total),
        'notas': venta.notas or ''
    }
    
    cliente_data = {
        'nombre': venta.cliente_nombre,
        'documento': venta.cliente_documento or 'N/A',
        'email': venta.cliente_email or 'N/A',
        'telefono': 'N/A'
    }
    
    # Generate PDF
    generator = PDFGenerator(template, organization)
    pdf_buffer = generator.generate_invoice_pdf(venta_data, cliente_data)
    
    filename = f"{venta.factura_numero or venta.numero}.pdf"
    
    return StreamingResponse(
        iter([pdf_buffer.getvalue()]),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
