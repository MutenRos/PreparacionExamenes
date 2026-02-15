"""Advanced Marketing & Campaign Management Models (Dynamics 365 parity)."""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
import enum

from dario_app.database import Base


class MarketingCampaign(Base):
    """Marketing campaign definition with budget and KPI tracking."""
    __tablename__ = "marketing_campaigns"

    id = Column(String(36), primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    organization_id = Column(String(36), nullable=False, index=True)
    campaign_code = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    campaign_type = Column(String(50), nullable=False)  # Email, Social, Webinar, Content, Event, Paid_Search
    status = Column(String(50), default="Draft")  # Draft, Scheduled, Active, Completed, Cancelled
    
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    launch_date = Column(DateTime)
    
    owner_id = Column(String(36))  # FK to User
    budget = Column(Float, default=0.0)
    actual_cost = Column(Float, default=0.0)
    
    target_audience_id = Column(String(36))  # FK to MarketingList
    expected_reach = Column(Integer)
    expected_revenue = Column(Float)
    
    channels = Column(JSON, default=[])  # ['Email', 'Social', 'Web']
    objectives = Column(JSON, default=[])  # ['Awareness', 'Lead Generation', 'Conversion']
    success_criteria = Column(JSON)  # {'target_reach': 5000, 'target_leads': 500}
    
    # Metrics
    actual_reach = Column(Integer, default=0)
    total_leads = Column(Integer, default=0)
    qualified_leads = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    roi_percent = Column(Float, default=0.0)
    
    template_id = Column(String(36))  # FK to CampaignTemplate
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MarketingActivity(Base):
    """Individual marketing activity/tactic within a campaign."""
    __tablename__ = "marketing_activities"

    id = Column(String(36), primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    organization_id = Column(String(36), nullable=False, index=True)
    activity_code = Column(String(50), unique=True, nullable=False)
    campaign_id = Column(String(36), ForeignKey("marketing_campaigns.id"), nullable=False)
    
    name = Column(String(255), nullable=False)
    activity_type = Column(String(50), nullable=False)  # Email_Send, Social_Post, Landing_Page, Event, Webinar
    description = Column(Text)
    
    status = Column(String(50), default="Planned")  # Planned, Scheduled, Active, Completed, Failed
    scheduled_date = Column(DateTime)
    actual_date = Column(DateTime)
    
    channel = Column(String(50), nullable=False)  # Email, Facebook, LinkedIn, Instagram, Twitter, Web
    
    # Performance metrics
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    click_through_rate = Column(Float, default=0.0)
    conversions = Column(Integer, default=0)
    conversion_rate = Column(Float, default=0.0)
    cost = Column(Float, default=0.0)
    revenue = Column(Float, default=0.0)
    
    target_list_id = Column(String(36))  # FK to MarketingList
    audience_size = Column(Integer)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MarketingList(Base):
    """Segment/list of contacts for marketing campaigns."""
    __tablename__ = "marketing_lists"

    id = Column(String(36), primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    organization_id = Column(String(36), nullable=False, index=True)
    list_code = Column(String(50), unique=True, nullable=False)
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    list_type = Column(String(50), nullable=False)  # Static, Dynamic, Ad_Hoc
    status = Column(String(50), default="Active")  # Active, Inactive, Archived
    
    # List definition
    segment_criteria = Column(JSON)  # { 'industry': 'Technology', 'country': 'USA', 'employee_count': '>100' }
    filter_expression = Column(Text)  # SQL-like filter
    
    # Member counts
    total_members = Column(Integer, default=0)
    active_members = Column(Integer, default=0)
    unsubscribed = Column(Integer, default=0)
    bounced = Column(Integer, default=0)
    
    # List health
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_member_sync = Column(DateTime)
    
    # Privacy
    double_opt_in = Column(Boolean, default=False)
    purpose = Column(String(255))  # GDPR purpose


class EmailTemplate(Base):
    """Email marketing templates."""
    __tablename__ = "email_templates"

    id = Column(String(36), primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    organization_id = Column(String(36), nullable=False, index=True)
    template_code = Column(String(50), unique=True, nullable=False)
    
    name = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)  # Promotional, Transactional, Newsletter, Nurture
    template_type = Column(String(50), nullable=False)  # Standard, Responsive, AMP
    status = Column(String(50), default="Draft")  # Draft, Active, Archived
    
    # Content
    subject_line = Column(String(255), nullable=False)
    preview_text = Column(String(255))
    html_content = Column(Text, nullable=False)
    plain_text_content = Column(Text)
    
    # Design
    template_language = Column(String(10), default="en")
    brand_variant = Column(String(50))
    
    # Personalization
    dynamic_content_blocks = Column(JSON)  # [{block_id: '', conditions: []}]
    personalization_fields = Column(JSON, default=[])  # ['FirstName', 'LastName', 'Company']
    
    # Compliance
    footer_required = Column(Boolean, default=True)
    unsubscribe_link = Column(Boolean, default=True)
    privacy_link = Column(Boolean, default=True)
    
    created_by = Column(String(36))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CustomerJourneyMap(Base):
    """Customer journey orchestration and automation."""
    __tablename__ = "customer_journey_maps"

    id = Column(String(36), primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    organization_id = Column(String(36), nullable=False, index=True)
    journey_code = Column(String(50), unique=True, nullable=False)
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    journey_type = Column(String(50), nullable=False)  # Awareness, Consideration, Decision, Retention, Advocacy
    persona_id = Column(String(36))  # FK to Persona
    
    status = Column(String(50), default="Draft")  # Draft, Active, Paused, Completed
    
    # Journey structure
    journey_stages = Column(JSON, default=[])  # [{stage: 'Awareness', activities: []}]
    entry_triggers = Column(JSON, default=[])  # [{trigger_type: 'email_open', action: 'send_email'}]
    exit_criteria = Column(JSON)
    
    # Automation rules
    automation_rules = Column(JSON, default=[])  # [{condition: '', then: '', else: ''}]
    branch_logic = Column(JSON)  # For A/B testing and personalization
    
    # Performance
    enrolled_contacts = Column(Integer, default=0)
    completed_contacts = Column(Integer, default=0)
    dropped_contacts = Column(Integer, default=0)
    avg_duration_days = Column(Float)
    conversion_rate = Column(Float, default=0.0)
    
    # Publishing
    is_published = Column(Boolean, default=False)
    published_date = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LeadScoreModel(Base):
    """Lead scoring and qualification models."""
    __tablename__ = "lead_score_models"

    id = Column(String(36), primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    organization_id = Column(String(36), nullable=False, index=True)
    model_code = Column(String(50), unique=True, nullable=False)
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    model_type = Column(String(50), nullable=False)  # Behavioral, Demographic, Firmographic, Engagement
    status = Column(String(50), default="Draft")  # Draft, Active, Archived
    
    # Scoring criteria
    scoring_rules = Column(JSON, default=[])  # [{criteria: 'email_open', points: 5}, {criteria: 'website_visit', points: 10}]
    
    # Lead grade thresholds
    grade_a_threshold = Column(Float, default=75.0)
    grade_b_threshold = Column(Float, default=50.0)
    grade_c_threshold = Column(Float, default=25.0)
    
    # Model performance
    model_accuracy = Column(Float)  # Percentage
    training_data_size = Column(Integer)
    last_trained_date = Column(DateTime)
    
    # Decay settings
    enable_decay = Column(Boolean, default=False)
    decay_rate = Column(Float)  # Percent per day
    
    # Engagement weights
    weights = Column(JSON, default={})  # {'email_engagement': 0.3, 'website_behavior': 0.4, 'demographic': 0.3}
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
