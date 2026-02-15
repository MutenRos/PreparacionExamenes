"""Commerce models for retail, catalogs, and pricing."""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class Catalog(Base):
    """Product catalog."""
    __tablename__ = "commerce_catalogs"
    __table_args__ = (
        Index("idx_commerce_catalog_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    catalog_code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    
    status: Mapped[str] = mapped_column(String(30), default="active")  # active, inactive
    
    valid_from: Mapped[Optional[date]] = mapped_column(Date)
    valid_to: Mapped[Optional[date]] = mapped_column(Date)
    
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CatalogProduct(Base):
    """Products in a catalog."""
    __tablename__ = "commerce_catalog_products"
    __table_args__ = (
        Index("idx_commerce_catalog_prod_org_catalog", "organization_id", "catalog_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    catalog_id: Mapped[int] = mapped_column(Integer, ForeignKey("commerce_catalogs.id"), nullable=False)

    product_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to productos
    
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PriceList(Base):
    """Price list for different customer segments."""
    __tablename__ = "commerce_price_lists"
    __table_args__ = (
        Index("idx_commerce_pricelist_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    price_list_code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    
    status: Mapped[str] = mapped_column(String(30), default="active")  # active, inactive
    currency: Mapped[str] = mapped_column(String(3), default="EUR")
    
    valid_from: Mapped[Optional[date]] = mapped_column(Date)
    valid_to: Mapped[Optional[date]] = mapped_column(Date)
    
    # Priority for price resolution
    priority: Mapped[int] = mapped_column(Integer, default=0)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PriceListItem(Base):
    """Individual product prices in a price list."""
    __tablename__ = "commerce_price_list_items"
    __table_args__ = (
        Index("idx_commerce_priceitem_org_list", "organization_id", "price_list_id"),
        Index("idx_commerce_priceitem_org_product", "organization_id", "product_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    price_list_id: Mapped[int] = mapped_column(Integer, ForeignKey("commerce_price_lists.id"), nullable=False)

    product_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to productos
    
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    discount_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("0"))
    
    min_quantity: Mapped[int] = mapped_column(Integer, default=1)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Discount(Base):
    """Promotional discount."""
    __tablename__ = "commerce_discounts"
    __table_args__ = (
        Index("idx_commerce_discount_org_status", "organization_id", "status"),
        Index("idx_commerce_discount_org_code", "organization_id", "discount_code"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    discount_code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    
    discount_type: Mapped[str] = mapped_column(String(30), default="percentage")  # percentage, fixed_amount
    discount_value: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    
    status: Mapped[str] = mapped_column(String(30), default="active")  # active, inactive, expired
    
    valid_from: Mapped[Optional[date]] = mapped_column(Date)
    valid_to: Mapped[Optional[date]] = mapped_column(Date)
    
    min_purchase_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    max_uses: Mapped[Optional[int]] = mapped_column(Integer)
    uses_count: Mapped[int] = mapped_column(Integer, default=0)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class OnlineOrder(Base):
    """eCommerce/online order."""
    __tablename__ = "commerce_online_orders"
    __table_args__ = (
        Index("idx_commerce_order_org_status", "organization_id", "status"),
        Index("idx_commerce_order_org_customer", "organization_id", "customer_email"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    order_number: Mapped[str] = mapped_column(String(50), nullable=False)
    
    customer_id: Mapped[Optional[int]] = mapped_column(Integer)  # FK to clientes
    customer_email: Mapped[str] = mapped_column(String(255), nullable=False)
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    status: Mapped[str] = mapped_column(String(30), default="pending")  # pending, confirmed, shipped, delivered, canceled
    payment_status: Mapped[str] = mapped_column(String(30), default="pending")  # pending, paid, failed, refunded
    
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    shipping_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    
    discount_code: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Shipping
    shipping_address: Mapped[Optional[str]] = mapped_column(Text)
    shipping_city: Mapped[Optional[str]] = mapped_column(String(100))
    shipping_postal_code: Mapped[Optional[str]] = mapped_column(String(20))
    shipping_country: Mapped[Optional[str]] = mapped_column(String(100))
    
    tracking_number: Mapped[Optional[str]] = mapped_column(String(100))
    
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class OnlineOrderLine(Base):
    """Line item in an online order."""
    __tablename__ = "commerce_online_order_lines"
    __table_args__ = (
        Index("idx_commerce_orderline_org_order", "organization_id", "order_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("commerce_online_orders.id"), nullable=False)

    product_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to productos
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    discount_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("0"))
    line_total: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CustomerReview(Base):
    """Product review."""
    __tablename__ = "commerce_customer_reviews"
    __table_args__ = (
        Index("idx_commerce_review_org_product", "organization_id", "product_id"),
        Index("idx_commerce_review_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    product_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to productos
    customer_id: Mapped[Optional[int]] = mapped_column(Integer)  # FK to clientes
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    rating: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-5
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    
    status: Mapped[str] = mapped_column(String(30), default="pending")  # pending, approved, rejected
    
    helpful_count: Mapped[int] = mapped_column(Integer, default=0)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    moderated_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
