"""CRM models - Leads, Opportunities, Activities, Customer Scoring."""

from datetime import datetime
from decimal import Decimal
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, Index, JSON
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class Lead(Base):
    """Lead/Prospect model - potential customers."""
    
    __tablename__ = "crm_leads"
    __table_args__ = (
        Index("ix_lead_org_status", "organization_id", "status"),
        Index("ix_lead_org_score", "organization_id", "score"),
        {"extend_existing": True},
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)
    
    # Lead info
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    apellidos: Mapped[str | None] = mapped_column(String(200), nullable=True)
    empresa: Mapped[str | None] = mapped_column(String(200), nullable=True)
    cargo: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    # Contact
    email: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    telefono: Mapped[str | None] = mapped_column(String(50), nullable=True)
    telefono_secundario: Mapped[str | None] = mapped_column(String(50), nullable=True)
    website: Mapped[str | None] = mapped_column(String(500), nullable=True)
    
    # Source
    source: Mapped[str] = mapped_column(String(50), default="web", nullable=False)  # web, referral, campaign, cold_call
    source_details: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Qualification
    status: Mapped[str] = mapped_column(String(20), default="new", nullable=False, index=True)
    # new, contacted, qualified, unqualified, converted
    score: Mapped[int] = mapped_column(Integer, default=0, nullable=False, index=True)  # 0-100
    
    # Estimated value
    valor_estimado: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    moneda: Mapped[str] = mapped_column(String(3), default="EUR", nullable=False)
    
    # Assignment
    assigned_to_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=True, index=True)
    assigned_to_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    
    # Conversion
    converted_to_customer_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("clientes.id"), nullable=True)
    converted_to_opportunity_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    converted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    
    # Notes
    notas: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_contacted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class Opportunity(Base):
    """Sales opportunity model."""
    
    __tablename__ = "crm_opportunities"
    __table_args__ = (
        Index("ix_opp_org_stage", "organization_id", "stage"),
        Index("ix_opp_org_close_date", "organization_id", "expected_close_date"),
        {"extend_existing": True},
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)
    
    # Basic info
    nombre: Mapped[str] = mapped_column(String(300), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Customer
    cliente_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("clientes.id"), nullable=True, index=True)
    cliente_nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    
    # Value
    valor_estimado: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    moneda: Mapped[str] = mapped_column(String(3), default="EUR", nullable=False)
    probabilidad: Mapped[int] = mapped_column(Integer, default=50, nullable=False)  # 0-100%
    valor_ponderado: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)  # valor * probabilidad
    
    # Stage (pipeline)
    stage: Mapped[str] = mapped_column(String(50), default="prospecting", nullable=False, index=True)
    # prospecting, qualification, needs_analysis, proposal, negotiation, closed_won, closed_lost
    stage_changed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Assignment
    assigned_to_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=True, index=True)
    assigned_to_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    
    # Dates
    expected_close_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    actual_close_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    
    # Products/Services
    productos_interes: Mapped[list] = mapped_column(JSON, default=list)  # List of product IDs
    
    # Competition
    competidores: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Loss reason (if closed_lost)
    loss_reason: Mapped[str | None] = mapped_column(String(50), nullable=True)
    loss_details: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Activity(Base):
    """CRM activity model - calls, meetings, emails, tasks."""
    
    __tablename__ = "crm_activities"
    __table_args__ = (
        Index("ix_activity_org_date", "organization_id", "scheduled_at"),
        Index("ix_activity_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)
    
    # Type
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    # call, meeting, email, task, note
    
    # Subject
    asunto: Mapped[str] = mapped_column(String(300), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Related to
    related_to_type: Mapped[str | None] = mapped_column(String(50), nullable=True)  # lead, opportunity, customer
    related_to_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    related_to_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    
    # Assignment
    assigned_to_id: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    assigned_to_name: Mapped[str] = mapped_column(String(200), nullable=False)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="planned", nullable=False, index=True)
    # planned, in_progress, completed, cancelled
    
    # Priority
    prioridad: Mapped[str] = mapped_column(String(20), default="medium", nullable=False)
    # low, medium, high, urgent
    
    # Schedule
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, index=True)
    duracion_minutos: Mapped[int | None] = mapped_column(Integer, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    
    # Outcome
    resultado: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class CustomerScore(Base):
    """Customer scoring and segmentation."""
    
    __tablename__ = "crm_customer_scores"
    __table_args__ = (
        Index("ix_score_org_customer", "organization_id", "cliente_id"),
        Index("ix_score_org_segment", "organization_id", "segment"),
        {"extend_existing": True},
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)
    cliente_id: Mapped[int] = mapped_column(Integer, ForeignKey("clientes.id"), nullable=False, index=True)
    
    # RFM Scores
    recency_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # 1-5
    frequency_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # 1-5
    monetary_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # 1-5
    rfm_segment: Mapped[str] = mapped_column(String(50), nullable=True)  # Champions, Loyal, At Risk, etc
    
    # Overall score
    score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # 0-100
    segment: Mapped[str] = mapped_column(String(50), default="regular", nullable=False, index=True)
    # vip, high_value, regular, at_risk, lost
    
    # Metrics
    total_compras: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    numero_compras: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    promedio_compra: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    dias_ultima_compra: Mapped[int | None] = mapped_column(Integer, nullable=True)
    
    # Credit
    limite_credito: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    credito_usado: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    credito_disponible: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    
    # Payment behavior
    payment_score: Mapped[int] = mapped_column(Integer, default=50, nullable=False)  # 0-100
    promedio_dias_pago: Mapped[int | None] = mapped_column(Integer, nullable=True)
    facturas_vencidas: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Calculated
    calculated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
