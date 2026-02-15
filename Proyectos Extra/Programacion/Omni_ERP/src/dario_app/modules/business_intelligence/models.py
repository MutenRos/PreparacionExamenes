"""
Business Intelligence & Analytics Module - Models
Comprehensive BI capabilities with dashboards, KPIs, reports, and data visualizations
"""
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from dario_app.database import Base


class Dashboard(Base):
    """Interactive dashboard with widgets and visualizations"""
    __tablename__ = "bi_dashboards"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    
    # Basic Info
    dashboard_code = Column(String(50), unique=True, nullable=False, index=True)  # DASH-001
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(100))  # Sales, Finance, Operations, HR, Custom
    
    # Configuration
    layout_config = Column(JSON)  # Grid layout, widget positions
    refresh_interval = Column(Integer)  # Seconds, auto-refresh interval
    time_range = Column(String(50))  # Last_7_Days, Last_30_Days, Last_Quarter, Custom
    filters = Column(JSON)  # Global dashboard filters
    
    # Sharing & Access
    visibility = Column(String(50), default="Private")  # Private, Organization, Public
    owner_id = Column(Integer)  # User who created it
    shared_with = Column(JSON)  # List of user/role IDs
    
    # Performance
    load_time_ms = Column(Integer)  # Average load time
    total_views = Column(Integer, default=0)
    last_viewed_at = Column(DateTime)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_favorite = Column(Boolean, default=False)
    is_default = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    
    # Relationships
    kpis = relationship("KPI", back_populates="dashboard", cascade="all, delete-orphan")
    visualizations = relationship("DataVisualization", back_populates="dashboard", cascade="all, delete-orphan")


class KPI(Base):
    """Key Performance Indicator with targets and thresholds"""
    __tablename__ = "bi_kpis"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    dashboard_id = Column(Integer, ForeignKey("bi_dashboards.id"))
    
    # Basic Info
    kpi_code = Column(String(50), unique=True, nullable=False, index=True)  # KPI-001
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(100))  # Revenue, Efficiency, Quality, Customer, Employee
    
    # Metric Configuration
    metric_type = Column(String(50))  # Count, Sum, Average, Percentage, Ratio
    data_source = Column(String(100))  # Table or view name
    calculation_formula = Column(Text)  # SQL or expression
    aggregation_level = Column(String(50))  # Daily, Weekly, Monthly, Quarterly, Yearly
    
    # Current Values
    current_value = Column(Float)
    previous_value = Column(Float)
    change_value = Column(Float)  # Absolute change
    change_percentage = Column(Float)  # Percentage change
    
    # Targets & Thresholds
    target_value = Column(Float)
    threshold_warning = Column(Float)  # Warning threshold
    threshold_critical = Column(Float)  # Critical threshold
    target_achievement = Column(Float)  # Percentage of target achieved
    
    # Display
    unit = Column(String(50))  # $, %, Units, Hours
    display_format = Column(String(50))  # Currency, Percentage, Number, Time
    icon = Column(String(100))  # Icon identifier
    color_scheme = Column(String(50))  # Green_Red, Blue_Orange, Custom
    
    # Status
    status = Column(String(50), default="On_Track")  # On_Track, Warning, Critical, Exceeded
    trend = Column(String(50))  # Improving, Declining, Stable
    is_active = Column(Boolean, default=True)
    
    # Update Info
    last_calculated_at = Column(DateTime)
    next_update_at = Column(DateTime)
    update_frequency = Column(String(50))  # Real_Time, Hourly, Daily
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    
    # Relationships
    dashboard = relationship("Dashboard", back_populates="kpis")


class Report(Base):
    """Scheduled or on-demand business reports"""
    __tablename__ = "bi_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    
    # Basic Info
    report_code = Column(String(50), unique=True, nullable=False, index=True)  # REP-001
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(100))  # Financial, Sales, Inventory, HR, Custom
    report_type = Column(String(50))  # Tabular, Summary, Detailed, Matrix, Chart
    
    # Configuration
    data_source = Column(String(100))  # Main table/view
    query_definition = Column(Text)  # SQL query or query builder config
    parameters = Column(JSON)  # Report parameters (date ranges, filters)
    columns = Column(JSON)  # Column definitions
    grouping = Column(JSON)  # Grouping configuration
    sorting = Column(JSON)  # Sorting rules
    
    # Formatting
    template_id = Column(String(100))  # Report template
    page_orientation = Column(String(50), default="Portrait")  # Portrait, Landscape
    page_size = Column(String(50), default="A4")  # A4, Letter, Legal
    header_footer = Column(JSON)  # Header/footer configuration
    
    # Scheduling
    is_scheduled = Column(Boolean, default=False)
    schedule_frequency = Column(String(50))  # Daily, Weekly, Monthly, Quarterly
    schedule_time = Column(String(50))  # Time of day
    schedule_days = Column(JSON)  # Days of week/month
    next_run_at = Column(DateTime)
    
    # Distribution
    delivery_method = Column(String(50))  # Email, Portal, File_Share, API
    recipients = Column(JSON)  # Email addresses or user IDs
    file_format = Column(String(50), default="PDF")  # PDF, Excel, CSV, HTML
    
    # Execution History
    last_run_at = Column(DateTime)
    last_run_duration_ms = Column(Integer)
    last_run_status = Column(String(50))  # Success, Failed, Timeout
    last_run_rows = Column(Integer)  # Number of rows returned
    total_runs = Column(Integer, default=0)
    
    # Status
    status = Column(String(50), default="Draft")  # Draft, Active, Paused, Archived
    is_active = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    
    # Relationships
    visualizations = relationship("DataVisualization", back_populates="report", cascade="all, delete-orphan")


class DataVisualization(Base):
    """Chart, graph, or visual element for dashboards/reports"""
    __tablename__ = "bi_visualizations"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    dashboard_id = Column(Integer, ForeignKey("bi_dashboards.id"), nullable=True)
    report_id = Column(Integer, ForeignKey("bi_reports.id"), nullable=True)
    
    # Basic Info
    visualization_code = Column(String(50), unique=True, nullable=False, index=True)  # VIZ-001
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Visualization Type
    chart_type = Column(String(50))  # Line, Bar, Pie, Donut, Area, Scatter, Heatmap, Gauge, Table, Map
    chart_library = Column(String(50))  # Chart.js, D3.js, Highcharts, Custom
    
    # Data Configuration
    data_source = Column(String(100))  # Table/view name
    query = Column(Text)  # Data query
    x_axis_field = Column(String(100))
    y_axis_field = Column(String(100))
    series_field = Column(String(100))  # For multi-series charts
    aggregation = Column(String(50))  # Sum, Average, Count, Max, Min
    
    # Display Configuration
    width = Column(Integer, default=400)  # Pixels
    height = Column(Integer, default=300)
    position_x = Column(Integer, default=0)  # Grid position
    position_y = Column(Integer, default=0)
    color_palette = Column(JSON)  # Array of colors
    
    # Chart Options
    show_legend = Column(Boolean, default=True)
    show_labels = Column(Boolean, default=True)
    show_grid = Column(Boolean, default=True)
    is_interactive = Column(Boolean, default=True)  # Enable hover, zoom, etc.
    animation_enabled = Column(Boolean, default=True)
    
    # Filters
    filters = Column(JSON)  # Visualization-specific filters
    drill_down_enabled = Column(Boolean, default=False)
    drill_down_config = Column(JSON)
    
    # Performance
    cache_duration = Column(Integer, default=300)  # Seconds
    last_cached_at = Column(DateTime)
    query_execution_time_ms = Column(Integer)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    
    # Relationships
    dashboard = relationship("Dashboard", back_populates="visualizations")
    report = relationship("Report", back_populates="visualizations")


class AnalyticsQuery(Base):
    """Saved analytics queries for reuse"""
    __tablename__ = "bi_analytics_queries"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    
    # Basic Info
    query_code = Column(String(50), unique=True, nullable=False, index=True)  # QRY-001
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(100))  # Sales, Finance, Operations, Custom
    
    # Query Definition
    query_type = Column(String(50))  # SQL, NoSQL, API, Custom
    query_text = Column(Text, nullable=False)
    parameters = Column(JSON)  # Query parameters
    
    # Data Source
    data_source = Column(String(100))  # Database, API, File, Custom
    connection_string = Column(Text)  # Encrypted connection info
    schema_name = Column(String(100))
    
    # Output Configuration
    output_format = Column(String(50))  # JSON, CSV, Table
    column_mappings = Column(JSON)  # Column name mappings
    transformations = Column(JSON)  # Data transformations
    
    # Performance
    timeout_seconds = Column(Integer, default=30)
    max_rows = Column(Integer, default=10000)
    use_cache = Column(Boolean, default=True)
    cache_duration = Column(Integer, default=300)  # Seconds
    
    # Usage Stats
    total_executions = Column(Integer, default=0)
    last_executed_at = Column(DateTime)
    avg_execution_time_ms = Column(Integer)
    last_row_count = Column(Integer)
    
    # Sharing
    is_public = Column(Boolean, default=False)
    shared_with = Column(JSON)  # User/role IDs
    
    # Status
    is_active = Column(Boolean, default=True)
    is_validated = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))


class MetricDefinition(Base):
    """Standardized metric definitions for consistent calculations"""
    __tablename__ = "bi_metric_definitions"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    
    # Basic Info
    metric_code = Column(String(50), unique=True, nullable=False, index=True)  # MET-001
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(100))  # Financial, Operational, Customer, Employee
    
    # Calculation
    calculation_formula = Column(Text, nullable=False)  # Standard formula
    calculation_method = Column(String(50))  # Sum, Average, Count, Ratio, Custom
    data_source = Column(String(100))
    required_fields = Column(JSON)  # Fields needed for calculation
    
    # Business Rules
    business_definition = Column(Text)  # Plain language definition
    calculation_frequency = Column(String(50))  # Real_Time, Daily, Weekly, Monthly
    calculation_level = Column(String(50))  # Transaction, Daily, Monthly, Quarterly
    
    # Industry Standards
    industry_standard = Column(String(100))  # GAAP, IFRS, Custom
    industry_benchmark = Column(Float)  # Industry average
    best_in_class_value = Column(Float)
    
    # Display
    unit = Column(String(50))  # $, %, Units, Hours
    display_format = Column(String(50))
    decimal_places = Column(Integer, default=2)
    
    # Targets
    default_target = Column(Float)
    direction = Column(String(50))  # Higher_Better, Lower_Better, Target_Range
    
    # Usage
    used_in_dashboards = Column(Integer, default=0)  # Count
    used_in_reports = Column(Integer, default=0)
    used_in_kpis = Column(Integer, default=0)
    
    # Governance
    owner_id = Column(Integer)  # Metric owner
    approval_status = Column(String(50), default="Draft")  # Draft, Approved, Deprecated
    approved_by = Column(String(100))
    approved_at = Column(DateTime)
    version = Column(String(50), default="1.0")
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
