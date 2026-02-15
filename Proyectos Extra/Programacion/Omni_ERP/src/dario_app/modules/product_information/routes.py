"""Product Information Management routes."""

from datetime import datetime, date
from typing import Optional
from decimal import Decimal
import json

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import require_permission, get_tenant_db, get_org_id
from dario_app.modules.usuarios.models import Usuario

from .models import (
    ProductCategory, ProductAttribute, ProductAttributeValue,
    ProductMedia, ProductRelationship, ProductVariant,
    ProductChannelListing, ProductLocalization, ProductPriceHistory
)

router = APIRouter(prefix="/api/pim", tags=["Product Information Management"])


# Schemas

class CategoryCreate(BaseModel):
    name: str
    descripcion: Optional[str] = None
    parent_id: Optional[int] = None


class AttributeCreate(BaseModel):
    name: str
    data_type: str = "text"
    allowed_values: Optional[str] = None
    is_required: bool = False


class AttributeValueCreate(BaseModel):
    product_id: int
    attribute_id: int
    value_text: Optional[str] = None
    value_number: Optional[Decimal] = None
    value_boolean: Optional[bool] = None


class MediaCreate(BaseModel):
    product_id: int
    media_type: str = "image"
    file_name: str
    file_path: str
    title: Optional[str] = None
    is_primary: bool = False


class RelationshipCreate(BaseModel):
    product_id: int
    related_product_id: int
    relationship_type: str = "related"


class ChannelListingCreate(BaseModel):
    product_id: int
    channel_id: int
    channel_name: str
    is_published: bool = False
    channel_price: Optional[Decimal] = None


# Categories

@router.post("/categories")
async def create_category(
    payload: CategoryCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("pim.categories.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate category code
    stmt = select(ProductCategory).where(ProductCategory.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    category_code = f"CAT-{count + 1:04d}"
    
    # Calculate level
    level = 1
    path = ""
    if payload.parent_id:
        parent_stmt = select(ProductCategory).where(
            ProductCategory.id == payload.parent_id,
            ProductCategory.organization_id == org_id
        )
        parent_result = await db.execute(parent_stmt)
        parent = parent_result.scalar_one_or_none()
        if parent:
            level = parent.level + 1
            path = f"{parent.path}{parent.id}/"
    
    category = ProductCategory(
        organization_id=org_id,
        category_code=category_code,
        level=level,
        path=path,
        **payload.model_dump()
    )
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


@router.get("/categories")
async def list_categories(
    parent_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("pim.categories.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(ProductCategory).where(ProductCategory.organization_id == org_id)
    if parent_id is not None:
        query = query.where(ProductCategory.parent_id == parent_id)
    if is_active is not None:
        query = query.where(ProductCategory.is_active == is_active)
    query = query.order_by(ProductCategory.display_order, ProductCategory.name)
    result = await db.execute(query)
    return result.scalars().all()


# Attributes

@router.post("/attributes")
async def create_attribute(
    payload: AttributeCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("pim.attributes.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate attribute code from name
    attribute_code = payload.name.lower().replace(" ", "_")
    
    attribute = ProductAttribute(
        organization_id=org_id,
        attribute_code=attribute_code,
        **payload.model_dump()
    )
    db.add(attribute)
    await db.commit()
    await db.refresh(attribute)
    return attribute


@router.get("/attributes")
async def list_attributes(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("pim.attributes.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(ProductAttribute).where(ProductAttribute.organization_id == org_id)
    if status:
        query = query.where(ProductAttribute.status == status)
    query = query.order_by(ProductAttribute.display_order)
    result = await db.execute(query)
    return result.scalars().all()


# Attribute Values

@router.post("/attribute-values")
async def set_attribute_value(
    payload: AttributeValueCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("pim.products.edit")),
    org_id: int = Depends(get_org_id),
):
    # Check if value already exists
    stmt = select(ProductAttributeValue).where(
        ProductAttributeValue.organization_id == org_id,
        ProductAttributeValue.product_id == payload.product_id,
        ProductAttributeValue.attribute_id == payload.attribute_id
    )
    result = await db.execute(stmt)
    value = result.scalar_one_or_none()
    
    if value:
        # Update existing
        value.value_text = payload.value_text
        value.value_number = payload.value_number
        value.value_boolean = payload.value_boolean
        value.updated_at = datetime.utcnow()
    else:
        # Create new
        value = ProductAttributeValue(
            organization_id=org_id,
            **payload.model_dump()
        )
        db.add(value)
    
    await db.commit()
    await db.refresh(value)
    return value


@router.get("/products/{product_id}/attributes")
async def get_product_attributes(
    product_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("pim.products.read")),
    org_id: int = Depends(get_org_id),
):
    """Get all attribute values for a product."""
    query = select(ProductAttributeValue).where(
        ProductAttributeValue.organization_id == org_id,
        ProductAttributeValue.product_id == product_id
    )
    result = await db.execute(query)
    return result.scalars().all()


# Media

@router.post("/media")
async def add_media(
    payload: MediaCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("pim.media.create")),
    org_id: int = Depends(get_org_id),
):
    # If this is primary, unset other primary images
    if payload.is_primary:
        stmt = select(ProductMedia).where(
            ProductMedia.organization_id == org_id,
            ProductMedia.product_id == payload.product_id,
            ProductMedia.is_primary == True
        )
        result = await db.execute(stmt)
        for media in result.scalars().all():
            media.is_primary = False
    
    media = ProductMedia(
        organization_id=org_id,
        **payload.model_dump()
    )
    db.add(media)
    await db.commit()
    await db.refresh(media)
    return media


@router.get("/products/{product_id}/media")
async def get_product_media(
    product_id: int,
    media_type: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("pim.media.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(ProductMedia).where(
        ProductMedia.organization_id == org_id,
        ProductMedia.product_id == product_id
    )
    if media_type:
        query = query.where(ProductMedia.media_type == media_type)
    query = query.order_by(ProductMedia.display_order)
    result = await db.execute(query)
    return result.scalars().all()


# Relationships

@router.post("/relationships")
async def create_relationship(
    payload: RelationshipCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("pim.relationships.create")),
    org_id: int = Depends(get_org_id),
):
    relationship = ProductRelationship(
        organization_id=org_id,
        **payload.model_dump()
    )
    db.add(relationship)
    await db.commit()
    await db.refresh(relationship)
    return relationship


@router.get("/products/{product_id}/relationships")
async def get_product_relationships(
    product_id: int,
    relationship_type: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("pim.relationships.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(ProductRelationship).where(
        ProductRelationship.organization_id == org_id,
        ProductRelationship.product_id == product_id
    )
    if relationship_type:
        query = query.where(ProductRelationship.relationship_type == relationship_type)
    query = query.order_by(ProductRelationship.display_order)
    result = await db.execute(query)
    return result.scalars().all()


# Variants

@router.get("/products/{product_id}/variants")
async def get_product_variants(
    product_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("pim.variants.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(ProductVariant).where(
        ProductVariant.organization_id == org_id,
        ProductVariant.parent_product_id == product_id
    ).order_by(ProductVariant.display_order)
    result = await db.execute(query)
    return result.scalars().all()


# Channel Listings

@router.post("/channel-listings")
async def create_channel_listing(
    payload: ChannelListingCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("pim.channels.create")),
    org_id: int = Depends(get_org_id),
):
    listing = ProductChannelListing(
        organization_id=org_id,
        **payload.model_dump()
    )
    db.add(listing)
    await db.commit()
    await db.refresh(listing)
    return listing


@router.get("/products/{product_id}/channels")
async def get_product_channels(
    product_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("pim.channels.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(ProductChannelListing).where(
        ProductChannelListing.organization_id == org_id,
        ProductChannelListing.product_id == product_id
    )
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/channel-listings/{listing_id}/publish")
async def publish_to_channel(
    listing_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("pim.channels.manage")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(ProductChannelListing).where(
        ProductChannelListing.id == listing_id,
        ProductChannelListing.organization_id == org_id
    )
    result = await db.execute(stmt)
    listing = result.scalar_one_or_none()
    
    if not listing:
        raise HTTPException(status_code=404, detail="Channel listing not found")
    
    listing.is_published = True
    listing.published_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(listing)
    return listing


# Localization

@router.get("/products/{product_id}/localizations")
async def get_product_localizations(
    product_id: int,
    locale: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("pim.localizations.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(ProductLocalization).where(
        ProductLocalization.organization_id == org_id,
        ProductLocalization.product_id == product_id
    )
    if locale:
        query = query.where(ProductLocalization.locale == locale)
    result = await db.execute(query)
    return result.scalars().all()


# Price History

@router.get("/products/{product_id}/price-history")
async def get_price_history(
    product_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("pim.price_history.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(ProductPriceHistory).where(
        ProductPriceHistory.organization_id == org_id,
        ProductPriceHistory.product_id == product_id
    ).order_by(ProductPriceHistory.effective_date.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/products/{product_id}/record-price-change")
async def record_price_change(
    product_id: int,
    old_price: Decimal,
    new_price: Decimal,
    change_reason: Optional[str] = None,
    effective_date: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("pim.price_history.create")),
    org_id: int = Depends(get_org_id),
):
    """Record a price change in history."""
    price_change = new_price - old_price
    price_change_percent = (price_change / old_price * 100) if old_price > 0 else Decimal("0")
    
    eff_date = datetime.strptime(effective_date, "%Y-%m-%d").date() if effective_date else date.today()
    
    history = ProductPriceHistory(
        organization_id=org_id,
        product_id=product_id,
        old_price=old_price,
        new_price=new_price,
        price_change=price_change,
        price_change_percent=price_change_percent,
        change_reason=change_reason,
        changed_by_user_id=user.id,
        changed_by_name=user.nombre_completo,
        effective_date=eff_date
    )
    db.add(history)
    await db.commit()
    await db.refresh(history)
    return history


# Analytics

@router.get("/analytics/category-distribution")
async def get_category_distribution(
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("pim.analytics.read")),
    org_id: int = Depends(get_org_id),
):
    """Get product count by category."""
    # This would require joining with products table
    # Simplified version - just return categories
    stmt = select(ProductCategory).where(
        ProductCategory.organization_id == org_id,
        ProductCategory.is_active == True
    )
    result = await db.execute(stmt)
    categories = result.scalars().all()
    
    return {
        "total_categories": len(categories),
        "categories": [{"id": c.id, "name": c.name, "code": c.category_code} for c in categories]
    }


@router.get("/analytics/media-stats")
async def get_media_stats(
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("pim.analytics.read")),
    org_id: int = Depends(get_org_id),
):
    """Get media statistics."""
    stmt = select(ProductMedia).where(ProductMedia.organization_id == org_id)
    result = await db.execute(stmt)
    media = result.scalars().all()
    
    by_type = {}
    total_size = 0
    for m in media:
        media_type = m.media_type
        by_type[media_type] = by_type.get(media_type, 0) + 1
        if m.file_size_bytes:
            total_size += m.file_size_bytes
    
    return {
        "total_media": len(media),
        "by_type": by_type,
        "total_size_mb": round(total_size / (1024 * 1024), 2)
    }
