"""Dynamics 365 Viva Models - Employee Experience, Engagement, and Wellbeing."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
import enum

from dario_app.database import Base


class EngagementSurveyType(str, enum.Enum):
    """Types of employee engagement surveys."""
    PULSE = "pulse"
    ESAT = "esat"  # Employee Satisfaction
    NPS = "nps"    # Net Promoter Score  
    CLIMATE = "climate"
    CULTURE = "culture"
    CUSTOM = "custom"


class WellbeingCategory(str, enum.Enum):
    """Categories of employee wellbeing."""
    PHYSICAL = "physical"
    MENTAL = "mental"
    FINANCIAL = "financial"
    SOCIAL = "social"
    PROFESSIONAL = "professional"


class EmployeeEngagementSurvey(Base):
    """Employee engagement surveys and feedback."""
    __tablename__ = "employee_engagement_surveys"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)

    survey_name = Column(String(255), nullable=False)
    survey_type = Column(Enum(EngagementSurveyType), nullable=False)
    description = Column(Text)
    
    status = Column(String(50), default="draft")  # draft, active, closed, analyzed
    scheduled_start = Column(DateTime)
    scheduled_end = Column(DateTime)
    actual_start = Column(DateTime)
    actual_end = Column(DateTime)
    
    target_respondents = Column(Integer)
    actual_respondents = Column(Integer, default=0)
    response_rate = Column(Float, default=0.0)  # Percentage
    
    overall_engagement_score = Column(Float)  # 0-100
    
    questions_count = Column(Integer)
    average_completion_time = Column(Integer)  # Seconds
    
    created_by = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    questions = relationship("SurveyQuestion", back_populates="survey", cascade="all, delete-orphan")
    responses = relationship("SurveyResponse", back_populates="survey", cascade="all, delete-orphan")


class SurveyQuestion(Base):
    """Individual survey questions."""
    __tablename__ = "survey_questions"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    survey_id = Column(Integer, ForeignKey("employee_engagement_surveys.id"), nullable=False)

    question_text = Column(Text, nullable=False)
    question_type = Column(String(100))  # rating, multiple_choice, open_text, likert
    
    order_index = Column(Integer)
    is_required = Column(Boolean, default=True)
    
    options = Column(JSON)  # For multiple choice: ["option1", "option2", ...]
    
    average_response = Column(Float)  # For numeric questions
    response_distribution = Column(JSON)  # Distribution of responses

    survey = relationship("EmployeeEngagementSurvey", back_populates="questions")
    survey_responses = relationship("SurveyQuestionResponse", back_populates="question", cascade="all, delete-orphan")


class SurveyResponse(Base):
    """Survey responses from employees."""
    __tablename__ = "survey_responses"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    survey_id = Column(Integer, ForeignKey("employee_engagement_surveys.id"), nullable=False)
    
    respondent_id = Column(Integer)  # Employee ID
    respondent_department = Column(String(255))
    respondent_role = Column(String(255))
    
    completion_status = Column(String(50), default="in_progress")  # in_progress, completed
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    overall_sentiment = Column(String(50))  # positive, neutral, negative
    sentiment_score = Column(Float)  # -1.0 to 1.0

    survey = relationship("EmployeeEngagementSurvey", back_populates="responses")
    question_responses = relationship("SurveyQuestionResponse", back_populates="survey_response", cascade="all, delete-orphan")


class SurveyQuestionResponse(Base):
    """Individual question responses."""
    __tablename__ = "survey_question_responses"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    survey_response_id = Column(Integer, ForeignKey("survey_responses.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("survey_questions.id"), nullable=False)

    response_value = Column(Text)  # Text, number, or choice
    response_time = Column(Integer)  # Seconds to answer
    
    survey_response = relationship("SurveyResponse", back_populates="question_responses")
    question = relationship("SurveyQuestion", back_populates="survey_responses")


class EmployeeWellnessProfile(Base):
    """Employee wellness tracking and wellbeing programs."""
    __tablename__ = "employee_wellness_profiles"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    
    employee_id = Column(Integer, nullable=False, index=True)
    
    overall_wellness_score = Column(Float, default=0.0)  # 0-100
    physical_health_score = Column(Float, default=0.0)
    mental_health_score = Column(Float, default=0.0)
    financial_wellness_score = Column(Float, default=0.0)
    social_wellness_score = Column(Float, default=0.0)
    professional_development_score = Column(Float, default=0.0)
    
    wellness_goals = Column(JSON)  # Active goals
    wellness_activities = Column(JSON)  # Participated activities
    
    last_assessment = Column(DateTime)
    risk_level = Column(String(50), default="low")  # low, medium, high
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WellnessInitiative(Base):
    """Wellness programs and initiatives."""
    __tablename__ = "wellness_initiatives"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)

    initiative_name = Column(String(255), nullable=False)
    initiative_category = Column(Enum(WellbeingCategory), nullable=False)
    description = Column(Text)
    
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    
    objective = Column(Text)
    target_audience = Column(String(255))  # All, Department, Job Level, etc.
    
    enrollment_count = Column(Integer, default=0)
    participation_rate = Column(Float, default=0.0)
    
    success_metrics = Column(JSON)
    impact_on_wellness = Column(Float)  # Average improvement
    
    budget = Column(Float)
    budget_spent = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    activities = relationship("WellnessActivity", back_populates="initiative", cascade="all, delete-orphan")


class WellnessActivity(Base):
    """Individual wellness activities and events."""
    __tablename__ = "wellness_activities"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    initiative_id = Column(Integer, ForeignKey("wellness_initiatives.id"), nullable=False)

    activity_name = Column(String(255), nullable=False)
    activity_type = Column(String(100))  # workshop, challenge, class, session, retreat
    activity_category = Column(Enum(WellbeingCategory), nullable=False)
    
    description = Column(Text)
    
    scheduled_date = Column(DateTime)
    duration_minutes = Column(Integer)
    
    max_participants = Column(Integer)
    actual_participants = Column(Integer, default=0)
    completion_rate = Column(Float, default=0.0)
    
    learning_objectives = Column(JSON)
    instructor = Column(String(255))
    
    created_at = Column(DateTime, default=datetime.utcnow)

    initiative = relationship("WellnessInitiative", back_populates="activities")


class VivaGoal(Base):
    """Employee goals and career development."""
    __tablename__ = "viva_goals"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    
    employee_id = Column(Integer, nullable=False, index=True)
    manager_id = Column(Integer)
    
    goal_title = Column(String(255), nullable=False)
    goal_description = Column(Text)
    
    goal_type = Column(String(100))  # OKR, SMART, Project, Development
    alignment_level = Column(Integer)  # 0 = Not aligned, 5 = Perfectly aligned
    
    target_date = Column(DateTime)
    status = Column(String(50), default="active")  # active, on_track, at_risk, completed, abandoned
    
    completion_percentage = Column(Float, default=0.0)
    
    key_results = Column(JSON)  # For OKRs
    milestones = Column(JSON)  # Progress checkpoints
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    check_ins = relationship("GoalCheckIn", back_populates="goal", cascade="all, delete-orphan")


class GoalCheckIn(Base):
    """Goal progress check-ins and feedback."""
    __tablename__ = "goal_check_ins"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    goal_id = Column(Integer, ForeignKey("viva_goals.id"), nullable=False)

    check_in_date = Column(DateTime, default=datetime.utcnow)
    progress_percentage = Column(Float)
    
    status_update = Column(Text)
    challenges = Column(Text)
    next_steps = Column(Text)
    
    confidence_level = Column(String(50))  # low, medium, high
    
    feedback_from_manager = Column(Text)
    feedback_provided_at = Column(DateTime)
    
    goal = relationship("VivaGoal", back_populates="check_ins")


class EmployeeFeedback(Base):
    """Peer and manager feedback system."""
    __tablename__ = "employee_feedback"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)

    feedback_recipient_id = Column(Integer, nullable=False, index=True)
    feedback_provider_id = Column(Integer, nullable=False)
    
    feedback_type = Column(String(100))  # peer, manager, 360, anonymous
    
    rating = Column(Float)  # 1-5 or custom scale
    
    strengths = Column(Text)
    areas_for_improvement = Column(Text)
    specific_examples = Column(JSON)
    
    is_anonymous = Column(Boolean, default=False)
    is_actionable = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    visibility_status = Column(String(50), default="pending")  # pending, visible, archived


class RecognitionEvent(Base):
    """Employee recognition and rewards."""
    __tablename__ = "recognition_events"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    
    recognized_employee_id = Column(Integer, nullable=False, index=True)
    recognized_by_id = Column(Integer, nullable=False)
    
    recognition_type = Column(String(100))  # peer_to_peer, manager, award, milestone
    
    title = Column(String(255), nullable=False)
    description = Column(Text)
    
    significance_level = Column(String(50))  # low, medium, high, exceptional
    points_awarded = Column(Integer, default=0)
    
    visibility = Column(String(50), default="team")  # private, team, department, company
    
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)  # Badges may expire
