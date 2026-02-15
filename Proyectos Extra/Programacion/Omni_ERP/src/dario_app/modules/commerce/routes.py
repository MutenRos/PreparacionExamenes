"""Commerce routes - Catalogs, Price Lists, Discounts, Online Orders."""

from datetime import datetime
from typing import List, Optional
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import require_permission, get_tenant_db, get_org_id
from dario_app.modules.usuarios.models import Usuario

from .models import (
    Catalog, CatalogProduct, PriceList, PriceListItem, 
    Discount, OnlineOrder, OnlineOrderLine, CustomerReview
)

router = APIRouter(prefix="/api/commerce", tags=["Commerce"])


# Schemas

class CatalogCreate(BaseModel):
    name: str
    descripcion: Optional[str] = None
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None
    is_public: bool = True


class PriceListCreate(BaseModel):
    name: str
    descripcion: Optional[str] = None
    currency: str = "EUR"
    priority: int = 0
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None


class PriceListItemCreate(BaseModel):
    product_id: int
    unit_price: float
    discount_percent: float = 0
    min_quantity: int = 1


class DiscountCreate(BaseModel):
    name: str
    descripcion: Optional[str] = None
    discount_type: str = "percentage"
    discount_value: float
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None
    min_purchase_amount: float = 0
    max_uses: Optional[int] = None


class OnlineOrderCreate(BaseModel):
    customer_email: str
    customer_name: str
    customer_id: Optional[int] = None
    shipping_address: Optional[str] = None
    shipping_city: Optional[str] = None
    shipping_postal_code: Optional[str] = None
    shipping_country: Optional[str] = None


class OnlineOrderLineCreate(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    unit_price: float
    discount_percent: float = 0


class ReviewCreate(BaseModel):
    product_id: int
    customer_name: str
    customer_id: Optional[int] = None
    rating: int
    title: str
    comment: str


# Catalogs

@router.post("/catalogs")
async def create_catalog(
    payload: CatalogCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("commerce.catalogs.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate catalog code
    stmt = select(Catalog).where(Catalog.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    catalog_code = f"CAT-{count + 1:04d}"
    
    catalog = Catalog(
        organization_id=org_id,
        catalog_code=catalog_code,
        **payload.model_dump()
    )
    db.add(catalog)
    await db.commit()
    await db.refresh(catalog)
    return catalog


@router.get("/catalogs")
async def list_catalogs(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("commerce.catalogs.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(Catalog).where(Catalog.organization_id == org_id)
    if status:
        query = query.where(Catalog.status == status)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/catalogs/{catalog_id}/products")
async def add_product_to_catalog(
    catalog_id: int,
    product_id: int,
    display_order: int = 0,
    is_featured: bool = False,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("commerce.catalogs.manage")),
    org_id: int = Depends(get_org_id),
):
    catalog_product = CatalogProduct(
        organization_id=org_id,
        catalog_id=catalog_id,
        product_id=product_id,
        display_order=display_order,
        is_featured=is_featured
    )
    db.add(catalog_product)
    await db.commit()
    await db.refresh(catalog_product)
    return catalog_product


@router.get("/catalogs/{catalog_id}/products")
async def list_catalog_products(
    catalog_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("commerce.catalogs.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(CatalogProduct).where(
        CatalogProduct.organization_id == org_id,
        CatalogProduct.catalog_id == catalog_id
    ).order_by(CatalogProduct.display_order, CatalogProduct.id)
    result = await db.execute(query)
    return result.scalars().all()


# Price Lists

@router.post("/price-lists")
async def create_price_list(
    payload: PriceListCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("commerce.pricing.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate price list code
    stmt = select(PriceList).where(PriceList.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    price_list_code = f"PL-{count + 1:04d}"
    
    price_list = PriceList(
        organization_id=org_id,
        price_list_code=price_list_code,
        **payload.model_dump()
    )
    db.add(price_list)
    await db.commit()
    await db.refresh(price_list)
    return price_list


@router.get("/price-lists")
async def list_price_lists(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("commerce.pricing.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(PriceList).where(PriceList.organization_id == org_id)
    if status:
        query = query.where(PriceList.status == status)
    query = query.order_by(PriceList.priority.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/price-lists/{price_list_id}/items")
async def add_price_list_item(
    price_list_id: int,
    payload: PriceListItemCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("commerce.pricing.manage")),
    org_id: int = Depends(get_org_id),
):
    item = PriceListItem(
        organization_id=org_id,
        price_list_id=price_list_id,
        **payload.model_dump()
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router.get("/price-lists/{price_list_id}/items")
async def list_price_list_items(
    price_list_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("commerce.pricing.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(PriceListItem).where(
        PriceListItem.organization_id == org_id,
        PriceListItem.price_list_id == price_list_id
    )
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/products/{product_id}/price")
async def get_product_price(
    product_id: int,
    price_list_id: Optional[int] = None,
    quantity: int = 1,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id),
):
    """Get effective price for a product."""
    query = select(PriceListItem).where(
        PriceListItem.organization_id == org_id,
        PriceListItem.product_id == product_id,
        PriceListItem.min_quantity <= quantity
    )
    
    if price_list_id:
        query = query.where(PriceListItem.price_list_id == price_list_id)
    
    result = await db.execute(query)
    items = result.scalars().all()
    
    if not items:
        return {"product_id": product_id, "price": None}
    
    # Find best price
    best_item = min(items, key=lambda x: x.unit_price * (1 - x.discount_percent / 100))
    
    return {
        "product_id": product_id,
        "price": float(best_item.unit_price),
        "discount_percent": float(best_item.discount_percent),
        "effective_price": float(best_item.unit_price * (1 - best_item.discount_percent / 100))
    }


# Discounts

@router.post("/discounts")
async def create_discount(
    payload: DiscountCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("commerce.discounts.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate discount code
    stmt = select(Discount).where(Discount.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    discount_code = f"DISC-{count + 1:04d}"
    
    discount = Discount(
        organization_id=org_id,
        discount_code=discount_code,
        **payload.model_dump()
    )
    db.add(discount)
    await db.commit()
    await db.refresh(discount)
    return discount


@router.get("/discounts")
async def list_discounts(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("commerce.discounts.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(Discount).where(Discount.organization_id == org_id)
    if status:
        query = query.where(Discount.status == status)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/discounts/{code}/validate")
async def validate_discount(
    code: str,
    order_amount: float,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id),
):
    """Validate if a discount code is applicable."""
    stmt = select(Discount).where(
        Discount.organization_id == org_id,
        Discount.discount_code == code,
        Discount.status == "active"
    )
    result = await db.execute(stmt)
    discount = result.scalar_one_or_none()
    
    if not discount:
        return {"valid": False, "message": "Invalid discount code"}
    
    if discount.min_purchase_amount > Decimal(str(order_amount)):
        return {"valid": False, "message": f"Minimum purchase amount is €{discount.min_purchase_amount}"}
    
    if discount.max_uses and discount.uses_count >= discount.max_uses:
        return {"valid": False, "message": "Discount code has reached maximum uses"}
    
    # Calculate discount amount
    if discount.discount_type == "percentage":
        discount_amount = Decimal(str(order_amount)) * (discount.discount_value / 100)
    else:
        discount_amount = discount.discount_value
    
    return {
        "valid": True,
        "discount_type": discount.discount_type,
        "discount_value": float(discount.discount_value),
        "discount_amount": float(discount_amount)
    }


# Online Orders

@router.post("/online-orders")
async def create_online_order(
    payload: OnlineOrderCreate,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id),
):
    # Generate order number
    stmt = select(OnlineOrder).where(OnlineOrder.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    order_number = f"WEB-{datetime.now().strftime('%Y%m')}-{count + 1:05d}"
    
    order = OnlineOrder(
        organization_id=org_id,
        order_number=order_number,
        **payload.model_dump()
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


@router.get("/online-orders")
async def list_online_orders(
    status: Optional[str] = None,
    payment_status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("commerce.orders.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(OnlineOrder).where(OnlineOrder.organization_id == org_id)
    if status:
        query = query.where(OnlineOrder.status == status)
    if payment_status:
        query = query.where(OnlineOrder.payment_status == payment_status)
    query = query.order_by(OnlineOrder.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/online-orders/{order_id}/lines")
async def add_order_line(
    order_id: int,
    payload: OnlineOrderLineCreate,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id),
):
    line_total = Decimal(str(payload.unit_price)) * payload.quantity * (1 - Decimal(str(payload.discount_percent)) / 100)
    
    line = OnlineOrderLine(
        organization_id=org_id,
        order_id=order_id,
        line_total=line_total,
        **payload.model_dump()
    )
    db.add(line)
    
    # Update order totals
    stmt = select(OnlineOrder).where(
        OnlineOrder.id == order_id,
        OnlineOrder.organization_id == org_id
    )
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()
    if order:
        order.subtotal += line_total
        order.total_amount = order.subtotal + order.tax_amount + order.shipping_amount - order.discount_amount
    
    await db.commit()
    await db.refresh(line)
    return line


@router.get("/online-orders/{order_id}/lines")
async def list_order_lines(
    order_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id),
):
    query = select(OnlineOrderLine).where(
        OnlineOrderLine.organization_id == org_id,
        OnlineOrderLine.order_id == order_id
    )
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/online-orders/{order_id}/confirm")
async def confirm_order(
    order_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("commerce.orders.manage")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(OnlineOrder).where(
        OnlineOrder.id == order_id,
        OnlineOrder.organization_id == org_id
    )
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = "confirmed"
    await db.commit()
    await db.refresh(order)
    return order


# Customer Reviews

@router.post("/reviews")
async def create_review(
    payload: ReviewCreate,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id),
):
    review = CustomerReview(
        organization_id=org_id,
        **payload.model_dump()
    )
    db.add(review)
    await db.commit()
    await db.refresh(review)
    return review


@router.get("/reviews")
async def list_reviews(
    product_id: Optional[int] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id),
):
    query = select(CustomerReview).where(CustomerReview.organization_id == org_id)
    if product_id:
        query = query.where(CustomerReview.product_id == product_id)
    if status:
        query = query.where(CustomerReview.status == status)
    query = query.order_by(CustomerReview.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/reviews/{review_id}/approve")
async def approve_review(
    review_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("commerce.reviews.moderate")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(CustomerReview).where(
        CustomerReview.id == review_id,
        CustomerReview.organization_id == org_id
    )
    result = await db.execute(stmt)
    review = result.scalar_one_or_none()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    review.status = "approved"
    review.moderated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(review)
    return review
