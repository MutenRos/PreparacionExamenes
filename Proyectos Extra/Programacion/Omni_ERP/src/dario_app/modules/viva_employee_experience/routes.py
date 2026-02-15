"""Dynamics 365 Viva Routes - Employee Experience API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from dario_app.database import get_db
from dario_app.modules.viva_employee_experience import models
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api/viva", tags=["viva_employee_experience"])


# Pydantic Schemas
class EngagementSurveyCreate(BaseModel):
    survey_name: str
    survey_type: str
    description: Optional[str] = None
    target_respondents: int


class WellnessInitiativeCreate(BaseModel):
    initiative_name: str
    category: str
    description: Optional[str] = None
    target_audience: Optional[str] = None
    budget: Optional[float] = None


class VivaGoalCreate(BaseModel):
    employee_id: int
    goal_title: str
    goal_type: str
    description: Optional[str] = None
    target_date: Optional[str] = None


class EmployeeFeedbackCreate(BaseModel):
    feedback_recipient_id: int
    feedback_provider_id: int
    feedback_type: str
    rating: Optional[float] = None
    strengths: Optional[str] = None
    areas_for_improvement: Optional[str] = None


class RecognitionCreate(BaseModel):
    recognized_employee_id: int
    recognized_by_id: int
    title: str
    description: Optional[str] = None
    recognition_type: str


# Engagement Survey Endpoints
@router.post("/surveys")
async def create_engagement_survey(
    survey: EngagementSurveyCreate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Create a new engagement survey."""
    db_survey = models.EmployeeEngagementSurvey(
        organization_id=organization_id,
        survey_name=survey.survey_name,
        survey_type=survey.survey_type,
        description=survey.description,
        target_respondents=survey.target_respondents,
    )
    db.add(db_survey)
    await db.commit()
    await db.refresh(db_survey)
    return {"id": db_survey.id, "survey_name": db_survey.survey_name, "status": "created"}


@router.get("/surveys")
async def list_engagement_surveys(
    organization_id: int = Query(...),
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List engagement surveys."""
    query = db.query(models.EmployeeEngagementSurvey).filter(
        models.EmployeeEngagementSurvey.organization_id == organization_id
    )
    
    if status:
        query = query.filter(models.EmployeeEngagementSurvey.status == status)
    
    surveys = await query.all()
    return {"surveys": surveys, "total": len(surveys)}


@router.get("/surveys/{survey_id}/results")
async def get_survey_results(
    survey_id: int,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Get survey results and analytics."""
    survey = await db.query(models.EmployeeEngagementSurvey).filter(
        models.EmployeeEngagementSurvey.id == survey_id,
        models.EmployeeEngagementSurvey.organization_id == organization_id
    ).first()
    
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    
    return {
        "survey_id": survey.id,
        "engagement_score": survey.overall_engagement_score,
        "response_rate": survey.response_rate,
        "respondents": survey.actual_respondents,
        "status": survey.status,
    }


# Wellness Endpoints
@router.post("/wellness/initiatives")
async def create_wellness_initiative(
    initiative: WellnessInitiativeCreate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Create a wellness initiative."""
    db_initiative = models.WellnessInitiative(
        organization_id=organization_id,
        initiative_name=initiative.initiative_name,
        initiative_category=initiative.category,
        description=initiative.description,
        target_audience=initiative.target_audience,
        budget=initiative.budget,
    )
    db.add(db_initiative)
    await db.commit()
    await db.refresh(db_initiative)
    return {"id": db_initiative.id, "initiative_name": db_initiative.initiative_name}


@router.get("/wellness/initiatives")
async def list_wellness_initiatives(
    organization_id: int = Query(...),
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List wellness initiatives."""
    query = db.query(models.WellnessInitiative).filter(
        models.WellnessInitiative.organization_id == organization_id
    )
    
    if category:
        query = query.filter(models.WellnessInitiative.initiative_category == category)
    
    initiatives = await query.all()
    return {"initiatives": initiatives, "total": len(initiatives)}


@router.get("/wellness/profiles/{employee_id}")
async def get_wellness_profile(
    employee_id: int,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Get employee wellness profile."""
    profile = await db.query(models.EmployeeWellnessProfile).filter(
        models.EmployeeWellnessProfile.employee_id == employee_id,
        models.EmployeeWellnessProfile.organization_id == organization_id
    ).first()
    
    if not profile:
        # Create a new profile if it doesn't exist
        profile = models.EmployeeWellnessProfile(
            organization_id=organization_id,
            employee_id=employee_id,
        )
        db.add(profile)
        await db.commit()
        await db.refresh(profile)
    
    return {
        "employee_id": employee_id,
        "overall_wellness_score": profile.overall_wellness_score,
        "physical_health": profile.physical_health_score,
        "mental_health": profile.mental_health_score,
        "financial_wellness": profile.financial_wellness_score,
        "social_wellness": profile.social_wellness_score,
        "professional_development": profile.professional_development_score,
        "risk_level": profile.risk_level,
    }


# Goals Endpoints
@router.post("/goals")
async def create_goal(
    goal: VivaGoalCreate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Create an employee goal."""
    db_goal = models.VivaGoal(
        organization_id=organization_id,
        employee_id=goal.employee_id,
        goal_title=goal.goal_title,
        goal_type=goal.goal_type,
        goal_description=goal.description,
    )
    db.add(db_goal)
    await db.commit()
    await db.refresh(db_goal)
    return {"id": db_goal.id, "goal_title": db_goal.goal_title, "status": "created"}


@router.get("/goals")
async def list_goals(
    organization_id: int = Query(...),
    employee_id: Optional[int] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List goals with optional filters."""
    query = db.query(models.VivaGoal).filter(
        models.VivaGoal.organization_id == organization_id
    )
    
    if employee_id:
        query = query.filter(models.VivaGoal.employee_id == employee_id)
    if status:
        query = query.filter(models.VivaGoal.status == status)
    
    goals = await query.all()
    return {"goals": goals, "total": len(goals)}


@router.post("/goals/{goal_id}/check-in")
async def add_goal_check_in(
    goal_id: int,
    progress_percentage: float,
    status_update: str,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Add a check-in to a goal."""
    goal = await db.query(models.VivaGoal).filter(
        models.VivaGoal.id == goal_id,
        models.VivaGoal.organization_id == organization_id
    ).first()
    
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    check_in = models.GoalCheckIn(
        organization_id=organization_id,
        goal_id=goal_id,
        progress_percentage=progress_percentage,
        status_update=status_update,
    )
    db.add(check_in)
    await db.commit()
    
    return {"id": check_in.id, "progress": progress_percentage}


# Feedback Endpoints
@router.post("/feedback")
async def submit_feedback(
    feedback: EmployeeFeedbackCreate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Submit employee feedback."""
    db_feedback = models.EmployeeFeedback(
        organization_id=organization_id,
        feedback_recipient_id=feedback.feedback_recipient_id,
        feedback_provider_id=feedback.feedback_provider_id,
        feedback_type=feedback.feedback_type,
        rating=feedback.rating,
        strengths=feedback.strengths,
        areas_for_improvement=feedback.areas_for_improvement,
    )
    db.add(db_feedback)
    await db.commit()
    await db.refresh(db_feedback)
    return {"id": db_feedback.id, "status": "submitted"}


@router.get("/feedback/{employee_id}")
async def get_employee_feedback(
    employee_id: int,
    organization_id: int = Query(...),
    feedback_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get feedback for an employee."""
    query = db.query(models.EmployeeFeedback).filter(
        models.EmployeeFeedback.feedback_recipient_id == employee_id,
        models.EmployeeFeedback.organization_id == organization_id,
        models.EmployeeFeedback.visibility_status == "visible"
    )
    
    if feedback_type:
        query = query.filter(models.EmployeeFeedback.feedback_type == feedback_type)
    
    feedback_items = await query.all()
    
    return {
        "employee_id": employee_id,
        "feedback_count": len(feedback_items),
        "feedback": feedback_items,
    }


# Recognition Endpoints
@router.post("/recognition")
async def create_recognition(
    recognition: RecognitionCreate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Create an employee recognition."""
    db_recognition = models.RecognitionEvent(
        organization_id=organization_id,
        recognized_employee_id=recognition.recognized_employee_id,
        recognized_by_id=recognition.recognized_by_id,
        title=recognition.title,
        description=recognition.description,
        recognition_type=recognition.recognition_type,
    )
    db.add(db_recognition)
    await db.commit()
    await db.refresh(db_recognition)
    return {"id": db_recognition.id, "title": db_recognition.title}


@router.get("/recognition/{employee_id}")
async def get_employee_recognition(
    employee_id: int,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Get recognitions for an employee."""
    recognitions = await db.query(models.RecognitionEvent).filter(
        models.RecognitionEvent.recognized_employee_id == employee_id,
        models.RecognitionEvent.organization_id == organization_id
    ).all()
    
    return {
        "employee_id": employee_id,
        "recognition_count": len(recognitions),
        "recognitions": recognitions,
        "total_points": sum([r.points_awarded for r in recognitions]),
    }


# Health Check
@router.get("/health")
async def health_check():
    """Check Viva Employee Experience module health."""
    return {
        "status": "healthy",
        "module": "viva_employee_experience",
        "version": "1.0.0",
        "features": [
            "Employee Engagement Surveys",
            "Wellness Initiatives",
            "Goal Management & Check-ins",
            "Peer & Manager Feedback",
            "Employee Recognition",
            "Wellness Profiles",
        ]
    }
