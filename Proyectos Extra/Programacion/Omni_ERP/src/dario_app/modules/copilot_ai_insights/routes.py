"""Dynamics 365 Copilot & AI Insights Routes - API endpoints for AI features."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from dario_app.database import get_db
from dario_app.modules.copilot_ai_insights import models
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api/copilot-ai", tags=["copilot_ai_insights"])


# Pydantic Schemas
class AIInsightCreate(BaseModel):
    insight_type: str
    title: str
    description: Optional[str] = None
    confidence_score: float
    impact_score: float
    urgency_level: str
    affected_entity_type: Optional[str] = None
    affected_entity_id: Optional[int] = None
    recommended_action: Optional[str] = None
    implementation_cost: Optional[float] = None
    expected_benefit: Optional[float] = None


class AIInsightUpdate(BaseModel):
    status: Optional[str] = None
    confidence_score: Optional[float] = None
    reviewed_by: Optional[str] = None


class CopilotInteractionCreate(BaseModel):
    assistant_id: int
    user_id: int
    user_query: str
    context_entities: Optional[dict] = None


class PredictiveModelCreate(BaseModel):
    model_name: str
    model_type: str
    target_entity: str
    accuracy_score: Optional[float] = None
    features_used: List[str]
    training_dataset_size: int


class PromptTemplateCreate(BaseModel):
    template_name: str
    template_category: str
    prompt_template: str
    output_format: str
    required_variables: List[str]
    example_response: Optional[str] = None


# AI Insights Endpoints
@router.post("/insights", response_model=dict)
async def create_ai_insight(
    insight: AIInsightCreate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Create a new AI insight."""
    db_insight = models.AIInsight(
        organization_id=organization_id,
        insight_type=insight.insight_type,
        title=insight.title,
        description=insight.description,
        confidence_score=insight.confidence_score,
        impact_score=insight.impact_score,
        urgency_level=insight.urgency_level,
        affected_entity_type=insight.affected_entity_type,
        affected_entity_id=insight.affected_entity_id,
        recommended_action=insight.recommended_action,
        implementation_cost=insight.implementation_cost,
        expected_benefit=insight.expected_benefit,
    )
    db.add(db_insight)
    await db.commit()
    await db.refresh(db_insight)
    return {"id": db_insight.id, "status": "created"}


@router.get("/insights")
async def list_ai_insights(
    organization_id: int = Query(...),
    insight_type: Optional[str] = None,
    status: Optional[str] = None,
    min_confidence: Optional[float] = 0.0,
    db: AsyncSession = Depends(get_db)
):
    """List all AI insights with optional filters."""
    query = db.query(models.AIInsight).filter(
        models.AIInsight.organization_id == organization_id
    )
    
    if insight_type:
        query = query.filter(models.AIInsight.insight_type == insight_type)
    if status:
        query = query.filter(models.AIInsight.status == status)
    if min_confidence:
        query = query.filter(models.AIInsight.confidence_score >= min_confidence)
    
    insights = await query.all()
    return {"insights": insights, "total": len(insights)}


@router.get("/insights/{insight_id}")
async def get_ai_insight(
    insight_id: int,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific AI insight."""
    insight = await db.query(models.AIInsight).filter(
        models.AIInsight.id == insight_id,
        models.AIInsight.organization_id == organization_id
    ).first()
    
    if not insight:
        raise HTTPException(status_code=404, detail="Insight not found")
    return insight


@router.put("/insights/{insight_id}")
async def update_ai_insight(
    insight_id: int,
    update: AIInsightUpdate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Update an AI insight status."""
    insight = await db.query(models.AIInsight).filter(
        models.AIInsight.id == insight_id,
        models.AIInsight.organization_id == organization_id
    ).first()
    
    if not insight:
        raise HTTPException(status_code=404, detail="Insight not found")
    
    if update.status:
        insight.status = update.status
    if update.confidence_score is not None:
        insight.confidence_score = update.confidence_score
    if update.reviewed_by:
        insight.reviewed_by = update.reviewed_by
        insight.reviewed_at = datetime.utcnow()
    
    await db.commit()
    return {"id": insight.id, "status": "updated"}


# Copilot Assistant Endpoints
@router.post("/assistants")
async def create_copilot_assistant(
    name: str,
    assistant_type: str,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Create a new Copilot assistant."""
    assistant = models.CopilotAssistant(
        organization_id=organization_id,
        name=name,
        assistant_type=assistant_type,
    )
    db.add(assistant)
    await db.commit()
    await db.refresh(assistant)
    return {"id": assistant.id, "name": assistant.name}


@router.get("/assistants")
async def list_copilot_assistants(
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """List all Copilot assistants."""
    assistants = await db.query(models.CopilotAssistant).filter(
        models.CopilotAssistant.organization_id == organization_id
    ).all()
    return {"assistants": assistants, "total": len(assistants)}


@router.post("/interactions")
async def log_copilot_interaction(
    interaction: CopilotInteractionCreate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Log a Copilot user interaction."""
    db_interaction = models.CopilotInteraction(
        organization_id=organization_id,
        assistant_id=interaction.assistant_id,
        user_id=interaction.user_id,
        user_query=interaction.user_query,
        context_entities=interaction.context_entities,
    )
    db.add(db_interaction)
    await db.commit()
    await db.refresh(db_interaction)
    return {"id": db_interaction.id, "status": "logged"}


@router.get("/interactions")
async def get_interactions(
    organization_id: int = Query(...),
    user_id: Optional[int] = None,
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get interaction history."""
    query = db.query(models.CopilotInteraction).filter(
        models.CopilotInteraction.organization_id == organization_id
    )
    
    if user_id:
        query = query.filter(models.CopilotInteraction.user_id == user_id)
    
    interactions = await query.order_by(models.CopilotInteraction.created_at.desc()).limit(limit).all()
    return {"interactions": interactions, "total": len(interactions)}


# Predictive Models Endpoints
@router.post("/models")
async def create_predictive_model(
    model: PredictiveModelCreate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Create a new predictive model."""
    db_model = models.PredictiveModel(
        organization_id=organization_id,
        model_name=model.model_name,
        model_type=model.model_type,
        target_entity=model.target_entity,
        accuracy_score=model.accuracy_score,
        features_used=model.features_used,
        training_dataset_size=model.training_dataset_size,
        last_trained=datetime.utcnow(),
    )
    db.add(db_model)
    await db.commit()
    await db.refresh(db_model)
    return {"id": db_model.id, "model_name": db_model.model_name}


@router.get("/models")
async def list_predictive_models(
    organization_id: int = Query(...),
    model_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all predictive models."""
    query = db.query(models.PredictiveModel).filter(
        models.PredictiveModel.organization_id == organization_id,
        models.PredictiveModel.is_active == True
    )
    
    if model_type:
        query = query.filter(models.PredictiveModel.model_type == model_type)
    
    db_models = await query.all()
    return {"models": db_models, "total": len(db_models)}


@router.get("/models/{model_id}/metrics")
async def get_model_metrics(
    model_id: int,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Get detailed metrics for a model."""
    model = await db.query(models.PredictiveModel).filter(
        models.PredictiveModel.id == model_id,
        models.PredictiveModel.organization_id == organization_id
    ).first()
    
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    return {
        "model_id": model.id,
        "accuracy": model.accuracy_score,
        "precision": model.precision,
        "recall": model.recall,
        "f1_score": model.f1_score,
        "last_trained": model.last_trained,
    }


# Prompt Templates Endpoints
@router.post("/templates")
async def create_prompt_template(
    template: PromptTemplateCreate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Create a new prompt template."""
    db_template = models.AIPromptTemplate(
        organization_id=organization_id,
        template_name=template.template_name,
        template_category=template.template_category,
        prompt_template=template.prompt_template,
        output_format=template.output_format,
        required_variables=template.required_variables,
        example_response=template.example_response,
    )
    db.add(db_template)
    await db.commit()
    await db.refresh(db_template)
    return {"id": db_template.id, "template_name": db_template.template_name}


@router.get("/templates")
async def list_prompt_templates(
    organization_id: int = Query(...),
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List prompt templates."""
    query = db.query(models.AIPromptTemplate).filter(
        models.AIPromptTemplate.organization_id == organization_id
    )
    
    if category:
        query = query.filter(models.AIPromptTemplate.template_category == category)
    
    templates = await query.all()
    return {"templates": templates, "total": len(templates)}


# Market Insights Endpoints
@router.post("/market-insights")
async def create_market_insight(
    title: str,
    category: str,
    summary: str,
    organization_id: int = Query(...),
    recommendation: Optional[str] = None,
    estimated_impact: Optional[float] = None,
    db: AsyncSession = Depends(get_db)
):
    """Create a new market insight."""
    insight = models.MarketInsight(
        organization_id=organization_id,
        insight_title=title,
        insight_category=category,
        analysis_summary=summary,
        recommendation=recommendation,
        estimated_impact=estimated_impact,
    )
    db.add(insight)
    await db.commit()
    await db.refresh(insight)
    return {"id": insight.id, "status": "created"}


@router.get("/market-insights")
async def list_market_insights(
    organization_id: int = Query(...),
    category: Optional[str] = None,
    urgency: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List market insights."""
    query = db.query(models.MarketInsight).filter(
        models.MarketInsight.organization_id == organization_id
    )
    
    if category:
        query = query.filter(models.MarketInsight.insight_category == category)
    if urgency:
        query = query.filter(models.MarketInsight.urgency == urgency)
    
    insights = await query.order_by(models.MarketInsight.created_at.desc()).all()
    return {"insights": insights, "total": len(insights)}


# Health Check
@router.get("/health")
async def health_check():
    """Check Copilot AI module health."""
    return {
        "status": "healthy",
        "module": "copilot_ai_insights",
        "version": "1.0.0",
        "features": [
            "AI Insights",
            "Copilot Assistant",
            "Predictive Models",
            "Market Intelligence",
            "Prompt Templates"
        ]
    }
