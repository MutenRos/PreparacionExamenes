"""Dynamics 365 Copilot & AI Insights Models - Advanced AI Analytics."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
import enum

from dario_app.database import Base


class InsightType(str, enum.Enum):
    """Types of AI insights available."""
    SALES_FORECAST = "sales_forecast"
    CUSTOMER_CHURN = "customer_churn"
    INVENTORY_OPTIMIZATION = "inventory_optimization"
    CASH_FLOW_PREDICTION = "cash_flow_prediction"
    ANOMALY_DETECTION = "anomaly_detection"
    RECOMMENDATION = "recommendation"
    RISK_ASSESSMENT = "risk_assessment"
    PROCESS_OPTIMIZATION = "process_optimization"


class AIInsight(Base):
    """AI-generated insights and recommendations."""
    __tablename__ = "ai_insights"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)

    insight_type = Column(Enum(InsightType), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    
    confidence_score = Column(Float, default=0.0)  # 0.0 to 1.0
    impact_score = Column(Float, default=0.0)      # 0.0 to 1.0
    urgency_level = Column(String(50), default="low")  # low, medium, high, critical
    
    affected_entity_type = Column(String(100))  # Customer, Product, Order, etc.
    affected_entity_id = Column(Integer)
    
    recommended_action = Column(Text)
    implementation_cost = Column(Float)  # Estimated cost to implement
    expected_benefit = Column(Float)      # Expected benefit from action
    
    insight_metadata = Column("metadata", JSON)  # Additional context, parameters, etc.
    status = Column(String(50), default="new")  # new, reviewed, implemented, dismissed

    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    reviewed_at = Column(DateTime)
    implemented_at = Column(DateTime)
    reviewed_by = Column(String(255))
    
    insights = relationship("InsightDetail", back_populates="insight", cascade="all, delete-orphan")


class InsightDetail(Base):
    """Detailed breakdown of an AI insight."""
    __tablename__ = "insight_details"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    insight_id = Column(Integer, ForeignKey("ai_insights.id"), nullable=False)

    detail_type = Column(String(100))  # metric, trend, pattern, outlier
    label = Column(String(255))
    value = Column(Float)
    context = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    insight = relationship("AIInsight", back_populates="insights")


class CopilotAssistant(Base):
    """Copilot assistant configuration and interaction tracking."""
    __tablename__ = "copilot_assistants"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    assistant_type = Column(String(100))  # sales, finance, supply_chain, hr, service
    
    enabled_features = Column(JSON)  # Available features for this assistant
    prompt_templates = Column(JSON)   # Custom prompts
    
    users_count = Column(Integer, default=0)
    interactions_count = Column(Integer, default=0)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    interactions = relationship("CopilotInteraction", back_populates="assistant", cascade="all, delete-orphan")


class CopilotInteraction(Base):
    """User interactions with Copilot assistant."""
    __tablename__ = "copilot_interactions"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    assistant_id = Column(Integer, ForeignKey("copilot_assistants.id"))
    user_id = Column(Integer, nullable=False)

    user_query = Column(Text, nullable=False)
    copilot_response = Column(Text)
    response_type = Column(String(100))  # answer, recommendation, alert, suggestion
    
    satisfaction_score = Column(Float)  # 1-5 rating
    was_helpful = Column(Boolean)
    follow_up_questions = Column(JSON)  # Suggested follow-ups
    
    context_entities = Column(JSON)  # Related records (customer_id, order_id, etc.)
    model_version = Column(String(50))  # AI model version used
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    assistant = relationship("CopilotAssistant", back_populates="interactions")


class PredictiveModel(Base):
    """Predictive AI models for forecasting and analysis."""
    __tablename__ = "predictive_models"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)

    model_name = Column(String(255), nullable=False, unique=True)
    model_type = Column(String(100))  # regression, classification, clustering, time_series
    target_entity = Column(String(100))  # Sales, Inventory, Customer, etc.
    
    accuracy_score = Column(Float)  # Model accuracy on test data
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    
    last_trained = Column(DateTime)
    next_training = Column(DateTime)
    training_frequency = Column(String(50))  # daily, weekly, monthly
    
    features_used = Column(JSON)  # List of feature names
    training_dataset_size = Column(Integer)  # Rows used for training
    
    predictions_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    predictions = relationship("CopilotPrediction", back_populates="model", cascade="all, delete-orphan")


class CopilotPrediction(Base):
    """Individual predictions made by ML models."""
    __tablename__ = "copilot_predictions"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    model_id = Column(Integer, ForeignKey("predictive_models.id"), nullable=False)

    predicted_value = Column(Float, nullable=False)
    confidence_interval_lower = Column(Float)
    confidence_interval_upper = Column(Float)
    
    actual_value = Column(Float)  # To be filled later for validation
    error_percentage = Column(Float)  # Actual vs predicted error
    
    target_entity_type = Column(String(100))
    target_entity_id = Column(Integer)
    
    prediction_horizon = Column(String(100))  # 1_week, 1_month, 1_quarter, 1_year
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    materialized_at = Column(DateTime)  # When prediction happened

    model = relationship("PredictiveModel", back_populates="predictions")


class AIPromptTemplate(Base):
    """Reusable Copilot prompt templates for common tasks."""
    __tablename__ = "ai_prompt_templates"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)

    template_name = Column(String(255), nullable=False)
    template_category = Column(String(100))  # analysis, decision, reporting, automation
    
    prompt_template = Column(Text, nullable=False)  # Template with {variables}
    output_format = Column(String(100))  # json, markdown, html, email
    
    required_variables = Column(JSON)  # List of required {variables}
    example_response = Column(Text)
    
    usage_count = Column(Integer, default=0)
    success_rate = Column(Float)
    
    created_by = Column(String(255))
    is_standard = Column(Boolean, default=False)  # Microsoft-provided vs custom
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MarketInsight(Base):
    """Market and competitive intelligence AI insights."""
    __tablename__ = "market_insights"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)

    insight_title = Column(String(255), nullable=False)
    insight_category = Column(String(100))  # competitor, market_trend, customer_sentiment, technology
    
    source_data = Column(Text)  # Where this insight came from
    analysis_summary = Column(Text)
    
    relevant_products = Column(JSON)  # Product IDs affected
    relevant_customers = Column(JSON)  # Customer IDs affected
    
    recommendation = Column(Text)
    estimated_impact = Column(Float)  # Revenue or cost impact
    urgency = Column(String(50), default="medium")  # low, medium, high, critical
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    expires_at = Column(DateTime)  # When insight becomes stale
    
    actions_taken = relationship("InsightAction", back_populates="market_insight", cascade="all, delete-orphan")


class InsightAction(Base):
    """Actions taken based on AI insights."""
    __tablename__ = "insight_actions"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    market_insight_id = Column(Integer, ForeignKey("market_insights.id"))

    action_type = Column(String(100))  # price_change, inventory_adjustment, campaign, alert
    action_description = Column(Text)
    
    created_by = Column(String(255))
    status = Column(String(50), default="pending")  # pending, in_progress, completed, rejected
    
    effectiveness_score = Column(Float)  # How effective was the action?
    
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    market_insight = relationship("MarketInsight", back_populates="actions_taken")

