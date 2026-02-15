"""Advanced Financial Reporting Models - Consolidation, IFRS, Reporting."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
import enum

from dario_app.database import Base


class ReportingStandard(str, enum.Enum):
    """Financial reporting standards."""
    GAAP = "gaap"
    IFRS = "ifrs"
    LOCAL = "local"
    HYBRID = "hybrid"


class ConsolidationMethod(str, enum.Enum):
    """Consolidation methods."""
    FULL = "full"
    PROPORTIONAL = "proportional"
    EQUITY = "equity"
    NONE = "none"


class FinancialReportTemplate(Base):
    """Financial report templates."""
    __tablename__ = "financial_report_templates"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)

    template_name = Column(String(255), nullable=False)
    report_type = Column(String(100))  # income_statement, balance_sheet, cash_flow, consolidated
    
    reporting_standard = Column(Enum(ReportingStandard), default=ReportingStandard.IFRS)
    
    structure = Column(JSON)  # Report line structure
    
    period_type = Column(String(50))  # monthly, quarterly, yearly
    is_automated = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    generated_reports = relationship("GeneratedReport", back_populates="template", cascade="all, delete-orphan")


class GeneratedReport(Base):
    """Generated financial reports."""
    __tablename__ = "generated_reports"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    template_id = Column(Integer, ForeignKey("financial_report_templates.id"))

    report_name = Column(String(255), nullable=False)
    report_period = Column(String(50))  # e.g., "2025-Q4"
    
    generation_date = Column(DateTime, default=datetime.utcnow)
    reporting_date = Column(DateTime)
    
    report_content = Column(JSON)  # Actual report data
    
    audited = Column(Boolean, default=False)
    signed_off = Column(Boolean, default=False)
    approved_by = Column(String(255))
    approval_date = Column(DateTime)
    
    distribution_list = Column(JSON)  # Recipients
    
    created_at = Column(DateTime, default=datetime.utcnow)

    template = relationship("FinancialReportTemplate", back_populates="generated_reports")


class ConsolidationGroup(Base):
    """Consolidation groups for multi-entity reporting."""
    __tablename__ = "consolidation_groups"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)

    group_name = Column(String(255), nullable=False)
    group_type = Column(String(100))  # parent_subsidiary, joint_venture, associated_company
    
    parent_entity_id = Column(Integer)
    
    consolidation_method = Column(Enum(ConsolidationMethod), default=ConsolidationMethod.FULL)
    ownership_percentage = Column(Float)  # Parent ownership %
    
    goodwill_amount = Column(Float)
    intercompany_elimination = Column(Boolean, default=True)
    
    status = Column(String(50), default="active")
    
    created_at = Column(DateTime, default=datetime.utcnow)

    entities = relationship("ConsolidatedEntity", back_populates="group", cascade="all, delete-orphan")


class ConsolidatedEntity(Base):
    """Individual entities in consolidation groups."""
    __tablename__ = "consolidated_entities"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    group_id = Column(Integer, ForeignKey("consolidation_groups.id"))

    entity_code = Column(String(100), unique=True, nullable=False)
    entity_name = Column(String(255), nullable=False)
    country = Column(String(100))
    
    ownership_percentage = Column(Float)
    acquisition_date = Column(DateTime)
    
    consolidation_method = Column(Enum(ConsolidationMethod))
    
    last_report_date = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    group = relationship("ConsolidationGroup", back_populates="entities")
    intercompany_transactions = relationship("IntercompanyTransaction", back_populates="entity", cascade="all, delete-orphan")


class IntercompanyTransaction(Base):
    """Inter-company transactions for elimination."""
    __tablename__ = "intercompany_transactions"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    entity_id = Column(Integer, ForeignKey("consolidated_entities.id"))

    transaction_type = Column(String(100))  # sale, service, loan, dividend, transfer
    
    source_entity_id = Column(Integer)
    target_entity_id = Column(Integer)
    
    transaction_date = Column(DateTime)
    
    transaction_amount = Column(Float)
    elimination_amount = Column(Float)
    remaining_amount = Column(Float)
    
    gl_account = Column(String(100))
    
    status = Column(String(50), default="pending")  # pending, reviewed, eliminated
    reviewed_by = Column(String(255))
    
    created_at = Column(DateTime, default=datetime.utcnow)

    entity = relationship("ConsolidatedEntity", back_populates="intercompany_transactions")


class ReportingVariance(Base):
    """Variance analysis for reporting."""
    __tablename__ = "reporting_variances"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)

    variance_period = Column(String(50))  # e.g., "2025-Q4"
    
    line_item = Column(String(255))  # GL account or report line
    
    budgeted_amount = Column(Float)
    actual_amount = Column(Float)
    variance_amount = Column(Float)
    variance_percentage = Column(Float)
    
    variance_category = Column(String(100))  # favorable, unfavorable
    
    explanation = Column(Text)
    responsible_manager = Column(String(255))
    
    created_at = Column(DateTime, default=datetime.utcnow)


class AuditTrail(Base):
    """Financial reporting audit trail."""
    __tablename__ = "audit_trails"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)

    report_id = Column(Integer)
    
    action = Column(String(100))  # created, modified, reviewed, approved, published
    
    performed_by = Column(String(255))
    performed_at = Column(DateTime, default=datetime.utcnow)
    
    change_description = Column(Text)
    previous_values = Column(JSON)
    new_values = Column(JSON)
    
    approval_status = Column(String(50))


class SegmentReporting(Base):
    """Segment reporting for business segments."""
    __tablename__ = "segment_reporting"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)

    reporting_period = Column(String(50))
    segment_code = Column(String(100), nullable=False)
    segment_name = Column(String(255), nullable=False)
    segment_type = Column(String(100))  # geographic, product_line, customer_type
    
    revenue = Column(Float)
    operating_profit = Column(Float)
    assets = Column(Float)
    capital_expenditure = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)
