"""
Learning Management System Module - Models
Courses, lessons, enrollments, assessments, certifications, and learning paths
"""
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from dario_app.database import Base


class Course(Base):
    """Training course or learning program"""
    __tablename__ = "lms_courses"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    
    # Basic Info
    course_code = Column(String(50), unique=True, nullable=False, index=True)  # CRS-001
    title = Column(String(300), nullable=False)
    description = Column(Text)
    short_description = Column(String(500))
    
    # Classification
    category = Column(String(100))  # Technical, Leadership, Compliance, Soft_Skills, Safety
    subcategory = Column(String(100))
    difficulty_level = Column(String(50))  # Beginner, Intermediate, Advanced, Expert
    language = Column(String(50), default="en")
    
    # Content
    learning_objectives = Column(JSON)  # List of learning objectives
    prerequisites = Column(JSON)  # Required prior knowledge/courses
    duration_hours = Column(Float)  # Total course duration
    total_lessons = Column(Integer, default=0)
    
    # Format
    delivery_method = Column(String(50))  # Online, In_Person, Hybrid, Self_Paced
    format_type = Column(String(50))  # Video, Interactive, Reading, Workshop, Webinar
    has_practical_exercises = Column(Boolean, default=False)
    has_final_exam = Column(Boolean, default=False)
    
    # Instructor
    instructor_name = Column(String(200))
    instructor_id = Column(Integer)
    instructor_bio = Column(Text)
    instructor_credentials = Column(String(500))
    
    # Enrollment
    max_enrollments = Column(Integer)  # Capacity limit
    current_enrollments = Column(Integer, default=0)
    enrollment_status = Column(String(50), default="Open")  # Open, Full, Closed
    requires_approval = Column(Boolean, default=False)
    
    # Scheduling
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    enrollment_deadline = Column(DateTime)
    is_self_paced = Column(Boolean, default=False)
    
    # Certification
    provides_certificate = Column(Boolean, default=False)
    certificate_template_id = Column(Integer)
    certificate_validity_months = Column(Integer)  # Certificate expiry
    continuing_education_credits = Column(Float)  # CEU/CPE credits
    
    # Pricing
    is_free = Column(Boolean, default=True)
    price = Column(Float, default=0)
    currency = Column(String(10), default="USD")
    
    # Performance Metrics
    total_completions = Column(Integer, default=0)
    average_rating = Column(Float)  # 0-5 stars
    total_reviews = Column(Integer, default=0)
    average_completion_time_hours = Column(Float)
    completion_rate = Column(Float)  # Percentage who complete
    
    # Content URLs
    thumbnail_url = Column(String(500))
    video_url = Column(String(500))
    materials_url = Column(String(500))
    
    # Status
    status = Column(String(50), default="Draft")  # Draft, Published, Archived
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    is_mandatory = Column(Boolean, default=False)  # Required training
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    
    # Relationships
    lessons = relationship("Lesson", back_populates="course", cascade="all, delete-orphan")
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="course")


class Lesson(Base):
    """Individual lesson or module within a course"""
    __tablename__ = "lms_lessons"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("lms_courses.id"), nullable=False)
    
    # Basic Info
    lesson_code = Column(String(50), unique=True, nullable=False, index=True)  # LES-001
    title = Column(String(300), nullable=False)
    description = Column(Text)
    
    # Structure
    section_number = Column(Integer)  # Chapter/section
    lesson_number = Column(Integer)  # Order within section
    sequence_order = Column(Integer)  # Overall sequence
    
    # Content
    content_type = Column(String(50))  # Video, Text, Interactive, Quiz, Assignment, Discussion
    content_text = Column(Text)  # Text content or HTML
    video_url = Column(String(500))
    duration_minutes = Column(Integer)
    
    # Resources
    attachments = Column(JSON)  # File attachments
    external_links = Column(JSON)  # External resources
    downloadable_materials = Column(JSON)
    
    # Learning Objectives
    objectives = Column(JSON)  # Lesson-specific objectives
    key_concepts = Column(JSON)  # Main concepts covered
    
    # Requirements
    is_mandatory = Column(Boolean, default=True)
    requires_completion = Column(Boolean, default=True)  # Must complete to proceed
    minimum_time_minutes = Column(Integer)  # Minimum viewing time
    
    # Assessment
    has_quiz = Column(Boolean, default=False)
    quiz_passing_score = Column(Float)  # Minimum % to pass
    max_attempts = Column(Integer, default=3)
    
    # Progress Tracking
    total_views = Column(Integer, default=0)
    average_completion_time = Column(Float)  # Average time to complete
    completion_rate = Column(Float)  # % of enrolled who complete
    
    # Status
    is_active = Column(Boolean, default=True)
    is_published = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    
    # Relationships
    course = relationship("Course", back_populates="lessons")


class Enrollment(Base):
    """Student enrollment in a course"""
    __tablename__ = "lms_enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("lms_courses.id"), nullable=False)
    
    # Student Info
    student_id = Column(Integer, nullable=False, index=True)  # User ID
    student_name = Column(String(200))
    student_email = Column(String(200))
    student_department = Column(String(100))
    
    # Enrollment Details
    enrollment_code = Column(String(50), unique=True, nullable=False, index=True)  # ENR-001
    enrollment_date = Column(DateTime, default=datetime.utcnow)
    enrollment_method = Column(String(50))  # Self_Enrollment, Manager_Assignment, Auto_Assignment
    enrollment_reason = Column(String(200))  # Why enrolled (mandatory, development, etc.)
    
    # Access
    access_granted_date = Column(DateTime)
    access_expires_date = Column(DateTime)
    access_status = Column(String(50), default="Active")  # Active, Suspended, Expired, Revoked
    
    # Progress
    status = Column(String(50), default="Enrolled")  # Enrolled, In_Progress, Completed, Failed, Dropped
    progress_percentage = Column(Float, default=0)  # 0-100%
    lessons_completed = Column(Integer, default=0)
    lessons_total = Column(Integer)
    
    # Time Tracking
    started_date = Column(DateTime)
    last_accessed_date = Column(DateTime)
    completed_date = Column(DateTime)
    total_time_spent_minutes = Column(Integer, default=0)
    
    # Performance
    current_score = Column(Float)  # Current overall score
    final_score = Column(Float)  # Final grade
    grade = Column(String(10))  # A, B, C, D, F or Pass/Fail
    passing_threshold = Column(Float, default=70.0)
    
    # Completion Requirements
    completion_deadline = Column(DateTime)
    is_overdue = Column(Boolean, default=False)
    extension_requested = Column(Boolean, default=False)
    extension_granted_until = Column(DateTime)
    
    # Certification
    certificate_issued = Column(Boolean, default=False)
    certificate_number = Column(String(100))
    certificate_issue_date = Column(DateTime)
    certificate_expiry_date = Column(DateTime)
    certificate_file_path = Column(String(500))
    
    # Feedback
    student_rating = Column(Integer)  # 1-5 stars
    student_feedback = Column(Text)
    feedback_date = Column(DateTime)
    
    # Manager Review
    manager_id = Column(Integer)
    manager_approved = Column(Boolean)
    manager_comments = Column(Text)
    
    # Payment (if paid course)
    payment_required = Column(Boolean, default=False)
    payment_status = Column(String(50))  # Pending, Completed, Failed
    payment_amount = Column(Float)
    payment_date = Column(DateTime)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    
    # Relationships
    course = relationship("Course", back_populates="enrollments")


class Assessment(Base):
    """Quiz, test, or assessment for a course"""
    __tablename__ = "lms_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("lms_courses.id"))
    lesson_id = Column(Integer)  # Optional - assessment for specific lesson
    
    # Basic Info
    assessment_code = Column(String(50), unique=True, nullable=False, index=True)  # ASS-001
    title = Column(String(300), nullable=False)
    description = Column(Text)
    
    # Type
    assessment_type = Column(String(50))  # Quiz, Test, Exam, Assignment, Project, Survey
    format_type = Column(String(50))  # Multiple_Choice, True_False, Essay, Practical, Mixed
    
    # Configuration
    total_questions = Column(Integer)
    total_points = Column(Float)
    passing_score = Column(Float)  # Minimum score to pass
    time_limit_minutes = Column(Integer)  # Time limit
    
    # Attempts
    max_attempts = Column(Integer, default=3)
    cooldown_hours = Column(Integer)  # Hours between attempts
    allow_review = Column(Boolean, default=True)  # Can review after submission
    show_correct_answers = Column(Boolean, default=False)
    
    # Questions
    questions = Column(JSON)  # Question bank
    randomize_questions = Column(Boolean, default=False)
    randomize_options = Column(Boolean, default=False)
    
    # Scheduling
    available_from = Column(DateTime)
    available_until = Column(DateTime)
    is_available = Column(Boolean, default=True)
    
    # Proctoring
    requires_proctor = Column(Boolean, default=False)
    proctoring_method = Column(String(50))  # In_Person, Online, AI_Proctored
    webcam_required = Column(Boolean, default=False)
    screen_recording_required = Column(Boolean, default=False)
    
    # Grading
    auto_graded = Column(Boolean, default=True)
    manual_review_required = Column(Boolean, default=False)
    graded_by = Column(String(100))
    grading_rubric = Column(JSON)
    
    # Statistics
    total_attempts = Column(Integer, default=0)
    total_completions = Column(Integer, default=0)
    average_score = Column(Float)
    pass_rate = Column(Float)  # % who pass
    average_completion_time_minutes = Column(Float)
    
    # Status
    status = Column(String(50), default="Draft")  # Draft, Active, Archived
    is_active = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    
    # Relationships
    course = relationship("Course", back_populates="assessments")


class Certification(Base):
    """Professional certification or credential"""
    __tablename__ = "lms_certifications"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    
    # Basic Info
    certification_code = Column(String(50), unique=True, nullable=False, index=True)  # CERT-001
    certification_name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Issuing Organization
    issuing_organization = Column(String(200))  # Internal or external
    accreditation_body = Column(String(200))  # Accrediting authority
    credential_id_format = Column(String(100))  # Format for credential IDs
    
    # Requirements
    required_courses = Column(JSON)  # List of course IDs
    required_experience_years = Column(Float)
    required_credits = Column(Float)  # CEU/CPE credits needed
    prerequisite_certifications = Column(JSON)  # Required prior certs
    
    # Assessment
    requires_exam = Column(Boolean, default=False)
    exam_passing_score = Column(Float)
    exam_retake_allowed = Column(Boolean, default=True)
    max_exam_attempts = Column(Integer)
    
    # Validity
    validity_period_months = Column(Integer)  # How long cert is valid
    renewal_required = Column(Boolean, default=False)
    renewal_credits_required = Column(Float)
    
    # Maintenance
    continuing_education_required = Column(Boolean, default=False)
    annual_credits_required = Column(Float)
    recertification_exam_required = Column(Boolean, default=False)
    
    # Benefits
    salary_impact_percentage = Column(Float)  # Typical salary increase
    career_level_unlocked = Column(String(100))
    job_roles_qualified = Column(JSON)  # Job roles this qualifies for
    
    # Statistics
    total_certified = Column(Integer, default=0)
    total_in_progress = Column(Integer, default=0)
    average_time_to_certify_months = Column(Float)
    pass_rate = Column(Float)
    
    # Status
    status = Column(String(50), default="Active")  # Active, Suspended, Retired
    is_active = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))


class LearningPath(Base):
    """Structured learning journey with multiple courses"""
    __tablename__ = "lms_learning_paths"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    
    # Basic Info
    path_code = Column(String(50), unique=True, nullable=False, index=True)  # PATH-001
    path_name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Target Audience
    target_role = Column(String(100))  # Job role this path is for
    target_level = Column(String(50))  # Entry, Mid, Senior, Executive
    target_department = Column(String(100))
    
    # Structure
    total_courses = Column(Integer, default=0)
    course_sequence = Column(JSON)  # Ordered list of course IDs
    estimated_duration_hours = Column(Float)
    
    # Requirements
    prerequisites = Column(JSON)  # Required knowledge/certs
    is_sequential = Column(Boolean, default=True)  # Must complete in order
    minimum_completion_percentage = Column(Float, default=100.0)
    
    # Certification
    awards_certification = Column(Boolean, default=False)
    certification_id = Column(Integer)
    
    # Enrollment
    total_enrolled = Column(Integer, default=0)
    total_completed = Column(Integer, default=0)
    completion_rate = Column(Float)
    average_completion_time_days = Column(Float)
    
    # Status
    status = Column(String(50), default="Active")  # Active, Draft, Archived
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
