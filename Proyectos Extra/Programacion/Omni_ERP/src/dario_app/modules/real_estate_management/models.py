"""Real Estate Management Models."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON, Boolean, Date
from sqlalchemy.orm import relationship

from dario_app.database import Base


class Property(Base):
    """Real estate property information."""
    
    __tablename__ = "property"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, nullable=False, index=True)
    property_code = Column(String(50), unique=True, index=True)
    property_name = Column(String(200), nullable=False)
    property_type = Column(String(50))  # office, warehouse, retail, industrial, mixed-use
    address = Column(String(500))
    city = Column(String(100))
    state_province = Column(String(100))
    postal_code = Column(String(20))
    country = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    total_area_sqft = Column(Float)
    usable_area_sqft = Column(Float)
    year_built = Column(Integer)
    acquisition_date = Column(Date)
    acquisition_cost = Column(Float)
    current_market_value = Column(Float)
    ownership_type = Column(String(50))  # owned, leased, mortgaged
    ownership_percentage = Column(Float)
    property_status = Column(String(50))  # active, inactive, for-sale, under-development
    environmental_certification = Column(String(100))  # LEED, BREEAM, etc.
    facility_grade = Column(String(20))  # A, B, C, D
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LeaseAgreement(Base):
    """Lease agreement management."""
    
    __tablename__ = "lease_agreement"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, nullable=False, index=True)
    property_id = Column(Integer, ForeignKey("property.id"))
    lease_number = Column(String(50), unique=True, index=True)
    tenant_name = Column(String(200), nullable=False)
    lease_type = Column(String(50))  # triple-net, full-service, modified-gross
    commencement_date = Column(Date, nullable=False)
    expiration_date = Column(Date, nullable=False)
    lease_term_years = Column(Integer)
    renewal_option = Column(Boolean, default=False)
    renewal_term_years = Column(Integer)
    base_rent_annual = Column(Float)
    rent_escalation_percentage = Column(Float)
    escalation_frequency = Column(String(50))  # annual, bi-annual, per-lease-term
    operating_expense_estimate = Column(Float)
    property_tax_estimate = Column(Float)
    insurance_estimate = Column(Float)
    security_deposit = Column(Float)
    tenant_improvement_allowance = Column(Float)
    guarantor_name = Column(String(200))
    lease_status = Column(String(50))  # active, expiring, expired, renewed
    lease_documents = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RentCollection(Base):
    """Rent payment and collection tracking."""
    
    __tablename__ = "rent_collection"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, nullable=False, index=True)
    lease_id = Column(Integer, ForeignKey("lease_agreement.id"))
    rental_period = Column(String(50))  # YYYY-MM
    due_date = Column(Date)
    base_rent_amount = Column(Float)
    operating_expense_amount = Column(Float)
    tax_amount = Column(Float)
    insurance_amount = Column(Float)
    additional_charges = Column(Float)
    total_due = Column(Float)
    amount_paid = Column(Float)
    payment_date = Column(Date)
    payment_method = Column(String(50))  # check, ACH, credit_card
    late_fee_applied = Column(Float, default=0)
    collection_status = Column(String(50))  # due, partial, collected, overdue
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MaintenanceRequest(Base):
    """Facility maintenance request and tracking."""
    
    __tablename__ = "maintenance_request"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, nullable=False, index=True)
    property_id = Column(Integer, ForeignKey("property.id"))
    request_number = Column(String(50), unique=True, index=True)
    maintenance_type = Column(String(50))  # preventive, corrective, emergency
    request_date = Column(DateTime, default=datetime.utcnow)
    requested_by = Column(String(200))
    description = Column(Text)
    priority = Column(String(20))  # low, medium, high, critical
    assigned_to = Column(String(200))
    estimated_cost = Column(Float)
    actual_cost = Column(Float)
    scheduled_date = Column(DateTime)
    completion_date = Column(DateTime)
    status = Column(String(50))  # open, in-progress, completed, closed
    work_order_number = Column(String(50))
    vendor_id = Column(Integer)
    completion_notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class SpaceAllocation(Base):
    """Space allocation and utilization planning."""
    
    __tablename__ = "space_allocation"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, nullable=False, index=True)
    property_id = Column(Integer, ForeignKey("property.id"))
    department = Column(String(200))
    floor_number = Column(Integer)
    space_code = Column(String(50))
    allocated_area_sqft = Column(Float)
    current_occupants = Column(Integer)
    persons_per_sqft = Column(Float)
    allocation_type = Column(String(50))  # office, workspace, meeting, storage, parking
    move_in_date = Column(Date)
    lease_expiration = Column(Date)
    allocation_status = Column(String(50))  # occupied, vacant, under-renovation
    reallocation_recommended = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class FacilityCondition(Base):
    """Building systems and facility condition assessment."""
    
    __tablename__ = "facility_condition"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, nullable=False, index=True)
    property_id = Column(Integer, ForeignKey("property.id"))
    assessment_date = Column(DateTime, default=datetime.utcnow)
    building_envelope = Column(String(20))  # A, B, C, D (condition rating)
    hvac_system = Column(String(20))
    electrical_system = Column(String(20))
    plumbing_system = Column(String(20))
    roof_condition = Column(String(20))
    structural_condition = Column(String(20))
    overall_condition_rating = Column(String(20))
    deferred_maintenance_estimate = Column(Float)
    critical_repairs_needed = Column(Text)
    capital_improvement_plan = Column(Text)
    next_assessment_date = Column(DateTime)
    assessor_name = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)


class PropertyPortfolioAnalysis(Base):
    """Real estate portfolio analytics and reporting."""
    
    __tablename__ = "property_portfolio_analysis"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, nullable=False, index=True)
    analysis_date = Column(DateTime, default=datetime.utcnow)
    total_properties = Column(Integer)
    total_portfolio_value = Column(Float)
    total_area_sqft = Column(Float)
    average_occupancy_rate = Column(Float)
    overall_facility_grade = Column(String(20))
    total_annual_rent = Column(Float)
    cost_per_sqft = Column(Float)
    deferred_maintenance_total = Column(Float)
    number_of_leases = Column(Integer)
    leases_expiring_within_year = Column(Integer)
    properties_for_divestment = Column(Integer)
    expansion_opportunities = Column(Integer)
    sustainability_score = Column(Float)
    portfolio_optimization_recommendations = Column(Text)
    created_by = Column(String(200))
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
