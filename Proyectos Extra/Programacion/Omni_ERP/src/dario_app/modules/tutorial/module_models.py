"""Extended database model for module-specific tutorial progress."""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class ModuleTutorialProgress(Base):
    """Track tutorial progress for each module per user."""

    __tablename__ = "module_tutorial_progress"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    org_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    module_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    # Module tutorial state
    has_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    current_step: Mapped[int] = mapped_column(Integer, default=0)
    last_step_viewed: Mapped[int] = mapped_column(Integer, default=0)
    
    # Store completed step numbers as JSON array
    completed_steps: Mapped[dict] = mapped_column(JSON, default=list)

    # Timestamps
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_accessed_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<ModuleTutorialProgress(user={self.user_id}, module={self.module_name}, step={self.current_step})>"
