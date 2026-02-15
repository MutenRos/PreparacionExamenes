"""Advanced Inventory Optimization Models."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship

from dario_app.database import Base


class ABCAnalysisResult(Base):
    """ABC inventory classification based on consumption value."""
    
    __tablename__ = "abc_analysis_result"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, nullable=False, index=True)
    analysis_date = Column(DateTime, default=datetime.utcnow)
    product_id = Column(Integer, nullable=False)
    category = Column(String(1), nullable=False)  # A, B, C
    annual_consumption_value = Column(Float)
    percentage_of_total = Column(Float)
    cumulative_percentage = Column(Float)
    priority_level = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DemandForecast(Base):
    """Demand forecasting using time series analysis."""
    
    __tablename__ = "demand_forecast"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, nullable=False, index=True)
    product_id = Column(Integer, nullable=False)
    forecast_period = Column(String(50), nullable=False)
    forecasting_method = Column(String(50))  # moving_average, exponential_smoothing, regression
    forecast_quantity = Column(Float)
    confidence_interval_lower = Column(Float)
    confidence_interval_upper = Column(Float)
    confidence_level = Column(Float)
    forecast_accuracy = Column(Float)
    seasonality_factor = Column(Float)
    trend = Column(String(20))  # upward, downward, stable
    created_at = Column(DateTime, default=datetime.utcnow)
    forecast_date = Column(DateTime)


class SafetyStockCalculation(Base):
    """Safety stock optimization for demand and supply variability."""
    
    __tablename__ = "safety_stock_calculation"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, nullable=False, index=True)
    product_id = Column(Integer, nullable=False)
    average_demand = Column(Float)
    demand_std_deviation = Column(Float)
    lead_time_days = Column(Integer)
    lead_time_std_deviation = Column(Float)
    service_level = Column(Float)  # 95%, 99%, etc.
    z_score = Column(Float)
    calculated_safety_stock = Column(Float)
    current_safety_stock = Column(Float)
    reorder_point = Column(Float)
    optimization_recommendation = Column(Text)
    last_calculated = Column(DateTime, default=datetime.utcnow)


class SupplierPerformance(Base):
    """Track and optimize supplier performance metrics."""
    
    __tablename__ = "supplier_performance"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, nullable=False, index=True)
    supplier_id = Column(Integer, nullable=False)
    evaluation_period = Column(String(50))
    on_time_delivery_rate = Column(Float)  # percentage
    quality_acceptance_rate = Column(Float)
    price_competitiveness_score = Column(Float)
    communication_score = Column(Float)
    overall_performance_score = Column(Float)
    delivery_time_variance = Column(Float)
    defect_rate = Column(Float)
    lead_time_reliability = Column(Float)
    tier_classification = Column(String(20))  # Tier 1, Tier 2, Tier 3
    certification_status = Column(String(50))
    last_audit_date = Column(DateTime)
    performance_trend = Column(String(20))  # improving, stable, declining
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ReorderOptimization(Base):
    """Reorder point and quantity optimization."""
    
    __tablename__ = "reorder_optimization"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, nullable=False, index=True)
    product_id = Column(Integer, nullable=False)
    current_reorder_point = Column(Float)
    optimal_reorder_point = Column(Float)
    current_order_quantity = Column(Float)
    economic_order_quantity = Column(Float)
    holding_cost_per_unit = Column(Float)
    ordering_cost_per_order = Column(Float)
    stockout_cost_per_unit = Column(Float)
    total_annual_inventory_cost = Column(Float)
    potential_cost_savings = Column(Float)
    optimization_status = Column(String(50))  # recommended, implemented, deferred
    implementation_date = Column(DateTime)
    last_optimized = Column(DateTime, default=datetime.utcnow)


class InventoryTurnoverAnalysis(Base):
    """Inventory turnover ratio and efficiency analysis."""
    
    __tablename__ = "inventory_turnover_analysis"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, nullable=False, index=True)
    product_id = Column(Integer, nullable=False)
    analysis_period = Column(String(50))
    beginning_inventory = Column(Float)
    ending_inventory = Column(Float)
    average_inventory = Column(Float)
    cost_of_goods_sold = Column(Float)
    turnover_ratio = Column(Float)
    days_inventory_outstanding = Column(Float)
    inventory_velocity = Column(Float)
    slow_moving_indicator = Column(Boolean, default=False)
    obsolescence_risk = Column(String(20))  # low, medium, high
    recommendations = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class StockoutPrevention(Base):
    """Stockout prevention and alert system."""
    
    __tablename__ = "stockout_prevention"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, nullable=False, index=True)
    product_id = Column(Integer, nullable=False)
    current_stock_level = Column(Float)
    reorder_point = Column(Float)
    minimum_required_stock = Column(Float)
    stockout_probability = Column(Float)
    days_until_stockout = Column(Integer)
    alert_status = Column(String(50))  # normal, warning, critical
    alert_timestamp = Column(DateTime)
    recommended_action = Column(Text)
    supplier_lead_time = Column(Integer)
    alternative_supplier_available = Column(Boolean, default=False)
    emergency_procurement_option = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class InventoryOptimizationReport(Base):
    """Summary report on inventory optimization recommendations."""
    
    __tablename__ = "inventory_optimization_report"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, nullable=False, index=True)
    report_name = Column(String(200))
    report_date = Column(DateTime, default=datetime.utcnow)
    period_covered = Column(String(50))
    total_products_analyzed = Column(Integer)
    abc_categories = Column(JSON)  # {"A": count, "B": count, "C": count}
    estimated_cost_savings = Column(Float)
    inventory_reduction_potential = Column(Float)
    improvement_opportunities = Column(Integer)
    critical_alerts = Column(Integer)
    supplier_performance_summary = Column(JSON)
    recommendations_count = Column(Integer)
    implementation_status = Column(String(50))
    report_details = Column(Text)
    created_by = Column(String(200))
    last_modified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
