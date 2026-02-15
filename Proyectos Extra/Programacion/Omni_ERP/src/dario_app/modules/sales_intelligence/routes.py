"""Sales Intelligence API routes (Dynamics 365 parity)."""

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import uuid

from dario_app.database import get_db

router = APIRouter(prefix="/sales_intelligence", tags=["Sales Intelligence"])


class InsightCreate(BaseModel):
    insight_type: str
    target_type: str
    target_id: str
    title: str
    description: str
    recommendation: Optional[str] = None


class OpportunityScoringCreate(BaseModel):
    name: str
    model_type: str
    accuracy_rate: Optional[float] = None


class CompetitorIntelCreate(BaseModel):
    competitor_name: str
    intel_type: str
    topic: str
    description: str


class ForecastCreate(BaseModel):
    forecast_period: str
    forecast_type: str
    quota: Optional[float] = None
    pipeline: Optional[float] = None


@router.post("/insights")
async def create_insight(data: InsightCreate, session: AsyncSession = Depends(get_db), org_id: str = "default"):
    """Create sales insight."""
    from dario_app.modules.sales_intelligence.models import SalesInsight
    
    insight = SalesInsight(
        organization_id=org_id,
        insight_code=f"INS-{uuid.uuid4().hex[:8].upper()}",
        insight_type=data.insight_type,
        target_type=data.target_type,
        target_id=data.target_id,
        title=data.title,
        description=data.description,
        recommendation=data.recommendation
    )
    session.add(insight)
    await session.commit()
    return {"insight_id": insight.id, "insight_code": insight.insight_code}


@router.get("/insights")
async def list_insights(session: AsyncSession = Depends(get_db), insight_type: Optional[str] = None, status: Optional[str] = None, org_id: str = "default"):
    """List sales insights."""
    from dario_app.modules.sales_intelligence.models import SalesInsight
    
    query = select(SalesInsight).where(SalesInsight.organization_id == org_id)
    if insight_type:
        query = query.where(SalesInsight.insight_type == insight_type)
    if status:
        query = query.where(SalesInsight.status == status)
    
    result = await session.execute(query)
    insights = result.scalars().all()
    
    return {
        "total": len(insights),
        "insights": [
            {
                "id": i.id,
                "insight_code": i.insight_code,
                "insight_type": i.insight_type,
                "title": i.title,
                "confidence_score": i.confidence_score,
                "status": i.status
            }
            for i in insights
        ]
    }


@router.patch("/insights/{insight_id}/acknowledge")
async def acknowledge_insight(insight_id: str, session: AsyncSession = Depends(get_db)):
    """Acknowledge insight."""
    from dario_app.modules.sales_intelligence.models import SalesInsight
    
    insight = await session.get(SalesInsight, insight_id)
    if not insight:
        raise HTTPException(status_code=404, detail="Insight not found")
    
    insight.status = "Acknowledged"
    insight.action_date = datetime.utcnow()
    await session.commit()
    
    return {"message": "Insight acknowledged"}


@router.post("/opportunity-scoring-models")
async def create_scoring_model(data: OpportunityScoringCreate, session: AsyncSession = Depends(get_db), org_id: str = "default"):
    """Create opportunity scoring model."""
    from dario_app.modules.sales_intelligence.models import OpportunityScoringModel
    
    model = OpportunityScoringModel(
        organization_id=org_id,
        model_code=f"OSM-{uuid.uuid4().hex[:8].upper()}",
        name=data.name,
        model_type=data.model_type,
        accuracy_rate=data.accuracy_rate
    )
    session.add(model)
    await session.commit()
    return {"model_id": model.id, "model_code": model.model_code}


@router.get("/opportunity-scoring-models")
async def list_scoring_models(session: AsyncSession = Depends(get_db), model_type: Optional[str] = None, org_id: str = "default"):
    """List opportunity scoring models."""
    from dario_app.modules.sales_intelligence.models import OpportunityScoringModel
    
    query = select(OpportunityScoringModel).where(OpportunityScoringModel.organization_id == org_id)
    if model_type:
        query = query.where(OpportunityScoringModel.model_type == model_type)
    
    result = await session.execute(query)
    models = result.scalars().all()
    
    return {
        "total": len(models),
        "models": [
            {
                "id": m.id,
                "model_code": m.model_code,
                "name": m.name,
                "model_type": m.model_type,
                "accuracy_rate": m.accuracy_rate
            }
            for m in models
        ]
    }


@router.post("/competitor-intelligence")
async def create_intel(data: CompetitorIntelCreate, session: AsyncSession = Depends(get_db), org_id: str = "default"):
    """Create competitor intelligence record."""
    from dario_app.modules.sales_intelligence.models import CompetitorIntelligence
    
    intel = CompetitorIntelligence(
        organization_id=org_id,
        intel_code=f"COMP-{uuid.uuid4().hex[:8].upper()}",
        competitor_name=data.competitor_name,
        intel_type=data.intel_type,
        topic=data.topic,
        description=data.description,
        discover_date=datetime.utcnow()
    )
    session.add(intel)
    await session.commit()
    return {"intel_id": intel.id, "intel_code": intel.intel_code}


@router.get("/competitor-intelligence")
async def list_competitor_intel(session: AsyncSession = Depends(get_db), competitor_name: Optional[str] = None, org_id: str = "default"):
    """List competitor intelligence records."""
    from dario_app.modules.sales_intelligence.models import CompetitorIntelligence
    
    query = select(CompetitorIntelligence).where(CompetitorIntelligence.organization_id == org_id)
    if competitor_name:
        query = query.where(CompetitorIntelligence.competitor_name == competitor_name)
    
    result = await session.execute(query)
    intel_records = result.scalars().all()
    
    return {
        "total": len(intel_records),
        "intelligence": [
            {
                "id": i.id,
                "intel_code": i.intel_code,
                "competitor_name": i.competitor_name,
                "intel_type": i.intel_type,
                "topic": i.topic,
                "impact_to_us": i.impact_to_us,
                "discover_date": i.discover_date
            }
            for i in intel_records
        ]
    }


@router.post("/sales-forecasts")
async def create_forecast(data: ForecastCreate, session: AsyncSession = Depends(get_db), org_id: str = "default"):
    """Create sales forecast."""
    from dario_app.modules.sales_intelligence.models import SalesForecast
    
    forecast = SalesForecast(
        organization_id=org_id,
        forecast_code=f"FOR-{uuid.uuid4().hex[:8].upper()}",
        forecast_period=data.forecast_period,
        forecast_type=data.forecast_type,
        quota=data.quota,
        pipeline=data.pipeline,
        weighted_pipeline=data.pipeline * 0.5 if data.pipeline else 0
    )
    session.add(forecast)
    await session.commit()
    return {"forecast_id": forecast.id, "forecast_code": forecast.forecast_code}


@router.get("/sales-forecasts")
async def list_forecasts(session: AsyncSession = Depends(get_db), forecast_type: Optional[str] = None, org_id: str = "default"):
    """List sales forecasts."""
    from dario_app.modules.sales_intelligence.models import SalesForecast
    
    query = select(SalesForecast).where(SalesForecast.organization_id == org_id)
    if forecast_type:
        query = query.where(SalesForecast.forecast_type == forecast_type)
    
    result = await session.execute(query)
    forecasts = result.scalars().all()
    
    return {
        "total": len(forecasts),
        "forecasts": [
            {
                "id": f.id,
                "forecast_code": f.forecast_code,
                "forecast_period": f.forecast_period,
                "forecast_type": f.forecast_type,
                "quota": f.quota,
                "pipeline": f.pipeline,
                "weighted_pipeline": f.weighted_pipeline,
                "forecast_confidence": f.forecast_confidence
            }
            for f in forecasts
        ]
    }


@router.get("/analytics/sales-health")
async def get_sales_health(org_id: str = "default"):
    """Get overall sales health analytics."""
    return {
        "organization_id": org_id,
        "total_insights": 0,
        "pending_insights": 0,
        "win_probability_average": 0.0,
        "pipeline_health": "Good",
        "top_risks": [],
        "recommendations": []
    }
