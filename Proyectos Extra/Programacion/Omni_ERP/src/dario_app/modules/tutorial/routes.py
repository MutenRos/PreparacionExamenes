"""API routes for tutorial system."""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import require_auth, get_org_id
from dario_app.core.dependencies import get_db
from dario_app.modules.tutorial.models import UserTutorialProgress
from dario_app.modules.tutorial.module_models import ModuleTutorialProgress
from dario_app.modules.tutorial.schemas import (
    TutorialCompleteSchema,
    TutorialStepSchema,
    UserTutorialStatusSchema,
)
from dario_app.modules.tutorial.steps import TUTORIAL_STEPS, get_step
from dario_app.modules.tutorial.module_tutorials import (
    get_module_tutorial,
    get_available_modules,
)

router = APIRouter(prefix="/api/tutorial", tags=["tutorial"])


@router.get("/steps", response_model=list[dict])
async def get_tutorial_steps():
    """Get all tutorial steps."""
    return TUTORIAL_STEPS


@router.get("/steps/{step_number}")
async def get_tutorial_step(step_number: int = Path(..., ge=1, le=50)):
    """Get specific tutorial step."""
    step = get_step(step_number)
    if not step:
        raise HTTPException(status_code=404, detail="Step not found")
    return step


@router.get("/status", response_model=UserTutorialStatusSchema)
async def get_tutorial_status(
    user_context=Depends(require_auth),
    db: AsyncSession = Depends(get_db),
    org_id: int = Depends(get_org_id),
):
    """Get user's tutorial progress status."""
    user_id = user_context["user_id"]
    stmt = select(UserTutorialProgress).where(
        (UserTutorialProgress.user_id == user_id)
        & (UserTutorialProgress.org_id == org_id)
    )
    result = await db.execute(stmt)
    progress = result.scalar_one_or_none()

    if not progress:
        # Create new progress record
        progress = UserTutorialProgress(
            user_id=user_id,
            org_id=org_id,
            current_step=1,
            last_step_viewed=0,
        )
        db.add(progress)
        await db.commit()
        await db.refresh(progress)

    total_steps = len(TUTORIAL_STEPS)
    percentage = (progress.current_step / total_steps) * 100 if total_steps > 0 else 0

    return UserTutorialStatusSchema(
        has_completed=progress.has_completed_tutorial,
        current_step=progress.current_step,
        total_steps=total_steps,
        percentage_complete=percentage,
    )


@router.post("/start")
async def start_tutorial(
    user_context=Depends(require_auth),
    db: AsyncSession = Depends(get_db),
    org_id: int = Depends(get_org_id),
):
    """Mark tutorial as started."""
    user_id = user_context["user_id"]
    stmt = select(UserTutorialProgress).where(
        (UserTutorialProgress.user_id == user_id)
        & (UserTutorialProgress.org_id == org_id)
    )
    result = await db.execute(stmt)
    progress = result.scalar_one_or_none()

    if not progress:
        progress = UserTutorialProgress(
            user_id=user_id,
            org_id=org_id,
            current_step=1,
            last_step_viewed=1,
        )
        db.add(progress)
    else:
        progress.current_step = 1
        progress.last_step_viewed = 1
        progress.started_at = datetime.utcnow()

    await db.commit()
    return {"status": "tutorial_started", "step": 1}


@router.post("/step/{step_number}")
async def update_tutorial_step(
    step_number: int,
    user_context=Depends(require_auth),
    db: AsyncSession = Depends(get_db),
    org_id: int = Depends(get_org_id),
):
    """Update user's current tutorial step."""
    user_id = user_context["user_id"]
    stmt = select(UserTutorialProgress).where(
        (UserTutorialProgress.user_id == user_id)
        & (UserTutorialProgress.org_id == org_id)
    )
    result = await db.execute(stmt)
    progress = result.scalar_one_or_none()

    if not progress:
        progress = UserTutorialProgress(
            user_id=user_id,
            org_id=org_id,
            current_step=step_number,
            last_step_viewed=step_number,
        )
        db.add(progress)
    else:
        progress.current_step = step_number
        progress.last_step_viewed = max(progress.last_step_viewed, step_number)

    await db.commit()
    return {"status": "step_updated", "current_step": step_number}


@router.post("/complete")
async def complete_tutorial(
    data: TutorialCompleteSchema,
    user_context=Depends(require_auth),
    db: AsyncSession = Depends(get_db),
    org_id: int = Depends(get_org_id),
):
    """Mark tutorial as complete."""
    user_id = user_context["user_id"]
    stmt = select(UserTutorialProgress).where(
        (UserTutorialProgress.user_id == user_id)
        & (UserTutorialProgress.org_id == org_id)
    )
    result = await db.execute(stmt)
    progress = result.scalar_one_or_none()

    if not progress:
        progress = UserTutorialProgress(
            user_id=user_id,
            org_id=org_id,
            current_step=len(TUTORIAL_STEPS),
            last_step_viewed=len(TUTORIAL_STEPS),
        )
        db.add(progress)

    if data.completed:
        progress.has_completed_tutorial = True
        progress.completed_at = datetime.utcnow()

    await db.commit()
    return {"status": "tutorial_completed", "completed": True}


@router.post("/skip")
async def skip_tutorial(
    user_context=Depends(require_auth),
    db: AsyncSession = Depends(get_db),
    org_id: int = Depends(get_org_id),
):
    """Skip tutorial and mark as complete."""
    user_id = user_context["user_id"]
    stmt = select(UserTutorialProgress).where(
        (UserTutorialProgress.user_id == user_id)
        & (UserTutorialProgress.org_id == org_id)
    )
    result = await db.execute(stmt)
    progress = result.scalar_one_or_none()

    if not progress:
        progress = UserTutorialProgress(
            user_id=user_id,
            org_id=org_id,
            has_completed_tutorial=True,
            completed_at=datetime.utcnow(),
        )
        db.add(progress)
    else:
        progress.has_completed_tutorial = True
        progress.completed_at = datetime.utcnow()

    await db.commit()
    return {"status": "tutorial_skipped"}


@router.delete("/reset")
async def reset_tutorial(
    user_context=Depends(require_auth),
    db: AsyncSession = Depends(get_db),
    org_id: int = Depends(get_org_id),
):
    """Reset tutorial progress to restart from beginning."""
    user_id = user_context["user_id"]
    stmt = select(UserTutorialProgress).where(
        (UserTutorialProgress.user_id == user_id)
        & (UserTutorialProgress.org_id == org_id)
    )
    result = await db.execute(stmt)
    progress = result.scalar_one_or_none()

    if progress:
        progress.has_completed_tutorial = False
        progress.current_step = 1
        progress.last_step_viewed = 1
        progress.completed_at = None
        progress.started_at = datetime.utcnow()
        await db.commit()

    return {"status": "tutorial_reset"}


# ============== MODULE-SPECIFIC TUTORIAL ROUTES ==============

@router.get("/modules")
async def get_available_tutorial_modules():
    """Get list of modules that have tutorials available."""
    return {
        "modules": get_available_modules(),
        "count": len(get_available_modules())
    }


@router.get("/modules/{module_name}/steps")
async def get_module_tutorial_steps(module_name: str):
    """Get all tutorial steps for a specific module."""
    steps = get_module_tutorial(module_name)
    if not steps:
        raise HTTPException(
            status_code=404,
            detail=f"No tutorial found for module: {module_name}"
        )
    return steps


@router.get("/modules/{module_name}/status")
async def get_module_tutorial_status(
    module_name: str,
    user_context=Depends(require_auth),
    db: AsyncSession = Depends(get_db),
    org_id: int = Depends(get_org_id),
):
    """Get user's progress for a specific module tutorial."""
    user_id = user_context["user_id"]
    
    # Verify module exists
    steps = get_module_tutorial(module_name)
    if not steps:
        raise HTTPException(
            status_code=404,
            detail=f"No tutorial found for module: {module_name}"
        )
    
    stmt = select(ModuleTutorialProgress).where(
        (ModuleTutorialProgress.user_id == user_id)
        & (ModuleTutorialProgress.org_id == org_id)
        & (ModuleTutorialProgress.module_name == module_name)
    )
    result = await db.execute(stmt)
    progress = result.scalar_one_or_none()

    if not progress:
        # Create new progress record
        progress = ModuleTutorialProgress(
            user_id=user_id,
            org_id=org_id,
            module_name=module_name,
            current_step=1,
            last_step_viewed=0,
            completed_steps=[],
        )
        db.add(progress)
        await db.commit()
        await db.refresh(progress)

    total_steps = len(steps)
    percentage = (progress.current_step / total_steps) * 100 if total_steps > 0 else 0

    return {
        "module": module_name,
        "has_completed": progress.has_completed,
        "current_step": progress.current_step,
        "total_steps": total_steps,
        "percentage_complete": percentage,
        "completed_steps": progress.completed_steps or [],
    }


@router.post("/modules/{module_name}/start")
async def start_module_tutorial(
    module_name: str,
    user_context=Depends(require_auth),
    db: AsyncSession = Depends(get_db),
    org_id: int = Depends(get_org_id),
):
    """Start or restart a module tutorial."""
    user_id = user_context["user_id"]
    
    # Verify module exists
    steps = get_module_tutorial(module_name)
    if not steps:
        raise HTTPException(
            status_code=404,
            detail=f"No tutorial found for module: {module_name}"
        )
    
    stmt = select(ModuleTutorialProgress).where(
        (ModuleTutorialProgress.user_id == user_id)
        & (ModuleTutorialProgress.org_id == org_id)
        & (ModuleTutorialProgress.module_name == module_name)
    )
    result = await db.execute(stmt)
    progress = result.scalar_one_or_none()

    if not progress:
        progress = ModuleTutorialProgress(
            user_id=user_id,
            org_id=org_id,
            module_name=module_name,
            current_step=1,
            last_step_viewed=1,
            completed_steps=[],
        )
        db.add(progress)
    else:
        progress.current_step = 1
        progress.last_step_viewed = 1
        progress.started_at = datetime.utcnow()
        progress.has_completed = False
        progress.completed_at = None

    await db.commit()
    return {"status": "module_tutorial_started", "module": module_name, "step": 1}


@router.post("/modules/{module_name}/step/{step_number}")
async def update_module_tutorial_step(
    module_name: str,
    step_number: int,
    user_context=Depends(require_auth),
    db: AsyncSession = Depends(get_db),
    org_id: int = Depends(get_org_id),
):
    """Update user's current step in module tutorial."""
    user_id = user_context["user_id"]
    
    stmt = select(ModuleTutorialProgress).where(
        (ModuleTutorialProgress.user_id == user_id)
        & (ModuleTutorialProgress.org_id == org_id)
        & (ModuleTutorialProgress.module_name == module_name)
    )
    result = await db.execute(stmt)
    progress = result.scalar_one_or_none()

    if not progress:
        progress = ModuleTutorialProgress(
            user_id=user_id,
            org_id=org_id,
            module_name=module_name,
            current_step=step_number,
            last_step_viewed=step_number,
            completed_steps=[step_number],
        )
        db.add(progress)
    else:
        progress.current_step = step_number
        progress.last_step_viewed = max(progress.last_step_viewed, step_number)
        
        # Add to completed steps if not already there
        completed = progress.completed_steps or []
        if step_number not in completed:
            completed.append(step_number)
            progress.completed_steps = completed

    await db.commit()
    return {
        "status": "step_updated",
        "module": module_name,
        "current_step": step_number
    }


@router.post("/modules/{module_name}/complete")
async def complete_module_tutorial(
    module_name: str,
    user_context=Depends(require_auth),
    db: AsyncSession = Depends(get_db),
    org_id: int = Depends(get_org_id),
):
    """Mark module tutorial as complete."""
    user_id = user_context["user_id"]
    
    stmt = select(ModuleTutorialProgress).where(
        (ModuleTutorialProgress.user_id == user_id)
        & (ModuleTutorialProgress.org_id == org_id)
        & (ModuleTutorialProgress.module_name == module_name)
    )
    result = await db.execute(stmt)
    progress = result.scalar_one_or_none()

    steps = get_module_tutorial(module_name)
    total_steps = len(steps) if steps else 0

    if not progress:
        progress = ModuleTutorialProgress(
            user_id=user_id,
            org_id=org_id,
            module_name=module_name,
            current_step=total_steps,
            last_step_viewed=total_steps,
            has_completed=True,
            completed_at=datetime.utcnow(),
        )
        db.add(progress)
    else:
        progress.has_completed = True
        progress.completed_at = datetime.utcnow()
        progress.current_step = total_steps

    await db.commit()
    return {
        "status": "module_tutorial_completed",
        "module": module_name,
        "completed": True
    }


@router.delete("/modules/{module_name}/reset")
async def reset_module_tutorial(
    module_name: str,
    user_context=Depends(require_auth),
    db: AsyncSession = Depends(get_db),
    org_id: int = Depends(get_org_id),
):
    """Reset module tutorial progress."""
    user_id = user_context["user_id"]
    
    stmt = select(ModuleTutorialProgress).where(
        (ModuleTutorialProgress.user_id == user_id)
        & (ModuleTutorialProgress.org_id == org_id)
        & (ModuleTutorialProgress.module_name == module_name)
    )
    result = await db.execute(stmt)
    progress = result.scalar_one_or_none()

    if progress:
        progress.has_completed = False
        progress.current_step = 1
        progress.last_step_viewed = 1
        progress.completed_at = None
        progress.started_at = datetime.utcnow()
        progress.completed_steps = []
        await db.commit()

    return {"status": "module_tutorial_reset", "module": module_name}


    return {"status": "tutorial_reset"}

