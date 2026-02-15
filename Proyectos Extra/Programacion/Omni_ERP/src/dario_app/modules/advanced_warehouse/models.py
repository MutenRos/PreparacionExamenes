"""Advanced Warehouse Management System models."""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class WarehouseZone(Base):
    """Warehouse zone/area definition."""
    __tablename__ = "wms_zones"
    __table_args__ = (
        Index("idx_wmszone_org_warehouse", "organization_id", "warehouse_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    warehouse_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to almacenes

    zone_code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    zone_type: Mapped[str] = mapped_column(String(30), default="storage")  # storage, picking, packing, staging, shipping
    
    temperature_controlled: Mapped[bool] = mapped_column(Boolean, default=False)
    hazmat_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    
    status: Mapped[str] = mapped_column(String(20), default="active")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class WarehouseBin(Base):
    """Specific storage bin/location."""
    __tablename__ = "wms_bins"
    __table_args__ = (
        Index("idx_wmsbin_org_zone", "organization_id", "zone_id"),
        Index("idx_wmsbin_org_barcode", "organization_id", "barcode"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    zone_id: Mapped[int] = mapped_column(Integer, ForeignKey("wms_zones.id"), nullable=False)

    bin_code: Mapped[str] = mapped_column(String(50), nullable=False)
    barcode: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Location (aisle-rack-shelf-bin)
    aisle: Mapped[Optional[str]] = mapped_column(String(10))
    rack: Mapped[Optional[str]] = mapped_column(String(10))
    shelf: Mapped[Optional[str]] = mapped_column(String(10))
    bin: Mapped[Optional[str]] = mapped_column(String(10))
    
    # Capacity
    max_weight_kg: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"))
    max_volume_m3: Mapped[Decimal] = mapped_column(Numeric(10, 3), default=Decimal("0"))
    
    current_weight_kg: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"))
    current_volume_m3: Mapped[Decimal] = mapped_column(Numeric(10, 3), default=Decimal("0"))
    
    # Status
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Wave(Base):
    """Wave picking wave."""
    __tablename__ = "wms_waves"
    __table_args__ = (
        Index("idx_wmswave_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    wave_number: Mapped[str] = mapped_column(String(50), nullable=False)
    
    wave_type: Mapped[str] = mapped_column(String(30), default="batch")  # batch, discrete, cluster, zone
    
    warehouse_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to almacenes
    zone_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("wms_zones.id"))
    
    # Planning
    planned_date: Mapped[date] = mapped_column(Date, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, default=5)  # 1-10
    
    # Assignment
    assigned_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    assigned_user_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Metrics
    total_lines: Mapped[int] = mapped_column(Integer, default=0)
    picked_lines: Mapped[int] = mapped_column(Integer, default=0)
    total_quantity: Mapped[int] = mapped_column(Integer, default=0)
    picked_quantity: Mapped[int] = mapped_column(Integer, default=0)
    
    # Status
    status: Mapped[str] = mapped_column(String(30), default="planned")  # planned, released, in_progress, completed, cancelled
    
    released_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PickTask(Base):
    """Individual picking task."""
    __tablename__ = "wms_pick_tasks"
    __table_args__ = (
        Index("idx_wmspick_org_wave", "organization_id", "wave_id"),
        Index("idx_wmspick_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    wave_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("wms_waves.id"))

    task_number: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Source
    source_order_type: Mapped[str] = mapped_column(String(30), default="sales")  # sales, transfer, production
    source_order_id: Mapped[int] = mapped_column(Integer, nullable=False)
    source_line_id: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Item
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to productos
    product_code: Mapped[str] = mapped_column(String(100), nullable=False)
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Location
    from_bin_id: Mapped[int] = mapped_column(Integer, ForeignKey("wms_bins.id"), nullable=False)
    from_bin_code: Mapped[str] = mapped_column(String(50), nullable=False)
    
    to_location: Mapped[Optional[str]] = mapped_column(String(255))  # Staging/packing area
    
    # Quantity
    quantity_requested: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity_picked: Mapped[int] = mapped_column(Integer, default=0)
    
    # Assignment
    assigned_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    assigned_user_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    sequence: Mapped[int] = mapped_column(Integer, default=1)  # Pick path sequence
    
    # Status
    status: Mapped[str] = mapped_column(String(30), default="pending")  # pending, assigned, in_progress, completed, short_picked
    
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PackTask(Base):
    """Packing task."""
    __tablename__ = "wms_pack_tasks"
    __table_args__ = (
        Index("idx_wmspack_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    task_number: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Source order
    order_type: Mapped[str] = mapped_column(String(30), default="sales")
    order_id: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Packing station
    station_id: Mapped[Optional[int]] = mapped_column(Integer)
    station_name: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Assignment
    assigned_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    assigned_user_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Container
    container_type: Mapped[Optional[str]] = mapped_column(String(50))  # box, pallet, envelope
    container_count: Mapped[int] = mapped_column(Integer, default=1)
    
    tracking_number: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Weight/dimensions
    total_weight_kg: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"))
    
    # Status
    status: Mapped[str] = mapped_column(String(30), default="pending")  # pending, in_progress, completed
    
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CycleCount(Base):
    """Cycle counting task."""
    __tablename__ = "wms_cycle_counts"
    __table_args__ = (
        Index("idx_wmscount_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    count_number: Mapped[str] = mapped_column(String(50), nullable=False)
    
    count_type: Mapped[str] = mapped_column(String(30), default="spot")  # full, cycle, spot, blind
    
    warehouse_id: Mapped[int] = mapped_column(Integer, nullable=False)
    zone_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("wms_zones.id"))
    bin_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("wms_bins.id"))
    
    product_id: Mapped[Optional[int]] = mapped_column(Integer)  # Null for zone counts
    
    # Expected vs actual
    expected_quantity: Mapped[int] = mapped_column(Integer, default=0)
    counted_quantity: Mapped[Optional[int]] = mapped_column(Integer)
    variance: Mapped[int] = mapped_column(Integer, default=0)
    
    # Assignment
    assigned_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    assigned_user_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    counted_by_id: Mapped[Optional[int]] = mapped_column(Integer)
    counted_by_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    scheduled_date: Mapped[date] = mapped_column(Date, nullable=False)
    counted_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    # Status
    status: Mapped[str] = mapped_column(String(30), default="scheduled")  # scheduled, in_progress, completed, variance_review
    
    # Variance handling
    variance_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    variance_notes: Mapped[Optional[str]] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Replenishment(Base):
    """Inventory replenishment task."""
    __tablename__ = "wms_replenishments"
    __table_args__ = (
        Index("idx_wmsrepl_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    replenishment_number: Mapped[str] = mapped_column(String(50), nullable=False)
    
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)
    product_code: Mapped[str] = mapped_column(String(100), nullable=False)
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # From (reserve/bulk) to (forward/pick)
    from_bin_id: Mapped[int] = mapped_column(Integer, ForeignKey("wms_bins.id"), nullable=False)
    from_bin_code: Mapped[str] = mapped_column(String(50), nullable=False)
    
    to_bin_id: Mapped[int] = mapped_column(Integer, ForeignKey("wms_bins.id"), nullable=False)
    to_bin_code: Mapped[str] = mapped_column(String(50), nullable=False)
    
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Priority
    priority: Mapped[int] = mapped_column(Integer, default=5)  # 1-10
    replenishment_type: Mapped[str] = mapped_column(String(30), default="min_max")  # min_max, demand_based, wave_based
    
    # Assignment
    assigned_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    assigned_user_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Status
    status: Mapped[str] = mapped_column(String(30), default="pending")  # pending, in_progress, completed
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)


class PutawayTask(Base):
    """Putaway task for received inventory."""
    __tablename__ = "wms_putaway_tasks"
    __table_args__ = (
        Index("idx_wmsputaway_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    task_number: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Source
    receipt_id: Mapped[Optional[int]] = mapped_column(Integer)  # FK to recepcion_logistica
    
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)
    product_code: Mapped[str] = mapped_column(String(100), nullable=False)
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Location
    from_location: Mapped[str] = mapped_column(String(255), nullable=False)  # Receiving dock
    to_bin_id: Mapped[int] = mapped_column(Integer, ForeignKey("wms_bins.id"), nullable=False)
    to_bin_code: Mapped[str] = mapped_column(String(50), nullable=False)
    
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Assignment
    assigned_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    assigned_user_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Status
    status: Mapped[str] = mapped_column(String(30), default="pending")  # pending, in_progress, completed
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
