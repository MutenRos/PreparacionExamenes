"""Sustainability Management models."""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class SustainabilityGoal(Base):
    """Sustainability/ESG goal."""
    __tablename__ = "sust_goals"
    __table_args__ = (
        Index("idx_sustgoal_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    goal_code: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    
    # ESG Category
    esg_category: Mapped[str] = mapped_column(String(30), default="environmental")  # environmental, social, governance
    
    # UN SDG alignment
    sdg_number: Mapped[Optional[int]] = mapped_column(Integer)  # 1-17
    
    # Target
    target_value: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    target_unit: Mapped[str] = mapped_column(String(50), nullable=False)
    baseline_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2))
    baseline_year: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Timeline
    target_year: Mapped[int] = mapped_column(Integer, nullable=False)
    start_year: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="active")
    
    # Ownership
    owner_name: Mapped[Optional[str]] = mapped_column(String(255))
    owner_id: Mapped[Optional[int]] = mapped_column(Integer)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class EmissionSource(Base):
    """Carbon emission source."""
    __tablename__ = "sust_emission_sources"
    __table_args__ = (
        Index("idx_sustemit_org_category", "organization_id", "scope"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    source_code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Scope (GHG Protocol)
    scope: Mapped[str] = mapped_column(String(10), nullable=False)  # Scope 1, 2, 3
    
    # Category
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    subcategory: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Emission factor
    emission_factor: Mapped[Decimal] = mapped_column(Numeric(15, 6), nullable=False)  # kg CO2e per unit
    emission_factor_unit: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Data quality
    data_quality_score: Mapped[Optional[int]] = mapped_column(Integer)  # 1-5
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class EmissionRecord(Base):
    """Carbon emission record."""
    __tablename__ = "sust_emission_records"
    __table_args__ = (
        Index("idx_sustemitrec_org_source", "organization_id", "source_id"),
        Index("idx_sustemitrec_org_period", "organization_id", "reporting_period"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    source_id: Mapped[int] = mapped_column(Integer, ForeignKey("sust_emission_sources.id"), nullable=False)

    reporting_period: Mapped[str] = mapped_column(String(10), nullable=False)  # YYYY-MM
    
    quantity: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    quantity_unit: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Calculated emissions
    emissions_kg_co2e: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    
    # Verification
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    verified_by: Mapped[Optional[str]] = mapped_column(String(255))
    verification_date: Mapped[Optional[date]] = mapped_column(Date)
    
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class WasteRecord(Base):
    """Waste/recycling record."""
    __tablename__ = "sust_waste_records"
    __table_args__ = (
        Index("idx_sustwaste_org_type", "organization_id", "waste_type"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    reporting_period: Mapped[str] = mapped_column(String(10), nullable=False)
    
    waste_type: Mapped[str] = mapped_column(String(50), nullable=False)  # hazardous, non-hazardous, plastic, paper, etc
    
    quantity_kg: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    
    disposal_method: Mapped[str] = mapped_column(String(50), nullable=False)  # landfill, recycled, incinerated, composted
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class SustainabilityReport(Base):
    """ESG/Sustainability report."""
    __tablename__ = "sust_reports"
    __table_args__ = (
        Index("idx_sustexh_org_year", "organization_id", "reporting_year"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    report_number: Mapped[str] = mapped_column(String(50), nullable=False)
    reporting_year: Mapped[int] = mapped_column(Integer, nullable=False)
    
    report_type: Mapped[str] = mapped_column(String(50), default="annual")  # annual, interim, special
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Scope
    reporting_scope: Mapped[Optional[str]] = mapped_column(Text)  # JSON array of entities
    
    # GHG emissions summary (kg CO2e)
    total_emissions_scope_1: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2))
    total_emissions_scope_2: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2))
    total_emissions_scope_3: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2))
    total_emissions: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2))
    
    # Other metrics
    energy_consumed_kwh: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2))
    water_consumed_m3: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2))
    waste_generated_kg: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2))
    waste_recycled_kg: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2))
    
    # Content
    executive_summary: Mapped[Optional[str]] = mapped_column(Text)
    data_summary: Mapped[Optional[str]] = mapped_column(Text)  # JSON
    
    # Publishing
    status: Mapped[str] = mapped_column(String(20), default="draft")  # draft, review, published
    published_date: Mapped[Optional[date]] = mapped_column(Date)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ComplianceRequirement(Base):
    """Sustainability compliance requirement."""
    __tablename__ = "sust_compliance"
    __table_args__ = (
        Index("idx_sustcomp_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    requirement_code: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Regulation
    regulation_name: Mapped[str] = mapped_column(String(255), nullable=False)
    jurisdiction: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="compliant")  # compliant, non_compliant, at_risk
    
    # Assessment
    last_assessed_date: Mapped[Optional[date]] = mapped_column(Date)
    next_assessment_date: Mapped[Optional[date]] = mapped_column(Date)
    
    compliance_notes: Mapped[Optional[str]] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
