"""
Resource Scheduling Optimization Module - Models
Advanced scheduling with optimization algorithms for resources
"""
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from dario_app.database import Base


class OptimizationJob(Base):
    """Optimization job that runs scheduling algorithms"""
    __tablename__ = "rso_optimization_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    
    # Basic Info
    job_code = Column(String(50), unique=True, nullable=False, index=True)  # OPT-001
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Optimization Scope
    optimization_type = Column(String(50))  # Route, Resource, Schedule, Capacity
    scope = Column(String(50))  # Daily, Weekly, Monthly, Real_Time
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    
    # Constraints
    constraints = Column(JSON)  # Skills, availability, geography, cost
    hard_constraints = Column(JSON)  # Must be satisfied
    soft_constraints = Column(JSON)  # Preferably satisfied
    
    # Objectives
    primary_objective = Column(String(50))  # Minimize_Travel, Maximize_Utilization, Minimize_Cost
    secondary_objectives = Column(JSON)  # Additional objectives with weights
    optimization_weights = Column(JSON)  # Weight for each objective
    
    # Algorithm Configuration
    algorithm = Column(String(50))  # Genetic, Simulated_Annealing, Branch_And_Bound, ML_Based
    max_runtime_seconds = Column(Integer, default=300)
    max_iterations = Column(Integer, default=1000)
    convergence_threshold = Column(Float, default=0.01)
    
    # Execution
    status = Column(String(50), default="Pending")  # Pending, Running, Completed, Failed, Cancelled
    priority = Column(Integer, default=5)  # 1-10, higher = more urgent
    scheduled_start = Column(DateTime)
    actual_start = Column(DateTime)
    actual_end = Column(DateTime)
    
    # Results
    solution_quality = Column(Float)  # 0-100%, how close to optimal
    improvement_percentage = Column(Float)  # Improvement over current schedule
    iterations_completed = Column(Integer)
    runtime_seconds = Column(Integer)
    
    # Resources
    resources_evaluated = Column(Integer)  # Number of resources considered
    schedules_generated = Column(Integer)  # Number of schedule variations
    best_solution_id = Column(Integer)  # ID of best solution found
    
    # Status Messages
    progress_percentage = Column(Float, default=0)
    current_phase = Column(String(100))  # Initializing, Optimizing, Validating, Finalizing
    error_message = Column(Text)
    warnings = Column(JSON)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    
    # Relationships
    optimizations = relationship("ScheduleOptimization", back_populates="job", cascade="all, delete-orphan")


class ScheduleOptimization(Base):
    """Optimized schedule solution"""
    __tablename__ = "rso_schedule_optimizations"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    job_id = Column(Integer, ForeignKey("rso_optimization_jobs.id"), nullable=False)
    
    # Basic Info
    schedule_code = Column(String(50), unique=True, nullable=False, index=True)  # SCH-001
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Schedule Period
    schedule_date = Column(DateTime, nullable=False, index=True)
    shift_start = Column(DateTime)
    shift_end = Column(DateTime)
    total_duration_hours = Column(Float)
    
    # Resource Assignment
    resource_id = Column(Integer)  # Assigned resource (technician, vehicle, etc.)
    resource_type = Column(String(50))  # Technician, Equipment, Vehicle, Room
    resource_name = Column(String(200))
    
    # Task Assignment
    assigned_tasks = Column(JSON)  # List of task IDs and details
    total_tasks = Column(Integer, default=0)
    completed_tasks = Column(Integer, default=0)
    
    # Route/Sequence
    task_sequence = Column(JSON)  # Ordered list of tasks
    route_waypoints = Column(JSON)  # Geographic waypoints
    total_travel_distance_km = Column(Float)
    total_travel_time_minutes = Column(Float)
    
    # Utilization
    productive_time_hours = Column(Float)  # Time spent on tasks
    travel_time_hours = Column(Float)
    idle_time_hours = Column(Float)
    utilization_percentage = Column(Float)  # (productive / total) * 100
    
    # Performance Scores
    efficiency_score = Column(Float)  # 0-100
    quality_score = Column(Float)
    customer_satisfaction_score = Column(Float)
    cost_score = Column(Float)
    overall_score = Column(Float)  # Weighted average
    
    # Constraints Satisfaction
    hard_constraints_met = Column(Boolean, default=True)
    soft_constraints_met = Column(Integer)  # Count of soft constraints satisfied
    constraint_violations = Column(JSON)  # List of any violations
    
    # Comparison with Previous
    previous_schedule_id = Column(Integer)
    improvement_percentage = Column(Float)
    cost_savings = Column(Float)
    time_savings_hours = Column(Float)
    
    # Status
    status = Column(String(50), default="Draft")  # Draft, Proposed, Approved, Active, Completed, Cancelled
    is_optimal = Column(Boolean, default=False)
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime)
    
    # Acceptance
    accepted_by = Column(String(100))
    accepted_at = Column(DateTime)
    rejection_reason = Column(Text)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    
    # Relationships
    job = relationship("OptimizationJob", back_populates="optimizations")


class ResourceRequirement(Base):
    """Resource requirements for tasks/projects"""
    __tablename__ = "rso_resource_requirements"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    
    # Basic Info
    requirement_code = Column(String(50), unique=True, nullable=False, index=True)  # REQ-001
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Source
    source_type = Column(String(50))  # Work_Order, Project, Event, Maintenance
    source_id = Column(Integer)  # ID of the source entity
    source_reference = Column(String(100))
    
    # Resource Needs
    resource_type = Column(String(50))  # Technician, Equipment, Vehicle, Material
    required_quantity = Column(Integer, default=1)
    required_skills = Column(JSON)  # List of required skills
    skill_level_required = Column(String(50))  # Beginner, Intermediate, Advanced, Expert
    
    # Timing
    required_start = Column(DateTime, nullable=False)
    required_end = Column(DateTime, nullable=False)
    duration_hours = Column(Float)
    flexibility_hours = Column(Float)  # How much timing can flex
    
    # Priority
    priority = Column(String(50))  # Critical, High, Medium, Low
    priority_score = Column(Integer)  # Numeric priority for optimization
    is_urgent = Column(Boolean, default=False)
    
    # Preferences
    preferred_resources = Column(JSON)  # Preferred resource IDs
    excluded_resources = Column(JSON)  # Resources to avoid
    preferred_time_slots = Column(JSON)  # Preferred time windows
    
    # Geographic
    location_latitude = Column(Float)
    location_longitude = Column(Float)
    location_address = Column(Text)
    travel_distance_from_base_km = Column(Float)
    
    # Constraints
    must_schedule_together = Column(JSON)  # Requirements that must be scheduled together
    cannot_schedule_with = Column(JSON)  # Requirements that can't overlap
    predecessor_requirements = Column(JSON)  # Requirements that must complete first
    
    # Assignment
    assigned_resource_id = Column(Integer)
    assigned_schedule_id = Column(Integer)
    scheduled_start = Column(DateTime)
    scheduled_end = Column(DateTime)
    assignment_status = Column(String(50), default="Unassigned")  # Unassigned, Assigned, In_Progress, Completed
    
    # Status
    status = Column(String(50), default="Open")  # Open, Scheduled, In_Progress, Completed, Cancelled
    fulfillment_percentage = Column(Float, default=0)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))


class SchedulingParameter(Base):
    """Configuration parameters for scheduling algorithms"""
    __tablename__ = "rso_scheduling_parameters"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    
    # Basic Info
    parameter_code = Column(String(50), unique=True, nullable=False, index=True)  # PAR-001
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(100))  # Optimization, Constraint, Cost, Performance
    
    # Parameter Definition
    parameter_type = Column(String(50))  # Weight, Threshold, Limit, Cost, Time
    data_type = Column(String(50))  # Integer, Float, Boolean, String, JSON
    parameter_value = Column(Text)  # Stored as string, converted based on data_type
    default_value = Column(Text)
    unit = Column(String(50))  # $, %, hours, km
    
    # Constraints
    min_value = Column(Float)
    max_value = Column(Float)
    allowed_values = Column(JSON)  # For enum-type parameters
    
    # Usage
    applies_to = Column(String(50))  # Global, Resource_Type, Task_Type, Geographic
    scope = Column(JSON)  # Specific entities this applies to
    
    # Business Rules
    business_rule = Column(Text)  # Plain language rule
    formula = Column(Text)  # Mathematical formula if applicable
    dependencies = Column(JSON)  # Other parameters this depends on
    
    # Weighting (for optimization objectives)
    weight = Column(Float, default=1.0)  # Importance weight
    normalized_weight = Column(Float)  # Weight normalized to 0-1
    
    # Status
    is_active = Column(Boolean, default=True)
    is_editable = Column(Boolean, default=True)
    requires_approval = Column(Boolean, default=False)
    
    # Versioning
    version = Column(String(50), default="1.0")
    previous_value = Column(Text)
    changed_at = Column(DateTime)
    changed_by = Column(String(100))
    change_reason = Column(Text)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))


class OptimizationResult(Base):
    """Results and analytics from optimization runs"""
    __tablename__ = "rso_optimization_results"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    job_id = Column(Integer, ForeignKey("rso_optimization_jobs.id"))
    
    # Basic Info
    result_code = Column(String(50), unique=True, nullable=False, index=True)  # RES-001
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Solution Quality
    solution_rank = Column(Integer)  # 1 = best solution
    objective_value = Column(Float)  # Value of optimization objective
    is_feasible = Column(Boolean)  # Does it satisfy all hard constraints?
    is_optimal = Column(Boolean)  # Is this provably optimal?
    optimality_gap = Column(Float)  # Distance from theoretical optimum (%)
    
    # Performance Metrics
    total_cost = Column(Float)
    total_travel_distance_km = Column(Float)
    total_travel_time_hours = Column(Float)
    total_idle_time_hours = Column(Float)
    average_utilization_percentage = Column(Float)
    
    # Resource Metrics
    resources_used = Column(Integer)
    resources_available = Column(Integer)
    resource_utilization = Column(Float)  # Percentage of available resources used
    overtime_hours = Column(Float)
    
    # Task Metrics
    tasks_scheduled = Column(Integer)
    tasks_unscheduled = Column(Integer)
    scheduling_success_rate = Column(Float)  # Percentage of tasks scheduled
    average_task_delay_hours = Column(Float)
    
    # Constraint Satisfaction
    hard_constraints_violated = Column(Integer)
    soft_constraints_violated = Column(Integer)
    constraint_violation_score = Column(Float)
    violation_details = Column(JSON)
    
    # Comparison
    baseline_cost = Column(Float)  # Cost without optimization
    cost_savings = Column(Float)
    cost_savings_percentage = Column(Float)
    improvement_over_baseline = Column(Float)  # Overall improvement (%)
    
    # Detailed Results
    resource_assignments = Column(JSON)  # Detailed assignment data
    task_schedule = Column(JSON)  # Detailed task schedule
    route_details = Column(JSON)  # Route information
    
    # Algorithm Info
    algorithm_used = Column(String(50))
    iterations_required = Column(Integer)
    computation_time_seconds = Column(Float)
    convergence_achieved = Column(Boolean)
    
    # Sensitivity Analysis
    sensitivity_to_demand = Column(Float)  # How sensitive to demand changes
    sensitivity_to_capacity = Column(Float)  # How sensitive to capacity changes
    robustness_score = Column(Float)  # How robust to disruptions
    
    # Recommendations
    recommendations = Column(JSON)  # Suggested improvements
    alternative_scenarios = Column(JSON)  # What-if scenarios
    risk_factors = Column(JSON)  # Potential risks
    
    # Status
    status = Column(String(50), default="Draft")  # Draft, Validated, Approved, Implemented
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
