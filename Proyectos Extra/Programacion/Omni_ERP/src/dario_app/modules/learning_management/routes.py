"""
Learning Management System Module - Routes
REST API endpoints for courses, enrollments, assessments, and certifications
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import List, Optional
from datetime import datetime

from dario_app.database import get_db
from dario_app.modules.learning_management.models import (
    Course, Lesson, Enrollment, Assessment, Certification, LearningPath
)

router = APIRouter(prefix="/learning-management", tags=["Learning Management"])


# ============================================================================
# COURSES
# ============================================================================

@router.post("/courses")
async def create_course(
    organization_id: int,
    title: str,
    description: str,
    category: str,
    difficulty_level: str = "Beginner",
    db: AsyncSession = Depends(get_db)
):
    """Create a new course"""
    result = await db.execute(
        select(func.count(Course.id)).where(Course.organization_id == organization_id)
    )
    count = result.scalar() or 0
    course_code = f"CRS-{count + 1:04d}"
    
    course = Course(
        organization_id=organization_id,
        course_code=course_code,
        title=title,
        description=description,
        category=category,
        difficulty_level=difficulty_level,
        created_by="system"
    )
    
    db.add(course)
    await db.commit()
    await db.refresh(course)
    return course


@router.get("/courses")
async def get_courses(
    organization_id: int,
    category: Optional[str] = None,
    difficulty_level: Optional[str] = None,
    status: Optional[str] = None,
    is_featured: Optional[bool] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all courses with filters"""
    query = select(Course).where(Course.organization_id == organization_id)
    
    if category:
        query = query.where(Course.category == category)
    if difficulty_level:
        query = query.where(Course.difficulty_level == difficulty_level)
    if status:
        query = query.where(Course.status == status)
    if is_featured is not None:
        query = query.where(Course.is_featured == is_featured)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/courses/{course_id}")
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    """Get course details with lessons"""
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.patch("/courses/{course_id}/publish")
async def publish_course(course_id: int, db: AsyncSession = Depends(get_db)):
    """Publish a course"""
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    course.status = "Published"
    course.is_active = True
    
    await db.commit()
    await db.refresh(course)
    return course


# ============================================================================
# LESSONS
# ============================================================================

@router.post("/lessons")
async def create_lesson(
    organization_id: int,
    course_id: int,
    title: str,
    content_type: str,
    sequence_order: int,
    duration_minutes: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """Create a lesson"""
    result = await db.execute(
        select(func.count(Lesson.id)).where(Lesson.organization_id == organization_id)
    )
    count = result.scalar() or 0
    lesson_code = f"LES-{count + 1:04d}"
    
    lesson = Lesson(
        organization_id=organization_id,
        course_id=course_id,
        lesson_code=lesson_code,
        title=title,
        content_type=content_type,
        sequence_order=sequence_order,
        duration_minutes=duration_minutes,
        created_by="system"
    )
    
    db.add(lesson)
    await db.commit()
    await db.refresh(lesson)
    return lesson


@router.get("/lessons")
async def get_lessons(
    organization_id: int,
    course_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all lessons"""
    query = select(Lesson).where(Lesson.organization_id == organization_id)
    
    if course_id:
        query = query.where(Lesson.course_id == course_id)
    
    query = query.order_by(Lesson.sequence_order)
    result = await db.execute(query)
    return result.scalars().all()


# ============================================================================
# ENROLLMENTS
# ============================================================================

@router.post("/enrollments")
async def enroll_student(
    organization_id: int,
    course_id: int,
    student_id: int,
    student_name: str,
    student_email: str,
    enrollment_method: str = "Self_Enrollment",
    db: AsyncSession = Depends(get_db)
):
    """Enroll a student in a course"""
    # Check if already enrolled
    existing = await db.execute(
        select(Enrollment).where(
            and_(
                Enrollment.course_id == course_id,
                Enrollment.student_id == student_id
            )
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Student already enrolled")
    
    result = await db.execute(
        select(func.count(Enrollment.id)).where(
            Enrollment.organization_id == organization_id
        )
    )
    count = result.scalar() or 0
    enrollment_code = f"ENR-{count + 1:04d}"
    
    enrollment = Enrollment(
        organization_id=organization_id,
        course_id=course_id,
        student_id=student_id,
        student_name=student_name,
        student_email=student_email,
        enrollment_code=enrollment_code,
        enrollment_method=enrollment_method,
        access_granted_date=datetime.utcnow(),
        created_by="system"
    )
    
    db.add(enrollment)
    
    # Update course enrollment count
    course_result = await db.execute(select(Course).where(Course.id == course_id))
    course = course_result.scalar_one_or_none()
    if course:
        course.current_enrollments += 1
    
    await db.commit()
    await db.refresh(enrollment)
    return enrollment


@router.get("/enrollments")
async def get_enrollments(
    organization_id: int,
    student_id: Optional[int] = None,
    course_id: Optional[int] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get enrollments"""
    query = select(Enrollment).where(Enrollment.organization_id == organization_id)
    
    if student_id:
        query = query.where(Enrollment.student_id == student_id)
    if course_id:
        query = query.where(Enrollment.course_id == course_id)
    if status:
        query = query.where(Enrollment.status == status)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/enrollments/{enrollment_id}/progress")
async def update_enrollment_progress(
    enrollment_id: int,
    progress_percentage: float,
    lessons_completed: int,
    db: AsyncSession = Depends(get_db)
):
    """Update enrollment progress"""
    result = await db.execute(
        select(Enrollment).where(Enrollment.id == enrollment_id)
    )
    enrollment = result.scalar_one_or_none()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    enrollment.progress_percentage = progress_percentage
    enrollment.lessons_completed = lessons_completed
    enrollment.last_accessed_date = datetime.utcnow()
    
    if progress_percentage >= 100:
        enrollment.status = "Completed"
        enrollment.completed_date = datetime.utcnow()
    elif progress_percentage > 0:
        enrollment.status = "In_Progress"
        if not enrollment.started_date:
            enrollment.started_date = datetime.utcnow()
    
    await db.commit()
    await db.refresh(enrollment)
    return enrollment


@router.patch("/enrollments/{enrollment_id}/complete")
async def complete_enrollment(
    enrollment_id: int,
    final_score: float,
    issue_certificate: bool = True,
    db: AsyncSession = Depends(get_db)
):
    """Complete an enrollment"""
    result = await db.execute(
        select(Enrollment).where(Enrollment.id == enrollment_id)
    )
    enrollment = result.scalar_one_or_none()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    enrollment.status = "Completed"
    enrollment.completed_date = datetime.utcnow()
    enrollment.final_score = final_score
    enrollment.progress_percentage = 100
    
    # Determine grade
    if final_score >= enrollment.passing_threshold:
        enrollment.grade = "Pass"
        if issue_certificate:
            enrollment.certificate_issued = True
            enrollment.certificate_issue_date = datetime.utcnow()
            enrollment.certificate_number = f"CERT-{enrollment.enrollment_code}"
    else:
        enrollment.grade = "Fail"
    
    # Update course stats
    course_result = await db.execute(
        select(Course).where(Course.id == enrollment.course_id)
    )
    course = course_result.scalar_one_or_none()
    if course:
        course.total_completions += 1
    
    await db.commit()
    await db.refresh(enrollment)
    return enrollment


# ============================================================================
# ASSESSMENTS
# ============================================================================

@router.post("/assessments")
async def create_assessment(
    organization_id: int,
    course_id: int,
    title: str,
    assessment_type: str,
    total_questions: int,
    passing_score: float,
    db: AsyncSession = Depends(get_db)
):
    """Create an assessment"""
    result = await db.execute(
        select(func.count(Assessment.id)).where(
            Assessment.organization_id == organization_id
        )
    )
    count = result.scalar() or 0
    assessment_code = f"ASS-{count + 1:04d}"
    
    assessment = Assessment(
        organization_id=organization_id,
        course_id=course_id,
        assessment_code=assessment_code,
        title=title,
        assessment_type=assessment_type,
        total_questions=total_questions,
        passing_score=passing_score,
        created_by="system"
    )
    
    db.add(assessment)
    await db.commit()
    await db.refresh(assessment)
    return assessment


@router.get("/assessments")
async def get_assessments(
    organization_id: int,
    course_id: Optional[int] = None,
    assessment_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all assessments"""
    query = select(Assessment).where(Assessment.organization_id == organization_id)
    
    if course_id:
        query = query.where(Assessment.course_id == course_id)
    if assessment_type:
        query = query.where(Assessment.assessment_type == assessment_type)
    
    result = await db.execute(query)
    return result.scalars().all()


# ============================================================================
# CERTIFICATIONS
# ============================================================================

@router.post("/certifications")
async def create_certification(
    organization_id: int,
    certification_name: str,
    issuing_organization: str,
    requires_exam: bool = False,
    db: AsyncSession = Depends(get_db)
):
    """Create a certification program"""
    result = await db.execute(
        select(func.count(Certification.id)).where(
            Certification.organization_id == organization_id
        )
    )
    count = result.scalar() or 0
    cert_code = f"CERT-{count + 1:04d}"
    
    certification = Certification(
        organization_id=organization_id,
        certification_code=cert_code,
        certification_name=certification_name,
        issuing_organization=issuing_organization,
        requires_exam=requires_exam,
        created_by="system"
    )
    
    db.add(certification)
    await db.commit()
    await db.refresh(certification)
    return certification


@router.get("/certifications")
async def get_certifications(
    organization_id: int,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all certifications"""
    query = select(Certification).where(
        Certification.organization_id == organization_id
    )
    
    if status:
        query = query.where(Certification.status == status)
    
    result = await db.execute(query)
    return result.scalars().all()


# ============================================================================
# LEARNING PATHS
# ============================================================================

@router.post("/learning-paths")
async def create_learning_path(
    organization_id: int,
    path_name: str,
    target_role: str,
    description: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Create a learning path"""
    result = await db.execute(
        select(func.count(LearningPath.id)).where(
            LearningPath.organization_id == organization_id
        )
    )
    count = result.scalar() or 0
    path_code = f"PATH-{count + 1:04d}"
    
    path = LearningPath(
        organization_id=organization_id,
        path_code=path_code,
        path_name=path_name,
        target_role=target_role,
        description=description,
        created_by="system"
    )
    
    db.add(path)
    await db.commit()
    await db.refresh(path)
    return path


@router.get("/learning-paths")
async def get_learning_paths(
    organization_id: int,
    target_role: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all learning paths"""
    query = select(LearningPath).where(LearningPath.organization_id == organization_id)
    
    if target_role:
        query = query.where(LearningPath.target_role == target_role)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/analytics/lms-dashboard")
async def get_lms_dashboard(
    organization_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get LMS dashboard analytics"""
    # Total courses
    courses_result = await db.execute(
        select(
            func.count(Course.id),
            func.avg(Course.completion_rate),
            func.avg(Course.average_rating)
        ).where(Course.organization_id == organization_id)
    )
    total_courses, avg_completion, avg_rating = courses_result.first()
    
    # Active enrollments
    enrollments_result = await db.execute(
        select(func.count(Enrollment.id)).where(
            and_(
                Enrollment.organization_id == organization_id,
                Enrollment.status.in_(["Enrolled", "In_Progress"])
            )
        )
    )
    active_enrollments = enrollments_result.scalar() or 0
    
    return {
        "total_courses": total_courses or 0,
        "avg_completion_rate": float(avg_completion) if avg_completion else 0,
        "avg_rating": float(avg_rating) if avg_rating else 0,
        "active_enrollments": active_enrollments
    }
