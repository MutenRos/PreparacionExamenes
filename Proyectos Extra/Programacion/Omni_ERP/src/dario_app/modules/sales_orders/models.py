"""Sales Orders & Quotes models for Quote-to-Cash process."""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class Quote(Base):
    """Sales quotation."""
    __tablename__ = "sales_quotes"
    __table_args__ = (
        Index("idx_quote_org_status", "organization_id", "status"),
        Index("idx_quote_org_customer", "organization_id", "customer_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    quote_number: Mapped[str] = mapped_column(String(50), nullable=False)
    revision: Mapped[int] = mapped_column(Integer, default=1)
    
    customer_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to clientes
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    status: Mapped[str] = mapped_column(String(30), default="draft")  # draft, sent, accepted, rejected, expired
    
    quote_date: Mapped[date] = mapped_column(Date, nullable=False)
    expiration_date: Mapped[date] = mapped_column(Date, nullable=False)
    
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    
    currency: Mapped[str] = mapped_column(String(3), default="EUR")
    
    payment_terms: Mapped[Optional[str]] = mapped_column(String(100))
    delivery_terms: Mapped[Optional[str]] = mapped_column(String(100))
    
    notes: Mapped[Optional[str]] = mapped_column(Text)
    internal_notes: Mapped[Optional[str]] = mapped_column(Text)
    
    owner_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    owner_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Conversion tracking
    converted_to_order: Mapped[bool] = mapped_column(Boolean, default=False)
    order_id: Mapped[Optional[int]] = mapped_column(Integer)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class QuoteLine(Base):
    """Quote line item."""
    __tablename__ = "sales_quote_lines"
    __table_args__ = (
        Index("idx_quoteline_org_quote", "organization_id", "quote_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    quote_id: Mapped[int] = mapped_column(Integer, ForeignKey("sales_quotes.id"), nullable=False)

    line_number: Mapped[int] = mapped_column(Integer, nullable=False)
    
    product_id: Mapped[Optional[int]] = mapped_column(Integer)  # FK to productos
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    quantity: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    discount_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("0"))
    line_total: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    
    delivery_date: Mapped[Optional[date]] = mapped_column(Date)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class SalesOrder(Base):
    """Sales order."""
    __tablename__ = "sales_orders"
    __table_args__ = (
        Index("idx_salesorder_org_status", "organization_id", "status"),
        Index("idx_salesorder_org_customer", "organization_id", "customer_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    order_number: Mapped[str] = mapped_column(String(50), nullable=False)
    
    customer_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to clientes
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    status: Mapped[str] = mapped_column(String(30), default="pending")  # pending, confirmed, processing, shipped, delivered, canceled
    fulfillment_status: Mapped[str] = mapped_column(String(30), default="unfulfilled")  # unfulfilled, partial, fulfilled
    
    order_date: Mapped[date] = mapped_column(Date, nullable=False)
    requested_delivery_date: Mapped[Optional[date]] = mapped_column(Date)
    confirmed_delivery_date: Mapped[Optional[date]] = mapped_column(Date)
    
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    shipping_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    
    currency: Mapped[str] = mapped_column(String(3), default="EUR")
    
    payment_terms: Mapped[Optional[str]] = mapped_column(String(100))
    payment_status: Mapped[str] = mapped_column(String(30), default="pending")  # pending, partial, paid
    
    shipping_address: Mapped[Optional[str]] = mapped_column(Text)
    shipping_city: Mapped[Optional[str]] = mapped_column(String(100))
    shipping_postal_code: Mapped[Optional[str]] = mapped_column(String(20))
    shipping_country: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Reference to quote
    quote_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("sales_quotes.id"))
    
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    owner_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    owner_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SalesOrderLine(Base):
    """Sales order line item."""
    __tablename__ = "sales_order_lines"
    __table_args__ = (
        Index("idx_orderline_org_order", "organization_id", "order_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("sales_orders.id"), nullable=False)

    line_number: Mapped[int] = mapped_column(Integer, nullable=False)
    
    product_id: Mapped[Optional[int]] = mapped_column(Integer)  # FK to productos
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    quantity_ordered: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    quantity_shipped: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    quantity_invoiced: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    discount_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("0"))
    line_total: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    
    delivery_date: Mapped[Optional[date]] = mapped_column(Date)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Shipment(Base):
    """Order shipment."""
    __tablename__ = "sales_shipments"
    __table_args__ = (
        Index("idx_shipment_org_order", "organization_id", "order_id"),
        Index("idx_shipment_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("sales_orders.id"), nullable=False)

    shipment_number: Mapped[str] = mapped_column(String(50), nullable=False)
    
    status: Mapped[str] = mapped_column(String(30), default="preparing")  # preparing, shipped, in_transit, delivered, returned
    
    shipped_date: Mapped[Optional[date]] = mapped_column(Date)
    delivered_date: Mapped[Optional[date]] = mapped_column(Date)
    
    carrier: Mapped[Optional[str]] = mapped_column(String(100))
    tracking_number: Mapped[Optional[str]] = mapped_column(String(100))
    
    shipping_cost: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ShipmentLine(Base):
    """Shipment line item."""
    __tablename__ = "sales_shipment_lines"
    __table_args__ = (
        Index("idx_shipmentline_org_shipment", "organization_id", "shipment_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    shipment_id: Mapped[int] = mapped_column(Integer, ForeignKey("sales_shipments.id"), nullable=False)
    order_line_id: Mapped[int] = mapped_column(Integer, ForeignKey("sales_order_lines.id"), nullable=False)

    product_id: Mapped[Optional[int]] = mapped_column(Integer)
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    quantity: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
