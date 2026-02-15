"""Manufacturing Execution System Models - Shop Floor, Production, Quality Control."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
import enum

from dario_app.database import Base


class ProductionOrderStatus(str, enum.Enum):
    """Production order statuses."""
    PLANNED = "planned"
    RELEASED = "released"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class EquipmentStatus(str, enum.Enum):
    """Equipment operational status."""
    OPERATIONAL = "operational"
    MAINTENANCE = "maintenance"
    BREAKDOWN = "breakdown"
    IDLE = "idle"


class ShopFloorWorkOrder(Base):
    """Work orders on shop floor."""
    __tablename__ = "shop_floor_work_orders"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    production_order_id = Column(Integer, nullable=False, index=True)

    work_order_number = Column(String(100), unique=True, nullable=False, index=True)
    status = Column(Enum(ProductionOrderStatus), default=ProductionOrderStatus.PLANNED, index=True)
    
    operation_sequence = Column(Integer)
    work_center_id = Column(Integer)
    
    scheduled_start = Column(DateTime)
    scheduled_end = Column(DateTime)
    actual_start = Column(DateTime)
    actual_end = Column(DateTime)
    
    standard_hours = Column(Float)
    actual_hours = Column(Float)
    labor_hours = Column(Float)
    
    material_picked = Column(Boolean, default=False)
    setup_complete = Column(Boolean, default=False)
    
    quantity_planned = Column(Float)
    quantity_produced = Column(Float)
    quantity_scrapped = Column(Float)
    quantity_rework = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    production_details = relationship("ProductionEventLog", back_populates="work_order", cascade="all, delete-orphan")


class ProductionEventLog(Base):
    """Real-time production events from shop floor."""
    __tablename__ = "production_event_logs"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    work_order_id = Column(Integer, ForeignKey("shop_floor_work_orders.id"), nullable=False)

    event_type = Column(String(100))  # start, pause, resume, stop, quality_issue, equipment_failure
    event_description = Column(Text)
    
    production_count = Column(Integer)
    scrap_count = Column(Integer)
    rework_count = Column(Integer)
    
    operator_id = Column(Integer)
    equipment_id = Column(Integer)
    
    recorded_at = Column(DateTime, default=datetime.utcnow)
    data_source = Column(String(100))  # manual, IoT, barcode, RFID

    work_order = relationship("ShopFloorWorkOrder", back_populates="production_details")


class WorkCenter(Base):
    """Manufacturing work centers/machines."""
    __tablename__ = "work_centers"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)

    work_center_code = Column(String(100), unique=True, nullable=False, index=True)
    work_center_name = Column(String(255), nullable=False)
    description = Column(Text)
    
    capacity_per_hour = Column(Float)
    available_hours_per_day = Column(Float)
    
    equipment_ids = Column(JSON)  # List of equipment at this center
    qualified_operators = Column(JSON)  # List of operator IDs
    
    status = Column(String(50), default="operational")
    utilization_percentage = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Equipment(Base):
    """Manufacturing equipment/machines."""
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)

    equipment_code = Column(String(100), unique=True, nullable=False, index=True)
    equipment_name = Column(String(255), nullable=False)
    equipment_type = Column(String(100))  # CNC, Assembly, Press, etc.
    
    manufacturer = Column(String(255))
    model_number = Column(String(100))
    serial_number = Column(String(100))
    
    status = Column(Enum(EquipmentStatus), default=EquipmentStatus.OPERATIONAL, index=True)
    
    setup_time_minutes = Column(Integer)
    cycle_time_minutes = Column(Float)
    
    purchase_date = Column(DateTime)
    last_maintenance = Column(DateTime)
    next_maintenance = Column(DateTime)
    
    total_runtime_hours = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    maintenance_records = relationship("MaintenanceRecord", back_populates="equipment", cascade="all, delete-orphan")


class MaintenanceRecord(Base):
    """Equipment maintenance tracking."""
    __tablename__ = "maintenance_records"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)

    maintenance_type = Column(String(100))  # preventive, corrective, inspection
    status = Column(String(50), default="pending")  # pending, in_progress, completed
    
    scheduled_date = Column(DateTime)
    actual_start = Column(DateTime)
    actual_completion = Column(DateTime)
    
    description = Column(Text)
    performed_by = Column(String(255))
    
    duration_hours = Column(Float)
    cost = Column(Float)
    
    parts_replaced = Column(JSON)
    downtime_minutes = Column(Integer)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    equipment = relationship("Equipment", back_populates="maintenance_records")


class QualityInspection(Base):
    """In-process quality control."""
    __tablename__ = "quality_inspections"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    work_order_id = Column(Integer, ForeignKey("shop_floor_work_orders.id"))

    inspection_type = Column(String(100))  # in_process, final, sample
    inspection_date = Column(DateTime, default=datetime.utcnow)
    
    sample_size = Column(Integer)
    accepted_count = Column(Integer)
    rejected_count = Column(Integer)
    rework_count = Column(Integer)
    
    acceptance_rate = Column(Float)
    
    inspection_criteria = Column(JSON)  # Dimensions, appearance, etc.
    findings = Column(Text)
    
    inspector_id = Column(Integer)
    status = Column(String(50))  # pass, fail, conditional
    
    corrective_actions = Column(JSON)


class ProductionSchedule(Base):
    """Master production schedule."""
    __tablename__ = "production_schedules"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)

    schedule_name = Column(String(255), nullable=False)
    schedule_type = Column(String(100))  # daily, weekly, monthly, custom
    
    period_start = Column(DateTime)
    period_end = Column(DateTime)
    
    total_planned_hours = Column(Float)
    total_available_hours = Column(Float)
    
    work_orders_count = Column(Integer, default=0)
    completion_percentage = Column(Float, default=0.0)
    
    status = Column(String(50), default="draft")  # draft, published, active, completed
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LaborTracking(Base):
    """Labor time tracking on production."""
    __tablename__ = "labor_tracking"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    work_order_id = Column(Integer, ForeignKey("shop_floor_work_orders.id"))

    operator_id = Column(Integer, nullable=False, index=True)
    operation_id = Column(Integer)
    
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    
    setup_time = Column(Float)  # Hours
    production_time = Column(Float)  # Hours
    idle_time = Column(Float)  # Hours
    
    reason_for_idle = Column(String(255))
    
    efficiency_percentage = Column(Float)
    pieces_produced = Column(Integer)
    
    created_at = Column(DateTime, default=datetime.utcnow)


class ScrapTracking(Base):
    """Scrap and rework tracking."""
    __tablename__ = "scrap_tracking"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    work_order_id = Column(Integer, ForeignKey("shop_floor_work_orders.id"))

    scrap_quantity = Column(Float)
    scrap_reason = Column(String(255))
    scrap_category = Column(String(100))  # material, labor, equipment, design
    
    scrap_cost = Column(Float)
    
    rework_possible = Column(Boolean, default=False)
    rework_quantity = Column(Float)
    rework_cost = Column(Float)
    
    recorded_by = Column(String(255))
    recorded_at = Column(DateTime, default=datetime.utcnow)


class MaterialConsumption(Base):
    """Actual material consumption tracking."""
    __tablename__ = "material_consumption"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    work_order_id = Column(Integer, ForeignKey("shop_floor_work_orders.id"))

    material_id = Column(Integer, nullable=False, index=True)
    
    planned_quantity = Column(Float)
    actual_quantity = Column(Float)
    variance = Column(Float)
    variance_percentage = Column(Float)
    
    unit_of_measure = Column(String(50))
    
    consumption_date = Column(DateTime, default=datetime.utcnow)
    consumed_by = Column(String(255))
