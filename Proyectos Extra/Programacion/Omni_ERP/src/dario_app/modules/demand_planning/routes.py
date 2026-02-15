"""Demand Planning API routes (Dynamics 365 parity)."""

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import uuid

from dario_app.database import get_db

router = APIRouter(prefix="/demand_planning", tags=["Demand Planning"])


class ForecastCreate(BaseModel):
    product_id: str
    forecast_period_start: datetime
    forecast_period_end: datetime
    baseline_demand: float
    forecast_method: str = "Time_Series"


class SeasonalityCreate(BaseModel):
    factor_name: str
    factor_type: str
    product_id: Optional[str] = None


class ScenarioCreate(BaseModel):
    scenario_name: str
    scenario_type: str
    base_period_start: datetime
    base_period_end: datetime
    parameters: dict


@router.post("/forecasts")
async def create_forecast(data: ForecastCreate, session: AsyncSession = Depends(get_db), org_id: str = "default"):
    """Create demand forecast."""
    from dario_app.modules.demand_planning.models import DemandForecast
    
    forecast = DemandForecast(
        organization_id=org_id,
        forecast_code=f"FOR-{uuid.uuid4().hex[:8].upper()}",
        product_id=data.product_id,
        forecast_period_start=data.forecast_period_start,
        forecast_period_end=data.forecast_period_end,
        baseline_demand=data.baseline_demand,
        total_demand=data.baseline_demand,
        forecast_method=data.forecast_method
    )
    session.add(forecast)
    await session.commit()
    return {"forecast_id": forecast.id, "forecast_code": forecast.forecast_code}


@router.get("/forecasts")
async def list_forecasts(session: AsyncSession = Depends(get_db), product_id: Optional[str] = None, status: Optional[str] = None, org_id: str = "default"):
    """List demand forecasts."""
    from dario_app.modules.demand_planning.models import DemandForecast
    
    query = select(DemandForecast).where(DemandForecast.organization_id == org_id)
    if product_id:
        query = query.where(DemandForecast.product_id == product_id)
    if status:
        query = query.where(DemandForecast.status == status)
    
    result = await session.execute(query)
    forecasts = result.scalars().all()
    
    return {
        "total": len(forecasts),
        "forecasts": [
            {
                "id": f.id,
                "forecast_code": f.forecast_code,
                "product_id": f.product_id,
                "forecast_period": f"{f.forecast_period_start.date()} to {f.forecast_period_end.date()}",
                "baseline_demand": f.baseline_demand,
                "total_demand": f.total_demand,
                "forecast_method": f.forecast_method,
                "status": f.status,
                "forecast_error": f.forecast_error
            }
            for f in forecasts
        ]
    }


@router.get("/forecasts/{forecast_id}")
async def get_forecast_details(forecast_id: str, session: AsyncSession = Depends(get_db)):
    """Get detailed forecast information."""
    from dario_app.modules.demand_planning.models import DemandForecast
    
    forecast = await session.get(DemandForecast, forecast_id)
    if not forecast:
        raise HTTPException(status_code=404, detail="Forecast not found")
    
    return {
        "forecast_id": forecast.id,
        "forecast_code": forecast.forecast_code,
        "product_id": forecast.product_id,
        "baseline_demand": forecast.baseline_demand,
        "trend_demand": forecast.trend_demand,
        "seasonal_demand": forecast.seasonal_demand,
        "promotional_demand": forecast.promotional_demand,
        "total_demand": forecast.total_demand,
        "upper_confidence_bound": forecast.upper_confidence_bound,
        "lower_confidence_bound": forecast.lower_confidence_bound,
        "forecast_method": forecast.forecast_method,
        "forecast_error": forecast.forecast_error,
        "status": forecast.status,
        "actual_demand": forecast.actual_demand,
        "variance": forecast.variance
    }


@router.post("/seasonality-factors")
async def create_seasonality_factor(data: SeasonalityCreate, session: AsyncSession = Depends(get_db), org_id: str = "default"):
    """Create seasonality factor."""
    from dario_app.modules.demand_planning.models import SeasonalityFactor
    
    factor = SeasonalityFactor(
        organization_id=org_id,
        factor_code=f"SEA-{uuid.uuid4().hex[:8].upper()}",
        factor_name=data.factor_name,
        factor_type=data.factor_type,
        product_id=data.product_id,
        period_type="Month"
    )
    session.add(factor)
    await session.commit()
    return {"factor_id": factor.id, "factor_code": factor.factor_code}


@router.get("/seasonality-factors")
async def list_seasonality_factors(session: AsyncSession = Depends(get_db), factor_type: Optional[str] = None, org_id: str = "default"):
    """List seasonality factors."""
    from dario_app.modules.demand_planning.models import SeasonalityFactor
    
    query = select(SeasonalityFactor).where(SeasonalityFactor.organization_id == org_id)
    if factor_type:
        query = query.where(SeasonalityFactor.factor_type == factor_type)
    
    result = await session.execute(query)
    factors = result.scalars().all()
    
    return {
        "total": len(factors),
        "factors": [
            {
                "id": f.id,
                "factor_code": f.factor_code,
                "factor_name": f.factor_name,
                "factor_type": f.factor_type,
                "avg_seasonality_index": f.avg_seasonality_index,
                "is_active": f.is_active
            }
            for f in factors
        ]
    }


@router.post("/planning-scenarios")
async def create_scenario(data: ScenarioCreate, session: AsyncSession = Depends(get_db), org_id: str = "default"):
    """Create planning scenario."""
    from dario_app.modules.demand_planning.models import PlanningScenario
    
    scenario = PlanningScenario(
        organization_id=org_id,
        scenario_code=f"SCN-{uuid.uuid4().hex[:8].upper()}",
        scenario_name=data.scenario_name,
        scenario_type=data.scenario_type,
        base_period_start=data.base_period_start,
        base_period_end=data.base_period_end,
        parameters=data.parameters,
        status="Draft"
    )
    session.add(scenario)
    await session.commit()
    return {"scenario_id": scenario.id, "scenario_code": scenario.scenario_code}


@router.get("/planning-scenarios")
async def list_scenarios(session: AsyncSession = Depends(get_db), scenario_type: Optional[str] = None, status: Optional[str] = None, org_id: str = "default"):
    """List planning scenarios."""
    from dario_app.modules.demand_planning.models import PlanningScenario
    
    query = select(PlanningScenario).where(PlanningScenario.organization_id == org_id)
    if scenario_type:
        query = query.where(PlanningScenario.scenario_type == scenario_type)
    if status:
        query = query.where(PlanningScenario.status == status)
    
    result = await session.execute(query)
    scenarios = result.scalars().all()
    
    return {
        "total": len(scenarios),
        "scenarios": [
            {
                "id": s.id,
                "scenario_code": s.scenario_code,
                "scenario_name": s.scenario_name,
                "scenario_type": s.scenario_type,
                "status": s.status,
                "total_projected_demand": s.total_projected_demand,
                "variance_percent": s.variance_percent
            }
            for s in scenarios
        ]
    }


@router.get("/forecast-accuracy")
async def get_forecast_accuracy(session: AsyncSession = Depends(get_db), product_id: Optional[str] = None, org_id: str = "default"):
    """Get forecast accuracy metrics."""
    from dario_app.modules.demand_planning.models import ForecastAccuracy
    
    query = select(ForecastAccuracy).where(ForecastAccuracy.organization_id == org_id)
    if product_id:
        query = query.where(ForecastAccuracy.product_id == product_id)
    
    result = await session.execute(query)
    accuracy_records = result.scalars().all()
    
    if not accuracy_records:
        return {
            "message": "No forecast accuracy data available yet",
            "total_records": 0
        }
    
    return {
        "total_records": len(accuracy_records),
        "accuracy_metrics": [
            {
                "accuracy_code": a.accuracy_code,
                "measurement_period": a.measurement_period,
                "forecast_method": a.forecast_method,
                "mape": a.mean_absolute_percentage_error,
                "mae": a.mean_absolute_error,
                "rmse": a.root_mean_squared_error,
                "directional_accuracy": a.directional_accuracy
            }
            for a in accuracy_records
        ]
    }


@router.get("/analytics/demand-analysis")
async def get_demand_analysis(product_id: Optional[str] = None, org_id: str = "default"):
    """Get demand analysis and trends."""
    return {
        "organization_id": org_id,
        "product_id": product_id,
        "total_forecasts": 0,
        "avg_forecast_accuracy": 0.0,
        "demand_trend": "Stable",
        "seasonality_detected": False,
        "forecast_methods_used": [],
        "recommendations": []
    }
