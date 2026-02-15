"""Demand Planning & Forecasting Models (Dynamics 365 parity)."""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, Text

from dario_app.database import Base


class DemandForecast(Base):
    """Demand forecasting for inventory and production planning."""
    __tablename__ = "demand_forecasts"

    id = Column(String(36), primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    organization_id = Column(String(36), nullable=False, index=True)
    forecast_code = Column(String(50), unique=True, nullable=False)
    
    # Product & location
    product_id = Column(String(36), nullable=False, index=True)
    warehouse_id = Column(String(36))  # Optional - forecast can be location-specific
    customer_id = Column(String(36))  # Optional - customer-specific forecast
    
    # Time period
    forecast_period_start = Column(DateTime, nullable=False)
    forecast_period_end = Column(DateTime, nullable=False)
    forecast_type = Column(String(50), nullable=False)  # Daily, Weekly, Monthly, Quarterly, Annual
    
    # Forecast values
    baseline_demand = Column(Float, nullable=False)
    trend_demand = Column(Float, default=0.0)
    seasonal_demand = Column(Float, default=0.0)
    promotional_demand = Column(Float, default=0.0)
    
    total_demand = Column(Float, nullable=False)
    upper_confidence_bound = Column(Float)  # Upper bound estimate (90%)
    lower_confidence_bound = Column(Float)  # Lower bound estimate (10%)
    
    # Forecast method
    forecast_method = Column(String(50), nullable=False)  # Time_Series, Regression, ML_Model, Consensus, Manual
    model_version = Column(String(50))
    
    # Seasonality
    seasonality_index = Column(Float)
    seasonal_factors = Column(JSON)  # {month: factor}
    
    # Factors
    influencing_factors = Column(JSON, default=[])  # ['Promotion', 'Holiday', 'Weather', 'Competition']
    
    # Accuracy tracking
    forecast_error = Column(Float)  # MAPE or other metric
    error_margin_percent = Column(Float)
    
    # Actual demand (populated later)
    actual_demand = Column(Float)
    actual_demand_date = Column(DateTime)
    variance = Column(Float)  # Actual - Forecast
    variance_percent = Column(Float)
    
    # Status
    status = Column(String(50), default="Draft")  # Draft, Published, Superseded, Archived
    published_date = Column(DateTime)
    is_locked = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SeasonalityFactor(Base):
    """Seasonality patterns and factors for demand forecasting."""
    __tablename__ = "seasonality_factors"

    id = Column(String(36), primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    organization_id = Column(String(36), nullable=False, index=True)
    factor_code = Column(String(50), unique=True, nullable=False)
    
    # Definition
    factor_name = Column(String(255), nullable=False)
    description = Column(Text)
    factor_type = Column(String(50), nullable=False)  # Monthly, Quarterly, Seasonal, Holiday, Custom
    
    # Scope
    product_id = Column(String(36))  # Can be null for all products
    product_category_id = Column(String(36))
    customer_id = Column(String(36))
    region = Column(String(100))
    
    # Pattern definition
    period_type = Column(String(50), nullable=False)  # Month, Quarter, Week, Day
    
    # Seasonal factors by period (1 = no seasonality, >1 = above average, <1 = below average)
    january_factor = Column(Float, default=1.0)
    february_factor = Column(Float, default=1.0)
    march_factor = Column(Float, default=1.0)
    april_factor = Column(Float, default=1.0)
    may_factor = Column(Float, default=1.0)
    june_factor = Column(Float, default=1.0)
    july_factor = Column(Float, default=1.0)
    august_factor = Column(Float, default=1.0)
    september_factor = Column(Float, default=1.0)
    october_factor = Column(Float, default=1.0)
    november_factor = Column(Float, default=1.0)
    december_factor = Column(Float, default=1.0)
    
    # Holiday adjustments
    holiday_factors = Column(JSON, default={})  # {holiday_name: factor}
    
    # Statistical measures
    avg_seasonality_index = Column(Float)
    standard_deviation = Column(Float)
    
    # Data basis
    based_on_historical_years = Column(Integer)  # Number of years of data used
    last_updated_with_data = Column(DateTime)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ForecastAccuracy(Base):
    """Forecast accuracy metrics and analytics."""
    __tablename__ = "forecast_accuracy"

    id = Column(String(36), primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    organization_id = Column(String(36), nullable=False, index=True)
    accuracy_code = Column(String(50), unique=True, nullable=False)
    
    # Scope
    product_id = Column(String(36))
    product_category_id = Column(String(36))
    customer_id = Column(String(36))
    warehouse_id = Column(String(36))
    
    # Time period
    measurement_period = Column(String(50), nullable=False)  # YYYY-MM (monthly), YYYY (annual)
    
    # Forecast method being evaluated
    forecast_method = Column(String(50), nullable=False)  # Time_Series, Regression, ML_Model, etc.
    
    # Accuracy metrics
    mean_absolute_percentage_error = Column(Float)  # MAPE (0-100%)
    mean_absolute_error = Column(Float)  # MAE
    root_mean_squared_error = Column(Float)  # RMSE
    mean_bias_error = Column(Float)  # MBE (over/under forecast)
    
    # Directional accuracy
    directional_accuracy = Column(Float)  # % of correct up/down predictions
    
    # By demand size
    accuracy_high_volume = Column(Float)  # For products with >100 units
    accuracy_medium_volume = Column(Float)  # 10-100 units
    accuracy_low_volume = Column(Float)  # <10 units
    
    # Trend accuracy
    trend_capture_rate = Column(Float)  # % of trend correctly captured
    
    # Forecast bias
    over_forecast_percentage = Column(Float)
    under_forecast_percentage = Column(Float)
    
    # Comparison
    vs_previous_period = Column(Float)  # Improvement/degradation
    vs_benchmark = Column(Float)  # vs. industry benchmark
    vs_naive_forecast = Column(Float)  # vs. simple "same as last period"
    
    # Sample size
    forecast_evaluations = Column(Integer)
    
    # Insights
    top_improvement_opportunities = Column(JSON, default=[])
    root_cause_analysis = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PlanningScenario(Base):
    """What-if planning scenarios for demand simulation."""
    __tablename__ = "planning_scenarios"

    id = Column(String(36), primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    organization_id = Column(String(36), nullable=False, index=True)
    scenario_code = Column(String(50), unique=True, nullable=False)
    
    scenario_name = Column(String(255), nullable=False)
    description = Column(Text)
    scenario_type = Column(String(50), nullable=False)  # Best_Case, Worst_Case, Most_Likely, Custom
    
    # Base period
    base_period_start = Column(DateTime, nullable=False)
    base_period_end = Column(DateTime, nullable=False)
    
    # Scenario parameters
    parameters = Column(JSON, nullable=False)  # {param: value, param: value}
    # Examples: {'growth_rate': 0.15, 'promotion_discount': 0.20, 'market_expansion': True}
    
    # Scope
    product_ids = Column(JSON, default=[])  # List of product IDs affected
    applies_to_all_products = Column(Boolean, default=False)
    
    # Results
    scenario_demand = Column(JSON)  # {period: demand_value}
    total_projected_demand = Column(Float)
    variance_from_baseline = Column(Float)
    variance_percent = Column(Float)
    
    # Supply chain impact
    inventory_impact = Column(Text)  # Description of inventory implications
    capacity_impact = Column(Text)  # Description of capacity implications
    cost_impact = Column(Float)  # Projected cost change
    revenue_impact = Column(Float)  # Projected revenue change
    
    # Status & approval
    status = Column(String(50), default="Draft")  # Draft, Under_Review, Approved, Active, Archived
    created_by = Column(String(36))
    reviewed_by = Column(String(36))
    
    # Version control
    parent_scenario_id = Column(String(36))  # Link to base scenario if this is a variation
    version_number = Column(Integer, default=1)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
