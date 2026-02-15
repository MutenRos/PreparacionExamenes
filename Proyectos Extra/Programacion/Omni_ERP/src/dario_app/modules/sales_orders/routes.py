"""Sales Orders & Quotes routes - Quote-to-Cash process."""

from datetime import datetime, date
from typing import List, Optional
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import require_permission, get_tenant_db, get_org_id
from dario_app.modules.usuarios.models import Usuario

from .models import Quote, QuoteLine, SalesOrder, SalesOrderLine, Shipment, ShipmentLine

router = APIRouter(prefix="/api/sales-orders", tags=["Sales Orders"])


# Schemas

class QuoteCreate(BaseModel):
    customer_id: int
    customer_name: str
    quote_date: str
    expiration_date: str
    payment_terms: Optional[str] = None
    delivery_terms: Optional[str] = None
    notes: Optional[str] = None


class QuoteLineCreate(BaseModel):
    product_id: Optional[int] = None
    product_name: str
    description: Optional[str] = None
    quantity: float
    unit_price: float
    discount_percent: float = 0
    delivery_date: Optional[str] = None


class SalesOrderCreate(BaseModel):
    customer_id: int
    customer_name: str
    order_date: str
    requested_delivery_date: Optional[str] = None
    payment_terms: Optional[str] = None
    shipping_address: Optional[str] = None
    quote_id: Optional[int] = None


class SalesOrderLineCreate(BaseModel):
    product_id: Optional[int] = None
    product_name: str
    description: Optional[str] = None
    quantity_ordered: float
    unit_price: float
    discount_percent: float = 0
    delivery_date: Optional[str] = None


class ShipmentCreate(BaseModel):
    order_id: int
    carrier: Optional[str] = None
    tracking_number: Optional[str] = None


# Quotes

@router.post("/quotes")
async def create_quote(
    payload: QuoteCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("sales.quotes.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate quote number
    stmt = select(Quote).where(Quote.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    quote_number = f"QT-{datetime.now().strftime('%Y%m')}-{count + 1:05d}"
    
    quote = Quote(
        organization_id=org_id,
        quote_number=quote_number,
        owner_user_id=user.id,
        owner_name=user.nombre_completo,
        **payload.model_dump()
    )
    db.add(quote)
    await db.commit()
    await db.refresh(quote)
    return quote


@router.get("/quotes")
async def list_quotes(
    status: Optional[str] = None,
    customer_id: Optional[int] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("sales.quotes.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(Quote).where(Quote.organization_id == org_id)
    if status:
        query = query.where(Quote.status == status)
    if customer_id:
        query = query.where(Quote.customer_id == customer_id)
    query = query.order_by(Quote.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/quotes/{quote_id}")
async def get_quote(
    quote_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("sales.quotes.read")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(Quote).where(Quote.id == quote_id, Quote.organization_id == org_id)
    result = await db.execute(stmt)
    quote = result.scalar_one_or_none()
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    return quote


@router.post("/quotes/{quote_id}/lines")
async def add_quote_line(
    quote_id: int,
    payload: QuoteLineCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("sales.quotes.manage")),
    org_id: int = Depends(get_org_id),
):
    # Get current line count
    stmt = select(QuoteLine).where(
        QuoteLine.organization_id == org_id,
        QuoteLine.quote_id == quote_id
    )
    result = await db.execute(stmt)
    line_number = len(result.scalars().all()) + 1
    
    line_total = Decimal(str(payload.quantity)) * Decimal(str(payload.unit_price)) * (1 - Decimal(str(payload.discount_percent)) / 100)
    
    line = QuoteLine(
        organization_id=org_id,
        quote_id=quote_id,
        line_number=line_number,
        line_total=line_total,
        **payload.model_dump()
    )
    db.add(line)
    
    # Update quote totals
    quote_stmt = select(Quote).where(Quote.id == quote_id, Quote.organization_id == org_id)
    quote_result = await db.execute(quote_stmt)
    quote = quote_result.scalar_one_or_none()
    if quote:
        quote.subtotal += line_total
        quote.total_amount = quote.subtotal + quote.tax_amount - quote.discount_amount
    
    await db.commit()
    await db.refresh(line)
    return line


@router.get("/quotes/{quote_id}/lines")
async def list_quote_lines(
    quote_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("sales.quotes.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(QuoteLine).where(
        QuoteLine.organization_id == org_id,
        QuoteLine.quote_id == quote_id
    ).order_by(QuoteLine.line_number)
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/quotes/{quote_id}/send")
async def send_quote(
    quote_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("sales.quotes.send")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(Quote).where(Quote.id == quote_id, Quote.organization_id == org_id)
    result = await db.execute(stmt)
    quote = result.scalar_one_or_none()
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    
    quote.status = "sent"
    await db.commit()
    await db.refresh(quote)
    return quote


@router.post("/quotes/{quote_id}/convert-to-order")
async def convert_quote_to_order(
    quote_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("sales.quotes.convert")),
    org_id: int = Depends(get_org_id),
):
    # Get quote
    quote_stmt = select(Quote).where(Quote.id == quote_id, Quote.organization_id == org_id)
    quote_result = await db.execute(quote_stmt)
    quote = quote_result.scalar_one_or_none()
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    
    # Generate order number
    order_stmt = select(SalesOrder).where(SalesOrder.organization_id == org_id)
    order_result = await db.execute(order_stmt)
    count = len(order_result.scalars().all())
    order_number = f"SO-{datetime.now().strftime('%Y%m')}-{count + 1:05d}"
    
    # Create sales order
    order = SalesOrder(
        organization_id=org_id,
        order_number=order_number,
        customer_id=quote.customer_id,
        customer_name=quote.customer_name,
        order_date=date.today(),
        subtotal=quote.subtotal,
        tax_amount=quote.tax_amount,
        discount_amount=quote.discount_amount,
        total_amount=quote.total_amount,
        payment_terms=quote.payment_terms,
        quote_id=quote.id,
        owner_user_id=user.id,
        owner_name=user.nombre_completo
    )
    db.add(order)
    await db.flush()
    
    # Copy quote lines
    lines_stmt = select(QuoteLine).where(
        QuoteLine.organization_id == org_id,
        QuoteLine.quote_id == quote_id
    )
    lines_result = await db.execute(lines_stmt)
    quote_lines = lines_result.scalars().all()
    
    for qline in quote_lines:
        order_line = SalesOrderLine(
            organization_id=org_id,
            order_id=order.id,
            line_number=qline.line_number,
            product_id=qline.product_id,
            product_name=qline.product_name,
            description=qline.description,
            quantity_ordered=qline.quantity,
            unit_price=qline.unit_price,
            discount_percent=qline.discount_percent,
            line_total=qline.line_total,
            delivery_date=qline.delivery_date
        )
        db.add(order_line)
    
    # Update quote
    quote.status = "accepted"
    quote.converted_to_order = True
    quote.order_id = order.id
    
    await db.commit()
    await db.refresh(order)
    return order


# Sales Orders

@router.post("/orders")
async def create_sales_order(
    payload: SalesOrderCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("sales.orders.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate order number
    stmt = select(SalesOrder).where(SalesOrder.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    order_number = f"SO-{datetime.now().strftime('%Y%m')}-{count + 1:05d}"
    
    order = SalesOrder(
        organization_id=org_id,
        order_number=order_number,
        owner_user_id=user.id,
        owner_name=user.nombre_completo,
        **payload.model_dump()
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


@router.get("/orders")
async def list_sales_orders(
    status: Optional[str] = None,
    customer_id: Optional[int] = None,
    fulfillment_status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("sales.orders.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(SalesOrder).where(SalesOrder.organization_id == org_id)
    if status:
        query = query.where(SalesOrder.status == status)
    if customer_id:
        query = query.where(SalesOrder.customer_id == customer_id)
    if fulfillment_status:
        query = query.where(SalesOrder.fulfillment_status == fulfillment_status)
    query = query.order_by(SalesOrder.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/orders/{order_id}")
async def get_sales_order(
    order_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("sales.orders.read")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(SalesOrder).where(SalesOrder.id == order_id, SalesOrder.organization_id == org_id)
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Sales order not found")
    return order


@router.post("/orders/{order_id}/lines")
async def add_order_line(
    order_id: int,
    payload: SalesOrderLineCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("sales.orders.manage")),
    org_id: int = Depends(get_org_id),
):
    # Get current line count
    stmt = select(SalesOrderLine).where(
        SalesOrderLine.organization_id == org_id,
        SalesOrderLine.order_id == order_id
    )
    result = await db.execute(stmt)
    line_number = len(result.scalars().all()) + 1
    
    line_total = Decimal(str(payload.quantity_ordered)) * Decimal(str(payload.unit_price)) * (1 - Decimal(str(payload.discount_percent)) / 100)
    
    line = SalesOrderLine(
        organization_id=org_id,
        order_id=order_id,
        line_number=line_number,
        line_total=line_total,
        **payload.model_dump()
    )
    db.add(line)
    
    # Update order totals
    order_stmt = select(SalesOrder).where(SalesOrder.id == order_id, SalesOrder.organization_id == org_id)
    order_result = await db.execute(order_stmt)
    order = order_result.scalar_one_or_none()
    if order:
        order.subtotal += line_total
        order.total_amount = order.subtotal + order.tax_amount + order.shipping_amount - order.discount_amount
    
    await db.commit()
    await db.refresh(line)
    return line


@router.get("/orders/{order_id}/lines")
async def list_order_lines(
    order_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("sales.orders.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(SalesOrderLine).where(
        SalesOrderLine.organization_id == org_id,
        SalesOrderLine.order_id == order_id
    ).order_by(SalesOrderLine.line_number)
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/orders/{order_id}/confirm")
async def confirm_order(
    order_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("sales.orders.confirm")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(SalesOrder).where(SalesOrder.id == order_id, SalesOrder.organization_id == org_id)
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Sales order not found")
    
    order.status = "confirmed"
    await db.commit()
    await db.refresh(order)
    return order


# Shipments

@router.post("/shipments")
async def create_shipment(
    payload: ShipmentCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("sales.shipments.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate shipment number
    stmt = select(Shipment).where(Shipment.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    shipment_number = f"SHIP-{datetime.now().strftime('%Y%m')}-{count + 1:05d}"
    
    shipment = Shipment(
        organization_id=org_id,
        shipment_number=shipment_number,
        **payload.model_dump()
    )
    db.add(shipment)
    await db.commit()
    await db.refresh(shipment)
    return shipment


@router.get("/shipments")
async def list_shipments(
    order_id: Optional[int] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("sales.shipments.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(Shipment).where(Shipment.organization_id == org_id)
    if order_id:
        query = query.where(Shipment.order_id == order_id)
    if status:
        query = query.where(Shipment.status == status)
    query = query.order_by(Shipment.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/shipments/{shipment_id}/ship")
async def ship_shipment(
    shipment_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("sales.shipments.manage")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(Shipment).where(Shipment.id == shipment_id, Shipment.organization_id == org_id)
    result = await db.execute(stmt)
    shipment = result.scalar_one_or_none()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    
    shipment.status = "shipped"
    shipment.shipped_date = date.today()
    
    # Update order status
    order_stmt = select(SalesOrder).where(
        SalesOrder.id == shipment.order_id,
        SalesOrder.organization_id == org_id
    )
    order_result = await db.execute(order_stmt)
    order = order_result.scalar_one_or_none()
    if order:
        order.status = "shipped"
    
    await db.commit()
    await db.refresh(shipment)
    return shipment
