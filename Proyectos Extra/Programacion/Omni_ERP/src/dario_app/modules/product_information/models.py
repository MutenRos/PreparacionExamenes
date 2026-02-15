"""Product Information Management models."""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class ProductCategory(Base):
    """Product category hierarchy."""
    __tablename__ = "pim_categories"
    __table_args__ = (
        Index("idx_pimcat_org_parent", "organization_id", "parent_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    category_code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    
    # Hierarchy
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("pim_categories.id"))
    level: Mapped[int] = mapped_column(Integer, default=1)
    path: Mapped[Optional[str]] = mapped_column(String(500))  # /1/5/12/
    
    # Display
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ProductAttribute(Base):
    """Product attribute definition (e.g., Color, Size, Material)."""
    __tablename__ = "pim_attributes"
    __table_args__ = (
        Index("idx_pimattr_org_code", "organization_id", "attribute_code"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    attribute_code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    
    data_type: Mapped[str] = mapped_column(String(20), default="text")  # text, number, boolean, date, select, multiselect
    
    # For select types
    allowed_values: Mapped[Optional[str]] = mapped_column(Text)  # JSON array
    
    # Validation
    is_required: Mapped[bool] = mapped_column(Boolean, default=False)
    is_unique: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Display
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    is_searchable: Mapped[bool] = mapped_column(Boolean, default=True)
    is_filterable: Mapped[bool] = mapped_column(Boolean, default=True)
    
    status: Mapped[str] = mapped_column(String(20), default="active")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ProductAttributeValue(Base):
    """Product attribute value."""
    __tablename__ = "pim_attribute_values"
    __table_args__ = (
        Index("idx_pimattrval_org_product", "organization_id", "product_id"),
        Index("idx_pimattrval_org_attribute", "organization_id", "attribute_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    product_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to productos
    attribute_id: Mapped[int] = mapped_column(Integer, ForeignKey("pim_attributes.id"), nullable=False)
    
    value_text: Mapped[Optional[str]] = mapped_column(Text)
    value_number: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 4))
    value_boolean: Mapped[Optional[bool]] = mapped_column(Boolean)
    value_date: Mapped[Optional[date]] = mapped_column(Date)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ProductMedia(Base):
    """Product media (images, videos, documents)."""
    __tablename__ = "pim_media"
    __table_args__ = (
        Index("idx_pimmedia_org_product", "organization_id", "product_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    product_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to productos
    
    media_type: Mapped[str] = mapped_column(String(20), default="image")  # image, video, document, 3d_model
    
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_url: Mapped[Optional[str]] = mapped_column(String(500))
    
    title: Mapped[Optional[str]] = mapped_column(String(255))
    alt_text: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Display
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Metadata
    file_size_bytes: Mapped[Optional[int]] = mapped_column(Integer)
    mime_type: Mapped[Optional[str]] = mapped_column(String(100))
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ProductRelationship(Base):
    """Product relationships (cross-sell, upsell, accessories)."""
    __tablename__ = "pim_relationships"
    __table_args__ = (
        Index("idx_pimrel_org_product", "organization_id", "product_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    product_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to productos
    related_product_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to productos
    
    relationship_type: Mapped[str] = mapped_column(String(30), default="related")  # related, cross_sell, upsell, accessory, substitute, bundle
    
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ProductVariant(Base):
    """Product variant (e.g., size/color combinations)."""
    __tablename__ = "pim_variants"
    __table_args__ = (
        Index("idx_pimvar_org_parent", "organization_id", "parent_product_id"),
        Index("idx_pimvar_org_sku", "organization_id", "sku"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    parent_product_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to productos (parent)
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to productos (variant)
    
    sku: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Variant attributes (JSON)
    variant_attributes: Mapped[str] = mapped_column(Text, nullable=False)  # {"color": "red", "size": "L"}
    
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ProductChannelListing(Base):
    """Product listing per sales channel."""
    __tablename__ = "pim_channel_listings"
    __table_args__ = (
        Index("idx_pimchannel_org_product", "organization_id", "product_id"),
        Index("idx_pimchannel_org_channel", "organization_id", "channel_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    product_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to productos
    channel_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to sales channels
    
    channel_name: Mapped[str] = mapped_column(String(100), nullable=False)  # web, amazon, ebay, store
    
    # Channel-specific data
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    channel_title: Mapped[Optional[str]] = mapped_column(String(255))
    channel_description: Mapped[Optional[str]] = mapped_column(Text)
    channel_sku: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Pricing per channel
    channel_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    channel_compare_at_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ProductLocalization(Base):
    """Product localization for different languages/regions."""
    __tablename__ = "pim_localizations"
    __table_args__ = (
        Index("idx_pimloc_org_product", "organization_id", "product_id"),
        Index("idx_pimloc_org_locale", "organization_id", "locale"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    product_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to productos
    
    locale: Mapped[str] = mapped_column(String(10), nullable=False)  # en_US, es_ES, fr_FR
    
    localized_name: Mapped[str] = mapped_column(String(255), nullable=False)
    localized_description: Mapped[Optional[str]] = mapped_column(Text)
    localized_short_description: Mapped[Optional[str]] = mapped_column(Text)
    
    # SEO
    meta_title: Mapped[Optional[str]] = mapped_column(String(255))
    meta_description: Mapped[Optional[str]] = mapped_column(Text)
    meta_keywords: Mapped[Optional[str]] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ProductPriceHistory(Base):
    """Product price change history."""
    __tablename__ = "pim_price_history"
    __table_args__ = (
        Index("idx_pimprice_org_product", "organization_id", "product_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    product_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to productos
    
    old_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    new_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    price_change: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    price_change_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    
    change_reason: Mapped[Optional[str]] = mapped_column(String(255))
    
    changed_by_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    changed_by_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    effective_date: Mapped[date] = mapped_column(Date, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
