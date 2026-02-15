"""
Compliance Management Module - Models
Regulatory compliance, certifications, audits, and violation management
"""
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from dario_app.database import Base


class ComplianceFramework(Base):
    """Compliance framework definition (ISO, GDPR, SOX, etc.)"""
    __tablename__ = "compliance_frameworks"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    
    # Basic Info
    framework_code = Column(String(50), unique=True, nullable=False, index=True)  # FRM-001
    name = Column(String(200), nullable=False)  # ISO 9001, GDPR, SOX, HIPAA
    description = Column(Text)
    short_name = Column(String(50))  # ISO9001, GDPR
    
    # Framework Details
    framework_type = Column(String(50))  # Quality, Security, Privacy, Financial, Industry_Specific
    regulatory_body = Column(String(200))  # ISO, EU, SEC, FDA
    geographic_scope = Column(String(100))  # Global, EU, US, Country_Specific
    industry = Column(String(100))  # Healthcare, Finance, Manufacturing, All
    
    # Versioning
    version = Column(String(50))  # 2015, 2016, etc.
    effective_date = Column(Date)
    expiration_date = Column(Date)
    is_current_version = Column(Boolean, default=True)
    
    # Requirements
    total_requirements = Column(Integer, default=0)
    total_controls = Column(Integer, default=0)
    requirements_structure = Column(JSON)  # Hierarchical structure
    
    # Applicability
    is_mandatory = Column(Boolean, default=False)
    applies_to_departments = Column(JSON)  # List of department IDs
    applies_to_processes = Column(JSON)  # List of process IDs
    
    # Certification
    requires_certification = Column(Boolean, default=False)
    certification_body = Column(String(200))
    certification_validity_years = Column(Integer)
    recertification_required = Column(Boolean, default=False)
    
    # Documentation
    documentation_url = Column(Text)
    reference_documents = Column(JSON)  # List of document references
    training_materials = Column(JSON)
    
    # Status
    status = Column(String(50), default="Active")  # Active, Deprecated, Under_Review
    implementation_status = Column(String(50))  # Not_Started, In_Progress, Implemented, Verified
    compliance_percentage = Column(Float, default=0)  # Overall compliance %
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    
    # Relationships
    regulations = relationship("Regulation", back_populates="framework", cascade="all, delete-orphan")
    audits = relationship("ComplianceAudit", back_populates="framework")


class Regulation(Base):
    """Specific regulation or requirement within a framework"""
    __tablename__ = "compliance_regulations"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    framework_id = Column(Integer, ForeignKey("compliance_frameworks.id"), nullable=False)
    
    # Basic Info
    regulation_code = Column(String(50), unique=True, nullable=False, index=True)  # REG-001
    reference_number = Column(String(100))  # 7.1.1, Article 6, etc.
    title = Column(String(300), nullable=False)
    description = Column(Text)
    
    # Classification
    category = Column(String(100))  # Documentation, Process, Technical, Organizational
    subcategory = Column(String(100))
    requirement_type = Column(String(50))  # Mandatory, Recommended, Optional
    
    # Hierarchy
    parent_regulation_id = Column(Integer)  # For nested regulations
    level = Column(Integer, default=1)  # Hierarchy level
    sequence_order = Column(Integer)  # Order within parent
    
    # Requirements
    requirement_text = Column(Text, nullable=False)  # Full requirement description
    acceptance_criteria = Column(Text)  # How to verify compliance
    evidence_required = Column(JSON)  # Types of evidence needed
    
    # Compliance
    compliance_status = Column(String(50), default="Not_Assessed")  # Not_Assessed, Compliant, Non_Compliant, Partial, Not_Applicable
    compliance_percentage = Column(Float, default=0)
    last_assessed_date = Column(Date)
    next_assessment_date = Column(Date)
    
    # Risk
    risk_level = Column(String(50))  # Critical, High, Medium, Low
    risk_if_non_compliant = Column(Text)  # Consequences of non-compliance
    penalty_description = Column(Text)  # Legal/financial penalties
    
    # Implementation
    implementation_status = Column(String(50), default="Not_Started")
    implementation_owner = Column(String(100))  # Responsible person/department
    implementation_deadline = Column(Date)
    implementation_cost = Column(Float)
    implementation_effort_hours = Column(Float)
    
    # Controls
    control_measures = Column(JSON)  # Implemented controls
    control_effectiveness = Column(Float)  # 0-100%
    
    # Documentation
    policy_document_ids = Column(JSON)  # Related policy documents
    procedure_document_ids = Column(JSON)  # Related procedures
    evidence_document_ids = Column(JSON)  # Evidence of compliance
    
    # Monitoring
    monitoring_frequency = Column(String(50))  # Continuous, Daily, Weekly, Monthly, Quarterly, Annually
    last_monitored_date = Column(Date)
    next_monitoring_date = Column(Date)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_applicable = Column(Boolean, default=True)
    non_applicability_reason = Column(Text)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    
    # Relationships
    framework = relationship("ComplianceFramework", back_populates="regulations")
    violations = relationship("ViolationReport", back_populates="regulation")


class CertificationProcess(Base):
    """Certification/accreditation process tracking"""
    __tablename__ = "compliance_certification_processes"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    framework_id = Column(Integer, ForeignKey("compliance_frameworks.id"))
    
    # Basic Info
    certification_code = Column(String(50), unique=True, nullable=False, index=True)  # CERT-001
    certification_name = Column(String(200), nullable=False)
    description = Column(Text)
    certification_type = Column(String(50))  # Initial, Renewal, Surveillance, Recertification
    
    # Certification Body
    certifying_body = Column(String(200))  # Name of certification organization
    auditor_name = Column(String(200))
    auditor_contact = Column(String(200))
    accreditation_number = Column(String(100))
    
    # Timeline
    application_date = Column(Date)
    planned_start_date = Column(Date)
    planned_end_date = Column(Date)
    actual_start_date = Column(Date)
    actual_end_date = Column(Date)
    certificate_issue_date = Column(Date)
    certificate_expiry_date = Column(Date)
    
    # Process Stages
    current_stage = Column(String(50))  # Application, Documentation_Review, On_Site_Audit, Corrective_Actions, Certification_Decision, Issued
    stages_completed = Column(JSON)  # List of completed stages
    stage_progress_percentage = Column(Float, default=0)
    
    # Readiness
    readiness_score = Column(Float)  # 0-100%
    readiness_assessment_date = Column(Date)
    gaps_identified = Column(Integer, default=0)
    gaps_closed = Column(Integer, default=0)
    
    # Audit Details
    audit_start_date = Column(Date)
    audit_end_date = Column(Date)
    audit_duration_days = Column(Integer)
    audit_type = Column(String(50))  # Document_Review, On_Site, Remote, Hybrid
    audit_scope = Column(Text)
    areas_audited = Column(JSON)  # List of areas/departments
    
    # Findings
    major_non_conformities = Column(Integer, default=0)
    minor_non_conformities = Column(Integer, default=0)
    observations = Column(Integer, default=0)
    opportunities_for_improvement = Column(Integer, default=0)
    findings_details = Column(JSON)
    
    # Corrective Actions
    corrective_actions_required = Column(Integer, default=0)
    corrective_actions_completed = Column(Integer, default=0)
    corrective_action_deadline = Column(Date)
    
    # Decision
    certification_decision = Column(String(50))  # Pending, Approved, Approved_with_Conditions, Denied, Suspended
    decision_date = Column(Date)
    decision_rationale = Column(Text)
    conditions = Column(JSON)  # Conditions if approved conditionally
    
    # Certificate Details
    certificate_number = Column(String(100))
    certificate_scope = Column(Text)
    certificate_status = Column(String(50))  # Valid, Expired, Suspended, Revoked
    certificate_file_path = Column(String(500))
    
    # Surveillance & Maintenance
    surveillance_audits_required = Column(Integer)  # Number required during validity
    surveillance_audits_completed = Column(Integer, default=0)
    next_surveillance_date = Column(Date)
    
    # Costs
    application_fee = Column(Float)
    certification_fee = Column(Float)
    annual_maintenance_fee = Column(Float)
    total_cost = Column(Float)
    
    # Status
    status = Column(String(50), default="Planning")  # Planning, In_Progress, Completed, On_Hold, Cancelled
    is_active = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))


class ComplianceAudit(Base):
    """Internal or external compliance audit"""
    __tablename__ = "compliance_audits"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    framework_id = Column(Integer, ForeignKey("compliance_frameworks.id"))
    
    # Basic Info
    audit_code = Column(String(50), unique=True, nullable=False, index=True)  # AUD-001
    audit_name = Column(String(200), nullable=False)
    description = Column(Text)
    audit_type = Column(String(50))  # Internal, External, Regulatory, Surveillance, Follow_Up
    
    # Audit Scope
    scope_description = Column(Text)
    departments_included = Column(JSON)
    processes_included = Column(JSON)
    locations_included = Column(JSON)
    regulations_audited = Column(JSON)  # List of regulation IDs
    
    # Scheduling
    fiscal_year = Column(Integer)
    audit_quarter = Column(String(20))  # Q1, Q2, Q3, Q4
    planned_start_date = Column(Date)
    planned_end_date = Column(Date)
    actual_start_date = Column(Date)
    actual_end_date = Column(Date)
    
    # Audit Team
    lead_auditor = Column(String(200))
    audit_team_members = Column(JSON)  # List of auditor names/IDs
    external_auditor_firm = Column(String(200))
    
    # Execution
    audit_approach = Column(String(50))  # Risk_Based, Process_Based, Comprehensive
    audit_checklist_id = Column(Integer)
    total_checkpoints = Column(Integer, default=0)
    checkpoints_completed = Column(Integer, default=0)
    progress_percentage = Column(Float, default=0)
    
    # Sampling
    sampling_method = Column(String(50))  # Random, Risk_Based, Stratified, Census
    population_size = Column(Integer)
    sample_size = Column(Integer)
    samples_reviewed = Column(Integer, default=0)
    
    # Findings
    findings_count = Column(Integer, default=0)
    critical_findings = Column(Integer, default=0)
    high_findings = Column(Integer, default=0)
    medium_findings = Column(Integer, default=0)
    low_findings = Column(Integer, default=0)
    positive_findings = Column(Integer, default=0)  # Good practices identified
    
    # Compliance Score
    overall_compliance_score = Column(Float)  # 0-100%
    previous_audit_score = Column(Float)
    score_change = Column(Float)  # Improvement or decline
    
    # Risk Assessment
    overall_risk_rating = Column(String(50))  # Critical, High, Medium, Low, Minimal
    residual_risk_level = Column(Float)
    risk_mitigation_required = Column(Boolean, default=False)
    
    # Reporting
    draft_report_date = Column(Date)
    final_report_date = Column(Date)
    report_file_path = Column(String(500))
    executive_summary = Column(Text)
    key_findings = Column(JSON)
    recommendations = Column(JSON)
    
    # Follow-Up
    follow_up_required = Column(Boolean, default=False)
    follow_up_deadline = Column(Date)
    follow_up_completed = Column(Boolean, default=False)
    follow_up_date = Column(Date)
    
    # Status
    status = Column(String(50), default="Planned")  # Planned, In_Progress, Report_Draft, Under_Review, Finalized, Closed
    is_passed = Column(Boolean)  # Overall pass/fail
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    
    # Relationships
    framework = relationship("ComplianceFramework", back_populates="audits")
    violations = relationship("ViolationReport", back_populates="audit")


class ViolationReport(Base):
    """Compliance violation or non-conformance report"""
    __tablename__ = "compliance_violation_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    regulation_id = Column(Integer, ForeignKey("compliance_regulations.id"))
    audit_id = Column(Integer, ForeignKey("compliance_audits.id"), nullable=True)
    
    # Basic Info
    violation_code = Column(String(50), unique=True, nullable=False, index=True)  # VIO-001
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=False)
    violation_type = Column(String(50))  # Non_Conformance, Deviation, Observation, Opportunity
    
    # Discovery
    discovered_date = Column(Date, nullable=False)
    discovered_by = Column(String(200))  # Person who found it
    discovery_method = Column(String(50))  # Audit, Inspection, Self_Report, Complaint, Incident
    
    # Severity
    severity = Column(String(50))  # Critical, Major, Minor, Observation
    risk_level = Column(String(50))  # Critical, High, Medium, Low
    impact = Column(String(50))  # Safety, Quality, Legal, Financial, Reputation
    
    # Details
    location = Column(String(200))  # Where violation occurred
    department = Column(String(200))
    process_affected = Column(String(200))
    root_cause = Column(Text)  # Root cause analysis
    contributing_factors = Column(JSON)
    
    # Regulatory Impact
    regulatory_requirement = Column(Text)  # What was violated
    potential_penalties = Column(Text)
    legal_implications = Column(Text)
    reportable_to_authority = Column(Boolean, default=False)
    authority_notified = Column(Boolean, default=False)
    notification_date = Column(Date)
    
    # Evidence
    evidence_description = Column(Text)
    evidence_files = Column(JSON)  # List of file paths/IDs
    photos = Column(JSON)
    witnesses = Column(JSON)  # List of witness names
    
    # Immediate Actions
    immediate_action_taken = Column(Text)
    immediate_action_date = Column(Date)
    immediate_action_by = Column(String(200))
    
    # Corrective Action
    corrective_action_required = Column(Boolean, default=True)
    corrective_action_plan = Column(Text)
    corrective_action_owner = Column(String(200))
    corrective_action_deadline = Column(Date)
    corrective_action_completed = Column(Boolean, default=False)
    corrective_action_completion_date = Column(Date)
    
    # Preventive Action
    preventive_action_required = Column(Boolean, default=False)
    preventive_action_plan = Column(Text)
    preventive_action_deadline = Column(Date)
    preventive_action_completed = Column(Boolean, default=False)
    
    # Verification
    verification_required = Column(Boolean, default=True)
    verification_method = Column(String(100))  # Re_Audit, Inspection, Document_Review
    verified_by = Column(String(200))
    verification_date = Column(Date)
    verification_status = Column(String(50))  # Pending, Verified, Not_Verified
    verification_notes = Column(Text)
    
    # Costs
    estimated_cost_to_fix = Column(Float)
    actual_cost = Column(Float)
    potential_penalty_amount = Column(Float)
    
    # Recurrence
    is_repeat_violation = Column(Boolean, default=False)
    previous_violation_ids = Column(JSON)  # IDs of previous similar violations
    recurrence_count = Column(Integer, default=0)
    
    # Status
    status = Column(String(50), default="Open")  # Open, In_Progress, Resolved, Verified, Closed
    resolution_date = Column(Date)
    closure_date = Column(Date)
    closure_approved_by = Column(String(200))
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    
    # Relationships
    regulation = relationship("Regulation", back_populates="violations")
    audit = relationship("ComplianceAudit", back_populates="violations")
