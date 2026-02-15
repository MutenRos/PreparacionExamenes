"""Supply Chain Management models - MRP, Reorder Policies, Landed Cost."""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, Index, JSON
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class ReorderPolicy(Base):
    """Reorder policy configuration for products."""
    
    __tablename__ = "reorder_policies"
    __table_args__ = (
        Index("idx_reorder_org_producto", "organization_id", "producto_id"),
        {"extend_existing": True}
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    producto_id: Mapped[int] = mapped_column(Integer, nullable=False)
    producto_codigo: Mapped[Optional[str]] = mapped_column(String(100))
    producto_nombre: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Policy type: min_max, reorder_point, fixed_quantity, economic_order_quantity
    policy_type: Mapped[str] = mapped_column(String(50), default="reorder_point")
    
    # Min/Max policy
    min_quantity: Mapped[Decimal] = mapped_column(Numeric(15, 3), default=Decimal("0"))
    max_quantity: Mapped[Decimal] = mapped_column(Numeric(15, 3), default=Decimal("0"))
    
    # Reorder point policy
    reorder_point: Mapped[Decimal] = mapped_column(Numeric(15, 3), default=Decimal("0"))
    reorder_quantity: Mapped[Decimal] = mapped_column(Numeric(15, 3), default=Decimal("0"))
    
    # Safety stock
    safety_stock: Mapped[Decimal] = mapped_column(Numeric(15, 3), default=Decimal("0"))
    
    # Lead time (days)
    lead_time_days: Mapped[int] = mapped_column(Integer, default=0)
    
    # EOQ parameters
    annual_demand: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 3))
    holding_cost_percent: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))  # % per year
    ordering_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))  # cost per order
    
    # Auto-reorder flag
    auto_reorder_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Preferred supplier
    preferred_supplier_id: Mapped[Optional[int]] = mapped_column(Integer)
    preferred_supplier_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Status
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MRPRun(Base):
    """MRP calculation run."""
    
    __tablename__ = "mrp_runs"
    __table_args__ = (
        Index("idx_mrp_org_status", "organization_id", "status"),
        Index("idx_mrp_run_date", "run_date"),
        {"extend_existing": True}
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    
    run_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    run_by_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    run_by_user_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Planning horizon (days)
    horizon_days: Mapped[int] = mapped_column(Integer, default=90)
    
    # Status: pending, running, completed, failed
    status: Mapped[str] = mapped_column(String(50), default="pending")
    
    # Results summary
    total_requirements: Mapped[int] = mapped_column(Integer, default=0)
    total_purchase_orders: Mapped[int] = mapped_column(Integer, default=0)
    total_production_orders: Mapped[int] = mapped_column(Integer, default=0)
    
    # Execution details
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    duration_seconds: Mapped[Optional[int]] = mapped_column(Integer)
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class MRPRequirement(Base):
    """MRP calculated requirement."""
    
    __tablename__ = "mrp_requirements"
    __table_args__ = (
        Index("idx_mrp_req_run", "mrp_run_id"),
        Index("idx_mrp_req_producto", "organization_id", "producto_id", "required_date"),
        {"extend_existing": True}
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    mrp_run_id: Mapped[int] = mapped_column(Integer, ForeignKey("mrp_runs.id"), nullable=False)
    
    producto_id: Mapped[int] = mapped_column(Integer, nullable=False)
    producto_codigo: Mapped[Optional[str]] = mapped_column(String(100))
    producto_nombre: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Requirement details
    required_quantity: Mapped[Decimal] = mapped_column(Numeric(15, 3), nullable=False)
    required_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    # Available inventory
    on_hand_quantity: Mapped[Decimal] = mapped_column(Numeric(15, 3), default=Decimal("0"))
    allocated_quantity: Mapped[Decimal] = mapped_column(Numeric(15, 3), default=Decimal("0"))
    available_quantity: Mapped[Decimal] = mapped_column(Numeric(15, 3), default=Decimal("0"))
    
    # Planned orders quantity
    planned_quantity: Mapped[Decimal] = mapped_column(Numeric(15, 3), default=Decimal("0"))
    
    # Source of requirement: sales_order, production_order, safety_stock, forecast
    source_type: Mapped[str] = mapped_column(String(50))
    source_id: Mapped[Optional[int]] = mapped_column(Integer)
    source_reference: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Action: purchase, produce, none
    suggested_action: Mapped[str] = mapped_column(String(50), default="none")
    
    # Order details
    order_quantity: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 3))
    order_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class LandedCostHeader(Base):
    """Landed cost calculation for purchase shipments."""
    
    __tablename__ = "landed_cost_headers"
    __table_args__ = (
        Index("idx_landed_org_compra", "organization_id", "compra_id"),
        Index("idx_landed_status", "organization_id", "status"),
        {"extend_existing": True}
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    
    # Purchase order reference
    compra_id: Mapped[int] = mapped_column(Integer, nullable=False)
    compra_numero: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Shipment details
    shipment_reference: Mapped[Optional[str]] = mapped_column(String(100))
    shipment_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    # Total values
    merchandise_value: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"))
    total_landed_costs: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"))
    total_value: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"))
    
    # Status: draft, calculated, applied
    status: Mapped[str] = mapped_column(String(50), default="draft")
    
    # Application details
    applied_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    applied_by_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    applied_by_user_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    notas: Mapped[Optional[str]] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LandedCostLine(Base):
    """Landed cost line items (freight, insurance, customs, etc.)."""
    
    __tablename__ = "landed_cost_lines"
    __table_args__ = (
        Index("idx_landed_line_header", "landed_cost_header_id"),
        {"extend_existing": True}
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    landed_cost_header_id: Mapped[int] = mapped_column(Integer, ForeignKey("landed_cost_headers.id"), nullable=False)
    
    # Cost type: freight, insurance, customs_duty, handling, other
    cost_type: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Cost amount
    cost_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    
    # Allocation method: by_value, by_quantity, by_weight, by_volume, manual
    allocation_method: Mapped[str] = mapped_column(String(50), default="by_value")
    
    # Supplier
    proveedor_id: Mapped[Optional[int]] = mapped_column(Integer)
    proveedor_nombre: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Invoice reference
    invoice_number: Mapped[Optional[str]] = mapped_column(String(100))
    invoice_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class LandedCostAllocation(Base):
    """Allocated landed costs to specific products."""
    
    __tablename__ = "landed_cost_allocations"
    __table_args__ = (
        Index("idx_landed_alloc_header", "landed_cost_header_id"),
        Index("idx_landed_alloc_producto", "organization_id", "producto_id"),
        {"extend_existing": True}
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    landed_cost_header_id: Mapped[int] = mapped_column(Integer, ForeignKey("landed_cost_headers.id"), nullable=False)
    landed_cost_line_id: Mapped[int] = mapped_column(Integer, ForeignKey("landed_cost_lines.id"), nullable=False)
    
    # Product
    producto_id: Mapped[int] = mapped_column(Integer, nullable=False)
    producto_codigo: Mapped[Optional[str]] = mapped_column(String(100))
    producto_nombre: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Purchase details
    compra_detalle_id: Mapped[Optional[int]] = mapped_column(Integer)
    quantity: Mapped[Decimal] = mapped_column(Numeric(15, 3), nullable=False)
    unit_cost: Mapped[Decimal] = mapped_column(Numeric(15, 4), nullable=False)
    total_value: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    
    # Allocated cost
    allocated_cost: Mapped[Decimal] = mapped_column(Numeric(15, 4), nullable=False)
    allocated_cost_per_unit: Mapped[Decimal] = mapped_column(Numeric(15, 4), nullable=False)
    
    # New unit cost with landed cost
    new_unit_cost: Mapped[Decimal] = mapped_column(Numeric(15, 4), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class InventoryLocation(Base):
    """Warehouse locations for multi-location inventory management."""
    
    __tablename__ = "inventory_locations"
    __table_args__ = (
        Index("idx_location_org_code", "organization_id", "location_code"),
        {"extend_existing": True}
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    
    location_code: Mapped[str] = mapped_column(String(50), nullable=False)
    location_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Location type: warehouse, store, production, transit, quarantine
    location_type: Mapped[str] = mapped_column(String(50), default="warehouse")
    
    # Address
    address: Mapped[Optional[str]] = mapped_column(String(255))
    city: Mapped[Optional[str]] = mapped_column(String(100))
    state: Mapped[Optional[str]] = mapped_column(String(100))
    country: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Manager
    manager_id: Mapped[Optional[int]] = mapped_column(Integer)
    manager_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Capacity
    capacity_m3: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    capacity_kg: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class InventoryByLocation(Base):
    """Inventory quantities by location."""
    
    __tablename__ = "inventory_by_location"
    __table_args__ = (
        Index("idx_inv_location_producto", "organization_id", "location_id", "producto_id", unique=True),
        {"extend_existing": True}
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey("inventory_locations.id"), nullable=False)
    location_code: Mapped[Optional[str]] = mapped_column(String(50))
    
    producto_id: Mapped[int] = mapped_column(Integer, nullable=False)
    producto_codigo: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Quantities
    on_hand: Mapped[Decimal] = mapped_column(Numeric(15, 3), default=Decimal("0"))
    allocated: Mapped[Decimal] = mapped_column(Numeric(15, 3), default=Decimal("0"))
    available: Mapped[Decimal] = mapped_column(Numeric(15, 3), default=Decimal("0"))
    
    # Physical attributes
    weight_kg: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 3))
    volume_m3: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 3))
    
    last_counted_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    last_movement_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
