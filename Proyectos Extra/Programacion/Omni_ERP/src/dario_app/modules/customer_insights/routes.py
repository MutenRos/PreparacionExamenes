"""Customer Insights routes - Analytics, Segmentation, Predictions."""

from datetime import datetime, date, timedelta
from typing import Optional
from decimal import Decimal
import json

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import require_permission, get_tenant_db, get_org_id
from dario_app.modules.usuarios.models import Usuario

from .models import (
    CustomerSegment, CustomerSegmentMember, CustomerMetric,
    CustomerJourney, CustomerPrediction, CustomerInsightReport, CustomerFeedback
)

router = APIRouter(prefix="/api/customer-insights", tags=["Customer Insights"])


# Schemas

class SegmentCreate(BaseModel):
    name: str
    descripcion: Optional[str] = None
    segment_type: str = "dynamic"
    criteria: Optional[str] = None


class JourneyCreate(BaseModel):
    customer_id: int
    journey_type: str
    stage: str
    touchpoint: str
    touchpoint_detail: Optional[str] = None
    outcome: Optional[str] = None
    timestamp: Optional[str] = None


class FeedbackCreate(BaseModel):
    customer_id: int
    feedback_type: str = "survey"
    rating: Optional[int] = None
    nps_score: Optional[int] = None
    comment: Optional[str] = None
    sentiment: str = "neutral"
    feedback_date: str


# Segments

@router.post("/segments")
async def create_segment(
    payload: SegmentCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("customer_insights.segments.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate segment code
    stmt = select(CustomerSegment).where(CustomerSegment.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    segment_code = f"SEG-{count + 1:04d}"
    
    segment = CustomerSegment(
        organization_id=org_id,
        segment_code=segment_code,
        **payload.model_dump()
    )
    db.add(segment)
    await db.commit()
    await db.refresh(segment)
    return segment


@router.get("/segments")
async def list_segments(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("customer_insights.segments.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(CustomerSegment).where(CustomerSegment.organization_id == org_id)
    if status:
        query = query.where(CustomerSegment.status == status)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/segments/{segment_id}/members/{customer_id}")
async def add_member_to_segment(
    segment_id: int,
    customer_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("customer_insights.segments.manage")),
    org_id: int = Depends(get_org_id),
):
    member = CustomerSegmentMember(
        organization_id=org_id,
        segment_id=segment_id,
        customer_id=customer_id
    )
    db.add(member)
    
    # Update segment count
    segment_stmt = select(CustomerSegment).where(
        CustomerSegment.id == segment_id,
        CustomerSegment.organization_id == org_id
    )
    segment_result = await db.execute(segment_stmt)
    segment = segment_result.scalar_one_or_none()
    if segment:
        segment.member_count += 1
    
    await db.commit()
    await db.refresh(member)
    return member


@router.get("/segments/{segment_id}/members")
async def list_segment_members(
    segment_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("customer_insights.segments.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(CustomerSegmentMember).where(
        CustomerSegmentMember.organization_id == org_id,
        CustomerSegmentMember.segment_id == segment_id,
        CustomerSegmentMember.left_at.is_(None)
    )
    result = await db.execute(query)
    return result.scalars().all()


# Customer Metrics

@router.get("/metrics")
async def list_customer_metrics(
    customer_id: Optional[int] = None,
    rfm_segment: Optional[str] = None,
    churn_risk_level: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("customer_insights.metrics.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(CustomerMetric).where(CustomerMetric.organization_id == org_id)
    if customer_id:
        query = query.where(CustomerMetric.customer_id == customer_id)
    if rfm_segment:
        query = query.where(CustomerMetric.rfm_segment == rfm_segment)
    if churn_risk_level:
        query = query.where(CustomerMetric.churn_risk_level == churn_risk_level)
    query = query.order_by(CustomerMetric.lifetime_value.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/metrics/{customer_id}/calculate")
async def calculate_customer_metrics(
    customer_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("customer_insights.metrics.manage")),
    org_id: int = Depends(get_org_id),
):
    """Calculate/update metrics for a customer."""
    # Check if metrics exist
    stmt = select(CustomerMetric).where(
        CustomerMetric.organization_id == org_id,
        CustomerMetric.customer_id == customer_id
    )
    result = await db.execute(stmt)
    metric = result.scalar_one_or_none()
    
    if not metric:
        metric = CustomerMetric(
            organization_id=org_id,
            customer_id=customer_id
        )
        db.add(metric)
    
    # TODO: Calculate actual metrics from orders/activity
    # For now, using placeholder values
    metric.total_orders = 10
    metric.total_revenue = Decimal("5000")
    metric.lifetime_value = Decimal("5000")
    metric.avg_order_value = Decimal("500")
    metric.recency_score = 4
    metric.frequency_score = 3
    metric.monetary_score = 5
    metric.rfm_segment = "Champions"
    metric.churn_risk_score = 15
    metric.churn_risk_level = "low"
    metric.calculated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(metric)
    return metric


# Journey Tracking

@router.post("/journeys")
async def track_journey(
    payload: JourneyCreate,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id),
):
    timestamp = datetime.strptime(payload.timestamp, "%Y-%m-%d %H:%M:%S") if payload.timestamp else datetime.utcnow()
    
    journey = CustomerJourney(
        organization_id=org_id,
        timestamp=timestamp,
        **payload.model_dump(exclude={"timestamp"})
    )
    db.add(journey)
    await db.commit()
    await db.refresh(journey)
    return journey


@router.get("/journeys")
async def list_journeys(
    customer_id: Optional[int] = None,
    journey_type: Optional[str] = None,
    stage: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("customer_insights.journeys.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(CustomerJourney).where(CustomerJourney.organization_id == org_id)
    if customer_id:
        query = query.where(CustomerJourney.customer_id == customer_id)
    if journey_type:
        query = query.where(CustomerJourney.journey_type == journey_type)
    if stage:
        query = query.where(CustomerJourney.stage == stage)
    query = query.order_by(CustomerJourney.timestamp.desc()).limit(100)
    result = await db.execute(query)
    return result.scalars().all()


# Predictions

@router.post("/predictions/{customer_id}")
async def generate_prediction(
    customer_id: int,
    prediction_type: str,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("customer_insights.predictions.create")),
    org_id: int = Depends(get_org_id),
):
    """Generate AI prediction for customer."""
    # Get customer metrics
    metric_stmt = select(CustomerMetric).where(
        CustomerMetric.organization_id == org_id,
        CustomerMetric.customer_id == customer_id
    )
    metric_result = await db.execute(metric_stmt)
    metric = metric_result.scalar_one_or_none()
    
    # Simple prediction logic
    if prediction_type == "churn":
        if metric:
            prediction_value = "high_risk" if metric.churn_risk_score > 70 else "low_risk"
            confidence_score = Decimal(str(metric.churn_risk_score))
        else:
            prediction_value = "unknown"
            confidence_score = Decimal("0")
    elif prediction_type == "next_purchase":
        prediction_value = "within_30_days"
        confidence_score = Decimal("75")
    elif prediction_type == "product_recommendation":
        prediction_value = "premium_tier"
        confidence_score = Decimal("82")
    else:
        prediction_value = "unknown"
        confidence_score = Decimal("0")
    
    prediction = CustomerPrediction(
        organization_id=org_id,
        customer_id=customer_id,
        prediction_type=prediction_type,
        prediction_value=prediction_value,
        confidence_score=confidence_score,
        valid_until=datetime.utcnow() + timedelta(days=30)
    )
    db.add(prediction)
    await db.commit()
    await db.refresh(prediction)
    return prediction


@router.get("/predictions")
async def list_predictions(
    customer_id: Optional[int] = None,
    prediction_type: Optional[str] = None,
    min_confidence: Optional[float] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("customer_insights.predictions.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(CustomerPrediction).where(CustomerPrediction.organization_id == org_id)
    if customer_id:
        query = query.where(CustomerPrediction.customer_id == customer_id)
    if prediction_type:
        query = query.where(CustomerPrediction.prediction_type == prediction_type)
    if min_confidence:
        query = query.where(CustomerPrediction.confidence_score >= min_confidence)
    query = query.order_by(CustomerPrediction.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


# Reports

@router.post("/reports/rfm-analysis")
async def generate_rfm_report(
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("customer_insights.reports.create")),
    org_id: int = Depends(get_org_id),
):
    """Generate RFM segmentation report."""
    # Get all customer metrics
    stmt = select(CustomerMetric).where(CustomerMetric.organization_id == org_id)
    result = await db.execute(stmt)
    metrics = result.scalars().all()
    
    # Count by RFM segment
    segments = {}
    for metric in metrics:
        seg = metric.rfm_segment or "Unknown"
        segments[seg] = segments.get(seg, 0) + 1
    
    report_data = {
        "segments": segments,
        "total_customers": len(metrics),
        "generated_at": datetime.utcnow().isoformat()
    }
    
    # Generate report number
    report_stmt = select(CustomerInsightReport).where(CustomerInsightReport.organization_id == org_id)
    report_result = await db.execute(report_stmt)
    count = len(report_result.scalars().all())
    report_number = f"CIR-{datetime.now().strftime('%Y%m')}-{count + 1:05d}"
    
    report = CustomerInsightReport(
        organization_id=org_id,
        report_number=report_number,
        report_type="rfm_analysis",
        title="RFM Segmentation Analysis",
        data=json.dumps(report_data),
        period_start=date.today() - timedelta(days=365),
        period_end=date.today(),
        generated_by_user_id=user.id,
        generated_by_name=user.nombre_completo
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)
    return report


@router.get("/reports")
async def list_reports(
    report_type: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("customer_insights.reports.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(CustomerInsightReport).where(CustomerInsightReport.organization_id == org_id)
    if report_type:
        query = query.where(CustomerInsightReport.report_type == report_type)
    query = query.order_by(CustomerInsightReport.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


# Feedback

@router.post("/feedback")
async def create_feedback(
    payload: FeedbackCreate,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id),
):
    feedback = CustomerFeedback(
        organization_id=org_id,
        **payload.model_dump()
    )
    db.add(feedback)
    await db.commit()
    await db.refresh(feedback)
    return feedback


@router.get("/feedback")
async def list_feedback(
    customer_id: Optional[int] = None,
    sentiment: Optional[str] = None,
    feedback_type: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("customer_insights.feedback.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(CustomerFeedback).where(CustomerFeedback.organization_id == org_id)
    if customer_id:
        query = query.where(CustomerFeedback.customer_id == customer_id)
    if sentiment:
        query = query.where(CustomerFeedback.sentiment == sentiment)
    if feedback_type:
        query = query.where(CustomerFeedback.feedback_type == feedback_type)
    query = query.order_by(CustomerFeedback.feedback_date.desc())
    result = await db.execute(query)
    return result.scalars().all()


# Analytics

@router.get("/analytics/nps")
async def get_nps_score(
    days: int = 30,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("customer_insights.analytics.read")),
    org_id: int = Depends(get_org_id),
):
    """Calculate Net Promoter Score."""
    cutoff_date = date.today() - timedelta(days=days)
    
    stmt = select(CustomerFeedback).where(
        CustomerFeedback.organization_id == org_id,
        CustomerFeedback.nps_score.isnot(None),
        CustomerFeedback.feedback_date >= cutoff_date
    )
    result = await db.execute(stmt)
    feedbacks = result.scalars().all()
    
    if not feedbacks:
        return {"nps_score": 0, "sample_size": 0}
    
    promoters = sum(1 for f in feedbacks if f.nps_score >= 9)
    detractors = sum(1 for f in feedbacks if f.nps_score <= 6)
    total = len(feedbacks)
    
    nps = ((promoters - detractors) / total * 100) if total > 0 else 0
    
    return {
        "nps_score": round(nps, 2),
        "promoters": promoters,
        "passives": total - promoters - detractors,
        "detractors": detractors,
        "sample_size": total
    }


@router.get("/analytics/lifetime-value")
async def get_ltv_distribution(
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("customer_insights.analytics.read")),
    org_id: int = Depends(get_org_id),
):
    """Get customer lifetime value distribution."""
    stmt = select(CustomerMetric).where(CustomerMetric.organization_id == org_id)
    result = await db.execute(stmt)
    metrics = result.scalars().all()
    
    # Calculate buckets
    buckets = {
        "0-1000": 0,
        "1000-5000": 0,
        "5000-10000": 0,
        "10000+": 0
    }
    
    total_ltv = Decimal("0")
    for metric in metrics:
        ltv = metric.lifetime_value
        total_ltv += ltv
        
        if ltv < 1000:
            buckets["0-1000"] += 1
        elif ltv < 5000:
            buckets["1000-5000"] += 1
        elif ltv < 10000:
            buckets["5000-10000"] += 1
        else:
            buckets["10000+"] += 1
    
    avg_ltv = (total_ltv / len(metrics)) if metrics else Decimal("0")
    
    return {
        "distribution": buckets,
        "average_ltv": float(avg_ltv),
        "total_customers": len(metrics)
    }
