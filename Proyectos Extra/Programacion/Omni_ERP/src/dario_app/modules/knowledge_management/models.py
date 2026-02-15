"""
Knowledge Management Module - Models
Knowledge base articles, categories, versions, ratings, and AI search
"""
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from dario_app.database import Base


class KnowledgeArticle(Base):
    """Knowledge base article"""
    __tablename__ = "km_knowledge_articles"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("km_article_categories.id"))
    
    # Basic Info
    article_code = Column(String(50), unique=True, nullable=False, index=True)  # ART-001
    title = Column(String(500), nullable=False)
    subtitle = Column(String(500))
    summary = Column(Text)  # Brief summary
    
    # Content
    content = Column(Text, nullable=False)  # Main article content (HTML/Markdown)
    content_format = Column(String(50), default="HTML")  # HTML, Markdown, Plain_Text
    content_length_words = Column(Integer)
    
    # Metadata
    keywords = Column(JSON)  # List of keywords for search
    tags = Column(JSON)  # User-defined tags
    related_articles = Column(JSON)  # List of related article IDs
    
    # Type & Purpose
    article_type = Column(String(50))  # How_To, Troubleshooting, FAQ, Reference, Policy, Best_Practice
    purpose = Column(String(50))  # Customer_Facing, Internal, Both
    topic = Column(String(200))  # Main topic/subject
    
    # Audience
    target_audience = Column(JSON)  # Roles/departments this is for
    skill_level = Column(String(50))  # Beginner, Intermediate, Advanced, Expert
    language = Column(String(50), default="en")
    
    # Authoring
    author_id = Column(Integer)  # Original author
    author_name = Column(String(200))
    contributors = Column(JSON)  # List of contributor IDs/names
    
    # Ownership
    owner_id = Column(Integer)  # Content owner
    owner_department = Column(String(100))
    subject_matter_expert_id = Column(Integer)  # SME responsible
    
    # Versioning
    version = Column(String(50), default="1.0")
    version_number = Column(Integer, default=1)
    is_latest_version = Column(Boolean, default=True)
    previous_version_id = Column(Integer)  # Link to previous version
    
    # Review & Approval
    status = Column(String(50), default="Draft")  # Draft, Under_Review, Approved, Published, Archived, Retired
    review_status = Column(String(50))  # Pending_Review, Approved, Changes_Requested, Rejected
    reviewed_by = Column(String(200))
    reviewed_at = Column(DateTime)
    review_notes = Column(Text)
    
    # Publishing
    published_date = Column(DateTime)
    published_by = Column(String(200))
    is_published = Column(Boolean, default=False)
    publication_channels = Column(JSON)  # Where it's published (Web, Mobile, PDF)
    
    # Expiration & Maintenance
    expiration_date = Column(DateTime)
    is_expired = Column(Boolean, default=False)
    requires_periodic_review = Column(Boolean, default=True)
    review_frequency_days = Column(Integer, default=180)  # Review every 6 months
    last_reviewed_date = Column(DateTime)
    next_review_date = Column(DateTime)
    
    # Quality Metrics
    accuracy_score = Column(Float)  # 0-100%, content accuracy
    completeness_score = Column(Float)  # 0-100%, how complete
    clarity_score = Column(Float)  # 0-100%, how clear
    overall_quality_score = Column(Float)  # Average of above
    
    # User Engagement
    view_count = Column(Integer, default=0)
    unique_viewers = Column(Integer, default=0)
    average_time_on_page_seconds = Column(Integer)
    bounce_rate = Column(Float)  # % who leave immediately
    
    # Helpfulness
    helpful_count = Column(Integer, default=0)  # "Was this helpful? Yes" count
    not_helpful_count = Column(Integer, default=0)  # "No" count
    helpfulness_percentage = Column(Float)  # % who found it helpful
    
    # Ratings & Feedback
    average_rating = Column(Float)  # 0-5 stars
    total_ratings = Column(Integer, default=0)
    total_comments = Column(Integer, default=0)
    
    # Search & Discovery
    search_ranking_score = Column(Float)  # For search algorithm
    featured_article = Column(Boolean, default=False)
    trending = Column(Boolean, default=False)
    popular = Column(Boolean, default=False)  # High view count
    
    # Attachments & Media
    attachments = Column(JSON)  # File attachments
    images = Column(JSON)  # Image URLs
    videos = Column(JSON)  # Video URLs
    external_links = Column(JSON)  # External references
    
    # AI Features
    ai_generated_summary = Column(Text)  # AI-generated summary
    ai_keywords = Column(JSON)  # AI-extracted keywords
    ai_sentiment = Column(String(50))  # Positive, Neutral, Negative
    ai_complexity_score = Column(Float)  # Readability/complexity
    
    # Analytics
    conversion_rate = Column(Float)  # % who take desired action
    support_ticket_reduction = Column(Float)  # % reduction in tickets
    estimated_time_saved_minutes = Column(Float)  # Time saved per use
    
    # Compliance
    contains_sensitive_data = Column(Boolean, default=False)
    data_classification = Column(String(50))  # Public, Internal, Confidential, Restricted
    requires_authentication = Column(Boolean, default=False)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_pinned = Column(Boolean, default=False)  # Pin to top of category
    is_template = Column(Boolean, default=False)  # Can be used as template
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    
    # Relationships
    category = relationship("ArticleCategory", back_populates="articles")
    versions = relationship("ArticleVersion", back_populates="article", cascade="all, delete-orphan")
    ratings = relationship("ArticleRating", back_populates="article", cascade="all, delete-orphan")


class ArticleCategory(Base):
    """Category/folder for organizing knowledge articles"""
    __tablename__ = "km_article_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    parent_category_id = Column(Integer)  # For nested categories
    
    # Basic Info
    category_code = Column(String(50), unique=True, nullable=False, index=True)  # CAT-001
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Hierarchy
    level = Column(Integer, default=1)  # Depth in hierarchy
    path = Column(String(500))  # Full path (e.g., "Tech/Hardware/Printers")
    sequence_order = Column(Integer)  # Display order
    
    # Icon & Display
    icon = Column(String(100))  # Icon identifier
    color = Column(String(50))  # Color code
    thumbnail_url = Column(String(500))
    
    # Content
    total_articles = Column(Integer, default=0)
    published_articles = Column(Integer, default=0)
    draft_articles = Column(Integer, default=0)
    
    # Access Control
    visibility = Column(String(50), default="Public")  # Public, Internal, Restricted
    allowed_roles = Column(JSON)  # Roles that can access
    allowed_departments = Column(JSON)
    
    # Featured
    is_featured = Column(Boolean, default=False)
    featured_order = Column(Integer)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    
    # Relationships
    articles = relationship("KnowledgeArticle", back_populates="category")


class ArticleVersion(Base):
    """Version history of knowledge articles"""
    __tablename__ = "km_article_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    article_id = Column(Integer, ForeignKey("km_knowledge_articles.id"), nullable=False)
    
    # Version Info
    version_code = Column(String(50), unique=True, nullable=False, index=True)  # VER-001
    version = Column(String(50), nullable=False)  # 1.0, 1.1, 2.0
    version_number = Column(Integer, nullable=False)
    
    # Content Snapshot
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text)
    
    # Change Information
    change_type = Column(String(50))  # Major, Minor, Patch, Correction
    change_description = Column(Text)  # What changed
    change_reason = Column(Text)  # Why it changed
    changes_list = Column(JSON)  # Detailed list of changes
    
    # Comparison
    added_content = Column(Text)  # New content added
    removed_content = Column(Text)  # Content removed
    modified_sections = Column(JSON)  # Sections that changed
    
    # Authoring
    author_id = Column(Integer)
    author_name = Column(String(200))
    approved_by = Column(String(200))
    approved_at = Column(DateTime)
    
    # Snapshot Data
    keywords = Column(JSON)
    tags = Column(JSON)
    article_type = Column(String(50))
    status = Column(String(50))
    
    # Statistics (at time of version)
    view_count_at_version = Column(Integer)
    rating_at_version = Column(Float)
    
    # Rollback
    can_rollback = Column(Boolean, default=True)
    rolled_back = Column(Boolean, default=False)
    rollback_date = Column(DateTime)
    rollback_reason = Column(Text)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    
    # Relationships
    article = relationship("KnowledgeArticle", back_populates="versions")


class ArticleRating(Base):
    """User ratings and reviews for articles"""
    __tablename__ = "km_article_ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    article_id = Column(Integer, ForeignKey("km_knowledge_articles.id"), nullable=False)
    
    # Rating Info
    rating_code = Column(String(50), unique=True, nullable=False, index=True)  # RAT-001
    
    # User
    user_id = Column(Integer, nullable=False, index=True)
    user_name = Column(String(200))
    user_email = Column(String(200))
    user_role = Column(String(100))
    
    # Rating
    rating_value = Column(Integer, nullable=False)  # 1-5 stars
    was_helpful = Column(Boolean)  # Yes/No helpful button
    
    # Feedback
    comment = Column(Text)  # Written feedback
    feedback_category = Column(String(50))  # Accuracy, Clarity, Completeness, Timeliness
    suggestions = Column(Text)  # Improvement suggestions
    
    # Issues Reported
    reported_issue = Column(Boolean, default=False)
    issue_type = Column(String(50))  # Outdated, Inaccurate, Incomplete, Unclear, Other
    issue_description = Column(Text)
    
    # Context
    use_case = Column(Text)  # How they used the article
    did_solve_problem = Column(Boolean)  # Did it solve their issue?
    time_to_solution_minutes = Column(Integer)
    
    # Sentiment Analysis
    sentiment = Column(String(50))  # Positive, Neutral, Negative
    sentiment_score = Column(Float)  # -1 to 1
    
    # Response
    author_response = Column(Text)
    responded_by = Column(String(200))
    responded_at = Column(DateTime)
    
    # Status
    is_verified = Column(Boolean, default=False)  # Verified as helpful by author
    is_featured = Column(Boolean, default=False)  # Featured review
    is_hidden = Column(Boolean, default=False)  # Hidden if inappropriate
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    
    # Relationships
    article = relationship("KnowledgeArticle", back_populates="ratings")


class SearchQuery(Base):
    """Search query logging and analytics"""
    __tablename__ = "km_search_queries"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    
    # Query Info
    query_code = Column(String(50), unique=True, nullable=False, index=True)  # QRY-001
    query_text = Column(String(500), nullable=False, index=True)
    normalized_query = Column(String(500))  # Lowercased, stemmed version
    
    # User
    user_id = Column(Integer, index=True)
    user_name = Column(String(200))
    user_role = Column(String(100))
    user_department = Column(String(100))
    
    # Search Context
    search_intent = Column(String(50))  # How_To, Troubleshooting, Definition, Policy
    search_type = Column(String(50))  # Keyword, Natural_Language, Advanced
    filters_used = Column(JSON)  # Category, date, author filters
    
    # Results
    results_count = Column(Integer)
    results_returned = Column(JSON)  # Top result IDs
    top_result_id = Column(Integer)  # Article ID of top result
    top_result_score = Column(Float)  # Relevance score
    
    # User Behavior
    clicked_result_id = Column(Integer)  # Which result was clicked
    clicked_position = Column(Integer)  # Position in results (1st, 2nd, etc.)
    time_to_click_seconds = Column(Integer)
    
    # Outcome
    found_answer = Column(Boolean)  # Did user find what they needed?
    refinement_needed = Column(Boolean)  # Did they search again?
    refinement_query = Column(String(500))  # Follow-up search
    
    # Performance
    search_duration_ms = Column(Integer)  # Time to return results
    algorithm_used = Column(String(50))  # Full_Text, Vector, Hybrid, AI
    
    # AI Features
    ai_suggestions = Column(JSON)  # AI-generated suggestions
    ai_answer = Column(Text)  # Direct AI-generated answer
    ai_confidence = Column(Float)  # 0-100%
    
    # Analytics
    is_zero_results = Column(Boolean, default=False)  # No results found
    is_popular_query = Column(Boolean, default=False)
    is_trending = Column(Boolean, default=False)
    
    # Session
    session_id = Column(String(100))  # User session
    search_sequence = Column(Integer)  # Search number in session
    
    # Geographic & Device
    ip_address = Column(String(50))
    country = Column(String(100))
    device_type = Column(String(50))  # Desktop, Mobile, Tablet
    browser = Column(String(100))
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
