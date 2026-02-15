"""Pydantic schemas for tutorial API."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TutorialStepSchema(BaseModel):
    """Schema for a single tutorial step."""

    step_number: int
    title: str
    description: str
    selector: str  # CSS selector del elemento a destacar
    position: str  # "top", "bottom", "left", "right"
    highlight: bool  # True si debe resaltarse el elemento
    action_text: str  # "Siguiente", "Finalizar", etc.
    image_url: Optional[str] = None  # URL de imagen opcional


class UserTutorialStatusSchema(BaseModel):
    """Status of user's tutorial progress."""

    has_completed: bool
    current_step: int
    total_steps: int
    percentage_complete: float

    class Config:
        from_attributes = True


class UserTutorialProgressSchema(BaseModel):
    """Tutorial progress record."""

    user_id: int
    has_completed_tutorial: bool
    current_step: int
    last_step_viewed: int
    started_at: datetime
    completed_at: Optional[datetime]
    last_accessed_at: datetime

    class Config:
        from_attributes = True


class TutorialCompleteSchema(BaseModel):
    """Request to mark tutorial as complete."""

    completed: bool = True
    final_step: Optional[int] = None
