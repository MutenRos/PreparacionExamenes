"""Sales Intelligence & Sales Cloud Models (Dynamics 365 parity)."""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, Text
import enum

from dario_app.database import Base


class SalesInsight(Base):
    """Sales insights with AI-powered recommendations."""
    __tablename__ = "sales_insights"

    id = Column(String(36), primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    organization_id = Column(String(36), nullable=False, index=True)
    insight_code = Column(String(50), unique=True, nullable=False)
    
    insight_type = Column(String(50), nullable=False)  # Deal_Risk, Engagement, Competitor, Next_Best_Action
    target_type = Column(String(50), nullable=False)  # Opportunity, Account, Lead
    target_id = Column(String(36), nullable=False)
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    recommendation = Column(Text)
    
    # Confidence & impact
    confidence_score = Column(Float)  # 0-100%
    impact_level = Column(String(50))  # High, Medium, Low
    predicted_impact = Column(Float)  # Projected revenue impact
    
    # AI Analysis
    analysis_data = Column(JSON)  # Raw analysis results
    signals = Column(JSON, default=[])  # [{signal: 'no_recent_activity', weight: 0.3}]
    
    status = Column(String(50), default="New")  # New, Acknowledged, Acted_Upon, Dismissed
    action_date = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class OpportunityScoringModel(Base):
    """Opportunity prediction and scoring models."""
    __tablename__ = "opportunity_scoring_models"

    id = Column(String(36), primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    organization_id = Column(String(36), nullable=False, index=True)
    model_code = Column(String(50), unique=True, nullable=False)
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Model configuration
    model_type = Column(String(50), nullable=False)  # Win_Probability, Deal_Stage_Prediction, Churn_Risk
    status = Column(String(50), default="Active")
    
    # Scoring factors
    scoring_factors = Column(JSON, default=[])  # [{factor: 'deal_size', weight: 0.2, range: [0, 1000000]}]
    
    # Model accuracy
    accuracy_rate = Column(Float)  # Percentage
    precision = Column(Float)  # True positives
    recall = Column(Float)  # Coverage
    f1_score = Column(Float)
    
    # Performance on deals
    total_predictions = Column(Integer, default=0)
    correct_predictions = Column(Integer, default=0)
    
    # Model parameters
    feature_importance = Column(JSON)  # {feature: weight}
    threshold_settings = Column(JSON)  # {low: 0.3, medium: 0.6, high: 0.8}
    
    # Training metadata
    training_data_period = Column(String(100))  # e.g., "Last 2 years"
    last_retrained = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CompetitorIntelligence(Base):
    """Competitive intelligence and analysis."""
    __tablename__ = "competitor_intelligence"

    id = Column(String(36), primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    organization_id = Column(String(36), nullable=False, index=True)
    intel_code = Column(String(50), unique=True, nullable=False)
    
    competitor_name = Column(String(255), nullable=False)
    intel_type = Column(String(50), nullable=False)  # Product, Pricing, Market_Activity, Partnership
    
    # Details
    topic = Column(String(255), nullable=False)
    description = Column(Text)
    source_url = Column(String(500))
    source_type = Column(String(50))  # Website, News, Social, Report, Document
    
    # Intelligence details
    impact_to_us = Column(String(50))  # High, Medium, Low
    relevance_score = Column(Float)  # 0-100%
    
    # Analysis
    analysis = Column(Text)
    recommended_action = Column(Text)
    affected_opportunities = Column(JSON, default=[])  # List of opportunity IDs
    
    # Timeline
    discover_date = Column(DateTime, nullable=False)
    publish_date = Column(DateTime)
    
    # Distribution
    shared_with_sales = Column(Boolean, default=False)
    shared_date = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SalesForecast(Base):
    """Sales forecasting and predictive analytics."""
    __tablename__ = "sales_forecasts"

    id = Column(String(36), primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    organization_id = Column(String(36), nullable=False, index=True)
    forecast_code = Column(String(50), unique=True, nullable=False)
    
    forecast_period = Column(String(50), nullable=False)  # YYYY-MM (monthly), YYYY-Q# (quarterly), YYYY (yearly)
    forecast_type = Column(String(50), nullable=False)  # Quota, Pipeline, Revenue, Unit_Sales
    
    # Forecast parameters
    sales_org_id = Column(String(36))  # FK to SalesOrganization
    territory_id = Column(String(36))
    manager_id = Column(String(36))
    
    # Forecast values
    quota = Column(Float)
    pipeline = Column(Float)
    weighted_pipeline = Column(Float)
    
    # Forecast breakdown
    won_forecast = Column(Float)  # Already won deals
    at_risk_forecast = Column(Float)  # Deals at risk
    upside_forecast = Column(Float)  # Upside potential
    
    # Actual performance
    actual_revenue = Column(Float, default=0.0)
    actual_units = Column(Integer, default=0)
    forecast_variance = Column(Float)  # Actual - Forecast
    variance_percentage = Column(Float)
    
    # Confidence
    forecast_confidence = Column(String(50))  # Commit, Best_Case, Pipeline
    confidence_score = Column(Float)  # 0-100%
    
    # Comparison
    vs_prior_forecast = Column(Float)  # Change from previous forecast
    vs_quota = Column(Float)  # Variance from quota
    
    # Status
    is_finalized = Column(Boolean, default=False)
    finalized_date = Column(DateTime)
    submitted_by = Column(String(36))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
