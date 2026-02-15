"""
Resource Scheduling Optimization Module - Routes
REST API endpoints for optimization jobs and schedule management
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from typing import List, Optional
from datetime import datetime, timedelta

from dario_app.database import get_db
from dario_app.modules.resource_scheduling_optimization.models import (
    OptimizationJob, ScheduleOptimization, ResourceRequirement,
    SchedulingParameter, OptimizationResult
)

router = APIRouter(prefix="/resource-scheduling-optimization", tags=["Resource Scheduling Optimization"])


# ============================================================================
# OPTIMIZATION JOBS
# ============================================================================

@router.post("/optimization-jobs")
async def create_optimization_job(
    organization_id: int,
    name: str,
    optimization_type: str,
    start_date: datetime,
    end_date: datetime,
    algorithm: Optional[str] = "Genetic",
    db: AsyncSession = Depends(get_db)
):
    """Create a new optimization job"""
    # Generate job code
    result = await db.execute(
        select(func.count(OptimizationJob.id)).where(
            OptimizationJob.organization_id == organization_id
        )
    )
    count = result.scalar() or 0
    job_code = f"OPT-{count + 1:04d}"
    
    job = OptimizationJob(
        organization_id=organization_id,
        job_code=job_code,
        name=name,
        optimization_type=optimization_type,
        start_date=start_date,
        end_date=end_date,
        algorithm=algorithm,
        created_by="system"
    )
    
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job


@router.get("/optimization-jobs")
async def get_optimization_jobs(
    organization_id: int,
    status: Optional[str] = None,
    optimization_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all optimization jobs"""
    query = select(OptimizationJob).where(
        OptimizationJob.organization_id == organization_id
    )
    
    if status:
        query = query.where(OptimizationJob.status == status)
    if optimization_type:
        query = query.where(OptimizationJob.optimization_type == optimization_type)
    
    query = query.order_by(OptimizationJob.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/optimization-jobs/{job_id}/start")
async def start_optimization_job(
    job_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Start an optimization job execution"""
    result = await db.execute(
        select(OptimizationJob).where(OptimizationJob.id == job_id)
    )
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Optimization job not found")
    
    if job.status not in ["Pending", "Failed"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot start job in status: {job.status}"
        )
    
    job.status = "Running"
    job.actual_start = datetime.utcnow()
    job.current_phase = "Initializing"
    job.progress_percentage = 0
    
    await db.commit()
    await db.refresh(job)
    
    # TODO: Trigger actual optimization algorithm here
    # This would be an async task that runs the optimization
    
    return job


@router.get("/optimization-jobs/{job_id}/progress")
async def get_optimization_progress(
    job_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get current progress of an optimization job"""
    result = await db.execute(
        select(OptimizationJob).where(OptimizationJob.id == job_id)
    )
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Optimization job not found")
    
    return {
        "job_id": job.id,
        "status": job.status,
        "progress_percentage": job.progress_percentage,
        "current_phase": job.current_phase,
        "iterations_completed": job.iterations_completed,
        "runtime_seconds": job.runtime_seconds,
        "solution_quality": job.solution_quality
    }


# ============================================================================
# SCHEDULE OPTIMIZATIONS
# ============================================================================

@router.get("/schedule-optimizations")
async def get_schedule_optimizations(
    organization_id: int,
    job_id: Optional[int] = None,
    schedule_date: Optional[datetime] = None,
    resource_id: Optional[int] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get optimized schedules"""
    query = select(ScheduleOptimization).where(
        ScheduleOptimization.organization_id == organization_id
    )
    
    if job_id:
        query = query.where(ScheduleOptimization.job_id == job_id)
    if schedule_date:
        query = query.where(func.date(ScheduleOptimization.schedule_date) == schedule_date.date())
    if resource_id:
        query = query.where(ScheduleOptimization.resource_id == resource_id)
    if status:
        query = query.where(ScheduleOptimization.status == status)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/schedule-optimizations/{schedule_id}/approve")
async def approve_schedule(
    schedule_id: int,
    accepted_by: str,
    db: AsyncSession = Depends(get_db)
):
    """Approve an optimized schedule"""
    result = await db.execute(
        select(ScheduleOptimization).where(ScheduleOptimization.id == schedule_id)
    )
    schedule = result.scalar_one_or_none()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    schedule.status = "Approved"
    schedule.accepted_by = accepted_by
    schedule.accepted_at = datetime.utcnow()
    schedule.is_published = True
    schedule.published_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(schedule)
    return schedule


@router.patch("/schedule-optimizations/{schedule_id}/reject")
async def reject_schedule(
    schedule_id: int,
    rejection_reason: str,
    db: AsyncSession = Depends(get_db)
):
    """Reject an optimized schedule"""
    result = await db.execute(
        select(ScheduleOptimization).where(ScheduleOptimization.id == schedule_id)
    )
    schedule = result.scalar_one_or_none()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    schedule.status = "Cancelled"
    schedule.rejection_reason = rejection_reason
    
    await db.commit()
    await db.refresh(schedule)
    return schedule


# ============================================================================
# RESOURCE REQUIREMENTS
# ============================================================================

@router.post("/resource-requirements")
async def create_resource_requirement(
    organization_id: int,
    name: str,
    resource_type: str,
    required_start: datetime,
    required_end: datetime,
    source_type: Optional[str] = None,
    source_id: Optional[int] = None,
    priority: str = "Medium",
    db: AsyncSession = Depends(get_db)
):
    """Create a resource requirement"""
    # Generate requirement code
    result = await db.execute(
        select(func.count(ResourceRequirement.id)).where(
            ResourceRequirement.organization_id == organization_id
        )
    )
    count = result.scalar() or 0
    req_code = f"REQ-{count + 1:04d}"
    
    # Calculate duration
    duration_hours = (required_end - required_start).total_seconds() / 3600
    
    requirement = ResourceRequirement(
        organization_id=organization_id,
        requirement_code=req_code,
        name=name,
        resource_type=resource_type,
        required_start=required_start,
        required_end=required_end,
        duration_hours=duration_hours,
        source_type=source_type,
        source_id=source_id,
        priority=priority,
        created_by="system"
    )
    
    db.add(requirement)
    await db.commit()
    await db.refresh(requirement)
    return requirement


@router.get("/resource-requirements")
async def get_resource_requirements(
    organization_id: int,
    status: Optional[str] = None,
    resource_type: Optional[str] = None,
    assignment_status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all resource requirements"""
    query = select(ResourceRequirement).where(
        ResourceRequirement.organization_id == organization_id
    )
    
    if status:
        query = query.where(ResourceRequirement.status == status)
    if resource_type:
        query = query.where(ResourceRequirement.resource_type == resource_type)
    if assignment_status:
        query = query.where(ResourceRequirement.assignment_status == assignment_status)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/resource-requirements/{requirement_id}/assign")
async def assign_resource_requirement(
    requirement_id: int,
    resource_id: int,
    scheduled_start: datetime,
    scheduled_end: datetime,
    db: AsyncSession = Depends(get_db)
):
    """Assign a resource to a requirement"""
    result = await db.execute(
        select(ResourceRequirement).where(ResourceRequirement.id == requirement_id)
    )
    requirement = result.scalar_one_or_none()
    if not requirement:
        raise HTTPException(status_code=404, detail="Requirement not found")
    
    requirement.assigned_resource_id = resource_id
    requirement.scheduled_start = scheduled_start
    requirement.scheduled_end = scheduled_end
    requirement.assignment_status = "Assigned"
    requirement.status = "Scheduled"
    
    await db.commit()
    await db.refresh(requirement)
    return requirement


# ============================================================================
# SCHEDULING PARAMETERS
# ============================================================================

@router.post("/scheduling-parameters")
async def create_scheduling_parameter(
    organization_id: int,
    name: str,
    parameter_type: str,
    data_type: str,
    parameter_value: str,
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Create a scheduling parameter"""
    # Generate parameter code
    result = await db.execute(
        select(func.count(SchedulingParameter.id)).where(
            SchedulingParameter.organization_id == organization_id
        )
    )
    count = result.scalar() or 0
    param_code = f"PAR-{count + 1:04d}"
    
    parameter = SchedulingParameter(
        organization_id=organization_id,
        parameter_code=param_code,
        name=name,
        parameter_type=parameter_type,
        data_type=data_type,
        parameter_value=parameter_value,
        category=category,
        default_value=parameter_value,
        created_by="system"
    )
    
    db.add(parameter)
    await db.commit()
    await db.refresh(parameter)
    return parameter


@router.get("/scheduling-parameters")
async def get_scheduling_parameters(
    organization_id: int,
    category: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all scheduling parameters"""
    query = select(SchedulingParameter).where(
        SchedulingParameter.organization_id == organization_id
    )
    
    if category:
        query = query.where(SchedulingParameter.category == category)
    if is_active is not None:
        query = query.where(SchedulingParameter.is_active == is_active)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/scheduling-parameters/{parameter_id}")
async def update_scheduling_parameter(
    parameter_id: int,
    parameter_value: str,
    change_reason: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Update a scheduling parameter value"""
    result = await db.execute(
        select(SchedulingParameter).where(SchedulingParameter.id == parameter_id)
    )
    parameter = result.scalar_one_or_none()
    if not parameter:
        raise HTTPException(status_code=404, detail="Parameter not found")
    
    # Store previous value
    parameter.previous_value = parameter.parameter_value
    parameter.parameter_value = parameter_value
    parameter.changed_at = datetime.utcnow()
    parameter.change_reason = change_reason
    
    await db.commit()
    await db.refresh(parameter)
    return parameter


# ============================================================================
# OPTIMIZATION RESULTS
# ============================================================================

@router.get("/optimization-results")
async def get_optimization_results(
    organization_id: int,
    job_id: Optional[int] = None,
    is_optimal: Optional[bool] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get optimization results"""
    query = select(OptimizationResult).where(
        OptimizationResult.organization_id == organization_id
    )
    
    if job_id:
        query = query.where(OptimizationResult.job_id == job_id)
    if is_optimal is not None:
        query = query.where(OptimizationResult.is_optimal == is_optimal)
    
    query = query.order_by(OptimizationResult.objective_value.asc())
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/optimization-results/{result_id}")
async def get_optimization_result_detail(
    result_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed optimization result"""
    result = await db.execute(
        select(OptimizationResult).where(OptimizationResult.id == result_id)
    )
    opt_result = result.scalar_one_or_none()
    if not opt_result:
        raise HTTPException(status_code=404, detail="Result not found")
    
    return opt_result


@router.get("/analytics/optimization-performance")
async def get_optimization_performance(
    organization_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get optimization performance analytics"""
    query = select(OptimizationJob).where(
        OptimizationJob.organization_id == organization_id,
        OptimizationJob.status == "Completed"
    )
    
    if start_date:
        query = query.where(OptimizationJob.created_at >= start_date)
    if end_date:
        query = query.where(OptimizationJob.created_at <= end_date)
    
    result = await db.execute(query)
    jobs = result.scalars().all()
    
    if not jobs:
        return {
            "total_jobs": 0,
            "avg_improvement": 0,
            "avg_runtime": 0,
            "success_rate": 0
        }
    
    total_improvement = sum(j.improvement_percentage or 0 for j in jobs)
    total_runtime = sum(j.runtime_seconds or 0 for j in jobs)
    successful = sum(1 for j in jobs if j.solution_quality and j.solution_quality > 80)
    
    return {
        "total_jobs": len(jobs),
        "avg_improvement": total_improvement / len(jobs),
        "avg_runtime": total_runtime / len(jobs),
        "success_rate": (successful / len(jobs)) * 100,
        "total_resources_optimized": sum(j.resources_evaluated or 0 for j in jobs)
    }
