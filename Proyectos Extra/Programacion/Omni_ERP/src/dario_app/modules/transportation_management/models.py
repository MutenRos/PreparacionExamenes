"""Transportation Management System models."""

from datetime import datetime, date, time
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, Time, Index
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class Carrier(Base):
    """Shipping carrier/transport company."""
    __tablename__ = "tms_carriers"
    __table_args__ = (
        Index("idx_tmscarrier_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    carrier_code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    carrier_type: Mapped[str] = mapped_column(String(30), default="ground")  # ground, air, sea, rail, courier
    
    contact_name: Mapped[Optional[str]] = mapped_column(String(255))
    phone: Mapped[Optional[str]] = mapped_column(String(50))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    website: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Pricing
    base_rate: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"))
    per_km_rate: Mapped[Decimal] = mapped_column(Numeric(10, 4), default=Decimal("0"))
    per_kg_rate: Mapped[Decimal] = mapped_column(Numeric(10, 4), default=Decimal("0"))
    
    # Performance
    on_time_delivery_rate: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("0"))  # %
    avg_rating: Mapped[Decimal] = mapped_column(Numeric(3, 2), default=Decimal("0"))  # 0-5
    
    status: Mapped[str] = mapped_column(String(20), default="active")  # active, inactive
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TransportRoute(Base):
    """Predefined transport route."""
    __tablename__ = "tms_routes"
    __table_args__ = (
        Index("idx_tmsroute_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    route_code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    origin: Mapped[str] = mapped_column(String(255), nullable=False)
    destination: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Intermediate stops (JSON array)
    stops: Mapped[Optional[str]] = mapped_column(Text)
    
    distance_km: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"))
    estimated_duration_hours: Mapped[Decimal] = mapped_column(Numeric(8, 2), default=Decimal("0"))
    
    # Preferred carrier
    preferred_carrier_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("tms_carriers.id"))
    
    status: Mapped[str] = mapped_column(String(20), default="active")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class FreightOrder(Base):
    """Freight/shipment order."""
    __tablename__ = "tms_freight_orders"
    __table_args__ = (
        Index("idx_tmsfreight_org_status", "organization_id", "status"),
        Index("idx_tmsfreight_org_carrier", "organization_id", "carrier_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    freight_number: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # References
    sales_order_id: Mapped[Optional[int]] = mapped_column(Integer)
    purchase_order_id: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Routing
    route_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("tms_routes.id"))
    carrier_id: Mapped[int] = mapped_column(Integer, ForeignKey("tms_carriers.id"), nullable=False)
    
    # Origin/Destination
    origin_address: Mapped[str] = mapped_column(Text, nullable=False)
    destination_address: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Shipping details
    service_type: Mapped[str] = mapped_column(String(50), default="standard")  # standard, express, overnight
    
    scheduled_pickup_date: Mapped[date] = mapped_column(Date, nullable=False)
    scheduled_delivery_date: Mapped[date] = mapped_column(Date, nullable=False)
    
    actual_pickup_date: Mapped[Optional[date]] = mapped_column(Date)
    actual_delivery_date: Mapped[Optional[date]] = mapped_column(Date)
    
    # Package details
    total_weight_kg: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"))
    total_volume_m3: Mapped[Decimal] = mapped_column(Numeric(10, 3), default=Decimal("0"))
    package_count: Mapped[int] = mapped_column(Integer, default=1)
    
    # Tracking
    tracking_number: Mapped[Optional[str]] = mapped_column(String(100))
    current_location: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Costs
    freight_cost: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"))
    fuel_surcharge: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"))
    additional_charges: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"))
    total_cost: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"))
    
    # Status
    status: Mapped[str] = mapped_column(String(30), default="pending")  # pending, scheduled, in_transit, delivered, cancelled
    
    # Special handling
    requires_signature: Mapped[bool] = mapped_column(Boolean, default=False)
    is_fragile: Mapped[bool] = mapped_column(Boolean, default=False)
    is_hazardous: Mapped[bool] = mapped_column(Boolean, default=False)
    temperature_controlled: Mapped[bool] = mapped_column(Boolean, default=False)
    
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LoadPlan(Base):
    """Load planning for vehicles."""
    __tablename__ = "tms_load_plans"
    __table_args__ = (
        Index("idx_tmsload_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    load_number: Mapped[str] = mapped_column(String(50), nullable=False)
    
    vehicle_id: Mapped[Optional[int]] = mapped_column(Integer)  # FK to assets/vehicles
    driver_id: Mapped[Optional[int]] = mapped_column(Integer)  # FK to employees
    
    # Capacity
    max_weight_kg: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"))
    max_volume_m3: Mapped[Decimal] = mapped_column(Numeric(10, 3), default=Decimal("0"))
    
    current_weight_kg: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"))
    current_volume_m3: Mapped[Decimal] = mapped_column(Numeric(10, 3), default=Decimal("0"))
    
    # Utilization %
    weight_utilization: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("0"))
    volume_utilization: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("0"))
    
    planned_date: Mapped[date] = mapped_column(Date, nullable=False)
    
    status: Mapped[str] = mapped_column(String(30), default="planning")  # planning, optimized, dispatched, completed
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LoadPlanItem(Base):
    """Items in a load plan."""
    __tablename__ = "tms_load_plan_items"
    __table_args__ = (
        Index("idx_tmsloaditem_org_plan", "organization_id", "load_plan_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    load_plan_id: Mapped[int] = mapped_column(Integer, ForeignKey("tms_load_plans.id"), nullable=False)

    freight_order_id: Mapped[int] = mapped_column(Integer, ForeignKey("tms_freight_orders.id"), nullable=False)
    
    sequence: Mapped[int] = mapped_column(Integer, default=1)  # Loading/delivery order
    
    weight_kg: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"))
    volume_m3: Mapped[Decimal] = mapped_column(Numeric(10, 3), default=Decimal("0"))
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class RateQuote(Base):
    """Freight rate quote."""
    __tablename__ = "tms_rate_quotes"
    __table_args__ = (
        Index("idx_tmsquote_org_carrier", "organization_id", "carrier_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    quote_number: Mapped[str] = mapped_column(String(50), nullable=False)
    
    carrier_id: Mapped[int] = mapped_column(Integer, ForeignKey("tms_carriers.id"), nullable=False)
    
    origin: Mapped[str] = mapped_column(String(255), nullable=False)
    destination: Mapped[str] = mapped_column(String(255), nullable=False)
    
    service_type: Mapped[str] = mapped_column(String(50), default="standard")
    
    weight_kg: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    volume_m3: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 3))
    
    quoted_rate: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    fuel_surcharge: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"))
    additional_fees: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"))
    total_quote: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    
    quote_date: Mapped[date] = mapped_column(Date, nullable=False)
    valid_until: Mapped[date] = mapped_column(Date, nullable=False)
    
    status: Mapped[str] = mapped_column(String(20), default="active")  # active, accepted, expired
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class TransportEvent(Base):
    """Shipment tracking event."""
    __tablename__ = "tms_events"
    __table_args__ = (
        Index("idx_tmsevent_org_freight", "organization_id", "freight_order_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    freight_order_id: Mapped[int] = mapped_column(Integer, ForeignKey("tms_freight_orders.id"), nullable=False)

    event_type: Mapped[str] = mapped_column(String(50), nullable=False)  # pickup, in_transit, delivery, exception
    event_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    # GPS coordinates
    latitude: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 7))
    longitude: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 7))
    
    # Who recorded
    recorded_by: Mapped[Optional[str]] = mapped_column(String(255))
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
