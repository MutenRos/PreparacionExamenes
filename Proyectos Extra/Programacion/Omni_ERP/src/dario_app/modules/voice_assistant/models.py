"""Voice Assistant Models - Data structures for voice interaction."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class VoiceMessage(BaseModel):
    """A single message in the voice conversation."""
    id: str
    text: str
    is_user: bool
    timestamp: datetime
    confidence: Optional[float] = None  # Speech recognition confidence (0-1)
    intent: Optional[str] = None  # Detected intent (e.g., "search", "navigate", "create")
    action: Optional[str] = None  # Associated action to execute


class VoiceInput(BaseModel):
    """Input for voice assistant."""
    text: str = Field(..., description="User text input (speech-to-text result)")
    audio_confidence: Optional[float] = Field(None, description="Confidence of speech recognition")
    conversation_id: Optional[str] = Field(None, description="Ongoing conversation ID")


class VoiceResponse(BaseModel):
    """Response from voice assistant."""
    message: str = Field(..., description="Assistant response text")
    intent: str = Field(..., description="Detected user intent")
    action: Optional[str] = Field(None, description="Action to execute on frontend")
    action_params: Optional[dict] = Field(None, description="Parameters for the action")
    conversation_id: str = Field(..., description="Conversation ID for continuity")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    data: Optional[dict] = Field(None, description="Data returned from ERP operations")
    success: bool = Field(True, description="Whether the operation was successful")


class ConversationContext(BaseModel):
    """Maintains context within a conversation."""
    conversation_id: str
    messages: List[VoiceMessage] = []
    user_id: str
    org_id: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_action: Optional[str] = None
    last_intent: Optional[str] = None


class CommandMapping(BaseModel):
    """Maps natural language to system commands."""
    keywords: List[str]  # Words to trigger this command
    intent: str  # Intent name (e.g., "search", "navigate")
    action: str  # Action to perform
    action_params_template: Optional[dict] = None  # Template for parameters
    description: str  # Human-readable description
