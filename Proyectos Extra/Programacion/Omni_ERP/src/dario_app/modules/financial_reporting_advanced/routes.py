"""Advanced Financial Reporting Routes - Consolidation & IFRS."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from dario_app.database import get_db
from dario_app.modules.financial_reporting_advanced import models
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api/financial-reporting", tags=["financial_reporting"])


# Pydantic Schemas
class ReportTemplateCreate(BaseModel):
    template_name: str
    report_type: str
    reporting_standard: str
    period_type: str


class ConsolidationGroupCreate(BaseModel):
    group_name: str
    group_type: str
    consolidation_method: str
    ownership_percentage: Optional[float] = None


class IntercompanyTransactionCreate(BaseModel):
    entity_id: int
    transaction_type: str
    source_entity_id: int
    target_entity_id: int
    transaction_amount: float


# Report Template Endpoints
@router.post("/templates")
async def create_report_template(
    template: ReportTemplateCreate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Create a financial report template."""
    db_template = models.FinancialReportTemplate(
        organization_id=organization_id,
        template_name=template.template_name,
        report_type=template.report_type,
        reporting_standard=template.reporting_standard,
        period_type=template.period_type,
    )
    db.add(db_template)
    await db.commit()
    await db.refresh(db_template)
    return {"id": db_template.id, "template_name": db_template.template_name}


@router.get("/templates")
async def list_report_templates(
    organization_id: int = Query(...),
    report_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List report templates."""
    query = db.query(models.FinancialReportTemplate).filter(
        models.FinancialReportTemplate.organization_id == organization_id
    )
    
    if report_type:
        query = query.filter(models.FinancialReportTemplate.report_type == report_type)
    
    templates = await query.all()
    return {"templates": templates, "total": len(templates)}


# Generated Reports Endpoints
@router.post("/reports")
async def generate_report(
    template_id: int,
    report_period: str,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Generate a financial report."""
    template = await db.query(models.FinancialReportTemplate).filter(
        models.FinancialReportTemplate.id == template_id,
        models.FinancialReportTemplate.organization_id == organization_id
    ).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    report = models.GeneratedReport(
        organization_id=organization_id,
        template_id=template_id,
        report_name=f"{template.template_name}_{report_period}",
        report_period=report_period,
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)
    return {"id": report.id, "report_period": report.report_period, "status": "generated"}


@router.get("/reports")
async def list_reports(
    organization_id: int = Query(...),
    report_period: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List generated reports."""
    query = db.query(models.GeneratedReport).filter(
        models.GeneratedReport.organization_id == organization_id
    )
    
    if report_period:
        query = query.filter(models.GeneratedReport.report_period == report_period)
    
    reports = await query.all()
    return {"reports": reports, "total": len(reports)}


@router.put("/reports/{report_id}/approve")
async def approve_report(
    report_id: int,
    approved_by: str,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Approve a financial report."""
    report = await db.query(models.GeneratedReport).filter(
        models.GeneratedReport.id == report_id,
        models.GeneratedReport.organization_id == organization_id
    ).first()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    report.signed_off = True
    report.approved_by = approved_by
    report.approval_date = datetime.utcnow()
    await db.commit()
    return {"id": report.id, "status": "approved"}


# Consolidation Endpoints
@router.post("/consolidation-groups")
async def create_consolidation_group(
    group: ConsolidationGroupCreate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Create a consolidation group."""
    db_group = models.ConsolidationGroup(
        organization_id=organization_id,
        group_name=group.group_name,
        group_type=group.group_type,
        consolidation_method=group.consolidation_method,
        ownership_percentage=group.ownership_percentage,
    )
    db.add(db_group)
    await db.commit()
    await db.refresh(db_group)
    return {"id": db_group.id, "group_name": db_group.group_name}


@router.get("/consolidation-groups")
async def list_consolidation_groups(
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """List consolidation groups."""
    groups = await db.query(models.ConsolidationGroup).filter(
        models.ConsolidationGroup.organization_id == organization_id
    ).all()
    return {"groups": groups, "total": len(groups)}


# Intercompany Transactions Endpoints
@router.post("/intercompany-transactions")
async def create_intercompany_transaction(
    transaction: IntercompanyTransactionCreate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Record intercompany transaction."""
    db_transaction = models.IntercompanyTransaction(
        organization_id=organization_id,
        entity_id=transaction.entity_id,
        transaction_type=transaction.transaction_type,
        source_entity_id=transaction.source_entity_id,
        target_entity_id=transaction.target_entity_id,
        transaction_amount=transaction.transaction_amount,
    )
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return {"id": db_transaction.id, "status": "pending"}


@router.get("/intercompany-transactions")
async def get_intercompany_transactions(
    organization_id: int = Query(...),
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get intercompany transactions."""
    query = db.query(models.IntercompanyTransaction).filter(
        models.IntercompanyTransaction.organization_id == organization_id
    )
    
    if status:
        query = query.filter(models.IntercompanyTransaction.status == status)
    
    transactions = await query.all()
    return {"transactions": transactions, "total": len(transactions)}


# Variance Analysis Endpoints
@router.get("/variance-analysis")
async def get_variance_analysis(
    organization_id: int = Query(...),
    variance_period: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get variance analysis."""
    query = db.query(models.ReportingVariance).filter(
        models.ReportingVariance.organization_id == organization_id
    )
    
    if variance_period:
        query = query.filter(models.ReportingVariance.variance_period == variance_period)
    
    variances = await query.all()
    
    total_variance = sum([v.variance_amount for v in variances])
    favorable_count = sum([1 for v in variances if v.variance_category == "favorable"])
    
    return {
        "variances": variances,
        "total": len(variances),
        "total_variance_amount": total_variance,
        "favorable_count": favorable_count,
    }


# Segment Reporting Endpoints
@router.get("/segment-reporting")
async def get_segment_reporting(
    organization_id: int = Query(...),
    reporting_period: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get segment reporting."""
    query = db.query(models.SegmentReporting).filter(
        models.SegmentReporting.organization_id == organization_id
    )
    
    if reporting_period:
        query = query.filter(models.SegmentReporting.reporting_period == reporting_period)
    
    segments = await query.all()
    
    total_revenue = sum([s.revenue for s in segments if s.revenue])
    total_profit = sum([s.operating_profit for s in segments if s.operating_profit])
    
    return {
        "segments": segments,
        "total": len(segments),
        "total_revenue": total_revenue,
        "total_operating_profit": total_profit,
    }


# Health Check
@router.get("/health")
async def health_check():
    """Check financial reporting module health."""
    return {
        "status": "healthy",
        "module": "financial_reporting_advanced",
        "version": "1.0.0",
        "features": [
            "Financial Report Templates",
            "Automated Report Generation",
            "Consolidation Management",
            "IFRS Compliance",
            "Intercompany Elimination",
            "Variance Analysis",
            "Segment Reporting",
            "Audit Trail"
        ]
    }
