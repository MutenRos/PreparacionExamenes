"""
Knowledge Management Module - Routes
REST API endpoints for knowledge articles, categories, and search
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from typing import List, Optional
from datetime import datetime

from dario_app.database import get_db
from dario_app.modules.knowledge_management.models import (
    KnowledgeArticle, ArticleCategory, ArticleVersion,
    ArticleRating, SearchQuery
)

router = APIRouter(prefix="/knowledge-management", tags=["Knowledge Management"])


# ============================================================================
# KNOWLEDGE ARTICLES
# ============================================================================

@router.post("/articles")
async def create_article(
    organization_id: int,
    title: str,
    content: str,
    category_id: Optional[int] = None,
    article_type: str = "How_To",
    author_name: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Create a knowledge article"""
    result = await db.execute(
        select(func.count(KnowledgeArticle.id)).where(
            KnowledgeArticle.organization_id == organization_id
        )
    )
    count = result.scalar() or 0
    article_code = f"ART-{count + 1:04d}"
    
    # Calculate word count
    word_count = len(content.split())
    
    article = KnowledgeArticle(
        organization_id=organization_id,
        category_id=category_id,
        article_code=article_code,
        title=title,
        content=content,
        content_length_words=word_count,
        article_type=article_type,
        author_name=author_name,
        created_by="system"
    )
    
    db.add(article)
    await db.commit()
    await db.refresh(article)
    return article


@router.get("/articles")
async def get_articles(
    organization_id: int,
    category_id: Optional[int] = None,
    status: Optional[str] = None,
    article_type: Optional[str] = None,
    featured: Optional[bool] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get knowledge articles with filters"""
    query = select(KnowledgeArticle).where(
        KnowledgeArticle.organization_id == organization_id
    )
    
    if category_id:
        query = query.where(KnowledgeArticle.category_id == category_id)
    if status:
        query = query.where(KnowledgeArticle.status == status)
    if article_type:
        query = query.where(KnowledgeArticle.article_type == article_type)
    if featured is not None:
        query = query.where(KnowledgeArticle.featured_article == featured)
    if search:
        # Simple search in title and content
        search_pattern = f"%{search}%"
        query = query.where(
            or_(
                KnowledgeArticle.title.ilike(search_pattern),
                KnowledgeArticle.content.ilike(search_pattern)
            )
        )
    
    query = query.order_by(KnowledgeArticle.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/articles/{article_id}")
async def get_article(article_id: int, db: AsyncSession = Depends(get_db)):
    """Get article details"""
    result = await db.execute(
        select(KnowledgeArticle).where(KnowledgeArticle.id == article_id)
    )
    article = result.scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Increment view count
    article.view_count += 1
    await db.commit()
    
    return article


@router.patch("/articles/{article_id}/publish")
async def publish_article(
    article_id: int,
    published_by: str,
    db: AsyncSession = Depends(get_db)
):
    """Publish an article"""
    result = await db.execute(
        select(KnowledgeArticle).where(KnowledgeArticle.id == article_id)
    )
    article = result.scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    article.status = "Published"
    article.is_published = True
    article.published_date = datetime.utcnow()
    article.published_by = published_by
    
    # Update category count
    if article.category_id:
        category_result = await db.execute(
            select(ArticleCategory).where(ArticleCategory.id == article.category_id)
        )
        category = category_result.scalar_one_or_none()
        if category:
            category.published_articles += 1
    
    await db.commit()
    await db.refresh(article)
    return article


@router.patch("/articles/{article_id}")
async def update_article(
    article_id: int,
    title: Optional[str] = None,
    content: Optional[str] = None,
    change_description: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Update an article (creates new version)"""
    result = await db.execute(
        select(KnowledgeArticle).where(KnowledgeArticle.id == article_id)
    )
    article = result.scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Create version snapshot before updating
    version_result = await db.execute(
        select(func.count(ArticleVersion.id)).where(
            ArticleVersion.article_id == article_id
        )
    )
    version_count = version_result.scalar() or 0
    version_code = f"VER-{article.article_code}-{version_count + 1:03d}"
    
    version = ArticleVersion(
        organization_id=article.organization_id,
        article_id=article_id,
        version_code=version_code,
        version=article.version,
        version_number=article.version_number,
        title=article.title,
        content=article.content,
        summary=article.summary,
        change_description=change_description,
        author_name=article.author_name,
        created_by="system"
    )
    db.add(version)
    
    # Update article
    if title:
        article.title = title
    if content:
        article.content = content
        article.content_length_words = len(content.split())
    
    # Increment version
    article.version_number += 1
    article.version = f"{article.version_number}.0"
    
    await db.commit()
    await db.refresh(article)
    return article


# ============================================================================
# ARTICLE CATEGORIES
# ============================================================================

@router.post("/categories")
async def create_category(
    organization_id: int,
    name: str,
    description: Optional[str] = None,
    parent_category_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """Create an article category"""
    result = await db.execute(
        select(func.count(ArticleCategory.id)).where(
            ArticleCategory.organization_id == organization_id
        )
    )
    count = result.scalar() or 0
    category_code = f"CAT-{count + 1:04d}"
    
    # Determine level
    level = 1
    if parent_category_id:
        parent_result = await db.execute(
            select(ArticleCategory).where(ArticleCategory.id == parent_category_id)
        )
        parent = parent_result.scalar_one_or_none()
        if parent:
            level = parent.level + 1
    
    category = ArticleCategory(
        organization_id=organization_id,
        parent_category_id=parent_category_id,
        category_code=category_code,
        name=name,
        description=description,
        level=level,
        created_by="system"
    )
    
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


@router.get("/categories")
async def get_categories(
    organization_id: int,
    parent_category_id: Optional[int] = None,
    is_featured: Optional[bool] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all categories"""
    query = select(ArticleCategory).where(
        ArticleCategory.organization_id == organization_id
    )
    
    if parent_category_id is not None:
        query = query.where(ArticleCategory.parent_category_id == parent_category_id)
    if is_featured is not None:
        query = query.where(ArticleCategory.is_featured == is_featured)
    
    query = query.order_by(ArticleCategory.sequence_order)
    result = await db.execute(query)
    return result.scalars().all()


# ============================================================================
# ARTICLE VERSIONS
# ============================================================================

@router.get("/articles/{article_id}/versions")
async def get_article_versions(article_id: int, db: AsyncSession = Depends(get_db)):
    """Get all versions of an article"""
    result = await db.execute(
        select(ArticleVersion).where(
            ArticleVersion.article_id == article_id
        ).order_by(ArticleVersion.version_number.desc())
    )
    return result.scalars().all()


@router.post("/articles/{article_id}/rollback/{version_id}")
async def rollback_article_version(
    article_id: int,
    version_id: int,
    rollback_reason: str,
    db: AsyncSession = Depends(get_db)
):
    """Rollback article to a previous version"""
    # Get article
    article_result = await db.execute(
        select(KnowledgeArticle).where(KnowledgeArticle.id == article_id)
    )
    article = article_result.scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Get version
    version_result = await db.execute(
        select(ArticleVersion).where(ArticleVersion.id == version_id)
    )
    version = version_result.scalar_one_or_none()
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    
    # Restore content from version
    article.title = version.title
    article.content = version.content
    article.summary = version.summary
    article.version = version.version
    article.version_number = version.version_number
    
    # Mark version as rolled back
    version.rolled_back = True
    version.rollback_date = datetime.utcnow()
    version.rollback_reason = rollback_reason
    
    await db.commit()
    await db.refresh(article)
    return article


# ============================================================================
# ARTICLE RATINGS
# ============================================================================

@router.post("/articles/{article_id}/ratings")
async def create_rating(
    article_id: int,
    organization_id: int,
    user_id: int,
    rating_value: int,
    was_helpful: bool,
    comment: Optional[str] = None,
    user_name: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Rate an article"""
    # Check if user already rated
    existing_result = await db.execute(
        select(ArticleRating).where(
            and_(
                ArticleRating.article_id == article_id,
                ArticleRating.user_id == user_id
            )
        )
    )
    if existing_result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User has already rated this article")
    
    result = await db.execute(
        select(func.count(ArticleRating.id)).where(
            ArticleRating.organization_id == organization_id
        )
    )
    count = result.scalar() or 0
    rating_code = f"RAT-{count + 1:04d}"
    
    rating = ArticleRating(
        organization_id=organization_id,
        article_id=article_id,
        rating_code=rating_code,
        user_id=user_id,
        user_name=user_name,
        rating_value=rating_value,
        was_helpful=was_helpful,
        comment=comment,
        created_by="system"
    )
    
    db.add(rating)
    
    # Update article stats
    article_result = await db.execute(
        select(KnowledgeArticle).where(KnowledgeArticle.id == article_id)
    )
    article = article_result.scalar_one_or_none()
    if article:
        article.total_ratings += 1
        if was_helpful:
            article.helpful_count += 1
        else:
            article.not_helpful_count += 1
        
        # Recalculate average rating
        ratings_result = await db.execute(
            select(func.avg(ArticleRating.rating_value)).where(
                ArticleRating.article_id == article_id
            )
        )
        avg_rating = ratings_result.scalar()
        article.average_rating = float(avg_rating) if avg_rating else 0
        
        # Recalculate helpfulness
        total = article.helpful_count + article.not_helpful_count
        if total > 0:
            article.helpfulness_percentage = (article.helpful_count / total) * 100
    
    await db.commit()
    await db.refresh(rating)
    return rating


@router.get("/articles/{article_id}/ratings")
async def get_article_ratings(
    article_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all ratings for an article"""
    result = await db.execute(
        select(ArticleRating).where(
            ArticleRating.article_id == article_id
        ).order_by(ArticleRating.created_at.desc())
    )
    return result.scalars().all()


# ============================================================================
# SEARCH
# ============================================================================

@router.post("/search")
async def search_articles(
    organization_id: int,
    query_text: str,
    user_id: Optional[int] = None,
    filters: Optional[dict] = None,
    db: AsyncSession = Depends(get_db)
):
    """Search knowledge articles"""
    start_time = datetime.utcnow()
    
    # Build search query
    search_pattern = f"%{query_text}%"
    query = select(KnowledgeArticle).where(
        and_(
            KnowledgeArticle.organization_id == organization_id,
            KnowledgeArticle.is_published == True,
            or_(
                KnowledgeArticle.title.ilike(search_pattern),
                KnowledgeArticle.content.ilike(search_pattern),
                KnowledgeArticle.summary.ilike(search_pattern)
            )
        )
    )
    
    # Apply filters if provided
    if filters:
        if "category_id" in filters:
            query = query.where(KnowledgeArticle.category_id == filters["category_id"])
        if "article_type" in filters:
            query = query.where(KnowledgeArticle.article_type == filters["article_type"])
    
    # Order by relevance (simplified - in production use full-text search)
    query = query.order_by(KnowledgeArticle.view_count.desc())
    
    result = await db.execute(query)
    articles = result.scalars().all()
    
    end_time = datetime.utcnow()
    duration_ms = int((end_time - start_time).total_seconds() * 1000)
    
    # Log search query
    query_result = await db.execute(
        select(func.count(SearchQuery.id)).where(
            SearchQuery.organization_id == organization_id
        )
    )
    count = query_result.scalar() or 0
    query_code = f"QRY-{count + 1:04d}"
    
    search_log = SearchQuery(
        organization_id=organization_id,
        query_code=query_code,
        query_text=query_text,
        user_id=user_id,
        results_count=len(articles),
        search_duration_ms=duration_ms,
        top_result_id=articles[0].id if articles else None,
        is_zero_results=(len(articles) == 0),
        created_by="system"
    )
    db.add(search_log)
    await db.commit()
    
    return {
        "query": query_text,
        "results_count": len(articles),
        "duration_ms": duration_ms,
        "articles": articles
    }


@router.get("/analytics/knowledge-dashboard")
async def get_knowledge_dashboard(
    organization_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get knowledge base analytics"""
    # Total articles
    articles_result = await db.execute(
        select(
            func.count(KnowledgeArticle.id),
            func.sum(KnowledgeArticle.view_count),
            func.avg(KnowledgeArticle.average_rating)
        ).where(KnowledgeArticle.organization_id == organization_id)
    )
    total_articles, total_views, avg_rating = articles_result.first()
    
    # Published articles
    published_result = await db.execute(
        select(func.count(KnowledgeArticle.id)).where(
            and_(
                KnowledgeArticle.organization_id == organization_id,
                KnowledgeArticle.is_published == True
            )
        )
    )
    published_articles = published_result.scalar() or 0
    
    # Popular articles
    popular_result = await db.execute(
        select(KnowledgeArticle).where(
            KnowledgeArticle.organization_id == organization_id
        ).order_by(KnowledgeArticle.view_count.desc()).limit(5)
    )
    popular_articles = popular_result.scalars().all()
    
    return {
        "total_articles": total_articles or 0,
        "published_articles": published_articles,
        "total_views": total_views or 0,
        "avg_rating": float(avg_rating) if avg_rating else 0,
        "popular_articles": [
            {
                "title": a.title,
                "views": a.view_count,
                "rating": a.average_rating
            } for a in popular_articles
        ]
    }
