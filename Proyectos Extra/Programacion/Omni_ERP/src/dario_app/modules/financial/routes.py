"""Financial Management API routes - Budgets, Bank Reconciliation, Deferrals, Cash Flow."""

from datetime import datetime
from typing import List, Optional
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import require_permission, get_tenant_db, get_org_id
from dario_app.modules.usuarios.models import Usuario
from .models import (
    FinancialDimension, Budget, BudgetActual, BankAccount, BankStatement,
    BankTransaction, Deferral, DeferralSchedule, CashFlowForecast,
    SEPARemittance, SEPARemittanceLine
)
from .service import FinancialService


router = APIRouter(prefix="/api/financial", tags=["Financial Management"])


# ========== SCHEMAS ==========

class FinancialDimensionCreate(BaseModel):
    dimension_type: str
    dimension_code: str
    dimension_name: str
    parent_id: Optional[int] = None
    manager_id: Optional[int] = None


class BudgetCreate(BaseModel):
    budget_name: str
    fiscal_year: int
    period: str
    start_date: datetime
    end_date: datetime
    dimension_id: Optional[int] = None
    revenue_budget: Decimal = Decimal("0")
    expense_budget: Decimal = Decimal("0")
    capex_budget: Decimal = Decimal("0")


class BankAccountCreate(BaseModel):
    account_name: str
    account_number: str
    iban: Optional[str] = None
    bank_name: str
    currency: str = "EUR"


class BankStatementCreate(BaseModel):
    bank_account_id: int
    statement_date: datetime
    opening_balance: Decimal
    closing_balance: Decimal


class BankTransactionCreate(BaseModel):
    transaction_date: datetime
    amount: Decimal
    transaction_type: str
    reference: Optional[str] = None
    description: Optional[str] = None
    counterparty_name: Optional[str] = None


class DeferralCreate(BaseModel):
    deferral_type: str
    source_type: Optional[str] = None
    source_id: Optional[int] = None
    total_amount: Decimal
    start_date: datetime
    end_date: datetime
    descripcion: Optional[str] = None


class SEPARemittanceLineCreate(BaseModel):
    debtor_name: str
    iban: str
    bic: Optional[str] = None
    amount: Decimal
    concept: Optional[str] = None
    reference: Optional[str] = None
    mandate_reference: Optional[str] = None
    mandate_date: Optional[datetime] = None


class SEPARemittanceCreate(BaseModel):
    bank_account_id: int
    execution_date: datetime
    scheme: str = "CORE"  # CORE or B2B
    description: Optional[str] = None
    lines: List[SEPARemittanceLineCreate]


# ========== FINANCIAL DIMENSIONS ==========

@router.post("/dimensions")
async def create_dimension(
    dim_data: FinancialDimensionCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("financial.dimensions.create")),
    org_id: int = Depends(get_org_id)
):
    """Create a financial dimension."""
    dimension = FinancialDimension(organization_id=org_id, **dim_data.model_dump())
    db.add(dimension)
    await db.commit()
    await db.refresh(dimension)
    return dimension


@router.get("/dimensions")
async def list_dimensions(
    dimension_type: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("financial.dimensions.read")),
    org_id: int = Depends(get_org_id)
):
    """List financial dimensions."""
    query = select(FinancialDimension).where(FinancialDimension.organization_id == org_id)
    if dimension_type:
        query = query.where(FinancialDimension.dimension_type == dimension_type)
    result = await db.execute(query)
    return result.scalars().all()


# ========== BUDGETS ==========

@router.post("/budgets")
async def create_budget(
    budget_data: BudgetCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("financial.budgets.create")),
    org_id: int = Depends(get_org_id)
):
    """Create a budget."""
    
    # Get dimension name if provided
    dimension_name = None
    dimension_code = None
    if budget_data.dimension_id:
        stmt = select(FinancialDimension).where(FinancialDimension.id == budget_data.dimension_id)
        result = await db.execute(stmt)
        dimension = result.scalar_one_or_none()
        if dimension:
            dimension_name = dimension.dimension_name
            dimension_code = dimension.dimension_code
    
    budget = Budget(
        organization_id=org_id,
        dimension_code=dimension_code,
        dimension_name=dimension_name,
        **budget_data.model_dump()
    )
    db.add(budget)
    await db.commit()
    await db.refresh(budget)
    return budget


@router.get("/budgets")
async def list_budgets(
    fiscal_year: Optional[int] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("financial.budgets.read")),
    org_id: int = Depends(get_org_id)
):
    """List budgets."""
    query = select(Budget).where(Budget.organization_id == org_id)
    if fiscal_year:
        query = query.where(Budget.fiscal_year == fiscal_year)
    if status:
        query = query.where(Budget.status == status)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/budgets/{budget_id}/calculate-actuals")
async def calculate_budget_actuals(
    budget_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("financial.budgets.calculate")),
    org_id: int = Depends(get_org_id)
):
    """Calculate budget vs actuals."""
    result = await FinancialService.calculate_budget_actuals(db, org_id, budget_id)
    return result


@router.get("/budgets/{budget_id}/actuals")
async def get_budget_actuals(
    budget_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("financial.budgets.read")),
    org_id: int = Depends(get_org_id)
):
    """Get budget actuals."""
    stmt = select(BudgetActual).where(BudgetActual.budget_id == budget_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# ========== BANK ACCOUNTS ==========

@router.post("/bank-accounts")
async def create_bank_account(
    account_data: BankAccountCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("financial.bank.create")),
    org_id: int = Depends(get_org_id)
):
    """Create a bank account."""
    account = BankAccount(organization_id=org_id, **account_data.model_dump())
    db.add(account)
    await db.commit()
    await db.refresh(account)
    return account


@router.get("/bank-accounts")
async def list_bank_accounts(
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("financial.bank.read")),
    org_id: int = Depends(get_org_id)
):
    """List bank accounts."""
    stmt = select(BankAccount).where(BankAccount.organization_id == org_id)
    result = await db.execute(stmt)
    return result.scalars().all()


# ========== BANK RECONCILIATION ==========

@router.post("/bank-statements")
async def create_bank_statement(
    statement_data: BankStatementCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("financial.bank.reconcile")),
    org_id: int = Depends(get_org_id)
):
    """Import a bank statement."""
    statement = BankStatement(
        organization_id=org_id,
        imported_by_user_id=user.id,
        imported_by_user_name=user.nombre_completo,
        **statement_data.model_dump()
    )
    db.add(statement)
    await db.commit()
    await db.refresh(statement)
    return statement


@router.post("/bank-statements/{statement_id}/transactions")
async def add_bank_transaction(
    statement_id: int,
    trans_data: BankTransactionCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("financial.bank.reconcile")),
    org_id: int = Depends(get_org_id)
):
    """Add a transaction to a bank statement."""
    
    # Verify statement exists
    stmt = select(BankStatement).where(
        BankStatement.id == statement_id,
        BankStatement.organization_id == org_id
    )
    result = await db.execute(stmt)
    statement = result.scalar_one_or_none()
    
    if not statement:
        raise HTTPException(status_code=404, detail="Bank statement not found")
    
    transaction = BankTransaction(
        organization_id=org_id,
        bank_statement_id=statement_id,
        bank_account_id=statement.bank_account_id,
        **trans_data.model_dump()
    )
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    return transaction


@router.post("/bank-statements/{statement_id}/auto-match")
async def auto_match_transactions(
    statement_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("financial.bank.reconcile")),
    org_id: int = Depends(get_org_id)
):
    """Auto-match bank transactions with invoices."""
    result = await FinancialService.auto_match_bank_transactions(db, org_id, statement_id)
    return result


@router.get("/bank-statements/{statement_id}/transactions")
async def get_statement_transactions(
    statement_id: int,
    reconciliation_status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("financial.bank.read")),
    org_id: int = Depends(get_org_id)
):
    """Get transactions for a bank statement."""
    query = select(BankTransaction).where(
        BankTransaction.bank_statement_id == statement_id,
        BankTransaction.organization_id == org_id
    )
    if reconciliation_status:
        query = query.where(BankTransaction.reconciliation_status == reconciliation_status)
    result = await db.execute(query)
    return result.scalars().all()


# ========== DEFERRALS ==========

@router.post("/deferrals")
async def create_deferral(
    deferral_data: DeferralCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("financial.deferrals.create")),
    org_id: int = Depends(get_org_id)
):
    """Create a deferral/accrual."""
    deferral = Deferral(
        organization_id=org_id,
        remaining_amount=deferral_data.total_amount,
        **deferral_data.model_dump()
    )
    db.add(deferral)
    await db.commit()
    await db.refresh(deferral)
    return deferral


@router.post("/deferrals/{deferral_id}/create-schedule")
async def create_deferral_schedule(
    deferral_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("financial.deferrals.create")),
    org_id: int = Depends(get_org_id)
):
    """Create amortization schedule for a deferral."""
    schedule = await FinancialService.create_deferral_schedule(db, org_id, deferral_id)
    return {"schedule_items": len(schedule)}


@router.get("/deferrals/{deferral_id}/schedule")
async def get_deferral_schedule(
    deferral_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("financial.deferrals.read")),
    org_id: int = Depends(get_org_id)
):
    """Get deferral schedule."""
    stmt = select(DeferralSchedule).where(DeferralSchedule.deferral_id == deferral_id)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/deferrals/recognize")
async def recognize_deferrals(
    up_to_date: datetime,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("financial.deferrals.recognize")),
    org_id: int = Depends(get_org_id)
):
    """Recognize deferrals up to a specific date."""
    result = await FinancialService.recognize_deferrals(db, org_id, up_to_date)
    return result


@router.get("/deferrals")
async def list_deferrals(
    status: Optional[str] = None,
    deferral_type: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("financial.deferrals.read")),
    org_id: int = Depends(get_org_id)
):
    """List deferrals."""
    query = select(Deferral).where(Deferral.organization_id == org_id)
    if status:
        query = query.where(Deferral.status == status)
    if deferral_type:
        query = query.where(Deferral.deferral_type == deferral_type)
    result = await db.execute(query)
    return result.scalars().all()


# ========== CASH FLOW ==========

@router.post("/cash-flow/forecast")
async def calculate_cash_flow_forecast(
    forecast_date: datetime,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("financial.cashflow.calculate")),
    org_id: int = Depends(get_org_id)
):
    """Calculate cash flow forecast."""
    forecast = await FinancialService.calculate_cash_flow_forecast(
        db, org_id, forecast_date, user.id
    )
    return forecast


@router.get("/cash-flow/forecasts")
async def list_cash_flow_forecasts(
    limit: int = 30,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("financial.cashflow.read")),
    org_id: int = Depends(get_org_id)
):
    """List cash flow forecasts."""
    stmt = select(CashFlowForecast).where(
        CashFlowForecast.organization_id == org_id
    ).order_by(CashFlowForecast.forecast_date.desc()).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


# ========== SEPA REMITTANCES ==========

@router.post("/sepa/remittances")
async def create_sepa_remittance(
    remittance_data: SEPARemittanceCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("financial.sepa.create")),
    org_id: int = Depends(get_org_id)
):
    """Create a SEPA remittance."""
    # Generate remittance ID
    count_stmt = select(func.count()).select_from(SEPARemittance).where(SEPARemittance.organization_id == org_id)
    result = await db.execute(count_stmt)
    count = result.scalar_one()
    remittance_ref = f"REM-{datetime.utcnow().year}-{count + 1:04d}"

    # Create header
    remittance = SEPARemittance(
        organization_id=org_id,
        remittance_id=remittance_ref,
        bank_account_id=remittance_data.bank_account_id,
        execution_date=remittance_data.execution_date,
        scheme=remittance_data.scheme,
        description=remittance_data.description,
        status="draft",
        total_amount=sum(line.amount for line in remittance_data.lines),
        created_by_user_id=user.id
    )
    db.add(remittance)
    await db.flush()  # Get ID
    
    # Create lines
    for line_data in remittance_data.lines:
        line = SEPARemittanceLine(
            organization_id=org_id,
            remittance_id=remittance.id,
            debtor_name=line_data.debtor_name,
            debtor_iban=line_data.iban,
            debtor_bic=line_data.bic,
            amount=line_data.amount,
            concept=line_data.concept or "Payment",
            mandate_reference=line_data.mandate_reference or f"MND-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            mandate_date=line_data.mandate_date or datetime.utcnow()
        )
        db.add(line)
        
    await db.commit()
    await db.refresh(remittance)
    return remittance


@router.get("/sepa/remittances")
async def list_sepa_remittances(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("financial.sepa.read")),
    org_id: int = Depends(get_org_id)
):
    """List SEPA remittances."""
    query = select(SEPARemittance).where(SEPARemittance.organization_id == org_id)
    if status:
        query = query.where(SEPARemittance.status == status)
    query = query.order_by(SEPARemittance.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/sepa/remittances/{remittance_id}")
async def get_sepa_remittance(
    remittance_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("financial.sepa.read")),
    org_id: int = Depends(get_org_id)
):
    """Get SEPA remittance details."""
    stmt = select(SEPARemittance).where(
        SEPARemittance.id == remittance_id,
        SEPARemittance.organization_id == org_id
    )
    result = await db.execute(stmt)
    remittance = result.scalar_one_or_none()
    if not remittance:
        raise HTTPException(status_code=404, detail="Remittance not found")
    return remittance


@router.post("/sepa/remittances/{remittance_id}/generate-xml")
async def generate_sepa_xml(
    remittance_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("financial.sepa.generate")),
    org_id: int = Depends(get_org_id)
):
    """Generate SEPA XML for a remittance."""
    try:
        xml_content = await FinancialService.generate_sepa_xml(db, remittance_id, org_id)
        return {"xml_content": xml_content}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ========== SMART EXPENSES (OCR) ==========

from fastapi import UploadFile, File
import shutil
import os

@router.post("/expenses/upload")
async def upload_expense_receipt(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("financial.expenses.create")),
    org_id: int = Depends(get_org_id)
):
    """Upload a receipt image for OCR processing."""
    # Save file temporarily
    upload_dir = f"/tmp/uploads/{org_id}"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = f"{upload_dir}/{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Process
    receipt = await FinancialService.process_receipt_image(
        db, org_id, user.id, file_path, file.filename
    )
    
    return receipt


@router.get("/expenses")
async def list_expenses(
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("financial.expenses.read")),
    org_id: int = Depends(get_org_id)
):
    """List processed expenses."""
    from .models import ExpenseReceipt
    stmt = select(ExpenseReceipt).where(
        ExpenseReceipt.organization_id == org_id
    ).order_by(ExpenseReceipt.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/sepa/remittances/{remittance_id}/generate-xml")
async def generate_sepa_xml(
    remittance_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("financial.sepa.generate")),
    org_id: int = Depends(get_org_id)
):
    """Generate SEPA XML for a remittance."""
    try:
        xml_content = await FinancialService.generate_sepa_xml(db, remittance_id, org_id)
        return {"xml_content": xml_content}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
